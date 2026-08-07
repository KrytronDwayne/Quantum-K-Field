<p align="center">
  <img src="./Assets/Quantum_K-Field_GitHub_Profile_500x500.png" alt="Krytronx Quantum K-Field" width="240">
</p>

# Quantum K-Field

**A public research archive in observational anisotropy, astronomical orientation geometry, precision metrology, and geometric modeling**

The **Quantum K-Field** is a research program developed by **Krytronx** and principal investigator **P. Dwayne Esterline**. The program began with repeated experimental observations of direction-dependent behavior and developed into a broader investigation of whether recurring structures seen across laboratory and astronomical datasets can be described within a common geometric framework.

The archive brings together astronomical orientation analysis, reference-frame geometry, precision oscillator metrology, rotating multispectral measurements, signal processing, graph and metric methods, physical-constant comparisons, and exploratory engineering studies. Its purpose is to make the complete research path inspectable: the observations that motivated the work, the geometric reconstruction that followed, the mathematical objects introduced along the way, the experimental comparisons, and the machine-readable records used to reproduce the analysis. Throughout this README, measured observations, mathematical reconstructions, framework interpretations, and downstream comparisons are kept distinct.

> **Research trajectory:** observation → celestial indexing → cross-domain comparison → galaxy-axis orientation analysis → rhombohedral geometric reconstruction → metric and graph formalization → physical-quantity comparison → laboratory testing and engineering studies.

[Start Here](./Start_Here/) · [Student Reconstruction](./Student_reconstruction_process/) · [Galaxy Analysis](./Galaxy_Analysis/) · [OCXO Experiments](./OCXO_Experiments/) · [Spectrophotometer Studies](./Spectrophotometer_Studies/) · [Topic Index](./Quantum-K-Field_topic_keyword_index_20260806T200100Z.json) · [Citation](./CITATION.cff)

---

## Public release status

All materials publicly present in this repository are released from any prior **confidential, confidential-information, trade-secret, restricted-distribution, or do-not-distribute status** under the repository-level [`PUBLIC_RELEASE_STATUS.json`](./PUBLIC_RELEASE_STATUS.json).

Many historical reports and machine-readable companions were originally generated while the research remained under confidential trade-secret controls. Some of those files therefore still contain legacy markings such as *Proprietary Confidential Information*, *Trade Secret*, *Do Not Distribute*, or similar language. For the copies publicly contained in this repository, those markings are retained only as historical provenance and are superseded by the top-level public-release declaration.

The public-release declaration changes confidentiality and trade-secret status only. It does **not** waive copyright or replace the applicable repository licenses. Software remains governed by [`LICENSE-CODE.md`](./LICENSE-CODE.md), and papers, reports, documentation, figures, and other non-code scholarly materials remain governed by [`LICENSE-PAPER.md`](./LICENSE-PAPER.md).

---

## How the research developed

### Observation came first

The K-Field research trajectory began with empirical measurement rather than with a selected physical constant or a preferred theoretical model. Across a series of experiments, repeated measurements showed anisotropic or direction-dependent behavior in metastable systems. Correlations with lunar motion, Earth rotation, orbital motion, and other celestial cycles initially suggested external modulation.

A central interpretive change occurred when those celestial motions were treated as **sampling motions** rather than as the presumed causes of the measured signals. In this view, rotation and translation of the laboratory provide changing position, orientation, and time coordinates with which a persistent anisotropic structure can be indexed and tested.

That change reframed the research question. Instead of asking only which celestial body might be producing a local signal, the program began asking whether a common geometric organization could be recovered independently across different observational systems.

### Cross-domain search

The investigation consequently expanded across local experiments, precision timing, spectrophotometer data, Kepler observations, galaxy-scale orientation statistics, and later comparisons with known physical quantities. These domains use different instruments and observables, but they provide independent opportunities to test recurring orientation, phase, recurrence, and geometric relationships.

Local observations motivated lattice-like geometric models. Kepler analyses provided an astronomical trajectory dataset for testing recurrence away from the laboratory. Galaxy orientation data then supplied the large-population astronomical dataset from which the foundational rhombohedral geometry was reconstructed.

