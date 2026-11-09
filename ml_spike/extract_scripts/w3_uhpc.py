# Builder for w3_uhpc.csv -- UHPC / RPC with steel fibres (fibre shape/length/dosage, SF content, w/b,
# steam vs standard curing, SCM replacement). All numbers transcribed from the papers' full text
# (Europe PMC fullTextXML for MDPI / Sci Rep; publisher HTML for Frontiers and SpringerOpen IJCSM).
import os, csv, re, glob
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
with open(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig") as f:
    H = next(csv.reader(f))

BINDER_COLS = ["OPC / Cement", "SAC (Calcium sulfoaluminate cement)", "CAC (Calcium aluminate cement)", "GGBS",
               "FA (Fly ash)", "SF (Silica fume)", "Metakaolin", "Limestone powder", "Diatomite", "Nano-SiO2",
               "Recycled powder (C&D waste)", "Dolomite powder", "Pond ash (PA)", "Other binder", "RHA (Rice husk ash)",
               "EAFD (Electric arc furnace dust)", "Reactive MgO", "CKD (Cement kiln dust)"]
FIB = ["PE fiber (vol%)", "PVA fiber (vol%)", "Steel fiber (vol%)", "PBO fiber (vol%)", "PP fiber (vol%)", "Glass fiber (vol%)",
       "PET fiber (vol%)", "Basalt fiber (vol%)", "Carbon fiber (vol%)"]
rows = []


def r4(x):
    return round(x, 4) if isinstance(x, float) else x


def add(base, **kw):
    d = dict(base)
    d.update(kw)
    for k in d:
        assert k in H, k
    s = sum(float(d.get(k) or 0) for k in BINDER_COLS)
    assert abs(s - 1) < 0.002, (d["Article Name"], s)
    if d.get("Total fiber (vol%)", "") == "":
        d["Total fiber (vol%)"] = sum(float(d.get(k) or 0) for k in FIB)
    rows.append({k: r4(v) for k, v in d.items()})


# ---------------------------------------------------------------- P1 Mousavinezhad et al. 2023 (non-proprietary UHPC, SCMs)
p1 = {"Article Name": "A Comprehensive Study on Non-Proprietary Ultra-High-Performance Concrete Containing Supplementary Cementitious Materials",
      "Author": "Mousavinezhad S.; Gonzales G.J.; Toledo W.K.; Garcia J.M.; Newtson C.M.; Allena S.", "Year": 2023,
      "DOI / URL": "https://doi.org/10.3390/ma16072622", "Sand max size (µm)": 4750,
      "Steel fiber (vol%)": 1.5, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 1900,
      "Curing method": "Demoulded at 24 h, moist cured at 98% RH and 23+/-2 C until testing", "Curing temperature (°C)": 23,
      "Curing RH (%)": 98, "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
      "Tensile specimen": "prism 76x102x406 (ASTM C1609 four-point bending)"}
# mix: cement, SF, FA, pumicite, MK, GGBS, sand, HRWRA ; fc28, fc56 ; MOR, peak
mix1 = [("F10/S10", 839, 104, 104, 0, 0, 0, 919, 59.3, 135.0, 156.5, 18.65, 19.55),
        ("N5/F5/S10", 839, 104, 52, 52, 0, 0, 925, 62.3, 132.0, 156.5, 20.05, 21.25),
        ("N7.5/F2.5/S10", 839, 104, 26, 78, 0, 0, 931, 62.3, 122.5, 155.5, 19.25, 20.80),
        ("N10/S10", 839, 104, 0, 104, 0, 0, 931, 65.3, 116.0, 154.5, 18.75, 20.00),
        ("M5/F5/S10", 839, 104, 52, 0, 52, 0, 913, 68.2, 134.0, 151.5, 19.50, 20.90),
        ("M7.5/F2.5/S10", 839, 104, 26, 0, 78, 0, 921, 68.2, 131.5, 152.0, 19.20, 20.50),
        ("M10/S10", 839, 104, 0, 0, 104, 0, 922, 71.2, 130.5, 152.5, 18.85, 20.40),
        ("G2/F8/S10", 839, 104, 83, 0, 0, 21, 920, 62.3, 134.5, 156.5, 18.60, 19.50),
        ("G4/F6/S10", 839, 104, 62, 0, 0, 42, 921, 65.3, 132.5, 155.5, 18.50, 19.30),
        ("M5/N5/S10", 839, 104, 0, 52, 52, 0, 926, 68.2, 123.0, 153.0, 20.65, 22.25),
        ("G2/M6/N2/S10", 839, 104, 0, 21, 62, 21, 923, 71.2, 131.0, 152.5, 19.50, 21.15),
        ("G2/M9/S9", 839, 94, 0, 0, 94, 21, 926, 71.2, 130.0, 152.5, 19.40, 20.85),
        ("G12/M9/S9", 755, 94, 0, 0, 94, 105, 928, 68.2, 111.5, 148.0, 16.95, 18.00),
        ("M10/N2.5/S7.5", 839, 78, 0, 26, 104, 0, 940, 65.3, 121.5, 142.5, 15.70, 17.00),
        ("M12.5/S7.5", 839, 78, 0, 0, 130, 0, 934, 68.2, 121.0, 142.0, 15.50, 16.40),
        ("M15/S5", 839, 52, 0, 0, 156, 0, 946, 65.3, 116.0, 138.0, 14.20, 15.05)]
for mid, c, sf, fa, np_, mk, gg, sand, sp, fc28, fc56, mor, pk in mix1:
    B = c + sf + fa + np_ + mk + gg
    base = {"OPC / Cement": c / B, "SF (Silica fume)": sf / B, "FA (Fly ash)": fa / B, "Other binder": np_ / B, "Metakaolin": mk / B,
            "GGBS": gg / B, "W / B": 147 / B, "Local sand / B": sand / B, "HRWR / B": sp / B, "Binder content (kg/m³)": B}
    note = (f"Mix {mid}. kg/m3 / binder (cement {c} + SF {sf} + FA {fa} + pumicite {np_} + MK {mk} + GGBFS {gg} = {B}). "
            f"Natural pozzolan (pumicite) in 'Other binder'. Water 147 kg/m3 (w/cm 0.14 nominal). Local sand max 4.75 mm. "
            f"Steel fibre 119 kg/m3 = 1.5 vol% (paper). HRWRA kg/m3 / binder.")
    add(p1, **base, **{"Test age (days)": 28, "Curing time (days)": 28, "Compressive strength (MPa)": fc28,
                       "Tensile strength (MPa)": pk, "First-cracking strength (MPa)": mor, "Tensile test type": "flexural",
                       "Source table/page": "Table 2 (mix), Table 3 (fc), Table 4 (flexural)",
                       "Conversions / notes": note + f" Tensile strength = ASTM C1609 peak flexural strength; First-cracking = MOR (first-peak) {mor} MPa. Flexural test age not stated explicitly (assumed same 28-d row; VERIFY)."})
    add(p1, **base, **{"Test age (days)": 56, "Curing time (days)": 56, "Compressive strength (MPa)": fc56,
                       "Source table/page": "Table 2 (mix), Table 3 (fc)", "Tensile specimen": "", "Conversions / notes": note})

# ---------------------------------------------------------------- P2 Chen et al. 2020 (UHPC SF + ultra-fine silica powder, steel + PP)
p2 = {"Article Name": "Mechanical Properties of Ultra-High Performance Concrete before and after Exposure to High Temperatures",
      "Author": "Chen H.-J.; Yu Y.-L.; Tang C.-W.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13030770",
      "Sand max size (µm)": 850, "Curing method": "Demoulded and kept in laboratory water bath until the day before testing",
      "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
      "Tensile specimen": "cylinder 150x300 (splitting, ASTM C496)", "Tensile test type": "splitting"}
mix2 = [("HPC-1", 196, 1005, 0, 0, 26, 1, 0, 0, 1286, 0, 0, (81.6, 6.6, 4.4), 90.0),
        ("UHPC-1", 187, 774, 167, 21, 25, 1, 0.3, 39, 1231, 0.03, 0.5, (95.7, 12.6, 7.3), 128.1),
        ("UHPC-2", 186, 756, 179, 21, 25, 1, 0.5, 78, 1223, 0.06, 1.0, (107.0, 15.1, 9.6), 127.0),
        ("UHPC-3", 186, 747, 179, 31, 25, 1, 0.3, 59, 1225, 0.03, 0.75, (97.8, 14.7, 10.5), 121.6),
        ("UHPC-4", 186, 744, 191, 21, 25, 1, 0.8, 59, 1223, 0.09, 0.75, (95.6, 12.2, 8.9), 123.6),
        ("UHPC-5", 186, 737, 191, 26, 25, 1, 0.3, 78, 1220, 0.03, 1.0, (111.5, 12.7, 10.8), 125.8)]
for mid, w, c, sf, sfp, sp, va, ppkg, stkg, sand, ppv, stv, (fc7, fr7, fs7), fc28 in mix2:
    B = c + sf + sfp
    base = {"OPC / Cement": c / B, "SF (Silica fume)": sf / B, "Other binder": sfp / B, "W / B": w / B, "SS / B (Silica sand)": sand / B,
            "SP / B": sp / B, "VMA / B": va / B, "Binder content (kg/m³)": B, "Steel fiber (vol%)": stv, "PP fiber (vol%)": ppv}
    if stv:
        base.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2000, "Steel elastic modulus (GPa)": 200})
    if ppv:
        base.update({"PP length (mm)": 12, "PP diameter (µm)": 50})
    note = (f"Mix {mid}. kg/m3 / binder (cement {c} + SF {sf} + ultra-fine silica powder {sfp} = {B}; SFP treated as binder because the paper defines it as cement replacement, put in 'Other binder'; paper W/B 0.195). "
            f"Fine aggregate = quartz sand types I+II (max 850 um). Steel {stkg} kg/m3 and PP {ppkg} kg/m3; vol% from Table 5 (paper). Viscous agent in VMA/B.")
    add(p2, **base, **{"Test age (days)": 7, "Compressive strength (MPa)": fc7, "Tensile strength (MPa)": fs7,
                       "Source table/page": "Table 4-5 (mix), Table 8 (7-d fc, flexural, splitting)",
                       "Conversions / notes": note + f" Tensile strength = 7-d splitting; 7-d flexural strength (ASTM C78, 100x100x360 prism) = {fr7} MPa."})
    add(p2, **base, **{"Test age (days)": 28, "Compressive strength (MPa)": fc28, "Tensile specimen": "", "Tensile test type": "",
                       "Source table/page": "Table 4-5 (mix), Table 9 (28-d fc)", "Conversions / notes": note})
    if mid == "UHPC-1":
        add(p2, **base, **{"Test age (days)": 56, "Compressive strength (MPa)": 155.8, "Tensile strength (MPa)": 9.8,
                           "Source table/page": "Table 4-5 (mix), Table 11 (56-d, room temperature)",
                           "Conversions / notes": note + " 56-d room-temperature reference of the high-temperature series. Tensile strength = splitting; flexural = 13.0 MPa."})

