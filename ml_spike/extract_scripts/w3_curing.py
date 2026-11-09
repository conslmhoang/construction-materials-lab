"""Builder for w3_curing.csv - ECC / SHCC (PVA or PE) studies on curing regime and age
(strength development 1-90 d, steam / natural / sprinkler / standard curing, post-curing temperature,
air vs water curing, early-age strength of rapid-hardening ECC, printed SHCC tested at several ages).
All values transcribed from the papers' full text (Europe PMC fullTextXML).
Run: python w3_curing.py  (writes ../additions/w3_curing.csv, UTF-8 with BOM)
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


# ------------------------------------------------------------------ 1 Zhang et al. 2024, Yellow River sand ECC, 4 curing methods x 3 ages
B = 1170.0  # cement 585 + FA 585
base = {"Article Name": "The Influence and Mechanism of Curing Methods and Curing Age on the Mechanical Properties of Yellow River Sand Engineered Cementitious Composites",
        "Author": "Zhang K., Wu W., Fan J., Yuan C., Caggiano A.", "Year": 2024, "DOI / URL": "https://doi.org/10.3390/ma17174307",
        "OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": R(410 / B), "SP / B": R(3.5 / B, 5),
        "HPMC / B (hydroxypropyl methyl cellulose)": R(1.8 / B, 5), "Binder content (kg/m³)": B,
        "PVA fiber (vol%)": R(19 / 1300 * 100, 3), "PVA length (mm)": 12, "PVA diameter (µm)": 40,
        "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": R(19 / 1300 * 100, 3),
        "Demolding age (days)": 2, "Compressive specimen": "prism halves (GB/T 17671)", "Compressive specimen size (mm)": "40x40x160",
        "Tensile specimen": "plate 330x60x13 (JC/T 2461-2018)", "Tensile test type": "direct"}
cur = {"B": dict(m="standard curing 20±2 °C, RH >95% from demoulding (48 h) to test", T=20, RH=95, h=None),
       "Z": dict(m="steam-curing box for 3 d after demoulding (steam temperature not reported), then 20±2 °C / 50% RH to test", T=None, RH=None, h=72),
       "S": dict(m="sprinkler curing: indoors under geotextile, sprinkled morning and evening, to test", T=None, RH=None, h=None),
       "K": dict(m="natural curing: room 20±2 °C, RH 50% from demoulding to test", T=20, RH=50, h=None)}
fc = {("B", 14): 22.9, ("Z", 14): 33.0, ("S", 14): 27.7, ("K", 14): 27.3,
      ("B", 28): 26.4, ("Z", 28): 34.9, ("S", 28): 29.3, ("K", 28): 30.8,
      ("B", 90): 32.7, ("Z", 90): 38.7, ("S", 90): 31.6, ("K", 90): 31.1}
# (ultimate tensile strength, ultimate tensile strain %) from Sect. 3.1.2 text
ten = {("K", 14): (1.3, 4.70), ("Z", 14): (1.82, 3.50), ("S", 14): (1.74, 2.82), ("B", 14): (1.54, 4.47),
       ("Z", 28): (2.05, 4.03), ("B", 28): (1.83, 3.71), ("K", 28): (1.79, 4.37), ("S", 28): (1.46, 1.91),
       ("K", 90): (1.59, 4.25), ("Z", 90): (1.62, 3.18), ("B", 90): (1.27, 1.86), ("S", 90): (1.17, 0.73)}
for (c, age), f in fc.items():
    ft, eps = ten[(c, age)]
    cc = cur[c]
    add(base, **{"River sand / B": R(700 / B), "Sand max size (µm)": 355, "Curing method": cc["m"], "Curing time (days)": age,
                 "Curing temperature (°C)": cc["T"], "Curing RH (%)": cc["RH"], "Test age (days)": age, "Heat curing duration (h)": cc["h"],
                 "Compressive strength (MPa)": f, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                 "First-cracking strength (MPa)": 0.47 if (c, age) == ("B", 28) else None,
                 "Source table/page": "Table 3 (mix), Table 5 (fc), Sect. 3.1.2 text (tension)" + (", Table 7 (first crack)" if (c, age) == ("B", 28) else ""),
                 "Conversions / notes": f"YRS-ECC {c}{age}: kg/m3 / binder {B:.0f} (cement 585 + FA 585, water 410, Yellow River sand 700 (0-355 um, recorded as river sand), "
                                        f"water reducer 3.5, HPMC 1.8). PVA 19 kg/m3 / 1300 = 1.46 vol%. Tensile values from text of Sect. 3.1.2 (also plotted in Fig. 6/11)."})
add(base, **{"SS / B (Silica sand)": R(700 / B), "Sand max size (µm)": 565, "Curing method": cur["B"]["m"], "Curing time (days)": 28,
             "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": 28,
             "Tensile strength (MPa)": 1.60, "First-cracking strength (MPa)": 0.48, "Tensile strain capacity (%)": 3.20,
             "Source table/page": "Table 3 (mix), Table 7 (tension)",
             "Conversions / notes": f"Traditional quartz-sand ECC B'28: same mix as YRS-ECC with quartz sand 700 kg/m3 (80-120 mesh, 0-565 um). Binder {B:.0f}. fc not reported for this mix."})

# ------------------------------------------------------------------ 2 Chai et al. 2023, HDC, 28 d + post-curing temperature treatment
base = {"Article Name": "Effect of Ambient Temperature on the Mechanical Properties of High Ductility Concrete",
        "Author": "Chai L., Chen B., Guo L., Ren B., Chen Z., Huang T., Lopes S.M.R.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16062465",
        "Sand max size (µm)": 1180, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1250,
        "PVA elastic modulus (GPa)": 30, "Total fiber (vol%)": 2.0, "Curing time (days)": 28, "Curing temperature (°C)": 20,
        "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
        "Tensile specimen": "dog-bone (13x30 mm section)", "Tensile gauge length (mm)": 100, "Tensile test type": "direct"}
hdc = {"HDC-1": (680, 600, 384, 1.01, 384, 48.0, 4.23, 1.15), "HDC-2": (768, 512, 384, 1.54, 397, 47.8, 4.47, 0.64),
       "HDC-3": (768, 512, 384, 1.31, 323, 50.2, 4.22, 0.55), "HDC-4": (768, 512, 384, 1.92, 253, 59.0, 4.83, 0.42)}
meth = "covered with film 1 d at 20±2 °C, then cured at 20±2 °C to 28 d (RH not reported)"
for k, (c, fa, s, ps, w, f, ft, eps) in hdc.items():
    Bk = c + fa
    mix = {"OPC / Cement": R(c / Bk), "FA (Fly ash)": R(fa / Bk), "W / B": R(w / Bk), "River sand / B": R(s / Bk), "SP / B": R(ps / Bk, 5),
           "Binder content (kg/m³)": Bk}
    note = f"{k}: kg/m3 / binder {Bk} (cement {c} + FA {fa}); river sand {s} (max 1.18 mm), powdered PCE {ps}, water {w}. PVA 26 kg/m3 = 2 vol%."
    add(base, **mix, **{"Curing method": meth, "Compressive strength (MPa)": f, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                        "Source table/page": "Table 1 (mix), Table 4 (28 d results)", "Conversions / notes": note})
    if k == "HDC-1":
        for T, fcu, ftT, epsT in [(-30, 46.7, 3.74, 1.34), (0, 47.1, 3.99, 1.46), (40, 50.9, 4.46, 1.23), (60, 52.7, 4.80, 1.31)]:
            add(base, **mix, **{"Curing method": meth + f"; then held 8 h at {T} °C and 1 h at room temperature before testing",
                                "Heat curing duration (h)": 8 if T > 20 else None,
                                "Compressive strength (MPa)": fcu, "Tensile strength (MPa)": ftT, "Tensile strain capacity (%)": epsT,
                                "Source table/page": "Table 1 (mix), Table 5 (fcu), Table 6 (tension)",
                                "Conversions / notes": note + f" Post-curing temperature treatment {T} °C for 8 h at age 28 d (axial prism fc {dict([(-30, 42.0), (0, 42.5), (40, 45.7), (60, 47.6)])[T]} MPa); cube fcu recorded. 'Curing temperature' column = 20 °C standard curing; treatment temperature only in text columns."})

# ------------------------------------------------------------------ 3 Feng et al. 2021, HD magnesium phosphate cement composite, air vs water curing
base = {"Article Name": "Mechanical Properties and Water Stability of High Ductility Magnesium Phosphate Cement-Based Composites (HDMC)",
        "Author": "Feng H., Wang Y., Guo A., Zhao X., Rahier H.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14123169",
        "Other binder": 0.8, "FA (Fly ash)": 0.2, "SS / B (Silica sand)": 0.2, "Sand max size (µm)": 180,
        "PVA fiber (vol%)": 1.6, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41,
        "Total fiber (vol%)": 1.6, "Curing temperature (°C)": 25, "Curing RH (%)": 45, "Demolding age (days)": 0.083,
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "50x50x50"}
hdmc = [  # (W/B, M/P, ambient d, water d, fc)
    (0.16, 4, 7, 0, 44.8), (0.16, 4, 28, 0, 40.0), (0.16, 4, 7, 7, 42.5),
    (0.14, 4, 7, 0, 49.5), (0.14, 4, 7, 7, 47.1), (0.20, 4, 7, 0, 43.8), (0.20, 4, 7, 7, 41.4),
    (0.16, 3, 7, 0, 33.7), (0.16, 3, 7, 7, 30.1), (0.16, 6, 7, 0, 49.2), (0.16, 6, 7, 7, 46.3)]
for wb, mp, amb, wat, f in hdmc:
    m = f"ambient curing room 25±2 °C, RH 45±5% for {amb} d (demoulded at 2 h)" + (f", then immersed in water {wat} d" if wat else "")
    add(base, **{"W / B": wb, "Curing method": m, "Curing time (days)": amb + wat, "Test age (days)": amb + wat, "Compressive strength (MPa)": f,
                 "Source table/page": "Table 6 (mix), Sect. 3.1.1/3.2.1/3.3.1 text (fc)",
                 "Conversions / notes": f"W/B {wb}, M/P {mp} (molar MgO/KH2PO4). Binder B = MPC (dead-burned MgO + KH2PO4, recorded in Other binder) 80% + FA 20%; "
                                        f"quartz sand S/B 0.2 (120-180 um); borax retarder 6% of MgO mass (no column). fc values quoted in text (also in Fig. 6/8/10)."})

# ------------------------------------------------------------------ 4 Chaves Figueiredo et al. 2020, printed SHCC, 14 / 28 / 35 d
base = {"Article Name": "Mechanical Behavior of Printed Strain Hardening Cementitious Composites",
        "Author": "Chaves Figueiredo S., Romero Rodríguez C., Ahmed Z.Y., Bos D.H., Xu Y., Salet T.M., Çopuroğlu O., Schlangen E., Bos F.P.", "Year": 2020,
        "DOI / URL": "https://doi.org/10.3390/ma13102253", "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
        "Curing method": "3D printed; covered with plastic foil + wet fabric 24 h, then chamber 20±2 °C, RH 98±2%", "Curing temperature (°C)": 20,
        "Curing RH (%)": 98, "Demolding age (days)": 1}
mixes = {"XVA3PVA20": dict(c=259.2, bfs=604.9, fa=0, lp=864.1, s=0, hp=5.1, sp=17.3, w=345.6),
         "YVA4PVA20-S05": dict(c=480.2, bfs=0, fa=567.6, lp=109.1, s=480.3, hp=6.5, sp=13.0, w=327.4)}
fc_p = {"XVA3PVA20": {("perpendicular", 14): 37.63, ("perpendicular", 28): 44.09, ("parallel", 14): 34.98, ("parallel", 28): 41.93},
        "YVA4PVA20-S05": {("perpendicular", 14): 14.57, ("perpendicular", 28): 17.66, ("parallel", 14): 12.03, ("parallel", 28): 15.02}}
ten_p = {"XVA3PVA20": {"LPA": (1.53, 2.4, 0.26), "LPE": (1.84, 2.41, 0.31)}, "YVA4PVA20-S05": {"LPA": (1.28, 1.64, 0.15), "LPE": (1.15, 1.65, 0.29)}}
for k, m in mixes.items():
    Bk = m["c"] + m["bfs"] + m["fa"] + m["lp"]
    mix = {"OPC / Cement": R(m["c"] / Bk), "GGBS": R(m["bfs"] / Bk) if m["bfs"] else None, "FA (Fly ash)": R(m["fa"] / Bk) if m["fa"] else None,
           "Limestone powder": R(m["lp"] / Bk), "W / B": R(m["w"] / Bk), "Fine sand / B": R(m["s"] / Bk) if m["s"] else None,
           "Sand max size (µm)": 500 if m["s"] else None, "SP / B": R(m["sp"] / Bk, 5), "HPMC / B (hydroxypropyl methyl cellulose)": R(m["hp"] / Bk, 5),
           "Binder content (kg/m³)": R(Bk, 1)}
    note = (f"{k}: kg/m3 / powder binder {Bk:.1f} (CEM I {m['c']}, BFS {m['bfs']}, FA {m['fa']}, limestone powder {m['lp']} - all powders taken as binder); "
            f"sand 125-500 um {m['s']}, HPMC {m['hp']}, SP {m['sp']}, water {m['w']}. PVA 26 kg/m3 = 2 vol% (fibre properties not given in this paper).")
    for (d_, age), f in fc_p[k].items():
        add(base, **mix, **{"Curing time (days)": age, "Test age (days)": age, "Compressive specimen": f"cube sawn from printed beam, load {d_} to layers",
                            "Compressive specimen size (mm)": "35x35x35", "Compressive strength (MPa)": f,
                            "Source table/page": "Table 1 (mix), Table 2 (fc)", "Conversions / notes": note})
    for d_, (fcr, ft, eps) in ten_p[k].items():
        add(base, **mix, **{"Curing time (days)": 35, "Test age (days)": 35,
                            "Tensile specimen": "sawn printed single-layer prism, " + ("loaded parallel to print direction, 150x40 mm" if d_ == "LPA" else "loaded perpendicular, 30x35 mm"),
                            "Tensile test type": "direct", "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                            "Source table/page": "Table 1 (mix), Tables 4-5 (tension)",
                            "Conversions / notes": note + " Strain = deformation at maximum tensile strength (Table 5)."})

# ------------------------------------------------------------------ 5 Ogura et al. 2018, printable PE-SHCC, water curing 7 d then 65% RH, 28 d
base = {"Article Name": "Developing and Testing of Strain-Hardening Cement-Based Composites (SHCC) in the Context of 3D-Printing",
        "Author": "Ogura H., Nerella V.N., Mechtcherine V.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/ma11081375",
        "OPC / Cement": 0.75, "SF (Silica fume)": 0.15, "FA (Fly ash)": 0.10, "W / B": 0.22, "Sand max size (µm)": 1000,
        "PE length (mm)": 6, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 3000,
        "Curing method": "sealed 24 h, water curing 7 d (age 1-8 d), then climatic chamber 20 °C / 65% RH to test",
        "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 65, "Demolding age (days)": 1, "Test age (days)": 28,
        "Tensile gauge length (mm)": 100, "Tensile test type": "direct"}
for k, sb, vf, fcr, ft, eps, fcv in [("B-print", 0.5, 1.0, 4.18, 5.32, 0.88, None), ("B-cast", 0.5, 1.0, 4.09, 4.53, 0.58, 105),
                                     ("C-print", 0.2, 1.5, 4.25, 5.66, 3.21, None), ("C-cast", 0.2, 1.5, 4.63, 6.32, 1.67, 104)]:
    pr = k.endswith("print")
    add(base, **{"Fine sand / B": sb, "PE fiber (vol%)": vf, "Total fiber (vol%)": vf,
                 "Tensile specimen": "prism 250x24x40 sawn from printed wall (glued ends)" if pr else "mould-cast dumbbell, 24x40 mm section",
                 "Compressive specimen": None if pr else "cube", "Compressive specimen size (mm)": None if pr else "100x100x100",
                 "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps, "Compressive strength (MPa)": fcv,
                 "Source table/page": "Sect. 2.1 + Table 1 (mix), Table 3 (results)",
                 "Conversions / notes": f"Mixture {k[0]} ({'printed' if pr else 'cast'}): binder = 75% CEM II/A-M (S-LL) 52.5R + 15% silica fume (slurry) + 10% FA by mass; "
                                        f"W/B {0.22}, S/B {sb} (fine sand <=1 mm), HDPE fibre {vf} vol% (density 0.97). SP content not reported."})

# ------------------------------------------------------------------ 6 Jang et al. 2014, sustainable SHCC (PVA + recycled PET), 28 / 74 d virgin specimens
B = 986.0  # cement 888 + FA 98
base = {"Article Name": "Influence of Rapid Freeze-Thaw Cycling on the Mechanical Properties of Sustainable Strain-Hardening Cement Composite (2SHCC)",
        "Author": "Jang S.-J., Rokugo K., Park W.-S., Yun H.-D.", "Year": 2014, "DOI / URL": "https://doi.org/10.3390/ma7021422",
        "OPC / Cement": R(888 / B), "FA (Fly ash)": R(98 / B), "W / B": R(444 / B), "SS / B (Silica sand)": R(355 / B), "VMA / B": R(0.53 / B, 5),
        "SP / B": R(6.91 / B, 5), "Binder content (kg/m³)": B, "PVA fiber (vol%)": R(19.2 / 1300 * 100, 3), "PVA length (mm)": 12, "PVA diameter (µm)": 40,
        "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40, "PET fiber (vol%)": R(5.05 / 1380 * 100, 3),
        "Total fiber (vol%)": R(19.2 / 1300 * 100 + 5.05 / 1380 * 100, 3),
        "Curing method": "demoulded 24 h, standard curing room 20±3 °C, RH 95% (reference specimens kept there to test)",
        "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
        "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200"}
note = ("Virgin (no freeze-thaw) 2SHCC: kg/m3 / binder 986 (cement 888 + FA 98); water 444, silica sand 355 (avg 110 um), recycled concrete sand 39 "
        "(max 3 mm, RS/B 0.0396; no template column), MC 0.53, SP 6.91, PVA 19.2 kg/m3 (/1300), recycled PET fibre 5.05 kg/m3 (10 mm, 33 um; density not given, "
        "1380 assumed for vol%).")
add(base, **{"Curing time (days)": 28, "Test age (days)": 28, "Compressive strength (MPa)": 37.9, "Tensile specimen": "dumbbell (JSCE)",
             "Tensile gauge length (mm)": 80, "Tensile test type": "direct", "First-cracking strength (MPa)": 3.41, "Tensile strength (MPa)": 4.76,
             "Tensile strain capacity (%)": 0.20, "Source table/page": "Table 1 (mix), Table 2 (fc), Table 3 (tension, 0 cycle)", "Conversions / notes": note})
add(base, **{"Curing time (days)": 74, "Test age (days)": 74, "Compressive strength (MPa)": 46.3,
             "Source table/page": "Table 1 (mix), Table 2 (fc)", "Conversions / notes": note})

# ------------------------------------------------------------------ 7 Su et al. 2026, rapid-hardening OPC-SAC ECC with recycled fine aggregate, 1-28 d
base = {"Article Name": "Rapid-Hardening Engineered Cementitious Composites with OPC-SAC Binder and Recycled Fine Aggregates: Mechanical Properties and Micro-Mechanisms",
        "Author": "Su Z., Gong J., Wang X., Hua M., Wang J.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19112355",
        "PVA fiber (vol%)": R(25.8 / 1280 * 100, 3), "PVA length (mm)": 12, "PVA diameter (µm)": 15, "PVA tensile strength (MPa)": 1830,
        "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": R(25.8 / 1280 * 100, 3), "Sand max size (µm)": 1180,
        "Curing method": "demoulded 24 h, standard curing room 20±2 °C, RH >=95% to test", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
        "Demolding age (days)": 1, "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160",
        "Tensile specimen": "dog-bone 330 mm, 30x13 mm section (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
su = {  # id: SAC, OPC, FA, SF, eff water, absorbed water, RFA, NFA, HRWR
    "N-25-0.27": (161.6, 484.8, 517.1, 129.3, 349.1, 8.0, 0, 465.4, 10.3), "R-0-0.27": (0, 644.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
    "R-25-0.27": (161.0, 483.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3), "R-50-0.27": (322.0, 322.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
    "R-75-0.27": (483.0, 161.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3), "R-100-0.27": (644.0, 0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
    "R-25-0.21": (174.6, 523.9, 558.8, 139.7, 293.4, 43.8, 503.0, 0, 11.2), "R-25-0.24": (167.5, 502.6, 536.1, 134.0, 321.7, 42.0, 482.5, 0, 10.7),
    "R-25-0.30": (155.0, 464.9, 495.9, 124.0, 371.9, 38.9, 446.3, 0, 9.9), "R-25-0.33": (149.4, 448.1, 478.0, 119.5, 394.3, 37.5, 430.2, 0, 9.6)}
# (id, age) -> dict of outputs, (value, verify-flag)
out = {("R-0-0.27", 1): {"fc": 6.8}, ("R-25-0.27", 1): {"fc": 19.3, "ft": 3.21}, ("R-50-0.27", 1): {"fc": 21.4}, ("R-75-0.27", 1): {"fc": 24.2},
       ("R-100-0.27", 1): {"fc": 25.6},
       ("R-0-0.27", 28): {"fc": 50.1}, ("R-25-0.27", 28): {"fc": 47.9, "fcr": 3.12, "ft": 3.91, "eps": 3.13}, ("R-50-0.27", 28): {"fc": 43.9},
       ("R-75-0.27", 28): {"fc": 44.3}, ("R-100-0.27", 28): {"fc": 40.4},
       ("R-25-0.21", 1): {"fc": 27.2}, ("R-25-0.21", 3): {"fc": 34.4}, ("R-25-0.21", 28): {"fc": 53.6}, ("R-25-0.24", 28): {"fc": 50.2},
       ("R-25-0.30", 28): {"fc": 45.2}, ("R-25-0.33", 1): {"fc": 13.5}, ("R-25-0.33", 28): {"fc": 48.4},
       ("R-25-0.27", 3): {"fc": 29.5, "ft": R(3.21 / 0.882, 2), "V": "VERIFY fc ~29.5 read as 'approximately' in text (Fig. 9); ft = 3.21/0.882 derived from % in text."},
       ("R-25-0.27", 7): {"fc": 33.5, "ft": R(3.21 / 0.856, 2), "V": "VERIFY fc ~33.5 'approximately' in text (Fig. 9); ft = 3.21/0.856 derived from % in text."},
       ("N-25-0.27", 1): {"fc": 22, "V": "VERIFY fc ~22 'approximately' in text (Fig. 9)."},
       ("N-25-0.27", 3): {"fc": 38, "V": "VERIFY fc ~38 'approximately' in text (Fig. 9)."},
       ("N-25-0.27", 7): {"fc": 44, "V": "VERIFY fc ~44 'approximately' in text (Fig. 9)."},
       ("N-25-0.27", 28): {"fc": R(47.9 / (1 - 0.104), 1), "eps": 2.71, "V": "VERIFY fc derived: RFA 28 d fc 47.9 is 10.4% below NFA (text); strain 2.71% quoted in text."}}
for (k, age), o in out.items():
    sac, opc, fa, sf, w, aw, rfa, nfa, hr = su[k]
    Bk = sac + opc + fa + sf
    agg = (f"recycled fine aggregate {rfa} kg/m3 (0.075-1.18 mm, RFA/B {rfa / Bk:.4f}; no template column)" if rfa else
           f"natural river sand {nfa} kg/m3")
    note = (f"{k} {age} d: kg/m3 / binder {Bk:.1f} (R-SAC 42.5 {sac}, P.O 52.5 {opc}, FA {fa}, SF {sf}); effective water {w} (W/B), "
            f"absorbed water {aw} (Extra water/B); {agg}; HRWR {hr}. PVA 25.8 kg/m3 / 1280 (paper density) = 2.02 vol%. Values from text (Sect. 3).")
    if "V" in o:
        note += " " + o["V"]
    add(base, **{"OPC / Cement": R(opc / Bk) if opc else None, "SAC (Calcium sulfoaluminate cement)": R(sac / Bk) if sac else None,
                 "FA (Fly ash)": R(fa / Bk), "SF (Silica fume)": R(sf / Bk), "W / B": R(w / Bk), "Extra water / B": R(aw / Bk),
                 "River sand / B": R(nfa / Bk) if nfa else None, "HRWR / B": R(hr / Bk, 5), "Binder content (kg/m³)": R(Bk, 1),
                 "Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": o.get("fc"), "Tensile strength (MPa)": o.get("ft"),
                 "First-cracking strength (MPa)": o.get("fcr"), "Tensile strain capacity (%)": o.get("eps"),
                 "Source table/page": "Table 4 (mix), Sect. 3.2-3.4 text (results)", "Conversions / notes": note})

# ------------------------------------------------------------------ write
df = pd.DataFrame(rows, columns=H)
out_path = os.path.join(D, "w3_curing.csv")
df.to_csv(out_path, index=False, encoding="utf-8-sig")
print(out_path, len(df), "rows,", df["DOI / URL"].nunique(), "papers")
