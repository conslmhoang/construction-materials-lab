# Brief for paper-extraction agents

Goal: grow an ML dataset that predicts compressive strength (fc), tensile strength (ft) and tensile
strain capacity of fibre-reinforced cementitious / geopolymer composites (ECC, SHCC, UHPC, HPFRCC,
fibre-reinforced mortars). Every number must come from the paper. Quality over quantity.

## Files (directory D = this folder, ml_spike\additions)
- `existing_papers.txt` — DOIs already collected or already rejected. SKIP all of them. Also check
  other agents' `w*_*.csv` files in D right before you write, and drop any DOI already there.
- `TEMPLATE.csv` — exact 99-column header. Your CSV uses it, same order.
- `pvaecc.csv`, `geopolymer.csv`, `uhpc_steel.csv` — finished examples; copy their conventions.
- Write output with pandas, UTF-8 with BOM (`encoding="utf-8-sig"`). Builder script goes to
  `D\..\extract_scripts\<name>.py`. Rejected papers + one-line reason go to `<name>_rejected.txt`.

## Access
mdpi.com / PMC HTML pages often return 403 or a CAPTCHA, and the Europe PMC *search* API may return 503.
What works:
- Find candidates with WebSearch, Crossref (`https://api.crossref.org/works?query=...&filter=has-full-text:true`),
  or NCBI E-utilities (`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pmc&term=...`).
- Convert DOI → PMCID: `https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=<DOI>&format=json`.
- Full text: `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML` (reliable).
- Frontiers / J-STAGE / SciELO HTML pages also usually work.
Do not download PDFs to disk; skip papers you cannot read as text.

## Inclusion
Mix proportions AND at least fc or a tensile value. fc-only papers are welcome.
"Tensile test type": "direct" (uniaxial / dog-bone), "splitting", or "flexural".
Skip ordinary concrete with coarse aggregate > 0.5 × binder.

## Conventions
- One row per mix × curing condition × test age. Title, authors, year, DOI (https://doi.org/...) on every row.
- Binder B = cementitious/powder binder as the paper defines it. Binder-composition columns are mass
  fractions of B summing to 1. Quartz powder is not binder → "QP / B (Quartz powder)".
- "X / B" = mass of X ÷ binder mass. kg/m³ → divide by binder kg/m³; record in "Conversions / notes";
  fill "Binder content (kg/m³)" when known.
- Activators: "WG / B", "NaOH / B", "Ca(OH)2 / B", "Na2SO4 / B", "SSM / B (Na2SiO3 anhydrous)",
  "Na2CO3 / B (anhydrous)"; plus "Activator modulus Ms (SiO2/Na2O)", "NaOH molarity (M)" if given.
- Fibres in vol% (2 = 2 vol%). kg/m³ → vol% with the paper's density, else steel 7850 / PVA 1300 /
  PE 970 / PP 910 (note it). Always fill "Total fiber (vol%)".
- Curing temperature °C, curing time days, RH %, test age days, "Heat curing duration (h)",
  free-text "Curing method".
- Outputs: "Compressive strength (MPa)", "Tensile strength (MPa)", "First-cracking strength (MPa)",
  "Tensile strain capacity (%)" in PERCENT (0.03 mm/mm → 3).
- Unknown → empty. Never guess. Values read off a figure or derived from % changes: note starts with VERIFY.
- "Source table/page", e.g. "Table 2 (mix), Table 4 (fc)".

## Before finishing (pandas)
Header identical to TEMPLATE; binder fractions ≈ 1; no DOI from existing_papers.txt or other agents' files;
strain in %; plausible ranges (W/B 0.1–0.7, fc 2–250, direct ft 0.5–25, strain 0–15, fibre 0–6 vol%).

## Final report (short)
Papers and rows added, DOIs, doubtful values.

## Sources that worked well in earlier waves (prefer these)
- SpringerOpen journals: International Journal of Concrete Structures and Materials (IJCSM, DOI 10.1186/s40069-...),
  Journal of Asian Architecture and Building Engineering, Construction & Building Materials OA mirrors are NOT reliable.
- Frontiers in Materials / Frontiers in Built Environment (10.3389/...) — HTML pages and table pages work.
- Scientific Reports (10.1038/s41598-...) — HTML works.
- J-STAGE (Journal of Advanced Concrete Technology) — PDF only, skip.
- Europe PMC fullTextXML for MDPI / Heliyon / PLOS.
Most rejections so far: results only in figures. Check the tables/text quickly before investing in a paper.
