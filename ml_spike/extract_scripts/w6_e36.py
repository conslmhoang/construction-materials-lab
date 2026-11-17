"""Wave 6, agent e36: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e36.csv (99-column TEMPLATE header).
Papers: conbuildmat 2020.119943, 2020.120225, 2020.120961, 2020.121382, 2021.122618, 2021.123427, 2021.125104,
        2022.127900, 2022.128422, 2023.131580, 2023.133917, 2024.135618, 2024.136063
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


# ---------- 1) Sun et al. 2020: PVA-ECC, three w/b, 28-d properties (Table 4)
P = paper("Chloride diffusion behavior of engineered cementitious composite under dry-wet cycles",
          "Renjuan Sun, Xinlei Hu, Yifeng Ling, Zhiwu Zuo, Peizhi Zhuang, Fei Wang", 2020, "10.1016/j.conbuildmat.2020.119943")
for nm, wb, w, c, fa, sand, pva, thick, hr, fc, ts, eps in [
        ("A", 0.26, 339, 593, 712, 474, 26, 0.59, 5.22, 48.6, 4.84, 4.21),
        ("B", 0.28, 356, 578, 693, 462, 26, 0.58, 5.08, 39.8, 3.08, 4.63),
        ("C", 0.30, 372, 563, 676, 450, 26, 0.56, 4.95, 33.7, 2.92, 4.85)]:
    B = c + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(sand / B),
              "VMA / B": r4(thick / B), "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": r4(pva / 1300 * 100), "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560,
              "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": r4(pva / 1300 * 100),
              "Curing method": "23 C, 90 % RH for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 90,
              "Test age (days)": 28, "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), Table 2 (PVA), Table 4 (28-d properties), sect. 2.2",
              "Conversions / notes": f"Mix {nm}, w/b {wb}. kg/m3 / B (cement + FA = {B}). PVA 26 kg/m3 / 1300 = 2.0 vol%. Thickener entered as VMA / B. "
                                     "'Ultimate tensile strain' = strain capacity. VERIFY: tensile specimen shape / test not described in the text (assumed direct tension)."})
    rows.append(r)

# ---------- 2) Wang et al. 2020: UHPC with 1.5 vol% steel fibre (Table 3), 7 and 28 d (Table 2)
P = paper("Experimental study on ultra-high performance concrete under triaxial compression",
          "Yuan-Zuo Wang, Yan-Bo Wang, Yuan-Zi Zhao, Guo-Qiang Li, Yi-Fan Lyu, Heng Li", 2020, "10.1016/j.conbuildmat.2020.120225")
B = 1028.17 + 102.81
for age, fc in [(7, 141.0), (28, 148.1)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1028.17 / B), "SF (Silica fume)": r4(102.81 / B), "W / B": r4(203.57 / B),
              "Sand (type not stated) / B": r4(1048.13 / B), "SP / B": r4(13.69 / B), "Binder content (kg/m³)": r4(B),
              "Steel fiber (vol%)": 1.5, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2600,
              "Total fiber (vol%)": 1.5,
              "Curing method": "24 h in mould, then curing room 20 +/- 3 C, 98 % RH", "Curing time (days)": age, "Curing temperature (°C)": 20,
              "Curing RH (%)": 98, "Demolding age (days)": 1, "Test age (days)": age, "Compressive specimen": "cylinder",
              "Compressive specimen size (mm)": "100 x 200", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 2 (fc at 7 and 28 curing days, 1.5 % fibre), sect. 2.1",
              "Conversions / notes": "UHPC with 1.5 vol% steel fibre (116.84 kg/m3). fc = mean of 3 cylinders in Table 2 (1.5 % row; density 2504 matches Table 3 mix). "
                                     "VERIFY: curing room conditions stated for the 7 d period, assumed the same up to 28 d. Sand type not stated. "
                                     "Steel fibre strength '>2600 MPa'. Triaxial results and fibre-free UHSC skipped. Core fc 153.4 MPa (Table 5) not used (age not stated)."})
    rows.append(r)

# ---------- 3) Zhang et al. 2020: SHUHPC with PE fibre only (S-PE1.5)
P = paper("Spalling resistance and mechanical properties of strain-hardening ultra-high performance concrete at elevated temperature",
          "Dong Zhang, Yuchen Liu, Kang Hai Tan", 2020, "10.1016/j.conbuildmat.2020.120961")
B = 1289 + 143
r = dict(P)
r.update({"OPC / Cement": r4(1289 / B), "SF (Silica fume)": r4(143 / B), "W / B": r4(284 / B), "SS / B (Silica sand)": r4(573 / B),
          "SP / B": r4(25 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 1.5, "PE length (mm)": 12, "PE diameter (µm)": 28,
          "PE tensile strength (MPa)": 3250, "PE elastic modulus (GPa)": 113, "Total fiber (vol%)": 1.5,
          "Curing method": "1 d under plastic sheet at room temp, demoulded, lime-saturated water at room temp 27 d", "Curing time (days)": 28,
          "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 7.69, "Tensile strength (MPa)": 9.17, "Tensile strain capacity (%)": 1.75,
          "Source table/page": "Table 1 (mix), Table 2 (PE), Table 3 (tensile, ambient), sect. 2.1-2.4",
          "Conversions / notes": "S-PE1.5 only (mixes with PP fibre skipped). kg/m3 / B (cement + SF = 1432). PE diameter 26-30 um, mid 28. "
                                 "Tensile test at ambient temperature (reference for the high-temperature series). VERIFY: tensile test age (28 d) assumed same as the stated 28-d curing."})
rows.append(r)

# ---------- 4) Shi et al. 2020: eco-efficient UHPC, 1.5 vol% steel fibre; ST 28 d, SC 80C 48 h, AC 180C 8 h (Table 7)
P = paper("Design of binder system of eco-efficient UHPC based on physical packing and chemical effect optimization",
          "Ye Shi, Guangcheng Long, Xiaohui Zen, Youjun Xie, Taoping Shang", 2020, "10.1016/j.conbuildmat.2020.121382")
mix = {  # C, FA, GGBS, SF, water(total), SP, sand
    "A1": (843.4, 0, 0, 210.9, 179.2, 32.7, 1159.7), "A2": (573.8, 0, 260.8, 208.6, 177.3, 27.1, 1147.5),
    "A3": (467.5, 0, 363.6, 207.8, 176.6, 27.0, 1142.7), "A4": (362.1, 0, 465.5, 206.9, 175.9, 21.7, 1137.9),
    "A5": (257.5, 0, 566.6, 206.0, 175.1, 16.5, 1133.2), "A6": (564.9, 256.8, 0, 205.4, 174.6, 27.7, 1129.7),
    "A7": (457.4, 355.8, 0, 203.3, 172.8, 26.4, 1118.1), "A8": (352.2, 452.8, 0, 201.2, 171.1, 25.2, 1106.8),
    "A9": (249.0, 547.9, 0, 199.2, 169.3, 22.9, 1095.7), "B1": (570.2, 103.7, 155.5, 207.3, 176.2, 24.9, 1140.3),
    "B2": (569.4, 186.4, 103.5, 176.0, 176.0, 19.7, 1138.9), "B3": (464.6, 103.2, 258.1, 206.5, 175.5, 22.7, 1135.6),
    "B4": (462.5, 174.7, 185.0, 205.6, 174.7, 22.6, 1130.6), "B5": (358.3, 235.4, 255.9, 174.0, 174.0, 20.5, 1126.0),
    "B6": (360.0, 154.3, 339.5, 174.9, 174.9, 20.6, 1131.6), "B7": (254.4, 203.5, 356.1, 203.5, 173.0, 16.3, 1119.3),
    "B8": (252.8, 303.4, 252.8, 202.3, 171.9, 16.2, 1112.4), "C1": (358.7, 153.7, 307.5, 205.0, 174.2, 18.4, 1127.4),
    "D1": (568.4, 155.0, 103.3, 206.7, 175.7, 21.5, 1136.8), "D2": (358.7, 153.7, 307.5, 205.0, 174.2, 11.6, 1127.4)}
fcs = {  # ST, SC, AC
    "A1": (156, 177, 202), "A2": (163, 182, 210), "A3": (161, 174, 199), "A4": (148, 160, 182), "A5": (135, 153, 156),
    "A6": (159, 179, 209), "A7": (155, 161, 182), "A8": (141, 147, 157), "A9": (122, 138, 140), "B1": (175, 164, 205),
    "B2": (166, 170, 204), "B3": (159, 167, 185), "B4": (157, 176, 185), "B5": (150, 150, 176), "B6": (152, 159, 185),
    "B7": (132, 155, 171), "B8": (131, 150, 157), "C1": (154, 161, 188), "D1": (167, None, 205), "D2": (149, None, 185)}
for nm, (c, fa, g, sf, wt, sp, sand) in mix.items():
    B = c + fa + g + sf
    wfree = wt - 0.6 * sp   # total water includes the water in the SP (solid content about 40 %)
    for k, kind in enumerate(["ST", "SC", "AC"]):
        fc = fcs[nm][k]
        if fc is None:
            continue
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "GGBS": r4(g / B), "SF (Silica fume)": r4(sf / B),
                  "W / B": r4(wfree / B), "SS / B (Silica sand)": r4(sand / B), "SP / B": r4(sp / B), "Binder content (kg/m³)": r4(B),
                  "Steel fiber (vol%)": 1.5, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Total fiber (vol%)": 1.5,
                  "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40 x 40 x 160 prism",
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 2 (mix), Table 7 (fc ST/SC/AC), sect. 2.1-2.3"})
        base = (f"Mix {nm}. kg/m3 / B (C + FA + GGBS + SF = {r4(B)}). Total water includes the SP water: free water = total - 0.6 x SP (SP solid content ~40 %, VERIFY derived). "
                "Quartz sand, steel fibre 1.5 vol% (120 kg/m3, 13 x 0.2 mm). Nano-material mixes C2, C3 skipped. ")
        if kind == "ST":
            r.update({"Curing method": "24 h covered with plastic, demoulded, standard curing 20 C, 100 % RH", "Curing time (days)": 28,
                      "Curing temperature (°C)": 20, "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": 28})
            r["Conversions / notes"] = base + "Standard curing, tested at 28 d (stated)."
        elif kind == "SC":
            r.update({"Curing method": "24 h in mould, then steam curing 80 C for 48 h (ramp 20 C/h)", "Curing time (days)": 3,
                      "Curing temperature (°C)": 80, "Demolding age (days)": 1, "Test age (days)": 3, "Heat curing duration (h)": 48})
            r["Conversions / notes"] = base + "VERIFY: steam-cured samples tested right after heat curing; test age 3 d derived (1 d + 48 h), ramp time ignored."
        else:
            r.update({"Curing method": "24 h in mould, then autoclave 180 C for 8 h (ramp 40 C/h)", "Curing time (days)": 1.33,
                      "Curing temperature (°C)": 180, "Demolding age (days)": 1, "Test age (days)": 1.33, "Heat curing duration (h)": 8})
            r["Conversions / notes"] = base + "VERIFY: autoclaved samples tested right after heat curing; test age ~1.33 d derived (1 d + 8 h), ramp time ignored."
        rows.append(r)

# ---------- 5) Zhou et al. 2021: GHD-ECC-0 (no nano-silica), 100 % recycled fine aggregate
P = paper("Performance enhancement of green high-ductility engineered cementitious composites by nano-silica incorporation",
          "Yingwu Zhou, Shuyue Zheng, Xiaoxu Huang, Bin Xi, Zhenyu Huang, Menghuan Guo", 2021, "10.1016/j.conbuildmat.2021.122618")
B = 600 + 750 + 150 + 180
r = dict(P)
r.update({"OPC / Cement": r4(600 / B), "GGBS": r4(750 / B), "SF (Silica fume)": r4(150 / B), "Limestone powder": r4(180 / B),
          "W / B": r4(300 / B), "Sand (type not stated) / B": r4(500 / B), "HRWR / B": r4(25 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": r4(20 / 970 * 100), "PE length (mm)": 18, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": r4(20 / 970 * 100),
          "Curing method": "24 h room condition, demoulded, standard curing room 23 +/- 3 C, 95 % RH", "Curing time (days)": 28,
          "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 60.6, "Tensile strength (MPa)": 4.85, "Tensile strain capacity (%)": 10.54,
          "Source table/page": "Table 4 (mix), Table 2 (PE), sect. 3.2 (fc), sect. 3.3 (tensile), sect. 2.2",
          "Conversions / notes": "GHD-ECC-0 only (NS mixes skipped). kg/m3 / B with LP counted in binder (C + GGBS + SF + LP = 1680; VERIFY LP as binder). "
                                 "VERIFY: sand = 100 % recycled fine aggregate (RFA, recycled-concrete sand) entered as sand. "
                                 "PE 20 kg/m3 / 970 = 2.06 vol% (derived). Tensile values: ultimate stress 4.85 MPa and strain ~10.54 % as stated in text."})
rows.append(r)

# ---------- 6) Dong et al. 2021: hybrid PE/steel fibre concrete, ambient tensile (Table 3), 28 d
P = paper("Effect of freeze-thaw cycling on mechanical properties of polyethylene fiber and steel fiber reinforced concrete",
          "Fangyuan Dong, Hanpeng Wang, Jiangtao Yu, Keke Liu, Zhenwen Guo, Xinzhi Duan, Xing Qiong", 2021, "10.1016/j.conbuildmat.2021.123427")
B = 666 + 133.2 + 437.7
for nm, sp, pe, st, ts, eps in [("M1", 12, 19.4, 0, 8.16, 6.43), ("M2", 9, 14.55, 39, 5.56, 5.28), ("M3", 7, 9.7, 78, 5.98, 1.15),
                                ("M4", 6, 4.9, 117, 6.56, 0.63), ("M5", 5, 0, 156, 6.22, 0.53)]:
    pv, sv = pe / 970 * 100, st / 7850 * 100
    r = dict(P)
    r.update({"OPC / Cement": r4(666 / B), "SF (Silica fume)": r4(133.2 / B), "FA (Fly ash)": r4(437.7 / B), "W / B": r4(272.1 / B),
              "River sand / B": r4(666 / B), "SP / B": r4(sp / B), "Sand max size (µm)": 210, "Binder content (kg/m³)": r4(B),
              "PE fiber (vol%)": r4(pv), "PE length (mm)": 24, "PE diameter (µm)": 18, "PE tensile strength (MPa)": 2900,
              "Steel fiber (vol%)": r4(sv), "Steel length (mm)": 25, "Steel diameter (µm)": 300, "Steel tensile strength (MPa)": 2000,
              "Total fiber (vol%)": r4(pv + sv),
              "Curing method": "24 h in mould under plastic sheet, demoulded, cured for another 27 d", "Curing time (days)": 28,
              "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix, g/L), Table 2 (fibres), Table 3 (tensile before freeze-thaw), sect. 2.1-2.2",
              "Conversions / notes": f"{nm}. Table 1 in g/L taken as kg/m3. B = cement + SF + FA = {r4(B)}; W/B = 272.1/B = 0.22 (the paper's w/b 0.143 equals water / (B + sand), VERIFY). "
                                     "PE 970 and steel 7850 kg/m3 densities for vol% (steel density printed as '78' in Table 2). "
                                     "Strain = 'strain at peak tensile strength' (ultimate strain 8.68 / 7.73 / 3.94 / 1.13 / 1.20 % also given); values before freeze-thaw only. "
                                     "VERIFY: curing temperature / RH not stated; fc only in a figure; PE/steel fibre content in g/L converted to vol%."})
    rows.append(r)

# ---------- 7) Pham et al. 2021: UHPC rubberised (static fc, Table 4)
P = paper("Experimental investigation on dynamic properties of ultra-high-performance rubberized concrete (UHPRuC)",
          "Thong M. Pham, John Davis, Ngoc San Ha, Emad Pournasiri, Feng Shi, Hong Hao", 2021, "10.1016/j.conbuildmat.2021.125104")
B = 995 + 238
for nm, sand, rp, fc in [("UHPC-R00", 1051, 0, 136.1), ("UHPC-R10", 946, 51, 115.8), ("UHPC-R20", 841, 103, 103.8), ("UHPC-R40", 631, 206, 67.8)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(995 / B), "SF (Silica fume)": r4(238 / B), "W / B": r4(180 / B), "SS / B (Silica sand)": r4(sand / B),
              "HRWR / B": r4(67 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": r4(156 / 7850 * 100), "Total fiber (vol%)": r4(156 / 7850 * 100),
              "Curing method": "24 h in mould, then steam room 70 C for 72 h, cooled at least 24 h before test", "Curing time (days)": 4,
              "Curing temperature (°C)": 70, "Demolding age (days)": 1, "Test age (days)": 5, "Heat curing duration (h)": 72,
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 4 (static compressive strength), sect. 2.1.2.3",
              "Conversions / notes": f"{nm}. kg/m3 / B (OPC + SF = {B}). Rubber powder 30 mesh (crumb rubber) replaces silica sand by volume. "
                                     "Steel fibre 156 kg/m3 / 7850 = 1.99 vol%. HRWR 67 kg/m3 as stated. "
                                     "VERIFY: static test age not stated, derived as >= 5 d (1 d + 72 h steam + >= 24 h cooling); specimen size for static fc not stated."})
    if rp:
        r["Crumb rubber / B"] = r4(rp / B)
    rows.append(r)

# ---------- 8) Kan et al. 2022: red-mud ECC, control 0%RM-ECC only
P = paper("An exploratory study on using red mud waste as a replacement for fly ash to prepare Engineered Cementitious Composites",
          "Lili Kan, Fei Wang, Yafeng Zhang, Yanping Wei, Min Wu", 2022, "10.1016/j.conbuildmat.2022.127900")
B = 42.91 + 18.39
r = dict(P)
r.update({"OPC / Cement": r4(18.39 / B), "FA (Fly ash)": r4(42.91 / B), "W / B": r4(18.39 / B), "Sand (type not stated) / B": r4(18.39 / B),
          "HRWR / B": r4(0.54 / B), "VMA / B": r4(0.10 / B), "PVA fiber (vol%)": 1.7, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
          "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 1.7,
          "Curing method": "24 h laboratory conditions, demoulded, 20 +/- 1 C, 70 +/- 5 % RH", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Curing RH (%)": 70, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80,
          "Tensile test type": DIRECT, "Tensile strength (MPa)": 3.19, "First-cracking strength (MPa)": 2.34, "Tensile strain capacity (%)": 3.22,
          "Source table/page": "Table 1 (mix, wt%), Table 2 (tensile 28 d), Table 6 (PVA), sect. 2.2-2.3",
          "Conversions / notes": "0%RM-ECC (control, no red mud) only. Mix in wt% of total, ratios to B = OPC + FA (61.30). PVA 1.7 vol%. "
                                 "HRWRA 0.54 and VM 0.10 wt% as listed (HRWRA/B 0.9 %, VM/B 0.2 % stated). Sand type not stated. fc only in a figure (120 d)."})
rows.append(r)

# ---------- 9) Lin et al. 2022: seawater sea-sand ECC, fresh-water control F0 (no sodium aluminate)
P = paper("Effects of sodium aluminate on the performance of seawater sea-sand engineered cementitious composites",
          "Chenlong Lin, Siyu Wang, Wentao Ma, Yuhong Yan, Yiyan Lu", 2022, "10.1016/j.conbuildmat.2022.128422")
fcF0 = {1: 1.73, 3: 7.06, 7: 14.31, 14: 18.98, 28: 23.98, 60: 29.35}
for age, fc in fcF0.items():
    r = dict(P)
    r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.72, "GGBS": 0.08, "W / B": 0.27, "Sea sand / B": 0.25, "HRWR / B": 0.002,
              "PVA fiber (vol%)": 2.5, "PVA length (mm)": 12, "PVA diameter (µm)": 20, "PVA tensile strength (MPa)": 1300, "PVA elastic modulus (GPa)": 37,
              "Total fiber (vol%)": 2.5, "Curing method": "demoulded after 1 d at 20 C, standard curing 20 +/- 2 C, RH >= 90 %", "Curing time (days)": age,
              "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": age,
              "Compressive specimen": "prism halves", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 2 (PVA), Table 4 (fc, average of 3), Table 5 (tensile F0), sect. 2.2-2.4",
              "Conversions / notes": "F0: fresh (tap) water, sea sand, no sodium aluminate. Mass ratios to binder (cement + FA + GGBS = 1). "
                                     "VERIFY: HRWR 0.2 % assumed to be relative to binder; sea sand dried (moisture < 0.35 %). Seawater mixes S0-S4 and NaAlO2 mixes skipped. "
                                     "fc = average of three specimens, 40 x 40 x 160 prism halves per GB/T 17671 (VERIFY)."})
    if age == 28:
        r.update({"Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT, "First-cracking strength (MPa)": 1.70,
                  "Tensile strength (MPa)": 3.21, "Tensile strain capacity (%)": 2.06})
        r["Conversions / notes"] += " Tensile: average sigma_cr 1.70, sigma_u 3.21 MPa, eps_u 2.06 % of F0 (Table 5)."
    rows.append(r)

# ---------- 10) Wang et al. 2023: UHPC reference (no freeze-thaw), air curing 28 d
P = paper("Systematic studies on behaviors of ultra-high performance concrete subject to freezing and thawing cycles combining DIC technology",
          "Fei Wang, Lili Kan, Jiangtao Yu, Xin-Zhi Duan", 2023, "10.1016/j.conbuildmat.2023.131580")
B = 35.4 + 7.1
r = dict(P)
r.update({"OPC / Cement": r4(35.4 / B), "SF (Silica fume)": r4(7.1 / B), "W / B": 0.18, "Sand (type not stated) / B": r4(42.5 / B),
          "SP / B": 0.005, "Steel fiber (vol%)": 2, "Steel length (mm)": 14, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2450,
          "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2,
          "Curing method": "covered 24 h in air 20 C, RH 70 %, demoulded, air curing to 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Curing RH (%)": 70, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "prism half",
          "Compressive specimen size (mm)": "100 x 100", "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 120.6, "First-cracking strength (MPa)": 6.10, "Tensile strength (MPa)": 7.90, "Tensile strain capacity (%)": 0.23,
          "Source table/page": "Table 3 (mix, wt%), Table 2 (steel fibre), Table 5 (tensile, 'Reference'), sect. 3 text (fc), sect. 2.2",
          "Conversions / notes": "Reference specimens (no freeze-thaw, 0 cycles). Mix wt%: C 35.4, SF 7.1, sand 42.5, water 7.8, SP 0.2; B = C + SF. "
                                 "W/B 0.18 and SP 0.5 % of cementitious as stated by the paper (7.8/42.5 = 0.184). Sand type not stated. "
                                 "VERIFY: tensile tested at 28 d presumed same as the other reference tests; fc from the 100 x 100 mm cross-section of bending prism halves."})
rows.append(r)

# ---------- 11) Chen et al. 2023: SMA-ECC, SC-1 (no SMA fibre) intact compressive peak stress
P = paper("Evaluation of compression self-healing performance of a smart cementitious composite SMA-ECC",
          "Weihong Chen, Chunhui Han, Yunjun Xie, Boxu Lin, Shuangshuang Cui", 2023, "10.1016/j.conbuildmat.2023.133917")
r = dict(P)
r.update({"OPC / Cement": 0.25, "FA (Fly ash)": 0.6, "GGBS": 0.15, "W / B": 0.25, "SS / B (Silica sand)": 0.4,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 42,
          "Total fiber (vol%)": 2, "Curing method": "standard curing room (CECS 13:2009), 28 d", "Curing time (days)": 28, "Test age (days)": 28,
          "Compressive specimen": "prism", "Compressive specimen size (mm)": "40 x 40 x 160", "Compressive strength (MPa)": 43.09,
          "Source table/page": "Table 2 (mix), Table 1 (PVA), Table 5 (sigma_c of SC-1), sect. 2.2",
          "Conversions / notes": "SC-1 (no SMA fibre) only. Weight proportions C : FA : mineral powder : quartz sand : water = 0.25 : 0.6 : 0.15 : 0.4 : 0.25. "
                                 "VERIFY: 'mineral powder' = S95 slag powder entered as GGBS; fc = peak stress sigma_c of intact specimens in the two-stage compression test. "
                                 "Water reducer dose not stated."})
rows.append(r)

# ---------- 12) Cheng et al. 2024: HSECC with original PE fibre (O-PE)
P = paper("Effect of modified PE fiber grafted with nano-SiO2 on the tensile properties of high-strength engineering cementitious composites",
          "Heng Cheng, Hao Sun, Zuhua Zhang, Jinbang Wang, Xiuzhi Zhang, Peng Du", 2024, "10.1016/j.conbuildmat.2024.135618")
r = dict(P)
r.update({"OPC / Cement": 0.45, "GGBS": 0.35, "FA (Fly ash)": 0.10, "SF (Silica fume)": 0.10, "W / B": 0.16, "SS / B (Silica sand)": 0.3,
          "SP / B": 0.004, "HPMC / B (hydroxypropyl methyl cellulose)": 0.0001, "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24,
          "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 80, "Total fiber (vol%)": 2,
          "Curing method": "24 h at 22 +/- 2 C, RH > 95 %, then water bath 90 C for 3 d", "Curing time (days)": 4, "Curing temperature (°C)": 90,
          "Demolding age (days)": 1, "Test age (days)": 4, "Heat curing duration (h)": 72, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 3.84, "Tensile strength (MPa)": 8.72, "Tensile strain capacity (%)": 3.01,
          "Source table/page": "Table 3 (mix, mass ratios to binder), Table 2 (PE), Table 4 (O-PE), sect. 2.3-2.4.3",
          "Conversions / notes": "O-PE (unmodified fibre) only; SCA / nano-SiO2 modified fibres skipped. Mass ratios of binder (C + slag + FA + SF = 1). "
                                 "HPMC 0.01 %, defoamer 0.1 % (defoamer not entered as a column). VERIFY: test age 4 d derived from 24 h + 3 d hot-water curing (end of curing, test age not stated). "
                                 "fc 'about 92 MPa' cited from another study, not entered."})
rows.append(r)

# ---------- 13) Wang et al. 2024: low-cost ECC with Yellow River silt as sand, 28 d
P = paper("Development of low-cost engineered cementitious composites using Yellow River silt and unoiled PVA fiber",
          "Hanghui Wang, Jinxia Xu, Yingbin Song, Manlin Hou, Yi Xu", 2024, "10.1016/j.conbuildmat.2024.136063")
WW = {"PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1073, "PVA elastic modulus (GPa)": 29}
RECF = {"PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41}
# id, S/B, W/B, vol%, fibre, fc, f0, fu, eps, note
data = [("W1", 0.375, 0.27, 2.0, WW, 29.5, 3.40, 4.00, 1.78, ""),
        ("W0", 0.375, 0.30, 2.0, WW, 25.1, 2.32, 3.00, 1.96, " fc 25.1 from the ingredient comparison (WW-ECC); the fibre-content text gives 25.6 for the same mix (VERIFY)."),
        ("W2", 0.375, 0.33, 2.0, WW, None, 2.06, 2.48, 2.02, " fc not stated as a number."),
        ("W3", 0.375, 0.36, 2.0, WW, 19.4, 1.88, 1.89, 2.09, ""),
        ("S1", 0.325, 0.30, 2.0, WW, 23.6, 1.27, 1.57, 1.64, ""),
        ("S2", 0.425, 0.30, 2.0, WW, None, 2.30, 2.63, 1.77, " fc not stated as a number."),
        ("S3", 0.475, 0.30, 2.0, WW, 25.7, 1.36, 1.41, 1.52, ""),
        ("F1", 0.375, 0.30, 1.75, WW, 24.3, 2.17, 2.20, 1.66, ""),
        ("F2", 0.375, 0.30, 2.25, WW, None, 2.44, 2.87, 1.83, " fc not stated as a number."),
        ("F3", 0.375, 0.30, 2.5, WW, 24.6, 2.58, 2.71, 1.67, ""),
        ("REC", 0.375, 0.30, 2.0, RECF, 24.4, 2.29, 2.40, 3.08, " Imported oiled PVA fibre (RECS15x12)."),
        ]
for nm, sb, wb, vol, fib, fc, f0, fu, eps, extra in data:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / 1.7), "FA (Fly ash)": r4(0.7 / 1.7), "W / B": wb, "Sand (type not stated) / B": sb, "SP / B": 0.01,
              "HPMC / B (hydroxypropyl methyl cellulose)": 0.0005, "PVA fiber (vol%)": vol, "Total fiber (vol%)": vol,
              "Curing method": "24 h under polyethylene film, demoulded, standard curing room 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "prism", "Compressive specimen size (mm)": "40 x 40 x 160 (40 x 40 face)",
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "First-cracking strength (MPa)": f0, "Tensile strength (MPa)": fu,
              "Tensile strain capacity (%)": eps, "Source table/page": "Table 3 (mix), Table 2 (PVA), Tables 4-6 and 8 (tensile), sect. 3.1-3.2 text (fc)",
              "Conversions / notes": f"{nm}. Ratios to B = cement + FA (FA/B 0.7, SP/B 0.01, HPMC/B 0.0005). Sand = Yellow River silt (natural fine material, VERIFY as sand; S/B {sb}). "
                                     "Strain = ultimate tensile strain (end of strain hardening, peak values)." + extra})
    r.update(fib)
    if nm == "REC":
        r["Conversions / notes"] += " Sand = Yellow River silt."
    rows.append(r)
# QS-ECC: fine quartz sand instead of silt
r = dict(P)
r.update({"OPC / Cement": r4(1 / 1.7), "FA (Fly ash)": r4(0.7 / 1.7), "W / B": 0.30, "SS / B (Silica sand)": 0.375, "SP / B": 0.01,
          "HPMC / B (hydroxypropyl methyl cellulose)": 0.0005, "PVA fiber (vol%)": 2, "Total fiber (vol%)": 2, "Sand max size (µm)": 212,
          "Curing method": "24 h under polyethylene film, demoulded, standard curing room 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
          "Test age (days)": 28, "Compressive specimen": "prism", "Compressive specimen size (mm)": "40 x 40 x 160 (40 x 40 face)",
          "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Compressive strength (MPa)": 21.8, "First-cracking strength (MPa)": 2.14,
          "Tensile strength (MPa)": 2.42, "Tensile strain capacity (%)": 2.16,
          "Source table/page": "Table 3 note (QS-ECC), Table 8 (tensile), sect. 3.2 text (fc)",
          "Conversions / notes": "QS-ECC: quartz sand 180-212 um (silica sand) instead of silt, otherwise as W0 (WW PVA fibre). Mix 'similar to W0' per text, S/B 0.375 assumed (VERIFY)."})
r.update(WW)
rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e36.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
