#!/usr/bin/env python3
"""Maintenance helper for the semantic extension.

The deployed HTML pages in this release already contain static JSON-LD. Future page
regeneration should treat page-metadata.json, dataset-catalog.jsonld, and
ontology-mappings.json as source metadata and preserve the
KFIELD-JSONLD:START/KFIELD-JSONLD:END block. This utility performs a guard check
so template pipelines fail loudly if that block is accidentally dropped.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
missing=[]
for p in ROOT.rglob('index.html'):
    t=p.read_text(encoding='utf-8')
    if 'KFIELD-JSONLD:START' not in t or 'KFIELD-JSONLD:END' not in t:
        missing.append(str(p.relative_to(ROOT)))
if missing:
    print('Missing semantic JSON-LD markers:')
    print('\n'.join(missing)); sys.exit(1)
print('All index.html pages preserve semantic JSON-LD markers.')
