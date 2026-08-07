(() => {
  "use strict";

  const cfg = window.KFIELD_INDEX_CONFIG || {};
  const repo = cfg.repository || "KrytronDwayne/Quantum-K-Field";
  const branch = cfg.branch || "main";
  const currentDirectory = cfg.directory || ".";
  const listNode = document.getElementById("file-list");
  const countNode = document.getElementById("catalog-count");
  const searchNode = document.getElementById("catalog-search");
  const dirsNode = document.getElementById("directory-grid");
  const dirsSection = document.getElementById("directories-section");
  let records = [];

  const ACRONYMS = new Map(Object.entries({
    "cmb":"CMB","icrs":"ICRS","ocxo":"OCXO","gps":"GPS","pca":"PCA","fft":"FFT","cwt":"CWT",
    "as7341":"AS7341","as7343":"AS7343","sgA":"SGA","sga":"SGA","ra":"RA","dec":"Dec",
    "json":"JSON","pdf":"PDF","png":"PNG","zip":"ZIP","github":"GitHub","api":"API","llm":"LLM",
    "qed":"QED","cmbdipole":"CMB dipole","emb":"EMB","utc":"UTC","sha256":"SHA-256"
  }));

  const genericWords = new Set([
    "k","field","quantum","report","analysis","study","studies","search","searchable","abstract",
    "companion","json","pdf","png","zip","file","data","dataset","archive","repository","2026"
  ]);

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, ch => ({
      "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
    }[ch]));
  }

  function cleanEpoch(text) {
    return String(text || "")
      .replace(/(?:[_\-\s])17\d{8,}$/g, "")
      .replace(/(?:[_\-\s])20\d{6}T\d{6}Z$/i, "")
      .replace(/\bsearchable abstract companion\b/ig, "")
      .trim();
  }

  function humanizeWords(text) {
    const words = cleanEpoch(String(text || "")
      .replace(/\.abstract\.json$/i, "")
      .replace(/\.(pdf|json|png|zip|txt|md|cff|py|html|css|js)$/i, "")
      .replace(/[_\-]+/g, " ")
      .replace(/\s+/g, " ")
      .trim()).split(" ").filter(Boolean);

    return words.map((word, index) => {
      const lower = word.toLowerCase();
      if (ACRONYMS.has(lower)) return ACRONYMS.get(lower);
      if (/^\d+(?:\.\d+)?$/.test(word) || /^[A-Z0-9]{2,}$/.test(word)) return word;
      if (lower === "kfield") return "K-Field";
      if (lower === "cell3") return "Cell3";
      if (lower === "bragg") return "Bragg";
      if (index === 0) return word.charAt(0).toUpperCase() + word.slice(1);
      return word;
    }).join(" ").replace(/\bK Field\b/g, "K-Field");
  }

  function humanizeTopic(text) {
    const t = String(text || "").replace(/-/g, " ");
    return humanizeWords(t);
  }

  function fileExtension(record) {
    if (record.extension) return String(record.extension).toLowerCase();
    const name = String(record.filename || record.name || "");
    if (/\.pdf\.abstract\.json$/i.test(name)) return "pdf.abstract.json";
    if (/\.json\.abstract\.json$/i.test(name)) return "json.abstract.json";
    if (/\.png\.abstract\.json$/i.test(name)) return "png.abstract.json";
    if (/\.zip\.abstract\.json$/i.test(name)) return "zip.abstract.json";
    const i = name.lastIndexOf(".");
    return i >= 0 ? name.slice(i + 1).toLowerCase() : "";
  }

  function titleFor(record) {
    if (record.normalized_title) return humanizeWords(record.normalized_title);
    return humanizeWords(record.filename || record.name || record.path || "Repository artifact");
  }

  function sourceTitleFor(record) {
    const source = record.authoritative_source_path || record.search_companion_path || "";
    if (!source) return titleFor(record).replace(/\s+Searchable Abstract Companion$/i, "");
    return humanizeWords(source.split("/").pop());
  }

  function cleanTerms(values, max = 7) {
    const seen = new Set();
    const out = [];
    for (const raw of Array.isArray(values) ? values : []) {
      let term = humanizeTopic(raw);
      const key = term.toLowerCase();
      if (!term || genericWords.has(key) || /^\d+$/.test(key) || seen.has(key)) continue;
      seen.add(key);
      out.push(term);
      if (out.length >= max) break;
    }
    return out;
  }

  function joinTerms(values) {
    if (!values.length) return "";
    if (values.length === 1) return values[0];
    if (values.length === 2) return `${values[0]} and ${values[1]}`;
    return `${values.slice(0, -1).join(", ")}, and ${values[values.length - 1]}`;
  }

  function limitWords(text, maxWords = 72) {
    const words = String(text).replace(/\s+/g, " ").trim().split(" ");
    if (words.length <= maxWords) return words.join(" ");
    return words.slice(0, maxWords).join(" ").replace(/[,:;]$/, "") + ".";
  }

  function descriptionFor(record) {
    const ext = fileExtension(record);
    const title = titleFor(record);
    const topics = cleanTerms(record.canonical_topic_ids, 6);
    const keywords = cleanTerms(record.raw_keywords, 8);
    const topicText = joinTerms(topics);
    const keywordText = joinTerms(keywords);
    const topicClause = topicText ? ` covering ${topicText}` : "";
    const keywordClause = keywordText ? ` Indexed terms include ${keywordText}.` : "";
    const filename = String(record.filename || record.name || "");

    if (/^README\.md$/i.test(filename)) {
      return "Directory documentation describing the purpose, scope, navigation, usage, and conventions of this portion of the Quantum K-Field research archive.";
    }
    if (/^LICENSE-CODE\.md$/i.test(filename)) {
      return "License terms governing repository source code and software-related materials in the Quantum K-Field public research archive.";
    }
    if (/^LICENSE-PAPER\.md$/i.test(filename)) {
      return "License terms governing papers, reports, educational documents, and other written research materials in the Quantum K-Field archive.";
    }
    if (/^PUBLIC_RELEASE_STATUS\.json$/i.test(filename)) {
      return "Machine-readable release-status record documenting the public availability and disclosure state of the Quantum K-Field repository materials.";
    }
    if (/topic_keyword_index/i.test(filename)) {
      return "Stable machine-readable entry point to the current sharded topic and keyword index, including repository snapshot metadata, artifact counts, taxonomy counts, and index locations.";
    }
    if (currentDirectory === "machine_index" && /^index\.json$/i.test(filename)) {
      return "Primary manifest for the sharded machine index, defining the repository snapshot, artifact inventory, taxonomy shards, lookup files, reconstruction metadata, and integrity information.";
    }
    if (currentDirectory === "machine_index" && /^core\.json$/i.test(filename)) {
      return "Core machine-index metadata defining repository identity, indexing scope, schema conventions, counts, and archive-level descriptive information.";
    }
    if (currentDirectory === "machine_index" && /^category-index\.json$/i.test(filename)) {
      return "Machine-readable category index mapping high-level research categories to indexed Quantum K-Field artifacts and canonical topics.";
    }
    if (currentDirectory === "machine_index" && /^keyword-index\.json$/i.test(filename)) {
      return "Machine-readable keyword index connecting normalized search terms to canonical topics and the repository artifacts in which they occur.";
    }
    if (currentDirectory === "machine_index" && /^normalization\.json$/i.test(filename)) {
      return "Normalization rules for filenames, aliases, abbreviations, legacy spellings, extensions, epoch suffixes, and canonical Quantum K-Field terminology.";
    }
    if (currentDirectory === "machine_index" && /^raw-keyword-vocabulary\.json$/i.test(filename)) {
      return "Observed repository keyword vocabulary preserving normalized raw terms extracted from public Quantum K-Field artifact names and metadata.";
    }
    if (currentDirectory === "machine_index" && /^extended-search-keyword-vocabulary\.json$/i.test(filename)) {
      return "Extended search vocabulary expanding canonical Quantum K-Field terms with aliases and related terminology for machine discovery and retrieval.";
    }
    if (currentDirectory === "machine_index" && /^search-companion-index\.json$/i.test(filename)) {
      return "Index of compact searchable abstract companions created for oversized or otherwise machine-discovery-sensitive research artifacts.";
    }
    if (/^recombine_index\.py$/i.test(filename)) {
      return "Python utility that reconstructs the logical monolithic machine index from the repository's sharded index components.";
    }
    if (currentDirectory === "machine_index/lookup" && /^artifact-locator\.json$/i.test(filename)) {
      return "Lookup table mapping exact repository artifact paths to the machine-index shard that contains each artifact record.";
    }
    if (currentDirectory === "machine_index/lookup" && /^term-locator\.json$/i.test(filename)) {
      return "Lookup table mapping canonical terms to the taxonomy or index shards that define and reference them.";
    }
    if (currentDirectory === "machine_index/artifacts" && /\.json$/i.test(filename)) {
      return limitWords(`Artifact-index shard for ${title}, enumerating repository paths, normalized titles, raw keywords, canonical topic identifiers, GitHub links, and searchable-companion metadata.`);
    }
    if (currentDirectory === "machine_index/taxonomy" && /\.json$/i.test(filename)) {
      return limitWords(`Taxonomy shard for ${title}, defining canonical topic relationships and the indexed artifacts associated with this research domain.`);
    }

    if (record.artifact_role === "searchable_abstract_companion" || /\.abstract\.json$/i.test(record.filename || "")) {
      return limitWords(`Machine-readable search companion for ${sourceTitleFor(record)}, exposing topic metadata and searchable terminology${topicText ? ` for ${topicText}` : ""}.${keywordText ? ` Indexed terms include ${keywordText}.` : ""}`);
    }

    if ((record.filename || "").toUpperCase() === "SHA256SUMS") {
      return "Integrity manifest containing SHA-256 checksums for repository artifacts and machine-index components.";
    }
    if (ext === "cff") {
      return "Citation metadata defining the preferred attribution, authorship, versioning, and bibliographic identity of the Quantum K-Field research archive.";
    }
    if (ext === "pdf") {
      return limitWords(`Authoritative report on ${title}.${topicText ? ` It documents ${topicText}.` : ""}${keywordClause}`);
    }
    if (ext === "json") {
      return limitWords(`Machine-readable analysis and data record for ${title}${topicClause}.${keywordClause}`);
    }
    if (ext === "png" || ext === "jpg" || ext === "jpeg" || ext === "svg") {
      return limitWords(`Visual research asset for ${title}${topicClause}.${keywordClause}`);
    }
    if (ext === "zip") {
      return limitWords(`Packaged research archive for ${title}${topicClause}.${keywordClause}`);
    }
    if (ext === "txt") {
      return limitWords(`Technical text resource for ${title}${topicClause}.${keywordClause}`);
    }
    if (ext === "md") {
      return limitWords(`Repository documentation for ${title}${topicClause}.${keywordClause}`);
    }
    if (ext === "py") {
      return limitWords(`Executable repository utility for ${title}${topicClause}.${keywordClause}`);
    }
    return limitWords(`Repository artifact for ${title}${topicClause}.${keywordClause}`);
  }

  function roleBadge(record) {
    return record.artifact_role === "searchable_abstract_companion" || /\.abstract\.json$/i.test(record.filename || "")
      ? '<span class="badge companion">Search companion</span>' : "";
  }

  function typeBadge(record) {
    const ext = fileExtension(record);
    const label = ext ? ext.replace(".abstract.json", " abstract").replace(/\./g, " ") : "resource";
    return `<span class="badge">${escapeHtml(label)}</span>`;
  }

  function relativeFileHref(record) {
    const name = record.filename || record.name || String(record.path || "").split("/").pop();
    return encodeURIComponent(name).replace(/%2F/gi, "/");
  }

  function recordSearchText(record) {
    return [
      record.filename, record.normalized_title, descriptionFor(record),
      ...(record.raw_keywords || []), ...(record.canonical_topic_ids || [])
    ].filter(Boolean).join(" ").toLowerCase();
  }

  function baseSortName(record) {
    const name = String(record.filename || record.name || "").toLowerCase();
    return name.replace(/\.abstract\.json$/, "") + (/\.abstract\.json$/.test(name) ? "~2" : "~1");
  }

  function renderRecords(query = "") {
    const q = query.trim().toLowerCase();
    const filtered = records.filter(r => !q || recordSearchText(r).includes(q));
    countNode.textContent = `${filtered.length} ${filtered.length === 1 ? "file" : "files"}`;

    if (!filtered.length) {
      listNode.innerHTML = `<div class="status">${escapeHtml(q ? "No files match this search." : (cfg.emptyMessage || "No indexed research files are stored directly in this directory."))}</div>`;
      return;
    }

    listNode.innerHTML = filtered.map(record => {
      const name = record.filename || record.name || record.path;
      return `
        <article class="file-card">
          <div class="file-main">
            <a class="file-title" href="${relativeFileHref(record)}">${escapeHtml(name)}</a>
            <p class="file-description">${escapeHtml(descriptionFor(record))}</p>
          </div>
          <div class="file-badges">${roleBadge(record)}${typeBadge(record)}</div>
        </article>`;
    }).join("");
  }

  function renderDirectories() {
    const dirs = Array.isArray(cfg.subdirectories) ? cfg.subdirectories : [];
    if (!dirs.length || !dirsNode || !dirsSection) return;
    dirsSection.hidden = false;
    dirsNode.innerHTML = dirs.map(dir => `
      <a class="directory-card" href="${escapeHtml(dir.href)}">
        <strong>${escapeHtml(dir.label)}</strong>
        <span>${escapeHtml(dir.description || "Open this repository directory.")}</span>
      </a>`).join("");
  }

  async function fetchJson(url) {
    const response = await fetch(url, { headers: { "Accept": "application/vnd.github+json" } });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    return response.json();
  }

  function inferredTopics(name) {
    return String(name || "")
      .replace(/\.[^.]+$/g, "")
      .split(/[_\-\s]+/)
      .filter(token => token.length > 2 && !/^\d+$/.test(token))
      .slice(0, 12);
  }

  function recordFromContentItem(item) {
    return {
      path: item.path,
      directory: currentDirectory,
      filename: item.name,
      extension: fileExtension({ filename: item.name }),
      normalized_title: humanizeWords(item.name),
      raw_keywords: inferredTopics(item.name),
      canonical_topic_ids: inferredTopics(item.name),
      artifact_role: "primary_or_authoritative_repository_artifact"
    };
  }

  function systemFile(name) {
    const n = String(name || "").toLowerCase();
    if (n === "index.html" || n === ".ds_store" || n === "thumbs.db" || n === "desktop.ini") return true;
    if (n.startsWith(".git")) return true;
    return (cfg.excludeFiles || []).map(x => String(x).toLowerCase()).includes(n);
  }

  async function recordsFromShards() {
    const urls = Array.isArray(cfg.shardUrls) ? cfg.shardUrls : [];
    if (!urls.length) return [];
    const shards = await Promise.all(urls.map(fetchJson));
    return shards.flatMap(shard => Array.isArray(shard.records) ? shard.records : []);
  }

  async function recordsFromApi() {
    const path = currentDirectory === "." ? "" : `/${currentDirectory.split("/").map(encodeURIComponent).join("/")}`;
    const url = cfg.contentsApiUrl || `https://api.github.com/repos/${repo}/contents${path}?ref=${encodeURIComponent(branch)}`;
    const data = await fetchJson(url);
    if (!Array.isArray(data)) return [];
    return data.filter(item => item.type === "file" && !systemFile(item.name)).map(recordFromContentItem);
  }

  async function loadRecords() {
    let loaded = [];
    let shardError = null;

    if (Array.isArray(cfg.manualFiles) && cfg.manualFiles.length) {
      loaded = cfg.manualFiles.map(name => recordFromContentItem({
        name,
        path: currentDirectory === "." ? name : `${currentDirectory}/${name}`,
        type: "file"
      }));
    }

    if (!loaded.length && Array.isArray(cfg.shardUrls) && cfg.shardUrls.length) {
      try { loaded = await recordsFromShards(); }
      catch (error) { shardError = error; }
    }

    if (!loaded.length && cfg.allowApiFallback !== false) {
      try { loaded = await recordsFromApi(); }
      catch (error) {
        if (shardError) error.message = `${shardError.message}; fallback: ${error.message}`;
        throw error;
      }
    }

    const seen = new Set();
    records = loaded
      .filter(record => {
        const name = record.filename || record.name || "";
        if (systemFile(name)) return false;
        const key = record.path || name;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      })
      .sort((a, b) => baseSortName(a).localeCompare(baseSortName(b), undefined, { numeric: true }));

    renderRecords(searchNode?.value || "");
  }

  function installStructuredData() {
    const data = {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": cfg.title || "Quantum K-Field Research Archive",
      "description": cfg.summary || "",
      "isPartOf": {
        "@type": "Dataset",
        "name": "Quantum K-Field Research Archive",
        "url": `https://github.com/${repo}`
      }
    };
    const node = document.createElement("script");
    node.type = "application/ld+json";
    node.textContent = JSON.stringify(data);
    document.head.appendChild(node);
  }

  renderDirectories();
  installStructuredData();
  if (searchNode) searchNode.addEventListener("input", () => renderRecords(searchNode.value));
  loadRecords().catch(error => {
    countNode.textContent = "Unavailable";
    listNode.innerHTML = `<div class="status error">The live catalog could not be loaded. Open the <a href="${escapeHtml(cfg.githubDirectoryUrl || `https://github.com/${repo}/tree/${branch}/${currentDirectory === "." ? "" : currentDirectory}`)}">GitHub directory</a> to browse files directly.<br><small>${escapeHtml(error.message)}</small></div>`;
  });
})();