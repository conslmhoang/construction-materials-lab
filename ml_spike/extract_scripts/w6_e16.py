"""Wave 6, agent e16: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e16.csv (99-column TEMPLATE header).
Papers: conbuildmat.2017.05.051, 2017.06.057, 2017.10.077, 2020.118211, 2020.119048, 2020.119412,
        2020.121959, 2021.122834, 2021.122863
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


# ------------------------------------------------ 1) SHCC with REC (PVA) fibres, fly ash content
P = {"Article Name": "Development of self-compacting strain-hardening cementitious composites by varying fly ash content",
     "Author": "Chang Lin, Obada Kayali, Evgeny V. Morozov, David J. Sharp", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.05.051"}
# id, FA/C, W/B, SP per cement, fc, fcr, ftu, strain (%)
for mid, fa, wb, sp, fc, fcr, ft, eps in [("P0_REC", 0, 0.24, 0.0062, 92.5, 6.66, 6.66, 0.0209),
                                          ("P1_REC", 1, 0.20, 0.017, 81.4, 4.05, 6.17, 2.1063),
                                          ("P2_REC", 2, 0.24, 0.015, 52.3, 3.93, 4.00, 1.2650),
                                          ("P4_REC", 4, 0.24, 0.020, 35.1, 3.02, 3.49, 1.7843)]:
    B = 1 + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fa / B) if fa else None, "W / B": wb, "SP / B": r4(sp / B),
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 24 h, demoulded, fog room 23 C until 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200", "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix, mass ratios), Table 3 (w/cm, SP), Table 7 (fc), Table 8 (tension)",
              "Conversions / notes": f"{mid}. Mass ratios to cement; B = cement + FA (FA/C {fa}); W/B = paper w/cm; SP given by mass of cement, divided by B. "
                                     "No sand. PVA fibre 'REC' 2 vol%. Tensile strain = eps_tu at ultimate strength (Table 8, %). "
                                     "P0_REC is strain-softening (0.0209 %). P0_SS (steel fibre) has no table values, skipped."})
    rows.append(r)

# ------------------------------------------------ 2) CaCO3 whisker ECC: only control D4-0
P = {"Article Name": "CaCO3 whisker modified Engineered Cementitious Composite with local ingredients",
     "Author": "Hui Ma, Jingming Cai, Zhan Lin, Shunzhi Qian, Victor C. Li", "Year": 2017,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.06.057"}
B = 5.0
r = dict(P)
r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.8, "W / B": r4(1.5 / B), "SS / B (Silica sand)": r4(1.8 / B), "HRWR / B": r4(0.02 / B),
          "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 35, "PVA tensile strength (MPa)": 1287,
          "PVA elastic modulus (GPa)": 31.3, "Total fiber (vol%)": 2.0,
          "Curing method": "demoulded 24 h, sealed, 90 +/- 5 % RH, 20 +/- 2 C until 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile specimen": "dog-bone",
          "Tensile test type": DIRECT, "First-cracking strength (MPa)": 1.64, "Tensile strength (MPa)": 2.15,
          "Tensile strain capacity (%)": 2.95, "Source table/page": "Table 4 (mix), Table 3 (fibre), Table 5 (tension)",
          "Conversions / notes": "D4-0 control (no CaCO3 whisker; whisker mixes skipped, not an allowed material). Mass ratios to cement 1 : FA 4.0 : sand 1.8 : "
                                 "water 1.5 : HRWRA 0.02, divided by B = 5. fc only in Fig. 4 (text: 0.5 % whisker mix 30 MPa = +30 % vs D4-0), not entered. "
                                 "Sand described as silica sand."})
rows.append(r)

# ------------------------------------------------ 3) ECC / hybrid ECC at 20 C reference
P = {"Article Name": "Behaviour of engineered cementitious composites and hybrid engineered cementitious composites at high temperatures",
     "Author": "S. Pourfalah, et al.", "Year": 2017, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2017.10.077"}
# id, water, cement, fa, sand, pva kg, steel kg, hrwr, steel len, fc20, first crack, max stress, max strain (%)
for mid, w, c, fa, sa, pv, st, hr, sl, fc, fcr, ft, eps in [
        ("ECC", 356, 454, 817, 273, 26.0, 0, 4.5, 0, 38.8, 2.75, 3.85, 3.5),
        ("H6ECC", 354, 451, 817, 273, 22.75, 58.86, 4.5, 6, 40.1, 2.89, 4.36, 3.0),
        ("H13ECC", 354, 451, 817, 273, 22.75, 58.86, 4.5, 13, 45.0, 3.32, 4.71, 2.5)]:
    B = c + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(sa / B),
              "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": r4(pv / 1300 * 100), "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 14, "Total fiber (vol%)": r4(pv / 1300 * 100 + st / 7800 * 100),
              "Curing method": "tension: covered 24 h, water 20 +/- 3 C to 28 d; compression: water 21 d then lab air 7 d (20 C, 60 % RH)",
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 3 (fibres), Table 4 (tension), Table 5 (compression, 20 C)",
              "Conversions / notes": f"{mid}. Unheated (20 C) reference only; high-temperature results skipped. kg/m3 / B (cement + FA). "
                                     "Silica sand 120 um mean size. Fibre vol% = kg/m3 / density (PVA 1300, steel 7800; paper gives 1.75 % PVA + 0.75 % steel for the hybrids; "
                                     "ECC PVA 26 kg/m3 = 2.0 %). Strain = max strain at peak stress (Table 4, decimal x 100). "
                                     + (f"Steel fibre {sl} mm x 0.15 mm, 3000 MPa, 210 GPa. " if st else "No steel fibre. ")
                                     + "VERIFY: fc specimens cured 21 d water + 7 d air, tension specimens 28 d water."})
    if st:
        r.update({"Steel fiber (vol%)": r4(st / 7800 * 100), "Steel length (mm)": sl, "Steel diameter (µm)": 150,
                  "Steel tensile strength (MPa)": 3000, "Steel elastic modulus (GPa)": 210})
    rows.append(r)

# ------------------------------------------------ 4) oiled / unoiled PVA ECC (Group 4)
P = {"Article Name": "Greener engineered cementitious composite (ECC) - The use of pozzolanic fillers and unoiled PVA fibers",
     "Author": "Qing Wang, M.H. Lai, J. Zhang, Zhenbo Wang, J.C.M. Ho", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.118211"}
t11 = {("O-PVA", 7): (37.01, 2.327, 3.702, 2.550), ("O-PVA", 28): (44.58, 2.489, 3.873, 2.013),
       ("U-PVA", 7): (36.50, 2.082, 3.552, 1.383), ("U-PVA", 28): (43.87, 2.104, 3.598, 1.075)}
for (mid, age), (fc, fcr, ft, eps) in t11.items():
    pv = {"O-PVA": (39, 1620, 42.8), "U-PVA": (26, 1560, 36.3)}[mid]
    sp = {"O-PVA": 0.57, "U-PVA": 0.65}[mid]
    r = dict(P)
    r.update({"OPC / Cement": 0.70, "SF (Silica fume)": 0.10, "GGBS": 0.10, "FA (Fly ash)": 0.10, "W / B": 0.35,
              "SP / B": r4(sp / 100),
              "PVA fiber (vol%)": 1.5, "PVA length (mm)": 12, "PVA diameter (µm)": pv[0], "PVA tensile strength (MPa)": pv[1],
              "PVA elastic modulus (GPa)": pv[2], "Total fiber (vol%)": 1.5,
              "Curing method": "covered 24 h, demoulded, curing chamber 20 +/- 2 C, 95 % RH", "Curing time (days)": age,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": age,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "rectangular coupon 100x200x20",
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 6 (mix), Table 2 (fibre), Table 10 (fc), Table 11 (tension)",
              "Conversions / notes": f"{mid} Group 4 ECC, binder = cement 0.70 + SF 0.10 + GGBFS 0.10 + FA 0.10 (by weight of binder), W/B 0.35. "
                                     "VERIFY: SP '(%)' column (0.57 / 0.65) taken as % by mass of binder. VERIFY: quartz sand dosage given only as 'volumetric ratio "
                                     "sand to mortar 0.833', mass ratio unknown, so sand left empty. Strain epsilon_t in % (Table 11)."})
    rows.append(r)

# ------------------------------------------------ 5) ECC overlay material (airfield pavement)
P = {"Article Name": "Paving an engineered cementitious composite (ECC) overlay on concrete airfield pavement for reflective cracking resistance",
     "Author": "Hui Ma, Zhigang Zhang", "Year": 2020, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.119048"}
B = 395 + 869
r = dict(P)
r.update({"OPC / Cement": r4(395 / B), "FA (Fly ash)": r4(869 / B), "W / B": r4(313 / B), "SS / B (Silica sand)": r4(549 / B),
          "SP / B": r4(5.1 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
          "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
          "Curing method": "plastic sheet 24 h, demoulded, laboratory air 20 +/- 3 C, 50 +/- 5 % RH to 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile specimen": "dog-bone",
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 46.6, "Tensile strain capacity (%)": 2.5,
          "Source table/page": "Table 1 (mix), sect. 3.1 (fibre, curing), sect. 4.1 (fc 46.6, strain 2.5 %)",
          "Conversions / notes": "ECC mix only (C40 concrete skipped). kg/m3 / B (cement + FA = 1264). PVA 26 kg/m3 stated as 2 vol%. "
                                 "Silica sand mean size 110 um. Test age 28 d taken from the 28-d curing statement. "
                                 "VERIFY: tensile strain 2.5 % stated in text; the stress-strain curve itself is a figure."})
rows.append(r)

# ------------------------------------------------ 6) slag in lieu of fly ash ECC (Table 3 strain), PVA 2 vol%
P = {"Article Name": "The influence of utilizing slag in lieu of fly ash on the performance of engineered cementitious composites",
     "Author": "Emad Booya, Karla Gorospe, Sreekanta Das, Philip Loh", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.119412"}
mixes = {"ECC1.2-0SG": (600, 700, 0, 446, 327), "ECC1.2-30SG": (600, 490, 210, 446, 327), "ECC1.2-70SG": (600, 210, 490, 446, 327),
         "ECC1.2-100SG": (600, 0, 700, 446, 327), "ECC2.2-0SG": (380, 836, 0, 437, 316), "ECC2.2-100SG": (420, 0, 924, 483, 350)}
t3 = {"ECC1.2-0SG": {28: (3.5, 2.4), 90: (3.7, 3.1)}, "ECC1.2-30SG": {28: (3.7, 2.9), 90: (4.4, 2.8)},
      "ECC1.2-70SG": {28: (4.1, 1.9), 90: (4.3, 2.0)}, "ECC1.2-100SG": {28: (4.3, 2.5), 90: (4.4, 2.5)},
      "ECC2.2-0SG": {28: (4.2, 2.6), 90: (4.5, 4.2)}, "ECC2.2-100SG": {28: (4.3, 1.8), 90: (4.6, 2.9)}}
for mid, (c, fa, sg, sa, w) in mixes.items():
    B = c + fa + sg
    for age, (ft, eps) in t3[mid].items():
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B) if fa else None, "GGBS": r4(sg / B) if sg else None,
                  "W / B": r4(w / B), "Sand (type not stated) / B": r4(sa / B), "Sand max size (µm)": 600,
                  "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39,
                  "PVA tensile strength (MPa)": 1600, "Total fiber (vol%)": 2.0,
                  "Curing method": "water curing (chamber) until test, air dried 2 d before testing", "Curing time (days)": age,
                  "Test age (days)": age, "Tensile specimen": "prism 50x50x431 mm",
                  "Tensile gauge length (mm)": 100, "Tensile test type": DIRECT, "Tensile strength (MPa)": ft,
                  "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 1 (mix kg/m3), Table 3 (tension), sect. 2.1-2.3",
                  "Conversions / notes": f"{mid}. kg/m3 / B (cement + FA + slag = {B}). PVA 26 kg/m3 / 1300 = 2.0 vol% (VERIFY: vol% not stated). "
                                         "Binder is general-use limestone cement (CSA GUL), entered as cement. Lake sand LS-50 max 600 um (type not stated as silica). "
                                         "HRWRA used but dosage not given. fc only in Fig. 2 (not entered). Strain = tensile strain at rupture (%). "
                                         "VERIFY: water curing temperature not stated; specimens water cured to test age minus 2 d air drying."})
        rows.append(r)

# ------------------------------------------------ 7) AAS + crumb rubber + PE fibre
P = {"Article Name": "Effects of crumb rubber particles on mechanical properties and sustainability of ultra-high-ductile slag-based composites",
     "Author": "Quang-Hieu Luong, Huy Hoang Nguyen, Jeong-Il Choi, Hyeong-Ki Kim, Bang Yeon Lee", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2020.121959"}
# id, ggbs, sf, cr, water, hrwra, fcr, ft, eps, fc
for mid, g, sf, cr, w, hr, fcr, ft, eps, fc in [("S-0", 0.90, None, None, 0.18, 0.027, 4.88, 11.26, 7.87, None),
                                                 ("S-CR5", 0.90, None, 0.05, 0.18, 0.036, 3.64, 9.48, 10.67, None),
                                                 ("S-CR10", 0.90, None, 0.10, 0.18, 0.050, 2.73, 5.43, 9.21, 30.5),
                                                 ("S-CR5-SF5", 0.85, 0.05, 0.05, 0.18, 0.029, 4.33, 10.58, 10.02, None)]:
    r = dict(P)
    r.update({"GGBS": g, "SF (Silica fume)": sf, "Ca(OH)2 / B": 0.10, "W / B": w, "Crumb rubber / B": cr, "HRWR / B": hr,
              "PE fiber (vol%)": 1.75, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700,
              "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1.75,
              "Curing method": "demoulded 2 d, pure water 23 +/- 3 C to 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23,
              "Demolding age (days)": 2, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 3 (PE), Table 4 (tension), sect. 3.2 (fc of S-CR10)",
              "Conversions / notes": f"{mid}. Weight ratios to total binder B (GGBS + SF + Ca(OH)2 = 1); Ca(OH)2 10 wt% of B as activator. Crumb rubber 400 um "
                                     "(by wt of binder, added as extra); defoamer 0.001 also used. No sand. Strain eps_c (%) at tensile strength. "
                                     "fc only entered where the text gives it (S-CR10); other fc are in Fig. 5 only."})
    rows.append(r)

# ------------------------------------------------ 8) ECC curing RH (Table 4 strain, 7/28/60 d)
P = {"Article Name": "Effect of curing relative humidity on mechanical properties of engineered cementitious composites at multiple scales",
     "Author": "Mingfeng Xu, Jing Yu, Jian Zhou, Yi Bao, Victor C. Li", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.122834"}
t4 = {1.2: {7: {25: (4.00, 6.22, 3.35), 55: (4.16, 6.97, 2.51), 95: (4.40, 6.98, 2.12)},
            28: {25: (4.07, 5.65, 3.12), 55: (4.16, 6.77, 2.29), 95: (4.40, 6.89, 1.63)},
            60: {25: (4.35, 6.82, 2.46), 55: (4.73, 6.87, 2.16), 95: (4.96, 7.41, 1.63)}},
      2.2: {7: {25: (2.98, 6.27, 4.00), 55: (3.74, 6.60, 3.87), 95: (4.24, 7.00, 2.43)},
            28: {25: (3.96, 6.76, 3.80), 55: (4.05, 6.72, 3.69), 95: (4.71, 7.01, 1.83)},
            60: {25: (4.40, 7.00, 3.63), 55: (4.71, 7.10, 3.23), 95: (5.13, 7.78, 1.94)}}}
for fa, d1 in t4.items():
    B = 1 + fa
    sp_c = {1.2: 0.004, 2.2: 0.006}[fa]
    for age, d2 in d1.items():
        for rh, (fcr, ft, eps) in d2.items():
            r = dict(P)
            r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fa / B), "W / B": 0.25, "SS / B (Silica sand)": 0.36,
                      "SP / B": r4(sp_c / B),
                      "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
                      "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
                      "Curing method": f"covered 24 h, demoulded, curing chamber RH {rh} % until test", "Curing time (days)": age,
                      "Curing RH (%)": rh, "Demolding age (days)": 1, "Test age (days)": age, "Tensile specimen": "dog-bone (JSCE)",
                      "Tensile test type": DIRECT, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
                      "Tensile strain capacity (%)": eps,
                      "Source table/page": "Table 1 (mix), Table 3 (fibre), Table 4 (tension), sect. 2.2 (curing)",
                      "Conversions / notes": f"FA/C = {fa}, RH {rh} %. Paper ratios W/(C+FA) 0.25 and S/(C+FA) 0.36 used directly. "
                                             f"VERIFY: SP column ({sp_c}) assumed per unit cement like the sand column (0.80 / 1.16 = 0.36 x B), so SP/B = SP/(1+FA). "
                                             "Fine siliceous sand 75 um mean. Curing temperature not stated (lab air-conditioned). fc not in tables (not entered)."})
            rows.append(r)

# ------------------------------------------------ 9) steel-fibre UHPC, random fibre cubes (fc at 5 d)
P = {"Article Name": "Influence of fiber alignment and length on flexural properties of UHPC",
     "Author": "Huanghuang Huang, Xiaojian Gao, Kamal H. Khayat, Anshuang Su", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.122863"}
B = 920 + 276
for mid, ln, w, sp, fc in [("SS", 6, 226.3, 21.5, 142.1), ("MS", 13, 224.9, 23.9, 149.8), ("LS", 20, 223.3, 26.3, 140.8)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(920 / B), "SF (Silica fume)": r4(276 / B), "W / B": r4(w / B), "SP / B": r4(sp / B),
              "Sand (type not stated) / B": r4((202 + 810) / B), "Sand max size (µm)": 380, "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": 2.0, "Steel length (mm)": ln, "Steel tensile strength (MPa)": 2850, "Total fiber (vol%)": 2.0,
              "Curing method": "plastic sheet 2 d room temperature, then steam curing 90 C 3 d", "Curing time (days)": 5,
              "Curing temperature (°C)": 90, "Test age (days)": 5, "Heat curing duration (h)": 72,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix kg/m3), sect. 2.1 (fc 5 d, random fibres)",
              "Conversions / notes": f"{mid} fibre length {ln} mm. kg/m3 / B (cement + SF = 1196). Two quartz sands (0.11-0.21 mm fine 202 + 0.21-0.38 mm coarse 810) summed. "
                                     "HRWRA dose per mix from Table 2. fc = 5-day (2 d + 3 d steam) cubes with random fibre orientation. "
                                     "VERIFY: 5-day age is stated in text; steam '3 days' entered as 72 h heat curing; fibre diameter not stated."})
    rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e16.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")
