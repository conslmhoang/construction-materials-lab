"""Wave 6, agent e11: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e11.csv (99-column TEMPLATE header).
Papers: conbuildmat.2018.03.172, 2018.06.009, 2018.07.012, 2018.12.207, 2019.03.112, 2019.03.129,
        2019.06.129, 2020.118917, 2020.119824, 2020.122028
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


# ------------------------------------------------ 1) HGM + hybrid fibre ECC, only the HGM-free mixes H0 (172)
P = {"Article Name": "Use of hollow glass microspheres and hybrid fibres to improve the mechanical properties of engineered cementitious composite",
     "Author": "Ali N. Al-Gemeel, Yan Zhuge, Osama Youssf", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.03.172"}
B = 605 + 726
# id, pva vol, steel vol, fc avg (Table 4)
for mid, pv, sv, fc, pk, sk in [("H0-2/0", 2.0, 0, 65.0, 26.0, 0), ("H0-1.75/0.25", 1.75, .25, 60.1, 22.8, 19.5),
                                ("H0-1.5/0.5", 1.5, .5, 55.4, 19.5, 39.0), ("H0-1.25/0.75", 1.25, .75, 61.6, 16.3, 58.5)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(605 / B), "FA (Fly ash)": r4(726 / B), "W / B": r4(338.6 / B), "River sand / B": r4(483 / B),
              "SP / B": r4(3.6 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": pv, "PVA length (mm)": 8, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 66, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 24 h, demoulded, curing pool 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
              "Compressive strength (MPa)": fc, "Source table/page": "Table 1 (mix), Table 2 (fibres), Table 4 (fc), sect. 2.3",
              "Conversions / notes": f"{mid}. kg/m3 / B (cement + FA = 1331). Mixes with HGM (H10-*, MH10-*) skipped. "
                                     f"PVA {pk} kg/m3 / 1300 and steel {sk} kg/m3 / 7800 (paper SG) give the vol% in the mix name. "
                                     "fc = mean of 3 cylinders. No direct tension test in paper (flexure only); axial strain in Table 4 is compressive, not entered. "
                                     "VERIFY: curing pool temperature not stated."})
    if sv:
        r.update({"Steel fiber (vol%)": sv, "Steel length (mm)": 12, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2600,
                  "Steel elastic modulus (GPa)": 200})
    rows.append(r)

# ------------------------------------------------ 2) SHCC with Class C fly ash, ambient reference (06.009)
P = {"Article Name": "Residual mechanical properties and spalling resistance of strain-hardening cementitious composite with Class C fly ash",
     "Author": "Jin-Cheng Liu, Kang Hai Tan, Shengxin Fan", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.06.009"}
B = 289 + 866
r = dict(P)
r.update({"OPC / Cement": r4(289 / B), "FA (Fly ash)": r4(866 / B), "W / B": r4(369 / B), "SS / B (Silica sand)": r4(404 / B),
          "SP / B": r4(15.2 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 1.5, "PVA length (mm)": 12, "PVA diameter (µm)": 38,
          "PVA tensile strength (MPa)": 1060, "PVA elastic modulus (GPa)": 42.8, "Steel fiber (vol%)": 0.99, "Steel length (mm)": 13,
          "Steel diameter (µm)": 160, "Steel tensile strength (MPa)": 2000, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2.49,
          "Curing method": "demoulded 1 d, sealed in plastic sheet 7 d, then laboratory air 28 +/- 3 C RH 50-85 % until 28 d",
          "Curing time (days)": 28, "Curing temperature (°C)": 28, "Curing RH (%)": 67, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 100,
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 50.3, "Tensile strength (MPa)": 5.5, "Tensile strain capacity (%)": 0.7,
          "Source table/page": "Table 1 (mix), Table 3 (fibres), text sect. 3 (ambient fc 50.3, ft 5.5, strain 0.7 %)",
          "Conversions / notes": "Ambient (20-28 C, unheated) reference only; elevated-temperature exposures skipped. PVA 19.5 kg/m3 / 1300 = 1.5 vol%, "
                                 "steel 78 kg/m3 / 7850 = 0.99 vol% (densities assumed, not in paper). RH given as 50-85 %, mid value 67 entered. "
                                 "VERIFY: strain 'tensile strain capacity 0.7 %' stated in text for room temperature."})
rows.append(r)

# ------------------------------------------------ 3) one-part engineered geopolymer composites (07.012)
P = {"Article Name": "Tensile behavior and microstructure of hybrid fiber ambient cured one-part engineered geopolymer composites",
     "Author": "Yazan Alrefaei, Jian-Guo Dai", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.07.012"}
# series, id, ggbs, fa, pe, st, sand/b, fcu, sfc, scu, ecu
t3 = [("P:EGC-S", 1, 0, 2.0, 0.0, 0, 63.5, 1.43, 3.30, 3.74), ("P:EGC-S", 1, 0, 1.5, 0.5, 0, 64.2, 1.51, 3.25, 4.01),
      ("P:EGC-S", 1, 0, 1.0, 1.0, 0, 69.0, 2.52, 3.43, 3.46), ("P:EGC-S", 1, 0, 0.5, 1.5, 0, 73.3, 2.57, 3.34, 0.33),
      ("P:EGC-S", 1, 0, 0.0, 2.0, 0, 77.1, 3.55, 4.16, 0.12),
      ("P:EGC-FA/S", .5, .5, 2.0, 0.0, 0, 64.8, 1.87, 3.32, 3.68), ("P:EGC-FA/S", .5, .5, 1.5, 0.5, 0, 63.8, 1.69, 2.27, 3.18),
      ("P:EGC-FA/S", .5, .5, 1.0, 1.0, 0, 68.2, 2.05, 2.61, 1.24), ("P:EGC-FA/S", .5, .5, 0.5, 1.5, 0, 77.0, 2.51, 2.97, 0.38),
      ("P:EGC-FA/S", .5, .5, 0.0, 2.0, 0, 78.0, 3.02, 3.68, 0.15),
      ("M:EGC-S", 1, 0, 1.5, 0.5, 0.3, 76.1, 2.78, 3.76, 2.54), ("M:EGC-FA/S", .5, .5, 1.5, 0.5, 0.3, 73.5, 2.41, 3.01, 0.57)]
for mid, g, fa, pe, st, sd, fc, fcr, ft, eps in t3:
    r = dict(P)
    r.update({"GGBS": g, "FA (Fly ash)": fa or None, "SSM / B (Na2SiO3 anhydrous)": 0.12, "W / B": 0.45,
              "Sand (type not stated) / B": sd or None, "Sand max size (µm)": 212 if sd else None,
              "PE fiber (vol%)": pe or None, "PE length (mm)": 13 if pe else None, "PE diameter (µm)": 17 if pe else None,
              "PE tensile strength (MPa)": 3000 if pe else None, "PE elastic modulus (GPa)": 114 if pe else None,
              "Steel fiber (vol%)": st or None, "Steel length (mm)": 13 if st else None, "Steel diameter (µm)": 180 if st else None,
              "Steel tensile strength (MPa)": 2850 if st else None, "Steel elastic modulus (GPa)": 200 if st else None,
              "Total fiber (vol%)": pe + st, "Curing method": "wet burlap + plastic 24 h, demoulded, water tank 27 d (ambient, no heat)",
              "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, by wt.), Table 2 (fibres), Table 4 (results), sect. 4.2 (curing)",
              "Conversions / notes": f"{mid} PE{pe}/ST{st}. Ratios by weight to binder (B = slag, or 50/50 slag + class F fly ash). Activator = anhydrous sodium "
                                     "metasilicate powder 12 % of B (50.46 % Na2O, 47.24 % SiO2, Ms 0.94). W/B 0.45 (W/GP solids 0.4). "
                                     "fc = composite 50 mm cubes (fcu); tensile strain = ecu (strain at ultimate strength). Mixes tested at 28 d."})
    rows.append(r)

# ------------------------------------------------ 4) ECC with coarse river sand (12.207), strain only (fc only in Fig. 6)
P = {"Article Name": "An economical ultra-high ductile engineered cementitious composite with large amount of coarse river sand",
     "Author": "Xinchun Guan, Yazhao Li, Tianan Liu, Chenchen Zhang, Hui Li, Jinping Ou", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2018.12.207"}
# id, cement, fa, sand, water, sp, sand type, max size, ffirst, fu, eps
t4 = [("CRS-ECC-1", 404, 605, 756, 242, 23, "CRS", 4750, 4.06, 5.21, 4.09), ("CRS-ECC-2", 450, 673, 617, 269, 17, "CRS", 4750, 3.76, 6.05, 9.07),
      ("CRS-ECC-3", 502, 753, 452, 301, 11, "CRS", 4750, 3.24, 6.02, 10.12), ("CRS-ECC-4", 493, 739, 437, 333, 8, "CRS", 4750, 3.14, 5.37, 8.74),
      ("CRS-ECC-5", 484, 726, 435, 363, 6, "CRS", 4750, 2.99, 5.36, 9.43),
      ("FRS-ECC-1", 404, 605, 756, 242, 20, "FRS", 2360, 3.66, 5.29, 4.07), ("FRS-ECC-2", 450, 673, 617, 269, 15, "FRS", 2360, 3.58, 6.03, 7.45),
      ("FRS-ECC-3", 502, 753, 452, 301, 10, "FRS", 2360, 3.33, 6.76, 9.44), ("FRS-ECC-4", 493, 739, 437, 333, 8, "FRS", 2360, 3.13, 6.12, 10.39),
      ("FRS-ECC-5", 484, 726, 435, 363, 6, "FRS", 2360, 2.89, 4.57, 9.54),
      ("USS-ECC-1", 404, 605, 756, 242, 20, "USS", 212, 3.62, 7.04, 6.47), ("USS-ECC-2", 450, 673, 617, 269, 15, "USS", 212, 3.34, 7.49, 9.95),
      ("USS-ECC-3", 502, 753, 452, 301, 10, "USS", 212, 3.28, 8.03, 10.75), ("USS-ECC-4", 493, 739, 437, 333, 8, "USS", 212, 3.02, 6.43, 9.21),
      ("USS-ECC-5", 484, 726, 435, 363, 6, "USS", 212, 3.01, 6.01, 8.12)]
for mid, c, fa, sa, w, sp, st, mx, fcr, fu, eps in t4:
    B = c + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SP / B": r4(sp / B), "Binder content (kg/m³)": B,
              "Sand max size (µm)": mx, "PE fiber (vol%)": 1.96, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 1.96,
              "Curing method": "demoulded 1 d, sealed container 98 % RH 75 C 2 d, then room temperature 7 d", "Curing time (days)": 9,
              "Curing temperature (°C)": 75, "Curing RH (%)": 98, "Demolding age (days)": 1, "Test age (days)": 10, "Heat curing duration (h)": 48,
              "Tensile specimen": "dog-bone 13x30 mm section", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, kg/m3), Table 2 (fibre), Table 6 (tensile), sect. 2.2 (curing)",
              "Conversions / notes": f"{mid}. kg/m3 / B (cement + FA). PE 19 kg/m3 / 970 = 1.96 vol%. Strain = ultimate tensile strain (strain at peak stress). "
                                     "fc only in Fig. 6, not entered. VERIFY: test age 10 d derived (1 d mould + 2 d 75 C + 7 d room); heat curing 48 h."})
    if st == "USS":
        r["SS / B (Silica sand)"] = r4(sa / B)
        r["Conversions / notes"] += " USS = ultrafine silica sand (max 212 um)."
    else:
        r["River sand / B"] = r4(sa / B)
        r["Conversions / notes"] += f" {st} = river sand sieved at {mx} um."
    rows.append(r)

# ------------------------------------------------ 5) TiO2-doped ECC, control C-ECC only (2019.03.112)
P = {"Article Name": "Multiscale investigation of tensile properties of a TiO2-doped Engineered Cementitious Composite",
     "Author": "Mingfeng Xu, Yi Bao, Kai Wu, Huisheng Shi, Xiaolu Guo, Victor C. Li", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.03.112"}
B = 3.2
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(2.2 / B), "W / B": 0.25, "SS / B (Silica sand)": 0.36, "SP / B": 0.006,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8,
          "Total fiber (vol%)": 2, "Curing method": "covered 24 h, demoulded, air curing 20 C RH 55 % until 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 55, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 52.6, "First-cracking strength (MPa)": 4.10, "Tensile strength (MPa)": 6.81, "Tensile strain capacity (%)": 3.95,
          "Source table/page": "Table 3 (mix, fc), Table 4 (tensile 28 d), sect. 2.2 (curing)",
          "Conversions / notes": "C-ECC control (no TiO2); TiO2-nano mixes skipped. Ratios by mass to cement (C = 1, FA 2.2, B = 3.2). "
                                 "Sand = finely ground quartz sand F75 (a sand, max grain small). VERIFY: SP 0.006 assumed to be per B (paper table column 'SP')."})
rows.append(r)

# ------------------------------------------------ 6) fly ash fineness / calcium content ECC (2019.03.129)
P = {"Article Name": "Effect of fineness and calcium content of fly ash on the mechanical properties of Engineered Cementitious Composites (ECC)",
     "Author": "Li-li Kan, Ruo-xin Shi, Jin Zhu", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.03.129"}
B = 346.33 + 808.10
base = {"OPC / Cement": r4(346.33 / B), "FA (Fly ash)": r4(808.10 / B), "W / B": r4(346.33 / B), "Sand (type not stated) / B": r4(346.33 / B),
        "HRWR / B": r4(10.17 / B), "VMA / B": r4(1.88 / B), "Binder content (kg/m³)": round(B, 2), "PVA fiber (vol%)": 1.87, "Total fiber (vol%)": 1.87,
        "Curing method": "demoulded 24 h, standard curing box 20 C RH 95 %", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
        "Demolding age (days)": 1, "Tensile specimen": "dog-bone (JSCE)"}
tens = {("A", 7): (2.39, 4.26), ("A", 28): (2.32, 3.12), ("B", 7): (2.44, 4.94), ("B", 28): (2.28, 4.35), ("C", 7): (2.20, 4.16),
        ("C", 28): (2.23, 3.53),
        ("FA-2", 7): (3.73, 3.84), ("FA-2", 28): (3.91, 2.35), ("FA-2", 150): (4.28, 2.04),
        ("FA-3", 7): (3.30, 4.31), ("FA-3", 28): (5.15, 3.81), ("FA-3", 150): (5.22, 3.72),
        ("FA-4", 7): (3.27, 3.03), ("FA-4", 28): (3.51, 2.49), ("FA-4", 150): (3.69, 2.18)}
fcs = {"A": 45.4, "B": 35.8, "C": 32.0}
for (g, age), (ft, eps) in tens.items():
    r = dict(P)
    r.update(base)
    r.update({"Curing time (days)": age, "Test age (days)": age, "Tensile test type": DIRECT, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 4 (FA-1 groups tensile), Table 5 (fc 28 d), Table 8 (FA-2..4 tensile), sect. 2.1 (curing)",
              "Conversions / notes": ("FA-1 ground to fineness group %s (mean diameter 9.7/7.5/5.8 um for A/B/C). " % g if len(g) == 1 else
                                      f"{g}: fly ash with different CaO content (FA-4 highest CaO, 16.4 %). ") +
                                     "kg/m3 / B (cement + FA = 1154.43). Ultimate tensile stress and tensile strain capacity (Tables 4, 8). "
                                     "PVA 24.29 kg/m3 / 1300 = 1.87 vol% (PVA density and dimensions not given in paper, 1300 assumed). "
                                     "Sand type not stated. Methyl cellulose thickener 1.88 kg/m3 entered as VMA. "
                                     "VERIFY: time zero for curing age (7/28/150 d) taken from casting."})
    if len(g) == 1 and age == 28:
        r["Compressive strength (MPa)"] = fcs[g]
        r["Compressive specimen"] = "cube"
        r["Compressive specimen size (mm)"] = "50"
    rows.append(r)

# ------------------------------------------------ 7) SHCC at different curing ages (2019.06.129)
P = {"Article Name": "Tensile characteristics of strain-hardening cement-based composites with different curing ages",
     "Author": "Ji-hong Hu, Ming-qing Sun, Jun Li, Yun-pang Wei, Jian-zhong Chen", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2019.06.129"}
B = 390.1 + 780.2
for age, fu, eps, fcr in [(3, 4.06, 4.30, 2.32), (7, 4.80, 4.52, 3.26), (28, 5.82, 3.61, 3.57)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(390.1 / B), "FA (Fly ash)": r4(780.2 / B), "W / B": r4(362.8 / B), "Sand (type not stated) / B": r4(526.6 / B),
              "SP / B": r4(4.1 / B), "VMA / B": r4(0.3 / B), "Binder content (kg/m³)": round(B, 1), "Sand max size (µm)": 300,
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded 1 d, then 20 C RH 95 %", "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
              "Demolding age (days)": 1, "Test age (days)": age, "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 65,
              "Tensile test type": DIRECT, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 2 (tensile), Table 3 (first cracking), sect. 2.2/2.1",
              "Conversions / notes": f"{age}d-SHCC. kg/m3 / B (cement + FA). PVA 2.0 vol% (26 kg/m3) stated. Water reducer WR entered as SP. "
                                     "VERIFY: test age = curing age (3/7/28 d) taken as age from casting; paper says 'demoulded after 1 day, then cured for 3d, 7d, 28d'. "
                                     "Ultimate tensile strength and strain eps_tu."})
    rows.append(r)

# ------------------------------------------------ 8) PE fibre ECC (2020.118917), tension only
P = {"Article Name": "Effect of polyethylene fiber content on physical and mechanical properties of engineered cementitious composites",
     "Author": "Yichao Wang, Feichi Liu, Jiangtao Yu, Fangyuan Dong, Junhong Ye", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.118917"}
B = 936.7 + 401.4
for mid, pe, fkg, fcr, eps, fu in [("PE-0.75%", 0.75, 7.5, 4.06, 1.59, 4.54), ("PE-1%", 1.0, 10, 4.51, 3.04, 6.33),
                                   ("PE-1.5%", 1.5, 15, 3.57, 9.38, 8.19), ("PE-2%", 2.0, 20, 3.00, 11.99, 7.28), ("ST-2%", 0, 157, 5.40, 0.37, 7.54)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(936.7 / B), "FA (Fly ash)": r4(401.4 / B), "W / B": r4(335.1 / B), "Sand (type not stated) / B": r4(401.4 / B),
              "HRWR / B": r4(4.2 / B), "VMA / B": r4(1.0 / B), "Binder content (kg/m³)": round(B, 1),
              "Curing method": "air curing 28 d", "Curing time (days)": 28, "Test age (days)": 28, "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 3 (fibres), Table 4 (tensile), sect. 2.1 (curing)",
              "Conversions / notes": f"{mid}. kg/m3 / B (cement + FA). Fiber kg/m3 in Table 1 note ({fkg}). fc values only in Fig. 10/15 (only % changes in text), not entered. "
                                     "Strain = eps_tu (ultimate tensile strain)."})
    if pe:
        r.update({"PE fiber (vol%)": pe, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
                  "Total fiber (vol%)": pe})
        r["Conversions / notes"] += f" PE {fkg} kg/m3 / 970 = {fkg / 970 * 100:.2f} vol% (mix names give nominal vol%)."
    else:
        r.update({"Steel fiber (vol%)": 2.0, "Steel length (mm)": 8, "Steel diameter (µm)": 130, "Steel tensile strength (MPa)": 2850,
                  "Steel elastic modulus (GPa)": 210, "Total fiber (vol%)": 2.0})
        r["Conversions / notes"] += " Steel 157 kg/m3 / 7850 = 2.0 vol% (Table 3 density '78' is a typo for 7.8 g/cm3)."
    rows.append(r)

# ------------------------------------------------ 9) PVA fibre length in HDCC (2020.119824)
P = {"Article Name": "An optimum polyvinyl alcohol fiber length for reinforced high ductility cementitious composites based on theoretical and experimental analyses",
     "Author": "Cong Ding, Liping Guo, Bo Chen", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.119824"}
for L, fcr, fu, eps in [(6, 3.6, 4.7, 1.2), (9, 3.7, 4.9, 2.5), (12, 3.5, 4.9, 2.3), (18, 3.3, 3.7, 1.0), (24, 3.0, 3.5, 0.7)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.8, "W / B": 0.3, "River sand / B": 0.3, "Sand max size (µm)": 600,
              "PVA fiber (vol%)": 2, "PVA length (mm)": L, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1260, "PVA elastic modulus (GPa)": 30,
              "Total fiber (vol%)": 2, "Curing method": "demoulded 1 d, water curing at 60 C for 3 d", "Curing time (days)": 3,
              "Curing temperature (°C)": 60, "Demolding age (days)": 1, "Test age (days)": 4, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "40", "Tensile specimen": "dumbbell (JSCE) 30x13 mm section", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": 35.0, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "sect. 3.1 (mix ratio 0.2:0.8:0.3:0.3, curing), Table 2 (fibre), Table 5 (tensile), sect. 4 text (fc ~35 MPa)",
              "Conversions / notes": f"L{L}. Mass ratio cement:FA:sand:water = 0.2:0.8:0.3:0.3 (B = 1). HPWR dose not stated (polycarboxylate used). "
                                     "PVA tensile strength 1260 MPa and E 30 GPa as tested in paper (Table 2). Fibers oil coated 1.2 wt%. "
                                     "VERIFY: test age 4 d derived (1 d + 3 d at 60 C), fc 'about 35.0 MPa' for all lengths (stated approximate in text)."})
    rows.append(r)

# ------------------------------------------------ 10) SHCC with slag and calcium carbonate powder (2020.122028)
P = {"Article Name": "Development of strain-hardening cementitious composites utilizing slag and calcium carbonate powder",
     "Author": "Dhanendra Kumar, Ravi Ranade", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.122028"}
t25 = {  # id: (slag, CC, water, hrwra, pva, fc, eps)
    1: (2.00, 2.20, 1.50, .006, .088, 52.8, 2.08), 2: (2.00, 2.68, 1.50, .008, .093, 50.8, 1.93), 3: (3.00, 2.95, 2.00, .008, .118, 51.2, 1.93),
    4: (3.00, 3.60, 2.00, .012, .124, 48.8, 1.70), 5: (2.50, 2.85, 1.75, .009, .106, 48.2, 1.71), 6: (2.50, 2.85, 1.75, .009, .106, 48.8, 1.83),
    7: (2.50, 2.85, 1.75, .009, .106, 52.0, 1.37), 8: (2.50, 2.85, 1.75, .009, .106, 44.6, 1.95), 9: (2.50, 3.28, 1.75, .011, .110, 55.4, 1.82),
    10: (3.20, 3.43, 2.11, .011, .127, 47.9, 1.97), 11: (1.80, 2.26, 1.40, .007, .084, 53.3, 2.46), 12: (2.50, 2.47, 1.75, .007, .102, 48.4, 2.04),
    13: (2.50, 2.10, 1.75, .006, .098, 47.3, 1.40), 14: (2.50, 3.84, 1.75, .013, .115, 60.9, 1.30), 15: (1.50, 2.02, 1.25, .005, .075, 55.8, 1.41),
    16: (3.50, 3.67, 2.25, .011, .136, 47.7, 0.92)}
t15 = {
    1: (2.00, 2.20, 1.65, .003, .092, 45.7, 2.74), 2: (2.00, 2.69, 1.65, .006, .097, 50.6, 2.72), 3: (3.00, 2.95, 2.20, .005, .123, 43.3, 2.79),
    4: (3.00, 3.60, 2.20, .008, .129, 44.2, 1.71), 5: (2.50, 2.85, 1.93, .008, .110, 44.8, 1.96), 6: (2.50, 2.85, 1.93, .008, .110, 44.9, 2.94),
    7: (2.50, 2.85, 1.93, .008, .110, 47.7, 2.08), 8: (2.50, 2.85, 1.93, .008, .110, 46.4, 1.84), 9: (2.50, 3.28, 1.93, .010, .114, 48.0, 1.81),
    10: (3.20, 3.43, 2.32, .009, .133, 42.4, 1.92), 11: (1.80, 2.26, 1.53, .004, .088, 44.5, 2.83), 12: (2.50, 2.47, 1.93, .006, .106, 40.3, 2.37),
    13: (2.50, 2.10, 1.93, .007, .103, 43.4, 1.65), 14: (2.50, 3.84, 1.93, .014, .120, 51.5, 1.18), 15: (1.50, 2.02, 1.38, .004, .078, 49.4, 1.67),
    16: (3.50, 3.67, 2.48, .010, .142, 41.9, 0.93)}
common = {"PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8,
          "Total fiber (vol%)": 2, "Curing method": "demoulded 24 h, moist curing 21 d, then air 20 C RH 50 +/- 20 % 21 d", "Curing time (days)": 42,
          "Curing temperature (°C)": 20, "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": 43, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "51", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT}
for grp, tab, tname, mm, wcm in (("M25", t25, "Table 4 (mix), Table 7 (results)", "CC-25 (mean size 25 um)", 0.50),
                                 ("M15", t15, "Table 5 (mix), Table 8 (results)", "CC-15 (mean size 15 um)", 0.55)):
    for k, (sl, cc, w, hr, pv, fc, eps) in tab.items():
        B = 1 + sl + cc
        r = dict(P)
        r.update(common)
        r.update({"OPC / Cement": r4(1 / B), "GGBS": r4(sl / B), "Limestone powder": r4(cc / B), "W / B": r4(w / B), "HRWR / B": r4(hr / B),
                  "Compressive strength (MPa)": fc, "Tensile strain capacity (%)": eps,
                  "Source table/page": tname + ", sect. 2.3/2.4 (curing, age 43 d)",
                  "Conversions / notes": f"{grp}-{k}. Ratios to cement by weight; B re-expressed as cement + slag + calcium carbonate powder ({mm}, entered as limestone powder); "
                                         f"paper w/cm = {wcm} on cement + slag, here W/B on total powder. Only compressive strength and tensile strain capacity reported "
                                         "(table means). Tensile strain = tensile strain capacity from dog-bone uniaxial tension. Age 43 d = 1 + 21 + 21 d (28 d + 15 d stated)."})
        rows.append(r)
# conventional fly ash SHCC references (Table 6): strain only, from text
for mid, fa, w, pv, hr, vma, eps, note in (("FA-SHCC", 1.2, 0.68, .049, .010, .018, 1.8, "text sect. 3.4: 'FA-SHCC (1.8 %)'"),
                                           ("HFA-SHCC", 2.2, 1.06, .072, .025, .064, 3.2, "text sect. 3.4: 'HFA-SHCC ... 3.2 %'")):
    B = 1 + fa
    r = dict(P)
    r.update(common)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(0.8 / B), "HRWR / B": r4(hr / B),
              "VMA / B": r4(vma / B), "Tensile strain capacity (%)": eps, "Compressive strength (MPa)": None,
              "Source table/page": "Table 6 (mix), " + note,
              "Conversions / notes": f"{mid}. Ratios to cement, B = cement + FA. F75 silica sand 0.8. fc only in Fig. 10, not entered. "
                                     "VERIFY: strain taken from running text; same 43 d regime assumed for these reference mixes."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e11.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e11.csv"))
