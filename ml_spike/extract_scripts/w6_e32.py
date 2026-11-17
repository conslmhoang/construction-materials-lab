"""Wave 6, agent e32: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e32.csv (99-column TEMPLATE header).
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


# ---------- jobe.2022.104552 Liao et al.: seawater sea-sand ECC, PE fibre
P = {"Article Name": "Mechanical behaviors and failure criteria of seawater sea-sand engineered cementitious composites under combined tension and shear",
     "Author": "Qiao Liao, Jiangtao Yu, Tianchen Shi, Yuanrui Su", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.jobe.2022.104552"}
Bs = 1 + .14 + .21 + 1.07
for nm, w, fc, eps, ts in [("SS-ECC-0.18", .44, 57.13, 5.65, 7.52), ("SS-ECC-0.21", .51, None, 8.3, 5.76), ("SS-ECC-0.27", .65, 42.14, 7.67, 5.84)]:
    add_row(P, {"OPC / Cement": r4(1 / Bs), "Limestone powder": r4(.14 / Bs), "SF (Silica fume)": r4(.21 / Bs), "GGBS": r4(1.07 / Bs),
                "W / B": r4(w / Bs), "Sea sand / B": r4(1.04 / Bs), "HRWR / B": r4(.015 / Bs), "PE fiber (vol%)": 1.5, "PE length (mm)": 18,
                "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 1.5,
                "Curing method": "demoulded after 48 h, cured in air 28 d", "Curing time (days)": 28, "Demolding age (days)": 2,
                "Test age (days)": 30, "Tensile test type": DIRECT, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
                "Compressive strength (MPa)": fc, "Source table/page": "Table 1 (mix, weight ratios), Table 4 (tensile), sect. 3.2 text (fc)",
                "Conversions / notes": f"{nm}. Weight ratios relative to cement = 1; B = cement + LP + SF + GGBS = 2.42; W/B = water/B (matches mix name). Artificial seawater (30 permille) as mixing water, sea sand as sand. "
                                       "VERIFY: test age 30 d = 48 h demould + 28 d air curing. "
                                       + ("fc not stated in text for this mix (only in Fig. 6)." if fc is None else "fc from text of sect. 3.2 (28 d curing).")})

# ---------- jobe.2022.105747 Shao et al.: steel fibre dry UHPC with HVFA and crumb rubber
P = {"Article Name": "Mechanical behaviour and environmental benefit of eco-friendly steel fibre-reinforced dry UHPC incorporating high-volume fly ash and crumb rubber",
     "Author": "Ruizhe Shao, Chengqing Wu, Jun Li, Zhongxian Liu, Pengtao Wu, Yekai Yang", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.jobe.2022.105747"}
mixes = [("D-FA20", .15, .31, .08, .25, .92, 0, 0, .25, .03, (120.6, 126.8, 134.0, 142.1)),
         ("D-FA30", .18, .55, .09, .30, 1.09, 0, 0, .29, .04, (106.6, 115.2, 125.1, 136.6)),
         ("D-FA40", .22, .89, .11, .36, 1.33, 0, 0, .36, .05, (92.0, 102.3, 115.8, 131.4)),
         ("D-FA50", .29, 1.43, .14, .47, 1.71, 0, 0, .46, .06, (76.7, 87.7, 106.6, 126.7)),
         ("D-FA60", .40, 2.40, .20, .65, 2.40, 0, 0, .65, .08, (56.8, 69.5, 94.7, 110.1))]
cr = [("D-FA50-RC10", 1.71, .47, 0, ((.5, (33.3, 35.1, 43.2, 52.0)), (1.0, (37.7, 40.6, 52.9, 65.7)), (1.5, (44.1, 49.2, 64.6, 81.5)))),
      ("D-FA50-RCM25", 1.01, .47, .70, ((.5, (19.4, 20.5, 26.4, 32.2)), (1.0, (21.3, 22.9, 30.4, 38.4)), (1.5, (24.1, 25.6, 36.3, 45.9)))),
      ("D-FA50-RCM35", .54, .47, 1.17, ((.5, (9.9, 10.4, 13.3, 15.8)), (1.0, (10.9, 12.0, 15.2, 18.2)), (1.5, (12.0, 13.3, 17.9, 22.0))))]
ages = (1, 7, 28, 60)


def dfa(nm, sf, fa, gg, css, mss, ccr, mcr, w, sp, vol, fcs, tab):
    B = 1 + sf + fa + gg
    base = {"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(sf / B), "FA (Fly ash)": r4(fa / B), "GGBS": r4(gg / B), "W / B": r4(w / B),
            "SS / B (Silica sand)": r4((css + mss) / B), "SP / B": r4(sp / B), "Steel fiber (vol%)": vol, "Total fiber (vol%)": vol,
            "Steel length (mm)": 10, "Steel tensile strength (MPa)": 4000, "Curing method": "plastic film 3 h, 50 C moist/steam first day, demoulded, then water at normal temperature until test",
            "Heat curing duration (h)": 24, "Compressive specimen": "cube", "Compressive specimen size (mm)": "40", "Source table/page": f"Table 3 (mix), {tab}"}
    if mcr or ccr:
        base["Crumb rubber / B"] = r4((ccr + mcr) / B)
    for a, fc in zip(ages, fcs):
        add_row(P, dict(base, **{"Curing time (days)": a, "Test age (days)": a, "Compressive strength (MPa)": fc,
                                 "Conversions / notes": f"{nm}, steel fibre {vol} vol%. Weight ratios relative to cement = 1; B = cement + SF + FA + GGBS. Silica sand = coarse + medium fractions. "
                                 "Steel fibre 10 mm, tensile strength >4000 MPa (text). Tensile strain not applicable (compression/flexure only). Moulds covered, curing temp for water stage not stated."}))


for nm, sf, fa, gg, css, mss, ccr, mcr, w, sp, fcs in mixes:
    dfa(nm, sf, fa, gg, css, mss, ccr, mcr, w, sp, 1.5, fcs, "Table 4 (fc)")
for nm, mss, ccr, mcr, lst in cr:
    for vol, fcs in lst:
        dfa(nm + f"-{vol}", .29, 1.43, .14, 0, mss, ccr, mcr, .46, .06, vol, fcs, "Table 7 (fc)")

# ---------- jobe.2023.107254 Gou et al.: EHLECC, only the control EC (no cenosphere / lightweight sand)
P = {"Article Name": "Matrix design and performance development of eco-friendly high-strength, lightweight engineered cementitious composites",
     "Author": "Hongxiang Gou, Massoud Sofi, Zipeng Zhang, Mintao Zhu, Priyan Mendis", "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.jobe.2023.107254"}
B = 750 + 26 + 600
add_row(P, {"OPC / Cement": r4(750 / B), "SF (Silica fume)": r4(26 / B), "FA (Fly ash)": r4(600 / B), "W / B": r4(217.5 / B), "Sand (type not stated) / B": r4(450 / B),
            "SP / B": r4(30 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 21.7, "PE tensile strength (MPa)": 3360,
            "PE elastic modulus (GPa)": 115, "Total fiber (vol%)": 2.0,
            "Curing method": "demoulded 24 h, curing room 20 +/- 2 C RH >= 95 %", "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
            "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
            "First-cracking strength (MPa)": 6.7, "Tensile strength (MPa)": 11.4, "Tensile strain capacity (%)": 6.0,
            "Source table/page": "Table 5 (mix EC, kg/m3), Table 3 (fibre), Table 7 (tensile), sect. 3.2-3.3",
            "Conversions / notes": "Control mix EC only (cenosphere / lightweight-sand mixes skipped). kg/m3 / B (cement + SF + FA = 1376). PE 19.4 kg/m3 -> 2.0 vol% with density 0.97 (VERIFY: derived). "
                                   "VERIFY: tensile test age not stated explicitly; 28 d inferred from text comparing tensile with 28-d compressive. fc of EC only in figure, not entered."})

# ---------- jobe.2023.107277 Wang et al.: recycled fine aggregate ECC, only the natural-sand control N-2-40
P = {"Article Name": "Improvement of mechanical properties and carbonation durability of recycled fine aggregate engineered cementitious composites for structural strengthening",
     "Author": "Xinjie Wang, Yinjia Wu, Pinghua Zhu, Jiagai Yang, Haichao Li, Fajing Wang, Xiancui Yan", "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.jobe.2023.107277"}
B = 566.23 + 452.99 + 113.25
add_row(P, {"OPC / Cement": r4(566.23 / B), "FA (Fly ash)": r4(452.99 / B), "SF (Silica fume)": r4(113.25 / B), "W / B": r4(339.74 / B),
            "Sand (type not stated) / B": r4(407.70 / B), "HRWR / B": r4(3.40 / B), "Binder content (kg/m³)": round(B, 2),
            "PVA fiber (vol%)": 2.0, "PVA length (mm)": 9, "PVA diameter (µm)": 15, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 38, "Total fiber (vol%)": 2.0,
            "Curing method": "20 C 24 h, demoulded, standard curing room 20 C RH 95 %", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
            "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "First-cracking strength (MPa)": 1.67,
            "Tensile strength (MPa)": 2.60, "Tensile strain capacity (%)": 2.32, "Source table/page": "Table 4 (mix N-2-40), Table 3 (fibre), Table 5 (tensile), sect. 3.3",
            "Conversions / notes": "N-2-40 only (natural fine aggregate NFA, 2 vol% PVA, FA 40 %). Recycled-fine-aggregate mixes skipped (RFA not in the 21 materials). kg/m3 / B (cement + FA + SF = 1132.47). "
                                   "Fiber 18.2 kg/m3 = 2 vol% (density 0.91). fc not reported in text/tables."})

# ---------- jobe.2023.107835 Abdellatief et al.: UHPC (cement) reference mixes with steel fibre
P = {"Article Name": "Ultra-high performance concrete versus ultra-high performance geopolymer concrete: Mechanical performance, microstructure, and ecological assessment",
     "Author": "Mohamed Abdellatief, Mohamed Abd Elrahman, Aref A. Abadel, Muhammad Wasim, Ahmed Tahwia", "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.jobe.2023.107835"}
for nm, gg, fa, fc in [("UHPC2F3", 100, 0, 154), ("UHPC4F3", 0, 100, 156)]:
    B = 900 + gg + fa + 137
    d = {"OPC / Cement": r4(900 / B), "SF (Silica fume)": r4(137 / B), "W / B": r4(167 / B), "SS / B (Silica sand)": r4(903 / B), "SP / B": r4(23 / B),
         "Binder content (kg/m³)": B, "Steel fiber (vol%)": 3.0, "Steel length (mm)": 13, "Steel diameter (µm)": 400, "Steel tensile strength (MPa)": 1950, "Steel elastic modulus (GPa)": 205,
         "Total fiber (vol%)": 3.0, "Curing method": "demoulded after 24 h, water pool 25 +/- 2 C RH > 95 %", "Curing time (days)": 28, "Curing temperature (°C)": 25, "Curing RH (%)": 95,
         "Demolding age (days)": 1, "Test age (days)": 28, "Compressive strength (MPa)": fc, "Source table/page": "Table 2 (mix, kg/m3), Table 4 (fc 28 d)",
         "Conversions / notes": f"{nm}. UHPC (cement) mixes only; geopolymer mixes skipped (KOH activator). kg/m3 / B (cement + {'GGBS' if gg else 'FA'} + SF = {B}). "
                                "VERIFY: SF 137 kg/m3 taken from the UHPC1F0 row (cells merged for the F3 rows). Steel 234 kg/m3 = 3 vol% as stated. Quartz sand used as sand. Cube size not stated. Flexural/splitting only otherwise."}
    if gg:
        d["GGBS"] = r4(gg / B)
    else:
        d["FA (Fly ash)"] = r4(fa / B)
    add_row(P, d)

# ---------- jobe.2024.109987 Lin et al.: seawater sea-sand ECC (PVA), C30 / C40 / C50
P = {"Article Name": "Mechanical properties, micro-mechanisms, and constitutive models of seawater sea-sand engineered cementitious composites",
     "Author": "Chenlong Lin, Dongming Huang, Zhenzhen Liu, Yiyan Lu", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.jobe.2024.109987"}
for nm, c, fa, g, ss, w, hr, fcp, scr, smax, eps in [("C30", 338.89, 847.23, 135.56, 475.80, 488.83, 1.72, 27.91, 1.76, 3.54, 2.88),
                                                     ("C40", 498.74, 723.18, 99.75, 440.51, 452.61, 1.98, 36.85, 2.64, 5.20, 3.42),
                                                     ("C50", 1133.79, 170.07, 56.69, 453.47, 465.92, 2.31, 44.94, 2.76, 4.18, 1.27)]:
    B = c + fa + g
    add_row(P, {"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "GGBS": r4(g / B), "W / B": r4(w / B), "Sea sand / B": r4(ss / B), "HRWR / B": r4(hr / B),
                "Binder content (kg/m³)": round(B, 2), "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1550,
                "PVA elastic modulus (GPa)": 36, "Total fiber (vol%)": 2.0, "Curing method": "demoulded after 1 d, standard curing 20 +/- 2 C RH >= 95 %",
                "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
                "Compressive specimen": "prism", "Compressive specimen size (mm)": "100x100x300", "Tensile test type": DIRECT, "Compressive strength (MPa)": fcp,
                "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": smax, "Tensile strain capacity (%)": eps,
                "Source table/page": "Table 3 (mix, kg/m3), Table 2 (fibre), Table 4 (fcp), Table 6 (tensile, averages of 3)",
                "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA + GBFS = {round(B, 2)}). Seawater (34 permille, tap water + sea salt) as mixing water, sea sand as sand. PVA 26 kg/m3 = 2 vol% (density 1.3). "
                                       "fc = prism axial compressive strength fcp (100x100x300 prism, not a cube). Tensile specimen shape not checked."})

# ---------- jobe.2024.110272 Zhang et al.: HS-ECC with iron sand; only the silica-sand mixes
P = {"Article Name": "Development of high-strength engineered cementitious composites using iron sand: Mechanical and shrinkage properties",
     "Author": "Zhi Zhang, Ajad Shrestha, Ziwei Cai, Nauman Ahmad, Kequan Yu, Lingzhi Li", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.jobe.2024.110272"}
Bs = 1 + 1.1 + .2
for nm, ag, scr, smax, eps in [("SS2-F", .5, 3.8, 11.3, 7.19), ("SS4-F", .9, 4.5, 12.3, 6.08), ("SS6-F", 1.4, 3.6, 11.8, 7.42)]:
    add_row(P, {"OPC / Cement": r4(1 / Bs), "GGBS": r4(1.1 / Bs), "SF (Silica fume)": r4(.2 / Bs), "W / B": r4(.4 / Bs), "SS / B (Silica sand)": r4(ag / Bs),
                "Sand max size (µm)": 180, "PE fiber (vol%)": 1.8, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
                "Total fiber (vol%)": 1.8, "Curing method": "20 +/- 5 C, RH 95 % for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
                "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": smax,
                "Tensile strain capacity (%)": eps, "Source table/page": "Table 4 (mix, mass ratios), Table 5 (tensile averages), sect. 2.2, 2.4.3",
                "Conversions / notes": f"{nm}. Silica sand 0.125-0.180 mm only (iron-sand mixes skipped). Mass ratios OPC : GGBS : SF = 1 : 1.1 : 0.2, B = 2.3; water 0.4 and aggregate {ag} on the same basis "
                                       "(consistent with listed s/b 0.2/0.4/0.6). HRWR dosage given as 10 g/L (not convertible), SP/B left empty. fc only in figures, not entered."})

# ---------- jobe.2024.111282 Liu et al.: ECC with extracted titanium tailing slag, control T0 only
P = {"Article Name": "Microstructure and mechanical properties of engineered cementitious composites (ECC) with recycling extracted titanium tailing slag (ETTS)",
     "Author": "Dawei Liu, Zhigang Zhang, Shuping Wang, Jamal A. Abdalla, Rami A. Hawileh, Jingxiong Zhong, Guanwu Zeng", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.jobe.2024.111282"}
B = 714.4 + 451.2 + 91.0 + 184.5
add_row(P, {"OPC / Cement": r4(714.4 / B), "FA (Fly ash)": r4(451.2 / B), "SF (Silica fume)": r4(91.0 / B), "Limestone powder": r4(184.5 / B), "W / B": r4(270 / B),
            "SS / B (Silica sand)": r4(451 / B), "SP / B": r4(20 / B), "Binder content (kg/m³)": round(B, 1), "PE fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
            "Curing method": "covered 24 h, demoulded, air curing 25 +/- 3 C RH 55 +/- 5 % until 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 25, "Curing RH (%)": 55,
            "Demolding age (days)": 1, "Test age (days)": 28, "Tensile test type": DIRECT, "First-cracking strength (MPa)": 8.11, "Tensile strength (MPa)": 10.54,
            "Tensile strain capacity (%)": 2.81, "Source table/page": "Table 2 (mix T0, kg/m3), Table 4 (tensile), sect. 2.3",
            "Conversions / notes": f"Control T0 only (ETTS mixes skipped, ETTS not in the 21 materials). kg/m3 / B (C + FA + SF + LP = {round(B, 1)}). Limestone powder as stated 'LP'. "
                                   "VERIFY: tensile specimen shape / gauge not read; fc not in table."})

# ---------- jobe.2025.112277 Yao et al.: LC3-based low-carbon ECC with different fine aggregates
P = {"Article Name": "Investigation on mechanical properties, pore distribution and crack evolution impact of high ductility low carbon engineered cementitious composites (LCECC) using different eco-friendly aggregates",
     "Author": "Qiyao Yao, Danni Luo, Xiaodan Teng", "Year": 2025, "DOI / URL": "https://doi.org/10.1016/j.jobe.2025.112277"}
Bb = 1 + .67 + .33 + .4 + .8 + .15
t5 = [("LCECC-CR-0.15", "CR", 2.50, 4.15, 6.60), ("LCECC-CR-0.30", "CR", 2.30, 4.80, 13.81), ("LCECC-CR-0.60", "CR", 2.49, 4.01, 8.91),
      ("LCECC-RS-0.60", "RS", 3.41, 8.29, 6.78), ("LCECC-RS-1.18", "RS", 4.49, 7.46, 5.33), ("LCECC-RS-2.36", "RS", 3.53, 8.44, 6.83),
      ("LCECC-AS-0.60", "AS", 3.19, 7.47, 4.39), ("LCECC-AS-1.18", "AS", 3.10, 6.39, 4.27), ("LCECC-AS-2.36", "AS", 2.68, 5.43, 3.50),
      ("LCECC-SS-1.18", "SS", 3.21, 6.81, 6.81), ("LCECC-MS", "MS", 4.46, 8.32, 5.27)]
for nm, ag, scr, smax, eps in t5:
    d = {"OPC / Cement": r4(1 / Bb), "Metakaolin": r4(.67 / Bb), "Limestone powder": r4(.33 / Bb), "FA (Fly ash)": r4(.4 / Bb), "GGBS": r4(.8 / Bb), "SF (Silica fume)": r4(.15 / Bb),
         "W / B": .18, "SP / B": 0.05 if ag == "CR" else 0.035, "PE fiber (vol%)": 1.8, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
         "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 1.8, "Curing method": "demoulded after 24 h, standard curing 20 +/- 1 C RH > 90 % for 28 d",
         "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone",
         "Tensile test type": DIRECT, "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": smax, "Tensile strain capacity (%)": eps,
         "Source table/page": "Table 3 (mix, mass ratios), Table 2 (fibre), Table 5 (tensile at 28 d), sect. 2.2",
         "Conversions / notes": f"{nm}. Binder mass ratios OPC 1 : MK 0.67 : LS 0.33 : FA 0.4 : GGBS 0.8 : SF 0.15 (B = 3.35; LC3 = OPC + MK + LS), converted to fractions of B. "
                                "S/B 0.36, W/B 0.18 (as stated). SP 3.5 wt % (5.0 wt % for CR mixes), taken as wt % of binder (VERIFY basis). "}
    s = .36 / Bb * Bb  # S/B stated = 0.36
    if ag == "RS":
        d["River sand / B"] = .36
    elif ag == "AS":
        d["M-sand / B"] = .36
        d["Conversions / notes"] += "Artificial (manufactured) sand. "
    elif ag == "SS":
        d["Sea sand / B"] = .36
    elif ag == "MS":
        d["SS / B (Silica sand)"] = .36
        d["Conversions / notes"] += "Microsilica sand (Dmax 0.30 mm). "
    else:
        d["Sea sand / B"] = r4(.36 * .6)
        d["Crumb rubber / B"] = r4(.36 * .4)
        d["Conversions / notes"] += "Crumb rubber replaces 40 wt % of the sea sand (VERIFY: split 0.216 sea sand + 0.144 CR assumed from the 40 % weight replacement). "
    d["Conversions / notes"] += "Aggregate size in the mix name = Dmax (mm). fc only in figure, not entered."
    add_row(P, d)

# ---------- jobe.2026.117313 Yu et al.: HS-ECC at elevated temperatures; keep the 25 C reference fc only
P = {"Article Name": "Elevated-temperature mechanical performance and spalling behavior of high strength ECC with varying strength levels: insights from micromechanics and direct pore-vapor-pressure measurements",
     "Author": "Jianqiao Yu, Rami A. Hawileh, Jamal A. Abdalla, Zhigang Zhang", "Year": 2026, "DOI / URL": "https://doi.org/10.1016/j.jobe.2026.117313"}
for nm, c, fa, sf, ss, w, sp, fc in [("C90", 717, 574, 115, 422, 281, 20, 94.87), ("C80", 582, 698, 112, 418, 278, 20, 80.49),
                                      ("C70", 489, 783, 111, 415, 276, 20, 76.65), ("C60", 422, 844, 110, 413, 275, 25, 65.84)]:
    B = c + fa + sf
    add_row(P, {"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(ss / B), "SP / B": r4(sp / B),
                "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0,
                "Curing method": "sealed with plastic film, demoulded after 24 h, then ~25 C RH 55 % until test", "Curing time (days)": 28, "Curing temperature (°C)": 25, "Curing RH (%)": 55,
                "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200", "Compressive strength (MPa)": fc,
                "Source table/page": "Table 2 (mix, kg/m3), Table 4 (fc at 25 C), sect. 2.1-2.2",
                "Conversions / notes": f"{nm}. 25 C reference only (heated specimens skipped). kg/m3 / B (cement + ultra-fine FA + SF = {B}). PE 19.4 kg/m3 -> 2.0 vol% with density 0.97 (VERIFY: derived). "
                                       "Tensile strain at 25 C only in figures, not entered."})

# ---------- jobe.2026.117803 Han et al.: steel-fibre UHPC, quasi-static fc only (dynamic tests skipped)
P = {"Article Name": "Multi-Scale Damage Mechanism of Reinforced UHPC by Steel Fibers Under Dynamic Compressive Loads",
     "Author": "Heng Han, Zhen Liu, Zhenqiang Zhao, Hang Dong, Qinshi Hu, Yan Li, Chao Zhang, Yulong Li", "Year": 2026, "DOI / URL": "https://doi.org/10.1016/j.jobe.2026.117803"}
B = 740 + 284 + 181
for nm, sfk, vol, fc in [("SF1", 78, 1.0, 127.99), ("SF2", 156, 2.0, 128.13), ("SF3", 234, 3.0, 124.28)]:
    add_row(P, {"OPC / Cement": r4(740 / B), "FA (Fly ash)": r4(284 / B), "SF (Silica fume)": r4(181 / B), "W / B": r4(217 / B), "SS / B (Silica sand)": r4(1446 / B), "SP / B": r4(30 / B),
                "Binder content (kg/m³)": B, "Steel fiber (vol%)": vol, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850, "Total fiber (vol%)": vol,
                "Curing method": "demoulded after 1 d, water curing 20 C until 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28,
                "Compressive specimen": "cylinder (cut)", "Compressive specimen size (mm)": "50x98", "Compressive strength (MPa)": fc,
                "Source table/page": "Table 3 (mix, kg/m3), Table 2 (fibre), Table 4 (quasi-static strength), sect. 2.2-2.4",
                "Conversions / notes": f"{nm}. Quasi-static fc only (dynamic SHPB results skipped). kg/m3 / B (cement + FA + SF = {B}). Quartz sand used as sand. Steel {sfk} kg/m3 = {vol} vol% as stated (density 7800)."})

# ---------- jobe.2023.107636 Wu et al.: ECC-I/II/III (ECC properties listed in Table 7)
P = {"Article Name": "Shear behaviors of engineered cementitious composites to seawater sea-sand concrete (ECC-to-SSSC) interfaces cast using 3D-printed pre-grooving formwork: Mechanical properties, characterization",
     "Author": "Xiaowei Wu, Jingwen He, Jun Tian, Xiao Tan, Shaowei Hu, Yu Zheng, Wen-Wei Wang, Weiguo Zhang", "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.jobe.2023.107636"}
B = 264.48 + 1057.92
for nm, w, hr, fc, ts, eps in [("ECC-I", 420.0, 3.10, 39.1, 6.31, 5.80), ("ECC-II", 370.0, 4.30, 50.7, 6.79, 8.30), ("ECC-III", 343.8, 9.00, 59.7, 8.06, 6.60)]:
    add_row(P, {"OPC / Cement": r4(264.48 / B), "FA (Fly ash)": r4(1057.92 / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(396.8 / B), "HRWR / B": r4(hr / B),
                "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.06, "PE length (mm)": 18, "PE diameter (µm)": 25, "Total fiber (vol%)": 2.06,
                "Curing method": "poured, cured 28 d under standard curing conditions (T / RH not given)", "Curing time (days)": 28, "Test age (days)": 28,
                "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
                "Source table/page": "Table 4 (mix, kg/m3), Table 5 (fibre), Table 7 (ECC fc / tensile / strain at 28 d)",
                "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA = {B}); W/B computed from water {w} (paper names 0.32 / 0.28 / 0.26). PE fibre 2.06 vol% of ECC volume as stated. "
                                       "Specimens (dog-bone ECC tensile and fc) are the ECC part of the interface shear study; standard curing T/RH not specified."})

# ---------- matpr.2023.03.071 Sushma, Nanditha: SHCC (PVA) with GGBS replacing part of fly ash
P = {"Article Name": "Development of strain hardening cement based composite for concrete retrofitting purposes",
     "Author": "Pallati Sushma, M. Nanditha", "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.matpr.2023.03.071"}
fcs = {(10, 0): 21.72, (10, 55): 22.59, (10, 110): 22.76, (10, 165): 24.66, (15, 0): 27.74, (15, 55): 28.12, (15, 110): 28.93, (15, 165): 29.2}
for (pva, gg), fc in fcs.items():
    fa = 550 - gg
    B = 500 + fa + gg
    vol = round(pva / 1300 * 100, 3)
    d = {"OPC / Cement": r4(500 / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(390 / B), "River sand / B": r4(500 / B), "SP / B": r4(5 / B), "Binder content (kg/m³)": B,
         "PVA fiber (vol%)": vol, "PVA length (mm)": 12, "PVA diameter (µm)": 38, "PVA tensile strength (MPa)": 1600, "Total fiber (vol%)": vol,
         "Curing method": "28 d curing (conditions not stated)", "Curing time (days)": 28, "Test age (days)": 28, "Compressive strength (MPa)": fc,
         "Source table/page": "Table 7 (mix, kg/m3), Table 8 (fc 28 d), Table 6 (fibre)",
         "Conversions / notes": f"VERIFY: PVA {pva} kg/m3 -> {vol} vol% with density 1.3 (paper says 2 % / 3 % of cement mass). kg/m3 / B (cement + FA + GGBS = {B}); "
                                f"W/B = 390/{B} (paper quotes w/c 0.39). GGBS {gg} kg/m3 replaces fly ash. Godavari river sand. Table 10 tensile strengths not entered (test type unclear, probably not direct). "
                                "Mix named C-1 (10 kg/m3 PVA) / C-2 (15 kg/m3)."}
    if gg:
        d["GGBS"] = r4(gg / B)
    add_row(P, d)

# ---------- rineng.2025.106159 Mahmoudi et al.: PE-ECC G40 / G60, ambient (25 C) reference only
P = {"Article Name": "Mechanical properties of GGBS-based polyethylene engineered cementitious composite (PE-ECC) at elevated temperature",
     "Author": "Fardin Mahmoudi, Jamal A. Abdalla, Rami A. Hawileh", "Year": 2025, "DOI / URL": "https://doi.org/10.1016/j.rineng.2025.106159"}
for nm, c, g, fc, scr, smax, eps, ne in [("G40", 888, 592, 71.3, 3.98, 7.64, 1.08, "average strain 1.08 % quoted in text (samples 1.45 / 0.72)"),
                                         ("G60", 592, 888, 57.0, 4.13, 6.24, 4.945, "VERIFY: strain = mean of the two samples in Table 7 (6.21, 3.68)")]:
    B = c + g + 125
    add_row(P, {"OPC / Cement": r4(c / B), "GGBS": r4(g / B), "SF (Silica fume)": r4(125 / B), "W / B": r4(294 / B), "Sand (type not stated) / B": r4(440 / B), "SP / B": r4(25 / B),
                "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.06, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 116,
                "Total fiber (vol%)": 2.06, "Curing method": "covered with plastic 24 h, demoulded, air-cured 365 d in laboratory 23 +/- 2 C", "Curing time (days)": 365,
                "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": 366, "Compressive specimen": "cube", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
                "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": smax, "Tensile strain capacity (%)": eps,
                "Source table/page": "Table 1 (mix, g/l = kg/m3), Table 3 (fibre), Table 5 (fc 25 C), Table 6-7 and sect. 4.3 (tensile 25 C)",
                "Conversions / notes": f"{nm}. 25 C (unheated) reference only. kg/m3 / B (cement + GGBS + SF = {B}). PE 20 kg/m3 -> 2.06 vol% with density 0.97 (VERIFY: derived). "
                                       f"VERIFY: test age 366 d = 1 d + 365 d air curing (text: 'air-cured for 365 curing days'). Strain: {ne}. Cube size not read."})

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e32.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
