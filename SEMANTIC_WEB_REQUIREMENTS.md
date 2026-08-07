# Quantum K-Field Semantic Web and Dataset Discovery Requirements

Version: 1.0.0  
Scope: `KrytronDwayne/Quantum-K-Field` public GitHub Pages archive  
Deployment target: `main` branch, repository root, published at `https://krytrondwayne.github.io/Quantum-K-Field/`

## 1. Objective

The archive SHALL expose a standards-based semantic discovery layer that improves search-engine dataset discovery, LLM/agent assimilation, machine interpretation of scientific fields, provenance tracing, and stable navigation without altering authoritative scientific source artifacts.

The semantic layer is metadata. It SHALL NOT rewrite experimental data, alter numerical results, replace primary reports, or imply equivalence between project-specific K-Field terminology and external scientific concepts where only a broader or related relationship is justified.

## 2. Normative vocabulary stack

The implementation SHALL use the following roles:

| Vocabulary | Required role |
|---|---|
| Schema.org | Search-facing WebSite, CollectionPage, DataCatalog, Dataset, DataDownload, PropertyValue, Person and Organization markup |
| W3C DCAT 3 | Machine-facing catalog, dataset and distribution interoperability |
| DCMI Metadata Terms | Bibliographic/resource metadata and general relations |
| W3C PROV-O | Provenance and derivation relationships |
| W3C SKOS | Explicit mapping strength between internal and external concepts |
| QUDT | Physical quantity kinds and units |
| IVOA reference-frame vocabulary | Astronomy-specific coordinate/reference-frame identifiers such as ICRS |
| IVOA UCD | Controlled astronomical quantity descriptors where an exact UCD is available |

Authoritative references:

- Google Dataset structured data: https://developers.google.com/search/docs/appearance/structured-data/dataset
- Schema.org Dataset: https://schema.org/Dataset
- Schema.org variableMeasured: https://schema.org/variableMeasured
- W3C DCAT 3: https://www.w3.org/TR/vocab-dcat-3/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- DCMI Metadata Terms: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
- QUDT catalog: https://www.qudt.org/catalog/qudt-catalog.html
- IVOA reference frames: https://www.ivoa.net/rdf/refframe

## 3. Canonical identity and URLs

1. GitHub Pages SHALL be the canonical Web identity for structured-data landing pages.
2. Every generated `index.html` SHALL include a `<link rel="canonical">` pointing to its GitHub Pages URL.
3. Semantic entities SHALL use stable `@id` values under the GitHub Pages domain.
4. GitHub repository/blob/raw URLs MAY be used for source distributions, repository identity, and `sameAs` relationships, but SHALL NOT replace the canonical landing-page URL.
5. Internal K-Field concept identifiers SHALL resolve to `machine_index/semantic/kfield-vocabulary.jsonld#<term-id>`.

## 4. Page typing requirements

1. Repository root SHALL be typed as `WebSite` and `DataCatalog`.
2. Directory landing pages SHALL be typed as `CollectionPage` unless they are specifically a data catalog.
3. `machine_index/` SHALL be typed as `DataCatalog`.
4. A `Dataset` SHALL be declared only when the resource is an actual data collection, structured machine-readable record set, or meaningful collection of data files.
5. Papers, commentary, lectures, press material, and introductory documentation SHALL NOT be mislabeled as datasets.
6. Dataset JSON-LD SHALL appear on the canonical landing page that describes that dataset or data collection.

## 5. Dataset metadata requirements

Each declared Dataset SHALL contain, at minimum:

- `@id`
- `@type: Dataset`
- `name`
- `description`
- canonical `url`
- `creator`
- `license`
- `keywords`
- `isAccessibleForFree`
- `includedInDataCatalog`

Where supported by the source record, the Dataset SHOULD also include:

- `distribution` using `DataDownload`
- `variableMeasured`
- `measurementTechnique`
- `temporalCoverage`
- geographic `spatialCoverage`
- `citation`
- `isBasedOn` / provenance relationships
- version or date metadata

Unknown values SHALL be omitted rather than inferred.

Dataset license metadata SHALL resolve through the repository controlling public license document (`LICENSE-PAPER.md`) so source-specific exceptions remain authoritative; semantic metadata SHALL NOT override a source-specific license notice.

## 6. Scientific coordinate and variable semantics