This historical order matters: the geometry was not selected from a table of physical constants and then projected backward onto the observations. In the research chronology, the astronomical geometric reconstruction precedes the later constant-spectrum comparison work.

---

## The astronomical foundation: galaxy-axis orientation, not galaxy position

The foundational galaxy analysis requires a distinction that is easy to miss.

A galaxy catalog contains information about **where galaxies appear on the sky**, but galaxies also have measurable **axis orientations**. Those are different observables. Sky coordinates describe galaxy locations. Axis-orientation measurements describe how the galaxies themselves are oriented.

The K-Field reconstruction uses galaxy-axis orientation information associated with the **Siena Galaxy Atlas**. The axis orientations are represented as a directional population on the unit sphere and analyzed in a celestial reference-frame context using the **International Celestial Reference System (ICRS)**; the archive also records the galactic-reference registration used in that orientation analysis. The object being analyzed is therefore **galaxy-axis orientation density on the unit sphere**, not ordinary galaxy sky-position density.

This distinction defines the provenance of the geometry. The oriented rhombohedral model was derived as a fit to organized structure in the galaxy-axis directional population. It was not obtained by plotting galaxy locations on a celestial map, and it was not constructed from CODATA constants.

In the archive reconstruction, the fitted directional structure is represented by three associated plane systems. Their intersections define an oriented rhombohedral primitive-cell model called **Cell3** in the archive. Cell3 preserves the fitted directional relationships, face geometry, basis orientation, and metric structure recovered in the reconstruction.

Earth and a terrestrial laboratory can also be represented in ICRS. Earth rotation, orbital motion, epoch, laboratory orientation, and motion relative to the **Cosmic Microwave Background (CMB)** can therefore be expressed in a common coordinate framework for comparison with the fixed astronomical orientation model.

The foundational reconstruction materials are collected in [`Start_Here`](./Start_Here/) and the independent educational reconstruction path is preserved in [`Student_reconstruction_process`](./Student_reconstruction_process/).

---

## From the rhombohedral cell to explicit mathematics

The archive uses several historical project names. For accessibility, each is best understood through the conventional mathematical object it denotes.

### Cell3 — oriented rhombohedral primitive cell

**Cell3** is the archive name for the corrected oriented rhombohedral primitive-cell model. It is represented by three basis vectors and the associated direct Gram metric, face areas, volume, reciprocal metric, plane families, and orientation in the working celestial reference frame.

### Devon Dimension — compact direct/reciprocal metric representation

The **Devon Dimension** is the archive name for the compact algebraic representation constructed from Cell3. It collects the direct metric, reciprocal metric, cofactors, face-area channels, scalar quantities, quadratic-form rule, and branch interfaces used by later analyses. Here, *dimension* is historical terminology for an algebraic coordinate representation; it does **not** mean an additional spatial dimension.

### Mass Bridge — projective face-area ratio closure

The **Mass Bridge** is a project-specific name for a closed system of dimensionless ratios formed from the three primitive Cell3 face areas. Because all three quantities are areas, their ratios are independent of uniform scale. The research compares these geometric ratios with the proton–electron mass ratio, the fine-structure constant, and related derived physical quantities.

Within the K-Field derivation chain, those physical comparisons occur **after** the geometric reconstruction. They are treated as downstream relationships and consistency tests of the geometric model rather than as inputs used to choose the rhombohedral geometry.

### Lucas Limit — finite 27-node address graph

The **Lucas Limit** is the archive name for the centered 27-node address graph on the discrete set $\{-1,0,1\}^3$, equivalent to the Cartesian-product graph $P_3 \square P_3 \square P_3$. Evaluating the reciprocal-metric quadratic form

$$
q(s)=s^T R s
$$

on these address vectors produces the archive's **q-spectrum**. The graph also carries an alternating parity/incidence labeling and finite shell structure.

### Emily Eigen-spectrum — graph adjacency spectrum

The **Emily Eigen-spectrum** is the archive name for the adjacency eigenspectrum of the finite Lucas graph. In conventional graph-theoretic language it is the spectrum of the adjacency operator on $P_3 \square P_3 \square P_3$.

### Jack Jacobian — logarithmic perturbation Jacobian

