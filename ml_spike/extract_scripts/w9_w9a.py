"""w9a: rows from 2 of the 5 assigned papers (3 rejected, see w9_w9a_rejected.txt).
 A) Oz, Gunes, Yucel (2022) J. Build. Eng. 105792 - only compressive strengths that the TEXT states (Fig. 12 values are not used)
 B) Li, Sheikh, Feng, Hadi (2023) Struct. Concrete 24(2) 2363 - Tables 3-5
"""
import os
import sys
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(here, "..", "additions_v2")
sys.path.insert(0, D)
from naoh_solution import naoh_split

cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), nrows=0, encoding="utf-8-sig").columns)
rows = []

# ---------------- A) JOBE 2022, 105792 (Table 3, Table 4, text of 3.2)
PA = {"Article Name": "Rheological and microstructural properties of FA+GGBFS-based engineered geopolymer composites (EGCs) capable of comparing with M45-ECC as mechanical performance",
      "Author": "Hatice Öznur Öz, Muhammet Güneş, Hasan Erhan Yücel", "Year": 2022,
      "DOI / URL": "https://doi.org/10.1016/j.jobe.2022.105792"}
pva_a = {"PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8,
         "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50"}
# M45-ECC (kg/m3): cement 564.4, FA 677.7, water 329.9, PVA 26, silica sand 451.1, SP 5.0
B = 564.4 + 677.7
for age, fc in ((7, 40.1), (28, 67.6)):
    r = dict(PA)
    r.update(pva_a)
    r.update({"OPC / Cement": round(564.4 / B, 4), "FA (Fly ash)": round(677.7 / B, 4), "W / B": round(329.9 / B, 4),
              "SP / B": round(5.0 / B, 4), "Sand (type not stated) / B": round(451.1 / B, 4), "Binder content (kg/m³)": round(B, 1),
              "Curing method": "demoulded after 24 h, then moist plastic bags at 23 ± 2 °C until test",
              "Curing time (days)": age, "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": age,
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Sect. 2.2 (curing), Sect. 3.2 text (fc with 2% PVA)",
              "Conversions / notes": "M45-ECC. kg/m3 divided by binder (cement+FA) 1242.1 kg/m3. Silica sand 0-400 um. PVA 26 kg/m3 = 2 vol% (1300 kg/m3). "
                                     "fc taken from the text (Fig. 12 not used). No direct tension test in the paper (4-point bending only)."})
    rows.append(r)
# FA+GGBFS EGCs: only those whose 28-d fc WITH PVA is stated in the text (M2 39.5, M4 68.9)
# (id, NaOH soln, Na2SiO3 soln, FA, GGBFS, sand, SP, extra water, fc28)
for mid, na, ns, fa, gg, sand, sp, ew, fc in (("M2_0.50_1250", 119.0, 297.6, 583.3, 250.0, 548.5, 2.0, 140.0, 39.5),
                                              ("M4_0.33_1250", 89.3, 223.2, 656.3, 281.3, 499.7, 1.0, 190.0, 68.9)):
    B = fa + gg
    s = naoh_split(13, solution_mass=na / B)
    r = dict(PA)
    r.update(pva_a)
    r.update({"FA (Fly ash)": round(fa / B, 4), "GGBS": round(gg / B, 4), "NaOH / B": round(s["NaOH"], 4),
              "NaOH molarity (M)": 13, "WG / B (Water glass)": round(ns / B, 4), "W / B": round((ew + s["water"] * B) / B, 4),
              "Sand (type not stated) / B": round(sand / B, 4), "SP / B": round(sp / B, 4), "Binder content (kg/m³)": round(B, 1),
              "Curing method": "demoulded after 24 h (lab conditions), then water at 60 °C until test",
              "Curing time (days)": 28, "Curing temperature (°C)": 60, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 4 (mix), Sect. 2.2 (curing), Sect. 3.2 text (fc 28 d with PVA)",
              "Conversions / notes": f"{mid}. B = FA + GGBFS (kg/m3 table values / {B:.1f}). NaOH column = 13 M NaOH solution ({na} kg/m3), converted: {s['note']}; "
                                     f"solution water added to W/B (extra water {ew} kg/m3). Na2SiO3 column = sodium silicate solution (solids/modulus not stated), as WG/B. "
                                     "PVA 26 kg/m3 = 2 vol%. VERIFY: fc 28 d with PVA from the sentence 'increased from 39.5 to 68.9 for M2_0.50_1250, M4_0.33_1250'; "
                                     "heat curing duration not stated separately (water 60 C until test). No direct tension test."})
    rows.append(r)

# ---------------- B) Struct. Concrete 2023 (Tables 2-5)
PB = {"Article Name": "Mechanical properties of ambient cured fly ash-slag-based engineered geopolymer composites with different types of fibers",
      "Author": "Zeya Li, M. Neaz Sheikh, Hu Feng, Muhammad N. S. Hadi", "Year": 2023, "DOI / URL": "https://doi.org/10.1002/suco.202200871"}
fib = {"L-PVA": dict(col="PVA", L=12, d=39.4, ts=1450, E=35), "H-PVA": dict(col="PVA", L=12, d=40.0, ts=1560, E=41),
       "PE": dict(col="PE", L=12, d=12.0, ts=3500, E=123)}
