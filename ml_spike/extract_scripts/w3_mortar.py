# Builder for fibre-reinforced mortar / HPFRCC additions (w3_mortar.csv)
# Topic: fibre-reinforced mortars (no coarse aggregate) with PVA, PP, glass, basalt, carbon, steel (+1 PE HPFRCC) fibres,
# SF / FA / slag blends, 3D-printable fibre mortar. Every number below was read from the cited paper's full text
# (Europe PMC fullTextXML). Derived quantities are explained in "Conversions / notes".
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
    r = {k: v for k, v in r.items() if v is not None}
    for k in r:
        assert k in H, k
    rows.append(r)


R = lambda x, n=4: round(x, n)

# ---------------------------------------------------------------- 1 Malek et al. 2021 (recycled glass fibre mortar)
B = 468
b = {"Article Name": "Mechanical and Material Properties of Mortar Reinforced with Glass Fiber: An Experimental Study",
     "Author": "Małek M., Jackowski M., Łasica W., Kadela M., Wachowski M.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14030698",
     "OPC / Cement": 1, "W / B": R(207 / B), "M-sand / B": R(1598 / B), "Sand max size (µm)": 2000, "Binder content (kg/m³)": B,
     "Curing method": "cast at 21 °C / 50% RH, stored in water (EN 12390-2) until test", "Curing time (days)": 28, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
     "Tensile specimen": "cylinder 150x300 (splitting, EN 12390-6)", "Tensile test type": "splitting",
     "Source table/page": "Table 4 (mix, kg/m3), Table 3 + Sec. 2.2 (fibre), Table 7 (fc, splitting, flexural)"}
for mid, g, fc, fst, ff in [("BM", 0, 47, 2.86, 8.0), ("600GF", 600, 53, 3.51, 9.0), ("1200GF", 1200, 57, 4.11, 10.0), ("1800GF", 1800, 61, 5.65, 10.4)]:
    vf = R(g / 1000 / 2700 * 100, 4)
    add(b, **{"Glass fiber (vol%)": vf, "Total fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": fst,
              "Conversions / notes": f"{mid}: Table 4 kg/m3 CEM 52.5 cement 468, water 207, crushed granite aggregate 0-2 mm 1598 (put in M-sand column), "
              f"glass fibre {g} g/m3; all /cement. Fibre vol% = {g} g/m3 / 2700 kg/m3 (paper prints density '2.7 kg/m3', read as 2.7 g/cm3). "
              "Recycled bottle-glass fibres ~49 mm long, flat 838x555 µm section, 1.7 GPa, 72 GPa. Polycarboxylate admixture used (dose not given). "
              f"3-point flexural strength (40x40x160) = {ff} MPa."})

# ---------------------------------------------------------------- 2 Safiuddin et al. 2021 (pitch carbon fibre mortar + SF)
b = {"Article Name": "Performance and Cost-Effectiveness of Short Pitch-Based Carbon Fiber Reinforced Mortar Composite",
     "Author": "Safiuddin M., Abdel-Sayed G., Hearn N.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14164693",
     "OPC / Cement": 0.85, "SF (Silica fume)": 0.15, "Sand max size (µm)": 2360,
     "Curing method": "demoulded 24 h, water-cured at 23±2 °C until test", "Curing temperature (°C)": 23, "Curing time (days)": 27,
     "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
     "Tensile specimen": "beam 400x100x75 (flexure, ASTM C1018)", "Tensile test type": "flexural",
     "Source table/page": "Table 1 (materials), Table 2 (mix, kg/m3), Table 4 (fc, flexural)"}
for mid, Bk, sand, cf, cfk, w, sp, fc, ff, ffc in [
        ("OPCM", 1124.6, 556.2, 0, 0, 394.1, 11.3, 39.0, 5.8, 5.8), ("CFRM1", 1079.1, 533.7, 1, 18.5, 372.8, 21.6, 49.8, 8.0, 6.6),
        ("CFRM2", 1056.5, 522.4, 2, 37.0, 359.8, 31.7, 56.7, 9.0, 7.0), ("CFRM3", 1033.7, 511.3, 3, 55.5, 346.7, 41.4, 63.0, 9.9, 7.4),
        ("CFRM4", 1011.1, 500.0, 4, 74.0, 334.1, 50.6, 47.7, 10.4, 8.1)]:
    add(b, **{"W / B": R(w / Bk), "River sand / B": R(sand / Bk), "SP / B": R(sp / Bk, 5), "Binder content (kg/m³)": Bk,
              "Carbon fiber (vol%)": cf, "Total fiber (vol%)": cf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
              "Conversions / notes": f"{mid}: Table 2 kg/m3 binder {Bk} (cement + SF, SF = 15% cement replacement by mass per text), river sand {sand}, "
              f"carbon fibre {cf} vol% ({cfk} kg/m3), water {w}, naphthalene SP {sp}; all /binder (W/B 0.35, S/B 0.5 design). "
              "Pitch carbon fibre 10 mm, 17 µm, 1770 MPa, 180 GPa. Tensile value = 28-d flexural strength. "
              f"Companion paper (doi 10.3390/ma15051657, same mixes, not added separately) reports 28-d first-crack flexural {ffc} MPa and 7-d flexural values."})

