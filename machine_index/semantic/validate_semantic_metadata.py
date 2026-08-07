#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, xml.etree.ElementTree as ET
from urllib.parse import urlparse

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
BASE='https://krytrondwayne.github.io/Quantum-K-Field/'
errors=[]; warnings=[]; parsed=0

def valid_http_uri(value):
    try:
        u=urlparse(value); return u.scheme in ('http','https') and bool(u.netloc)
    except Exception: return False

for p in ROOT.rglob('*'):
    if p.is_file() and (p.suffix=='.json' or p.suffix=='.jsonld'):
        try:
            json.loads(p.read_text(encoding='utf-8')); parsed+=1
        except Exception as e: errors.append(f'JSON parse failure {p.relative_to(ROOT)}: {e}')

script_re=re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',re.I|re.S)
canon_re=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',re.I)
html_count=0; jsonld_blocks=0; canonicals=[]
for p in ROOT.rglob('index.html'):
    text=p.read_text(encoding='utf-8'); html_count+=1
    cs=canon_re.findall(text)
    if len(cs)!=1: errors.append(f'{p.relative_to(ROOT)}: expected exactly one canonical URL, found {len(cs)}')
    elif not cs[0].startswith(BASE): errors.append(f'{p.relative_to(ROOT)}: canonical URL outside canonical archive base: {cs[0]}')
    else: canonicals.append(cs[0])
    blocks=script_re.findall(text)
    if len(blocks)!=1: errors.append(f'{p.relative_to(ROOT)}: expected exactly one embedded JSON-LD block, found {len(blocks)}')
    for block in blocks:
        try:
            obj=json.loads(block); jsonld_blocks+=1
            if '@context' not in obj or '@graph' not in obj: errors.append(f'{p.relative_to(ROOT)}: JSON-LD must contain @context and @graph')
        except Exception as e: errors.append(f'{p.relative_to(ROOT)}: invalid embedded JSON-LD: {e}')
    if 'KFIELD-JSONLD:START' not in text or 'KFIELD-JSONLD:END' not in text: errors.append(f'{p.relative_to(ROOT)}: semantic regeneration markers missing')
    if 'variablesMeasured' in text: errors.append(f'{p.relative_to(ROOT)}: legacy variablesMeasured spelling found')

for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix in ('.json','.jsonld','.html'):
        try:
            if 'variablesMeasured' in p.read_text(encoding='utf-8'): errors.append(f'{p.relative_to(ROOT)}: legacy variablesMeasured spelling found')
        except UnicodeDecodeError: pass

catalog=json.loads((HERE/'dataset-catalog.jsonld').read_text(encoding='utf-8'))
dataset_ids=[]
for node in catalog.get('@graph',[]):
    types=node.get('@type',[]); types=[types] if isinstance(types,str) else types
    if 'schema:Dataset' in types:
        dataset_ids.append(node.get('@id'))
        for key in ('schema:name','schema:description','schema:url','schema:creator','dcterms:license','dcat:inCatalog'):
            if key not in node: errors.append(f"Dataset {node.get('@id')} missing {key}")
        name=node.get('schema:name',''); desc=node.get('schema:description','')
        if not isinstance(name,str) or not name.strip(): errors.append(f"Dataset {node.get('@id')} has empty name")
        if not isinstance(desc,str) or not (50 <= len(desc) <= 5000): errors.append(f"Dataset {node.get('@id')} description length outside 50..5000 characters")
if len(dataset_ids)!=len(set(dataset_ids)): errors.append('Duplicate Dataset @id values in dataset catalog')

ontology=json.loads((HERE/'ontology-mappings.json').read_text(encoding='utf-8'))
for m in ontology.get('field_mappings',[]):
    if not valid_http_uri(m.get('external_uri','')): errors.append(f"Invalid field mapping URI for {m.get('internal_key')}: {m.get('external_uri')}")
fieldref=json.loads((HERE/'field-reference.json').read_text(encoding='utf-8'))
for key,rec in fieldref.get('fields',{}).items():
    for x in rec.get('external_terms',[]):
        if not valid_http_uri(x.get('uri','')): errors.append(f'Invalid field-reference URI for {key}: {x.get("uri")}')
    for ukey in ('quantity_kind','unit','reference_frame'):
        if ukey in rec and not valid_http_uri(rec[ukey]): errors.append(f'Invalid {ukey} URI for {key}: {rec[ukey]}')

manifest=json.loads((HERE/'index.json').read_text(encoding='utf-8'))
for label,rel in manifest.get('files',{}).items():
    target=HERE/rel
    if not target.exists(): errors.append(f'Semantic manifest file reference missing ({label}): {rel}')
for dp in manifest.get('dataset_profiles',[]):
    target=HERE/dp['jsonld']
    if not target.exists(): errors.append(f'Dataset profile missing: {dp["jsonld"]}')
    if not dp['canonical_landing_page'].startswith(BASE): errors.append(f'Dataset landing page outside canonical base: {dp["canonical_landing_page"]}')

registry=json.loads((HERE/'page-metadata.json').read_text(encoding='utf-8'))
registry_urls=[]
for rec in registry.get('pages',[]):
    registry_urls.append(rec['canonical_url'])
    hp=ROOT/'index.html' if rec['path']=='/' else ROOT/rec['path'].strip('/')/'index.html'
    if not hp.exists(): errors.append(f'Page registry target missing: {rec["path"]}')
if len(registry_urls)!=len(set(registry_urls)): errors.append('Duplicate canonical URL in page registry')

try:
    tree=ET.parse(ROOT/'sitemap.xml'); ns={'sm':'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sm_urls=[x.text for x in tree.findall('.//sm:loc',ns)]
    if len(sm_urls)!=len(set(sm_urls)): errors.append('Duplicate URL in sitemap.xml')
    missing=sorted(set(registry_urls)-set(sm_urls))
    if missing: errors.append('Sitemap missing registered landing pages: '+', '.join(missing))
except Exception as e: errors.append(f'sitemap.xml parse failure: {e}')

print(f'Parsed JSON/JSON-LD files: {parsed}')
print(f'HTML landing pages: {html_count}; valid embedded JSON-LD blocks: {jsonld_blocks}')
print(f'Dataset profiles: {len(dataset_ids)}; field references: {len(fieldref.get("fields",{}))}')
print(f'Warnings: {len(warnings)}; Errors: {len(errors)}')
for x in warnings: print('WARNING:',x)
for x in errors: print('ERROR:',x)
sys.exit(1 if errors else 0)
