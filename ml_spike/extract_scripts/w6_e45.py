"""Wave 6, agent e45: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e45.csv (99-column TEMPLATE header).
Papers: conbuildmat.2021.124329, 2024.134878, 2024.137306
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
DIRECT = "direct (uniaxial)"


def r4(x):
    return round(x, 4)


def paper(name, author, year, doi):
    return {"Article Name": name, "Author": author, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------- 1) Yuan et al. 2021: PVA-HDCC (control groups without CaCO3 whisker), 28-d fc (Table 4)
P = paper("Flexural properties of PVA fiber reinforced high ductility cementitious composites containing calcium carbonate whisker",
          "Zhen Yuan, Cong Zhang, Chaofan Xia, Lishan Wu, Zhihui Yu, Zhihua Li", 2021, "10.1016/j.conbuildmat.2021.124329")
for nm, v, fc in [("PVA-HDCC-1 (PVA2)", 2.0, 23.6), ("PVA-HDCC-2 (PVA1.75)", 1.75, 25.2), ("PVA-HDCC-3 (PVA1.5)", 1.5, 26.9)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.8, "W / B": 0.30, "SS / B (Silica sand)": 0.2,
              "PVA fiber (vol%)": v, "PVA length (mm)": 12, "PVA diameter (µm)": 35, "PVA tensile strength (MPa)": 1500,
              "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": v,
              "Curing method": "24 h in mould, demoulded, curing box 20 +/- 2 C and 95 % RH for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 4 (PVA vol%, fc 28 d), sect. 2.2 (ratio 1:1:4, w/b 0.30, curing), Table 3 (PVA)",
              "Conversions / notes": f"{nm}; control groups without CaCO3 whisker (whisker mixes skipped). Ratio cement : quartz sand : fly ash = 1 : 1 : 4 (by mass), "
                                     "so B = cement + FA = 5, sand/B = 0.2. SP 0.06-0.12 wt% of binder (adjusted per mix) not entered. "
                                     "VERIFY: compressive specimen shape/size not stated; w/b 0.30 taken on cement + FA. Quartz sand used as sand."})
    rows.append(r)

# ---------- 2) Li et al. 2024: PVA-ECC with river sand only (steel slag replacement 0 %), cube fc 28 d (Table 5)
P = paper("Compressive behavior of polyvinyl alcohol engineered cementitious composites incorporating steel slag as aggregate",
          "Tong Li, Qinghe Wang, Qingxin Ren", 2024, "10.1016/j.conbuildmat.2024.134878")
B = 540 + 648
for nm, v, fc in [("ECC-P1.5-S0", 1.5, 42.2), ("ECC-P2-S0", 2.0, 43.2), ("ECC-P2.5-S0", 2.5, 40.1)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(540 / B), "FA (Fly ash)": r4(648 / B), "W / B": r4(380 / B), "River sand / B": r4(428 / B),
              "HRWR / B": r4(10.9 / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": v, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": v,
              "Curing method": "24 h in standard curing chamber (20 +/- 2 C, 95 +/- 5 % RH), demoulded, same conditions until 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 4 (mix), Table 5 (cubic compressive strength), sect. 2.3-2.4.2, Table 3 (PVA)",
              "Conversions / notes": f"{nm}; only the 0 % steel-slag mixes (river sand only) taken, steel-slag aggregate mixes skipped. kg/m3 / B (OPC + FA = {B}). "
                                     "PVA kg/m3 consistent with stated vol% (density 1300). fc = cubic compressive strength (Table 5); prism peak stress not entered."})
    rows.append(r)

# ---------- 3) Li et al. 2024: ST/PE hybrid fibre ECC, quasi-static direct tension (Table 9), 28 d
P = paper("Influence of strain rate and fiber blend mode on the tensile behaviors of steel-polyethylene hybrid fiber reinforced engineered cementitious composites",
          "Liang Li, Zhengpeng Li, Jun Wu, Tangjun Li, Xiuli Du", 2024, "10.1016/j.conbuildmat.2024.137306")
B = 1.11
for nm, pe, st, fcr, ts, eps in [("E2", 2.0, 0.0, 2.37, 3.28, 3.42), ("E1.5S0.5", 1.5, 0.5, 2.14, 2.66, 0.67), ("E1S1", 1.0, 1.0, 2.41, 2.63, 0.64),
                                 ("E0.5S1.5", 0.5, 1.5, 2.30, 2.56, 0.44), ("S2", 0.0, 2.0, 2.17, 2.49, 0.22)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.11 / B), "W / B": r4(0.28 / B), "SP / B": r4(0.013 / B),
              "Total fiber (vol%)": 2.0,
              "Curing method": "curing room 20 +/- 0.5 C, 95 +/- 5 % RH, 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
              "Curing RH (%)": 95, "Test age (days)": 28,
              "Tensile specimen": "plate 300 x 75 x 20 mm with holes at both ends (steel plates at ends)", "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ts, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 7 (mix, mass ratio), Tables 5-6 (fibres), Table 9 (static tensile), sect. 2.2.1",
              "Conversions / notes": f"{nm}. Mass ratio to cement = 1 (cement 1 : SF 0.11 : water 0.28 : WRA 0.013, no sand), B = cement + SF = {B}; SF as binder fraction. "
                                     "Static tensile = peak stress and ultimate strain of Table 9; initial cracking stress as first-cracking strength. "
                                     "VERIFY: steel fibre diameter given as range 0.175-0.35 mm (not entered); fc not reported; gauge length not stated. "
                                     "Cement contains 12 % slag + 4 % gypsum (as supplied). Pure-matrix (no fibre) mix skipped."})
    if pe:
        r.update({"PE fiber (vol%)": pe, "PE length (mm)": 12, "PE diameter (µm)": 39, "PE tensile strength (MPa)": 2180, "PE elastic modulus (GPa)": 210})
    if st:
        r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 12, "Steel tensile strength (MPa)": 3000, "Steel elastic modulus (GPa)": 210})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e45.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")