The **Jack Jacobian** is the archive name for the derivative map that relates coherent changes in the primitive geometric directions to logarithmic changes in selected derived quantities. It is a perturbation/sensitivity Jacobian, not a separately introduced force law.

### Lucas Supergroup — recursive 9 × 9 × 9 cell complex

The historical term **Lucas Supergroup** denotes the larger recursive $9\times9\times9$ Cell3 aggregation used in later graph and volumetric studies. The name is retained for archival continuity; mathematically, the object is treated as a recursive finite cell complex rather than as a use of *supergroup* in its standard algebraic sense.

These project names remain important because they identify historical reports, filenames, figures, and machine-readable objects. The archive therefore preserves the original names while pairing them with explicit geometric, metric, graph-theoretic, or differential descriptions.

---

## From geometry to physical-quantity comparisons

Once the Cell3 geometry is fixed, ratios among its faces and other derived quantities form a connected algebraic dependency network. The research compares this network with the **proton–electron mass ratio**, **fine-structure constant**, **Bohr radius, atomic velocity, Rydberg constant, Hartree energy, classical electron radius, vacuum impedance**, gravitational quantities, and other standard physical values.

The archive's historical term **lock** refers to a downstream numerical or structural closure/comparison in this dependency network. The current 29-lock set is organized as a **29-member witness/comparison ledger** consisting of selected non-gravitational comparisons and observer-context gravitational-family comparisons. The constants are comparison targets after model quantities have been generated; they are not the source data from which the galaxy-derived rhombohedral geometry was constructed.

A separate scalar branch develops the gravitational relationships and their observer-context transformation. The finite-graph branch develops reciprocal-metric sampling, parity structure, graph spectra, recursion, and perturbation analysis. These branches share the same Cell3/metric foundation but represent different mathematical operations and should not be conflated.

The machine-readable graph structures and closure records are collected in [`Typed_Graphs`](./Typed_Graphs/), while later geometric, spectral, energetic, and projective extensions are collected in [`Discovered_Pathways`](./Discovered_Pathways/).

---

## Experimental and computational research

A major objective of the K-Field program is to test whether orientation-dependent structure derived in the astronomical reconstruction can be compared with independently measured laboratory and observational time series.

### Galaxy and celestial geometry

[`Galaxy_Analysis`](./Galaxy_Analysis/) contains galaxy-axis orientation, unit-sphere population, plane-system, Cell3, and related reconstruction studies. [`CMB_Modulation`](./CMB_Modulation/) develops Earth-trajectory and CMB-referenced coordinate analyses used to describe terrestrial sampling motion in a larger reference-frame context.

### Precision oscillator metrology

[`OCXO_Experiments`](./OCXO_Experiments/) contains the Dual-OCXO D101 studies. Orthogonally oriented oven-controlled crystal oscillators are compared through heterodyne, timing, and phase-sensitive measurement. The analyses examine directional frequency differentials, recurring celestial-coordinate crossings, long-duration recurrence, phase behavior, and time-frequency structure.

The directory also contains the public [`d101_source_data.zip`](./OCXO_Experiments/d101_source_data.zip) source-data archive used with the D101 studies.

### Rotating multispectral measurements

[`Spectrophotometer_Studies`](./Spectrophotometer_Studies/) contains rotating wavelength-resolved measurements and their geometric analysis. The work examines angular dependence across spectral channels, antipodal relationships, photon-energy mappings, Bragg-style geometric comparisons, interplanar-spacing models, unit-sphere coherence, and comparisons with Cell3 and astronomical reference-frame geometry.

### Applied devices and mechanics

[`Applied_Devices_Analysis`](./Applied_Devices_Analysis/) contains exploratory engineering and mechanics studies involving rotation, inertia, force-vector decomposition, flywheels, rotors, materials, apparent-weight measurements, and proposed device geometries. These records document the applied branch of the research program and the experiments or models proposed to test it.

### Derived mathematical pathways

[`Discovered_Pathways`](./Discovered_Pathways/) collects later deductions and extensions involving projective and reciprocal geometry, finite graph recursion, harmonic relationships, quadratic orientation surfaces, propagation models, internal-energy organization, and other structures derived from or compared with the core geometric framework.

---

## How to begin

