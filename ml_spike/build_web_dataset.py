"""Build the training file "04 Dataset_web.xlsx" with exactly the web's inputs:

  Paper, DOI | 21 materials (materials21.json) | curing method, curing temperature, curing duration, test age |
  compressive strength, tensile strain capacity

Rules
- A row is kept only if every material in it is one of the 21 (defoamer / anti-foamer is allowed but not listed).
  Rows of the same paper that use only the 21 materials are kept even if other rows of that paper are not.
- Binder = cement + fly ash + GGBS; their shares add up to 1. Anything the paper counted in its binder
  (silica fume, metakaolin, limestone powder, Ca(OH)2, Na2SiO3 ...) becomes a ratio to this binder:
  every "x / paper binder" value is divided by (cement + FA + GGBS share of the paper binder).
  The kg per m3 of the mix do not change; only the base of the ratios does.
- All sands -> "Sand"; SP + HRWR + water reducer -> "Superplasticizer (SP)"; VMA + HPMC -> "VMA";
  PE + selvage PE -> "PE fiber"; all steel fibers -> "Steel fiber". Ice is already inside W/B in the source.
- Curing: one of the web's 5 methods. Missing temperature -> 20 °C for non-heat methods. Duration: days at high
  temperature for heat curing (from "Heat curing duration (h)" when given), otherwise days of curing,
  and the test age when the paper does not say. Relative humidity is not used.
- Only rows that pass the cleaning (clean/dataset_clean.csv) plus the rows in additions_v2/*.csv.

Usage:  python build_web_dataset.py
"""
import os, re, json, glob
import numpy as np, pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
SRC = os.path.join(root, "03 Dataset_ratio.xlsx")
OUT = os.path.join(root, "04 Dataset_web.xlsx")
M21 = json.load(open(os.path.join(root, "materials21.json"), encoding="utf-8"))["materials"]
NAME = {m["key"]: m["name"] for m in M21}

# ---- source columns (03 Dataset_ratio.xlsx, 0-based) for each of the 21 materials
BINDER_FRAC = {"Cement": [4], "FA": [8], "GGBS": [7], "SF": [9], "MK": [10], "LP": [11]}   # shares of the paper binder
PER_B = {"WG": [67], "NaOH": [68], "CaOH2": [69], "Na2SO4": [70], "Na2SiO3": [71],
         "Sand": [86, 87, 90, 91, 92, 93, 94, 97, 181], "CR": [106], "EPS": [107],
         "SP": [110, 116, 172], "VMA": [117, 118]}
FIBER = {"PE": [182], "PVA": [189], "Steel": [199, 206, 207, 281, 282, 289], "PBO": [211]}
WATER_COLS = [83, 84, 85, 131, 132, 134]          # water in any form (W/B already includes ice)
DEFOAMER = [120, 126]
# every other material-amount column = not allowed
OTHER = [5, 6, 12, 13, 14, 15, 16, 17, 18, 19, 37, 55, 72, 88, 95, 96, 102, 103, 104, 105, 108, 109, 111, 119,
         124, 125, 138, 139, 148, 156, 161, 173, 174, 217, 227, 235, 241, 242, 271, 295, 303, 313]
assert not set(OTHER) & set(sum(list(BINDER_FRAC.values()) + list(PER_B.values()) + list(FIBER.values()), []))

raw = pd.read_excel(SRC, "Dataset", header=None)
hdr = raw.iloc[1].astype(str).tolist()
d = raw.iloc[2:].reset_index(drop=True)
d.columns = range(raw.shape[1])
d[0] = d[0].ffill()
d = d[d.iloc[:, 4:].notna().any(axis=1)].reset_index(drop=True)
F = pd.read_csv(os.path.join(here, "clean", "dataset_clean.csv"), encoding="utf-8-sig")
assert len(F) == len(d), (len(F), len(d))
d["_paper"], d["_doi"] = F["paper"].values, F["doi"].fillna("").values
d["_use_fc"], d["_use_eps"] = F["use_fc"].astype(bool).values, F["use_eps"].astype(bool).values