# ---------------------------------------------------------------- 3 Barnat-Hunek et al. 2018 (basalt fibre mortar)
b = {"Article Name": "Effect of Polysiloxanes on Roughness and Durability of Basalt Fibres–Reinforced Cement Mortar",
     "Author": "Barnat-Hunek D., Łagód G., Fic S., Jarosz-Hadam M.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/polym10040420",
     "OPC / Cement": 1, "Sand max size (µm)": 2000,
     "Curing method": "24 h in mould at lab conditions, then climatic chamber 23.5 °C / 73.5% RH", "Curing time (days)": 28,
     "Curing temperature (°C)": 23.5, "Curing RH (%)": 73.5, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160",
     "Tensile specimen": "prism 40x40x160 (EN 196-1 bending)", "Tensile test type": "flexural",
     "Source table/page": "Table 1 (mix, kg/m3), Table 3 + Sec. 2 (fibre), Table 6 (fc, flexural)"}
for mid, c, adm, bf, fc, ff in [("M0", 280, 0, 0, 9.53, 6.10), ("M0.5", 280, 0, 0.5, 9.01, 6.74), ("M1", 280, 0, 1, 8.31, 7.87), ("M1.5", 280, 0, 1.5, 7.63, 8.96),
                                ("H0", 274.4, 5.49, 0, 7.23, 5.32), ("H0.5", 274.4, 5.49, 0.5, 7.06, 5.98), ("H1", 274.4, 5.49, 1, 6.41, 6.47),
                                ("H1.5", 274.4, 5.49, 1.5, 5.68, 7.06)]:
    add(b, **{"W / B": R(126 / c), "SS / B (Silica sand)": R(1483 / c), "Binder content (kg/m³)": c,
              "Basalt fiber (vol%)": bf, "Total fiber (vol%)": bf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
              "Conversions / notes": f"{mid}: Table 1 kg/m3 CEM I 32.5R {c}, quartz sand <2 mm 1483, water 126, basalt fibre {bf} vol% "
              f"({R(bf * 26.4, 1)} kg/m3); hydrophobic admixture {adm} kg/m3 (no column; series H). All /cement. Basalt ~24 mm long, 11-18 µm, 2800-4500 MPa, 89-110 GPa. "
              "Note the low fc (lean mortar, ~5.3 sand/cement)."})

# ---------------------------------------------------------------- 4 Fan et al. 2020 (PE fibre CAC-GGBFS / OPC-GGBFS SHCC mortar)
b = {"Article Name": "Durability of Fibre-Reinforced Calcium Aluminate Cement (CAC)–Ground Granulated Blast Furnace Slag (GGBFS) Blended Mortar after Sulfuric Acid Attack",
     "Author": "Fan W., Zhuge Y., Ma X., Chow C.W.K., Gorjian N., Oh J.-A., Duan W.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13173822",
     "Curing method": "24 h in mould at ambient temperature, then curing room (conditions not stated)", "Curing time (days)": 28,
     "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50x50x50",
     "Source table/page": "Table 1 (fibre), Table 2 (mix, kg/m3), Sec. 3.4 text (28-d fc), Table 5 (0-day exposure tension)"}
for mid, cem, cemcol, slag, hpmc, pce, pe, fc, ftc, ftu, eps in [
        ("CAC-GGBFS 1.5 (control)", 480, "CAC (Calcium aluminate cement)", 720, 0, 3.7, 0, 49.42, None, None, None),
        ("CAC-GGBFS 1.5PE", 480, "CAC (Calcium aluminate cement)", 720, 0.5, 2.2, 1, 59.76, 4.05, 5.46, 5.78),
        ("CAC-GGBFS 3.8PE", 240, "CAC (Calcium aluminate cement)", 954, 0.5, 2.5, 1, 25.54, 2.18, 3.06, 7.42),
        ("OPC-GGBFS 1.5PE", 480, "OPC / Cement", 720, 0.5, 1.14, 1, 74.73, 5.51, 7.32, 4.59)]:
    Bk = cem + slag
    d = {cemcol: R(cem / Bk), "GGBS": R(slag / Bk), "W / B": R(370 / Bk), "SS / B (Silica sand)": R(594 / Bk),
         "HPMC / B (hydroxypropyl methyl cellulose)": R(hpmc / Bk, 5) if hpmc else None, "SP / B": R(pce / Bk, 5), "Binder content (kg/m³)": Bk,
         "Total fiber (vol%)": pe, "Compressive strength (MPa)": fc,
         "Conversions / notes": f"{mid}: Table 2 kg/m3 cement {cem}, GGBFS {slag}, water 370, fine silica sand 594, HPMC {hpmc}, PCE {pce}, PE fibre {'10 (1 vol%)' if pe else '0'}; "
                                "all /(cement+GGBFS). Unexposed 28-d values (acid-exposure series not transcribed). "
                                + ("Text gives 49.42 MPa in Sec. 3.4 and 49.26 MPa in Sec. 2 for the plain mix; 49.42 used." if not pe else
                                   "PE 18 mm, 20 µm, 3000 MPa, 100 GPa, density 970. Tension = dog-bone direct tension (geometry in authors' earlier work).")}
    if pe:
        d.update({"PE fiber (vol%)": pe, "PE length (mm)": 18, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100,
                  "Tensile specimen": "dog-bone", "Tensile test type": "direct", "Tensile strength (MPa)": ftu,
                  "First-cracking strength (MPa)": ftc, "Tensile strain capacity (%)": eps})
    add(b, **d)

