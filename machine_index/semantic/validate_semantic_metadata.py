#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys, xml.etree.ElementTree as ET
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = 'https://krytrondwayne.github.io/Quantum-K-Field/'
SNAPSHOT_COMMIT = 'de76315a0e7ef5f0d76d2bdbb90184bb8b0ae6fb'
SNAPSHOT_TREE = 'f730312eaf489d103f54d29aba40915fca5a2973'
PACKAGE_ONLY = {'UPLOAD_INSTRUCTIONS.md','UPLOAD_MANIFEST.json','VALIDATION_REPORT.txt','SHA256SUMS.semantic-upgrade'}
errors=[]; warnings=[]; parsed=0

def valid_http_uri(value):
    try:
        u=urlparse(value); return u.scheme in ('http','https') and bool(u.netloc)
    except Exception: return False

def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def git_blob_sha(path):
    data=path.read_bytes()
    header=f'blob {len(data)}\0'.encode('ascii')
    return hashlib.sha1(header+data).hexdigest()

def verify_checksum_file(path):
    if not path.exists():
        errors.append(f'Missing checksum file: {path.relative_to(ROOT)}'); return
    for lineno,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip() or line.lstrip().startswith('#'): continue
        m=re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not m:
            errors.append(f'{path.relative_to(ROOT)}:{lineno}: malformed checksum line'); continue
        expected,rel=m.groups(); target=ROOT/rel
        if not target.exists(): errors.append(f'{path.relative_to(ROOT)}:{lineno}: missing target {rel}')
        elif sha256(target)!=expected: errors.append(f'{path.relative_to(ROOT)}:{lineno}: checksum mismatch {rel}')

for p in ROOT.rglob('*'):
    try:
        is_file=p.is_file()
    except OSError:
        continue
    if is_file and (p.suffix=='.json' or p.suffix=='.jsonld'):
        try: json.loads(p.read_text(encoding='utf-8')); parsed+=1
        except Exception as e: errors.append(f'JSON parse failure {p.relative_to(ROOT)}: {e}')

script_re=re.compile(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>',re.I|re.S)
canon_re=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']',re.I)
html_count=0; jsonld_blocks=0
for p in ROOT.rglob('index.html'):
    text=p.read_text(encoding='utf-8'); html_count+=1
    cs=canon_re.findall(text)
    if len(cs)!=1: errors.append(f'{p.relative_to(ROOT)}: expected exactly one canonical URL, found {len(cs)}')
    elif not cs[0].startswith(BASE): errors.append(f'{p.relative_to(ROOT)}: canonical URL outside canonical archive base: {cs[0]}')
    blocks=script_re.findall(text)
    if len(blocks)!=1: errors.append(f'{p.relative_to(ROOT)}: expected exactly one static JSON-LD block, found {len(blocks)}')
    for block in blocks:
        try:
            obj=json.loads(block); jsonld_blocks+=1
            if '@context' not in obj or '@graph' not in obj: errors.append(f'{p.relative_to(ROOT)}: JSON-LD must contain @context and @graph')
        except Exception as e: errors.append(f'{p.relative_to(ROOT)}: invalid embedded JSON-LD: {e}')
    if 'KFIELD-JSONLD:START' not in text or 'KFIELD-JSONLD:END' not in text: errors.append(f'{p.relative_to(ROOT)}: semantic regeneration markers missing')
    if 'variablesMeasured' in text: errors.append(f'{p.relative_to(ROOT)}: legacy variablesMeasured spelling found')

shared_js=ROOT/'Assets/kfield-directory-index.js'
if not shared_js.exists(): errors.append('Missing Assets/kfield-directory-index.js')
else:
    jt=shared_js.read_text(encoding='utf-8')
    for token in ['installStructuredData','application/ld+json','document.createElement("script")',"document.createElement('script')"]:
        if token in jt: errors.append(f'Runtime structured-data injection remains in Assets/kfield-directory-index.js: {token}')

assets=ROOT/'Assets/index.html'
if assets.exists():
    at=assets.read_text(encoding='utf-8')
    for name in ('kfield-directory-index.css','kfield-directory-index.js'):
        if name not in at: errors.append(f'Assets/index.html fallback exclusion missing: {name}')

for p in ROOT.rglob('*'):
    try:
        is_file=p.is_file()
    except OSError:
        continue
    if is_file and p.suffix in ('.json','.jsonld','.html'):
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

for dp in (HERE/'datasets').glob('*.jsonld'):
    obj=json.loads(dp.read_text(encoding='utf-8'))
    for node in obj.get('@graph',[]):
        types=node.get('@type',[]); types=[types] if isinstance(types,str) else types
        if 'dcat:Distribution' in types and 'dcterms:license' not in node:
            errors.append(f'{dp.relative_to(ROOT)}: dcat:Distribution missing dcterms:license')

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