# ---------------------------------------------------------------- P3 Grzeszczyk et al. 2026 (RPC with waste biotite powder)
p3 = {"Article Name": "Waste Powder Biotite as a Factor Enhancing the Flexural Strength of RPC",
      "Author": "Grzeszczyk S.; Rajczyk T.; Matuszek-Chmurowska A.; Jurowski K.; Kaleta-Jurowska A.", "Year": 2026,
      "DOI / URL": "https://doi.org/10.3390/ma19020276", "Sand max size (µm)": 600,
      "Steel fiber (vol%)": 3, "Steel length (mm)": 12, "Steel diameter (µm)": 200,
      "Curing method": "Demoulded after 24 h, cured in water at 20+/-2 C until testing", "Curing temperature (°C)": 20, "Demolding age (days)": 1,
      "Compressive specimen": "prism halves (EN 196-1)", "Compressive specimen size (mm)": "40x40x160 prism halves",
      "Tensile specimen": "prism 40x40x160 (EN 196-1)", "Tensile test type": "flexural",
      "Source table/page": "Table 6 (mix), Table 7 (fc, flexural)"}
mix3 = [("RPC-1", 901, 180, 315, 730, 0, 0, 23, 216, (103.2, 146.6, 167.4), (21.7, 30.5, 33.4)),
        ("RPC-2", 933, 187, 0, 0, 326, 755, 23, 224, (89.8, 115.6, 143.5), (19.5, 27.0, 36.0)),
        ("RPC-3", 910, 182, 0, 737, 319, 0, 23, 218, (99.8, 125.6, 155.2), (26.7, 32.9, 41.2))]
for mid, c, sf, qp, qs, wp, ws, sp, w, fcs, ffs in mix3:
    B = c + sf
    for age, fc, ff in zip((2, 7, 28), fcs, ffs):
        add(p3, **{"OPC / Cement": c / B, "SF (Silica fume)": sf / B, "W / B": w / B, "QP / B (Quartz powder)": qp / B,
                   "SS / B (Silica sand)": qs / B, "Stone sludge powder / B": wp / B, "M-sand / B": ws / B, "SP / B": sp / B,
                   "Binder content (kg/m³)": B, "Test age (days)": age, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
                   "Conversions / notes": f"Mix {mid}. kg/m3 / binder (CEM I 52.5R {c} + SF {sf} = {B}; paper w/b 0.2). Waste migmatite-amphibolite powder (quarry waste, ~11% biotite) in 'Stone sludge powder/B'; waste crushed migmatite sand (<0.6 mm) in 'M-sand/B'; quartz sand and quartz powder as SS/B and QP/B. Steel fibre 3 vol% (paper; 12 mm x 0.2 mm). Tensile strength = flexural (EN 196-1)."})