# series, vol%, FA, slag, NaOH soln, Na2SiO3 soln, water, fc, fcr, ft, eps  (Table 4 and Table 5)
T = [("L-PVA", 1.5, 658.2, 438.8, 182.8, 365.7, 164.6, 51.5, 1.7, 2.6, 1.5),
     ("L-PVA", 1.75, 656.5, 437.7, 182.4, 364.7, 164.1, 49.1, 2.6, 4.4, 4.3),
     ("L-PVA", 2.0, 654.9, 436.6, 181.9, 363.8, 163.7, 48.7, 2.3, 3.8, 4.2),
     ("L-PVA", 2.25, 653.2, 435.5, 181.4, 362.9, 163.3, 47.5, 2.2, 3.6, 3.9),
     ("L-PVA", 2.5, 651.5, 434.3, 181.0, 362.0, 162.9, 46.8, 2.1, 3.3, 3.4),
     ("H-PVA", 1.5, 658.2, 438.8, 182.8, 365.7, 164.6, 52.7, 1.9, 2.9, 2.4),
     ("H-PVA", 1.75, 656.5, 437.7, 182.4, 364.7, 164.1, 51.3, 2.0, 3.1, 4.2),
     ("H-PVA", 2.0, 654.9, 436.6, 181.9, 363.8, 163.7, 50.9, 2.4, 4.1, 4.9),
     ("H-PVA", 2.25, 653.2, 435.5, 181.4, 362.9, 163.3, 50.0, 3.1, 5.4, 5.8),
     ("H-PVA", 2.5, 651.5, 434.3, 181.0, 362.0, 162.9, 45.6, 2.3, 3.8, 3.4),
     ("PE", 1.0, 661.5, 441.0, 183.8, 367.5, 165.4, 37.5, 0.9, 1.9, 7.0),
     ("PE", 1.5, 658.2, 438.8, 182.8, 365.7, 164.6, 40.2, 1.9, 4.5, 9.3),
     ("PE", 1.75, 656.5, 437.7, 182.4, 364.7, 164.1, 41.5, 1.8, 4.2, 8.8),
     ("PE", 2.0, 654.9, 436.6, 181.9, 363.8, 163.7, 44.0, 1.7, 3.9, 8.7),
     ("PE", 2.25, 653.2, 435.5, 181.4, 362.9, 163.3, 46.2, 1.6, 3.6, 8.4),
     ("PE", 2.5, 651.5, 434.3, 181.0, 362.0, 162.9, 46.7, 1.6, 3.5, 4.4)]
for ser, v, fa, sl, na, ns, w, fc, fcr, ft, eps in T:
    B = fa + sl
    s = naoh_split(14, solution_mass=na / B)
    f = fib[ser]
    c = f["col"]
    r = dict(PB)
    r.update({"FA (Fly ash)": round(fa / B, 4), "GGBS": round(sl / B, 4), "NaOH / B": round(s["NaOH"], 4), "NaOH molarity (M)": 14,
              "WG / B (Water glass)": round(ns / B, 4), "W / B": round((w + s["water"] * B) / B, 4), "Binder content (kg/m³)": round(B, 1),
              f"{c} fiber (vol%)": v, f"{c} length (mm)": f["L"], f"{c} diameter (µm)": f["d"], f"{c} tensile strength (MPa)": f["ts"],
              f"{c} elastic modulus (GPa)": f["E"], "Total fiber (vol%)": v,
              "Curing method": "covered with cling wrap at 23 ± 2 °C for 24 h, demoulded, then wrapped, control room 23 ± 2 °C, RH 70 ± 10% until test",
              "Curing temperature (°C)": 23, "Curing RH (%)": 70, "Demolding age (days)": 1, "Test age (days)": 28, "Curing time (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog bone (JSCE)",
              "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (fibers), Table 3-4 (mix), Table 5 (results), Sect. 2.1-2.3",
              "Conversions / notes": f"{ser}-{v}. B = FA + slag (kg/m3 / {B:.1f}). NaOH column = 14 M NaOH solution ({na} kg/m3), converted: {s['note']}; "
                                     "solution water added to W/B together with the 'Water' column (additional water). Na2SiO3 solution (SG 1.53; 44.1% solids, 14.7% Na2O, 29.4% SiO2) as WG/B. "
                                     "Fiber vol% = mix name (consistent with fiber kg/m3 x density). "
                                     "VERIFY: test age 28 d is stated for the Table 5 compressive results; tensile results are in the same Table 5, tensile age not stated separately."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(D, "w9_w9a.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")

# --- review 2026-11-19: 10.1002/suco.202200871 states 28 d only for compressive strength; the age of the tension
# tests is not stated, so the tensile results are left out (rule: test age must be stated)
import pandas as _pd
_p = OUT if "OUT" in globals() else r"ml_spike\additions_v2\w9_w9a.csv"
_A = _pd.read_csv(_p, encoding="utf-8-sig")
_m = _A["DOI / URL"].astype(str).str.contains("suco.202200871", case=False)
for _c in [c for c in _A.columns if any(k in c for k in ("Tensile strain", "Tensile strength", "First-cracking", "First crack", "Tensile test", "gauge", "Tensile specimen"))]:
    _A.loc[_m, _c] = None
_A.to_csv(_p, index=False, encoding="utf-8-sig")
