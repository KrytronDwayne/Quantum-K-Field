#!/usr/bin/env python3
"""Guard checks for generated landing pages and the shared runtime."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[2]
missing=[]; bad=[]
for p in ROOT.rglob('index.html'):
    t=p.read_text(encoding='utf-8')
    if 'KFIELD-JSONLD:START' not in t or 'KFIELD-JSONLD:END' not in t:
        missing.append(str(p.relative_to(ROOT)))
    count=len(re.findall(r'<script\s+type=["\']application/ld\+json["\']',t,re.I))
    if count!=1: bad.append(f'{p.relative_to(ROOT)}: static JSON-LD blocks={count}')
js=ROOT/'Assets/kfield-directory-index.js'
if js.exists():
    text=js.read_text(encoding='utf-8')
    if 'installStructuredData' in text or 'application/ld+json' in text:
        bad.append('Assets/kfield-directory-index.js: runtime JSON-LD injection detected')
else: bad.append('Assets/kfield-directory-index.js: missing')
if missing:
    print('Missing semantic JSON-LD markers:'); print('\n'.join(missing))
if bad:
    print('Structured-data guard failures:'); print('\n'.join(bad))
if missing or bad: sys.exit(1)
print('All index.html pages preserve exactly one static semantic JSON-LD block; shared JavaScript performs no JSON-LD injection.')
