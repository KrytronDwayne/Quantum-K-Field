# Upload Instructions — Quantum K-Field Semantic Web Upgrade

Use the companion `Quantum-K-Field_semantic_web_REPOSITORY_PAYLOAD_20260807.zip` for deployment. It is rooted exactly like the repository and contains only files that should be uploaded. Extract/copy that payload into the local `Quantum-K-Field` repository root, preserving paths. Existing scientific artifacts are not included and are not deleted.

The full package also contains `UPLOAD_INSTRUCTIONS.md`, `UPLOAD_MANIFEST.json`, `VALIDATION_REPORT.txt`, and `SHA256SUMS.semantic-upgrade`; these are deployment/audit aids and are not part of the repository payload.

## Files intentionally replaced

- `llms.txt`
- root and directory `index.html` landing pages listed in `UPLOAD_MANIFEST.json`
- `machine_index/recombine_index.py`
- `Quantum-K-Field_topic_keyword_index_20260806T200100Z.json` (additive semantic entry points; artifact snapshot counters preserved)

## Files added

- `SEMANTIC_WEB_REQUIREMENTS.md`
- `robots.txt`
- `sitemap.xml`
- `machine_index/semantic/**`
- `machine_index/schema/**`

## Recommended local deployment

From the local repository root after copying the package contents:

```text
python machine_index/semantic/validate_semantic_metadata.py
git status
# Stage only the files shown as add/replace in UPLOAD_MANIFEST.json.
# Review `git status --short` before committing.
git commit -m "Add semantic dataset discovery and ontology metadata"
git push origin main
```

If preferred, upload the same files through GitHub's web interface while preserving every relative path.

After GitHub Pages rebuilds, verify representative pages, especially `https://krytrondwayne.github.io/Quantum-K-Field/OCXO_Experiments/`, with Google's Rich Results Test and submit `https://krytrondwayne.github.io/Quantum-K-Field/sitemap.xml` in Search Console.

Do not delete existing `machine_index` shards. This package extends them.