# ---------------------------------------------------------------- P4 Paredes et al. 2021 (UHPC matrix optimisation: SF / MK / nano-silica)
p4 = {"Article Name": "Matrix Optimization of Ultra High Performance Concrete for Improving Strength and Durability",
      "Author": "Paredes J.A.; Gálvez J.C.; Enfedaque A.; Alberti M.G.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14226944",
      "Curing method": "Demoulded after 24 h, climatic chamber 20 C, >=95% RH until test age", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
      "Demolding age (days)": 1, "Compressive specimen": "prism halves after 3-point bending", "Compressive specimen size (mm)": "40x40 platens (160x40x40 prisms)",
      "Source table/page": "Table 2 (mix), Table 4 (fc)"}
mix4 = {"CTRL": (1100, 0, 0, 0, 0, 17.6, (102, 112, 124)), "8SF": (1012, 88, 0, 0, 0, 25.3, (101, 119, 138)),
        "8 MK": (1012, 0, 88, 0, 0, 26.4, (103, 117, 136)), "4MK4SF": (1012, 44, 44, 0, 0, 23.1, (106, 122, 140)),
        "10 MK": (990, 0, 110, 0, 0, 26.4, (96, 113, 133)), "10 MK + 2NS1": (968, 0, 110, 22, 0, 33.0, (98, 118, 136)),
        "4MK4SF + 1.5NS1": (995.5, 44, 44, 16.5, 0, 26.4, (105, 120, 141)), "4MK4SF + 2NS1": (990, 44, 44, 22, 0, 27.5, (101, 116, 144)),
        "4MK4SF + 2NSC": (990, 44, 44, 16.5, 5.5, 30.8, (105, 126, 140))}


def p4row(mid, c, sf, mk, ns1, ns2, sp, age, fc, fib):
    B = c + sf + mk + ns1 + ns2
    kw = {"OPC / Cement": c / B, "SF (Silica fume)": sf / B, "Metakaolin": mk / B, "Nano-SiO2": (ns1 + ns2) / B, "W / B": 220 / B,
          "SS / B (Silica sand)": 1211 / B, "SP / B": sp / B, "Binder content (kg/m³)": B, "Test age (days)": age, "Compressive strength (MPa)": fc,
          "Conversions / notes": f"Mix {mid}{' + fibres' if fib else ''}. kg/m3 / binder (cement {c} + SF {sf} + MK {mk} + nano-silica {ns1 + ns2} = {B}). Silica sand D50 0.75 mm."}
    if fib:
        kw.update({"Steel fiber (vol%)": 0.89, "Steel length (mm)": 13, "Steel diameter (µm)": 200})
        kw["Conversions / notes"] += " Dramix OL 13/0.20 steel fibres 0.89 vol% (text). SP of fibre mix assumed equal to the parent mix (not tabulated separately; VERIFY)."
    add(p4, **kw)


for mid, (c, sf, mk, ns1, ns2, sp, fcs) in mix4.items():
    for age, fc in zip((2, 7, 28), fcs):
        p4row(mid, c, sf, mk, ns1, ns2, sp, age, fc, False)
for mid, fcs in [("CTRL", (135, 153)), ("4MK4SF", (146, 171))]:
    c, sf, mk, ns1, ns2, sp, _ = mix4[mid]
    for age, fc in zip((7, 28), fcs):
        p4row(mid, c, sf, mk, ns1, ns2, sp, age, fc, True)

# ---------------------------------------------------------------- P5 Muhammed et al. 2026 (UHPC, micro vs hooked steel fibre; UHPC group only)
p5 = {"Article Name": "Comparative Thermal Performance of Ultra-High-Performance Concrete and Geopolymer Concrete: Influence of Steel Fibre Geometry on Residual Mechanical and Chemical Properties",
      "Author": "Muhammed Y.; Tashan J.; Saiyouri N.; Sleiman Y.; Lateef B.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19163562",
      "OPC / Cement": 1.0, "W / B": 180 / 990, "Sand (type not stated) / B": 1202 / 990, "SP / B": 28 / 990, "Binder content (kg/m³)": 990,
      "Curing method": "Controlled-environment chamber 15 C, 90% RH, 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 15, "Curing RH (%)": 90,
      "Test age (days)": 28, "Compressive specimen": "cube cut from flexural prisms", "Compressive specimen size (mm)": "40x40x40",
      "Source table/page": "Table 2 (fibres), Table 3 (mix), Table 6 (fc, ambient)"}
for mid, kg, shape, fc in [("UHPC", 0, None, 101.3), ("UHPC-H1.5", 14.85, "H", 104.8), ("UHPC-H2", 19.8, "H", 107.5),
                           ("UHPC-M1.5", 14.85, "M", 110.0), ("UHPC-M2", 19.8, "M", 113.5)]:
    kw = {"Steel fiber (vol%)": kg / 7850 * 100, "Compressive strength (MPa)": fc}
    note = f"Mix {mid} (cement-only binder, no SF; w/c 0.18). Ambient (unheated) compressive strength only; UHPGC geopolymer group not extracted."
    if kg:
        if shape == "H":
            kw.update({"Steel length (mm)": 0.75 * 46, "Steel diameter (µm)": 750, "Steel tensile strength (MPa)": 1150})
            note += " Hooked-end fibre d 0.75 mm, L/D 46 -> length 34.5 mm derived from aspect ratio; tensile strength '>1150 MPa'."
        else:
            kw.update({"Steel length (mm)": 0.25 * 56, "Steel diameter (µm)": 250, "Steel tensile strength (MPa)": 2850})
            note += " Micro straight fibre d 0.25 mm, L/D 56 -> length 14 mm derived from aspect ratio; tensile strength '>=2850 MPa'."
        note += f" DOUBTFUL fibre dosage: Table 3 lists fibre {kg} kg/m3 (= 1.5 or 2 % of binder MASS), labelled '1.5'/'2'; converted {kg} kg/m3 / 7850 (assumed) = {kg / 78.5:.3f} vol%. If the label meant vol%, the value would be 1.5/2 vol% (VERIFY)."
    kw["Conversions / notes"] = note
    add(p5, **kw)

# ---------------------------------------------------------------- P6 Lian et al. 2023 (UHPC with sugarcane bagasse ash, direct tension)
p6 = {"Article Name": "Mechanical, Electrical, and Tensile Self-Sensing Properties of Ultra-High-Performance Concrete Enhanced with Sugarcane Bagasse Ash",
      "Author": "Lian J.; Wang Y.; Fu T.; Easa S.M.; Zhou Y.; Li H.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma17010082",
      "Steel fiber (vol%)": 1.5, "Steel length (mm)": 16, "Steel diameter (µm)": 200,
      "Curing method": "Demoulded at 24 h, steam cured 90 C for 3 d, then 20 C / 65% RH until testing", "Curing temperature (°C)": 90, "Curing RH (%)": "",
      "Heat curing duration (h)": 72, "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "40x40x40",
      "Tensile specimen": "dog-bone (T/CECS 864-2021)", "Tensile test type": "direct",
      "Source table/page": "Table 4 (mix, g), Sec. 3.1 text (fc, flexural, tensile)"}
