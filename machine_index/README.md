# Quantum K-Field Machine Index

This directory is the current sharded machine-readable discovery index for the public Quantum K-Field archive.

Snapshot HEAD: `de76315a0e7ef5f0d76d2bdbb90184bb8b0ae6fb`  
Snapshot tree: `f730312eaf489d103f54d29aba40915fca5a2973`  
Generated: `2026-08-07T02:58:39Z`  
Schema: `2.1.0-sharded-live`

The artifact inventory contains **242 primary/public artifacts** and **130 searchable `.abstract.json` companions**, for **372 indexed public files** outside this generated directory. The `machine_index/**` directory is deliberately excluded from its own artifact inventory to prevent recursive self-indexing.

## Entry points

- `index.json` — authoritative shard manifest.
- `core.json` — snapshot, method, statistics, repository topics, and integrity.
- `normalization.json` — misspellings, abbreviations, and aliases.
- `category-index.json` — category-to-term lookup.
- `keyword-index.json` — normalized keyword-to-topic lookup.
- `search-companion-index.json` — authoritative source path to `.abstract.json` companion mapping.
- `taxonomy/` — canonical topic records.
- `artifacts/` — current public artifact records partitioned by repository directory.
- `lookup/term-locator.json` — topic ID to taxonomy shard.
- `lookup/artifact-locator.json` — artifact path to artifact shard.
- `recombine_index.py` — reconstructs the complete logical index if a monolithic copy is needed offline.
- `semantic/` — additive semantic-web catalog, ontology mappings, field registry, dataset profiles, and integrity validation.

The repository-root `Quantum-K-Field_topic_keyword_index_20260806T200100Z.json` is retained as a stable compatibility entry point for existing README links. It points to `machine_index/index.json`.
