# Construction Materials Lab — Mix Design & Strength Prediction

Live site: https://conslmhoang.github.io/construction-materials-lab/

A browser-only tool for fiber-reinforced cementitious and geopolymer composites (ECC/SHCC, UHPC, UHP-ECC):

1. **Mix design**: proportions → kg per m³ and per batch, with cost, embodied energy and CO₂ (20 materials, the same ones the model uses).
2. **Strength prediction**: compressive strength and tensile strain capacity from the mix,
   curing method/temperature/duration, test age and the fiber length, diameter, strength and modulus. It includes an 80% range, a strength-vs-age table,
   and a Save button that adds a result to the prediction log.
3. **Logs**: every mix design and batch is logged, predictions when you press Save; each row can be deleted (×), and the logs download as Excel/CSV.

| Page | What it shows |
|---|---|
| `index.html` | Calculator + prediction |
| `benchmark.html` | 10 ML models compared (10-fold cross-validation, random split) |
| `data.html` | The 485 source papers |

## Excel files: `excel/`

| File | Content |
|---|---|
| `Materials_20.xlsx` | Density, energy (MJ/kg), CO2 (kg/kg) and cost ($/kg) of the 20 materials, plus the suggested fiber length, diameter, tensile strength and elastic modulus, each with its source. The web can load it (Load material database from Excel). Rebuild: `python ml_spike/build_materials_xlsx.py` |
| `04 Dataset_web.xlsx` | Training data of the ML models (below) |

## Training data: `excel/04 Dataset_web.xlsx`

One sheet, one row per mix and test age, and only the columns the web has:

| Columns | Content |
|---|---|
| Paper, DOI | source paper |
| 20 materials | same names and units as the calculator (`materials21.json`): cement + fly ash + GGBS = the binder (shares add up to 1), the other 14 = mass ratio to that binder, 3 fibers (PE, PVA, steel) = vol%. PBO fiber was removed |
| 12 fiber properties | length (mm), diameter (µm), tensile strength (MPa) and elastic modulus (GPa) of each fiber type as reported in the paper; blank = not reported. The strain model uses all four (volume-weighted); a value the paper does not report = the reference value in `materials21.json` (PE and PVA: the fiber of Prof. Bang Yeon Lee's lab; steel: 10.3390/ma15051668), the same value the web suggests |
| 4 conditions | curing method, curing temperature (°C), curing duration (days), test age (days) |
| 2 outputs | compressive strength (MPa), tensile strain capacity (%); blank when not used |

`ml_spike/web_data.py` turns each row into the model inputs with the same rules as the web page,
so training and the web compute identical numbers. `03 Dataset_ratio.xlsx` is the full extraction
(773 columns) that this file is built from.

## Models (10-fold CV, random split, mean of 3 seeds)

| Output | Rows / papers | Model | R² | MAE |
|---|---|---|---|---|
| Compressive strength | 2,057 / 382 | Extra Trees × Abrams W/P + age curve | 0.94 | 7.6 MPa |
| Tensile strain capacity | 911 / 280 | Extra Trees × age curve | 0.78 | 1.00 % |

The strain model also uses the fiber length, diameter, tensile strength and elastic modulus; the compressive-strength
model does not (they did not improve it).

NaOH given only as a molar solution is converted to NaOH solids + water with the OxyChem Caustic Soda Handbook,
Table 1 (density and NaOH content at 60 °F): `ml_spike/additions_v2/naoh_solution.py`, `ml_spike/reference/naoh_solution_table.csv`.

The compressive-strength model is one model: Extra Trees that learn the deviation from an Abrams curve
(log fc = a + k · W/P + c · log(age), W/P = water / (cement + FA + GGBS + SF + MK + LP), fitted on the data: fc ≈ 166 · e^(−4.50 · W/P) · age^0.077). Trees alone often did not lower the
strength when more water was added: +0.05 water left the Extra Trees prediction unchanged or higher for 26 % of the mixes,
with the curve for 0.1 % (`ml_spike/bench10/abrams_check.csv`). The curve gives the right trend, not the right level for
every lab: for our high-fly-ash ECC-PE mix (air curing, 7 d, 47.4 MPa measured) Extra Trees alone predicted 60 MPa and the
curve model 31.9 MPa without the lab test as a training row (below). In the 10-model comparison every model gets the same Abrams curve for
compressive strength. Averaging with CatBoost or weighted stacking added only about 0.006 R², so the web keeps one model.

Strength and age (Nov 2026): in the papers the same mix is stronger at the later age in 95 % of 530 pairs. With age left to
the trees only, the predicted strength fell at a later age for 25 % of the mixes (e.g. our ECC-PE mix: 46.7 MPa at 7 d,
46.1 at 14 d). The log(age) term in the curve cut that to 8 % and raised R² from 0.937 to 0.941; the web shows the highest
value of the model at that age and the earlier ages 1, 3, 7, 14, 28, 56, 90, 180 d, so strength never falls with age.
Strain and age (Nov 2026): tensile strain capacity is taken to fall with age. The 23 papers in which the strain of a mix
rose at a later age were left out as a whole (our choice; `DROP_DOI` in `build_web_dataset.py`, 184 strain and 88
compressive-strength values). Before, strain rose in 49 and fell in 52 of 106 same-mix pairs; now it rises in none.
The strain model is Extra Trees × an age curve, strain ∝ (age / 28)^−0.116, the median slope of the 22 mixes still measured
at several ages (28 d ≈ 0.85 × 7 d), and on the web strain never rises at a later age.

Strain audit (Nov 2026): the 30 papers with the largest strain errors were checked against the papers. Every strain
value matched; the errors were in the inputs. 63 rows were removed (marble powder entered as limestone, curing that is not
one web method or has no stated temperature, unstated admixture dosage, one paper that could not be checked), curing labels,
water (from the mix table) and hybrid PVA fiber properties were corrected, and compressive strengths read from figures were
removed. Edits: `ml_spike/audit/corrections.json` (applied by `build_web_dataset.py`), evidence: `ml_spike/audit/report_*.md`.
On the rows the audit did not touch, the strain MAE fell from 1.00 to 0.95 %.

Own lab test (Nov 2026): one ECC-PE mix tested in the CNU lab (air curing, 7 days, CNU PE fiber; fc 47.38 MPa, tensile
strain 7.02 % = mean of 3 direct tension specimens) is a training row (`ml_spike/additions_v2/z_lab_cnu.csv`, source: the
lab test sheet), counted as one source in the table above. Our own lab tests count 10 times in training (`LAB_WEIGHT` in
`train_export.py`), because the web is used for our lab's mixes. Before the test was added the web predicted 34.5 MPa and
6.67 % for this mix at its real conditions; now 46.8 MPa and 7.00 %, and 50.9 MPa / 5.95 % at 28 d (the test itself is in the training data, so this
shows the fit to our lab, not the error on a new mix). The overall scores did not change.

## Rebuilding

```
cd ml_spike
python build_web_dataset.py              # 03 Dataset_ratio.xlsx -> excel/04 Dataset_web.xlsx
python benchmark10.py                    # compare 10 models (benchmark.html)
python train_export.py ../strength_model.js   # models for the web
python build_sources_json.py             # data/sources.json (data.html)
cd .. && python embed_materials.py "01 Datamix.xlsx" index.html   # material database
```

Python environment: `ml_spike/.venv` (pandas, scikit-learn, catboost, xgboost, matplotlib, openpyxl).

Le Minh Hoang — Construction Materials Lab, Chonnam National University (Prof. Bang Yeon Lee).