for mid, scba, w, sp, fc, ff, ft in [("Control", 0, 289.9, 41.4, 141.2, 23.6, 6.8), ("SCBA0.3", 3.5, 290.5, 41.5, 142.7, 23.9, 6.9),
                                     ("SCBA0.9", 10.4, 291.7, 41.7, 149.3, 24.6, 7.4), ("SCBA3.0", 34.8, 296.0, 42.3, 159.7, 27.7, 8.2),
                                     ("SCBA9.0", 104.4, 308.2, 44.0, 142.0, 23.6, 7.5)]:
    B = 1159.7 + 331.3 + 165.7 + scba
    add(p6, **{"OPC / Cement": 1159.7 / B, "SF (Silica fume)": 331.3 / B, "FA (Fly ash)": 165.7 / B, "Other binder": scba / B, "W / B": w / B,
               "SP / B": sp / B, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
               "Conversions / notes": f"Mix {mid}. Batch masses in g / binder (cement 1159.7 + SF 331.3 + FA 165.7 + SCBA {scba} = {B:.1f} g); no sand (paste-type UHPC). SCBA = carbonised sugarcane bagasse ash (600 C) in 'Other binder'. Steel fibre 1.5 vol% (text). Tensile strength = direct (dog-bone); flexural strength (40x40x160) = {ff} MPa. Test age not stated."})

# ---------------------------------------------------------------- P7 Zhang et al. 2022 (sprayed RPC, BBD: SF/B, FA/B, steel fibre)
p7 = {"Article Name": "Preparation, mechanics and self-sensing performance of sprayed reactive powder concrete",
      "Author": "Zhang Y.; Wang J.; Wang J.; Qian X.", "Year": 2022, "DOI / URL": "https://doi.org/10.1038/s41598-022-11836-y",
      "Steel length (mm)": 8, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2907,
      "Curing method": "Sprayed plates wrapped in plastic 24 h, demoulded, then outdoor curing 28 d (tunnel simulation)", "Curing time (days)": 28,
      "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube cut from sprayed plate", "Compressive specimen size (mm)": "100x100x100",
      "Tensile specimen": "cube 100x100x100 cut from plate (splitting)", "Tensile test type": "splitting",
      "Source table/page": "Table 2 (mix), Table 3 (levels), Table 4 (28-d fc, splitting)"}
mix7 = [("B-1", 928.40, 185.68, 123.79, 866.51, 247.57, 117, 13.62, 66.40, 9.38), ("B-2", 791.68, 304.49, 121.80, 852.58, 243.60, 117, 13.40, 70.00, 7.75),
        ("B-3", 798.49, 184.27, 245.69, 859.91, 245.69, 117, 13.51, 98.61, 8.24), ("B-4", 664.86, 302.21, 241.77, 846.19, 241.77, 117, 13.30, 85.79, 8.21),
        ("B-5", 863.20, 184.97, 184.97, 863.20, 246.63, 78, 13.56, 97.73, 8.08), ("B-6", 728.03, 303.35, 182.01, 849.37, 242.68, 78, 13.35, 113.80, 8.73),
        ("B-7", 863.20, 184.97, 184.97, 863.20, 246.63, 156, 13.56, 114.79, 11.23), ("B-8", 728.03, 303.35, 182.01, 849.37, 242.68, 156, 13.35, 99.58, 8.22),
        ("B-9", 859.49, 245.57, 122.78, 859.49, 245.57, 78, 13.51, 115.86, 9.62), ("B-10", 731.14, 243.71, 243.71, 852.99, 243.71, 78, 13.40, 100.49, 8.50),
        ("B-11", 859.49, 245.57, 122.78, 859.49, 245.57, 156, 13.51, 119.28, 8.44), ("B-12", 731.14, 243.71, 243.71, 852.99, 243.71, 156, 13.40, 113.27, 10.41),
        ("B-13", 795.07, 244.64, 183.48, 856.23, 244.64, 117, 13.46, 118.02, 10.28), ("B-14", 795.07, 244.64, 183.48, 856.23, 244.64, 117, 13.46, 105.50, 9.32),
        ("B-15", 795.07, 244.64, 183.48, 856.23, 244.64, 117, 13.46, 109.66, 9.86), ("B-16", 795.07, 244.64, 183.48, 856.23, 244.64, 117, 13.46, 94.13, 9.25),
        ("B-17", 795.07, 244.64, 183.48, 856.23, 244.64, 117, 13.46, 111.24, 8.33)]
vf7 = {78: 1.0, 117: 1.5, 156: 2.0}
for mid, c, sf, fa, ms, w, st, sp, fc, ft in mix7:
    B = c + sf + fa
    add(p7, **{"OPC / Cement": c / B, "SF (Silica fume)": sf / B, "FA (Fly ash)": fa / B, "W / B": w / B, "M-sand / B": ms / B, "SP / B": sp / B,
               "Binder content (kg/m³)": B, "Steel fiber (vol%)": vf7[st], "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
               "Conversions / notes": f"Mix {mid} (Box-Behnken; B-13..B-17 are replicate centre points). kg/m3 / binder (cement {c} + SF {sf} + FA {fa} = {B:.2f}). Manufactured sand (FM 3.6). Steel fibre {st} kg/m3 = {vf7[st]} vol% (Table 3 factor level), copper-plated 8 mm x 0.2 mm. Wet-mix sprayed RPC; specimens cut from sprayed plates. Outdoor curing temperature not reported."})

# ---------------------------------------------------------------- P8 Bo et al. 2025 (UHPC ultrafine fly ash / ultrafine mineral powder, steam cured)
p8 = {"Article Name": "Effect of Ultra-Fine Mineral Admixture on the Performance of Ultra-High-Performance Concrete",
      "Author": "Bo S.; Gong L.; Guo H.; Guo F.; Yao T.; Wei D.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma18040729",
      "SS / B (Silica sand)": 850 / 1220, "Sand max size (µm)": 1000, "HRWR / B": 10 / 1220, "Binder content (kg/m³)": 1220, "W / B": 195 / 1220,
      "Steel fiber (vol%)": 2.8, "Steel length (mm)": 13, "Steel diameter (µm)": 120, "Steel tensile strength (MPa)": 2850,
      "Curing method": "1 d at room temperature, demoulded, steam curing 90 C / 95% RH for 48 h, then tested", "Curing temperature (°C)": 90,
      "Curing RH (%)": 95, "Heat curing duration (h)": 48, "Demolding age (days)": 1, "Compressive specimen": "cube",
      "Compressive specimen size (mm)": "100x100x100", "Tensile specimen": "prism 100x100x400", "Tensile test type": "flexural",
      "Source table/page": "Table 2 (mix), Sec. 3.1 text (fc, flexural)"}
