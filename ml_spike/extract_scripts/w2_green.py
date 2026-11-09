"""Builder for w2_green.csv - green / low-carbon ECC (LC3, slag, recycled powders, MSWI, cenospheres, HVFA).
All values transcribed from the papers' full text (Europe PMC fullTextXML / Frontiers HTML).
Run: python w2_green.py  (writes ../additions/w2_green.csv, UTF-8 with BOM)
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "additions")
H = list(pd.read_csv(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
assert len(H) == 99
rows = []


def R(x, n=4):
    return round(x, n)


def add(base, **kw):
    r = dict(base)
    r.update({k: v for k, v in kw.items() if v is not None})
    for k in r:
        assert k in H, k
    rows.append(r)


# ---------------------------------------------------------------- 1 Jiang et al. 2026 LC3-ECC (PVA / PE / PP)
B = 1320.0
base = {"Article Name": "Multi-Dimensional Assessment of Low-Carbon Engineering Cement-Based Composites Based on Rheological, Mechanical and Sustainability Factors",
        "Author": "Jiang Z., Zhu Z., Fang D., Fu C., Li S., Jing Y.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19020424",
        "SS / B (Silica sand)": R(404 / B), "Sand max size (µm)": 212, "Binder content (kg/m³)": B,
        "Curing method": "demoulded 24 h, standard curing 20±3 °C, RH >95%", "Curing time (days)": 28, "Curing temperature (°C)": 20,
        "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
        "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160",
        "Tensile specimen": "dog-bone (Fig. 1)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
PVA = {"PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1833, "PVA elastic modulus (GPa)": 41}
PE = {"PE length (mm)": 12, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 3100, "PE elastic modulus (GPa)": 122}
PP = {"PP length (mm)": 12, "PP diameter (µm)": 48}
water = {"W22": 297, "W25": 330, "W27": 363, "W30": 396}
# (group, first-crack, ultimate, strain %, source table)
jiang = [("O-W22S60-A", 6.08, 7.87, 0.97, "Table 4"), ("L-W22S60-E", 5.21, 8.17, 3.70, "Table 4/6"), ("L-W22S60-P", 3.33, 3.33, 0.03, "Table 4/6"),
         ("O-W25S40-A", 3.94, 6.71, 1.24, "Table 4/5"), ("L-W25S40-A", 3.10, 7.28, 2.00, "Table 4/6"), ("L-W25S40-E", 4.60, 8.59, 6.04, "Table 4/5/6"),
         ("L-W25S40-P", 2.68, 2.68, 0.01, "Table 4/5/6"), ("O-W27S30-A", 7.13, 8.40, 0.95, "Table 4"), ("L-W27S30-A", 4.74, 7.18, 1.74, "Table 4/6"),
         ("L-W27S30-E", 4.41, 7.89, 7.78, "Table 4/6"), ("L-W27S30-P", 2.77, 2.77, 0.03, "Table 4/6"), ("O-W30S20-A", 4.88, 7.09, 1.14, "Table 4"),
         ("L-W30S20-A", 5.26, 6.29, 4.20, "Table 4/6"), ("L-W30S20-P", 3.10, 3.10, 0.02, "Table 4/6"),
         ("O-W25S35-A", 6.15, 8.17, 1.13, "Table 5"), ("O-W25S45-A", 4.98, 5.68, 0.95, "Table 5"), ("L-W25S35-A", 4.37, 6.76, 4.47, "Table 5"),
         ("L-W25S45-A", 3.85, 4.88, 2.42, "Table 5"), ("L-W25S35-E", 6.48, 8.36, 4.39, "Table 5"), ("L-W25S45-E", 5.96, 7.94, 8.40, "Table 5"),
         ("L-W25S35-P", 3.05, 3.05, 0.01, "Table 5"), ("L-W25S45-P", 3.57, 3.57, 0.03, "Table 5"),
         ("L-W22S60-E1.5P", 4.32, 7.14, 5.48, "Table 6"), ("L-W22S60-E1.0P", 3.85, 4.55, 2.76, "Table 6"), ("L-W22S60-E0.5P", 3.52, 3.52, 1.37, "Table 6"),
         ("L-W25S40-E1.5P", 3.85, 6.39, 5.79, "Table 6"), ("L-W25S40-E1.0P", 4.74, 4.74, 1.71, "Table 6"), ("L-W25S40-E0.5P", 3.90, 3.90, 0.02, "Table 6"),
         ("L-W27S30-E1.5P", 2.39, 5.68, 3.82, "Table 6"), ("L-W27S30-E1.0P", 2.21, 4.37, 1.62, "Table 6"), ("L-W27S30-E0.5P", 2.68, 2.68, 0.88, "Table 6"),
         ("L-W25S40-A1.5P", 2.91, 5.63, 0.54, "Table 6"), ("L-W25S40-A1.0P", 2.96, 3.10, 0.24, "Table 6"), ("L-W25S40-A0.5P", 1.64, 1.83, 0.19, "Table 6"),
         ("L-W27S30-A1.5P", 4.46, 4.88, 0.32, "Table 6"), ("L-W27S30-A1.0P", 3.85, 4.46, 0.36, "Table 6"), ("L-W27S30-A0.5P", 2.30, 2.30, 0.37, "Table 6"),
         ("L-W30S20-A1.5P", 3.33, 5.49, 1.40, "Table 6"), ("L-W30S20-A1.0P", 2.54, 4.08, 1.63, "Table 6"), ("L-W30S20-A0.5P", 3.24, 3.24, 0.03, "Table 6")]
for g, fcr, ftu, eps, src in jiang:
    mat, ws, fib = g.split("-")
    w = ws[:3]
    sp = float(ws[4:]) / 100 / 100  # S40 = 0.40 % of binder
    if mat == "O":
        bind = {"OPC / Cement": R(600 / B), "FA (Fly ash)": R(720 / B)}
        bnote = "OPC matrix: PC 600 + FA 720 kg/m3"
    else:
        bind = {"OPC / Cement": R(330 / B), "FA (Fly ash)": R(720 / B), "Metakaolin": R(180 / B), "Limestone powder": R(90 / B)}
        bnote = "LC3 matrix: PC 330 + FA 720 + MK 180 + LS 90 kg/m3 (LC3 = PC+MK+LS)"
    main = fib[0]
    if "P" in fib[1:] or fib == "P":
        pp = 2.0 if fib == "P" else 2.0 - float(fib[1:-1])
    else:
        pp = 0.0
    mainv = 0.0 if fib == "P" else 2.0 - pp
    d = dict(bind)
    d.update({"W / B": R(water[w] / B), "SP / B": R(sp, 5), "Total fiber (vol%)": 2.0,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ftu, "Tensile strain capacity (%)": eps,
              "Source table/page": f"Table 2 (fibre), Table 3 (mix, kg/m3), {src} (tension)"})
    if fib != "P":
        if main == "A":
            d.update(PVA); d["PVA fiber (vol%)"] = mainv
        else:
            d.update(PE); d["PE fiber (vol%)"] = mainv
    if pp:
        d.update(PP); d["PP fiber (vol%)"] = pp
    extra = ""
    if g == "L-W25S40-A":
        extra = " Initial crack strength 3.10 in Tables 4/6 but 3.15 in Table 5 (paper inconsistency); 3.10 used."
    if fcr == ftu:
        extra += " First-crack = ultimate (no strain hardening)."
    d["Conversions / notes"] = (f"{g}: {bnote}, binder 1320 kg/m3; QS 404 kg/m3 (70-110 mesh, max taken as 212 µm); water {water[w]} kg/m3; "
                                f"SP {sp*100:.2f}% of binder (Table 3 'SP (%)'). Fibres: A=PVA (1.3 g/cm3), E=PE ZTD25 (0.97), P=PP (0.92, 580 MPa, 4.7 GPa) - "
                                f"PP strength/modulus not in template. Total fibre 2 vol%. Compressive strength only in Figs 5-7 (not filled).{extra}")
    add(base, **d)

# ---------------------------------------------------------------- 2 Gong et al. 2022 LC3 + PE
base = {"Article Name": "Multiscale Investigation on the Performance of Engineered Cementitious Composites Incorporating PE Fiber and Limstone Calcined Clay Cement (LC3)",
        "Author": "Gong G., Guo M., Zhou Y., Zheng S., Hu B., Zhu Z., Huang Z.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/polym14071291",
        "PE fiber (vol%)": R(20 / 970 * 100, 2), "Total fiber (vol%)": R(20 / 970 * 100, 2), "PE length (mm)": 18, "PE diameter (µm)": 25,
        "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
        "Curing method": "demoulded 24 h, standard curing room 23±3 °C, RH 95%", "Curing time (days)": 28, "Curing temperature (°C)": 23,
        "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
        "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
for name, c, cc, gy, ls, hr, ft, eps in [("ECC-LC3-35", 905, 304, 21, 152, 13, 9.55, None), ("ECC-LC3-50", 732, 415, 28, 207, 18, None, 8.53)]:
    b = c + cc + gy + ls
    add(base, **{"OPC / Cement": R(c / b), "Metakaolin": R(cc / b), "Other binder": R(gy / b), "Limestone powder": R(ls / b),
                 "W / B": R(345 / b), "SS / B (Silica sand)": R(500 / b), "HRWR / B": R(hr / b, 5), "Binder content (kg/m³)": b,
                 "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                 "Source table/page": "Table 1 (mix, kg/m3), Table 3 (fibre), Sec. 5.2 text (tension)",
                 "Conversions / notes": (f"{name}: kg/m3 / binder {b} (OPC 52.5R + calcined clay + gypsum + limestone). Calcined clay from kaolin tailings "
                                         f"(Al2O3 39%, contains quartz/illite) recorded as Metakaolin; gypsum ({gy} kg/m3) in Other binder. PE 20 kg/m3 / 970 = 2.06 vol%. "
                                         "Only one tensile value per mix is given numerically in text (sigma_tu 9.55 MPa for LC3-35, eps_tu 8.53% for LC3-50); "
                                         "other tensile values and all fc (3/7/28 d) only in Figs 9-12. OPC reference mix not included (no numeric values).")})

# ---------------------------------------------------------------- 3 Zhou et al. 2023 LC3 + recycled fine aggregate + PE
base = {"Article Name": "Development of Sustainable Engineered Cementitious Composites by Incorporating Local Recycled Fine Aggregate",
        "Author": "Zhou Y., Guo W., Zheng S., Xing F., Guo M., Zhu Z.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/polym15122701",
        "PE fiber (vol%)": R(20 / 970 * 100, 2), "Total fiber (vol%)": R(20 / 970 * 100, 2), "PE length (mm)": 18, "PE diameter (µm)": 25,
        "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116, "Demolding age (days)": 1,
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
        "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
zmix = {"R-PC": (1382, 0, 0, 0, 9), "R-LC3-35": (905, 304, 21, 152, 17), "R-LC3-50": (732, 415, 28, 207, 25)}
zres = [("R-PC", 28, 48.2, 5.67, 7.28, 5.5, "fc derived: 55.07/1.142 = 48.22 and 54.13/1.123 = 48.20 (text gives LC3 values as +14.2%/+12.3% vs PC)."),
        ("R-LC3-35", 28, 55.07, 5.89, 10.40, 8.48, ""), ("R-LC3-50", 28, 54.13, 5.51, 9.86, 8.78, ""),
        ("R-PC", 150, 48.9, None, None, None, "fc derived: 56.13/1.147 = 48.94 and 63.08/1.289 = 48.94."),
        ("R-LC3-35", 150, 56.13, None, None, None, ""), ("R-LC3-50", 150, 63.08, None, None, None, "")]
for name, age, fc, fcr, ft, eps, nn in zres:
    c, cc, gy, ls, hr = zmix[name]
    b = c + cc + gy + ls
    d = {"OPC / Cement": R(c / b), "Metakaolin": R(cc / b) if cc else None, "Other binder": R(gy / b) if gy else None, "Limestone powder": R(ls / b) if ls else None,
         "W / B": R(328 / b), "HRWR / B": R(hr / b, 5), "Binder content (kg/m³)": b, "Test age (days)": age,
         "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
         "Curing method": "demoulded 24 h, curing room 23±3 °C, RH 95% for 28 d" + ("; later conditions to 150 d not stated" if age == 150 else ""),
         "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Curing time (days)": 28 if age == 28 else None,
         "Source table/page": "Table 1 (mix, kg/m3), Table 3 (fibre), Sec. 3.2 text (fc), Sec. 3.3 text (tension)",
         "Conversions / notes": (f"{name} {age} d: kg/m3 / binder {b}. Effective water 328 kg/m3 (paper: effective W/B 0.24). Aggregate = 500 kg/m3 recycled fine "
                                 f"aggregate (RFA/B = {500/b:.4f}, density 2408, absorption 10.2%; no template column). Calcined clay from kaolin tailings recorded as Metakaolin; "
                                 f"gypsum in Other binder. PE 20 kg/m3 / 970 = 2.06 vol%. {nn}" + (" Tensile values at 150 d only in Fig. 8." if age == 150 else ""))}
    if name == "R-PC":
        d.update({"Metakaolin": None, "Other binder": None, "Limestone powder": None})
    add(base, **d)

# ---------------------------------------------------------------- 4 Wang et al. 2019 recycled powder + crumb rubber, PE
base = {"Article Name": "Using Green Supplementary Materials to Achieve More Ductile ECC",
        "Author": "Wang Y., Zhang Z., Yu J., Xiao J., Xu Q.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12060858",
        "OPC / Cement": 0.45, "PE fiber (vol%)": 2, "Total fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 25,
        "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
        "Curing method": "air curing 20±3 °C, RH 40±5%", "Curing time (days)": 27, "Curing temperature (°C)": 20, "Curing RH (%)": 40,
        "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100",
        "Tensile specimen": "dog-bone (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
for name, fa, rp, cr80, cr40, s, w, fcr, ft, eps in [
        ("R5040C13", 0.275, 0.275, 0, 0.04, 0.27, 0.35, 2.22, 4.62, 7.37), ("R5040C30", 0.275, 0.275, 0, 0.08, 0.23, 0.37, 1.97, 4.24, 7.42),
        ("R5080C13", 0.275, 0.275, 0.04, 0, 0.27, 0.40, 2.12, 6.00, 7.45), ("R5080C30", 0.275, 0.275, 0.08, 0, 0.23, 0.36, 1.72, 5.63, 7.68),
        ("R10040C13", 0, 0.55, 0, 0.04, 0.27, 0.34, 2.23, 4.59, 7.71), ("R10040C30", 0, 0.55, 0, 0.08, 0.23, 0.37, 1.72, 4.38, 8.55),
        ("R10080C13", 0, 0.55, 0.04, 0, 0.27, 0.39, 1.96, 5.54, 8.81), ("R10080C30", 0, 0.55, 0.08, 0, 0.23, 0.34, 2.21, 5.07, 12.26)]:
    cr = cr80 or cr40
    size = "80 mesh" if cr80 else "40 mesh"
    add(base, **{"FA (Fly ash)": fa if fa else None, "Recycled powder (C&D waste)": rp, "Crumb rubber / B": cr, "SS / B (Silica sand)": s, "W / B": w,
                 "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                 "Source table/page": "Table 1 (fibre), Table 3 (mix, mass ratio to binder), Table 4 (tension)",
                 "Conversions / notes": (f"{name}-ECC: Table 3 ratios by binder mass (cement 0.45, FA {fa}, recycled C&D powder {rp}, crumb rubber {cr} ({size}), "
                                         f"silica sand {s}, water {w}); PE 0.015 by binder mass = 2 vol% (text). RP avg 45 µm replaces FA. HRWR used, dose not given. "
                                         "Strain = strain at peak stress. fc only in Fig. 11. Curing time = 28 d age minus 1 d in mould.")})

# ---------------------------------------------------------------- 5 Shumuye et al. 2022 slag/FA PE-ECC
B = 1333.2
base = {"Article Name": "Eco-Friendly, High-Ductility Slag/Fly-Ash-Based Engineered Cementitious Composite (ECC) Reinforced with PE Fibers",
        "Author": "Shumuye E.D., Liu J., Li W., Wang Z.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/polym14091760",
        "OPC / Cement": R(533.3 / B), "W / B": R(400 / B), "Sand (type not stated) / B": R(266.6 / B), "HRWR / B": R(4 / B, 5), "Binder content (kg/m³)": B,
        "PE fiber (vol%)": R(15 / 970 * 100, 2), "Total fiber (vol%)": R(15 / 970 * 100, 2), "PE length (mm)": 18, "PE diameter (µm)": 20,
        "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100, "Demolding age (days)": 1,
        "Curing method": "covered with plastic sheet 24 h, then cured (conditions not stated)",
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
        "Tensile specimen": "dog-bone (stated 80 x 30 x 13 mm)", "Tensile test type": "direct"}
sh = {"SF-0-60": (0, 799.9, (2.21, 6.57), (2.25, 5.35), 40.79, 2.0, "fc 40.79 MPa from text (28-d range 40.79-55.05)."),
      "SF-5-55": (66.6, 733.2, (1.42, 4.48), (1.23, 5.20), 42.22, 3.5, "fc derived: 40.79 x 1.035 (text: +3.5% vs SF-0-60)."),
      "SF-10-50": (133.3, 666.6, (1.88, 6.59), (2.51, 5.70), 52.42, 2.9, "fc derived: 40.79 x 1.285 (text: +28.5%)."),
      "SF-15-45": (199.9, 599.9, (1.29, 5.26), (2.57, 5.18), 55.05, None, "fc 55.05 MPa from text (= 40.79 x 1.349, +34.9%).")}
for name, (sl, fa, t7, t28, fc28, eps, nn) in sh.items():
    for age, (fcr, ft) in [(7, t7), (28, t28)]:
        d = {"GGBS": R(sl / B) if sl else None, "FA (Fly ash)": R(fa / B), "Test age (days)": age,
             "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft,
             "Compressive strength (MPa)": fc28 if age == 28 else None,
             "Tensile strain capacity (%)": eps if age == 28 else None,
             "Source table/page": "Table 1 (mix, kg/m3), Table 3 (fibre), Table 4 (tension 7/28 d), Sec. 3.1 text (fc), Sec. 3.2 text (strain)",
             "Conversions / notes": (f"{name} {age} d: kg/m3 / binder {B} (slag + FA + cement 533.3). PE 15 kg/m3 / 970 = 1.55 vol%. Sand type not stated. "
                                     + (nn + " " if age == 28 else "7-d fc only as % in text / Fig. 4. ")
                                     + ("VERIFY: strain read from text 'approximately' (3.5% SF-5-55, ~2.9% SF-10-50, ~2.0% SF-0-60), age assumed 28 d; SF-15-45 only 'similar'. "
                                        if age == 28 else "")
                                     + "Gauge length not stated.")}
        add(base, **d)

# ---------------------------------------------------------------- 6 Dong et al. 2022 MSWI bottom-ash powder ECC
base = {"Article Name": "Study on the Properties of Fiber/Matrix Interface and Strain-Hardening Behavior of ECC Containing Municipal Solid Waste Incineration (MSWI) Powder",
        "Author": "Dong Y., Cheng Y., Lu H.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15144905",
        "SS / B (Silica sand)": 0.36, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
        "PVA tensile strength (MPa)": 3000, "PVA elastic modulus (GPa)": 42,
        "Tensile specimen": "dumbbell 330 x 60 x 13 mm", "Tensile test type": "direct"}
for name, x, w, vf, fcr, ft, eps, nn in [
        ("D1", 1.2, 0.25, 2.0, 3.07, 3.63, 1.0, "Strain 'around 1.0%' (text); no obvious strain hardening per text."),
        ("D5", 4.0, 0.25, 2.0, 1.84, 2.06, 2.0, "fcr/ft 'only around' 1.84/2.06 MPa (text)."),
        ("D6", 2.2, 0.20, 2.0, 2.32, 2.68, None, ""), ("D7", 2.2, 0.30, 2.0, 1.56, 1.78, None, ""),
        ("D8", 2.2, 0.25, 1.5, 1.86, 2.4, None, "No strain hardening (single crack) per text."),
        ("D9", 2.2, 0.25, 2.5, 2.33, 3.0, 2.27, "")]:
    b = 1 + x
    add(base, **{"OPC / Cement": R(1 / b), "Other binder": R(x / b), "W / B": w, "SP / B": 0.02,
                 "PVA fiber (vol%)": vf, "Total fiber (vol%)": vf,
                 "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                 "Source table/page": "Table 3 (fibre), Table 6 (mix), Sec. 3.2 text (tension)",
                 "Conversions / notes": (f"{name}: Table 6 mass ratios cement 1 : MSWI powder {x}; binder = cement + MSWI micropowder (WTQ/BA: water-washed, heat-treated, "
                                         f"ball-milled MSWI bottom ash, per Fig. 8 caption) -> Other binder {x/b:.4f}. Sand/B 0.36 and W/B {w} as printed (text calls it w/c). "
                                         f"Water reducer 0.02 'mass ratio' assumed per binder. Quartz sand ~100 µm (150 mesh). Curing regime and test age not stated. {nn}")})

# ---------------------------------------------------------------- 7 Fu et al. 2022 lightweight green ECC with fly-ash cenospheres
B = 913 + 391.5
base = {"Article Name": "Green-Engineered Cementitious Composite Production with High-Strength Synthetic Fiber and Aggregate Replacement",
        "Author": "Fu C., Chen M., Guo R., Qi R.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15093047",
        "OPC / Cement": R(913 / B), "FA (Fly ash)": R(391.5 / B), "FA cenosphere / B": R(195.8 / B), "W / B": R(251.7 / B), "HRWR / B": R(101.7 / B, 4),
        "Binder content (kg/m³)": B, "PE length (mm)": 12, "PE diameter (µm)": 26, "PE tensile strength (MPa)": 2900,
        "PE elastic modulus (GPa)": 116, "Curing method": "demoulded 1 d, standard curing 20±3 °C, RH 95%", "Curing temperature (°C)": 20,
        "Curing RH (%)": 95, "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
        "Tensile specimen": "dog-bone (Fig. 7a)", "Tensile test type": "direct"}
for vf, fc, ft, eps in [(1, 52.8, 5.6, 2.5), (2, 47.5, 7.2, 5.6)]:
    add(base, **{"PE fiber (vol%)": vf, "Total fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                 "Source table/page": "Table 2 (fibre), Table 3 (mix, kg/m3), Sec. 4.2 text (fc), Sec. 4.4 text (tension)",
                 "Conversions / notes": (f"FAC0.15-PE{vf}: kg/m3 / binder {B} (P.O 52.5 cement 913 + FA 391.5). Fly-ash cenospheres (FACs, 0.01-0.5 mm, 530 kg/m3) "
                                         "are the only aggregate (FAC/B 0.15). WR 101.7 kg/m3 as printed in Table 3. PE diameter 26 µm derived from length 12 mm / aspect ratio 460. "
                                         "Test age not stated. Other FAC0.15/0.30/0.45 mixes only in Figs 12/15.")})

# ---------------------------------------------------------------- 8 Tian et al. 2022 HVFA PE-ECC
B = 592.4 + 710.8
add({"Article Name": "Experimental investigation on seismic performance of plain engineered cementitious composite beams",
     "Author": "Tian L., Tan Y., Wei X.-X., Ouyang L.-J., Xu R., Yu J.-T.", "Year": 2022, "DOI / URL": "https://doi.org/10.3389/fmats.2022.1056809"},
    **{"OPC / Cement": R(592.4 / B), "FA (Fly ash)": R(710.8 / B), "W / B": R(412.7 / B), "Sand (type not stated) / B": R(873.9 / B), "SP / B": R(5.0 / B, 5),
       "Binder content (kg/m³)": R(B, 1), "PE fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900,
       "PE elastic modulus (GPa)": 116, "Tensile test type": "direct",
       "Compressive strength (MPa)": 20.79, "Tensile strength (MPa)": 5.69, "Tensile strain capacity (%)": 10.59,
       "Source table/page": "Table 1 (mix, kg/m3), Table 2 (fibre), Table 3 (properties)",
       "Conversions / notes": (f"ECC mix: kg/m3 / binder {B:.1f} (OPC 52.5 + FA). W/B stated 0.32. PE 19 kg/m3 (= 1.96 vol% at 970) - text states 2.0 vol%. "
                               "Water reducing agent 5.0 kg/m3. Average values; max strain 12.13%. Uniaxial compression (compressive modulus 10.71 GPa). "
                               "Fibre length, specimen geometry, curing and test age not stated.")})

df = pd.DataFrame(rows, columns=H)
out = os.path.join(D, "w2_green.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", out)