# ---- new papers (same 99-column template as the earlier additions)
for f in sorted(glob.glob(os.path.join(here, "additions_v2", "*.csv"))):
    a = pd.read_csv(f, encoding="utf-8-sig")
    rows = pd.DataFrame(np.nan, index=range(len(a)), columns=d.columns, dtype=object)
    for c in a.columns:
        if c in hdr: rows[hdr.index(c)] = a[c].values
    rows["_paper"], rows["_doi"] = a["Article Name"].values, a["DOI / URL"].values
    tt = a["Tensile test type"].astype(str).str.lower()
    ok = pd.to_numeric(a["W / B"], errors="coerce").notna() & pd.to_numeric(a["Test age (days)"], errors="coerce").notna()
    rows["_use_fc"] = (ok & pd.to_numeric(a["Compressive strength (MPa)"], errors="coerce").notna()).values
    rows["_use_eps"] = (ok & tt.str.contains("direct|uniaxial") & pd.to_numeric(a["Tensile strain capacity (%)"], errors="coerce").notna()).values
    d = pd.concat([d, rows], ignore_index=True)
    print(f"+ {len(a)} rows from {os.path.basename(f)}")

N = lambda i: pd.to_numeric(d[i], errors="coerce").fillna(0)
S = lambda idx: sum(N(i) for i in idx)

other = pd.concat([N(i) != 0 for i in OTHER], axis=1).any(axis=1)
fib = {k: S(v) for k, v in FIBER.items()}
no_fiber_type = sum(fib.values()) == 0
B3 = S(BINDER_FRAC["Cement"] + BINDER_FRAC["FA"] + BINDER_FRAC["GGBS"])     # share of the paper binder
W = pd.to_numeric(d[83], errors="coerce").fillna(pd.to_numeric(d[134], errors="coerce")).fillna(pd.to_numeric(d[85], errors="coerce"))
# papers checked by hand and left out (DOI -> reason)
DROP_DOI = {"10.1155/2022/7876056": "'elongation (%)' equals the tension displacement in mm, no gauge length, no fc",
            "10.1016/j.jobe.2020.101613": "fine aggregate is crushed basalt (basalt is not one of the 21 materials)",
            "10.1016/j.cemconres.2007.12.006": "fc quoted from another paper (ref. [12]), not measured in this study",
            "10.1016/j.ceramint.2021.11.232": "fiber 'vol%' in the text contradicts the kg/m3 in Table 3 (wt% of binder)"}
drop_doi = d["_doi"].astype(str).str.lower().str.contains("|".join(map(re.escape, DROP_DOI)))
keep = (d["_use_fc"] | d["_use_eps"]) & ~other & ~no_fiber_type & (B3 > 0) & W.notna() & ~drop_doi
# W/B below 0.12 is not credible for these composites; with water glass most of the water is inside the WG
# (W/B here is free water only), so the check applies only to mixes without water glass
keep &= (W >= 0.12) | (S(PER_B["WG"]) > 0)

D = pd.DataFrame(index=d.index)
D["Paper"], D["DOI"] = d["_paper"], d["_doi"]
for k, idx in BINDER_FRAC.items():
    D[NAME[k]] = S(idx) / B3.replace(0, np.nan)
for k in ["Sand", "CR", "EPS"]:
    D[NAME[k]] = S(PER_B[k]) / B3.replace(0, np.nan)
D[NAME["Water"]] = W / B3.replace(0, np.nan)
for k in ["SP", "VMA", "NaOH", "Na2SO4", "Na2SiO3", "WG", "CaOH2"]:
    D[NAME[k]] = S(PER_B[k]) / B3.replace(0, np.nan)
for k, v in fib.items():
    D[NAME[k]] = v
D = D[["Paper", "DOI"] + [m["name"] for m in M21]]