for mid, ufa, ump, fc, ff in [("UC-0", 300, 0, 168.1, 26.3), ("UC-17", 250, 50, 170.2, 28.2), ("UC-33", 200, 100, 172.9, 31.2),
                              ("UC-50", 150, 150, 176.7, 33.2), ("UC-67", 100, 200, 170.6, 31.4), ("UC-83", 50, 250, 167.2, 28.2),
                              ("UC-100", 0, 300, 162.7, 27.3)]:
    B = 1220.0
    add(p8, **{"OPC / Cement": 800 / B, "FA (Fly ash)": ufa / B, "Other binder": ump / B, "SF (Silica fume)": 120 / B,
               "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
               "Conversions / notes": f"Mix {mid}. kg/m3 / binder (cement 800 + ultrafine FA {ufa} + ultrafine mineral powder {ump} + SF 120 = 1220). Ultrafine mineral powder (UMP; type not specified beyond 'mineral powder') in 'Other binder'. Excluded from binder: MgO-type expansive agent 20 kg/m3, defoamer 2 kg/m3. Steel fibre 220 kg/m3 = 2.8 vol% (paper). Tensile strength = flexural. Test age after steam curing not stated."})

# ---------------------------------------------------------------- P9 Abid et al. 2019 (RPC steel / PP / hybrid fibres; ambient values)
p9 = {"Article Name": "Effect of Fibers on High-Temperature Mechanical Behavior and Microstructure of Reactive Powder Concrete",
      "Author": "Abid M.; Hou X.; Zheng W.; Hussain R.R.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12020329",
      "Curing method": "1 d at 25 C / 70% RH, demoulded, steam curing 90 C for 72 h, then laboratory storage 60 d", "Curing temperature (°C)": 90,
      "Heat curing duration (h)": 72, "Demolding age (days)": 1, "Tensile specimen": "cube 70.7 mm (splitting)", "Tensile test type": "splitting",
      "Source table/page": "Table 2 (mix), Sec. 3.1.2-3.1.3 text (ambient splitting and flexural)"}
for mid, c, sf, sl, qc, qf, sp, pp, ppv, st, w, fs, fr in [("SRPC", 800.53, 240.16, 120.08, 480.32, 480.32, 34.82, 0, 0, 2, 185.72, 14.2, 29.8),
                                                         ("PRPC", 816.42, 244.33, 122.16, 490.32, 490.32, 35.47, 2.73, 0.3, 0, 189.20, 9.5, 13.5),
                                                         ("HRPC", 815.18, 245.31, 120.08, 480.32, 480.32, 35.40, 1.82, 0.2, 2, 188.81, 17.9, 32.4)]:
    B = c + sf + sl
    kw = {"OPC / Cement": c / B, "SF (Silica fume)": sf / B, "GGBS": sl / B, "W / B": w / B, "SS / B (Silica sand)": (qc + qf) / B, "SP / B": sp / B,
          "Binder content (kg/m³)": B, "Steel fiber (vol%)": st, "PP fiber (vol%)": ppv, "Tensile strength (MPa)": fs,
          "Conversions / notes": f"Mix {mid}. kg/m3 / binder (cement {c} + SF {sf} + slag {sl} = {B:.2f}; paper w/b 0.16). Quartz sand coarse (avg 0.4 mm) + fine (avg 0.2 mm). Fibre vol% from Table 2 footnote. Ambient (20 C) values only; compressive strength only in figures. Tensile strength = splitting; flexural strength (70.7x70.7x220 prism) = {fr} MPa. Exact test age not stated (after 60 d storage)."}
    if st:
        kw.update({"Steel length (mm)": 13, "Steel diameter (µm)": 220, "Steel tensile strength (MPa)": 2850, "Steel elastic modulus (GPa)": 200})
    if ppv:
        kw.update({"PP length (mm)": 19, "PP diameter (µm)": 45})
        kw["Conversions / notes"] += " PP length given as 18-20 mm (19 entered)."
    add(p9, **kw)

# ---------------------------------------------------------------- P10 Wang et al. 2025 (ultra-high-performance shotcrete with waste glass sand)
p10 = {"Article Name": "Study on the mechanics and self-sensing properties of ultrahigh-performance shotcrete containing waste glass aggregates",
       "Author": "Wang J.; Wu S.; Zhang Y.; Qian X.", "Year": 2025, "DOI / URL": "https://doi.org/10.1038/s41598-025-86257-8",
       "OPC / Cement": 0.7, "SF (Silica fume)": 0.1, "FA (Fly ash)": 0.1, "Metakaolin": 0.1, "W / B": 0.2, "SP / B": 0.008, "Sand max size (µm)": 1180,
       "Carbon fiber (vol%)": 0.7, "Curing method": "Sprayed plates cured outdoors 24 h, demoulded, then natural (outdoor) curing until test age",
       "Demolding age (days)": 1, "Compressive specimen": "cube cut from sprayed plate", "Compressive specimen size (mm)": "100x100x100"}
fc10 = {(0, 0): (66.71, 91.36, 98.62, 100.41, 112.42), (0, 25): (59.83, 82.26, 95.36, 97.79, 107.35), (0, 50): (58.03, 80.91, 90.72, 92.14, 98.76),
        (0, 75): (46.84, 77.65, 87.34, 89.79, 94.84), (0, 100): (51.28, 84.75, 94.32, 96.35, 111.9),
        (0.5, 0): (70.51, 92.95, 101.94, 110.2, 113.45), (0.5, 25): (57.73, 90.46, 96.36, 98.12, 107.8), (0.5, 50): (58.18, 88.62, 93.26, 94.89, 102.4),
        (0.5, 75): (59.35, 83.38, 89.71, 91.15, 99.6), (0.5, 100): (55.08, 81.09, 95.63, 96.54, 113.21),
        (1.0, 0): (69.96, 93.94, 108.06, 115.27, 117.16), (1.0, 25): (70.69, 98.08, 103.82, 109.84, 113.68), (1.0, 50): (58.68, 84.34, 100.87, 108.87, 110.33),
        (1.0, 75): (56.64, 83.98, 101.71, 110.75, 114.74), (1.0, 100): (55.49, 90.25, 103.33, 115.58, 118.91),
        (1.5, 0): (76.08, 100.48, 112.74, 121.02, 127.25), (1.5, 25): (77.45, 97.59, 110.37, 116.84, 118.52), (1.5, 50): (68.64, 95.13, 108.52, 115.72, 118.00),
        (1.5, 75): (74.09, 90.51, 106.85, 115.73, 120.44), (1.5, 100): (74.16, 91.77, 109.39, 119.00, 124.36),
        (2.0, 0): (77.27, 112.65, 121.95, 129.42, 132.51), (2.0, 25): (74.04, 104.26, 121.21, 126.03, 129.97), (2.0, 50): (73.76, 105.81, 119.27, 123.07, 125.52),
        (2.0, 75): (74.72, 105.8, 117.14, 127.28, 130.87), (2.0, 100): (72.96, 103.03, 121.66, 131.84, 135.16)}