# ---------------------------------------------------------------- 5 Drzymala et al. 2025 (PP fibre + SF mortar, direct tension briquettes)
Bk = 846 + 84.6
b = {"Article Name": "Thermoanalytical and Tensile Strength Studies of Polypropylene Fibre-Reinforced Cement Composites Designed for Tunnel Applications",
     "Author": "Drzymała T., Rudnik E., Lewicka S.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma19010142",
     "OPC / Cement": R(846 / Bk), "SF (Silica fume)": R(84.6 / Bk), "W / B": R(215 / Bk), "River sand / B": R(1249 / Bk), "Sand max size (µm)": 2000,
     "SP / B": R(0.02 * 846 / Bk, 5), "Binder content (kg/m³)": Bk, "PP diameter (µm)": None,
     "Curing method": "24 h under foil, demoulded, water 27 d, climatic chamber 60 d at 20 °C / 99% RH, then oven-dried at 105 °C to constant mass; tested at 20 °C (unheated reference)",
     "Curing time (days)": 87, "Curing temperature (°C)": 20, "Demolding age (days)": 1,
     "Tensile specimen": "figure-eight briquette (PN-85/B-04500)", "Tensile test type": "direct",
     "Source table/page": "Table 4 (fibres), Table 5 (mix, kg/m3), Table 10 (ftm at 20 °C)"}
for mid, kg, typ, ft in [("0F", 0, None, 5.03), ("1.8I", 1.8, "I", 5.84), ("3.0I", 3.0, "I", 5.98), ("3.6I", 3.6, "I", 6.05),
                         ("1.8F", 1.8, "F", 5.88), ("3.0F", 3.0, "F", 6.14), ("3.6F", 3.6, "F", 6.28)]:
    vf = R(kg / 910 * 100, 4)
    d = {"PP fiber (vol%)": vf, "Total fiber (vol%)": vf, "Tensile strength (MPa)": ft,
         "Conversions / notes": f"{mid}: Table 5 kg/m3 CEM I 42.5R 846, silica fume 84.6, sand 0/2 mm 1249, water 215, PCE plasticiser 2% of cement, PP {kg} kg/m3; "
                                "all /(cement+SF). PP vol% = kg/m3 / 910. Test age not stated (>= 88 d after 1+27+60 d conditioning). Mean of 3 (Table 10, 20 °C row)."}
    if typ == "I":
        d.update({"PP length (mm)": 12, "PP diameter (µm)": 18})
        d["Conversions / notes"] += " Ignis monofilament 12 mm, 18 µm."
    elif typ == "F":
        d.update({"PP length (mm)": 19})
        d["Conversions / notes"] += " Fibrofor High Grade fibrillated 19 mm, film thickness 80 µm (~400 MPa)."
    add(b, **d)

# ---------------------------------------------------------------- 6 Huang et al. 2022 (nano-SiO2 + PVA, high-volume FA mortar)
b = {"Article Name": "Effect of Nano-SiO2/PVA Fiber on Sulfate Resistance of Cement Mortar Containing High-Volume Fly Ash",
     "Author": "Huang J., Wang Z., Li D., Li G.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/nano12030323",
     "PVA length (mm)": 12, "PVA diameter (µm)": 38, "PVA tensile strength (MPa)": 1092, "PVA elastic modulus (GPa)": 30,
     "Curing method": "demoulded 24 h, air-cured at 25±2 °C to 28 d (watered daily for the first 7 days)", "Curing time (days)": 27,
     "Curing temperature (°C)": 25, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
     "Tensile specimen": "prism 40x40x160 (3-point, span 100)", "Tensile test type": "flexural",
     "Source table/page": "Table 2 (PVA), Table 3 (mix, kg/m3), Table 4 (28-d flexural, fc)"}
