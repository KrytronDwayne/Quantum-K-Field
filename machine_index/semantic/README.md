# Quantum K-Field Semantic Metadata

This directory is the semantic-web extension of the existing sharded machine index. It is additive: authoritative research artifacts and existing artifact/taxonomy shards remain unchanged.

Start with `index.json`. `dataset-catalog.jsonld` supplies the machine-facing DCAT/Schema.org catalog; `ontology-mappings.json` maps internal fields and scientific concepts to external vocabularies; `field-reference.json` provides deterministic exact-key semantics and unit/reference-frame constraints; `kfield-vocabulary.jsonld` assigns stable internal IDs to project-specific terminology; `page-metadata.json` is the generator registry; and `datasets/` contains standalone extended JSON-LD profiles.

Canonical semantic base: `https://krytrondwayne.github.io/Quantum-K-Field/machine_index/semantic/`

Search-facing HTML uses static Schema.org JSON-LD. Standalone semantic records additionally use W3C DCAT 3, DCMI, PROV-O, SKOS, QUDT and IVOA identifiers where appropriate.

Run `python validate_semantic_metadata.py` from this directory after repository deployment or from the update package before upload. When page metadata or dataset profiles change, run `python refresh_embedded_jsonld.py` from this directory to deterministically refresh canonical links and embedded search-facing JSON-LD blocks, then rerun validation.