mi=json.loads((ROOT/'machine_index/index.json').read_text(encoding='utf-8'))
core=json.loads((ROOT/'machine_index/core.json').read_text(encoding='utf-8'))['payload']
for label,obj in [('manifest',mi.get('repository_snapshot',{})),('core',core.get('repository_snapshot',{}))]:
    if obj.get('head_commit_sha_observed')!=SNAPSHOT_COMMIT: errors.append(f'{label}: incorrect snapshot commit SHA')
    if obj.get('tree_sha_observed')!=SNAPSHOT_TREE: errors.append(f'{label}: incorrect snapshot tree SHA')
    if obj.get('tree_sha_observed')==obj.get('head_commit_sha_observed'): errors.append(f'{label}: commit SHA incorrectly reused as tree SHA')
if core.get('integrity',{}).get('snapshot_tree_sha')!=SNAPSHOT_TREE: errors.append('core integrity snapshot_tree_sha missing or incorrect')

tax=json.loads((ROOT/'machine_index/taxonomy/14-named-k-field-structures.json').read_text(encoding='utf-8'))
taxrec={r.get('id'):r for r in tax.get('records',[])}
expected_devon='Archive name for the compact direct/reciprocal algebraic metric representation constructed from Cell3; dimension is historical terminology rather than an extra spatial dimension.'
if taxrec.get('devon-dimension',{}).get('definition')!=expected_devon: errors.append('Devon Dimension definition drift between canonical taxonomy and semantic vocabulary')
if 'Emily Eigenspectrum' not in taxrec.get('emily-eigen-spectrum',{}).get('aliases',[]): errors.append('Emily Eigenspectrum alias missing from canonical taxonomy')
kv=json.loads((HERE/'kfield-vocabulary.jsonld').read_text(encoding='utf-8'))
kv_ids={n.get('@id') for n in kv.get('@graph',[])}
canonical_emily=BASE+'machine_index/semantic/kfield-vocabulary.jsonld#emily-eigen-spectrum'
legacy_emily=BASE+'machine_index/semantic/kfield-vocabulary.jsonld#emily-eigenspectrum'
if canonical_emily not in kv_ids: errors.append('Canonical Emily Eigen-spectrum semantic identifier missing')
if legacy_emily in kv_ids: errors.append('Legacy Emily semantic identifier remains as a second identifier')
if legacy_emily in (HERE/'ontology-mappings.json').read_text(encoding='utf-8'): errors.append('Ontology mappings still reference legacy Emily semantic identifier')

cff=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
if 'type: dataset' not in cff: errors.append('CITATION.cff top-level type is not dataset')
if 'url: "https://krytrondwayne.github.io/Quantum-K-Field/"' not in cff: errors.append('CITATION.cff canonical url is not the GitHub Pages archive')

for name in PACKAGE_ONLY:
    if (ROOT/name).exists(): errors.append(f'Package-only deployment file remains in repository root: {name}')

verify_checksum_file(ROOT/'SHA256SUMS')
verify_checksum_file(HERE/'SHA256SUMS')

try:
    import jsonschema
    pairs=[
        (HERE/'ontology-mappings.json',ROOT/'machine_index/schema/ontology-mappings.schema.json'),
        (HERE/'field-reference.json',ROOT/'machine_index/schema/field-reference.schema.json'),
        (HERE/'page-metadata.json',ROOT/'machine_index/schema/page-metadata.schema.json'),
        (HERE/'index.json',ROOT/'machine_index/schema/semantic-manifest.schema.json'),
    ]
    for instance,schema in pairs:
        validator=jsonschema.Draft202012Validator(json.loads(schema.read_text(encoding='utf-8')))
        for e in validator.iter_errors(json.loads(instance.read_text(encoding='utf-8'))):
            errors.append(f'JSON Schema error {instance.relative_to(ROOT)}: {e.message}')
except ImportError:
    warnings.append('jsonschema package not installed; Draft 2020-12 validation skipped')

try:
    import rdflib
    for p in sorted(HERE.rglob('*.jsonld')):
        try:
            g=rdflib.Graph(); g.parse(data=p.read_text(encoding='utf-8'),format='json-ld')
        except Exception as e: errors.append(f'RDF JSON-LD parse failure {p.relative_to(ROOT)}: {e}')
except ImportError:
    warnings.append('rdflib package not installed; RDF JSON-LD parse skipped')

print(f'Parsed JSON/JSON-LD files: {parsed}')
print(f'HTML landing pages: {html_count}; valid static embedded JSON-LD blocks: {jsonld_blocks}')
print(f'Dataset profiles: {len(dataset_ids)}; field references: {len(fieldref.get("fields",{}))}')
print(f'Warnings: {len(warnings)}; Errors: {len(errors)}')
for x in warnings: print('WARNING:',x)
for x in errors: print('ERROR:',x)
sys.exit(1 if errors else 0)