For a first encounter with the research, begin with **[K-Field: An Introduction](./Start_Here/K-Field_An_Introduction.pdf)**. It provides the shortest conceptual entry before the detailed reconstruction chain.

The [`Start_Here`](./Start_Here/) directory then presents the core progression from the native galaxy-derived geometry through Cell3, the projective face-ratio system, the physics-formula comparison bridge, and the 29-member closure/comparison ledger.

Readers who want to reproduce the derivation step by step should continue to [`Student_reconstruction_process`](./Student_reconstruction_process/). The [`Step_by_Step_Galaxy_to_100_physics_formulas`](./Student_reconstruction_process/Step_by_Step_Galaxy_to_100_physics_formulas/) directory organizes the reconstruction as an educational sequence, while [`Galax_Derivation_Methods`](./Student_reconstruction_process/Galax_Derivation_Methods/) preserves multiple galaxy-to-Cell3 reconstruction methods. The historical directory name `Galax_Derivation_Methods` is retained for path stability and is cross-referenced to the canonical term *Galaxy Derivation Methods* in the machine-readable topic index.

For structured introductory teaching material, see the [`Lectures`](./Lectures/) directory. It contains the K-Field 101 educational lecture series and related explanatory material.

---

## Repository map

| Path | Contents |
|---|---|
| [`Start_Here/`](./Start_Here/) | Public introduction and core galaxy-axis → Cell3 → face-ratio → physics-comparison reconstruction sequence |
| [`Student_reconstruction_process/`](./Student_reconstruction_process/) | Step-by-step educational reconstruction and alternate galaxy-axis derivation methods |
| [`Galaxy_Analysis/`](./Galaxy_Analysis/) | Galaxy-axis orientation, unit-sphere population, plane-system, and Cell3 analysis |
| [`Typed_Graphs/`](./Typed_Graphs/) | Dependency graphs, reconstruction kernels, closure records, and unified typed-graph representations |
| [`Discovered_Pathways/`](./Discovered_Pathways/) | Projective, reciprocal, graph, harmonic, propagation, and energy-structure extensions |
| [`CMB_Modulation/`](./CMB_Modulation/) | Earth/CMB reference-frame and trajectory-indexing analyses |
| [`OCXO_Experiments/`](./OCXO_Experiments/) | D101 dual-OCXO metrology, celestial-coordinate recurrence studies, and source-data archive |
| [`Spectrophotometer_Studies/`](./Spectrophotometer_Studies/) | Rotating multispectral, photon-energy, geometric, spherical-coherence, and Cell3 comparison studies |
| [`Applied_Devices_Analysis/`](./Applied_Devices_Analysis/) | Applied mechanics, force, inertia, rotor, flywheel, material, and device analyses |
| [`Lectures/`](./Lectures/) | K-Field 101 educational lecture series |
| [`Commentary/`](./Commentary/) | Conceptual frameworks, explanatory treatments, educational drafts, implications, and synthesis records |
| [`Press_Release/`](./Press_Release/) | Investigator biography, press package, and media-facing material |
| [`Assets/`](./Assets/) | Repository visual assets and Quantum K-Field logo |

---

## Machine-readable discovery and indexing

The archive is intended to be readable by both people and automated research systems.

The top-level **[Quantum K-Field Topic and Keyword Index](./Quantum-K-Field_topic_keyword_index_20260806T200100Z.json)** provides the machine-readable vocabulary for the archive. It connects canonical scientific topics to project-specific archive terms, aliases, abbreviations, historical spellings, and legacy filename forms. This allows historical filenames to remain stable while search systems can resolve them to more explicit terminology.

The index spans astronomical orientation analysis, ICRS and CMB reference frames, anisotropy, direct and reciprocal metric geometry, finite graph methods, precision and frequency metrology, OCXO signal analysis, wavelength-resolved photometry, optical and Bragg-style geometry, Fourier and wavelet analysis, recurrence and coherence methods, nonlinear analysis, instrumentation, materials studies, and reproducible research. It also cross-references broader theoretical and literature contexts used for comparison, including foundational physics, quantum geometry, emergent-spacetime models, structured-vacuum models, quantum sensing, and experimental gravitation.

Additional machine-readable entry points include:

- [`CITATION.cff`](./CITATION.cff) for repository citation metadata and research keywords;
- [`Typed_Graphs/`](./Typed_Graphs/) for dependency graphs, reconstruction kernels, validation records, and unified typed representations;
- paired `.json` companions beside many archival `.pdf` reports; and
- [`PUBLIC_RELEASE_STATUS.json`](./PUBLIC_RELEASE_STATUS.json) for machine-readable public-release and confidentiality-status interpretation.

Search engines, archival systems, AI systems, and other automated agents should use the canonical vocabulary in the topic index while retaining legacy aliases when resolving historical filenames.

---

## Reproducibility and provenance

The archive is organized so that a reader can follow the path from measured observation to geometric extraction, from geometry to mathematical representation, and from mathematical representation to experimental or physical-quantity comparison.

Many research packages preserve a human-readable PDF together with a machine-readable JSON companion. Those JSON files commonly record generation metadata, source relationships, parameters, derived quantities, and checksums. Source-data archives are included where they have been released publicly, and the student reconstruction directories provide an independent pathway through the foundational derivation.

Historical terminology and filenames are generally retained rather than rewritten after publication. This preserves the chronological research record. The machine-readable topic index supplies canonical terminology and reverse mappings so that older archive names can coexist with explicit scientific descriptions.

Independent reproduction, alternative analysis, documented correction, and technically grounded critique are welcome.

---

## External scientific references

The K-Field archive uses established astronomical reference systems, catalogs, and physical constants as external reference material. Useful primary reference points include:

- [Siena Galaxy Atlas 2020](https://sga.legacysurvey.org/) — the astronomical catalog used for the galaxy-orientation reconstruction;
- [International Earth Rotation and Reference Systems Service — ICRF/ICRS](https://www.iers.org/IERS/EN/DataProducts/ICRF/ICRF/icrf) — the international celestial reference-system context;
- [NIST Fundamental Physical Constants](https://physics.nist.gov/cuu/Constants/) — CODATA reference values for fundamental physical constants; and
- [NASA LAMBDA](https://lambda.gsfc.nasa.gov/) — public Cosmic Microwave Background data and reference resources.

These external sources provide reference data and standards. The K-Field derivations, models, experimental interpretations, and machine-readable records are contained within this archive.

---

## Citation

Repository-level citation metadata is provided in [`CITATION.cff`](./CITATION.cff).

When citing a specific paper, dataset, machine-readable analysis, or reconstruction package, cite the specific artifact in addition to the repository. Preserve its filename or version identifier so the referenced record remains reproducible.

**Principal Investigator:** P. Dwayne Esterline  
**Research Program:** Krytronx Quantum K-Field Research  
**Public Archive:** Quantum K-Field Public Release

---

## Licensing

Copyright © 2026 Krytronx, LLC.

**Software and code** are governed by [`LICENSE-CODE.md`](./LICENSE-CODE.md) under **GNU AGPL-3.0-only**, unless a specific source file states a different applicable license.

**Papers, reports, documentation, figures, diagrams, and other non-code scholarly materials** are governed by [`LICENSE-PAPER.md`](./LICENSE-PAPER.md) under **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**, unless a specific artifact states a different applicable public license.

The [`PUBLIC_RELEASE_STATUS.json`](./PUBLIC_RELEASE_STATUS.json) declaration removes prior confidentiality and trade-secret restrictions from public repository copies but does not alter these copyright licenses. Historical confidentiality language embedded in older artifacts should therefore be read as provenance, not as the current distribution status of the public copy.

Alternative licensing and commercial-use inquiries may be directed to `dwayne.esterline@krytronx.com`.

---

## About the principal investigator

**P. Dwayne Esterline**  
Principal Investigator, Krytronx Quantum K-Field Research  
BS, Huntington University, 1999  
MBA, Indiana Wesleyan University, 2008  
Contact: `dwayne.esterline@krytronx.com`

---

## Follow the research

Star the repository to support its visibility and watch the project for new papers, machine-readable analyses, datasets, experimental results, educational materials, and public research packages.

The archive is organized around a traceable research chain: **from experimental anisotropy to celestial indexing, from galaxy-axis orientation data to geometric reconstruction, from geometry to explicit metric and graph mathematics, and from those mathematical structures to laboratory and physical-quantity comparisons.**
