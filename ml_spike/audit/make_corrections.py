"""Write audit/corrections.json from the strain audit (2026-11-20; reports audit/report_*.md).
Rows are named by their Excel row in the current 04 Dataset_web.xlsx and stored as (DOI, n-th row of that DOI,
expected strain / fc) so build_web_dataset.py can apply them and stop if the source rows ever move."""
import os, json, numpy as np, pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
D = pd.read_excel(os.path.join(here, "..", "..", "excel", "04 Dataset_web.xlsx"), sheet_name="Data"); D.index += 2
D["_k"] = D.groupby("DOI").cumcount()
R = lambda a, b=None: list(range(a, (b or a) + 1))
CM, CT, CD, TA, FC = "Curing method", "Curing temperature (°C)", "Curing duration (days)", "Test age (days)", "Compressive strength (MPa)"
STD, AIR, HEAT = "Standard moist room", "Air (lab ambient)", "Heat / steam curing"
ops = []   # (rows, action, {col: value}, reason)
def drop(rows, why): ops.append((rows, "drop", {}, why))
def setv(rows, vals, why): ops.append((rows, "set", vals, why))
drop(R(1157, 1190), "CC powder is ground white marble (Imerfill), not limestone; 1189-1190 test age / curing not stated")
drop(R(861, 872), "paper could not be checked (no copy, publisher blocks download); identical inputs with swapped-looking strains")
drop(R(171, 176), "superplasticizer used but dosage not stated; sodium lignosulfonate (no column); fc 62 vs 66 conflict, 27 read from figure")
drop(R(1286, 1288), "curing = 11 d air + 12 d water + 24 h 80 °C + air (not one web method); fc 54.6 / 52.2 not stated")
drop(R(1808, 1809), "28 d standard curing then indoor 18.3 °C / 32 % RH to 60 / 90 d (not one web method)")
drop([464, 468, 472], "steam curing box 3 d, steam temperature not stated")
drop([465, 469, 473], "sprinkler curing under geotextile, temperature not stated")
setv([466, 470, 474], {CM: AIR, CT: 20}, "natural curing 20 ± 2 °C, 50 % RH")
setv(R(1345, 1362)[0::3] + R(1345, 1362)[1::3], {CM: AIR}, "cured at RH 25 % / 55 %, 20 °C (not a moist room)")
setv(R(1833, 1844), {CM: STD, CT: 20}, "48 h ambient, then standard curing chamber RH >= 90 %, about 20 °C")
setv([1680, 1681, 1683, 1684, 1686, 1687], {CM: AIR}, "48 h sealed, then RH 30 % / 60 % at 20 °C")
setv([1682, 1685, 1688], {CM: STD}, "48 h sealed, then RH 100 % at 20 °C")
setv([2758], {CM: AIR, CT: 20}, "dry curing 20 °C, RH 60 % to 27 d")
setv([2759], {CM: STD, CT: 20}, "standard curing 20 °C, RH 95 %")
setv([2760], {CM: HEAT, CT: 60, CD: 1}, "60 °C for 1 d, then dry curing to 28 d")
setv([2761], {CM: AIR, CT: -5}, "-5 °C to 28 d")
setv(R(1113, 1127), {CM: HEAT, CT: 75, CD: 2}, "about 98 % RH at 75 °C for 2 days, then room temperature for 7 days")
setv(R(2, 5), {CT: 23}, "air and water curing in a chamber at (23 ± 3) °C")
setv([2, 4, 5, 6] + R(7, 10), {FC: np.nan}, "compressive strength only in Figs. 8-9")
setv([3], {CT: 23, FC: 142.0}, "fc stated in the text: 142 MPa; chamber (23 ± 3) °C")
setv(R(729, 734), {FC: np.nan}, "fc only in Fig. 5 (dataset value was tensile strength / ratio)")
setv([2576], {FC: 59.9}, "PC75-MK25: 59.9 MPa at 28 days (text)")
setv([2577], {FC: 39.5}, "PC50-MK50: 39.5 MPa at 28 days (text)")
for rows, w in [(R(1214, 1218), 230 / 1450), (R(1219, 1224), 267 / 1423), (R(1225, 1230), 284 / 1340), (R(1231, 1236), 320 / 1253), (R(1237, 1242), 388 / 1094)]:
    setv(rows, {"Water": round(w, 5)}, "water from Table 2 (kg/m3) / (cement + GGBS); was W/B x binder incl. HRWR water")
PV = {"PVA fiber length (mm)": 12}
for rows, u in [([1852], .35), ([1853], .50), ([1854], .65), (R(1855, 1858), .50)]:
    setv(rows, {**PV, "PVA fiber diameter (µm)": round(u * 12 + (1 - u) * 40, 2), "PVA fiber tensile strength (MPa)": round(u * 1300 + (1 - u) * 1560, 1),
                "PVA fiber elastic modulus (GPa)": round(u * 30 + (1 - u) * 41, 2)},
         f"hybrid PVA: {int(u*100)} % unoiled (12 µm, 1300 MPa, 30 GPa) + oiled (40 µm, 1560 MPa, 41 GPa), volume-weighted (Table 5)")
out = []
for rows, act, vals, why in ops:
    for r in rows:
        x = D.loc[r]; e = x["Tensile strain capacity (%)"]; f = x[FC]
        out.append(dict(doi=x["DOI"], k=int(x["_k"]), excel_row=r, eps=None if pd.isna(e) else float(e), fc=None if pd.isna(f) else float(f),
                        action=act, set={c: (None if pd.isna(v) else v) for c, v in vals.items()}, reason=why))
json.dump(out, open(os.path.join(here, "corrections.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "row edits;", sum(o["action"] == "drop" for o in out), "drops")