res6 = {(0, 0): (4.00, 13.00), (0, .2): (3.65, 11.35), (0, .5): (4.43, 14.98), (0, 1): (5.73, 19.56),
        (.5, 0): (5.21, 22.95), (.5, .2): (4.74, 23.33), (.5, .5): (5.21, 24.81), (.5, 1): (6.16, 25.00),
        (1, 0): (5.00, 19.68), (1, .2): (4.98, 17.90), (1, .5): (5.50, 20.46), (1, 1): (6.28, 22.58),
        (1.5, 0): (5.59, 20.00), (1.5, .2): (5.60, 15.63), (1.5, .5): (6.30, 19.59), (1.5, 1): (7.59, 20.10)}
for (ns, pva), (ff, fc) in res6.items():
    nsk = 550 * ns / 100
    Bk = 550 + nsk
    d = {"OPC / Cement": R(220 / Bk), "FA (Fly ash)": R(330 / Bk), "Nano-SiO2": R(nsk / Bk, 5) if ns else None,
         "W / B": R(220 / Bk), "Sand (type not stated) / B": R(1100 / Bk), "SP / B": R(0.01 * 550 / Bk, 5), "Binder content (kg/m³)": R(Bk, 2),
         "PVA fiber (vol%)": pva, "Total fiber (vol%)": pva, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
         "Conversions / notes": f"NS{ns}-PVA{pva}: Table 3 kg/m3 water 220, cement 220, FA 330 (60% FA), sand 1100, nano-SiO2 {ns} wt%, PVA {pva} vol%, SP 1 wt%. "
                                "NS and SP wt% taken as % of cement+FA mass (basis not stated - VERIFY); NS counted in binder. PVA density 1.3."}
    if not pva:
        for k in ["PVA length (mm)", "PVA diameter (µm)", "PVA tensile strength (MPa)", "PVA elastic modulus (GPa)"]:
            d[k] = None
    r = dict(b); r.update(d)
    add({k: v for k, v in r.items() if v is not None})

# ---------------------------------------------------------------- 7 Chen et al. 2020 (basalt-PP hybrid mortar, orthogonal design)
b = {"Article Name": "Orthogonal Analysis on Mechanical Properties of Basalt–Polypropylene Fiber Mortar",
     "Author": "Chen H., Xie C., Fu C., Liu J., Wei X., Wu D.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13132937",
     "OPC / Cement": 1, "W / B": 0.4, "River sand / B": 3, "SP / B": 0.01,
     "Curing method": "standard curing room 20±2 °C, RH > 95%", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
     "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7x70.7x70.7",
     "Tensile specimen": "prism 40x40x160", "Tensile test type": "flexural",
     "Source table/page": "Tables 1-2 (fibres), Sec. 2.3 (mix ratio), Table 5 (28-d fc, flexural)"}
for no, bl, pl, bv, pv, fc, ff in [(0, 0, 0, 0, 0, 18.73, 8.66), (1, 6, 6, .3, .3, 16.05, 11.50), (2, 9, 19, .1, .2, 20.17, 10.08), (3, 12, 19, .3, .4, 18.71, 10.32),
                                    (4, 18, 6, .1, .1, 20.18, 10.76), (5, 6, 9, .1, .4, 23.30, 11.33), (6, 9, 3, .3, .1, 19.58, 10.57), (7, 12, 3, .1, .3, 20.87, 10.59),
                                    (8, 18, 9, .3, .2, 19.76, 11.14), (9, 6, 3, .4, .2, 25.14, 11.62), (10, 9, 9, .2, .3, 19.54, 11.45), (11, 12, 9, .4, .1, 25.18, 11.41),
                                    (12, 18, 3, .2, .4, 26.12, 10.98), (13, 6, 19, .2, .1, 25.85, 11.51), (14, 9, 6, .4, .4, 18.76, 12.01), (15, 12, 6, .2, .2, 18.46, 11.50),
                                    (16, 18, 19, .4, .3, 21.92, 11.39)]:
    d = {"Basalt fiber (vol%)": bv, "PP fiber (vol%)": pv, "Total fiber (vol%)": R(bv + pv, 2), "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
         "Conversions / notes": f"Test {no}: cement:sand 1:3, w/c 0.4, PCE 1% of cement (blank group; fibres added by volume). P.O 42.5, river sand FM 2.36. "
                                f"Basalt {bl} mm (7-15 µm, 3000-4800 MPa, 91-110 GPa) {bv}%; PP {pl} mm (31 µm, >=460 MPa) {pv}%. "
                                "Flexural strengths are high relative to fc (as printed in Table 5)."}
    if pv:
        d.update({"PP length (mm)": pl, "PP diameter (µm)": 31})
    add(b, **d)

# ---------------------------------------------------------------- 8 Li et al. 2025 (hydrophobic basalt fibre mortar)
b = {"Article Name": "Effect of basalt fiber content on mechanical properties of hydrophobic mortar",
     "Author": "Li Y., Wang Q., Zheng X., Zhang R., Wang N.", "Year": 2025, "DOI / URL": "https://doi.org/10.1038/s41598-025-90138-5",
     "OPC / Cement": 1, "W / B": 0.45, "Sand max size (µm)": 300,
     "Curing method": "covered 24 h, demoulded, curing chamber 23 °C / 95% RH", "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 95,
     "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7x70.7x70.7",
     "Source table/page": "Table 1 (fibre), Table 2 (mix, g), Table 3 (fc)"}