# ---- curing and test conditions
cm = d[327].astype(str).str.lower().where(d[327].notna(), "")
T = pd.to_numeric(d[329], errors="coerce")
heat = cm.str.contains("heat|steam|oven|°c") & (T.fillna(20) > 40)
method = np.select([heat, cm.str.contains("water"), cm.str.contains("seal|wrap|plastic"), cm.str.contains(r"\bair\b|ambient")],
                   ["Heat / steam curing", "Water curing", "Sealed / wrapped", "Air (lab ambient)"], "Standard moist room")
age = pd.to_numeric(d[341], errors="coerce").fillna(pd.to_numeric(d[328], errors="coerce"))
days = pd.to_numeric(d[328], errors="coerce")
heat_d = pd.to_numeric(d[345], errors="coerce") / 24
days = np.where(heat & heat_d.notna(), heat_d, days)
days = pd.Series(days, index=d.index).fillna(age)
D["Curing method"] = method
D["Curing temperature (°C)"] = T.where(T.notna(), np.where(heat, np.nan, 20.0))
D["Curing duration (days)"] = days.round(3)
D["Test age (days)"] = age
D["Compressive strength (MPa)"] = pd.to_numeric(d[389], errors="coerce").where(d["_use_fc"])
D["Tensile strain capacity (%)"] = pd.to_numeric(d[418], errors="coerce").where(d["_use_eps"])

keep &= D["Test age (days)"].notna() & D["Curing temperature (°C)"].notna()
keep &= D["Compressive strength (MPa)"].notna() | D["Tensile strain capacity (%)"].notna()
print("rows dropped - other material:", int(((d['_use_fc'] | d['_use_eps']) & other).sum()),
      "| no fiber type:", int(((d['_use_fc'] | d['_use_eps']) & ~other & no_fiber_type).sum()),
      "| no cement/FA/GGBS:", int(((d['_use_fc'] | d['_use_eps']) & ~other & ~no_fiber_type & (B3 <= 0)).sum()))
D = D[keep].reset_index(drop=True)
num = D.columns[2:2 + len(M21)]
D[num] = D[num].round(5)

guide = pd.DataFrame({"Item": [
    "One row", "Paper / DOI", "Cement, Fly ash, GGBS", "Other materials", "Fibers", "Curing method",
    "Curing temperature", "Curing duration", "Outputs", "Rules", "Source", "Rebuild"], "Meaning": [
    "One mix at one test age.",
    "Source paper (rows are grouped by paper on data.html).",
    "Share of the binder; the binder is only cement + fly ash + GGBS, so these three add up to 1.",
    "Mass ratio to that binder (silica fume, metakaolin and limestone powder too). Sand = any sand; SP includes HRWR; VMA includes HPMC; Na2SiO3 = SSM / ASM / SMP (anhydrous).",
    "Volume % of the mix.",
    "Standard moist room / Water curing / Sealed / wrapped / Air (lab ambient) / Heat / steam curing (same list as the web).",
    "°C; 20 °C when a non-heat paper does not state it.",
    "Heat curing: days at high temperature. Otherwise days of curing; the test age when not stated.",
    "Blank when not reported or excluded during cleaning (see data.html).",
    "Rows using any material outside the 21 are left out (defoamer allowed). Ratios re-expressed per cement + FA + GGBS.",
    "Built from 03 Dataset_ratio.xlsx and ml_spike/additions_v2/*.csv by ml_spike/build_web_dataset.py.",
    "python ml_spike/build_web_dataset.py, then python ml_spike/train_export.py ../strength_model.js"]})
with pd.ExcelWriter(OUT, engine="openpyxl") as w:
    D.to_excel(w, sheet_name="Data", index=False)
    guide.to_excel(w, sheet_name="Guide", index=False)
print("wrote", OUT, D.shape, "| papers:", D["Paper"].nunique(),
      "| fc rows:", int(D["Compressive strength (MPa)"].notna().sum()), "| strain rows:", int(D["Tensile strain capacity (%)"].notna().sum()))
