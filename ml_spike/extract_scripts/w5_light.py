"""Wave-5 agent 'light': lightweight / low-cost / local-material fiber composites from open-access papers.
Writes ml_spike/additions_v2/w5_light.csv (99-column TEMPLATE header).

All numbers were read from the paper text/tables (MDPI html tables, Wiley/Hindawi html, SciELO html).
Ratios are per the paper's binder B; kg/m3 values are divided by the binder content (noted per row).
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []


def r4(x):
    return None if x is None else round(x, 4)


def add_row(meta, **kw):
    r = dict(meta)
    r.update(kw)
    rows.append(r)


def meta(title, authors, year, doi):
    return {"Article Name": title, "Author": authors, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------------------------------------------------------------- 1) Hyun, Lee, Kim (2018) Appl. Sci. 8, 151
M = meta("Composite Properties and Micromechanical Analysis of Highly Ductile Cement Composite Incorporating Limestone Powder",
         "Jung Hwan Hyun, Bang Yeon Lee, Yun Yong Kim", 2018, "10.3390/app8020151")
# id, cement, LP, SP, VMA, fcr, ft, eps, ft/fc (%)
for mid, c, lp, sp, vma, fcr, ft, eps, ratio in [
        ("HDCC0", 1.0, 0.0, 0.0031, 0.0020, 4.0, 5.1, 2.6, 10.5),
        ("HDCC15", 0.85, 0.15, 0.0026, 0.0026, 3.7, 4.8, 3.1, 10.7),
        ("HDCC30", 0.70, 0.30, 0.0025, 0.0030, 3.2, 4.3, 3.7, 11.1),
        ("HDCC45", 0.55, 0.45, 0.0023, 0.0035, 2.6, 3.5, 4.2, 11.2)]:
    if mid == "HDCC0":
        fc, fcnote = 48.8, "fc 28 d = 48.8 MPa from text (p.4)."
    else:
        fc = round(ft / (ratio / 100), 1)
        fcnote = f"VERIFY: fc = ft / (ft/fc = {ratio} %, text p.4); fc itself only plotted in Fig. 3."
    add_row(M, **{"OPC / Cement": c, "Limestone powder": lp, "W / B": 0.45, "SS / B (Silica sand)": 0.80,
                  "SP / B": sp, "VMA / B": vma,
                  "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560,
                  "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2,
                  "Curing method": "covered with plastic sheet, demolded at 3 d, then water 23 °C",
                  "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 3, "Test age (days)": 28,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
                  "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
                  "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr,
                  "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 1 (fiber), Table 2 (mix), Table 3 (fcr, ft, strain), p.4 text (fc, ratios)",
                  "Conversions / notes": f"{mid}. Proportions by weight of cement + limestone powder (= B). Silica sand avg size 100 µm. "
                                         f"Defoamer 0.002 (not listed). {fcnote}"})

# ---------------------------------------------------------------- 2) Choi, Kim, Lee (2020) Appl. Sci. 10, 4300
M = meta("Mechanical and Fiber-Bridging Behavior of Slag-Based Composite with High Tensile Ductility",
         "Jeong-Il Choi, Hyeong-Ki Kim, Bang Yeon Lee", 2020, "10.3390/app10124300")
add_row(M, **{"GGBS": 0.895, "Ca(OH)2 / B": 0.075, "Na2SO4 / B": 0.030, "W / B": 0.30, "SP / B": 0.005, "VMA / B": 0.002,
              "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700,
              "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1.5,
              "Curing method": "sealed in molds 23 °C / 60 % RH for 2 d, demolded, then water 23 °C",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": 36.8, "Tensile strength (MPa)": 8.5, "First-cracking strength (MPa)": 3.4,
              "Tensile strain capacity (%)": 7.5,
              "Source table/page": "Table 1 (mix), Table 3 (fc, fcr, ft, strain), Section 2.1-2.2",
              "Conversions / notes": "Binder = GGBS 0.895 + Ca(OH)2 0.075 + Na2SO4 0.030 (paper's binder). Anti-foam 0.001 (not listed)."})

# ---------------------------------------------------------------- 3) Wen et al. (2026) Buildings 16, 1022 (river sand + tap water ECC only)
M = meta("Mechanical Strength and Toughness Performance of Seawater Sea Sand ECC with Variable Polyethylene Fiber Content and Length",
         "Zheming Wen, Qinghai Xie, Jie Zeng, Heng Dai, Haoyang Huang", 2026, "10.3390/buildings16051022")
B = 588.96 + 82.45 + 123.68 + 630.18
add_row(M, **{"OPC / Cement": r4(588.96 / B), "Limestone powder": r4(82.45 / B), "SF (Silica fume)": r4(123.68 / B),
              "GGBS": r4(630.18 / B), "W / B": r4(353.37 / B), "River sand / B": r4(612.51 / B), "SP / B": r4(8.83 / B),
              "Binder content (kg/m³)": round(B, 1),
              "PE fiber (vol%)": 1.5, "PE length (mm)": 12, "PE diameter (µm)": 25, "Total fiber (vol%)": 1.5,
              "Curing method": "film-covered in mold 1 d, demolded, film-covered at room temperature",
              "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
              "Tensile specimen": "dog-bone 368x100x50", "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": 45.92, "Tensile strength (MPa)": 2.04,
              "Source table/page": "Table 1 (mix), Table 8 (fcu, ft of 1.5%-12-ECC), Section 2",
              "Conversions / notes": "Mix 1.5%-12-ECC (river sand + tap water reference); kg/m3 / binder 1425.3 (C+LP+SF+slag). "
                                     "Seawater/sea-sand mixes not included. VERIFY: Table 1 uses merged cells (shared binder row). "
                                     "Doubtful: ft 2.04 MPa unusually low for 1.5 % PE ECC; strain not measured (strain gauges failed)."})

# ---------------------------------------------------------------- 4) Mathew & Aslani (2024) Buildings 14, 1092 (control ECC only)
M = meta("Investigation of Drying Shrinkage Characteristics in Lightweight Engineered Cementitious Composites",
         "Agnel Mathew, Farhad Aslani", 2024, "10.3390/buildings14041092")
B = 1 + 1.33 + 0.11
for age, fc in [(7, 40.75), (28, 45.02)]:
    add_row(M, **{"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(1.33 / B), "SF (Silica fume)": r4(0.11 / B),
                  "W / B": r4(0.65 / B), "SS / B (Silica sand)": r4(0.89 / B), "Sand max size (µm)": 600,
                  "PVA fiber (vol%)": 1.75, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
                  "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 1.75,
                  "Curing method": "demolded at 48 h, then controlled room 20 °C / 50 % RH (curing stated for shrinkage specimens)",
                  "Curing temperature (°C)": 20, "Curing RH (%)": 50, "Demolding age (days)": 2, "Test age (days)": age,
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 5 (mix), Table 7 (fc), Section 2.2",
                  "Conversions / notes": "Control-ECC only (other mixes contain hollow glass microspheres). Proportions by mass of cement; "
                                         "B = cement + FA + SF = 2.44. Effective w/b 0.27 (text). SP 1.000 % listed, reference mass not stated -> not filled. "
                                         "Sand AFS 45/50 (0.3 % retained on 600 µm sieve)."})

# ---------------------------------------------------------------- 5) Wang, Che, Liu, Chin (2023) Buildings 13, 1538
M = meta("Enhanced Ductility and Toughness of Desert Sand Engineered Cementitious Composites",
         "Dan Wang, Jialing Che, Haifeng Liu, Siew Choo Chin", 2023, "10.3390/buildings13061538")
# id, W/B, S/B, FA ratio, sand column, sand max, {age: (ft, eps, fc)}
mix5 = [("M1", 0.29, 0.46, 0.5, "Dune sand / B", 546, "Mu Us desert sand", {28: (10.18, 3.23, 51.34), 56: (9.71, 3.19, 57.66)}),
        ("M2", 0.35, 0.35, 0.5, "Dune sand / B", 546, "Mu Us desert sand", {28: (14.84, 4.06, 34.31), 56: (10.67, 4.82, 52.98)}),
        ("M3", 0.35, 0.35, 0.7, "Dune sand / B", 546, "Mu Us desert sand", {28: (12.17, 5.38, 23.85), 56: (11.07, 6.68, 25.77)}),
        ("T4", 0.35, 0.35, 0.5, "Dune sand / B", 376, "Tengger desert sand", {28: (10.03, 3.76, 36.50), 56: (9.55, 2.74, 46.27)}),
        ("R6", 0.35, 0.35, 0.5, "River sand / B", 1180, "river sand", {28: (12.27, 2.64, 41.32), 56: (11.44, 4.58, 51.94)})]
for mid, wb, sb, fa, scol, smax, sname, res in mix5:
    for age, (ft, eps, fc) in res.items():
        add_row(M, **{"OPC / Cement": round(1 - fa, 2), "FA (Fly ash)": fa, "W / B": wb, scol: sb, "Sand max size (µm)": smax,
                      "SP / B": 0.001,
                      "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
                      "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": 2,
                      "Curing method": "demolded at 24 h, fog room 20 °C / 95 % RH",
                      "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
                      "Test age (days)": age,
                      "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75x150",
                      "Tensile specimen": "dumbbell (JSCE) 330x60x13", "Tensile test type": "direct (uniaxial)",
                      "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                      "Source table/page": "Table 3 (mix), Table 4 (sigma_ut, eps_ut, sigma_uc), Section 2.1-2.3",
                      "Conversions / notes": f"{mid}, {sname}. B = cement + FA. VERIFY: SP 0.1 % shown once in merged mix-table cells, "
                                             f"assumed for all mixes. Doubtful: tensile strengths 9.5-14.8 MPa are unusually high for PVA-ECC "
                                             f"(values as printed in Table 4)."})

# ---------------------------------------------------------------- 6) Abd Elmoaty, Morsy, Harraz (2022) Buildings 12, 2108 (steel-fiber mixes only)
M = meta("Effect of Fiber Type and Volume Fraction on Fiber Reinforced Concrete and Engineered Cementitious Composite Mechanical Properties",
         "Abd Elmoaty M. Abd Elmoaty, Alaa M. Morsy, Abdelrhman B. Harraz", 2022, "10.3390/buildings12122108")
B = 578 + 693.5
for mid, vf, sand, hrwr, res in [("Mixture 7 (2% C.S.F)", 2, 462.25, 3.00, {7: 48.20, 28: 72.00}),
                                 ("Mixture 8 (4% C.S.F)", 4, 411.45, 3.50, {7: 55.00, 28: 89.00})]:
    for age, fc in res.items():
        add_row(M, **{"OPC / Cement": r4(578 / B), "FA (Fly ash)": r4(693.5 / B), "W / B": r4(323.5 / B),
                      "SS / B (Silica sand)": r4(sand / B), "Sand max size (µm)": 200, "SP / B": r4(hrwr / B),
                      "Binder content (kg/m³)": B,
                      "Steel fiber (vol%)": vf, "Steel length (mm)": 60, "Steel diameter (µm)": 900, "Steel tensile strength (MPa)": 1000,
                      "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": vf,
                      "Curing method": "in molds 24 h at room temperature, demolded, water 20 °C",
                      "Curing time (days)": age, "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": age,
                      "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
                      "Compressive strength (MPa)": fc,
                      "Source table/page": "Table 2 (fiber), Table 3 (mix), Table 6 (fc)",
                      "Conversions / notes": f"{mid}, corrugated steel fiber. kg/m3 / binder 1271.5 (cement + FA). HRWR assumed kg/m3 (column unit not printed). "
                                             f"No direct tension test (splitting only). PP/PO/glass mixes not included."})

# ---------------------------------------------------------------- 7) da Costa & Magalhaes (2026) Ambiente Construido 26, e154564
M = meta("Manufactured sand particle size and mechanical behaviour of strain-hardening cementitious composites",
         "Vivianne Machado da Costa, Margareth da Silva Magalhães", 2026, "10.1590/s1678-86212026000101003")
for mid, c, fa, s, w, sp, scol, smax, fcr, ft, eps in [
        ("NS", 530.94, 637.12, 420.50, 355.27, 9.34, "Fine sand / B", 300, 3.79, 5.01, 2.26),
        ("MS-0.3", 528.64, 634.37, 418.69, 353.73, 9.30, "M-sand / B", 300, 3.77, 4.72, 2.27),
        ("MS-0.6", 524.46, 629.35, 415.37, 354.05, 4.96, "M-sand / B", 600, 3.92, 4.65, 2.16),
        ("MS-1.18", 527.97, 633.56, 418.15, 356.68, 4.65, "M-sand / B", 1180, 5.03, 5.75, 1.98),
        ("MS-2.36", 529.64, 635.57, 419.47, 356.95, 5.83, "M-sand / B", 2360, 4.78, 5.15, 0.97)]:
    B = c + fa
    add_row(M, **{"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), scol: r4(s / B),
                  "Sand max size (µm)": smax, "SP / B": r4(sp / B), "Binder content (kg/m³)": round(B, 1),
                  "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40,
                  "Total fiber (vol%)": 2,
                  "Curing method": "demolded at 24 h, lime-saturated water",
                  "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
                  "Tensile specimen": "dogbone 330 mm, 30x30 mm section", "Tensile test type": "direct (uniaxial)",
                  "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 3 (mix), Table 6 (tensile)",
                  "Conversions / notes": f"{mid}. kg/m3 / binder (cement CP II-F-40 + fly ash). "
                                         f"{'Natural fine sand < 0.30 mm. ' if mid == 'NS' else 'Crushed gneissic-granitic manufactured sand. '}"
                                         f"PVA 26 kg/m3 = 2 vol%. Composite fc only in Fig. 7a -> not filled. Test age taken as end of 28 d curing."})

# ---------------------------------------------------------------- 8) Shiferaw et al. (2024) Fibers 12, 70
M = meta("Influence of Fiber Dimensions on Bridging Performance of Polyvinyl Alcohol Fiber-Reinforced Cementitious Composite (PVA-FRCC)",
         "Helen Negash Shiferaw, Selamawit Fthanegest Abrha, Toshiyuki Kanakubo, Madappa V. R. Sivasubramanian, Shamsher Bahadur Singh",
         2024, "10.3390/fib12080070")
B = 678 + 291
for mid, d, L, fu, E, fc in [("PVA027-06", 27, 6, 1800, 46, 49.0), ("PVA040-12", 40, 12, 1560, 41, 37.2),
                             ("PVA100-12", 100, 12, 1200, 28, 47.7), ("PVA200-12", 200, 12, 910, 30, 45.0),
                             ("PVA200-18", 200, 18, 975, 27, 43.3), ("PVA660-30", 660, 30, 900, 23, 47.4)]:
    add_row(M, **{"OPC / Cement": r4(678 / B), "FA (Fly ash)": r4(291 / B), "W / B": r4(380 / B),
                  "Sand (type not stated) / B": r4(484 / B), "Sand max size (µm)": 200, "SP / B": 0.006,
                  "Binder content (kg/m³)": B,
                  "PVA fiber (vol%)": 2, "PVA length (mm)": L, "PVA diameter (µm)": d, "PVA tensile strength (MPa)": fu,
                  "PVA elastic modulus (GPa)": E, "Total fiber (vol%)": 2,
                  "Curing method": "sealed 7 d, then air at room temperature",
                  "Curing time (days)": 7, "Test age (days)": 30,
                  "Compressive specimen": "cylinder",
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 1 (fiber), Table 2 (mix), Table 3 (fc)",
                  "Conversions / notes": f"{mid}. kg/m3 / binder 969 (high-early-strength PC + JIS type II FA). SP = binder x 0.6 %. "
                                         f"No direct tension test (notched bending only)."})

# ---------------------------------------------------------------- 9) Ding et al. (2021) Adv. Mater. Sci. Eng. 7183288
M = meta("Polyvinyl Alcohol Fiber Length Optimization for High Ductility Cementitious Composites with Different Compressive Strength Grades",
         "Ding Cong, Guo Liping, Ren Jinming, Wang Yongming, Li Xinyu, Yu Bing, Gao Yuan, Liu Wanpeng", 2021, "10.1155/2021/7183288")
mix9 = [("0.30-80%", 0.2, 0.8, 0.30, 0.0017, 0.0004, "P II 42.5 R",
         {6: 36.7, 9: 35.4, 12: 35.9, 18: 35.4, 24: 36.1}, {9: (4.91, 2.52), 12: (4.92, 2.34)}),
        ("0.30-60%", 0.4, 0.6, 0.30, 0.0019, 0.0004, "P II 42.5 R",
         {6: 52.9, 9: 51.5, 12: 52.2, 18: 51.1, 24: 51.8}, {9: (4.69, 2.05), 12: (4.91, 1.74)}),
        ("0.25-60%", 0.4, 0.6, 0.25, 0.0032, 0.0005, "P II 42.5 R",
         {6: 66.6, 9: 64.3, 12: 64.3, 18: 62.5, 24: 62.7}, {9: (4.74, 1.67), 12: (5.87, 1.05)}),
        ("0.22-60%", 0.4, 0.6, 0.22, 0.010, 0.001, "P II 52.5 R",
         {6: 77.9, 9: 76.2, 12: 75.9, 18: 76.9, 24: 76.3}, {9: (6.08, 0.40), 12: (5.67, 0.39)})]
for mid, c, fa, wb, sp, hpmc, cem, fcs, tens in mix9:
    for L, fc in fcs.items():
        ft, eps = tens.get(L, (None, None))
        add_row(M, **{"OPC / Cement": c, "FA (Fly ash)": fa, "W / B": wb, "River sand / B": 0.3, "SP / B": sp,
                      "HPMC / B (hydroxypropyl methyl cellulose)": hpmc,
                      "PVA fiber (vol%)": 2, "PVA length (mm)": L, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1260,
                      "PVA elastic modulus (GPa)": 30, "Total fiber (vol%)": 2,
                      "Curing method": "covered with plastic sheet, demolded at 24 h, standard curing 20 °C / 95 % RH",
                      "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
                      "Test age (days)": 28,
                      "Compressive specimen": "cube", "Compressive specimen size (mm)": "40",
                      "Tensile specimen": "dogbone (JSCE), 13x30 section" if ft else None,
                      "Tensile test type": "direct (uniaxial)" if ft else None,
                      "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                      "Source table/page": "Table 2 (fiber), Table 3 (mix), Table 4 (fc, tensile)",
                      "Conversions / notes": f"HDCC {mid}-{L} mm. Proportions by weight of binder (cement {cem} + class F FA). "
                                             f"HPWR and HPMC given as % of binder. Tension tested only for 9 and 12 mm fibers."})

# ---------------------------------------------------------------- 10) Han, Liu, Guo, Niu (2022) Adv. Mater. Sci. Eng. 7876056
M = meta("Optimized Design of Polyethylene Fiber-Engineered Cementitious Composite Mix Ratio Based on the Analytic Hierarchy Process",
         "Fengxia Han, Qing Liu, Xin Guo, Yanfeng Niu", 2022, "10.1155/2022/7876056")
mix10 = {"A-0.25": (742.2, 318.1, 318.1, 265.1, 10.00), "A-0.27": (721.9, 309.4, 309.4, 278.5, 8.25),
         "A-0.29": (702.8, 301.2, 301.2, 291.1, 5.02), "A-0.31": (684.6, 293.4, 293.4, 303.2, 3.91),
         "B-0.27": (610.6, 407.0, 305.3, 274.8, 8.14), "C-0.27": (502.1, 502.1, 301.3, 271.1, 3.50),
         "D-0.27": (396.5, 594.7, 297.3, 267.6, 2.97)}
res10 = {
    "FA-A-0.25": [(7, 2.13, 5.63, 3.59), (28, 2.34, 6.34, 4.23), (60, 2.71, 6.75, 7.07)],
    "FA-A-0.27": [(7, 1.92, 4.96, 4.03), (28, 2.93, 6.59, 7.34), (60, 2.49, 5.83, 4.55)],
    "FA-A-0.29": [(7, 2.32, 4.26, 3.34), (28, 2.13, 4.91, 2.85), (60, 2.33, 5.37, 3.97)],
    "FA-A-0.31": [(7, 1.97, 4.45, 3.37), (28, 1.99, 5.79, 3.97), (60, 1.93, 5.56, 4.88)],
    "FA-B-0.27": [(7, 2.21, 4.81, 4.01), (28, 2.15, 4.84, 4.36), (60, 2.14, 5.90, 4.55)],
    "FA-C-0.27": [(7, 2.56, 5.23, 4.48), (28, 2.21, 5.56, 4.33), (60, 2.18, 6.29, 5.86)],
    "FA-D-0.27": [(7, 2.06, 4.53, 3.46), (28, 2.63, 5.46, 5.30), (60, 1.97, 4.93, 3.04)],
    "KF-A-0.25": [(7, 2.32, 6.36, 6.16), (28, 2.39, 6.66, 6.46), (60, 2.82, 6.08, 6.00)],
    "KF-A-0.27": [(7, 2.00, 6.02, 6.01), (28, 2.50, 5.98, 5.18), (60, 2.16, 5.54, 4.40)],
    "KF-A-0.29": [(7, 2.20, 4.67, 4.10), (28, 2.49, 5.60, 5.37), (60, 2.10, 6.03, 6.15)],
    "KF-A-0.31": [(7, 2.20, 4.75, 4.04), (28, 2.40, 5.77, 5.72), (60, 2.59, 5.31, 3.47)],
    "KF-B-0.27": [(7, 2.27, 6.00, 7.30), (28, 2.64, 4.82, 3.64), (60, 2.53, 5.24, 4.70)],
    "KF-C-0.27": [(7, 2.62, 4.93, 4.84), (28, 2.27, 5.09, 4.35), (70, 2.33, 5.39, 4.94)],
    "KF-D-0.27": [(7, 2.39, 4.47, 5.07), (28, 1.72, 5.13, 3.98), (60, 1.90, 5.86, 6.00)]}
for mid, res in res10.items():
    kind, key = mid[:2], mid[3:]
    c, ma, s, w, wr = mix10[key]
    B = c + ma
    for age, fcr, ft, eps in res:
        add_row(M, **{"OPC / Cement": r4(c / B), ("FA (Fly ash)" if kind == "FA" else "GGBS"): r4(ma / B),
                      "W / B": r4(w / B), "Sand (type not stated) / B": r4(s / B), "Sand max size (µm)": 1180,
                      "SP / B": r4(wr / B), "VMA / B": r4(0.25 / B),
                      "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
                      "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2,
                      "Curing method": "standard curing 20 °C / RH >= 95 %",
                      "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": age,
                      "Tensile specimen": "dumbbell, 80x30x15 mm middle part", "Tensile gauge length (mm)": 80,
                      "Tensile test type": "direct (uniaxial)",
                      "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
                      "Source table/page": "Table 4 (fiber), Table 5 (mix, g per batch), Table 8 (tensile)",
                      "Conversions / notes": f"PE-{mid}. Batch masses (g) / binder (P.O 42.5 + {'class II fly ash' if kind == 'FA' else 'GGBS (KF)'}). "
                                             f"Natural washed sand < 1.18 mm. Thickening agent stored as VMA. "
                                             f"VERIFY: strain = Table 8 'average elongation (%)', which equals the tabulated tensile "
                                             f"displacement in mm (gauge 80 mm) - possible unit inconsistency in the paper."
                                             f"{' Age 70 d as printed (other mixes 60 d).' if age == 70 else ''}"})

# ---------------------------------------------------------------- 11) Chen et al. (2025) Buildings 15, 4003 (PE and PVA mixes)
M = meta("Flexural Performance and Flexural Toughness Evaluation Method of High-Strength Engineered Cementitious Composites",
         "Bo Chen, Liang Hou, Rong-Guo Yan, Xiang-Yu Zhang, Hao Meng, Jing-Tian Li", 2025, "10.3390/buildings15214003")
B = 543.2 * 2 + 135.8 * 2
for fib, vals in [("PE", [51.7, 54.3, 61.3, 70.1, 83.6]), ("PVA", [50.1, 50.8, 56.3, 62.6, 58.4])]:
    for vf, fc in zip([0.5, 1.0, 1.5, 2.0, 2.5], vals):
        r = {"OPC / Cement": r4(543.2 / B), "FA (Fly ash)": r4(543.2 / B), "GGBS": r4(135.8 / B), "SF (Silica fume)": r4(135.8 / B),
             "W / B": r4(339.5 / B), "SS / B (Silica sand)": r4(502.5 / B), "Sand max size (µm)": 2000,
             "Binder content (kg/m³)": B, "Total fiber (vol%)": vf,
             "Curing method": "standard curing 20 °C / RH >= 95 %", "Curing time (days)": 28, "Curing temperature (°C)": 20,
             "Curing RH (%)": 95, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive strength (MPa)": fc,
             "Source table/page": "Table 1 (fiber), Table 2 (mix), Table 3 (fcu)",
             "Conversions / notes": f"{fib}-{vf}. kg/m3 / binder 1358. Superplasticizer used but dosage not reported (SP/B empty). "
                                    f"Fiber diameter from aspect ratio ({'480' if fib == 'PE' else '500'}) and 12 mm length. No direct tension (flexure only)."}
        if fib == "PE":
            r.update({"PE fiber (vol%)": vf, "PE length (mm)": 12, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 3100,
                      "PE elastic modulus (GPa)": 122})
        else:
            r.update({"PVA fiber (vol%)": vf, "PVA length (mm)": 12, "PVA diameter (µm)": 24, "PVA tensile strength (MPa)": 1600,
                      "PVA elastic modulus (GPa)": 40})
        add_row(M, **r)

# ---------------------------------------------------------------- 12) Liu et al. (2023) Buildings 13, 1341 (IOT0 control only)
M = meta("Development of Engineered Cementitious Composites (ECCs) Incorporating Iron Ore Tailings as Eco-Friendly Aggregates",
         "Kangning Liu, Sheliang Wang, Xiaoyi Quan, Jing Wu, Jin Xu, Nan Zhao, Bo Liu", 2023, "10.3390/buildings13051341")
B = 692 + 377.4 + 188.7
add_row(M, **{"OPC / Cement": r4(692 / B), "FA (Fly ash)": r4(377.4 / B), "Metakaolin": r4(188.7 / B), "W / B": r4(440.3 / B),
              "SS / B (Silica sand)": r4(565.6 / B), "SP / B": r4(5.66 / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 42, "Total fiber (vol%)": 2, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
              "Compressive strength (MPa)": 28.1,
              "Source table/page": "Table 3 (fiber), Table 4 (mix), Table 7 (fc), Section 2.5",
              "Conversions / notes": "IOT0-P2.0 (reference with silica sand; iron-ore-tailing mixes not included). kg/m3 / binder 1258.1. "
                                     "PVA 26 kg/m3 = 2 vol% (density 1.3). Axial (cylinder) compressive strength; 100 mm cube fcu only in Fig. 4. "
                                     "Curing regime not stated."})

# ---------------------------------------------------------------- 13) Kang, Adsul, Lee (2025) Fibers 13, 133
M = meta("Structural Behaviour of Slab-on-Grade Constructed Using High-Ductility Fiber-Reinforced Cement Composite: Experimental and Analytical Investigation",
         "Su-Tae Kang, Nilam Adsul, Bang Yeon Lee", 2025, "10.3390/fib13100133")
B = 1217
add_row(M, **{"OPC / Cement": 1.0, "W / B": r4(426 / B), "Sand (type not stated) / B": r4(483 / B), "Sand max size (µm)": 500,
              "SP / B": r4(4.26 / B), "VMA / B": r4(0.852 / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": round(14.55 / 970 * 100, 2), "PE length (mm)": 12, "PE diameter (µm)": 16,
              "Total fiber (vol%)": round(14.55 / 970 * 100, 2), "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
              "Compressive strength (MPa)": 54,
              "Source table/page": "Table 2 (mix), Section 4.1 / abstract (fc)",
              "Conversions / notes": "HDFRCC, kg/m3 / cement 1217. PE 14.55 kg/m3 (1.2 wt% of cement) -> vol% with PE density 970. "
                                     "Anti-foam 0.298 kg/m3 (not listed). 'Sand with a grain size of 0.5 mm'. Curing regime not stated."})

# ---------------------------------------------------------------- 14) Kim et al. (2021) Sustainability 13, 3607
M = meta("Structural Performance and Reinforcement Improvement of Structural Walls Using Strain-Hardening Cementitious Composites",
         "Hyeong-Ki Kim, Chang-Geun Cho, Sun-Ju Lee, Young Hak Lee, Taehoon Kim", 2021, "10.3390/su13073607")
B = 500 + 167 + 167
add_row(M, **{"OPC / Cement": r4(500 / B), "FA (Fly ash)": r4(167 / B), "GGBS": r4(167 / B), "W / B": r4(375 / B),
              "SS / B (Silica sand)": r4(692 / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": 2,
              "Curing method": "demolded at 1 d, water", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": 38.4, "Tensile strength (MPa)": 3.8, "First-cracking strength (MPa)": 3.3,
              "Tensile strain capacity (%)": 3.6,
              "Source table/page": "Table 1 (fiber), Table 2 (mix), Table 3 (tensile), Section 2.2 (fc)",
              "Conversions / notes": "kg/m3 / binder 834 (OPC + FA + BFS; table prints B = 883). W/B 0.45 as stated. "
                                     "VERIFY: table also states S/C = 71 % while silica sand 692 kg/m3 (used). PCSP 0.37, HPMC 0.18, "
                                     "defoamer 0.45 printed without unit -> SP/HPMC not filled. Tensile values = average of 3 specimens."})

# ---------------------------------------------------------------- 15) Zhang et al. (2024) Buildings 14, 449
M = meta("Mechanical Properties and Microstructure of Highly Flowable Geopolymer Composites with Low-Content Polyvinyl Alcohol Fiber",
         "Hongmei Zhang, Fan Hu, Yuanfeng Duan, Jian Liao, Jiaqi Yang", 2024, "10.3390/buildings14020449")
B = 80.2 + 641.6 + 80.2
for vf, fc3, fc28 in [(0.1, 21.66, 49.12), (0.15, 22.04, 50.04), (0.2, 21.04, 47.56)]:
    for age, fc in [(3, fc3), (28, fc28)]:
        add_row(M, **{"GGBS": r4(80.2 / B), "FA (Fly ash)": r4(641.6 / B), "SF (Silica fume)": r4(80.2 / B),
                      "WG / B (Water glass)": r4(270.8 / B), "NaOH / B": r4(24.3 / B), "Activator modulus Ms (SiO2/Na2O)": None,
                      "W / B": r4(104.3 / B), "SS / B (Silica sand)": r4(962.4 / B), "Sand max size (µm)": 425,
                      "Binder content (kg/m³)": B,
                      "PVA fiber (vol%)": vf, "PVA length (mm)": 6, "PVA diameter (µm)": 17, "Total fiber (vol%)": vf,
                      "Test age (days)": age, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
                      "Compressive strength (MPa)": fc,
                      "Source table/page": "Table 2 (fiber), Table 3 (mix), Table 5 (cube fc), Section 2.1",
                      "Conversions / notes": f"PVA {vf} vol%. kg/m3 / binder 802 (slag + FA + SF). Activator: sodium silicate solution "
                                             f"(initial modulus 2.25, solids not given) 270.8 + NaOH 24.3 kg/m3; W/B = added water only "
                                             f"(paper's overall w/b 0.32 incl. activator water; Na2O 6 % of binder). Quartz sand 0.180-0.425 mm. "
                                             f"Curing regime not stated in text. Tensile (dog-bone) results only in figures; fiber-free control not included."})

# ---------------------------------------------------------------- drop DOIs already present in other agents' w5 files / existing list
other = set()
for f in os.listdir(out_dir):
    if f.startswith("w5_") and f != "w5_light.csv" and f != "w5_light_rejected.txt":
        p = os.path.join(out_dir, f)
        if f.endswith(".csv"):
            other |= set(pd.read_csv(p, encoding="utf-8-sig")["DOI / URL"].astype(str).str.lower()
                         .str.replace("https://doi.org/", "", regex=False))
        elif f.endswith(".txt"):
            for line in open(p, encoding="utf-8", errors="ignore"):
                if line.strip():
                    other.add(line.split("|")[0].split()[0].strip().lower().replace("https://doi.org/", ""))
existing = set(l.strip().lower() for l in open(os.path.join(out_dir, "existing_dois.txt")) if l.strip())
# Fixed list (checked 2026-11-16 against w5_pe.csv, which was written first). Kept static so that re-running
# this script never makes two agents drop the same paper from each other.
TAKEN_BY_OTHERS = {"10.3390/app10124300", "10.3390/buildings16051022", "10.1155/2022/7876056", "10.3390/buildings15214003"}
rows = [r for r in rows if r["DOI / URL"].lower().replace("https://doi.org/", "") not in TAKEN_BY_OTHERS]
mine = {r["DOI / URL"].lower().replace("https://doi.org/", "") for r in rows}
if mine & (other | existing):
    print("WARNING - overlap with other files:", sorted(mine & (other | existing)))

df = pd.DataFrame(rows).reindex(columns=cols)
out = os.path.join(out_dir, "w5_light.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", out)