gsl = [0, 25, 50, 75, 100]
st10 = {0: (7.92, 8.11, 7.57, 7.70, 8.19), 0.5: (12.29, 12.17, 12.02, 12.29, 12.91), 1.0: (15.14, 14.33, 14.35, 14.80, 14.99),
        1.5: (16.35, 16.16, 16.41, 16.37, 16.39), 2.0: (19.75, 19.43, 18.77, 19.53, 19.49)}
fl10 = {0: (6.42, 6.56, 6.13, 6.51, 6.67), 0.5: (12.25, 12.14, 11.82, 12.00, 12.37), 1.0: (14.76, 15.16, 14.84, 14.52, 15.00),
        1.5: (18.62, 18.93, 19.28, 19.73, 19.59), 2.0: (21.38, 20.74, 21.28, 22.03, 21.69)}
for (sf_, gs), fcs in fc10.items():
    kw = {"M-sand / B": 0.7 * (100 - gs) / 100, "Fine sand / B": 0.7 * gs / 100, "Steel fiber (vol%)": sf_, "Total fiber (vol%)": sf_ + 0.7}
    if sf_:
        kw.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850, "Steel elastic modulus (GPa)": 200})
    note = (f"Mix {sf_}%SF{gs}%GS. Binder cement:SF:FA:MK = 0.7:0.1:0.1:0.1, w/b 0.2, sand/binder 0.7 (machine-made sand in M-sand/B; waste glass sand 0.15-1.18 mm in 'Fine sand/B' - no glass-sand column), "
            f"water reducer 0.8 % of binder. Steel fibre {sf_} % (vol% assumed per 'SF(%)'). Carbon fibre 0.7 % in every mix (6 mm, 7 um): unit not stated, entered as vol% (VERIFY). Outdoor curing temperature not reported.")
    for age, fc in zip((1, 3, 7, 14, 28), fcs):
        extra = {}
        if age == 28:
            j = gsl.index(gs)
            extra = {"Tensile strength (MPa)": st10[sf_][j], "Tensile test type": "splitting", "Tensile specimen": "cube 100x100x100 (splitting)",
                     "Source table/page": "Sec. 'Mix design' + Table 3 (mix), Table 4 (fc), Table 5 (splitting), Table 6 (flexural)",
                     "Conversions / notes": note + f" Tensile strength = 28-d splitting; flexural (100x100x400) = {fl10[sf_][j]} MPa (age as Table 6, assumed 28 d)."}
        else:
            extra = {"Source table/page": "Sec. 'Mix design' + Table 3 (mix), Table 4 (fc)", "Conversions / notes": note}
        add(p10, **kw, **{"Test age (days)": age, "Compressive strength (MPa)": fc}, **extra)

# ---------------------------------------------------------------- P11 Liu et al. 2026 (UHPC with FA / MK, direct tension)
p11 = {"Article Name": "Effect of fly ash and metakaolin on early-age autogenous shrinkage and mechanical properties of ultra-high-performance concrete",
       "Author": "Liu Y.; Hao R.; Liao L.; Zhao J.; Liao Z.; Hou Z.; Ding M.", "Year": 2026, "DOI / URL": "https://doi.org/10.3389/fmats.2026.1813690",
       "Sand max size (µm)": 425, "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2300,
       "Curing method": "Covered with film, demoulded at 24 h, standard curing 20+/-2 C, >95% RH for 28 d", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
       "Demolding age (days)": 1, "Compressive specimen": "per GB/T 17671 (40 mm prism halves)",
       "Tensile specimen": "dog-bone (reported as 100x100x560)", "Tensile test type": "direct"}
mix11 = [("N", 820, 0, 0, (111, 125.3, 166.2), 8.21, 0.210), ("FA10", 738, 82, 0, (102.9, 119.9, 155.1), 7.50, 0.057),
         ("FA20", 656, 164, 0, (99.2, 115.6, 150.5), 4.90, 0.097), ("FA30", 574, 246, 0, (94.4, 111.7, 143.7), 4.31, 0.013),
         ("MK5", 779, 0, 41, (115.9, 122.3, 153.5), 7.24, 0.082), ("MK10", 738, 0, 82, (118.4, 126.6, 145.4), 8.98, 0.182),
         ("MK15", 697, 0, 123, (110.3, 125.5, 139.2), 9.42, 0.501), ("FA15MK5", 656, 123, 41, (113.2, 122.1, 152.9), 7.11, 0.430),
         ("FA10MK10", 656, 82, 82, (108.9, 118.3, 145.5), 8.48, 0.355), ("FA5MK15", 656, 41, 123, (105.3, 111.7, 137.2), 7.79, None)]
for mid, c, fa, mk, fcs, ft, eps in mix11:
    B = c + 111 + fa + mk + 111
    base = {"OPC / Cement": c / B, "SF (Silica fume)": 111 / B, "FA (Fly ash)": fa / B, "Metakaolin": mk / B, "Limestone powder": 111 / B,
            "W / B": 187 / B, "QP / B (Quartz powder)": 111 / B, "SS / B (Silica sand)": 1100 / B, "SP / B": 5.8 / B, "Binder content (kg/m³)": B}
    note = (f"Mix {mid}. kg/m3 / binder (cement {c} + SF 111 + FA {fa} + MK {mk} + limestone powder 111 = {B}). The column headed 'QS' (111) between LP and QS1-3 is taken as quartz powder (footnote defines QP) and kept out of binder; "
            "paper states W/B 0.16, which matches water/(binder + QP) = 187/1153. Quartz sand QS1+QS2+QS3 = 550+220+330 (0.106-0.425 mm). Defoamer 0.2 kg/m3. Steel fibre 156 kg/m3 = 2 vol% (paper).")
    for age, fc in zip((3, 7, 28), fcs):
        kw = {"Test age (days)": age, "Compressive strength (MPa)": fc, "Source table/page": "Table 3 (mix), Table 6 (fc)", "Conversions / notes": note}
        if age == 28:
            kw.update({"Curing time (days)": 28, "Tensile strength (MPa)": ft, "Source table/page": "Table 3 (mix), Table 6 (fc), Table 7 (direct tension)"})
            if eps is not None:
                kw["Tensile strain capacity (%)"] = eps
                kw["Conversions / notes"] = note + " Ultimate tensile stress and strain from Table 7 (strain already in %). Tensile test age assumed 28 d (same batch as compressive specimens)."
            else:
                kw["Conversions / notes"] = note + " Tensile stress 7.79 MPa from text (row missing in Table 7, strain not available). Tensile test age assumed 28 d."
        else:
            kw.update({"Tensile specimen": "", "Tensile test type": ""})
        add(p11, **base, **kw)

