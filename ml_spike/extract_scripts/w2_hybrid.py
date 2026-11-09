# Builder for hybrid-fibre ECC/SHCC additions (w2_hybrid.csv)
# Every number below was read from the cited paper's tables/text (full text via Europe PMC / publisher HTML).
import csv, os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
with open(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig") as f:
    H = next(csv.reader(f))
assert len(H) == 99
rows = []


def add(base, **kw):
    r = dict(base)
    r.update({k: v for k, v in kw.items() if v is not None})
    for k in r:
        assert k in H, k
    rows.append(r)


R = lambda x, n=4: round(x, n)

# ---------------------------------------------------------------- 1 Liao et al. 2023 (PVA + basalt / PP)
B = 382 + 890
b = {"Article Name": "Cost-Effective Engineered Cementitious Composites with Hybrid PVA and Basalt/PP Fiber: A Study on Compressive, Tensile and Impact Performance",
     "Author": "Liao W., Wu P., Huang J., Chen G., Lin J., Guo Y., Chen R.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16145172",
     "OPC / Cement": R(382 / B), "FA (Fly ash)": R(890 / B), "W / B": R(297 / B), "SS / B (Silica sand)": R(460 / B), "SP / B": R(18 / B, 5),
     "Sand max size (µm)": 150, "Binder content (kg/m³)": B,
     "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA elastic modulus (GPa)": 40,
     "Curing method": "standard curing chamber ~24 h in mould, then standard curing chamber 28 d (temperature/RH not stated)",
     "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
     "Tensile specimen": "dog-bone (30x13 mm section)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
for g, pva, bf, pp, ft, eps in [("PCC", 0, 0, 0, 4.34, 0.17), ("1.0%PVA", 1, 0, 0, 4.44, 1.13), ("1.5%PVA", 1.5, 0, 0, 7.54, 1.76),
                                ("1.0%PVA+0.5%BF", 1, 0.5, 0, 7.62, 1.44), ("1.0%PVA+0.5%PP", 1, 0, 0.5, 4.86, 1.38),
                                ("2.0%PVA", 2, 0, 0, 7.60, 2.29), ("1.0%PVA+1.0%BF", 1, 1, 0, 5.73, 1.35), ("1.0%PVA+1.0%PP", 1, 0, 1, 5.6, 1.8),
                                ("2.5%PVA", 2.5, 0, 0, 6.27, 3.33), ("1.0%PVA+1.5%PP", 1, 0, 1.5, 7.0, 1.91), ("1.0%PVA+1.5%BF", 1, 1.5, 0, 6.86, 1.5)]:
    d = {"PVA fiber (vol%)": pva, "Basalt fiber (vol%)": bf, "PP fiber (vol%)": pp, "Total fiber (vol%)": pva + bf + pp,
         "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
         "Source table/page": "Table 1 (fibres), Table 2 (mix, kg/m3), Table 3 (tension averages)",
         "Conversions / notes": f"{g}: Table 2 kg/m3 cement 382, FA 890, water 297, silica sand 460, water reducer 18; binder = cement+FA = {B} kg/m3, all /B. "
                                "P.II 52.5R cement, class F FA, silica sand 100-200 mesh (max ~150 µm). Basalt fibre 15 mm/16 µm/E 34 GPa; PP 16 mm/20 µm/E 4.3 GPa (no strength given). "
                                "Tensile values = averages of 3 specimens (Table 3). fc only in Fig. 12 (text gives only % changes) - left blank."}
    if pp:
        d["PP length (mm)"] = 16; d["PP diameter (µm)"] = 20
    if not pva:
        for k in ["PVA length (mm)", "PVA diameter (µm)", "PVA elastic modulus (GPa)"]:
            d[k] = None
    r = dict(b); r.update(d)
    add({k: v for k, v in r.items() if v is not None})

# ---------------------------------------------------------------- 2 Wang & Zhang 2024 (steel + PVA, two PVA sources)
b = {"Article Name": "Multi-Objective Optimization and Mechanical Properties Analysis of Steel–PVA Hybrid Fiber-Reinforced Cementitious Composites",
     "Author": "Wang R., Zhang P.", "Year": 2024, "DOI / URL": "https://doi.org/10.3390/ma17174324",
     "OPC / Cement": R(1 / 2.8), "FA (Fly ash)": R(1.8 / 2.8), "W / B": R(0.56 / 2.8), "SS / B (Silica sand)": R(0.6 / 2.8), "Sand max size (µm)": 210,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
     "Tensile specimen": "dumbbell (30x15 mm section)", "Tensile gauge length (mm)": 90, "Tensile test type": "direct"}
common2 = ("Matrix 'cement fly ash/sand/water = 1:1.8:0.6:0.56' (Sec. 3, read as cement 1 : FA 1.8 : sand 0.6 : water 0.56 by mass) -> binder 2.8, W/B 0.20. "
           "P.O 42.5 cement, grade I FA, quartz sand 140-210 µm. Paper states tensile and compressive values were multiplied by a 0.95 conversion factor. "
           "Curing regime and test age not reported (left blank). Japan PVA = Kuraray K-I 12 mm/39 µm/1620 MPa/42.8 GPa; China PVA = 12 mm/15.09 µm/1830 MPa/40 GPa; "
           "steel = copper-plated micro steel 13 mm/200 µm/2850 MPa/210 GPa. Bending strength {fb} MPa (thin plate 400x100x15).")
for g, s, c, j, ft, fc, fb, src in [("C0", 0, 0, 0, 1.43, 30.28, 2.11, 6), ("C0.4J0", 0, 0.4, 0, 2.62, 29.14, 3.43, 6), ("C0.8J0", 0, 0.8, 0, 2.28, 26.86, 3.59, 6),
                                     ("C1.2J0", 0, 1.2, 0, 2.30, 30.69, 4.71, 6), ("C1.6J0", 0, 1.6, 0, 3.08, 32.04, 4.12, 6), ("C2.0J0", 0, 2.0, 0, 3.68, 34.39, 4.35, 6),
                                     ("C2.2J0", 0, 2.2, 0, 3.31, 28.21, 4.38, 6), ("C0J0.4", 0, 0, 0.4, 2.89, 29.00, 2.02, 6), ("C0J0.8", 0, 0, 0.8, 2.16, 26.10, 3.01, 6),
                                     ("C0J1.2", 0, 0, 1.2, 2.38, 30.52, 4.38, 6), ("C0J1.6", 0, 0, 1.6, 3.31, 31.23, 5.13, 6), ("C0J2.0", 0, 0, 2.0, 4.23, 34.09, 5.23, 6),
                                     ("C0J2.2", 0, 0, 2.2, 3.74, 29.94, 4.65, 6),
                                     ("S0.2C0J2", 0.2, 0, 2.0, 3.61, 33.77, 9.21, 7), ("S0.2C0.5J1.5", 0.2, 0.5, 1.5, 3.37, 26.79, 6.39, 7),
                                     ("S0.2C1.0J1.0", 0.2, 1.0, 1.0, 3.37, 30.53, 5.66, 7), ("S0.2C1.5J0.5", 0.2, 1.5, 0.5, 3.50, 33.54, 5.26, 7),
                                     ("S0.2C2.0J0", 0.2, 2.0, 0, 3.21, 44.07, 5.28, 7), ("S0.4C0J2", 0.4, 0, 2.0, 3.66, 42.98, 9.83, 7),
                                     ("S0.4C0.5J1.5", 0.4, 0.5, 1.5, 2.57, 26.92, 4.66, 7), ("S0.4C1J1", 0.4, 1.0, 1.0, 3.36, 36.36, 5.83, 7),
                                     ("S0.4C1.5J0.5", 0.4, 1.5, 0.5, 2.48, 43.48, 6.21, 7), ("S0.4C2.0J0", 0.4, 2.0, 0, 3.46, 43.24, 6.57, 7)]:
    pva = R(c + j, 2)
    d = {"PVA fiber (vol%)": pva, "Steel fiber (vol%)": s, "Total fiber (vol%)": R(pva + s, 2), "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
         "Source table/page": f"Table 5 (fibres), Sec. 3 text (matrix ratio), Table {src} (results)",
         "Conversions / notes": f"{g}: China PVA {c}%, Japan PVA {j}%, steel {s}% (PVA column = sum of both PVA types). " + common2.format(fb=fb)}
    if pva:
        d["PVA length (mm)"] = 12
        if c == 0:
            d.update({"PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8})
        elif j == 0:
            d.update({"PVA diameter (µm)": 15.09, "PVA tensile strength (MPa)": 1830, "PVA elastic modulus (GPa)": 40})
    if s:
        d.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850, "Steel elastic modulus (GPa)": 210})
    add(b, **d)

# ---------------------------------------------------------------- 3 Hu et al. 2021 (PVA + PP, PVC aggregate)
B = 395 + 869
b = {"Article Name": "Performance Test and Microstructure of Modified PVC Aggregate-Hybrid Fiber Reinforced Engineering Cementitious Composite (ECC)",
     "Author": "Hu S., Cai H., Hong R., Li M., Yao F.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14081856",
     "OPC / Cement": R(395 / B), "FA (Fly ash)": R(869 / B), "W / B": R(313 / B), "SP / B": R(5.1 / B, 5), "Binder content (kg/m³)": B, "Sand max size (µm)": 150,
     "Curing method": "room temperature 36 h in mould, then standard curing room 28 d", "Curing time (days)": 28, "Demolding age (days)": 1.5, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile test type": "splitting"}
for g, pvc, mpvc, pva, pp, sand, fc, fts in [("A-0", 0, 0, 0, 0, 459, 51.14, 1.84), ("A-1", 94.5, 0, 0, 0, 321.3, 41.42, 1.52), ("A-2", 0, 94.5, 0, 0, 321.3, 43.98, 1.71),
                                             ("B-1", 0, 0, 0, 4.55, 459, 46.36, 2.47), ("B-2", 0, 0, 13, 0, 459, 47.51, 3.4), ("B-3", 0, 0, 19.5, 0, 459, 43.4, 3.75),
                                             ("B-4", 0, 0, 26, 0, 459, 41.6, 4.25), ("B-5", 0, 0, 19.5, 4.55, 459, 39.07, 3.82), ("C-1", 0, 31.5, 19.5, 4.55, 413.1, 36.16, 3.73),
                                             ("C-2", 0, 63, 19.5, 4.55, 367.2, 35.95, 3.72), ("C-3", 0, 94.5, 19.5, 4.55, 321.3, 35.28, 3.67)]:
    vpva = R(pva / 1300 * 100, 3); vpp = R(pp / 910 * 100, 3)
    d = {"SS / B (Silica sand)": R(sand / B), "PVA fiber (vol%)": vpva, "PP fiber (vol%)": vpp, "Total fiber (vol%)": R(vpva + vpp, 3),
         "Compressive strength (MPa)": fc, "Tensile strength (MPa)": fts,
         "Source table/page": "Table 1 (fibres), Table 2 + Sec. 2.2 text (mix, kg/m3), Table 3 (fc, splitting)",
         "Conversions / notes": f"{g}: cement 395, FA 869, water 313, water reducer 5.1 kg/m3 (text); binder = {B}. Quartz sand {sand} kg/m3 (100-200 mesh). "
                                f"PVA {pva} kg/m3 / 1300 (paper density) -> {vpva}%; PP {pp} kg/m3 / 910 (paper density) -> {vpp}%. "
                                f"PVC aggregate {pvc} kg/m3, silica-fume-coated PVC aggregate {mpvc} kg/m3 (PVC/B = {R((pvc + mpvc) / B)}; no column; replaces sand by volume; coating SF = 30% of PVC mass, not counted in binder). "
                                "Splitting-test specimen not explicitly stated (100 mm cubes and Φ150x65 cylinders cast). Elastic modulus/brittleness also in Table 3."}
    if pva:
        d.update({"PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 42.8})
    if pp:
        d.update({"PP length (mm)": 12, "PP diameter (µm)": 18})
    add(b, **d)

# ---------------------------------------------------------------- 4 Cui et al. 2019 (PVA/PP/steel, compression)
B = 475 + 710
b = {"Article Name": "Experimental Research on Uniaxial Compression Constitutive Model of Hybrid Fiber-Reinforced Cementitious Composites",
     "Author": "Cui T., He H., Yan W.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12152370",
     "OPC / Cement": R(475 / B), "FA (Fly ash)": R(710 / B), "W / B": R(400 / B), "SS / B (Silica sand)": R(415 / B),
     "SP / B": R(0.035 / B, 6), "Binder content (kg/m³)": B,
     "Curing method": "standard curing room 20 °C, RH 95%", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
     "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "150"}
for g, pva, pp, st, fcu, fc0 in [("DB", 0, 0, 0, 55.6, 42.1), ("PC1", 2, 0, 0, 52.8, 41.2), ("PC2", 1.5, 0.5, 0, 50.0, 38.5), ("PC3", 1, 1, 0, 47.9, 37.2),
                                 ("PC4", 0.5, 1.5, 0, 46.1, 36.9), ("PC5", 0, 2, 0, 45.2, 35.7), ("SC1", 0, 0, 2, 47.6, 36.7), ("SC2", 0, 0.5, 1.5, 50.6, 40.0),
                                 ("SC3", 0, 1, 1, 53.6, 41.3), ("SC4", 0, 1.5, 0.5, 54.1, 42.3)]:
    d = {"PVA fiber (vol%)": pva, "PP fiber (vol%)": pp, "Steel fiber (vol%)": st, "Total fiber (vol%)": pva + pp + st, "Compressive strength (MPa)": fcu,
         "Source table/page": "Table 1 (mix, kg/m3), Sec. 2.1 (fibres), Table 3 (fcu, fc0)",
         "Conversions / notes": f"{g}: Table 1 cement 475, FA 710, quartz sand 415 (fineness modulus 2.69), water 400 kg/m3, water reducer 35 g/m3; binder = {B}. "
                                f"Computed W/B = {R(400 / B, 3)} while text states w/b 0.35. fc = 150 mm cube fcu; prism (150x150x300) axial strength fc0 = {fc0} MPa. "
                                "PVA tensile strength >=1200 MPa, steel >=1100 MPa, PP >=500 MPa (minimum values, not entered). No tensile test."}
    if pva:
        d.update({"PVA length (mm)": 12, "PVA diameter (µm)": 39})
    if pp:
        d.update({"PP length (mm)": 12, "PP diameter (µm)": 31})
    if st:
        d.update({"Steel length (mm)": 25, "Steel diameter (µm)": 400})
    add(b, **d)

# ---------------------------------------------------------------- 5 Wang et al. 2019 (PVA + steel, low-shrinkage cement)
b = {"Article Name": "Stress–Strain Properties and Gas Permeability Evolution of Hybrid Fiber Engineered Cementitious Composites in the Process of Compression",
     "Author": "Wang Z., Zuo J., Liu C., Zhang Z., Han Y.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12091382",
     "OPC / Cement": 1, "W / B": 0.25, "SS / B (Silica sand)": 0.2, "Sand max size (µm)": 150, "SP / B": 0.01,
     "PVA fiber (vol%)": 1.7, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8,
     "Curing method": "covered 24 h, then standard curing room 20±2 °C, RH >95%", "Curing time (days)": 27, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
     "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100"}
for g, st, fc, E in [("Mono", 0, 53.3, 18.7), ("Hy1", 0.6, 51.7, 18.6), ("Hy2", 1.0, 59.4, 21.5)]:
    d = {"Steel fiber (vol%)": st, "Total fiber (vol%)": R(1.7 + st, 2), "Compressive strength (MPa)": fc,
         "Source table/page": "Sec. 2.1 (mix), Table 1 (fibres), Table 2 (fibre fractions), Table 3 (uniaxial fc)",
         "Conversions / notes": f"{g}: binder is a single 'newly developed composite cement with low drying shrinkage' (entered as cement = 1). w/c 0.25, s/c 0.20, PCE SP 1.0% of cement. "
                                f"Fine silica sand max 150 µm, mean 100 µm. Uniaxial fc (avg of 3), E0 = {E} GPa. PVA density given as 1.2 g/cm3. No tensile test."}
    if st:
        d.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2750, "Steel elastic modulus (GPa)": 210})
    add(b, **d)

# 6 Jiang et al. 2026 (ma19020424, LC3-ECC PVA/PE/PP) removed: already extracted by sibling agent in w2_green.csv

# ---------------------------------------------------------------- 7 Liu & Han 2019 (PVA + steel, compression)
B = 530 + 753
b = {"Article Name": "Experimental Investigation on Compressive Toughness of the PVA-Steel Hybrid Fiber Reinforced Cementitious Composites",
     "Author": "Liu W., Han J.", "Year": 2019, "DOI / URL": "https://doi.org/10.3389/fmats.2019.00108",
     "OPC / Cement": R(530 / B), "FA (Fly ash)": R(753 / B), "W / B": R(404.5 / B), "Sand (type not stated) / B": R(467 / B), "Binder content (kg/m³)": B,
     "Curing method": "standard curing room 20±2 °C, RH 95%", "Curing time (days)": 27, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
     "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "prism", "Compressive specimen size (mm)": "150x150x300"}
for g, pva, st, ar, P in [("A1", 0, 0, None, 1033.5), ("A2", 0.5, 0, None, 918.00), ("A3", 1.0, 0, None, 961.50), ("A4", 1.5, 0, None, 996.00),
                          ("A5", 1.0, 0.5, 40, 918.75), ("A6", 1.0, 1.0, 40, 923.25), ("A7", 1.0, 1.5, 40, 954.00), ("A8", 1.0, 0.5, 80, 938.25),
                          ("A9", 1.0, 1.0, 80, 941.25), ("A10", 1.0, 1.5, 80, 951.00), ("A11", 0.5, 0.5, 60, 862.50), ("A12", 0.5, 1.0, 60, 885.00),
                          ("A13", 0.5, 1.5, 60, 895.50), ("A14", 1.0, 0.5, 60, 918.75), ("A15", 1.0, 1.0, 60, 929.25), ("A16", 1.0, 1.5, 60, 945.75),
                          ("A17", 1.5, 0.5, 60, 924.00), ("A18", 1.5, 1.0, 60, 964.50), ("A19", 1.5, 1.5, 60, 979.88)]:
    fc = R(P * 1000 / (150 * 150), 2)
    d = {"PVA fiber (vol%)": pva, "Steel fiber (vol%)": st, "Total fiber (vol%)": pva + st, "Compressive strength (MPa)": fc,
         "Source table/page": "Table 1 (mix, kg/m3), Tables 2-3 (fibres), Table 4 (peak load)",
         "Conversions / notes": f"{g}: cement 530, FA 753, standard sand 467, water 404.5 kg/m3; binder {B}. "
                                f"fc DERIVED = prism peak load {P} kN / (150x150 mm) = {fc} MPa (axial prism strength; 150 mm cube strengths tested but not tabulated). "
                                "P.O 42.5, class II FA, standard sand (ISO cement-test sand). PVA Kuraray KII RECS15 12 mm/40 µm/1600 MPa/40 GPa."}
    if pva:
        d.update({"PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40})
    if st:
        d.update({"Steel length (mm)": {40: 24, 60: 36, 80: 48}[ar], "Steel diameter (µm)": 600, "Steel tensile strength (MPa)": 600})
        d["Conversions / notes"] += f" Crimped steel, aspect ratio {ar} (Table 2 lengths 24/36/48 mm, d 0.6 mm); tensile strength '>=600 MPa'."
    add(b, **d)

# ---------------------------------------------------------------- 8 Son et al. 2021 (hooked + smooth steel hybrid HPFRCC)
b = {"Article Name": "Effect of Fiber Blending Ratio on the Tensile Properties of Steel Fiber Hybrid Reinforced Cementitious Composites under Different Strain Rates",
     "Author": "Son M., Kim G., Kim H., Lee S., Lee Y., Nam J., Kobayashi K.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14164504",
     "OPC / Cement": 0.85, "FA (Fly ash)": 0.15, "W / B": 0.4, "SS / B (Silica sand)": 0.35, "Sand max size (µm)": 300,
     "Steel fiber (vol%)": 2, "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2,
     "Curing method": "1 d in constant temperature/humidity chamber, then standard water curing to 28 d", "Curing time (days)": 27,
     "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dumbbell 400x100x25 mm, 25x50 mm central section", "Tensile test type": "direct"}
for g, h, s, fc, ft, eps in [("H2.0", 2, 0, 61.06, 3.75, 0.34), ("S2.0", 0, 2, 65.98, 4.33, 0.23), ("H1.5S0.5", 1.5, 0.5, 61.80, 3.93, 0.39),
                             ("H1.0S1.0", 1.0, 1.0, 62.21, 4.15, 0.30), ("H0.5S1.5", 0.5, 1.5, 64.92, 4.51, 0.21)]:
    d = {"Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
         "Source table/page": "Table 2 (materials), Table 4 (mix ratios, fc), Tables 5-6 (static-rate tension averages)",
         "Conversions / notes": f"{g}: hooked steel (HSF 30 mm/0.5 mm/1140 MPa) {h}% + smooth brass-coated steel (SSF 13 mm in Table 2, 12 mm in text; 0.2 mm/2700 MPa) {s}%. "
                                "Table 4 mass ratios water 0.4 : cement 0.85 : FA 0.15 : silica sand 0.35 (Type 7, max 0.3 mm); small SP dosage not quantified. "
                                "Tension values = static rate (1e-6 /s) averages; high-rate (~10 /s) results also in Tables 5-6. Compressive specimen size not stated."}
    if h == 2:
        d.update({"Steel length (mm)": 30, "Steel diameter (µm)": 500, "Steel tensile strength (MPa)": 1140})
    elif s == 2:
        d.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2700})
    else:
        d["Conversions / notes"] += " Mixed steel geometries - steel length/diameter/strength left blank."
    add(b, **d)

# ---------------------------------------------------------------- 9 Krishnaraja et al. 2019 (PVA/PP/steel hybrids)
b = {"Article Name": "Study on impact of fiber hybridization in material properties of engineered cementitious composites",
     "Author": "Krishnaraja A.R., Anandakumar S., Jegan M., Mukesh T.S., Kumar K.S.", "Year": 2019, "DOI / URL": "https://doi.org/10.1590/S1517-707620190002.0662",
     "OPC / Cement": R(1 / 1.43), "FA (Fly ash)": R(0.43 / 1.43), "Sand (type not stated) / B": R(0.71 / 1.43), "W / B": 0.35, "SP / B": 0.01,
     "Curing method": "24 h at room temperature in moulds, then water curing", "Demolding age (days)": 1,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile specimen": "dog-bone (30x30 mm section)", "Tensile test type": "direct"}
for g, pva, pp, st, fc28, ft28, ft14, ft7 in [("ECC 1", 2, 0, 0, 51, 5.53, 2.92, 1.38), ("ECC 2", 0, 2, 0, 47.8, 4.55, 2.29, 1.23), ("ECC 3", 0, 0, 2, 54.1, 7.24, 4.19, 2.09),
                                              ("HECC 1", 1.35, 0.65, 0, 48, 4.94, 2.66, 1.79), ("HECC 2", 1.35, 0, 0.65, 51.8, 6.3, 3.79, 1.84),
                                              ("HECC 3", 1, 1, 0, 50.85, 5.09, 2.73, 1.85), ("HECC 4", 1, 0, 1, 52.1, 6.39, 3.84, 1.91)]:
    for age, fc, ft in [(28, fc28, ft28), (14, None, ft14), (7, None, ft7)]:
        d = {"PVA fiber (vol%)": pva, "PP fiber (vol%)": pp, "Steel fiber (vol%)": st, "Total fiber (vol%)": R(pva + pp + st, 2),
             "Curing time (days)": age - 1, "Test age (days)": age, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
             "Source table/page": "Table 2 (fibres), Table 3 (mix), Sec. 3.1-3.2 text (fc 28 d, ft 7/14/28 d)",
             "Conversions / notes": f"{g}: Table 3 cement 1 : FA 0.43 : sand 0.71 (read as mass ratios to cement; binder = 1.43), W/B 0.35, SP 1% (taken as of binder). "
                                    "OPC 53 grade, class F FA. Dog-bone gauge length stated inconsistently (60 mm and 80 mm) - left blank. "
                                    "fc at 3/7/14 d only in Fig. 6. Conclusions mislabel the best hybrid ('HECC 3'); values taken from the per-mix listings in Sec. 3."}
        if pva:
            d.update({"PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42.5})
        if pp:
            d.update({"PP length (mm)": 10, "PP diameter (µm)": 37})
        if st:
            d.update({"Steel length (mm)": 12, "Steel diameter (µm)": 300, "Steel tensile strength (MPa)": 2000, "Steel elastic modulus (GPa)": 175})
        add(b, **d)

# ---------------------------------------------------------------- 10 Tulun et al. 2025 (steel / macro-synthetic / PVA, binary & ternary)
B = 700 + 350 + 50
b = {"Article Name": "Experimental study of mechanical and durability properties in hybrid binary and ternary fiber-reinforced ECC",
     "Author": "Tulun M.K., Sobhani J., Mirhosseini S.M., Zeighami E., Basiri M.R.", "Year": 2025, "DOI / URL": "https://doi.org/10.3389/fbuil.2025.1603359",
     "OPC / Cement": R(700 / B), "GGBS": R(350 / B), "SF (Silica fume)": R(50 / B), "W / B": R(220 / B), "SS / B (Silica sand)": R(500 / B),
     "QP / B (Quartz powder)": R(200 / B), "Binder content (kg/m³)": B,
     "Curing method": "24 h under damp burlap at 25 °C, then lime-saturated water 23±2 °C (ASTM C511)", "Curing temperature (°C)": 23, "Demolding age (days)": 1}
for g, s, f_, p, fc7, fc28, fc90, fsp in [("S0F0P0", 0, 0, 0, 64.2, 91.2, 104, 7.32), ("S10F0P1", 10, 0, 1, 88.1, 91.8, 95.6, 7.16), ("S10F0P2", 10, 0, 2, 73.2, 94.8, 98.1, 7.32),
                                         ("S20F0P1", 20, 0, 1, 80.6, 89.7, 97.8, 7.73), ("S20F0P2", 20, 0, 2, 77, 89, 103.9, 7.93), ("S0F10P1", 0, 10, 1, 70.9, 83.8, 94.8, 7.55),
                                         ("S0F10P2", 0, 10, 2, 80, 83, 96.1, 6.62), ("S0F20P1", 0, 20, 1, 69.2, 76.8, 83.2, 5.24), ("S0F20P2", 0, 20, 2, 77.1, 84, 93.9, 5.93),
                                         ("S10F10P1", 10, 10, 1, 65, 79.4, 90.4, 7.91), ("S20F10P1", 20, 10, 1, 75.4, 89.7, 94, 8.93), ("S10F20P1", 10, 20, 1, 68.5, 83.2, 92.8, 8.87),
                                         ("S10F10P2", 10, 10, 2, 87.7, 93.8, 103.3, 7.68), ("S20F10P2", 20, 10, 2, 76.4, 86.7, 97.6, 7.86), ("S10F20P2", 10, 20, 2, 69.7, 71.7, 88, 8.99)]:
    vs, vf, vp = R(s / 7850 * 100, 3), R(f_ / 900 * 100, 3), R(p / 1300 * 100, 3)
    for age, fc in [(7, fc7), (28, fc28), (90, fc90)]:
        d = {"Steel fiber (vol%)": vs, "PP fiber (vol%)": vf, "PVA fiber (vol%)": vp, "Total fiber (vol%)": R(vs + vf + vp, 3),
             "Curing time (days)": age - 1, "Test age (days)": age, "Compressive strength (MPa)": fc,
             "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
             "Source table/page": "Table 2 (fibres), Table 3 + footnote (mix, kg/m3), Table 5 (fc)" + (", Table 8 (splitting)" if age == 28 else ""),
             "Conversions / notes": f"{g}: steel {s}, synthetic {f_}, PVA {p} kg/m3 -> vol% with paper densities 7.85/0.9/1.3 g/cm3. Table 3 parenthetical values "
                                    "(0.05/0.1/0.5/1) do not match vol% and are unexplained - not used. Binder = OPC 700 + GGBFS 350 + SF 50 = 1100 kg/m3 "
                                    "(paper: W/C(OPC+GGBFS+SF)=0.2). Micro silica 200 kg/m3 (98% SiO2) is excluded from binder by the authors; entered in QP/B as siliceous filler. "
                                    "Silica sand 500 kg/m3; PCE SP dosage not given. Low fibre dosages (<=1.4 vol%); strain hardening not demonstrated."}
        if f_:
            d["Conversions / notes"] += " VERIFY: 'synthetic fiber' (60 mm, 0.4-0.5 mm, 570-660 MPa, E 6 GPa, 0.9 g/cm3) type not named; entered in PP column."
            d.update({"PP length (mm)": 60})
        if p:
            d.update({"PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1400, "PVA elastic modulus (GPa)": 32})
        if s:
            d.update({"Steel length (mm)": 60, "Steel diameter (µm)": 900, "Steel tensile strength (MPa)": 1600, "Steel elastic modulus (GPa)": 200})
            d["Conversions / notes"] += " Steel = hooked-end."
        if age == 28:
            d.update({"Tensile strength (MPa)": fsp, "Tensile specimen": "cylinder 150x300", "Tensile test type": "splitting"})
            if g == "S0F0P0":
                d["Conversions / notes"] += " Splitting strength of plain mix: Table 8 gives 7.32 MPa, text says 6.86 MPa (Table value used)."
        add(b, **d)

# ---------------------------------------------------------------- 11 Jacintho et al. 2024 (UHPC, steel + low-dose PVA)
B = 1 + 0.194
b = {"Article Name": "Mechanical Properties of Ultra-High-Performance Concrete with Steel and PVA Fibers",
     "Author": "Jacintho A.E.P.G.A., dos Santos A.M., Santos Junior G.B., Krahl P.A., Barbante G.G., Pimentel L.L., Forti N.C.S.", "Year": 2024,
     "DOI / URL": "https://doi.org/10.3390/ma17235990",
     "OPC / Cement": R(1 / B), "SF (Silica fume)": R(0.194 / B), "W / B": R(0.19 / B), "SS / B (Silica sand)": R(1.1 / B), "QP / B (Quartz powder)": R(0.1 / B),
     "SP / B": R(0.04 / B), "Sand max size (µm)": 516,
     "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2160, "Steel elastic modulus (GPa)": 210,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75x150"}
for g, st, pva, fc7, fc28, E in [("T1", 1.00, 0.19, 60.94, 122.94, 46.14), ("T2", 1.15, 0.08, 89.36, 110.13, 41.44), ("T3", 1.15, 0.38, 82.89, 124.21, 43.63),
                                 ("T4", 1.50, 0.00, 91.83, 125.54, 46.08), ("T5", 1.50, 0.19, 87.15, 106.00, 40.90), ("T6", 1.50, 0.19, 66.99, 131.67, 48.24),
                                 ("T7", 1.50, 0.19, 71.00, 135.86, 47.27), ("T8", 1.50, 0.30, 93.77, 106.29, 38.23), ("T9", 1.85, 0.08, 99.63, 114.88, 40.33),
                                 ("T10", 1.85, 0.38, 90.25, 119.94, 39.06), ("T11", 2.00, 0.19, 112.67, 131.04, 41.70)]:
    for age, fc in [(7, fc7), (28, fc28)]:
        d = {"Steel fiber (vol%)": st, "PVA fiber (vol%)": pva, "Total fiber (vol%)": R(st + pva, 2), "Test age (days)": age, "Compressive strength (MPa)": fc,
             "Source table/page": "Sec. 2.1 (materials/fibres), Sec. 2.2 (mix ratio), Table 2 (specimens), Table 4 (fc 7/28 d)",
             "Conversions / notes": f"{g}: mix ratio cement 1 : quartz sand 1.1 : quartz powder 0.1 : silica fume 0.194 : water 0.19 (w/c) : PCE additive 0.04 by mass; "
                                    f"binder = cement + SF = 1.194, all /B. CP V-ARI (Type III) cement; sand max 0.516 mm, quartz powder max 0.052 mm. "
                                    f"CCRD design (T5-T7 are repeated centre points). 28-d E = {E} GPa. Curing regime not reported. Only bending tension (optimized mix) - no direct tension."}
        if pva:
            d.update({"PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 41})
        add(b, **d)

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows, columns=H)
out = os.path.join(D, "w2_hybrid.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", out)
