"""Wave 5, agent 'pe': PE / UHMWPE fiber cementitious composites (HS-ECC, UHP-ECC, UHP-SHCC, PE hybrids).
Writes ml_spike/additions_v2/w5_pe.csv (99-column TEMPLATE header).
Every number is from the paper's text/tables; derived values are flagged VERIFY in the notes.
Ratios are per the paper's binder B; build_web_dataset.py re-expresses them per (cement + fly ash + GGBS).
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2"); os.makedirs(out_dir, exist_ok=True)
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []


def meta(title, authors, year, doi):
    return {"Article Name": title, "Author": authors, "Year": year, "DOI / URL": "https://doi.org/" + doi}


def kgm3(binder_parts, others):
    """binder_parts: {col: kg/m3}; others: {col: kg/m3} -> fractions of B and X/B."""
    B = sum(binder_parts.values())
    d = {k: round(v / B, 4) for k, v in binder_parts.items()}
    d.update({k: round(v / B, 4) for k, v in others.items()})
    d["Binder content (kg/m³)"] = round(B, 1)
    return d


# ---------------------------------------------------------------------------------------------------------
# 1) Chen et al. (2025) Buildings 15(21) 4003 - HS-ECC with PP / PE / PVA fibers (PP mixes excluded)
P = meta("Flexural Performance and Flexural Toughness Evaluation Method of High-Strength Engineered Cementitious Composites",
         "Bo Chen, Liang Hou, Rong-Guo Yan, Xiang-Yu Zhang, Hao Meng, Jing-Tian Li", 2025, "10.3390/buildings15214003")
base = kgm3({"OPC / Cement": 543.2, "FA (Fly ash)": 543.2, "GGBS": 135.8, "SF (Silica fume)": 135.8},
            {"SS / B (Silica sand)": 502.5, "W / B": 339.5})
fc = {"PE": {0.5: 51.7, 1.0: 54.3, 1.5: 61.3, 2.0: 70.1, 2.5: 83.6},
      "PVA": {0.5: 50.1, 1.0: 50.8, 1.5: 56.3, 2.0: 62.6, 2.5: 58.4}}
for ft, d in fc.items():
    for vf, f in d.items():
        r = dict(P); r.update(base)
        if ft == "PE":
            r.update({"PE fiber (vol%)": vf, "PE length (mm)": 12, "PE tensile strength (MPa)": 3100,
                      "PE elastic modulus (GPa)": 122})
        else:
            r.update({"PVA fiber (vol%)": vf, "PVA length (mm)": 12, "PVA tensile strength (MPa)": 1600,
                      "PVA elastic modulus (GPa)": 40})
        r.update({"Total fiber (vol%)": vf, "Curing method": "standard curing 20 ± 2 °C, RH ≥ 95%",
                  "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": 28,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
                  "Compressive strength (MPa)": f,
                  "Source table/page": "Table 1 (fibers), Table 2 (mix), Table 3 (fcu), Sec. 2 (curing)",
                  "Conversions / notes": f"{ft}-{vf}. kg/m3 / binder (C+FA+GGBS+SF = 1358 kg/m3). Silica sand 0.044-2 mm. "
                                         "Superplasticizer (>=25% water reduction) used but dosage not reported -> SP empty. "
                                         f"Fiber aspect ratio {'480' if ft == 'PE' else '500'} given (diameter not stated). "
                                         "No direct tension test (four-point bending only)."})
        rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 2) Lu et al. (2026) Polymers 18(21) 2798 - HS PE-ECC, MgO vs SRA. Only reference H-3 qualifies (MgO / SRA excluded).
P = meta("Material-Level Shrinkage and Tensile-Performance Screening of High-Strength Polyethylene-Fibre Engineered "
         "Cementitious Composite (PE-ECC) Mortar: MgO Versus Liquid Shrinkage-Reducing Admixture",
         "Qi Lu, Xian Zhou, Xian Wu, Zeyu Fan, Peihang Li, Wei Han", 2026, "10.3390/polym18212798")
for age, f in [(1, 33.0), (7, 67.8), (28, 90.1)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.65, "SF (Silica fume)": 0.10, "GGBS": 0.25, "W / B": 0.27,
              "Sand (type not stated) / B": 0.40, "Sand max size (µm)": 160, "SP / B": 0.01,
              "PE fiber (vol%)": 2.5, "Total fiber (vol%)": 2.5,
              "Curing method": "20 ± 2 °C, RH > 90% for 24 h, demolded, then standard curing to test age",
              "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1,
              "Test age (days)": age, "Compressive specimen": "cube (40 mm, from prism halves)",
              "Compressive specimen size (mm)": "40", "Compressive strength (MPa)": f,
              "Source table/page": "Table 4 (materials), Sec. 2.2 (mix H-3), Table 9 (fc), Table 10 (tension)",
              "Conversions / notes": "Reference mix H-3 only (other mixes contain MgO expansive agent or liquid SRA -> excluded). "
                                     "Fine ground sand, max 160 µm (authors call it sand). PCA superplasticizer liquid, 1% of binder. "
                                     "PE fiber properties not reported."})
    if age == 28:
        r.update({"Tensile specimen": "dumbbell plate (JC/T 2461-2018), 80 x 30 mm gauge section",
                  "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
                  "Tensile strength (MPa)": 7.1, "Tensile strain capacity (%)": 6.6})
        r["Conversions / notes"] += " VERIFY: direct-tension age not stated explicitly; assigned to 28 d (Table 11 pairs it with fc,28d)."
    rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 3) Choi, Kim, Lee (2020) Appl. Sci. 10(12) 4300 - slag-based (Ca(OH)2 + Na2SO4 activated) PE composite
P = meta("Mechanical and Fiber-Bridging Behavior of Slag-Based Composite with High Tensile Ductility",
         "Jeong-Il Choi, Hyeong-Ki Kim, Bang Yeon Lee", 2020, "10.3390/app10124300")
r = dict(P)
r.update({"GGBS": 0.895, "Ca(OH)2 / B": 0.075, "Na2SO4 / B": 0.030, "W / B": 0.30, "SP / B": 0.005, "VMA / B": 0.002,
          "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700,
          "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1.5,
          "Curing method": "in molds covered with plastic sheet, 23 ± 3 °C / 60% RH for 2 d, then water 23 ± 3 °C",
          "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 2, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dumbbell (JSCE), 30 x 13 mm section", "Tensile gauge length (mm)": 80,
          "Tensile test type": "direct (uniaxial)", "Compressive strength (MPa)": 36.8, "Tensile strength (MPa)": 8.5,
          "First-cracking strength (MPa)": 3.4, "Tensile strain capacity (%)": 7.5,
          "Source table/page": "Table 1 (mix), Table 3 (fc, fcr, ft, strain), Sec. 2 (fiber, curing)",
          "Conversions / notes": "Binder = GGBS 0.895 + Ca(OH)2 0.075 + Na2SO4 0.030 (paper's weight ratios). "
                                 "Polycarboxylate SP, VMA; anti-foam 0.001 (not listed). No sand."})
rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 4) Deng & Li (2025) J. Compos. Sci. 9(9) 502 - PE-ECC (cement + FA) with strain up to 18% (PE/PP hybrids excluded)
P = meta("High-Performance Cementitious Composites with Tensile Strain Capacity Up to 18%",
         "Zongcai Deng, Wenzhe Li", 2025, "10.3390/jcs9090502")
# (id, cement, FA, sand, water, fcr, ft, eps_u)   all kg/m3; PE 17.46 kg/m3 (18 mm) in every mix kept
mix = [("C1", 875, 375, 375, 375, 2.0, 6.3, 8.3), ("C2", 750, 500, 375, 380, 2.2, 7.3, 8.7),
       ("C3", 625, 625, 375, 390, 3.0, 9.9, 18.3), ("C4", 500, 750, 375, 395, 2.8, 7.2, 11.8),
       ("S1", 875, 375, 375, 375, 1.9, 6.3, 8.3), ("S2", 843, 361, 433, 360, 2.1, 6.1, 13.0),
       ("S3", 814, 349, 488, 350, 2.1, 6.3, 15.2), ("S4", 500, 750, 375, 375, 2.4, 7.2, 11.8),
       ("S5", 482, 723, 433, 360, 2.5, 7.4, 10.4), ("S6", 465, 698, 488, 350, 2.8, 8.3, 16.3),
       ("F4", 500, 750, 375, 395, 2.0, 6.4, 8.3), ("F8", 875, 375, 375, 375, 2.6, 7.2, 11.8)]
for mid, c, fa, s, w, fcr, ft, eps in mix:
    r = dict(P)
    r.update(kgm3({"OPC / Cement": c, "FA (Fly ash)": fa},
                  {"SS / B (Silica sand)": s, "W / B": w, "HRWR / B": 2.5, "VMA / B": 0.5}))
    r.update({"Sand max size (µm)": 180, "PE fiber (vol%)": 1.8, "PE length (mm)": 18, "PE diameter (µm)": 25,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 140, "Total fiber (vol%)": 1.8,
              "Curing method": "room, demolded at 24 h, then 25 °C / 90% RH", "Curing time (days)": 28,
              "Curing temperature (°C)": 25, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": "direct (uniaxial)",
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (fibers), Table 3 (mix), Table 5 (tension), Sec. 2 (HRWR, MC, curing)",
              "Conversions / notes": f"{mid}. kg/m3 / binder (cement + FA = {c + fa} kg/m3). Quartz sand 0.125-0.180 mm "
                                     "(fine sand, not powder) -> SS/B. HRWR 2.5 kg/m3, methyl cellulose 0.5 kg/m3 (VMA). "
                                     "PE 17.46 kg/m3 = 1.8 vol% (paper). fc only in Fig. 14 (C3/S3/F6 > 60 MPa) -> empty. "
                                     "Mixes with macro-PP fiber (F1-F3, F5-F7) excluded."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 5) Wen et al. (2026) Buildings 16(5) 1022 - seawater sea-sand PE-ECC, fiber content / length
P = meta("Mechanical Strength and Toughness Performance of Seawater Sea Sand ECC with Variable Polyethylene Fiber Content and Length",
         "Zheming Wen, Qinghai Xie, Jie Zeng, Heng Dai, Haoyang Huang", 2026, "10.3390/buildings16051022")
# (id, vf, Lf, sea?, fcu cube 70.7, ft)
mix = [("1%-12-SSE", 1.0, 12, True, 53.1, 2.06), ("1.5%-12-SSE", 1.5, 12, True, 41.1, 2.29),
       ("2%-12-SSE", 2.0, 12, True, 52.4, 2.64), ("1.5%-18-SSE", 1.5, 18, True, 49.4, 2.24),
       ("1.5%-24-SSE", 1.5, 24, True, 46.4, 3.23), ("1.5%-12-ECC", 1.5, 12, False, 45.92, 2.04)]
for mid, vf, lf, sea, fcu, ft in mix:
    r = dict(P)
    r.update(kgm3({"OPC / Cement": 588.96, "Limestone powder": 82.45, "SF (Silica fume)": 123.68, "GGBS": 630.18},
                  {"Sea sand / B" if sea else "River sand / B": 612.51, "W / B": 353.37, "SP / B": 8.83}))
    r.update({"PE fiber (vol%)": vf, "PE length (mm)": lf, "PE diameter (µm)": 25, "Total fiber (vol%)": vf,
              "Curing method": "film-covered (sealed) at room temperature; demolded at 1 d", "Curing time (days)": 28,
              "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
              "Tensile specimen": "dog-bone 368 x 100 x 50 mm (T/CCPA 7-2018)", "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": fcu, "Tensile strength (MPa)": ft,
              "Source table/page": "Table 1 (mix), Table 2 / Table 8 (fcu, ft), Sec. 2 (materials, curing, tests)",
              "Conversions / notes": f"{mid}. kg/m3 / binder (cement + limestone powder + SF + slag = 1425.27 kg/m3; "
                                     "w/b 0.25 stated, consistent). VERIFY: binder values sit in merged cells of Table 1; "
                                     "assigned in header order (cement 588.96, LP 82.45, SF 123.68, slag 630.18). "
                                     + ("Natural seawater as mixing water (Cl- 14.0 g/L), sea sand. " if sea else
                                        "Reference with river sand and tap water. ")
                                     + "Powder PCE SP. ft from Table 8 for the ECC reference. No strain capacity reported. "
                                       "fcu of 1.5%-12-ECC from Table 8 (45.92)."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 6) Zhang & Zeng (2026) Buildings 16(8) 1520 - steel-PE hybrid ECC with geopolymer aggregate.
#    Only the quartz-sand reference SS100G0 qualifies (GPA mixes use geopolymer aggregate -> excluded).
P = meta("Experimental Study on the Mechanical Properties of Steel-PE Hybrid Fiber Reinforced Engineering Cementitious "
         "Composites Containing Geopolymer Aggregates", "Jin Zhang, Yuzhuo Zeng", 2026, "10.3390/buildings16081520")
r = dict(P)
r.update(kgm3({"OPC / Cement": 1182.0, "SF (Silica fume)": 295.5},
              {"W / B": 259.2, "SS / B (Silica sand)": 352.2, "SP / B": 19.8}))
r.update({"PE fiber (vol%)": 2.0, "PE diameter (µm)": 25, "PE length (mm)": 18, "PE tensile strength (MPa)": 2900,
          "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2.0,
          "Curing method": "covered with film 24 h at room temperature, then standard curing room 20 ± 2 °C, RH ≥ 95%",
          "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
          "Test age (days)": 28, "Tensile specimen": "dog-bone 330 x 60 x 13 mm (JSCE)", "Tensile gauge length (mm)": 80,
          "Tensile test type": "direct (uniaxial)", "Tensile strength (MPa)": 9.79, "First-cracking strength (MPa)": 7.30,
          "Tensile strain capacity (%)": 5.44,
          "Source table/page": "Table 5 (PE), Table 7 (mix), Table 9 (tension), Sec. 2.2-2.4",
          "Conversions / notes": "SS100G0 (quartz sand reference, PE only). kg/m3 / binder (cement + SF = 1477.5 kg/m3). "
                                 "PR = polycarboxylate water reducer 19.8 kg/m3. PE 18.9 kg/m3 (= 1.95 vol% at 970 kg/m3; paper "
                                 "labels it 2.0 vol%). PE length = 25 µm x aspect ratio 720 = 18 mm (derived). "
                                 "fc only in Fig. 8 -> empty. Strain unit not printed in Table 9; values read as %."})
rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 7) Niu et al. (2023) Appl. Sci. 13(10) 6078 - natural-sand vs desert-sand PE-ECC, uniaxial tension at 3-28 d
P = meta("Effect of Desert Sand on the Section Bonding Properties of Polyethylene Fiber-Engineered Cementitious Composites",
         "Yanfeng Niu, Fengxia Han, Qing Liu, Xu Yang", 2023, "10.3390/app13106078")
B = 43.95 + 18.84  # mass % of cement + fly ash
# (id, natural sand %, desert sand %, age, avg cracking load N, avg ultimate load N)
mix = [("NSPE-ECC", 18.84, 0, 3, 899.3, 2512.3), ("NSPE-ECC", 18.84, 0, 7, 1156.0, 2589.7),
       ("NSPE-ECC", 18.84, 0, 14, 961.0, 2451.7), ("NSPE-ECC", 18.84, 0, 28, 1227.7, 2920.3),
       ("DSPE-ECC", 13.19, 5.65, 3, 1049.7, 1907.3), ("DSPE-ECC", 13.19, 5.65, 7, 1484.3, 2440.0),
       ("DSPE-ECC", 13.19, 5.65, 14, 1184.3, 2456.0), ("DSPE-ECC", 13.19, 5.65, 28, 1356.7, 2907.3)]
for mid, ns, ds, age, pcr, pu in mix:
    r = dict(P)
    r.update({"OPC / Cement": round(43.95 / B, 4), "FA (Fly ash)": round(18.84 / B, 4), "W / B": round(16.96 / B, 4),
              "Sand (type not stated) / B": round(ns / B, 4), "Dune sand / B": round(ds / B, 4) if ds else None,
              "SP / B": round(0.49 / B, 4), "VMA / B": round(0.02 / B, 5),
              "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2.0,
              "Curing method": "standard curing 20 ± 2 °C, RH ≥ 95%", "Curing time (days)": age,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": age,
              "Tensile specimen": "dumbbell 230 x 60 x 15 mm, 80 x 30 x 15 mm gauge part", "Tensile gauge length (mm)": 80,
              "Tensile test type": "direct (uniaxial)",
              "Tensile strength (MPa)": round(pu / 450, 2), "First-cracking strength (MPa)": round(pcr / 450, 2),
              "Source table/page": "Table 4 (PE), Table 5 (mix, mass %), Table 6 (loads), Sec. 2 (curing, specimen)",
              "Conversions / notes": f"{mid}, {age} d. Mix in mass % of batch; ratios / (cement + FA). Natural sand FM 1.87; "
                                     "desert sand FM 0.60 (Dune sand). Water reducer + thickening agent (VMA). PE 0.90 mass % "
                                     "= 2 vol% (abstract). VERIFY: ft and fcr = average ultimate / cracking load (N) / 450 mm2 "
                                     "gauge section (30 x 15 mm); paper reports loads only. No fc, no strain."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 8) AlAraj et al. (2024) Fibers 12(1) 1 - mortar with PE fibers / CNTs. Only mix C (PE only) qualifies (CNT excluded).
P = meta("Mechanical Performance of Cementitious Materials Reinforced with Polyethylene Fibers and Carbon Nanotubes",
         "Rashad R. AlAraj, Adil K. Tamimi, Noha M. Hassan, Kazi Parvez Fattah", 2024, "10.3390/fib12010001")
r = dict(P)
r.update(kgm3({"OPC / Cement": 706, "SF (Silica fume)": 125}, {"Sand (type not stated) / B": 920, "W / B": 380}))
r.update({"PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 38, "PE tensile strength (MPa)": 2500,
          "PE elastic modulus (GPa)": 70, "Total fiber (vol%)": 2.0,
          "Curing method": "demolded at 24 h, water basin", "Curing time (days)": 28, "Demolding age (days)": 1,
          "Test age (days)": 28, "Compressive specimen": "cylinder (ASTM C39)", "Compressive strength (MPa)": 49.2,
          "Source table/page": "Table 2 (PE), Table 3 (mix C), Table 5 (fc), Sec. 2 (curing)",
          "Conversions / notes": "Mix C (control mortar + 2 vol% UHM-PE fiber, 19.2 kg/m3). kg/m3 / binder (cement + SF = 831). "
                                 "No SP reported. Cylinder size not given in text read. No tension test (flexure only)."})
rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 9) Han et al. (2022) Adv. Mater. Sci. Eng. 7876056 - PE-ECC with FA or slag ("mineral powder"), w/b 0.25-0.31
P = meta("Optimized Design of Polyethylene Fiber-Engineered Cementitious Composite Mix Ratio Based on the Analytic Hierarchy Process",
         "Fengxia Han, Qing Liu, Xin Guo, Yanfeng Niu", 2022, "10.1155/2022/7876056")
# batch (g): cement, admixture, sand, water, water reducer; fiber 14.7 g (2 vol%), thickener 0.25 g
batch = {"A-0.25": (742.2, 318.1, 318.1, 265.1, 10.00), "A-0.27": (721.9, 309.4, 309.4, 278.5, 8.25),
         "A-0.29": (702.8, 301.2, 301.2, 291.1, 5.02), "A-0.31": (684.6, 293.4, 293.4, 303.2, 3.91),
         "B-0.27": (610.6, 407.0, 305.3, 274.8, 8.14), "C-0.27": (502.1, 502.1, 301.3, 271.1, 3.50),
         "D-0.27": (396.5, 594.7, 297.3, 267.6, 2.97)}
# (adm, mix, age, fcr, ft, elongation %)
res = [("FA", "A-0.25", 7, 2.13, 5.63, 3.59), ("FA", "A-0.25", 28, 2.34, 6.34, 4.23), ("FA", "A-0.25", 60, 2.71, 6.75, 7.07),
       ("FA", "A-0.27", 7, 1.92, 4.96, 4.03), ("FA", "A-0.27", 28, 2.93, 6.59, 7.34), ("FA", "A-0.27", 60, 2.49, 5.83, 4.55),
       ("FA", "A-0.29", 7, 2.32, 4.26, 3.34), ("FA", "A-0.29", 28, 2.13, 4.91, 2.85), ("FA", "A-0.29", 60, 2.33, 5.37, 3.97),
       ("FA", "A-0.31", 7, 1.97, 4.45, 3.37), ("FA", "A-0.31", 28, 1.99, 5.79, 3.97), ("FA", "A-0.31", 60, 1.93, 5.56, 4.88),
       ("FA", "B-0.27", 7, 2.21, 4.81, 4.01), ("FA", "B-0.27", 28, 2.15, 4.84, 4.36), ("FA", "B-0.27", 60, 2.14, 5.90, 4.55),
       ("FA", "C-0.27", 7, 2.56, 5.23, 4.48), ("FA", "C-0.27", 28, 2.21, 5.56, 4.33), ("FA", "C-0.27", 60, 2.18, 6.29, 5.86),
       ("FA", "D-0.27", 7, 2.06, 4.53, 3.46), ("FA", "D-0.27", 28, 2.63, 5.46, 5.30), ("FA", "D-0.27", 60, 1.97, 4.93, 3.04),
       ("KF", "A-0.25", 7, 2.32, 6.36, 6.16), ("KF", "A-0.25", 28, 2.39, 6.66, 6.46), ("KF", "A-0.25", 60, 2.82, 6.08, 6.00),
       ("KF", "A-0.27", 7, 2.00, 6.02, 6.01), ("KF", "A-0.27", 28, 2.50, 5.98, 5.18), ("KF", "A-0.27", 60, 2.16, 5.54, 4.40),
       ("KF", "A-0.29", 7, 2.20, 4.67, 4.10), ("KF", "A-0.29", 28, 2.49, 5.60, 5.37), ("KF", "A-0.29", 60, 2.10, 6.03, 6.15),
       ("KF", "A-0.31", 7, 2.20, 4.75, 4.04), ("KF", "A-0.31", 28, 2.40, 5.77, 5.72), ("KF", "A-0.31", 60, 2.59, 5.31, 3.47),
       ("KF", "B-0.27", 7, 2.27, 6.00, 7.30), ("KF", "B-0.27", 28, 2.64, 4.82, 3.64), ("KF", "B-0.27", 60, 2.53, 5.24, 4.70),
       ("KF", "C-0.27", 7, 2.62, 4.93, 4.84), ("KF", "C-0.27", 28, 2.27, 5.09, 4.35), ("KF", "C-0.27", 60, 2.33, 5.39, 4.94),
       ("KF", "D-0.27", 7, 2.39, 4.47, 5.07), ("KF", "D-0.27", 28, 1.72, 5.13, 3.98), ("KF", "D-0.27", 60, 1.90, 5.86, 6.00)]
for adm, mid, age, fcr, ft, el in res:
    c, a, s, w, sp = batch[mid]
    r = dict(P)
    r.update(kgm3({"OPC / Cement": c, ("FA (Fly ash)" if adm == "FA" else "GGBS"): a},
                  {"Sand (type not stated) / B": s, "W / B": w, "SP / B": sp, "VMA / B": 0.25}))
    r["Binder content (kg/m³)"] = None  # batch in grams, not kg/m3
    r.update({"Sand max size (µm)": 1180, "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 24,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2.0,
              "Curing method": "standard curing 20 ± 2 °C, RH ≥ 95%", "Curing time (days)": age,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": age,
              "Tensile specimen": "dumbbell, 80 x 30 x 15 mm middle part", "Tensile test type": "direct (uniaxial)",
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": el,
              "Source table/page": "Tables 1-5 (materials, batch in g), tension results table (fcr, ft, elongation)",
              "Conversions / notes": f"PE-{adm}-{mid}. Batch in grams -> ratios / (cement + admixture). Admixture = "
                                     f"{'grade II fly ash' if adm == 'FA' else 'mineral powder (KF = ground slag)'}. Natural washed sand "
                                     "< 1.18 mm. Water reducer and thickening agent (VMA) as dosed. VERIFY: 'average elongation (%)' "
                                     "column is numerically identical to the tensile displacement (mm) column; stored as reported."
                                     + (" Age printed as 70 d for KF-C third row; read as 60 d." if (adm, mid, age) == ("KF", "C-0.27", 60) else "")})
    rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 10) Yun et al. (2023) J. Phys.: Conf. Ser. 2548 012008 - PE-FRCC with micro steel fibers 0-1.5 %
P = meta("Effect of micro steel fibre contents on compressive and self-sensing properties of polyethylene fibre-reinforced "
         "cement composite (PE-FRCC) in cyclic compression",
         "Hyun-Do Yun, Won-Chang Choi, Wan-Shin Park, Ai-Hua Jin, Yong-Chul Kim, Soo-Yeon Seo", 2023,
         "10.1088/1742-6596/2548/1/012008")
for sf, fc in [(0.0, 32.8), (0.25, 37.7), (0.50, 47.5), (1.00, 48.2), (1.50, 45.7)]:
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": 0.30, "SS / B (Silica sand)": 0.4, "Sand max size (µm)": 300, "SP / B": 0.001,
              "PE fiber (vol%)": 0.75, "PE length (mm)": 15, "PE diameter (µm)": 12,
              "Steel fiber (vol%)": sf if sf else None, "Steel length (mm)": 15 if sf else None,
              "Steel diameter (µm)": 200 if sf else None, "Total fiber (vol%)": 0.75 + sf,
              "Curing method": "demolded at 24 h, wet-cured", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube (KS L 5105)", "Compressive specimen size (mm)": "50",
              "Compressive strength (MPa)": fc,
              "Source table/page": "Sec. 2 (materials, mix, curing), Sec. 3.1 (fc text)",
              "Conversions / notes": f"PE0.75{'+SF%.2f' % sf if sf else ''}. Binder = Type I OPC only. Silica sand 0.2-0.3 mm. "
                                     "PCE SP 0.1% of cement. Fiber fractions stated 'by volume fraction'. Micro straight steel fibers. "
                                     "No direct tension test."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# 11) Kunieda et al. (2012) JACT 10(9) 313 - UHP-SHCC (low-heat PC + SF, PE 1.5 %); virgin 28 d tensile properties only
P = meta("Recovery of Protective Performance of Cracked Ultra High Performance-Strain Hardening Cementitious Composites "
         "(UHP-SHCC) Due to Autogenous Healing", "Minoru Kunieda, Kang Choonghyun, Naoshi Ueda, Hikaru Nakamura", 2012,
         "10.3151/jact.10.313")
r = dict(P)
r.update(kgm3({"OPC / Cement": 1313, "SF (Silica fume)": 232}, {"W / B": 340, "SS / B (Silica sand)": 155, "SP / B": 15.4}))
r.update({"Sand max size (µm)": 500, "PE fiber (vol%)": 1.5, "PE length (mm)": 6, "PE diameter (µm)": 12,
          "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1.5,
          "Curing method": "demolded at 1 d, water curing at 20 °C (constant-temperature room)", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28,
          "Tensile specimen": "dumbbell, 10 x 30 mm tested section", "Tensile test type": "direct (uniaxial)",
          "Tensile strength (MPa)": 6.8, "Tensile strain capacity (%)": 1.04,
          "Source table/page": "Table 1 (mix), Table 2 (tension, 28 d), Sec. 3.1 / 3.4 (materials, curing), p.315",
          "Conversions / notes": "kg/m3 / binder (low-heat Portland cement 1313 + SF 232 = 1545; W/B 0.22 stated). Quartz sand "
                                 "< 0.5 mm (fine aggregate, not powder). Air reducing agent 0.062 kg/m3 (defoamer, allowed). "
                                 "VERIFY: water curing described for the healing specimens (Sec. 3.4); assumed same for the "
                                 "28 d dumbbells. Pre-cracking / healing results not used."})
rows.append(r)

# ---------------------------------------------------------------------------------------------------------
# PLACEHOLDER_NEXT

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w5_pe.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", os.path.join(out_dir, "w5_pe.csv"))
