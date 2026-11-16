# Brief for paper-extraction agents (wave 5, 21-material list)

Goal: add published fiber-reinforced cementitious / geopolymer composite mixes to the dataset that trains the
compressive-strength and tensile-strain models of the web calculator. Every number must come from the paper.

## The 21 allowed materials (a mix may use ONLY these; defoamer / anti-foamer is also allowed, record it in notes)
Binder: cement (OPC/PC, any Portland type), fly ash, GGBS (slag).
Other: silica fume, metakaolin, limestone powder, sand (any natural/silica/river/manufactured fine sand),
crumb rubber, EPS beads, water (ice counts as water), superplasticizer (SP / HRWR / PCE / P-SP),
VMA (incl. HPMC / methylcellulose), NaOH, Na2SO4, Na2SiO3 (SSM / ASM / SMA / SMP; SMP pentahydrate -> convert to
anhydrous x0.575 and add the 0.425 to water, note it), water glass (sodium silicate solution), Ca(OH)2.
Fibers: PE (incl. UHMWPE, Dyneema, Spectra, selvage PE), PVA, steel (any shape), PBO.
NOT allowed (skip such mixes; keep the paper's other mixes if they qualify): quartz powder/flour, nano-silica,
rice husk ash, PP/basalt/glass/carbon/PET/natural fibers, coarse aggregate, calcium sulfoaluminate or aluminate
cement, MgO, any other mineral or chemical admixture (expansive agent, SRA, accelerator, retarder, nano materials).

## Inclusion
Mix proportions of every included mix AND compressive strength and/or tensile strain capacity from a DIRECT
(uniaxial / dog-bone / dumbbell) tension test. At least one fiber. Ordinary test conditions only (no fire,
freeze-thaw, impact, chloride, carbonation, pre-cracking, high strain rate exposure before the test).
Prefer papers that report both outputs, and several mixes or ages.

## Files (D = ml_spike\additions_v2)
- `D\existing_dois.txt` — DOIs already in the dataset or rejected before. SKIP them. Right before writing,
  also read every `D\w5_*.csv` and `D\w5_*_rejected.txt` of the other agents and drop DOIs already there.
- Header: exactly the 99 columns of `ml_spike\additions\TEMPLATE.csv`, same order. Example of conventions:
  `ml_spike\extract_scripts\paper_news_2026_11.py` and `D\paper_news.csv`.
- Write `D\w5_<yourname>.csv` with pandas, `encoding="utf-8-sig"`. Builder script: `ml_spike\extract_scripts\w5_<yourname>.py`.
  Rejected papers (DOI + one-line reason): `D\w5_<yourname>_rejected.txt`.

## Conventions (same as before)
- One row per mix x curing condition x test age. "Article Name", "Author", "Year", "DOI / URL" (https://doi.org/...) on every row.
- Binder B = the binder as the paper defines it; binder-composition columns (OPC / Cement, GGBS, FA (Fly ash),
  SF (Silica fume), Metakaolin, Limestone powder) are mass fractions of B summing to 1 when those are in the
  paper's binder. Activators and everything else: "X / B" = mass of X / mass of B (e.g. "Ca(OH)2 / B",
  "SSM / B (Na2SiO3 anhydrous)", "WG / B (Water glass)", "NaOH / B", "Na2SO4 / B"). If the paper puts an activator
  inside its binder, still give it as "X / B" of that same B (the build script re-expresses all ratios per cement+FA+GGBS).
- kg/m3 -> divide by binder kg/m3; note it in "Conversions / notes"; fill "Binder content (kg/m³)".
- "W / B": all water incl. ice; do NOT add the water inside water glass (note WG solids if given).
- SP: "SP / B" (liquid as dosed). VMA/HPMC: "VMA / B" or "HPMC / B ...". Sand: "SS / B (Silica sand)",
  "River sand / B", "M-sand / B", or "Sand (type not stated) / B". Crumb rubber "Crumb rubber / B", EPS "EPS / B".
- Fibers in vol% (2 = 2 vol%): "PE fiber (vol%)", "PVA fiber (vol%)", "Steel fiber (vol%)", "PBO fiber (vol%)",
  plus "Total fiber (vol%)". kg/m3 -> vol% with the paper's density, else steel 7850 / PVA 1300 / PE 970 / PBO 1560.
- Curing: free text in "Curing method" (say water / sealed / moist room / air / steam / heat + °C), "Curing time (days)",
  "Curing temperature (°C)", "Curing RH (%)", "Test age (days)", "Heat curing duration (h)" for heat/steam curing.
- Outputs: "Compressive strength (MPa)", "Tensile strength (MPa)", "First-cracking strength (MPa)",
  "Tensile strain capacity (%)" in PERCENT (0.03 mm/mm -> 3). "Tensile test type": "direct (uniaxial)" etc.
- Unknown -> empty. Never guess. Values read off a figure or derived (e.g. from ratios) -> note starts with VERIFY.
- "Source table/page", e.g. "Table 2 (mix), Table 4 (fc)".

## Access (what worked before)
- Search: WebSearch, Crossref API (`https://api.crossref.org/works?query=...&filter=has-full-text:true,from-pub-date:2010`),
  NCBI E-utilities for PMC.
- Full text: Europe PMC `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML` (MDPI, Heliyon, PLOS ...),
  DOI -> PMCID via `https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=<DOI>&format=json`.
  Frontiers, Scientific Reports, SpringerOpen (IJCSM 10.1186/s40069-...), Developments in the Built Environment,
  Case Studies in Construction Materials, J. Building Engineering OA articles, Results in Engineering (Elsevier OA HTML) usually work.
- Skip papers whose mix table or results you cannot read as text, or whose results are only in figures.

## Before finishing (pandas checks)
Header identical to TEMPLATE; binder fractions ~1; no excluded material; no duplicate DOI (existing + other w5 files);
strain in %; plausible ranges (W/B 0.12-0.7, fc 5-250 MPa, strain 0-20 %, fiber 0.1-6 vol%).

## Final report (short)
Papers added (count + DOIs), rows, papers rejected, doubtful values.
