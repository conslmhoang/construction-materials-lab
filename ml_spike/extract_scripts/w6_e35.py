"""Wave 6, agent e35: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e35.csv (99-column TEMPLATE header).
Papers: conbuildmat.2018.07.194, 2018.10.114, 2018.11.093, 2019.02.033, 2019.117993, 2020.118487
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


# ---- 1) Othman & Marzouk 2018: UHP-FRC UF2-110 / UF2-130 (own mixes, no proprietary premix), 56 d
P = paper("Effects of variations in compressive strength and fibre content on dynamic properties of ultra-high performance fibre-reinforced concrete",
          "H. Othman, H. Marzouk", 2018, "10.1016/j.conbuildmat.2018.11.093")
for nm, c, sf, sand, w, sp, fc in [("UF2-110", 960, 190, 650, 210, 30, 110.8), ("UF2-130", 1050, 250, 630, 200, 40, 132.7)]:
    B = c + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B), "Fine sand / B": r4(sand / B),
              "SP / B": r4(sp / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
              "Steel tensile strength (MPa)": 2600, "Steel elastic modulus (GPa)": 205, "Total fiber (vol%)": 2,
              "Curing method": "moist burlap 7 d in mould, then moist chamber 20 C 95 % RH 3 more weeks, then lab air to test",
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": 56,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix, kg/m3), Table 3 (fibre), Table 6 (fc), sect. 3.1",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + SF = {B}). Fine sand < 0.5 mm. 156 kg/m3 steel = 2 vol%. Ductal premix mixes (UF1/UF2/UF3-150) skipped (proprietary). "
                                     "fc = quasi-static value (3e-5 1/s), Table 6, tested at 56 d (stated). Flexural only for tension, no direct tension."})
    rows.append(r)

# ---- 2) Fang et al. 2019: UHPFRC steel fibres, 28 d / 180 d fc, 28 d splitting
P = paper("The influence of steel fibre properties on the shrinkage of ultra-high performance fibre reinforced concrete",
          "Chengfeng Fang, Mohamed Ali, Tianyu Xie, Phillip Visintin, Abdul H. Sheikh", 2019, "10.1016/j.conbuildmat.2019.117993")
F = {"H1": (0.75, 35, 1225, 210), "H2": (0.55, 36, 1345, 210), "H3": (0.75, 60, 1225, 210), "S": (0.2, 13, 2850, 210)}
mixes = [("M2", "H1", 1.5, 129.1, 134.9, 14.1), ("M3", "H2", 1.5, 133.7, 137.1, 14.4), ("M4", "H3", 1.5, 141.8, 144.4, 14.8),
         ("M5", "S", 2.0, 122.6, 126.8, 13.6), ("M6", "H1", 2.0, 147.2, 151.4, 12.4), ("M7", "H2", 2.0, 133.7, 138.2, 11.8),
         ("M8", "H3", 2.0, 137.3, 139.7, 13.9), ("M9", "H2+S", 2.0, 133.9, 137.9, 12.0), ("M10", "H1", 2.5, 139.8, 142.6, 10.7),
         ("M11", "H2", 2.5, 125.8, 130.3, 11.9), ("M12", "H3", 2.5, 127.6, 131.0, 13.0)]
for mid, ft, vf, f28, f180, fst in mixes:
    for age, fc in ((28, f28), (180, f180)):
        r = dict(P)
        r.update({"OPC / Cement": 0.79, "SF (Silica fume)": 0.21, "W / B": 0.12, "Sand (type not stated) / B": 1.0, "SP / B": 0.06,
                  "Steel fiber (vol%)": vf, "Total fiber (vol%)": vf, "Test age (days)": age,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 1 (mix ratios, fc, fst), Table 2 (fibres), sect. 2.2.3",
                  "Curing method": "not described"})
        if ft in F:
            d, l, t, e = F[ft]
            r.update({"Steel length (mm)": l, "Steel diameter (µm)": d * 1000, "Steel tensile strength (MPa)": t, "Steel elastic modulus (GPa)": e})
        note = (f"{mid} ({ft}, {vf} vol%). Sulfate-resisting (Portland) cement 0.79 + silica fume 0.21 = binder 1; sand 1.00, water 0.12, SP 0.06. "
                "VERIFY: Table 1 headed kg/m3 but values are ratios; read as mass ratios to binder (cement + SF = 1). Curing not described; test age stated. "
                "Reference mix M1 (no fibre) skipped. ")
        if ft == "H2+S":
            note += "Blend 1:1 straight S + hooked H2 (fibre dims left blank). "
        if age == 28:
            r["Tensile strength (MPa)"] = fst
            r["Tensile test type"] = "splitting (cylinder 100 x 200)"
            note += "Tensile strength = 28-d splitting strength fst (not direct)."
        r["Conversions / notes"] = note
        rows.append(r)

# ---- 3) Abid et al. 2018: M45 ECC with PVA, 28 d cube fc and splitting
P = paper("Hydro-abrasive resistance of engineered cementitious composites with PP and PVA fibers",
          "Sallal R. Abid, Mohammed S. Shamkhi, Noor S. Mahdi, Yasir H. Daek", 2018, "10.1016/j.conbuildmat.2018.07.194")
B = 570 + 684
for vf, fc, st in [(0.5, 47.7, 5.0), (1.0, 46.5, 5.8), (1.5, 47.8, 6.5), (2.0, 48.4, 7.0)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(570 / B), "FA (Fly ash)": r4(684 / B), "W / B": 0.27, "SS / B (Silica sand)": r4(455 / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": vf, "PVA length (mm)": 6, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8,
              "Total fiber (vol%)": vf, "Curing method": "not described", "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": fc,
              "Tensile strength (MPa)": st, "Tensile test type": "splitting (cylinder 100 x 200)",
              "Source table/page": "Sect. 2.3 (M45 mix), Table 2 (fibre), Table 3 (strengths)",
              "Conversions / notes": f"PVA {vf} vol%. M45 ECC 570 : 684 : 455 (cement : FA : silica sand) kg/m3, w/cm 0.27 (as stated). No SP stated. "
                                     "VERIFY: curing not described, age 28 d stated. Splitting strength is not direct tension. PP mixes skipped."})
    rows.append(r)

# ---- 4) Mohammed et al. 2018: NS-free reference mixes (M1-M4), 23 C, fc 28 d
P = paper("The influence of high temperature on microstructural damage and residual properties of nano-silica-modified (NS-modified) self-consolidating engineering cementitious composites (SC-ECC) using response surface methodology (RSM)",
          "Bashar S. Mohammed, Bitrus Emmanuel Achara, Mohd Shahir Liew", 2018, "10.1016/j.conbuildmat.2018.10.114")
B = 583 + 700
for mid, vf, hr, fc in [("M1", 0.5, 0.77, 73.98), ("M2", 1.0, 0.82, 76.86), ("M3", 1.5, 0.89, 85.87), ("M4", 2.0, 0.99, 97.57)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(583 / B), "FA (Fly ash)": r4(700 / B), "W / B": r4(187 / B), "River sand / B": r4(467 / B), "HRWR / B": r4(hr / 100),
              "Binder content (kg/m³)": B, "PVA fiber (vol%)": vf, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": vf,
              "Curing method": "demoulded 24 h, water tank 23 +/- 2 C, RH ~95 % for 28 d, then unheated control",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 4 (mix), Table 3 (PVA), Table 6 (fc runs with NS 0 %, 23 C)",
              "Conversions / notes": f"{mid}: NS 0 % reference at 23 C only (nano-silica mixes and heated specimens skipped). kg/m3 / B (cement + FA = {B}). HRWR given as % of cementitious. "
                                     "VERIFY: W/B 0.146 from 187 kg/m3 water as tabulated; fc from RSM design table (Table 6), age taken as end of 28 d water curing."})
    rows.append(r)

# ---- 5) Mohammed et al. 2019: same mixes, direct tension at 23 C, NS 0 %
P = paper("Effects of elevated temperature on the tensile properties of NS-modified self-consolidating engineered cementitious composites and property optimization using response surface methodology (RSM)",
          "Bashar S. Mohammed, Bitrus Emmanuel Achara, Mohd Shahir Liew, W.S. Alaloul, Veerendrakumar C. Khed", 2019, "10.1016/j.conbuildmat.2019.02.033")
for mid, vf, hr, ts, eps in [("MC1", 0.5, 0.77, 3.06, 0.69), ("MC2", 1.0, 0.82, 3.61, 1.9), ("MC3", 1.5, 0.89, 3.9, 2.03), ("MC4", 2.0, 0.99, 4.38, 2.4)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(583 / B), "FA (Fly ash)": r4(700 / B), "W / B": r4(187 / B), "River sand / B": r4(467 / B), "HRWR / B": r4(hr / 100),
              "Binder content (kg/m³)": B, "PVA fiber (vol%)": vf, "Total fiber (vol%)": vf,
              "Curing method": "demoulded 24 h, water curing tank 22 +/- 2 C, RH 80 +/- 5 % for 28 d; unheated control",
              "Curing time (days)": 28, "Curing temperature (°C)": 22, "Curing RH (%)": 80, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 5 (runs with NS 0 %, 23 C)",
              "Conversions / notes": f"{mid}: NS 0 %, 23 C control only. kg/m3 / B (cement + FA = {B}); HRWR % of cementitious. PVA dims not given in this paper (same mixes as 10.1016/j.conbuildmat.2018.10.114). "
                                     "VERIFY: W/B 0.146 as tabulated; age taken as end of 28 d curing; tensile values from RSM design table."})
    rows.append(r)

# ---- 6) Li, Yang, Tan 2020: UHPFRC with PE + steel, ambient 28 d fc (Table 3)
P = paper("Flexural behavior of ultra-high performance hybrid fiber reinforced concrete at the ambient and elevated temperature",
          "Ye Li, En-Hua Yang, Kang Hai Tan", 2020, "10.1016/j.conbuildmat.2020.118487")
B = 1.25
for nm, wb, ag, fc in [("PE10ST20 (W/B 0.2, AG 0.6 mm)", 0.2, "0.6", 147.1), ("PE10ST20WB03 (W/B 0.3)", 0.3, "0.6", 127.6), ("PE10ST20AG23 (AG 2.3 mm)", 0.2, "2.3", 153.8)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.25 / B), "W / B": wb, "SS / B (Silica sand)": r4(0.25 / B), "River sand / B": r4(1.1 / B),
              "Sand max size (µm)": float(ag) * 1000, "SP / B": r4(0.04 / B), "PE fiber (vol%)": 1, "PE length (mm)": 19, "PE diameter (µm)": 23,
              "PE tensile strength (MPa)": 3250, "PE elastic modulus (GPa)": 113, "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 220,
              "Steel tensile strength (MPa)": 2800, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 3,
              "Curing method": "covered 24 h, demoulded, lime-saturated water at ambient temperature 27 d", "Curing time (days)": 27, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix, mass ratios to cement), Table 2 (fibres), Table 3 (fc), sect. 2.2",
              "Conversions / notes": f"{nm}. Mass ratios to cement: SF 0.25, aggregate (river sand) 1.1, silica sand 0.25, SP 0.04; B = cement + SF = 1.25. "
                                     "W/B as stated (0.2 / 0.3). Only fibre mixes with fc given as numbers in Table 3 (others only in Fig. 5). Unheated ambient specimens. "
                                     "VERIFY: SP basis (per cement) assumed; sand max size 0.6 / 2.3 mm for AG."})
    rows.append(r)

df = pd.DataFrame(rows)
bad = [c for c in df.columns if c not in cols]
assert not bad, bad
df = df.reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e35.csv"), index=False, encoding="utf-8-sig")
print(len(df), df["DOI / URL"].nunique())