for no, sand, bf, fc in [(1, 0, 0, 9.12), (2, 1000, 0, 23.15), (3, 1000, 1, 24.36), (4, 1000, 1.5, 25.59), (5, 1000, 2, 25.21)]:
    add(b, **{"River sand / B": R(sand / 1000) if sand else None, "Basalt fiber (vol%)": bf, "Total fiber (vol%)": bf, "Compressive strength (MPa)": fc,
              "Conversions / notes": f"Mix {no}: Table 2 PO 42.5 cement 1000 g, water 450 g, river sand (<300 µm) {sand} g, stearic acid 4 g (hydrophobic agent, no column; 0.004/B), "
              f"basalt fibre {bf} vol% (6 mm, 15 µm, 2400 MPa, 100 GPa). " + ("Mix 1 has no sand (paste)." if not sand else "")})

# ---------------------------------------------------------------- 9 Wang et al. 2021 (PVA HPFRM for pipelines; tap-water reference only)
b = {"Article Name": "Durability Study on High-Performance Fiber-Reinforced Mortar under Simulated Wastewater Pipeline Environment",
     "Author": "Wang T., Zhao Y., Ma B., Zeng C.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14143781",
     "Sand max size (µm)": None, "Compressive specimen": "cube", "Compressive specimen size (mm)": "40x40x40",
     "Source table/page": "Table 1 (mix, weight ratio), Sec. 2.1 (PVA), Sec. 3 text (fc in environment III, tap water)"}
