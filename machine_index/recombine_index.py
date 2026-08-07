#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "machine_index"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

core = load(IDX / "core.json")["payload"]
manifest = load(IDX / "index.json")
out = {}
for key in ["$schema","schema_title","schema_version","document_type",
            "repository_snapshot","indexing_method","statistics"]:
    out[key]=core[key]

out["normalization"]=load(IDX/"normalization.json")["payload"]
out["category_index"]=load(IDX/"category-index.json")["payload"]

out["topic_taxonomy"]=[]
for rel in manifest["reconstruction"]["logical_sections"]["topic_taxonomy"]:
    out["topic_taxonomy"].extend(load(ROOT/rel)["records"])

out["keyword_index"]=load(IDX/"keyword-index.json")["payload"]
out["cff_keywords_observed"]=core["cff_keywords_observed"]
out["github_topics"]=core["github_topics"]
out["raw_keyword_vocabulary"]=load(IDX/"raw-keyword-vocabulary.json")["records"]
out["extended_search_keyword_vocabulary"]=load(IDX/"extended-search-keyword-vocabulary.json")["records"]
out["search_companion_index"]=load(IDX/"search-companion-index.json")["records"]

out["artifact_index"]=[]
for rel in manifest["reconstruction"]["logical_sections"]["artifact_index"]:
    out["artifact_index"].extend(load(ROOT/rel)["records"])

semantic_manifest = IDX / "semantic" / "index.json"
if semantic_manifest.exists():
    out["semantic_web"] = load(semantic_manifest)

out["integrity"]=core["integrity"]
target=ROOT/"Quantum-K-Field_topic_keyword_index_recombined.json"
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(target)
