"""Wave 6, agent e13: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e13.csv (99-column TEMPLATE header).
Papers: cemconcomp 2011.10.002, 2019.01.001, 2020.103857, 2020.103875, 2021.104204, 2022.104434, 2022.104729, 2022.104895
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


# ---------------------------------------------------------------- 1) Sahmaran 2012 ECC (ECC1, ECC2 with PVA)
P = {"Article Name": "Frost resistance and microstructure of Engineered Cementitious Composites: Influence of fly ash and micro poly-vinyl-alcohol fiber",
     "Author": "Mustafa Sahmaran, Erdogan Ozbay, Hasan E. Yucel, Mohamed Lachemi, Victor C. Li", "Year": 2012,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2011.10.002"}
for mid, c, fa, w, pva, sand, sp, fcs, ten in [
        ("ECC1", 558, 669, 326, 26, 446, 2.3, {14: 39.2, 28: 62.5}, {14: (2.91, 4.63), 28: (2.73, 5.14)}),
        ("ECC2", 375, 823, 318, 26, 435, 2.0, {14: 27.7, 28: 54.1}, {14: (3.24, 4.17), 28: (3.02, 4.82)})]:
    B = c + fa
    for age in (14, 28):
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B),
                  "Sand (type not stated) / B": r4(sand / B), "SP / B": r4(sp / B), "Binder content (kg/m³)": B,
                  "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620,
                  "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
                  "Curing method": "environmental chamber 23 C, RH 95 % until test", "Curing time (days)": age,
                  "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Test age (days)": age,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "coupon 200x75x13 mm",
                  "Tensile test type": DIRECT, "Compressive strength (MPa)": fcs[age], "Tensile strength (MPa)": ten[age][1],
                  "Tensile strain capacity (%)": ten[age][0],
                  "Source table/page": "Table 2 (mix, fc with fiber), Table 3 (tension)",
                  "Conversions / notes": f"{mid}. kg/m3 / B (cement + FA). Micro silica sand (max 250 um). PVA 26 kg/m3 / 1300 = 2 vol%. "
                                         "Matrix mixes without fibre and freeze-thaw specimens skipped. HRWR in kg/m3 as dosed. "
                                         "VERIFY: year 2012 (volume year; DOI 2011)."})
        rows.append(r)

# ---------------------------------------------------------------- 2) Li 2019 SHCC with PE, w/b 0.14-0.32
P = {"Article Name": "Performance-based design of all-grade strain hardening cementitious composites with compressive strengths from 40 MPa to 120 MPa",
     "Author": "Linzhi Li, Ziwei Cai, Kequan Yu, Y.X. Zhang, Yao Ding", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2019.01.001"}
mixes = {  # w/b: (cement, LP, SF, GGBS, sand, water, HRWR)
    0.14: (700, 100, 150, 750, 500, 230, 25), 0.16: (687, 96, 144, 736, 485, 267, 20), 0.18: (647, 91, 136, 693, 458, 284, 12),
    0.22: (605, 85, 127, 648, 446, 320, 8), 0.32: (528, 74, 111, 566, 446, 388, 3)}
fib = {5: ("Type I (Lf 12 mm, df 24 um)", 1, 12, 24, 2400, 100), 7.5: ("Type II (18/24)", 1, 18, 24, 2400, 100),
       9: ("Type III (18/20)", 1, 18, 20, 2800, 120), 10: ("Type I (12/24)", 2, 12, 24, 2400, 100),
       15: ("Type II (18/24)", 2, 18, 24, 2400, 100), 18: ("Type III (18/20)", 2, 18, 20, 2800, 120)}
# w/b: {VfLf/df: (first crack MPa, strain capacity %, peak stress MPa)} Table 6
t6 = {0.32: {5: (2.5, 3.01, 4.3), 7.5: (3.2, 5.40, 4.5), 9: (3.1, 6.03, 4.8), 10: (3.2, 6.18, 5.1), 15: (4.7, 10.64, 6.2), 18: (5.2, 11.28, 6.5)},
      0.22: {5: (3.4, 2.59, 5.4), 7.5: (3.9, 5.91, 6.0), 9: (5.2, 6.13, 6.4), 10: (4.4, 6.88, 6.5), 15: (7.2, 11.14, 9.5), 18: (7.6, 12.00, 10.4)},
      0.18: {5: (4.4, 3.36, 6.6), 7.5: (4.3, 4.31, 7.3), 9: (4.6, 5.11, 7.7), 10: (5.2, 5.82, 8.9), 15: (7.5, 9.02, 11.4), 18: (8.3, 9.60, 11.9)},
      0.16: {5: (4.1, 2.61, 7.5), 7.5: (4.7, 3.66, 8.1), 9: (4.5, 4.59, 8.4), 10: (5.6, 6.69, 11.4), 15: (8.8, 10.13, 13.2), 18: (7.7, 10.11, 14.8)},
      0.14: {7.5: (8.2, 2.20, 10.3), 9: (8.2, 3.52, 10.7), 10: (9.5, 5.11, 12.1), 15: (10.5, 8.00, 16.5), 18: (12.1, 8.49, 17.8)}}
for wb, (c, lp, sf, gg, sd, w, hr) in mixes.items():
    B = c + lp + sf + gg
    for k, (fcr, eps, fu) in t6[wb].items():
        ftype, vf, L, d, ts, E = fib[k]
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "GGBS": r4(gg / B), "SF (Silica fume)": r4(sf / B), "Limestone powder": r4(lp / B),
                  "W / B": wb, "SS / B (Silica sand)": r4(sd / B), "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B,
                  "PE fiber (vol%)": vf, "PE length (mm)": L, "PE diameter (µm)": d, "PE tensile strength (MPa)": ts,
                  "PE elastic modulus (GPa)": E, "Total fiber (vol%)": vf,
                  "Curing method": "demoulded 24 h, water tank 28 d", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
                  "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
                  "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 2 (mix, 2 vol% basis), Table 3 (fibres), Table 6 (tension, VfLf/df = " + str(k) + ")",
                  "Conversions / notes": f"w/b {wb}, fibre {ftype}, Vf {vf} %. kg/m3 / B (cement + LP + SF + GGBS = {B}). Table 2 lists the 2 % PE dose (20 kg/m3); "
                                         "the 1 % mixes use the same other ingredients (water/HRWR as in table). W/B is the paper's W*/B, which includes the water of the HRWR. "
                                         "Compressive strength per mix is only in figures (stated 43 MPa at w/b 0.32 and 115 MPa at 0.14 for the series); not entered. "
                                         "Test age 28 d from 'cured in a water tank for 28 days'; PE tensile strength/modulus from Table 3."})
        rows.append(r)

# ---------------------------------------------------------------- 3) Wu 2021 MgO-doped ECC, MgO-free controls
P = {"Article Name": "Mechanical performance of MgO-doped Engineered Cementitious Composites (ECC)",
     "Author": "Haoliang Wu, Jing Yu, Yanjun Du, Victor C. Li", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2020.103857"}
for mid, fa, sp, fc, fcr, eps, fu in [("0%E1.2", 1.2, 0.0032, 52.8, 5.06, 3.35, 5.37), ("0%E2.2", 2.2, 0.0025, 41.9, 4.29, 3.76, 4.64)]:
    B = 1 + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fa / B), "W / B": 0.25, "SS / B (Silica sand)": 0.36,
              "SP / B": sp, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 24 h, demoulded, curing room 20 C RH 65 % for 27 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
              "Curing RH (%)": 65, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dumbbell (JSCE)", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 3 (PVA), Table 4 (tension), sect. 4.2 text (fc)",
              "Conversions / notes": f"{mid}: only the MgO-free control mix of each series (MgO not allowed). Weight ratios to binder (cement + FA). "
                                     "SP dose 0.32 % / 0.25 % of binder from Table 1. fc 52.8 / 41.9 MPa from text (value at 0 % MgO). "
                                     "VERIFY: test age 28 d derived (24 h + 27 d curing room); tensile test age not stated explicitly."})
    rows.append(r)

# ---------------------------------------------------------------- 4) Zhao 2020 AAFRC with steel slag, 0 % SS control
P = {"Article Name": "Influence of steel slag on the properties of alkali-activated fly ash and blast-furnace slag based fiber reinforced composites",
     "Author": "Yujing Zhao, Tao Shi, Liying Cao, Lili Kan, Min Wu", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2020.103875"}
B = 16.33 + 38.10
r = dict(P)
r.update({"GGBS": r4(38.10 / B), "FA (Fly ash)": r4(16.33 / B), "WG / B (Water glass)": r4(13.34 / B), "NaOH / B": r4(2.98 / B), "W / B": r4(11.97 / B),
          "Sand (type not stated) / B": r4(16.33 / B), "PE fiber (vol%)": 1.9, "PE length (mm)": 12, "PE diameter (µm)": 24,
          "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 1.9,
          "Curing method": "demoulded 24 h, plastic wrap, oven 100 C 2 h, then 20 C lab 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Demolding age (days)": 1, "Test age (days)": 28, "Heat curing duration (h)": 2, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 2.69, "Tensile strength (MPa)": 5.09, "Tensile strain capacity (%)": 3.28,
          "Source table/page": "Table 3 (mix, wt.%), Table 2 (PE), Table 4 (tension)",
          "Conversions / notes": "Control mix 0%-SS only (steel slag mixes skipped). Mix given in wt.% of total; B = FA + GGBS = 54.43. Na2SiO3 13.34 % is the sodium silicate solution "
                                 "(entered as water glass, its water not added to W). "
                                 "VERIFY: fibre vol% not stated; PE 0.95 wt% of mix converted with assumed densities (FA 2.2, GGBS 2.9, silicate 1.4, NaOH 2.13, sand 2.65, water 1) -> 1.9 vol%. "
                                 "fc of 0%-SS only in Fig. 6, not entered."})
rows.append(r)

# ---------------------------------------------------------------- 5) Li 2021 river sand ECC (matrix cracking), series 1 + MSS control of series 2
P = {"Article Name": "Investigation of matrix cracking properties of engineered cementitious composites (ECCs) incorporating river sands",
     "Author": "Yazhao Li, Junxia Li, En-Hua Yang, Xinchun Guan", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2021.104204"}
for mid, c, fa, sf, sd, w, sp, fc, sandkind, L, d, age, steam in [
        ("W/B-0.24-MSS/B-0.36", 502, 753, 0, 452, 301, 10, 63.70, "MSS", 12, 24, 3, "75 C 2 d"),
        ("W/B-0.24-RS/B-0.36", 502, 753, 0, 452, 301, 11, 59.88, "RS", 12, 24, 3, "75 C 2 d"),
        ("W/B-0.24-RS/B-0.55", 450, 673, 0, 617, 269, 17, 61.28, "RS", 12, 24, 3, "75 C 2 d"),
        ("W/B-0.16-MSS/B-0.45", 839, 419, 140, 629, 224, 20, 125.71, "MSS", 18, 19, 4, "90 C 3 d")]:
    B = c + fa + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B) if sf else None, "W / B": r4(w / B),
              "SP / B": r4(sp / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.0, "PE length (mm)": L, "PE diameter (µm)": d,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 2.0,
              "Curing method": f"covered in lab air 24 h, demoulded, steam {steam}", "Curing temperature (°C)": 75 if age == 3 else 90,
              "Demolding age (days)": 1, "Test age (days)": age, "Heat curing duration (h)": 48 if age == 3 else 72,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix), Table 3 (fc)",
              "Conversions / notes": f"{mid}. kg/m3 / B (OPC + FA + SF = {B}). Fibre 2 vol% (19 kg/m3). Only fc of this paper used (no tensile test in table). "
                                     "Mixes with coarse sand 2.36-4.75 mm (CS) skipped; W/B-0.24-RS/B-0.75 is entered under 10.1016/j.cemconcomp.2022.104434 (same data). "
                                     f"VERIFY: test age {age} d derived (24 h + steam cure before testing; test day not stated)."})
    r["Curing time (days)"] = age
    if sandkind == "MSS":
        r["SS / B (Silica sand)"] = r4(sd / B)
        r["Sand max size (µm)"] = 250
    else:
        r["River sand / B"] = r4(sd / B)
    rows.append(r)

# ---------------------------------------------------------------- 6) Li 2022 river sand ECC crack propagation (MSS 0.75, RS 0.75, MSS 0.65)
P = {"Article Name": "Mechanism study of crack propagation in river sand Engineered Cementitious Composites (ECC)",
     "Author": "Yazhao Li, Junxia Li, En-Hua Yang, Xinchun Guan", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2022.104434"}
for mid, c, fa, sf, sd, w, sp, kind, L, d, age, fc, fcr, fu, eps in [
        ("W/B-0.24-MSS/B-0.75", 404, 605, 0, 756, 242, 20, "MSS", 12, 24, 3, 60.72, 3.44, 7.33, 6.78),
        ("W/B-0.24-RS/B-0.75", 404, 605, 0, 756, 242, 23, "RS", 12, 24, 3, 62.83, 4.06, 5.46, 3.35),
        ("W/B-0.16-MSS/B-0.65", 746, 373, 124, 808, 199, 25, "MSS", 18, 19, 4, 116.21, 7.62, 11.88, 5.94)]:
    B = c + fa + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B) if sf else None, "W / B": r4(w / B),
              "SP / B": r4(sp / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.0, "PE length (mm)": L, "PE diameter (µm)": d,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 2.0,
              "Curing method": "sealed in lab air 25 C RH 60 % 24 h, demoulded, steam " + ("75 C 2 d" if age == 3 else "90 C 3 d"),
              "Curing time (days)": age, "Curing temperature (°C)": 75 if age == 3 else 90, "Demolding age (days)": 1, "Test age (days)": age,
              "Heat curing duration (h)": 48 if age == 3 else 72, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 4 (results)",
              "Conversions / notes": f"{mid}. kg/m3 / B ({B}). Fibre 2 vol% stated. "
                                     "Mix 4 (W/B-0.16-RS/B-0.65) skipped: its fc equals the coarse-sand mix of 104204 (sand 2.36-4.75 mm, not allowed as sand). "
                                     f"VERIFY: test age {age} d derived (24 h + steam cure before testing). Table prints strain of mix 2 as '3.35 +- 0.0.3'."})
    if kind == "MSS":
        r["SS / B (Silica sand)"] = r4(sd / B)
        r["Sand max size (µm)"] = 250
    else:
        r["River sand / B"] = r4(sd / B)
    rows.append(r)

# ---------------------------------------------------------------- 7) Choi 2022 selvage PE fibres
P = {"Article Name": "Highly ductile behavior and sustainability of engineered cementitious composites reinforced by PE based selvage fibers",
     "Author": "Jeong-Il Choi, Se-Eon Park, YoungMin Kim, Kanghyeok Yang, Yun Yong Kim, Bang Yeon Lee", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2022.104729"}
for mid, vma, L, d, fc, fcr, fu, eps, note in [
        ("M-PE", 0.0017, 18.0, 13, 56.8, 3.57, 11.10, 4.80, "normal PE fibre 13 um, 3200 MPa, 111 GPa"),
        ("M-S", 0.001, 50.5, 18, 61.2, 2.94, 7.32, 4.49, "selvage weft S fibre (PE sheath + S-glass core)"),
        ("M-SC", 0.0017, 16.0, 18, 58.2, 2.91, 10.81, 6.55, "chopped selvage SC fibre (PE sheath + S-glass core)"),
        ("M-SP", 0.0014, 41.4, 18, 57.9, 2.18, 6.02, 4.34, "selvage fibre SP incl. warp (PE sheath + S-glass core)")]:
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": 0.38, "SP / B": 0.001, "VMA / B": vma, "PE fiber (vol%)": 1.75, "PE length (mm)": L, "PE diameter (µm)": d,
              "PE tensile strength (MPa)": 3200 if mid == "M-PE" else 3000, "PE elastic modulus (GPa)": 111 if mid == "M-PE" else 120,
              "Total fiber (vol%)": 1.75, "Curing method": "covered in room 23 C 1 d, demoulded, water 23 C to 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "50", "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 2-3 (fibres), Table 4 (fc), Table 5 (tension)",
              "Conversions / notes": f"{mid}: {note}. Weight ratios to cement; cement-only paste (no sand). Defoamer 0.001 also added. "
                                     "VERIFY: selvage fibres contain 16 wt% S-glass core (treated as selvage PE per the brief); entered as PE vol%."})
    rows.append(r)

# ---------------------------------------------------------------- 8) Deng 2022 ULECC, control T1 (no cenospheres / HGM)
P = {"Article Name": "Sustainable and cost-effective ultra-lightweight engineered cementitious composite: Design and material characterization",
     "Author": "Bo-Yu Deng, Ling-Zhi Li, Di Tan, Md Nasir Uddin, Zi-Wei Cai, Ke-Quan Yu", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2022.104895"}
B = 1 + 0.94 + 0.23
for mid, hot, fc, fcr, fu, eps in [("T1", False, 35.0, 2.90, 5.54, 1.34), ("T1w", True, 37.5, 2.79, 6.07, 6.00)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(0.94 / B), "SF (Silica fume)": r4(0.23 / B), "W / B": 0.32,
              "Fine sand / B": r4(1.98 / B), "PE fiber (vol%)": 1.0, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900,
              "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 1.0,
              "Curing method": ("demoulded 24 h, hot water 60 C 48 h then 20 C RH 95 % to 28 d" if hot else "demoulded 24 h, 20 C RH 95 % to 28 d"),
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
              "Heat curing duration (h)": 48 if hot else None, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
              "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix), Table 3 (PE), " + ("Tables 6 and 8" if hot else "Tables 5 and 7"),
              "Conversions / notes": f"{mid}: control without lightweight filler (FAC/HGM mixes skipped, not allowed). Weight ratios to cement; B = cement + FA + SF = 2.17. "
                                     "W/B 0.32 stated (0.70/2.17 = 0.323). PE 9.7 g/L and 'fibre volume fraction 1 %' stated. "
                                     "Fine silica sand 1.98. SP (6 g/L, powder PCE) and HPMC 0.5 g/L given per litre of mix, not entered."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e13.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e13.csv"))