for mid, fa, sf, pva, age, fc, cm, ct in [
        ("M", 0.19, 0.08, 1.5, 7, 78.5, "water 7 d (value at start of exposure)", 7), ("M", 0.19, 0.08, 1.5, 127, 96.8, "water 7 d + tap water 120 d (environment III)", 127),
        ("P", 0, 0, 0, 7, 80.5, "water 7 d (value at start of exposure)", 7), ("P", 0, 0, 0, 127, 102.5, "water 7 d + tap water 120 d (environment III)", 127)]:
    Bk = 1 + fa + sf
    d = {"OPC / Cement": R(1 / Bk), "FA (Fly ash)": R(fa / Bk) if fa else None, "SF (Silica fume)": R(sf / Bk) if sf else None,
         "W / B": R(0.26 / Bk), "SS / B (Silica sand)": R(1.4 / Bk), "PVA fiber (vol%)": pva, "Total fiber (vol%)": pva,
         "Curing method": cm, "Curing time (days)": ct, "Test age (days)": age, "Compressive strength (MPa)": fc,
         "Conversions / notes": f"{mid}: Table 1 weight ratio PC 1, FA {fa}, SF {sf}, silica sand 1.4, water/cement 0.26 (W/B = 0.26/{Bk}), SP 0.12% by weight (basis not stated, not filled), "
                                f"PVA {pva} vol% (Kuraray, 12 mm, 40 µm, 1.6 GPa, >38 GPa). Text: fc of M and P after 120 d in tap water 'increasing from 78.5 and 80.5 MPa "
                                "to 96.8 and 102.5 MPa'. VERIFY: start values assigned to age 7 d (end of initial water curing), end values to 7+120 = 127 d. "
                                "Acid / acid-alkali exposure results not transcribed."}
    if pva:
        d.update({"PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 38})
    add(b, **d)

# ---------------------------------------------------------------- 10 Kaushik et al. 2023 (3D printable basalt-fibre mortar, factorial design)
b = {"Article Name": "Optimisation of Mix Proportion of 3D Printable Mortar Based on Rheological Properties and Material Strength Using Factorial Design of Experiment",
     "Author": "Kaushik S., Sonebi M., Amato G., Das U.K., Perrot A.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16041748",
     "W / B": 0.41, "Sand max size (µm)": 1180,
     "Curing method": "24 h at 100% RH / 20 °C, then water-cured to test age", "Curing temperature (°C)": 20, "Demolding age (days)": 1,
     "Tensile test type": "flexural",
     "Source table/page": "Table 3-4 (factor levels, mix), Sec. 2.1 (materials), Table 5 (7/28-d flexural, fc; cast and printed)"}
mix10 = {1: (550, 20, 1, 2), 2: (650, 5, 1, 4), 3: (650, 5, 3, 2), 4: (650, 5, 3, 4), 5: (550, 5, 3, 2), 6: (550, 20, 1, 4), 7: (650, 5, 1, 2), 8: (650, 20, 1, 4),
         9: (550, 20, 3, 4), 10: (550, 20, 3, 2), 11: (650, 20, 3, 4), 12: (650, 20, 1, 2), 13: (550, 5, 1, 2), 14: (650, 20, 3, 2), 15: (550, 5, 1, 4),
         16: (550, 5, 3, 4), 17: (600, 12.5, 2, 3), 18: (600, 12.5, 2, 3), 19: (600, 12.5, 2, 3), 20: (600, 12.5, 2, 3)}
NP = None
res10 = {1: (5.4, 22.9, NP, NP, 5.9, 40.3, NP, NP), 2: (7.9, 48.0, 7.7, 43.7, 10.7, 57.9, 11.3, 55.2), 3: (7.5, 41.6, NP, NP, 8.9, 43.9, NP, NP),
         4: (9.1, 47.6, 9.7, 40.6, 10.8, 66.4, 12.5, 53.8), 5: (5.9, 24.1, NP, NP, 7.3, 32.8, NP, NP), 6: (8.8, 42.8, 9.5, 38.5, 10.6, 53.4, 11.4, 44.8),
         7: (7.3, 43.0, 7.6, 37.5, 9.6, 48.0, 10.9, 45.9), 8: (8.8, 51.9, 9.0, 47.8, 9.3, 61.2, 9.9, 53.1), 9: (9.0, 42.7, 9.3, 38.1, 10.4, 52.2, 11.9, 43.1),
         10: (6.2, 33.6, NP, NP, 7.9, 37.4, NP, NP), 11: (8.1, 52.1, 8.9, 49.7, 10.2, 58.2, 11.8, 52.5), 12: (7.6, 43.7, 8.2, 39.6, 9.4, 57.4, 10.1, 53.0),
         13: (5.4, 29.2, NP, NP, 6.4, 41.9, NP, NP), 14: (7.9, 43.9, 8.8, 42.5, 9.9, 60.5, 11.6, 54.2), 15: (9.2, 43.0, 9.5, 41.3, 10.3, 50.0, 11.6, 46.1),
         16: (9.3, 47.2, 10.7, 44.1, 9.9, 48.3, 11.7, 46.5), 17: (8.5, 44.5, 9.0, 37.1, 10.3, 53.6, 11.8, 45.3), 18: (8.3, 46.4, 9.3, 37.3, 10.1, 48.0, 11.4, 46.1),
         19: (8.5, 41.0, 9.1, 38.4, 9.7, 52.5, 11.2, 47.6), 20: (8.4, 39.1, 9.1, 37.6, 9.9, 48.3, 11.2, 46.0)}
for m, (cem, fa, ba, sp) in mix10.items():
    Bk = cem / (1 - fa / 100)
    vf = R(ba / 2650 * 100, 4)
    r = res10[m]
    for age, (ftc, fcc, ftl, fcl) in [(7, r[0:4]), (28, r[4:8])]:
        for mode, ft, fc in [("cast", ftc, fcc), ("printed", ftl, fcl)]:
            if ft is None and fc is None:
                continue
            add(b, **{"OPC / Cement": R(1 - fa / 100), "FA (Fly ash)": R(fa / 100), "SP / B": R(sp / Bk, 5), "Binder content (kg/m³)": R(Bk, 1),
                      "Basalt fiber (vol%)": vf, "Total fiber (vol%)": vf, "Curing time (days)": age - 1, "Test age (days)": age,
                      "Compressive specimen": "cube (mould-cast)" if mode == "cast" else "cube cut from 3 printed layers",
                      "Compressive specimen size (mm)": "50x50x50" if mode == "cast" else "~50 (cut, see paper)",
                      "Tensile specimen": "prism 50x50x200 mould-cast (3-point, BS EN 1015-11)" if mode == "cast" else "3-layer printed beam ~42x42x180 (3-point)",
                      "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
                      "Conversions / notes": f"Mix {m} ({mode}): CEM I 52.5N {cem} kg/m3, fly ash {fa}%, basalt fibre {ba} kg/m3 (12.7 mm, SG 2.65 -> {vf} vol%), SP {sp} kg/m3, "
                                             f"w/b 0.41, sand <=1.18 mm adjusted for constant volume (content not reported). VERIFY: FA % taken as mass % of binder "
                                             f"(cement + FA), binder = {R(Bk, 1)} kg/m3. Mixes 17-20 are replicate centre points."
                                             + (" Printed values for flexural use the printed-member (aligned-fibre) test." if mode == "printed" else "")})

# ---------------------------------------------------------------- 11 Alshijlawi et al. 2026 (PP fibre mortar, unheated reference)
b = {"Article Name": "Performance of Polypropylene Fiber-Reinforced Mortar Exposed to Elevated Temperatures",
     "Author": "Alshijlawi M., Mahmoud Hama S., Abdulhamed M.A., Aidan I.A., Rajab N.A., Hameed Fayyadh A.", "Year": 2026,
     "DOI / URL": "https://doi.org/10.12688/f1000research.175541.2",
     "OPC / Cement": 1, "W / B": 0.45, "River sand / B": 3, "SP / B": 0.01, "Sand max size (µm)": 4250, "Binder content (kg/m³)": 550,
     "Curing method": "demoulded 24 h, immersed in tap water at 20±2 °C", "Curing time (days)": 27, "Curing temperature (°C)": 20, "Demolding age (days)": 1,
     "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50x50x50",
     "Tensile specimen": "prism 50x50x160 (ASTM C348)", "Tensile test type": "flexural",
     "Source table/page": "Table 1 (mix, kg/m3), Table 2 (specimens), Table 4 (fc), Table 6 (flexural); unheated rows only"}
for pp, fc, ff in [(0, 59.36, 10.50), (0.5, 54.77, 13.3125), (1.0, 47.88, 15.075), (1.5, 46.61, 14.325)]:
    d = {"PP fiber (vol%)": pp, "Total fiber (vol%)": pp, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
         "Conversions / notes": f"PP {pp}%: Table 1 kg/m3 OPC 550, river sand 1650, water 247.5, SP 1% of cement; PP {pp} vol%. PP 12 mm, 18 µm, 0.91 g/cm3. "
                                "Unheated ('0 °C' rows in Tables 4/6 = ambient reference). Elevated-temperature results not transcribed."}
    if pp:
        d.update({"PP length (mm)": 12, "PP diameter (µm)": 18})
    add(b, **d)

# ---------------------------------------------------------------- 12 Li et al. 2021 (chopped carbon fibre mortar, fibre length)
cem12 = 1 / (1 / 3.15 + 0.4 + 1.05 / 2.65 + 0.01 / 1.78) * 1000
vf12 = R(0.01 * cem12 / 1780 * 100, 3)
b = {"Article Name": "Static and Dynamic Performances of Chopped Carbon-Fiber-Reinforced Mortar and Concrete Incorporated with Disparate Lengths",
     "Author": "Li Y.F., Lee K.F., Ramanathan G.K., Cheng T.W., Huang C.H., Tsai Y.K.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14040972",
     "OPC / Cement": 1, "W / B": 0.4, "Sand (type not stated) / B": 1.05,
     "Curing method": "cured 28 d (method not stated)", "Curing time (days)": 28, "Test age (days)": 28,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
     "Tensile specimen": "prism 70x70x280 (3-point, ASTM C293)", "Tensile test type": "flexural",
     "Source table/page": "Table 2 (fibre), Sec. 2.4 text (mix), Table 4 (fc mortar), Table 6 (flexural mortar)"}
for mid, L, fc, ff in [("B-M", 0, 32.54, 7.57), ("L6-M", 6, 39.75, 9.43), ("L12-M", 12, 37.10, 9.77), ("L24-M", 24, 36.22, 10.76)]:
    add(b, **{"Carbon fiber (vol%)": vf12 if L else 0, "Total fiber (vol%)": vf12 if L else 0, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
              "Conversions / notes": f"{mid}: w/c 0.4, sand = 105% of cement mass, carbon fibre {'1% of cement mass, length ' + str(L) + ' mm' if L else 'none'} "
              "(7 µm, 4900 MPa, 250 GPa, 1.78 g/cm3). " + (f"VERIFY: vol% estimated - cement content by absolute volume (cement SG 3.15, sand SG 2.65 assumed, no air) "
              f"= {R(cem12, 0)} kg/m3 -> fibre {R(0.01 * cem12, 1)} kg/m3 / 1780 = {vf12} vol%. " if L else "") +
              "Concrete (CFRC) series of the paper not included."})

# ---------------------------------------------------------------- 13 Smarzewski 2020 (four fibres at 3 vol% in HPCC)
Bk = 947.3 + 54.2
b = {"Article Name": "Comparative Fracture Properties of Four Fibre Reinforced High Performance Cementitious Composites",
     "Author": "Smarzewski P.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13112612",
     "OPC / Cement": R(947.3 / Bk), "SF (Silica fume)": R(54.2 / Bk), "W / B": R(312 / Bk), "Fine sand / B": R(1042 / Bk), "Sand max size (µm)": 1000,
     "SP / B": R(31.2 * 1.07 / Bk, 5), "Binder content (kg/m³)": Bk,
     "Curing method": "48 h under foil at 20±2 °C, then water bath 20±2 °C until 28 d", "Curing time (days)": 26, "Curing temperature (°C)": 20,
     "Demolding age (days)": 2, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
     "Tensile specimen": "cube 100 (splitting, PN-EN 12390-6)", "Tensile test type": "splitting",
     "Source table/page": "Table 1 (mix, kg/m3), Table 2 (fibres), Table 4 (fc, splitting, flexural)"}
for mid, col, kg, rho, fc, fst, ff, extra in [
        ("HPCC-S3%", "Steel fiber (vol%)", 234, 7800, 102.7, 16.2, 7.89, {"Steel length (mm)": 50, "Steel diameter (µm)": 1000, "Steel tensile strength (MPa)": 1060, "Steel elastic modulus (GPa)": 200}),
        ("HPCC-PP3%", "PP fiber (vol%)", 27, 910, 93.8, 7.2, 3.90, {"PP length (mm)": 40, "PP diameter (µm)": 750}),
        ("HPCC-B3%", "Basalt fiber (vol%)", 81, 2700, 68.4, 8.8, 7.2, {}),
        ("HPCC-G3%", "Glass fiber (vol%)", 75, 2500, 83.3, 11.5, 13.3, {})]:
    vf = R(kg / rho * 100, 3)
    add(b, **{col: vf, "Total fiber (vol%)": vf, **extra, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": fst,
              "Conversions / notes": f"{mid}: Table 1 kg/m3 CEM I 52.5R 947.3, silica fume 54.2, sand 0.125/1 mm 1042, water 312 L, SP 31.2 L (x1.07 kg/L), fibre {kg} kg/m3 "
              f"(/ {rho} -> {vf} vol%, nominal 3%). All /(cement+SF). Fibres: steel hooked 50 mm/1 mm/>1060 MPa; PP crimped 40 mm/0.75 mm/>360 MPa; basalt 12 mm/13 µm/>1700 MPa; "
              f"glass 18 mm/14 µm/>1700 MPa. Flexural (notched-beam RILEM) strength {ff} MPa. Strength values given as >= (minimum) for fibre strength."})

# ---------------------------------------------------------------- 14 Ji et al. 2022 (carbon / glass / PVA fibre mortar, pre-freeze-thaw)
b = {"Article Name": "Frost Resistance Investigation of Fiber-Doped Cementitious Composites",
     "Author": "Ji Y., Zou Y., Ma Y., Wang H., Li W., Xu W.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15062226",
     "OPC / Cement": 1, "W / B": 0.5, "Sand (type not stated) / B": 2, "Sand max size (µm)": 2000, "Binder content (kg/m³)": 700,
     "Curing method": "demoulded after 24 h, cured in water at 20±1 °C (duration not stated)", "Curing temperature (°C)": 20, "Demolding age (days)": 1,
     "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160",
     "Tensile specimen": "prism 40x40x160 (GB/T 17671 bending)", "Tensile test type": "flexural",
     "Source table/page": "Table 3 (fibres), Table 4 (mix), Tables 5-6 (0 freeze-thaw cycles)"}
for mid, col, vf, kg, sp, fc, ff in [("Control", None, 0, 0, 0, 42.2, 4.8), ("Carbon 0.5", "Carbon fiber (vol%)", 0.5, 0.8, 5, 46.8, 6.9),
                                     ("Carbon 1", "Carbon fiber (vol%)", 1, 1.6, 15, 41.6, 7.6), ("Glass 0.5", "Glass fiber (vol%)", 0.5, 2.4, 5, 44.0, 6.4),
                                     ("Glass 1", "Glass fiber (vol%)", 1, 4.8, 15, 37.0, 6.7), ("PVA 0.5", "PVA fiber (vol%)", 0.5, 0.65, 5, 45.5, 6.4),
                                     ("PVA 1", "PVA fiber (vol%)", 1, 1.3, 15, 38.4, 6.5)]:
    d = {"SP / B": R(sp / 700, 5), "Total fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
         "Conversions / notes": f"{mid}: Table 4 kg/m3 cement 700, sand (ISO gradation, max 2 mm) 1400, water 350, SP {sp}, fibre {kg} kg/m3 labelled '{vf}%'. "
                                "VERIFY fibre dosage: paper states vol% (0.5/1), but listed kg/m3 with its densities give only ~0.05/0.1 vol%; labelled vol% used. "
                                "All fibres 10 mm; carbon 3500 MPa/230 GPa, glass 2500 MPa/70 GPa, PVA 1900 MPa/35 GPa. Test age not stated. 0 freeze-thaw cycles."}
    if col:
        d[col] = vf
    if col == "PVA fiber (vol%)":
        d.update({"PVA length (mm)": 10, "PVA tensile strength (MPa)": 1900, "PVA elastic modulus (GPa)": 35})
    add(b, **d)

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows)
# drop DOIs already collected by other agents (e.g. nano12030323 is in w3_nano.csv)
import glob
taken = set()
for f in glob.glob(os.path.join(D, "*.csv")):
    if os.path.basename(f) in ("w3_mortar.csv", "TEMPLATE.csv"):
        continue
    taken |= set(pd.read_csv(f, encoding="utf-8-sig", usecols=["DOI / URL"])["DOI / URL"].dropna().str.lower())
dup = sorted(set(df["DOI / URL"].str.lower()) & taken)
if dup:
    print("dropping DOIs present in other agents' files:", dup)
    df = df[~df["DOI / URL"].str.lower().isin(dup)]
for c in H:
    if c not in df.columns:
        df[c] = None
df = df[H]
out = os.path.join(D, "w3_mortar.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", out)