# ---------------------------------------------------------------- P12 Tian et al. 2022 (UHPC, normal vs long-term autoclave curing, FA)
p12 = {"Article Name": "The Influence of Long-Term Autoclaving on the Properties of Ultra-High Performance Concrete",
       "Author": "Tian H.; Hirsch T.; Stephan D.; Lehmann C.", "Year": 2022, "DOI / URL": "https://doi.org/10.3389/fmats.2022.844268",
       "W / B": 0.21, "Steel fiber (vol%)": 2, "Steel length (mm)": 12.5, "Steel diameter (µm)": 200, "Demolding age (days)": 1,
       "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160 prism halves",
       "Tensile specimen": "prism 40x40x160, 3-point bending, span 100 mm", "Tensile test type": "flexural",
       "Source table/page": "Table 2 (mix ratios), Table 3 (mechanical properties)"}
for mid, c, fa in [("C1", 1.0, 0.0), ("C2", 0.8, 0.2)]:
    B = c + fa + 0.26
    for cur, fc, ff in [("N", *((178.0, 26.4) if mid == "C1" else (169.9, 24.0))), ("A", *((195.5, 18.8) if mid == "C1" else (218.0, 26.5)))]:
        kw = {"OPC / Cement": c / B, "FA (Fly ash)": fa / B, "SF (Silica fume)": 0.26 / B, "QP / B (Quartz powder)": 0.76 / B, "SS / B (Silica sand)": 1.10 / B,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff}
        note = (f"Mix {mid}. Mass ratios cement:FA:SF:QP:sand = {c}:{fa}:0.26:0.76:1.10, divided by (cement+FA+SF) = {B}. Paper fixes 'w/b 0.21' without defining the binder (VERIFY: if binder = cement+FA only, water/(C+FA+SF) would be 0.167). "
                "SP (MasterGlenium ACE 430) dosage not reported. Steel fibre 2 vol% (12.5 mm x 0.2 mm). Tensile strength = flexural.")
        if cur == "N":
            kw.update({"Curing method": "Sealed 24 h at 20 C, demoulded, 24 h water pre-curing, then water at 20 C for 28 d", "Curing time (days)": 28,
                       "Curing temperature (°C)": 20, "Test age (days)": 30,
                       "Conversions / notes": note + " Test age 30 d derived (1 d sealed + 1 d water + 28 d water)."})
        else:
            kw.update({"Curing method": "Sealed 24 h, demoulded, 24 h water pre-curing, then autoclaved 200 C / 1.55 MPa saturated steam for 10 d",
                       "Curing time (days)": 10, "Curing temperature (°C)": 200, "Heat curing duration (h)": 240, "Test age (days)": 12,
                       "Conversions / notes": note + " Test age 12 d derived (1 + 1 + 10 d autoclave)."})
        add(p12, **kw)

# ---------------------------------------------------------------- P13 Sharma et al. 2024 (UHPC with LP and GGBFS, moist vs 90 C water bath)
p13 = {"Article Name": "Incorporating Limestone Powder and Ground Granulated Blast Furnace Slag in Ultra-high Performance Concrete to Enhance Sustainability",
       "Author": "Sharma Y.; Yeluri M.; Allena S.; Owusu-Danquah J.", "Year": 2024, "DOI / URL": "https://doi.org/10.1186/s40069-024-00723-7",
       "Sand max size (µm)": 4750, "Steel fiber (vol%)": 120 / 7850 * 100, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
       "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50x50x50",
       "Source table/page": "Table 2 (mix), Table 3 (curing), Table 4 (fc)"}
mix13 = {("S0", 0): (900, 0, 0, 1095), ("S0", 10): (810, 0, 90, 973), ("S0", 15): (765, 0, 135, 920), ("S0", 20): (720, 0, 180, 864),
         ("S25", 0): (675, 225, 0, 1080), ("S25", 10): (608, 225, 68, 985), ("S25", 15): (574, 225, 101, 944), ("S25", 20): (540, 225, 135, 903)}
# Table 4: (curing, LP) -> (with GGBFS 7d, 28d, without GGBFS 7d, 28d)
t13 = {("MC", 0): (122, 144, 130, 147), ("MC", 10): (119, 143, 122, 145), ("MC", 15): (117, 139, 119, 143), ("MC", 20): (114, 138, 116, 139),
       ("WB", 0): (155, 166, 164, 171), ("WB", 10): (153, 162, 157, 168), ("WB", 15): (150, 157, 152, 161), ("WB", 20): (139, 149, 146, 154)}
cur13 = {"MC": dict(m="Moist curing: 24 h in mould, then curing room with controlled temperature and humidity until testing", T=""),
         "WB": dict(m="Warm bath curing: 24 h in mould, then water bath at 90 C until testing", T=90)}
for (cur, lp), vals in t13.items():
    for gg, (fc7, fc28) in [("S25", vals[:2]), ("S0", vals[2:])]:
        c, g, l, sand = mix13[(gg, lp)]
        B = c + 69 + g + 103 + l
        for age, fc in [(7, fc7), (28, fc28)]:
            add(p13, **{"OPC / Cement": c / B, "SF (Silica fume)": 69 / B, "GGBS": g / B, "FA (Fly ash)": 103 / B, "Limestone powder": l / B,
                        "W / B": 160 / B, "Local sand / B": sand / B, "Binder content (kg/m³)": B, "Curing method": cur13[cur]["m"],
                        "Curing temperature (°C)": cur13[cur]["T"], "Test age (days)": age, "Compressive strength (MPa)": fc,
                        "Conversions / notes": f"Mix C-{gg}-LP{lp}, curing {cur}. kg/m3 / binder (cement {c} + SF 69 + GGBFS {g} + FA 103 + LP {l} = {B}; paper w/cm 0.15). Local sand max 4.75 mm. HRWRA 44.5 L/m3 (density not given, SP/B left blank). Steel fibre 120 kg/m3 -> vol% with 7850 (assumed); 13 mm straight, aspect ratio 65 -> diameter 0.2 mm derived. Flexural results only in figures."})

# ---------------------------------------------------------------- P14 Choi et al. 2023 (UHPC / UHPFRC with recycled sand)
p14 = {"Article Name": "Mechanical Properties of Ultra-High Performance Concrete (UHPC) and Ultra-High Performance Fiber-Reinforced Concrete (UHPFRC) with Recycled Sand",
       "Author": "Choi D.; Hong K.; Ochirbud M.; Meiramov D.; Sukontaskuul P.", "Year": 2023, "DOI / URL": "https://doi.org/10.1186/s40069-023-00631-2",
       "Curing method": "Covered with polyethylene 24 h, demoulded, cured under water (18-23 C) until testing", "Curing temperature (°C)": 20.5,
       "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50x50x50",
       "Tensile specimen": "prism 40x40x160, 3-point bending", "Source table/page": "Table 8 (mix), Table 10 (fc, flexural)"}