1. `spatialCoverage` SHALL be reserved for geographic/place coverage.
2. Celestial coordinates, ICRS vectors, right ascension, declination, sidereal angle, barycentric coordinates, CMB-referenced vectors, detector orientation, and similar quantities SHALL be represented as measured/derived variables, reference-frame properties, or additional properties.
3. ICRS SHALL map to the IVOA reference-frame identifier `http://www.ivoa.net/rdf/refframe#ICRS`.
4. Physical quantities SHOULD map to QUDT quantity-kind URIs and units when the unit is explicitly known.
5. A unit SHALL NOT be supplied from assumption when the source artifact does not establish it.

## 7. Internal terminology mapping

1. Project-specific names SHALL retain authoritative internal identifiers.
2. Mapping relationships SHALL explicitly state strength using `exactMatch`, `closeMatch`, `broadMatch`, `narrowMatch`, or `relatedMatch` semantics modeled after SKOS.
3. K-Field-specific structures such as Cell3, Devon Dimension, Mass Bridge, Lucas Limit, Emily Eigen-spectrum, Jack Jacobian, and Lucas Supergroup SHALL NOT be asserted as exact external ontology concepts.
4. Their conventional mathematical descriptions MAY be mapped as broader or related concepts.

## 8. Provenance requirements

1. Primary source artifacts SHALL remain authoritative.
2. Search companions SHALL be identified as discovery metadata, not independent experimental evidence.
3. Paired PDF/JSON representations of one work SHALL NOT be counted as independent experiments solely because they are separate files.
4. Derived datasets SHOULD carry `prov:wasDerivedFrom` or equivalent source relationships when known.
5. The public-release declaration and applicable license SHALL remain discoverable from semantic metadata.

## 9. JSON and JSON-LD requirements

1. All JSON/JSON-LD SHALL be UTF-8 and valid JSON.
2. JSON-LD embedded in HTML SHALL be static `<script type="application/ld+json">` content.
3. Search-facing embedded JSON-LD SHALL preferentially use Schema.org terms for maximum crawler compatibility.
4. Extended standalone JSON-LD MAY additionally use DCAT, DCTERMS, PROV-O, SKOS, QUDT, and IVOA identifiers.
5. The retired/legacy `variablesMeasured` spelling SHALL NOT be emitted; use `variableMeasured`.
6. Semantic JSON records SHALL include schema/version/document-type identifiers.

## 10. Crawl and discovery requirements

1. `robots.txt` SHALL permit public crawling and identify the sitemap.
2. `sitemap.xml` SHALL enumerate canonical archive landing pages, especially canonical pages containing Dataset markup.
3. `llms.txt` SHALL route agents to the semantic manifest, ontology mappings, dataset catalog, normalization, taxonomy, and artifact locators.
4. Dataset descriptions duplicated in machine catalogs SHALL identify the canonical landing page via stable IDs/URLs.

## 11. Validation requirements

Before deployment, the update SHALL pass all of the following local checks:

- parse every `.json` and `.jsonld` file;
- parse every embedded JSON-LD block in generated HTML;
- ensure every generated HTML page has exactly one canonical URL;
- reject use of `variablesMeasured`;
- ensure every Dataset has name, description, URL, creator, license and catalog membership;
- ensure all local semantic file references resolve inside the update set;
- ensure sitemap URLs are unique;
- generate SHA-256 checksums for the complete upload set.

After deployment, the maintainer SHOULD test representative dataset pages with Google's Rich Results Test / Search Console and a Schema.org validator, then submit `sitemap.xml` to Search Console.

## 12. Change-control requirements

1. The semantic layer SHALL be versioned independently from scientific artifacts.
2. Future additions SHOULD be made through `machine_index/semantic/page-metadata.json`, the standalone dataset profiles, and `machine_index/semantic/refresh_embedded_jsonld.py` rather than hand-editing JSON-LD on many pages.
3. Generated JSON-LD blocks SHALL be delimited by machine-readable comments to support deterministic replacement.
4. Existing raw datasets, reports, figures, analysis JSON and archival provenance SHALL not be modified by this upgrade.
5. `machine_index/semantic/field-reference.json` SHALL provide direct, full-URI mappings for exact/high-value archive field keys; mappings SHALL state unit or reference-frame conditions explicitly and SHALL never infer missing source semantics.
