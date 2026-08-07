#!/usr/bin/env python3
"""Refresh canonical links and static Schema.org JSON-LD on archive landing pages.

Inputs: page-metadata.json, index.json, and datasets/*.jsonld.
This script modifies only <link rel="canonical"> and the delimited
KFIELD-JSONLD block. It does not alter scientific artifacts or file catalogs.
"""
from pathlib import Path
import json, re, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
manifest=json.loads((HERE/'index.json').read_text(encoding='utf-8'))
registry=json.loads((HERE/'page-metadata.json').read_text(encoding='utf-8'))
BASE=manifest['canonical_base']
CAT=BASE+'#data-catalog'
MACHINE_CAT=BASE+'machine_index/#data-catalog'
LICENSE='https://github.com/KrytronDwayne/Quantum-K-Field/blob/main/LICENSE-PAPER.md'
ORG={'@id':BASE+'#organization','@type':'Organization','name':'Krytronx, LLC'}
PI={'@id':BASE+'#principal-investigator','@type':'Person','name':'P. Dwayne Esterline','givenName':'P. Dwayne','familyName':'Esterline','affiliation':{'@id':ORG['@id']}}
WEBSITE={'@id':BASE+'#website','@type':'WebSite','name':'Quantum K-Field Research Archive','url':BASE,'publisher':{'@id':ORG['@id']},'creator':{'@id':PI['@id']},'inLanguage':'en'}

profile_entries={x['id']:x for x in manifest['dataset_profiles']}

def load_dataset(profile_id):
    entry=profile_entries[profile_id]
    obj=json.loads((HERE/entry['jsonld']).read_text(encoding='utf-8'))
    node=None
    for n in obj.get('@graph',[]):
        t=n.get('@type',[]); t=[t] if isinstance(t,str) else t
        if 'schema:Dataset' in t:
            node=n; break
    if node is None: raise ValueError(f'No schema:Dataset in {entry["jsonld"]}')
    page_url=node.get('schema:url',{}).get('@id') if isinstance(node.get('schema:url'),dict) else node.get('schema:url')
    lic=node.get('dcterms:license')
    if isinstance(lic,dict) and '@id' in lic: lic=lic['@id']
    out={'@id':node['@id'],'@type':'Dataset','name':node['schema:name'],'description':node['schema:description'],'url':page_url,'identifier':node.get('schema:identifier',node['@id']),
         'creator':{'@id':PI['@id']},'publisher':{'@id':ORG['@id']},'license':lic or LICENSE,'isAccessibleForFree':True,
         'keywords':node.get('schema:keywords',[]),'includedInDataCatalog':{'@id':CAT}}
    for src,dst in [('schema:measurementTechnique','measurementTechnique'),('schema:variableMeasured','variableMeasured'),('schema:distribution','distribution')]:
        if src in node: out[dst]=node[src]
    return out

def page_to_html(path):
    if path=='/': return ROOT/'index.html'
    return ROOT/path.strip('/')/'index.html'

def graph_for(rec):
    path=rec['path']; page_url=rec['canonical_url']; desc=rec['description']; title=rec['title']; profile=rec.get('dataset_profile')
    if path=='/':
        graph=[WEBSITE,{'@id':CAT,'@type':'DataCatalog','name':'Quantum K-Field Research Archive Data Catalog','description':desc,'url':BASE,'creator':{'@id':PI['@id']},'publisher':{'@id':ORG['@id']},'license':LICENSE,'isAccessibleForFree':True,'dataset':[{'@id':load_dataset(x['id'])['@id']} for x in manifest['dataset_profiles']]},ORG,PI]
    elif path=='machine_index/':
        graph=[WEBSITE,{'@id':page_url+'#webpage','@type':'CollectionPage','name':title,'description':desc,'url':page_url,'isPartOf':{'@id':WEBSITE['@id']},'mainEntity':{'@id':MACHINE_CAT}},{'@id':MACHINE_CAT,'@type':'DataCatalog','name':'Quantum K-Field Machine-Readable Data Catalog','description':desc,'url':page_url,'creator':{'@id':PI['@id']},'publisher':{'@id':ORG['@id']},'license':LICENSE},ORG,PI]
    else:
        graph=[WEBSITE,{'@id':page_url+'#webpage','@type':'CollectionPage','name':title,'description':desc,'url':page_url,'isPartOf':{'@id':WEBSITE['@id']},'publisher':{'@id':ORG['@id']}},ORG,PI]
    if profile:
        ds=load_dataset(profile); graph.append(ds)
        if path=='machine_index/':
            for n in graph:
                if n.get('@id')==MACHINE_CAT: n['dataset']=[{'@id':ds['@id']}]
        else:
            for n in graph:
                if n.get('@type')=='CollectionPage' and n.get('@id')==page_url+'#webpage': n['mainEntity']={'@id':ds['@id']}
    return {'@context':'https://schema.org/','@graph':graph}

block_re=re.compile(r'\s*<!-- KFIELD-JSONLD:START -->.*?<!-- KFIELD-JSONLD:END -->',re.S)
canonical_re=re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']+["\']\s*/?>',re.I)
changed=[]; errors=[]
for rec in registry['pages']:
    hp=page_to_html(rec['path'])
    if not hp.exists(): errors.append(f'Missing landing page: {hp.relative_to(ROOT)}'); continue
    text=hp.read_text(encoding='utf-8')
    canonical=f'<link rel="canonical" href="{rec["canonical_url"]}">' 
    if canonical_re.search(text): text=canonical_re.sub(canonical,text,count=1)
    else:
        marker='<meta name="theme-color" content="#050b14">'
        if marker not in text: errors.append(f'No canonical insertion marker: {hp.relative_to(ROOT)}'); continue
        text=text.replace(marker,marker+'\n  '+canonical,1)
    payload=json.dumps(graph_for(rec),ensure_ascii=False,indent=2)
    block='\n  <!-- KFIELD-JSONLD:START -->\n  <script type="application/ld+json">\n'+payload+'\n  </script>\n  <!-- KFIELD-JSONLD:END -->'
    if not block_re.search(text): errors.append(f'No JSON-LD marker block: {hp.relative_to(ROOT)}'); continue
    new=block_re.sub(block,text,count=1)
    if new!=hp.read_text(encoding='utf-8'):
        hp.write_text(new,encoding='utf-8'); changed.append(str(hp.relative_to(ROOT)))
if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f'Refreshed {len(changed)} landing page(s).')
for x in changed: print(x)