mix14 = [("NS-U-20", 891, 0, 39.3, 141, 0, 1150, 214, 42.9, 0, (60.2, 90.1), 11.1), ("NS-U-16", 931, 0, 41.0, 147, 0, 1201, 179, 44.8, 0, (63.7, 112), 13.5),
         ("RS-U-20", 818, 72.1, 80.1, 95.6, 1084, 0, 199, 42.6, 0, (64.4, 86.3), 8.38), ("RS-U-18", 823, 72.6, 80.6, 96.2, 1092, 0, 193, 42.9, 0, (65.0, 87.4), 10.6),
         ("RS-U-17", 832, 73.4, 81.5, 97.2, 1104, 0, 184, 43.4, 0, (65.5, 102), 11.0), ("RS-U-16", 842, 74.2, 82.4, 98.3, 1116, 0, 175, 43.9, 0, (60.7, 97.4), 8.12),
         ("RS-F-17-1.0", 832, 73.4, 81.5, 97.2, 1104, 0, 184, 48.8, 1.0, (75.6, 100), 9.41), ("RS-F-17-2.0", 832, 73.4, 81.5, 97.2, 1104, 0, 184, 48.8, 2.0, (84.5, 128), 11.9),
         ("RS-F-17-3.0", 832, 73.4, 81.5, 97.2, 1104, 0, 184, 48.8, 3.0, (84.5, 113), 18.1), ("RS-F-16-2.0", 842, 74.2, 82.4, 98.3, 1116, 0, 175, 49.3, 2.0, (89.6, 108), 14.0)]
for mid, c, fa, sf, qp, rs, ns, w, sp, vf, (fc7, fc28), ff in mix14:
    B = c + fa + sf
    pw = w / (B + qp)
    base = {"OPC / Cement": c / B, "FA (Fly ash)": fa / B, "SF (Silica fume)": sf / B, "W / B": w / B, "QP / B (Quartz powder)": qp / B,
            "Sand (type not stated) / B": (rs + ns) / B, "SP / B": sp / B, "Binder content (kg/m³)": B, "Steel fiber (vol%)": vf}
    if vf:
        base.update({"Steel length (mm)": 13, "Steel diameter (µm)": 300})
    note = (f"Mix {mid}. kg/m3 / binder (OPC {c} + FA {fa} + SF {sf} = {B:.1f}); quartz powder {qp} kept out of binder, so W/B here = {w / B:.3f} vs paper W/B {pw:.2f} (incl. QP). "
            + ("Aggregate = 100 % recycled sand (wet-processed, absorption 5.12 %) in 'Sand (type not stated)/B'. " if rs else "Aggregate = natural sand in 'Sand (type not stated)/B'. ")
            + (f"Straight steel fibre {vf} vol% (paper), 13 mm x 0.3 mm. " if vf else "No fibres. "))
    add(p14, **base, **{"Test age (days)": 7, "Compressive strength (MPa)": fc7, "Tensile specimen": "", "Conversions / notes": note})
    add(p14, **base, **{"Test age (days)": 28, "Compressive strength (MPa)": fc28, "Tensile strength (MPa)": ff, "Tensile test type": "flexural",
                        "Conversions / notes": note + "Tensile strength = 28-d flexural strength (3-point)."})

# ---------------------------------------------------------------- P15 Pham et al. 2024 (ultra-high-performance rubberised concrete)
B = 995 + 238
p15 = {"Article Name": "Impact of Rubber Content on Performance of Ultra-High-Performance Rubberised Concrete (UHPRuC)",
       "Author": "Pham T.M.; Lee J.; Pournasiri E.; Li J.; Peng Z.; Bi K.; Tran T.M.", "Year": 2024, "DOI / URL": "https://doi.org/10.1186/s40069-024-00688-7",
       "OPC / Cement": 995 / B, "SF (Silica fume)": 238 / B, "W / B": 180 / B, "SP / B": 67 / B, "Binder content (kg/m³)": B, "Sand max size (µm)": 300,
       "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2300, "Steel elastic modulus (GPa)": 200,
       "Curing method": "24 h at room temperature in moulds, then steam curing 70 C for 72 h, +24 h gradual cooling in steam room", "Curing temperature (°C)": 70,
       "Heat curing duration (h)": 72, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
       "Tensile specimen": "beam 100x100x400, ASTM C1609 (span 300)", "Tensile test type": "flexural",
       "Source table/page": "Table 1 (mix), Sec. 4.3 text (fc), Table 3 (flexural)"}
for mid, ss, rub, fc, ff in [("UHPRuC_0", 1051, 0, 136.1, 19.56), ("UHPRuC_10", 945.9, 51.4, 115.8, 11.04),
                             ("UHPRuC_20", 840.8, 102.8, 103.8, 9.23), ("UHPRuC_40", 630.6, 205.7, 67.7, 7.44)]:
    add(p15, **{"SS / B (Silica sand)": ss / B, "Crumb rubber / B": rub / B, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
                "Conversions / notes": f"Mix {mid}. kg/m3 / binder (cement 995 + SF 238 = 1233; paper w/c 0.18). 30-mesh crumb rubber (0-0.625 mm, pre-soaked) replacing silica sand by volume. Steel fibre 156 kg/m3 = 2 vol% (paper). Tensile strength = ASTM C1609 peak flexural strength. fc also reported in Pham et al. 2021a (same specimens). Test age not stated."})

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows).reindex(columns=H)
# drop DOIs already collected (existing_papers.txt + other agents' files)
seen = set()
with open(os.path.join(D, "existing_papers.txt"), encoding="utf-8-sig") as f:
    for l in f:
        m = re.search(r"10\.\d+/\S+", l)
        if m:
            seen.add(m.group(0).lower().rstrip("/.,"))
for fn in glob.glob(os.path.join(D, "*.csv")):
    if os.path.basename(fn) in ("TEMPLATE.csv", "w3_uhpc.csv"):
        continue
    for v in pd.read_csv(fn, encoding="utf-8-sig", usecols=["DOI / URL"])["DOI / URL"].dropna().unique():
        m = re.search(r"10\.\d+/\S+", str(v))
        if m:
            seen.add(m.group(0).lower())
doi = df["DOI / URL"].str.extract(r"(10\.\d+/\S+)")[0].str.lower()
dup = sorted(set(doi[doi.isin(seen)]))
if dup:
    print("DROPPING already-collected DOIs:", dup)
df = df[~doi.isin(seen)]
df.to_csv(os.path.join(D, "w3_uhpc.csv"), index=False, encoding="utf-8-sig")
print(len(df), df["DOI / URL"].nunique())
