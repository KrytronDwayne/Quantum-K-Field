# Quantum K-Field Machine Index

The topic and keyword index is sharded here so GitHub Code Search can index it.

The former monolithic index was **576,149 bytes (562.6 KiB)**. GitHub Code Search excludes files over 350 KiB. This layout uses a conservative **128 KiB design ceiling** and semantic partitions rather than arbitrary byte chunks.

`index.json` is the authoritative manifest. Taxonomy records are partitioned by scientific category; artifact records are partitioned by the repository directory they describe. Alias, misspelling, abbreviation, keyword, and locator tables remain separate searchable files.

The root `Quantum-K-Field_topic_keyword_index_20260806T200100Z.json` is now a small compatibility pointer, so existing links to that filename do not need to change.

Use `python machine_index/recombine_index.py` from the repository root to reconstruct the original logical index.

Original source SHA-256: `4d75ebed5c5c24f714caf6b2c71238752ecfe3f9fd4ed0fdd104f05ae21cd1bd`
