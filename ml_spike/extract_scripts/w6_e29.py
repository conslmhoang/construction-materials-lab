"""Wave 6, agent e29: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e29.csv (99-column TEMPLATE header).
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


def add_row(P, d):
    r = dict(P)
    r.update(d)
    rows.append(r)


def pva(l, dia, ts, e):
    return {"PVA length (mm)": l, "PVA diameter (µm)": dia, "PVA tensile strength (MPa)": ts, "PVA elastic modulus (GPa)": e}


# ---------- 1) Tian et al. 2022: ECC-1 and ECC-4 (dog-bone tension, PVA type R)
P = {"Article Name": "Experimental study and mechanics model of ECC-to-concrete bond interface under tensile loading",
     "Author": "Jun Tian, Xiaowei Wu, Wen-Wei Wang, Shaowei Hu, Xiao Tan, Yinfei Du, Yu Zheng, Can Sun", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.compstruct.2022.115203"}
for nm, w, c, fa, sf, s, wr, fc, ft, eps in [("ECC-1", 397, 248, 992, 40, 248, 1, 21.7, 4.17, 3.03),
                                              ("ECC-4", 353, 379, 954, 40, 309, 4, 40.8, 5.52, 3.72)]:
    B = c + fa + sf
    add_row(P, {"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B),
                "Sand (type not stated) / B": r4(s / B), "HRWR / B": r4(wr / B), "Binder content (kg/m³)": B,
                "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, **pva(12, 39, 1560, 38),
                "Curing method": "demoulded, curing chamber 28 d, RH > 95 %", "Curing time (days)": 28, "Curing temperature (°C)": 20,
                "Curing RH (%)": 95, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
                "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                "Source table/page": "Table 1 (mix), Table 2 (fc, ft, elongation), sect. 2.3 (curing)",
                "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA + SF = {B}). VERIFY: Table 1 columns are garbled, row read as water, cement, FA, SF, fine aggregate, water reducer; "
                                       "ECC-2 / ECC-3 skipped (accelerator column, unclear). Test age 28 d assumed from the 28 d curing (ECC tests not dated explicitly). "
                                       "Strain = 'Elongation (%)' of Table 2 from dog-bone tests. PVA 2 vol% (Table 1), type R 12 mm / 39 um."})

# ---------- 2) Cao et al. 2023: ECC-50 and ECC-80, fc only
P = {"Article Name": "Experimental study on the bonding performance of engineered cementitious composites to normal concrete interface subjected to salt freeze-thaw cycles",
     "Author": "Jincheng Cao, Fangwen Wu, Song Lei, Xiangyan Fan, Laijun Liu, Zirun Li, Ao Chen", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.compstruct.2023.117828"}
for nm, w, c, fa, sf, wr, s, fc in [("ECC-50", 396.8, 248.0, 992.0, 40.0, 3, 248.0, 49.7), ("ECC-80", 473.0, 956.5, 286.5, 40.0, 4, 250.0, 79.5)]:
    B = c + fa + sf
    add_row(P, {"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B),
                "Sand (type not stated) / B": r4(s / B), "HRWR / B": r4(wr / B), "Binder content (kg/m³)": B,
                "PVA fiber (vol%)": 1.5, "Total fiber (vol%)": 1.5, **pva(12, 38, 1620, 42.8),
                "Curing method": "demoulded 48 h, standard curing room 28 d", "Curing time (days)": 28, "Test age (days)": 28,
                "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
                "Compressive strength (MPa)": fc, "Source table/page": "Table 3 (mix), Table 4 (fc), Table 2 (PVA), sect. 2.3 (curing)",
                "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA + SF = {B}). Silica sand per text, entered as sand. VERIFY: Table 4 gives no test age; 28 d taken from the 28 d standard curing. "
                                       "Tensile strength in Table 4 (test type not stated) not entered."})

# ---------- 3) Zhu et al. 2012: ECC reference, strain + fc
P = {"Article Name": "Autogenous self-healing of engineered cementitious composites under freeze-thaw cycles",
     "Author": "Yu Zhu, Yingzi Yang, Yan Yao", "Year": 2012, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2012.03.001"}
B = 636 + 636
add_row(P, {"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": r4(318 / B), "SS / B (Silica sand)": r4(462 / B), "HRWR / B": r4(18 / B),
            "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
            "Curing method": "20 C RH 90 % for 7 d, then lab 20 C RH 55 % for 20 d (after 24 h in mould)", "Curing time (days)": 27,
            "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": 28,
            "Tensile test type": DIRECT, "Compressive strength (MPa)": 60, "Tensile strength (MPa)": 5.0, "Tensile strain capacity (%)": 2.5,
            "Source table/page": "Table 1 (mix), sect. 2.3 (28 d tension and fc), sect. 2.2 (curing)",
            "Conversions / notes": "kg/m3 / B (PC + FA = 1272). PVA 26 kg/m3 -> 2.0 vol% (VERIFY: derived, density 1300). fc 'about 60 MPa' (VERIFY: approximate, from text). "
                                   "Strain 2.5 +/- 0.47 %, strength 5.0 +/- 0.53 MPa at 28 d (text). Microsilica sand entered as silica sand."})

# ---------- 4) Desai et al. 2014: 0% PCM-ECC control
P = {"Article Name": "Development of thermally adaptive Engineered Cementitious Composite for passive heat storage",
     "Author": "Devki Desai, Meredith Miller, Jerome P. Lynch, Victor C. Li", "Year": 2014, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2013.12.104"}
add_row(P, {"OPC / Cement": r4(1 / 3), "FA (Fly ash)": r4(2 / 3), "W / B": r4(0.79 / 3), "SS / B (Silica sand)": r4(1.11 / 3), "SP / B": r4(0.02 / 3),
            "PVA fiber (vol%)": 1.9, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "Total fiber (vol%)": 1.9,
            "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50.8", "Tensile specimen": "dog-bone",
            "Tensile test type": DIRECT, "Compressive strength (MPa)": 47, "Tensile strength (MPa)": 5.2, "First-cracking strength (MPa)": 3,
            "Tensile strain capacity (%)": 2, "Source table/page": "Table 1 (mix), sect. 3.1-3.2 (text values; figures 7-9)",
            "Conversions / notes": "0% PCM-ECC control only (PCM mix skipped). Ratios relative to cement 1 : FA 2 -> divided by B = 3. PVA 0.06 by mass of cement -> about 1.9 vol% (VERIFY: derived with assumed densities). "
                                   "VERIFY: values (fc 47, strength 5.2, strain 2 %, first crack 3 MPa) are rounded averages stated in the text. Curing not described. Sand F-100 treated as silica sand."})

# ---------- 5) Ma et al. 2014: C-ECC, fc at 3, 7, 28 d
P = {"Article Name": "Effect of self-healing on water permeability and mechanical property of Medium-Early-Strength Engineered Cementitious Composites",
     "Author": "Hui Ma, Shunzhi Qian, Zhigang Zhang", "Year": 2014, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2014.05.065"}
for age, fc in ((3, 10.9), (7, 20.0), (28, 40.1)):
    add_row(P, {"OPC / Cement": 0.4, "FA (Fly ash)": 0.6, "W / B": 0.3, "Sand (type not stated) / B": 0.36, "SP / B": 0.008,
                "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, **pva(8, 39, 1620, 42.8),
                "Curing method": "demoulded 24 h, sealed moist curing RH 95 % 20 C until test", "Curing time (days)": age,
                "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": age,
                "Compressive specimen": "cube", "Compressive specimen size (mm)": "75", "Compressive strength (MPa)": fc,
                "Source table/page": "Table 2 (mix, control C-ECC), Table 6 (fc), sect. 2.3 (curing)",
                "Conversions / notes": "C-ECC (without early-strength agent); MES-ECC skipped. Ratios C 1 : FA 1.5 : S 0.9, W/(C+FA) 0.3, divided by B = 2.5. "
                                       "VERIFY: SP 0.02 assumed relative to cement -> /B = 0.008. Sand type not stated (sand 0.9). Converted tensile strain (from bending) not entered."})

# ---------- 6) Wang et al. 2017: SHCC-PVA and SHCC-ST+PE, static fc 28 d
P = {"Article Name": "Effect of high strain rate on compressive behavior of strain-hardening cement composite in comparison to that of ordinary fiber-reinforced concrete",
     "Author": "Shasha Wang, Hoang Thanh Nam Le, Leong Hien Poh, Ser Tong Quek, Min-Hong Zhang", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2016.12.183"}
cur = "wet linen 24 h, fog room 20 d (28-30 C), then 30 C RH 65 % until test"
B = 587 + 704
add_row(P, {"OPC / Cement": r4(587 / B), "FA (Fly ash)": r4(704 / B), "W / B": r4(323 / B), "Sand (type not stated) / B": r4(469 / B),
            "Sand max size (µm)": 250, "SP / B": r4(10 / B), "VMA / B": r4(2.9 / B), "Binder content (kg/m³)": B,
            "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, **pva(12, 40, 1612, 41),
            "Curing method": cur, "Curing time (days)": 28, "Curing temperature (°C)": 30, "Curing RH (%)": 65, "Test age (days)": 28,
            "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": 62.0,
            "Source table/page": "Table 2 (mix), Table 4 (D100 cylinder fc), Table 3 (28 d static test), Table 1 (fibres)",
            "Conversions / notes": "SHCC-PVA, quasi-static fc of D100 x 200 cylinder at 28 d. kg/m3 / B (cement + FA = 1291). Sand < 0.25 mm. FRHSC mixes (coarse aggregate) skipped."})
B = 1478 + 148
add_row(P, {"OPC / Cement": r4(1478 / B), "SF (Silica fume)": r4(148 / B), "W / B": r4(414 / B), "SP / B": r4(17 / B), "Binder content (kg/m³)": B,
            "PE fiber (vol%)": 1.5, "PE length (mm)": 12, "PE diameter (µm)": 39, "PE tensile strength (MPa)": 2610, "PE elastic modulus (GPa)": 66,
            "Steel fiber (vol%)": 0.5, "Steel length (mm)": 13, "Steel diameter (µm)": 160, "Steel tensile strength (MPa)": 2500, "Steel elastic modulus (GPa)": 200,
            "Total fiber (vol%)": 2.0, "Curing method": cur, "Curing time (days)": 28, "Curing temperature (°C)": 30, "Curing RH (%)": 65, "Test age (days)": 28,
            "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": 80.4,
            "Source table/page": "Table 2 (mix), Table 4 (D100 cylinder fc), Table 3, Table 1 (fibres)",
            "Conversions / notes": "SHCC-ST+PE (0.5 vol% steel + 1.5 vol% PE), no sand. kg/m3 / B (cement 1478 + SF 148 = 1626; VERIFY: table lists cement 1478 as printed). fc at 28 d."})

# ---------- 7) Al-mashhadani et al. 2018: FA/GGBS geopolymer mortar with steel or PVA fibres, fc 7 and 28 d
P = {"Article Name": "Mechanical and microstructural characterization of fiber reinforced fly ash based geopolymer composites",
     "Author": "Mukhallad M. Al-mashhadani, Orhan Canpolat, Yurdakul Aygormez, Mucteba Uysal, Savas Erdem", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.02.061"}
fc7 = {("ST", 0.4): (61.37, 61.67), ("ST", 0.8): (61.54, 61.97), ("ST", 1.2): (61.89, 62.52),
       ("PVA", 0.4): (61.92, 62.07), ("PVA", 0.8): (62.22, 62.46), ("PVA", 1.2): (62.71, 63.06)}
B = 450 + 60
for (fib, v), vals in fc7.items():
    for age, fc in zip((7, 28), vals):
        d = {"FA (Fly ash)": r4(450 / B), "GGBS": r4(60 / B), "WG / B (Water glass)": r4(175 / B), "NaOH molarity (M)": 12,
             "Sand (type not stated) / B": r4(1237.5 / B), "Binder content (kg/m³)": None, "Total fiber (vol%)": v,
             "Curing method": "heat cured 80 C 24 h, then laboratory conditions", "Curing temperature (°C)": 80, "Heat curing duration (h)": 24,
             "Test age (days)": age, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
             "Source table/page": "Table 3 (mix, g), Table 2 (fibres), Table 4 (fc 7 / 28 d), sect. 3",
             "Conversions / notes": f"{fib} {v} vol%. Mix in g: FA 450, GGBS 60, standard sand 1237.5, NaOH 12 M solution 50, Na2SiO3 solution 175; B = FA + GGBS = 510. "
                                    "Water glass 8.2 % Na2O, 27 % SiO2 (solids 35.2 %). VERIFY: W/B and NaOH / B left empty (NaOH solution mass given, water not separable). "
                                    "Curing time (days) left empty."}
        if fib == "ST":
            d.update({"Steel fiber (vol%)": v, "Steel length (mm)": 6, "Steel diameter (µm)": 170, "Steel tensile strength (MPa)": 2100})
        else:
            d.update({"PVA fiber (vol%)": v, **pva(8, 40, 1620, None)})
        add_row(P, d)

# ---------- 8) Abid et al. 2018: ECC with PVA 0.5-2 %, fc 28 d
P = {"Article Name": "Experimental tests on the underwater abrasion of Engineered Cementitious Composites",
     "Author": "Sallal R. Abid, Ali N. Hilo, Yasir H. Daek", "Year": 2018, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.03.213"}
B = 570 + 684
for v, fc in ((0.5, 47.72), (1.0, 46.53), (1.5, 47.76), (2.0, 48.4)):
    add_row(P, {"OPC / Cement": r4(570 / B), "FA (Fly ash)": r4(684 / B), "W / B": r4(330 / B), "SS / B (Silica sand)": r4(455 / B),
                "HRWR / B": r4(4.9 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": v, "Total fiber (vol%)": v, **pva(6, 39, None, None),
                "Curing method": "water cured 23 C until test", "Curing time (days)": 28, "Curing temperature (°C)": 23, "Test age (days)": 28,
                "Compressive strength (MPa)": fc, "Source table/page": "Table 1 (mix), Table 4 (fc 28 d), Table 3 (PVA)",
                "Conversions / notes": f"PVA {v} vol%. kg/m3 / B (cement + FA = 1254). Plain mix (0 % PVA) skipped (no fibre). Splitting tensile strength not entered."})

# ---------- 9) Sherir et al. 2018: 4 ECC mixes, fc 28 / 56 / 90 d
P = {"Article Name": "Fresh state, mechanical & durability properties of strain hardening cementitious composite produced with locally available aggregates and high volume of fly ash",
     "Author": "Mohamed A.A. Sherir, Khandaker M.A. Hossain, Mohamed Lachemi", "Year": 2018, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.08.204"}
mixes = [("F_1.2_SS", 331, 570, 684, 455, "SS", 5.4, (60, 63, 64)), ("F_2.2_SS", 327, 386, 847, 448, "SS", 4.15, (52, 55, 56)),
         ("F_1.2_MS", 327, 559, 671, 446, "MS", 5.4, (64, 66, 67)), ("F_2.2_MS", 319, 376, 825, 436, "MS", 4.15, (48, 50, 51))]
for nm, w, c, fa, s, st, hr, fcs in mixes:
    B = c + fa
    for age, fc in zip((28, 56, 90), fcs):
        d = {"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B,
             "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, **pva(8, 39, 1620, 42.8),
             "Curing method": "sealed plastic bags, 23 C, RH 50 % until test", "Curing time (days)": age, "Curing temperature (°C)": 23, "Curing RH (%)": 50,
             "Test age (days)": age, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
             "Source table/page": "Table 2 (mix), Table 5 (fc), sect. 2.2.3 (curing)",
             "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA = {B}); paper lists w/b 0.27 (computed from kg/m3 here). PVA 26 kg/m3 = 2 vol% (text 2 %). "
                                    + ("Silica sand (<= 0.4 mm)." if st == "SS" else "Locally available mortar sand (<= 1.18 mm), type not stated.")}
        if st == "SS":
            d["SS / B (Silica sand)"] = r4(s / B)
        else:
            d["Sand (type not stated) / B"] = r4(s / B)
            d["Sand max size (µm)"] = 1180
        add_row(P, d)

# ---------- 10) Gao et al. 2018: ECC, 28 d cube fc
P = {"Article Name": "Study on the bonding properties of Engineered Cementitious Composites (ECC) and existing concrete exposed to high temperature",
     "Author": "Shuling Gao, Xiaochong Zhao, Jinli Qiao, Yadong Guo, Guanhua Hu", "Year": 2018, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.11.136"}
B = 583.0 + 699.9
add_row(P, {"OPC / Cement": r4(583.0 / B), "FA (Fly ash)": r4(699.9 / B), "W / B": r4(318.5 / B), "SS / B (Silica sand)": r4(465.7 / B), "SP / B": r4(7.6 / B),
            "Binder content (kg/m³)": r4(B), "PVA fiber (vol%)": 1.7, "Total fiber (vol%)": 1.7, **pva(12, 40, 1620, 42.8),
            "Curing method": "standard curing 28 d (demoulded after 24 h)", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
            "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Compressive strength (MPa)": 39.9,
            "Source table/page": "Table 2 (mix), Table 4 (fc), Table 1 (PVA)",
            "Conversions / notes": "ECC only (concrete with gravel skipped). kg/m3 / B (cement + FA = 1282.9). Specimens of the main bond tests are heated; the unheated 28 d reference fc is used. "
                                   "Curing temperature / RH not stated."})

# ---------- 11) Chen & Yang 2019: SHCC, direct tension + fc 28 d
P = {"Article Name": "Microstructural investigation of steel corrosion in strain hardening cementitious composite (SHCC)",
     "Author": "Zhitao Chen, En-Hua Yang", "Year": 2019, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.03.247"}
add_row(P, {"OPC / Cement": r4(1 / 2.2), "FA (Fly ash)": r4(1.2 / 2.2), "W / B": r4(0.59 / 2.2), "SS / B (Silica sand)": r4(0.8 / 2.2), "Sand max size (µm)": 160,
            "SP / B": r4(0.011 / 2.2), "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, **pva(12, 39, 1600, 41),
            "Curing method": "sealed, lab 23 C 65 % RH 1 d, then sealed container 23 C 85 % RH 27 d", "Curing time (days)": 27, "Curing temperature (°C)": 23,
            "Curing RH (%)": 85, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
            "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Compressive strength (MPa)": 53.6, "First-cracking strength (MPa)": 4.6,
            "Tensile strength (MPa)": 5.0, "Tensile strain capacity (%)": 1.4, "Source table/page": "Table 1 (mix + properties), sect. 2.1-2.2",
            "Conversions / notes": "SHCC row only (mortar without fibre skipped). Ratios to cement 1 : FA 1.2 : S 0.8 : W 0.59 : SP 0.011, divided by B = 2.2. Micro silica sand. Curing from the corrosion-specimen preparation (same mix)."})

# ---------- 12) Fakhri et al. 2019: SHCC fc 34 MPa (text)
P = {"Article Name": "On the use of Strain-Hardening Cementitious Composite covers to mitigate corrosion in reinforced concrete structures",
     "Author": "Hamidreza Fakhri, Ketan A. Ragalwar, Ravi Ranade", "Year": 2019, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.07.052"}
add_row(P, {"OPC / Cement": r4(1 / 2.2), "FA (Fly ash)": r4(1.2 / 2.2), "W / B": r4(0.84 / 2.2), "Sand (type not stated) / B": r4(0.82 / 2.2), "Sand max size (µm)": 300,
            "SP / B": r4(0.010 / 2.2), "VMA / B": r4(0.024 / 2.2), "PVA fiber (vol%)": 1.9, "Total fiber (vol%)": 1.9, **pva(12, 39, 1600, 41),
            "Curing method": "demoulded 24 h, moist (wet paper towels, airtight bags) 14 d, then dried at 20 C to 28 d", "Curing time (days)": 14,
            "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "51",
            "Compressive strength (MPa)": 34, "Source table/page": "Table 1 (mix), Table 3 (PVA), sect. 3.1 (text: fc about 34 MPa)",
            "Conversions / notes": "Ratios relative to cement (1 : FA 1.2 : fine sand 0.82 : water 0.84), divided by B = 2.2. PVA 0.049 by cement mass -> about 1.9 vol% (VERIFY: derived with assumed densities). "
                                   "VERIFY: fc 'about 34 MPa (32-37)' is an approximate text value; tensile strain only as range 2.1-2.7 % (not entered)."})

# ---------- 13) Luo et al. 2019: HS-ECC at room temperature (T-20)
P = {"Article Name": "Temperature impact on the micro-structures and mechanical properties of high-strength engineered cementitious composites",
     "Author": "Jianjun Luo, Ziwei Cai, Kequan Yu, Wenjun Zhu, Zhoudao Lu", "Year": 2019, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.07.322"}
B = 600 + 180 + 150 + 750
add_row(P, {"OPC / Cement": r4(600 / B), "GGBS": r4(750 / B), "SF (Silica fume)": r4(150 / B), "Limestone powder": r4(180 / B), "W / B": r4(250 / B),
            "SS / B (Silica sand)": r4(500 / B), "HRWR / B": r4(15 / B), "Binder content (kg/m³)": B,
            "PE fiber (vol%)": 2.06, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2400, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.06,
            "Curing method": "demoulded 24 h, water pool until 28 d", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
            "Compressive specimen": "cube", "Compressive specimen size (mm)": "40", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
            "Compressive strength (MPa)": 86.0, "First-cracking strength (MPa)": 6.27, "Tensile strength (MPa)": 9.46, "Tensile strain capacity (%)": 9.08,
            "Source table/page": "Table 2 (mix), Table 3 (PE), Table 5 (T-20 tension), sect. 3.1 (fc at room temperature)",
            "Conversions / notes": "Room temperature (T-20) reference only; heated specimens skipped. B = C + LP + SF + GGBS = 1680 (LP included in B; paper's W/(C+SF+GGBS) = 0.150). "
                                   "PE 20 kg/m3 -> 2.06 vol% (VERIFY: derived, density 0.97). Cast: 'T-20' tensile and cube fc both room temperature."})

# ---------- 14) Deshpande et al. 2019: three SHCCs, room temperature fc cylinders
P = {"Article Name": "Temperature effects on the bond behavior between deformed steel reinforcing bars and hybrid fiber-reinforced strain-hardening cementitious composite",
     "Author": "Alok A. Deshpande, Dhanendra Kumar, Ravi Ranade", "Year": 2019, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.117337"}
for nm, c, fa, s, w, hr, vma, pv, st, fc in [("HFR-SHCC", 1, 1.2, 0.8, 0.68, 0.007, 0.020, 2, 1, 31), ("PVA-SHCC", 1, 1.2, 0.8, 0.68, 0.007, 0.018, 2, 0, 53),
                                             ("HFA-SHCC", 1, 2.2, 1.2, 0.99, 0.010, 0.026, 2, 0, 43)]:
    B = c + fa
    d = {"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "Sand (type not stated) / B": r4(s / B), "HRWR / B": r4(hr / B), "VMA / B": r4(vma / B),
         "PVA fiber (vol%)": pv, "Total fiber (vol%)": pv + st, **pva(12, 39, None, None),
         "Curing method": "demoulded 24 h, water cured 14 d, then room storage until test", "Curing time (days)": 14, "Demolding age (days)": 1,
         "Test age (days)": 112, "Compressive specimen": "cylinder", "Compressive strength (MPa)": fc,
         "Source table/page": "Table 1 (mix), Table 3 (fibres), Table 6 (fc), sect. 3.2",
         "Conversions / notes": f"{nm}. Ratios relative to cement, divided by B = {B}. Water given as w/c (w/cm 0.31). VERIFY: test age 16 weeks = 112 d taken from the heating age of the companion specimens "
                                "(room-temperature specimens assumed tested at that age). Splitting strength not entered. Silica sand type not stated."}
    if st:
        d.update({"Steel fiber (vol%)": st, "Steel length (mm)": 25, "Steel diameter (µm)": 500})
    add_row(P, d)

# ---------- 15) Wang et al. 2019: OPC-HSECC control OC
P = {"Article Name": "Zeolite to improve strength-shrinkage performance of high-strength engineered cementitious composite",
     "Author": "Qing Wang, Jun Zhang, J.C.M. Ho", "Year": 2019, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.117335"}
add_row(P, {"OPC / Cement": 0.7, "GGBS": 0.1, "SF (Silica fume)": 0.1, "FA (Fly ash)": 0.1, "W / B": 0.20, "SS / B (Silica sand)": 0.833, "SP / B": 0.0088,
            "Binder content (kg/m³)": r4(787.8 / 0.7), "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, **pva(12, 39, 1620, 42.8),
            "Curing method": "sealed (plastic) curing", "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
            "Compressive strength (MPa)": 104.53, "Source table/page": "Table 3 (mix OC), Table 4 (fc), Table 2 (PVA)",
            "Conversions / notes": "Control OC only (zeolite mixes not allowed; SAC-HSECC skipped). Binder 1 = cement 0.7 : SF 0.1 : slag 0.1 : FA 0.1; binder from cement 787.8 kg/m3. "
                                   "Quartz sand used as sand. SP 0.88 % (of binder, VERIFY). Curing temperature not stated."})

# ---------- 16) Zhang et al. 2022: SH-UHPC, uniaxial tension + static fc
P = {"Article Name": "Effect of fiber content and fiber length on the dynamic compressive properties of strain-hardening ultra-high performance concrete",
     "Author": "Dong Zhang, Huan Tu, Ye Li, Yiwei Weng", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2022.127024"}
for nm, v, L, fc, fcr, ft, eps in [("S-18-1", 1.0, 18, 128.9, 5.67, 7.30, 0.37), ("S-18-1.5", 1.5, 18, 145.2, 7.29, 9.28, 0.75),
                                   ("S-18-2", 2.0, 18, 136.9, 7.63, 12.60, 5.71), ("S-12-2", 2.0, 12, 116.6, 5.88, 7.23, 0.80),
                                   ("S-6-2", 2.0, 6, 106.4, 4.63, 5.01, 0.13)]:
    add_row(P, {"OPC / Cement": r4(1 / 1.11), "SF (Silica fume)": r4(0.11 / 1.11), "W / B": 0.2, "SS / B (Silica sand)": r4(0.44 / 1.11), "Sand max size (µm)": 125,
                "SP / B": r4(0.02 / 1.11), "PE fiber (vol%)": v, "PE length (mm)": L, "PE diameter (µm)": 30, "PE tensile strength (MPa)": 3250, "PE elastic modulus (GPa)": 113,
                "Total fiber (vol%)": v, "Curing method": "covered 1 d, steam curing 90 C RH > 95 % 48 h, then ambient 7 d",
                "Curing time (days)": 9, "Curing temperature (°C)": 90, "Curing RH (%)": 95, "Demolding age (days)": 1, "Heat curing duration (h)": 48,
                "Test age (days)": 10, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
                "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                "Source table/page": "Table 1 (mix), Table 2 (fc, tension), sect. 2.1 (curing)",
                "Conversions / notes": f"{nm}. Mass ratio C 1 : SF 0.11 : sand 0.44 : SP 0.02, divided by B = 1.11 (w/b 0.2 as stated). Silica sand 120-150 mesh (max size about 125 um, VERIFY). "
                                       "VERIFY: test age 10 d = 1 d + 48 h steam + 7 d ambient ('tests right after curing')."})

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
unknown = [c for c in df.columns if c not in cols]
assert not unknown, unknown
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e29.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows", df["DOI / URL"].nunique(), "papers")
