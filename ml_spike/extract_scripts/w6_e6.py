"""Wave 6, agent e6: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e6.csv (99-column TEMPLATE header).
Papers: conbuildmat.2024.135354, 139432, 138081, 137822, conbuildmat.2023.133591, 134654, 134579,
        cscm.2023.e02369, e02434, istruc.2023.03.123
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


# ------------------------------------------------ 1) PVP-modified PE fibers in HS-ECC, pristine control only (135354)
P = {"Article Name": "On use of polyvinylpyrrolidone to modify polyethylene fibers for improving tensile properties of high strength ECC",
     "Author": "Pengfei Men, Xiu-man Wang, Dawei Liu, Zhigang Zhang, Qian Zhang, Youfu Lu", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2024.135354"}
B = 718 + 574 + 128
r = dict(P)
r.update({"OPC / Cement": r4(718 / B), "FA (Fly ash)": r4(574 / B), "SF (Silica fume)": r4(128 / B), "W / B": r4(290 / B),
          "SS / B (Silica sand)": r4(430 / B), "SP / B": r4(18 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 1.96, "PE length (mm)": 12, "PE diameter (µm)": 26, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 1.96,
          "Curing method": "demolded at 24 h, then air 25 C RH 55 % until test", "Curing time (days)": 28,
          "Curing temperature (°C)": 25, "Curing RH (%)": 55, "Demolding age (days)": 1, "Test age (days)": 28,
          "Tensile specimen": "dog-bone (JSCE), 15 mm thick", "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 4.32, "Tensile strength (MPa)": 6.47, "Tensile strain capacity (%)": 3.55,
          "Source table/page": "Table 1 (mix), Table 2 (tensile, averages), sect. 2.2/2.3 (curing)",
          "Conversions / notes": "P-ECC = control with pristine PE fiber; PVP-modified-fiber mixes skipped (surface-treated fiber). kg/m3 / B = 1420. "
                                 "PE 19 kg/m3 / 970 = 1.96 vol%. VERIFY: tensile test age not stated (compression stated 28 d), 28 d assumed. fc only in Fig. 9."})
rows.append(r)

# ------------------------------------------------ 2) UVLP-ECC, 19 mixes (139432)
P = {"Article Name": "Mechanical properties and statistical analysis of Engineered Cementitious Composites (ECC) with ultrahigh-volume limestone powder incorporating several supplementary cementitious materials",
     "Author": "Weikang Wang, Xinhua Cai, Wei Zhou, Yamin Wang", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2024.139432"}
# id: (PC, MK, FA, BS, SP mass %, first cracking, ft, strain %)
mx = {"PC100": (1, 0, 0, 0, 0, 1.906, 4.811, 0.633),
      "PC75-MK25": (.75, .25, 0, 0, 1.0, 2.450, 2.455, 0.673),
      "PC50-MK50": (.5, .5, 0, 0, 1.5, 2.287, 3.036, 1.252),
      "PC25-MK75": (.25, .75, 0, 0, 2.0, 1.401, 2.858, 5.657),
      "PC75-FA25": (.75, 0, .25, 0, .5, 2.390, 3.525, 0.933),
      "PC50-FA50": (.5, 0, .5, 0, .5, 1.650, 2.877, 4.084),
      "PC25-FA75": (.25, 0, .75, 0, .5, 1.032, 1.392, 4.194),
      "PC75-BS25": (.75, 0, 0, .25, 1.1, 3.525, 3.970, 0.677),
      "PC50-BS50": (.5, 0, 0, .5, 1.1, 1.904, 2.955, 0.621),
      "PC25-BS75": (.25, 0, 0, .75, 1.1, 1.420, 2.613, 0.492),
      "PC25-MK25-FA50": (.25, .25, .5, 0, .5, 1.094, 2.679, 5.664),
      "PC25-MK50-FA25": (.25, .5, .25, 0, 2.0, 1.441, 2.953, 5.321),
      "PC50-MK25-FA25": (.5, .25, .25, 0, .5, 2.545, 3.546, 0.813),
      "PC25-MK25-BS50": (.25, .25, 0, .5, .5, 1.450, 3.774, 3.584),
      "PC25-MK50-BS25": (.25, .5, 0, .25, 2.0, 2.167, 4.313, 2.399),
      "PC50-MK25-BS25": (.5, .25, 0, .25, .5, 2.686, 3.858, 1.197),
      "PC25-FA25-BS50": (.25, 0, .25, .5, .5, 1.790, 3.480, 1.323),
      "PC25-FA50-BS25": (.25, 0, .5, .25, .5, 1.046, 2.911, 1.374),
      "PC50-FA25-BS25": (.5, 0, .25, .25, .5, 2.001, 4.049, 0.857)}
for mid, (pc, mk, fa, bs, sp, fcr, ft, eps) in mx.items():
    r = dict(P)
    r.update({"OPC / Cement": pc * .5, "Metakaolin": mk * .5 or None, "FA (Fly ash)": fa * .5 or None, "GGBS": bs * .5 or None,
              "Limestone powder": .5, "W / B": 0.275, "SP / B": round(sp / 100 / 2, 5) if sp else None,
              "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 42, "Total fiber (vol%)": 2,
              "Curing method": "demolded at 24 h, standard curing 20 C RH 95 % until test", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone 30x13 mm section", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 5 (tensile, mean of 3), sect. 2.2/3.1 (fc text)",
              "Conversions / notes": f"{mid}. Paper binder B = PC+MK+FA+BS with W/B 0.55 and limestone powder L/B = 1:1 (LP = 1 x B, so LP/C = 1/PC fraction); "
                                     "re-expressed on total powder (B + LP): binder fractions halved, LP 0.5, W/B = 0.275 (paper W/S). "
                                     "VERIFY: SP given as 'mass %' (assumed % of paper B, divided by 2 here); PC100 SP = 0. "
                                     "Table 3 names mix 15 'PC25-MK50-BS50' but fractions sum to 1 only with BS 0.25 (named PC25-MK50-BS25). "
                                     "Ultimate strain = mean ultimate tensile strain (Table 5). fc at 28 d only in Fig. 6/7 except PC100."})
    if mid == "PC100":
        r["Compressive strength (MPa)"] = 39.5
        r["Compressive specimen"] = "cube"
        r["Compressive specimen size (mm)"] = "40"
    rows.append(r)

# ------------------------------------------------ 3) HS-ECC with expanded vermiculite, control M1 only (138081)
P = {"Article Name": "Expanded vermiculite acting as artificial flaws to enhance the tensile properties of high-strength engineered cementitious composites",
     "Author": "Zhigang Zhang, Qiang Shen, Fengjiang Qin, Jamal A. Abdalla, Rami A. Hawileh, Yan Xiong", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2024.138081"}
B = 1 + .8 + .16
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(.8 / B), "SF (Silica fume)": r4(.16 / B), "W / B": r4(.39 / B),
          "SS / B (Silica sand)": r4(.59 / B), "SP / B": r4(.024 / B), "PE fiber (vol%)": 2, "PE length (mm)": 12,
          "PE diameter (µm)": 26, "Total fiber (vol%)": 2,
          "Curing method": "demolded at 24 h, then ambient 25 C RH 50-60 % for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 25, "Curing RH (%)": 55, "Demolding age (days)": 1, "Test age (days)": 28,
          "Tensile specimen": "dog-bone 30x15 mm section", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 77.6, "First-cracking strength (MPa)": 5.39, "Tensile strength (MPa)": 7.88,
          "Tensile strain capacity (%)": 2.56,
          "Source table/page": "Table 1 (mix), Table 2 (tensile), sect. 4.1 text (fc)",
          "Conversions / notes": "M1 control (silica sand, no vermiculite); M2-M6 skipped (expanded vermiculite). Mix ratios by weight to cement (C = 1), B = 1.96."})
rows.append(r)

# ------------------------------------------------ 4) UHPC steel fiber geometry (137822)
P = {"Article Name": "Predicting the tensile strength of ultra-high performance concrete: New insights into the synergistic effects of steel fiber geometry and distribution",
     "Author": "Zichao Que, Jinhui Tang, Huinan Wei, Ao Zhou, Kai Wu, Dujian Zou, Jiazhi Yang, Tiejun Liu, Geert De Schutter", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2024.137822"}
B = 862.8 + 215.7
t4 = [(9, .2, 8.27, .20, 8.09), (12, .2, 8.66, .30, 8.08), (16, .2, 9.08, .54, 7.62), (19, .2, 9.10, .48, 7.46), (22, .2, 8.98, .45, 7.38),
      (9, .16, 8.33, .19, 7.19), (12, .16, 8.52, .19, 8.17), (16, .16, 9.41, .31, 8.74), (19, .16, 9.08, .44, 8.99), (22, .16, 8.66, .03, 8.66)]
for l, d, ft, eps, fcr in t4:
    r = dict(P)
    r.update({"OPC / Cement": r4(862.8 / B), "SF (Silica fume)": r4(215.7 / B), "W / B": r4(169.5 / B), "River sand / B": r4(1078.5 / B),
              "SP / B": r4(32.4 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 1.99, "Steel length (mm)": l,
              "Steel diameter (µm)": int(d * 1000), "Total fiber (vol%)": 1.99,
              "Curing method": "covered 24 h at room temperature, demolded, water curing until test", "Curing time (days)": 28,
              "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone 300 mm long, 30 mm thick", "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 4 (tensile, 28 d), sect. 2.2 (curing)",
              "Conversions / notes": f"S-{l}-{d} (length {l} mm, diameter {d} mm straight steel). Steel 156 kg/m3 / 7850 = 1.99 vol%. "
                                     "VERIFY: text gives W/B 0.18 but Table 3 water 169.5 / 1078.5 = 0.157 (table value used, SP water not added). "
                                     "Strain = strain at max tensile strength (eps_pt). Water-storage temperature not stated. fc only in Fig. 4."})
    rows.append(r)

# ------------------------------------------------ 5) greener ECC with GGBS (133591)
P = {"Article Name": "Adhesive characteristics of novel greener engineered cementitious composite with conventional concrete substrate",
     "Author": "N. Shanmugasundaram, S. Praveenkumar", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2023.133591"}
B = 1254
# (id, ggbs kg, water, hrwr, fc, fcr, ft, eps)
t5 = [("CM 0.29", 0, 364, 0, 54.45, 1.3654, 2.5649, 3.5452), ("10GGBS", 125, 364, .502, 56.09, 1.6852, 2.8158, 3.5846),
      ("20GGBS", 251, 364, 1.380, 63.64, 1.7845, 3.2458, 3.5645), ("30GGBS", 376, 364, 2.257, 65.28, 1.7894, 3.4125, 3.7501),
      ("40GGBS", 502, 364, 3.010, 66.59, 1.8854, 3.8356, 3.7845), ("50GGBS", 627, 364, 3.762, 62.00, 1.6547, 2.1145, 3.7254),
      ("55GGBS", 690, 364, 4.264, 60.36, 1.6151, 1.9692, 3.6875),
      ("CM 0.36", 0, 451, 0, 53.14, 1.3750, 2.4407, 2.9001), ("CM 0.37", 0, 464, 0, 52.16, 1.3458, 2.1655, 3.3455)]
for mid, g, w, hr, fc, fcr, ft, eps in t5:
    r = dict(P)
    r.update({"OPC / Cement": r4((B - g) / B), "GGBS": r4(g / B) if g else None, "W / B": r4(w / B), "M-sand / B": r4(456 / B),
              "HRWR / B": r4(hr / B) if hr else None, "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12,
              "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.6",
              "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix), Table 5 (fc and tensile at 28 d)",
              "Conversions / notes": f"{mid}. kg/m3 / B (OPC + SCM = 1254). PVA 26 kg/m3 / 1300 = 2.0 vol%. Bagasse-ash and RHA mixes skipped. "
                                     "Curing of ECC specimens not stated (test age 28 d from Table 5). Strain = ultimate strain. "
                                     "VERIFY: reported values look rounded/odd (e.g. SD columns), W/CM 0.29 stated for CM 0.29 matches 364/1254."})
    rows.append(r)

# ------------------------------------------------ 6) UHPC with PP/POM replacing steel, R-0% (steel only) (134654)
P = {"Article Name": "Coarse synthetic fibers (PP and POM) as a replacement to steel fibers in UHPC: Tensile behavior, environmental and economic assessment",
     "Author": "Jia-Xiang Lin, Rui-Hao Luo, Jia-Ying Su, Yong-Chang Guo, Wei-Shan Chen", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2023.134654"}
B = 809 + 270
r = dict(P)
r.update({"OPC / Cement": r4(809 / B), "SF (Silica fume)": r4(270 / B), "W / B": r4(177 / B), "SS / B (Silica sand)": r4(1079 / B),
          "SP / B": r4(21.6 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 3, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
          "Steel tensile strength (MPa)": 2600, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 3,
          "Curing method": "demolded at 24 h at room temperature, then natural curing 28 d", "Curing time (days)": 28,
          "Demolding age (days)": 1, "Test age (days)": 29, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
          "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT, "Compressive strength (MPa)": 161,
          "First-cracking strength (MPa)": 11.4, "Tensile strength (MPa)": 12.7, "Tensile strain capacity (%)": 0.142,
          "Source table/page": "Table 2 (mix), Table 3 (fc), Table 4 (tensile), sect. 2.1 (curing)",
          "Conversions / notes": "R-0% = 3 vol% steel fiber only (PP/POM replacement mixes and fiber-free matrix skipped). Quartz sand 1079 kg/m3 (sand, not powder). "
                                 "VERIFY: test age 29 d = 1 d + 28 d natural curing (derived); strain = peak strain 0.142 %."})
rows.append(r)

# ------------------------------------------------ 7) aligned-steel-fiber UHPC, Case 0 (random) only (134579)
P = {"Article Name": "Transverse isotropic compression behavior of aligned steel fiber UHPC produced by electromagnetic field",
     "Author": "Yongming Xiong, Ming Yang, Jiankai Zhao, Yan Yuan, Yan Liu, Heng Shi", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2023.134579"}
B = 1 + .34 + .28
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(.34 / B), "FA (Fly ash)": r4(.28 / B), "W / B": r4(.32 / B),
          "Sand (type not stated) / B": r4(1.1 / B), "SP / B": r4(.018 / B), "Steel fiber (vol%)": 1.5, "Steel length (mm)": 13,
          "Steel diameter (µm)": 200, "Total fiber (vol%)": 1.5,
          "Curing method": "demolded 24 h, 24 h at 20 C RH>95 %, then steam curing 90 C 48 h", "Curing time (days)": 4,
          "Curing temperature (°C)": 90, "Demolding age (days)": 1, "Test age (days)": 4, "Heat curing duration (h)": 48,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": 140.9,
          "Source table/page": "Table 1 (mix, ratios to cement), Table 2 (Case 0 fc), sect. 2.2 (curing)",
          "Conversions / notes": "Case 0 = randomly oriented straight steel fiber (no electromagnetic alignment); Case 1/2 skipped. Ratios to cement, B = 1.62; "
                                 "coarse sand 0.88 + fine sand 0.22. VERIFY: test age 4 d derived (24 h + 24 h + 48 h steam)."})
rows.append(r)

# ------------------------------------------------ 8) steel-PE hybrid FRCC, compression (02369)
P = {"Article Name": "Compressive behavior of steel-polyethylene hybrid fiber reinforced cementitious composite",
     "Author": "Qun Xie, Xinwei Chai, Xiaowei Yu, Taochun Yang, Mingqiang Lin", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.cscm.2023.e02369"}
B = 600 + 480 + 120
geo = {"NF": None, "L6D0.2": (6, 200), "L13D0.2": (13, 200), "L6D0.12": (6, 120), "L10D0.12": (10, 120), "L13D0.12": (13, 120)}
t8 = [("NF", 0, 61.18), ("L6D0.2", .3, 65.01), ("L6D0.2", .6, 72.99), ("L6D0.2", .9, 76.68),
      ("L13D0.2", .3, 70.76), ("L13D0.2", .6, 70.84), ("L13D0.2", .9, 68.78),
      ("L6D0.12", .3, 73.74), ("L6D0.12", .6, 67.24), ("L6D0.12", .9, 71.32),
      ("L10D0.12", .3, 67.74), ("L10D0.12", .6, 62.27), ("L10D0.12", .9, 74.39),
      ("L13D0.12", .3, 71.61), ("L13D0.12", .6, 81.87), ("L13D0.12", .9, 62.91)]
for g, v, fc in t8:
    r = dict(P)
    r.update({"OPC / Cement": .5, "FA (Fly ash)": .4, "SF (Silica fume)": .1, "W / B": r4(300 / B), "River sand / B": r4(690 / B),
              "SP / B": r4(8 / B), "HPMC / B (hydroxypropyl methyl cellulose)": r4(.7 / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": 1.0, "PE length (mm)": 18, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 60,
              "Total fiber (vol%)": 1.0 + v, "Curing method": "covered 24 h, then curing room 28 d", "Curing time (days)": 28,
              "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "40",
              "Compressive strength (MPa)": fc, "Source table/page": "Table 1 (matrix), Table 3 (fibers), Table 4 (fc)",
              "Conversions / notes": f"{g}V{v}. Matrix kg/m3 / B (1200). PAC = polycarboxylate SP powder, HPMC 0.7 kg/m3. Curing room temperature/RH not stated. "
                                     "Peak strain is compressive, not entered."})
    if geo[g]:
        L, D = geo[g]
        r.update({"Steel fiber (vol%)": v, "Steel length (mm)": L, "Steel diameter (µm)": D, "Steel tensile strength (MPa)": 2850, "Steel elastic modulus (GPa)": 200})
    rows.append(r)

# ------------------------------------------------ 9) high strength ECC with limestone powder (02434)
P = {"Article Name": "Mechanical properties of sustainable high strength ECC with substitution of cement by limestone powder",
     "Author": "Zhigang Zhang, Yifei Gao, Fengjiang Qin, Feng Sun, Yubin Huang", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.cscm.2023.e02434"}
# id: (cement, LP, fc28, fc7, first crack, ft, strain)
t9 = [("E-0", 898.91, 0, 100.8, 70.5, 6.13, 8.63, 3.29), ("E-20-500", 719.13, 179.78, 87.4, 67.0, 4.49, 9.66, 5.55),
      ("E-40-500", 539.35, 359.56, 79.9, None, 4.45, 7.78, 5.98), ("E-60-500", 359.56, 539.35, 58.3, None, 3.96, 6.42, 6.52),
      ("E-40-300", 539.35, 359.56, 74.9, None, 4.17, 7.31, 4.47), ("E-40-3000", 539.35, 359.56, None, None, 6.01, 11.51, 7.83)]
B = 898.91 + 451.2 + 90.99
for mid, c, lp, fc28, fc7, fcr, ft, eps in t9:
    base = dict(P)
    base.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(451.2 / B), "SF (Silica fume)": r4(90.99 / B),
                 "Limestone powder": r4(lp / B) if lp else None, "W / B": r4(275 / B), "SS / B (Silica sand)": r4(451 / B), "SP / B": r4(20 / B),
                 "Binder content (kg/m³)": round(B, 1), "PE fiber (vol%)": 2.06, "PE length (mm)": 18, "PE diameter (µm)": 26,
                 "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2.06,
                 "Curing method": "demolded at 24 h, then air 25 C RH 55 % until test", "Curing temperature (°C)": 25, "Curing RH (%)": 55,
                 "Demolding age (days)": 1, "Source table/page": "Table 2 (mix, g/L), Table 3 (tensile), sect. 3.3 text (fc)",
                 "Conversions / notes": f"{mid}. g/L = kg/m3, B = cement + FA + SF + LP = 1441.1 (LP replaces cement, binder total constant). PE 20 kg/m3 / 970 = 2.06 vol%. "
                                        "Article name taken from text (TITLE field says 'Case study'). "
                                        + ("fc 28 d of E-40-3000 only as +18.7 % vs E-40-300 (derived), not entered. " if mid == "E-40-3000" else "")})
    r = dict(base)
    r.update({"Curing time (days)": 28, "Test age (days)": 28, "Compressive strength (MPa)": fc28, "Tensile specimen": "dog-bone 30x15 mm section",
              "Tensile test type": DIRECT, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps})
    rows.append(r)
    if fc7:
        r = dict(base)
        r.update({"Curing time (days)": 7, "Test age (days)": 7, "Compressive strength (MPa)": fc7})
        rows.append(r)

# ------------------------------------------------ 10) steel-PVA hybrid SPHFRCC (istruc 03.123)
P = {"Article Name": "Predicting the flexural behavior of steel-PVA hybrid fiber reinforced cementitious composite",
     "Author": "Zhaoyao Wang, Xingwen Liang, Tianwen Zhai", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.istruc.2023.03.123"}
# id: (cement, water, FA, SF, sand, SP, steel vol, PVA vol, fc7, fc28, ft)
t10 = [("SPH-2", 693.85, 187.34, 173.46, 117.95, 1158.73, 24.63, 1.0, .75, 75.19, 100.97, 6.23),
       ("SPH-3", 693.85, 187.34, 173.46, 117.95, 1158.73, 24.63, 1.25, .5, 70.33, 92.11, 6.57),
       ("SPH-4", 693.85, 187.34, 173.46, 117.95, 1158.73, 24.63, 1.5, .25, 82.32, 111.38, 5.65),
       ("SPH-5", 693.85, 187.34, 173.46, 117.95, 1158.73, 24.63, 1.75, 0, 72.96, 103.45, 5.12),
       ("SPH-6", 695.61, 187.82, 173.90, 118.25, 1161.68, 24.69, 1.5, 0, 75.76, 118.97, None),
       ("SPH-7", 694.91, 187.63, 173.73, 118.13, 1160.50, 24.67, 1.5, .1, 72.74, 114.70, None),
       ("SPH-8", 692.79, 187.05, 173.20, 117.77, 1156.96, 24.59, 1.5, .4, 79.89, 106.31, None),
       ("SPH-10", 721.03, 194.68, 180.26, 122.58, 1204.12, 25.60, 1.0, .75, 76.23, 99.91, 5.97),
       ("SPH-11", 721.03, 194.68, 180.26, 122.58, 1204.12, 25.60, 1.25, .5, 73.95, 104.64, 6.35),
       ("SPH-12", 721.03, 194.68, 180.26, 122.58, 1204.12, 25.60, 1.5, .25, 87.33, 111.17, 5.51),
       ("SPH-13", 721.03, 194.68, 180.26, 122.58, 1204.12, 25.60, 1.75, 0, 87.22, 109.65, 5.23),
       ("SPH-15", 668.64, 180.53, 167.16, 113.67, 1116.63, 23.74, 1.0, .75, 76.94, 109.94, 6.15),
       ("SPH-16", 668.64, 180.53, 167.16, 113.67, 1116.63, 23.74, 1.25, .5, 65.72, 92.40, 6.49),
       ("SPH-17", 668.64, 180.53, 167.16, 113.67, 1116.63, 23.74, 1.5, .25, 76.19, 120.51, 5.34),
       ("SPH-18", 668.64, 180.53, 167.16, 113.67, 1116.63, 23.74, 1.75, 0, 93.11, 115.23, 4.92)]
for mid, c, w, fa, sf, sa, sp, sv, pv, f7, f28, ft in t10:
    B = c + fa + sf
    for age, fc in ((7, f7), (28, f28)):
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B),
                  "SS / B (Silica sand)": r4(sa / B), "SP / B": r4(sp / B), "Binder content (kg/m³)": round(B, 1),
                  "Steel fiber (vol%)": sv, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850,
                  "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": sv + pv,
                  "Curing method": "indoor 48 h, demolded, then standard curing box RH >= 90 % ~20 C", "Curing time (days)": age - 2,
                  "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 2, "Test age (days)": age,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 2 (mix), Table 3 (fc, ft), sect. 2.3 (curing)",
                  "Conversions / notes": f"{mid}. Water/binder 0.19 stated. kg/m3 / B. Silica sand graded. SP liquid polycarboxylate as dosed."})
        if pv:
            r.update({"PVA fiber (vol%)": pv, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42})
        if age == 28 and ft is not None:
            r.update({"Tensile strength (MPa)": ft, "Tensile test type": DIRECT})
            r["Conversions / notes"] += " VERIFY: age of direct tension test (ft) not stated, assigned to 28 d row. No strain reported."
        rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e6.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e6.csv"))
