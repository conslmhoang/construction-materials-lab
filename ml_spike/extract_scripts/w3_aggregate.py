"""Builder for w3_aggregate.csv - ECC/SHCC, fibre mortars and fibre UHPC/RPC with ALTERNATIVE FINE AGGREGATES
(recycled fine aggregate, desert/aeolian/dune sand, Yellow River sediment sand, superfine river sand, sea/coral sand +
seawater, manufactured/crushed sand, coal gangue sand, steel slag sand, sand size).
All values transcribed from the papers' full text (Europe PMC fullTextXML).
Run: python w3_aggregate.py  (writes ../additions/w3_aggregate.csv, UTF-8 with BOM)
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


# =====================================================================================================
# 1 Su et al. 2026 - rapid-hardening ECC, OPC-SAC binder, recycled fine aggregate (Materials 19:2355)
# =====================================================================================================
base = {"Article Name": "Rapid-Hardening Engineered Cementitious Composites with OPC–SAC Binder and Recycled Fine Aggregates: Mechanical Properties and Micro-Mechanisms",
        "Author": "Su Z., Gong J., Wang X., Hua M., Wang J.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19112355",
        "Sand max size (µm)": 1180,
        "PVA fiber (vol%)": R(25.8 / 1280 * 100, 2), "Total fiber (vol%)": R(25.8 / 1280 * 100, 2), "PVA length (mm)": 12, "PVA diameter (µm)": 15,
        "PVA tensile strength (MPa)": 1830, "PVA elastic modulus (GPa)": 40,
        "Curing method": "demoulded 24 h, standard curing room 20±2 °C, RH ≥95%", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
        "Demolding age (days)": 1, "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160"}
# mix: SAC, OPC, FA, SF, eff water, absorbed water, RFA, NFA, HRWR
su_mix = {"N-25-0.27": (161.6, 484.8, 517.1, 129.3, 349.1, 8.0, 0, 465.4, 10.3),
          "R-0-0.27": (0, 644.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
          "R-25-0.27": (161.0, 483.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
          "R-50-0.27": (322.0, 322.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
          "R-75-0.27": (483.0, 161.0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
          "R-100-0.27": (644.0, 0, 515.2, 128.8, 347.8, 40.4, 463.7, 0, 10.3),
          "R-25-0.21": (174.6, 523.9, 558.8, 139.7, 293.4, 43.8, 503.0, 0, 11.2),
          "R-25-0.24": (167.5, 502.6, 536.1, 134.0, 321.7, 42.0, 482.5, 0, 10.7),
          "R-25-0.30": (155.0, 464.9, 495.9, 124.0, 371.9, 38.9, 446.3, 0, 9.9),
          "R-25-0.33": (149.4, 448.1, 478.0, 119.5, 394.3, 37.5, 430.2, 0, 9.6)}
# (mix, age, fc, direct ft, fcr, eps, flexural strength, extra note)
su_res = [("R-0-0.27", 1, 6.8, None, None, None, 3.2, ""), ("R-0-0.27", 28, 50.1, None, None, None, None, ""),
          ("R-25-0.27", 1, 19.3, 3.21, None, None, 7.3, ""), ("R-25-0.27", 7, None, None, None, 3.85, None, ""),
          ("R-25-0.27", 28, 47.9, 3.91, 3.12, 3.13, 13.2, ""),
          ("R-50-0.27", 1, 21.4, None, None, None, 7.2, ""), ("R-50-0.27", 28, 43.9, None, None, None, None, ""),
          ("R-75-0.27", 1, 24.2, None, None, None, 8.5, ""), ("R-75-0.27", 28, 44.3, None, None, None, None, ""),
          ("R-100-0.27", 1, 25.6, None, None, None, 8.1, ""), ("R-100-0.27", 28, 40.4, None, None, None, None, ""),
          ("R-25-0.21", 1, 27.2, None, 2.97, 2.87, 8.81, ""), ("R-25-0.21", 3, 34.4, None, None, None, None, ""),
          ("R-25-0.21", 28, 53.6, None, None, 2.51, None, ""),
          ("R-25-0.24", 1, None, None, None, None, 7.9, ""), ("R-25-0.24", 28, 50.2, None, None, None, None, ""),
          ("R-25-0.30", 1, None, None, None, None, 6.6, ""), ("R-25-0.30", 28, 45.2, 3.41, None, 3.17, None, ""),
          ("R-25-0.33", 1, 13.5, None, 1.97, 3.67, 5.1, ""), ("R-25-0.33", 28, 48.4, 3.24, None, 3.51, None, ""),
          ("N-25-0.27", 28, R(47.9 / (1 - 0.104), 1), None, None, 2.71, None,
           "VERIFY fc derived: text says RFA reduced 28 d fc by 10.4% vs NFA -> 47.9/0.896. ")]
for mix, age, fc, ft, fcr, eps, fl, nn in su_res:
    sac, opc, fa, sf, w, wa, rfa, nfa, hr = su_mix[mix]
    B = sac + opc + fa + sf
    direct = (ft is not None) or (eps is not None) or (fcr is not None)
    kw = {"OPC / Cement": R(opc / B), "SAC (Calcium sulfoaluminate cement)": R(sac / B), "FA (Fly ash)": R(fa / B), "SF (Silica fume)": R(sf / B),
          "W / B": R(w / B), "Extra water / B": R(wa / B), "HRWR / B": R(hr / B, 5), "Binder content (kg/m³)": R(B, 1),
          "Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": fc}
    if nfa:
        kw["Sand (type not stated) / B"] = R(nfa / B)
    if direct:
        kw.update({"Tensile specimen": "dog-bone (JSCE), 330 mm long, gauge section 30x13 mm", "Tensile gauge length (mm)": 80,
                   "Tensile test type": "direct", "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr,
                   "Tensile strain capacity (%)": eps})
    elif fl is not None:
        kw.update({"Tensile specimen": "prism 40x40x160 (flexural)", "Tensile test type": "flexural", "Tensile strength (MPa)": fl})
    src = "Table 4 (mix), Sec. 3.1-3.3 text (results)"
    note = (f"{nn}Mix {mix}: kg/m3 / binder {B:.1f} (SAC+OPC+FA+SF). "
            + (f"Recycled fine aggregate (crushed concrete, FM 1.81, absorption 8.71%) RFA/B = {rfa / B:.4f} (no column), used oven-dry; "
               f"absorbed (compensation) water {wa} kg/m3 in Extra water/B; W/B is effective. " if rfa else
               f"Natural fine aggregate (FM 2.15, type not stated) NFA/B = {nfa / B:.4f}. ")
            + "PVA 25.8 kg/m3 / 1280 kg/m3 = 2.02 vol%. Aggregates 0.075-1.18 mm. "
            + (f"Flexural strength {fl} MPa (same age) not entered because direct tension is given. " if (direct and fl is not None) else "")
            + "Values only stated in text are entered; other ages/groups are figure-only (Figs 5-10).")
    add(base, **kw, **{"Source table/page": src, "Conversions / notes": note})

# =====================================================================================================
# 2 Xia et al. 2022 - PE-ECC with desert sand, washed desert sand, river sand, standard sand (Materials 15:7666)
# =====================================================================================================
base = {"Article Name": "Relationship between Fractal Dimension and Properties of Engineered Cementitious Composites with Different Aggregates",
        "Author": "Xia D., Chen R., Zhang D., Cheng J.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15217666",
        "OPC / Cement": 0.4, "FA (Fly ash)": 0.6, "SP / B": 0.0016,
        "PE fiber (vol%)": 1.5, "Total fiber (vol%)": 1.5, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
        "PE elastic modulus (GPa)": 110,
        "Curing method": "24 h at 18±2 °C, RH 65±5% in moulds; demoulded, standard curing box 20±2 °C, RH 95±5% for 28 d",
        "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
        "Tensile specimen": "dog-bone (Fig. 2, JC/T 2461-2018)", "Tensile test type": "direct",
        "Source table/page": "Table 3 (mix), Table 2 (fibre), Table 4 (tension)"}
xia = [("DSN-ECC", "Dune sand / B", "untreated desert sand (Taklimakan region, Xinjiang)", 2.74, 6.26, 3.638),
       ("DSY-ECC", "Dune sand / B", "water-washed desert sand", 2.63, 6.05, 1.827),
       ("RS-ECC", "River sand / B", "river sand", 2.49, 4.64, 2.752),
       ("SS-ECC", "SS / B (Silica sand)", "standard (quartz) sand", 3.16, 6.66, 3.282)]
for name, col, desc, fcr, ft, eps in xia:
    add(base, **{col: 0.62, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                 "Conversions / notes": (f"{name}: fine aggregate = {desc}. Table 3 gives weight ratios C 1.0 : FA 1.5 : sand 1.55 : W 0.34 : SP 0.004 : "
                                         "RLP (redispersible latex powder) 0.004 : PE 1.5 vol%; B = C+FA = 2.5 -> sand/B 0.62, SP/B 0.0016, RLP/B 0.0016 (no column). "
                                         "W/B left empty: taken literally W/B = 0.34/2.5 = 0.136, which is implausibly low for this mix; 0.34 may instead be W/B - not stated. "
                                         "fc only in Fig. 4 (order DSN > DSY > SS > RS; DSN = 1.16 x RS). Gauge length not stated.")})

# =====================================================================================================
# 3 Ling et al. 2020 - sand size, PVA + nano-SiO2 cementitious composite (Materials 13:325)
# =====================================================================================================
base = {"Article Name": "Effect of Sand Size on Mechanical Performance of Cement-Based Composite Containing PVA Fibers and Nano-SiO2",
        "Author": "Ling Y.F., Zhang P., Wang J., Shi Y.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13020325",
        "OPC / Cement": 0.63, "FA (Fly ash)": 0.35, "Nano-SiO2": 0.02, "W / B": 0.38, "SS / B (Silica sand)": 0.5, "HRWR / B": 0.003,
        "Binder content (kg/m³)": 1000,
        "PVA fiber (vol%)": 0.9, "Total fiber (vol%)": 0.9, "PVA length (mm)": 9, "PVA diameter (µm)": 20, "PVA tensile strength (MPa)": 1400,
        "Curing method": "demoulded at 1 d, room 20 °C, RH 95% for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
        "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
        "Tensile specimen": "prism 40x40x160, 3-point, span 100 mm", "Tensile test type": "flexural"}
add(base, **{"Sand max size (µm)": 830, "Compressive strength (MPa)": 70.6, "Tensile strength (MPa)": 8.3,
             "Source table/page": "Table 5 (mix), Sec. 3.2-3.3 text",
             "Conversions / notes": "Mix a: silica sand 380-830 µm. kg/m3 / binder 1000 (cement 630 + FA 350 + NS 20). fc 70.6 MPa (max, Mix a) and flexural 8.3 MPa stated in text; "
                                    "compressive specimen not stated. Uniaxial tension (305x76x20 plates) only in Figs 9-10."})
add(base, **{"Sand max size (µm)": 120, "Tensile strength (MPa)": 6.6, "Source table/page": "Table 5 (mix), Sec. 3.3 text",
             "Conversions / notes": "Mix d: silica sand 75-120 µm. Flexural 6.6 MPa (20% below Mix a) stated in text; fc for Mix d figure-only. "
                                    "Mixes b (212-380 µm) and c (120-212 µm) figure-only."})

# =====================================================================================================
# 4 Zhang et al. 2024 - Yellow River sand ECC, four curing methods x three ages (Materials 17:4307)
# =====================================================================================================
B = 1170.0
base = {"Article Name": "The Influence and Mechanism of Curing Methods and Curing Age on the Mechanical Properties of Yellow River Sand Engineered Cementitious Composites",
        "Author": "Zhang K., Wu W., Fan J., Yuan C.", "Year": 2024, "DOI / URL": "https://doi.org/10.3390/ma17174307",
        "OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": R(410 / B), "SP / B": R(3.5 / B, 5), "VMA / B": R(1.8 / B, 5),
        "Binder content (kg/m³)": B,
        "PVA fiber (vol%)": R(19 / 1300 * 100, 2), "Total fiber (vol%)": R(19 / 1300 * 100, 2), "PVA length (mm)": 12, "PVA diameter (µm)": 40,
        "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41,
        "Compressive specimen": "prism", "Compressive specimen size (mm)": "40x40x160"}
cur = {"B": ("standard curing: room 20±2 °C, RH >95% after demoulding", 20, 95),
       "Z": ("steam curing box 3 d after demoulding (temperature not stated), then 20±2 °C, RH 50%", 20, 50),
       "S": ("sprinkler curing: indoors under geotextile, watered morning and evening", None, None),
       "K": ("natural curing: room 20±2 °C, RH 50%", 20, 50)}
# (code, age, fc, flexural, direct ft, eps, fcr)
zh = [("B", 14, 22.9, 9.9, None, None, None), ("B", 28, 26.4, 11.5, 1.83, 3.71, 0.47), ("B", 90, 32.7, 14.0, 1.27, 1.86, None),
      ("Z", 14, 33.0, 14.8, 1.82, None, None), ("Z", 28, 34.9, 15.7, 2.05, 4.03, None), ("Z", 90, 38.7, 17.6, 1.62, 3.18, None),
      ("S", 14, 27.7, 11.8, None, None, None), ("S", 28, 29.3, 12.5, 1.46, 1.91, None), ("S", 90, 31.6, 13.4, 1.17, 0.73, None),
      ("K", 14, 27.3, 11.7, 1.3, 4.70, None), ("K", 28, 30.8, 13.2, 1.79, 4.37, None), ("K", 90, 31.1, 13.3, 1.59, 4.25, None)]
for code, age, fc, fl, ft, eps, fcr in zh:
    meth, T, RH = cur[code]
    kw = {"River sand / B": R(700 / B), "Sand max size (µm)": 355, "Curing method": meth, "Curing time (days)": age, "Curing temperature (°C)": T,
          "Curing RH (%)": RH, "Test age (days)": age, "Compressive strength (MPa)": fc}
    if ft is not None:
        kw.update({"Tensile specimen": "dog-bone 330x60x13", "Tensile test type": "direct", "Tensile strength (MPa)": ft,
                   "Tensile strain capacity (%)": eps, "First-cracking strength (MPa)": fcr})
        extra = f"Flexural strength {fl} MPa (Table 5) not entered because direct tension is given. "
    else:
        kw.update({"Tensile specimen": "prism 40x40x160 (flexural)", "Tensile test type": "flexural", "Tensile strength (MPa)": fl})
        extra = "Direct-tension values at this age only in Fig. 6. "
    if code == "K" and age == 14:
        extra += "Flexural given as 11.7 (Table 5) vs 11.6 (Table 6). "
    if code == "Z":
        extra += "Heat curing temperature/duration of steam box not stated (3 d in box). "
    add(base, **kw, **{"Source table/page": "Table 3 (mix), Tables 5-6 (fc, flexural), Table 7 + Sec. 3.2 text (tension)",
                       "Conversions / notes": f"{code}{age}: Yellow River sediment sand (YRS, 0-355 µm, D50 69 µm) entered as River sand/B; kg/m3 / binder 1170 (cement 585 + FA 585). "
                                              f"PVA 19 kg/m3 / 1300 kg/m3 = 1.46 vol%. {extra}Gauge length not stated."})
add(base, **{"SS / B (Silica sand)": R(700 / B), "Sand max size (µm)": 565, "Curing method": cur["B"][0], "Curing time (days)": 28,
             "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Test age (days)": 28,
             "Tensile specimen": "dog-bone 330x60x13", "Tensile test type": "direct", "First-cracking strength (MPa)": 0.48,
             "Tensile strength (MPa)": 1.60, "Tensile strain capacity (%)": 3.20,
             "Source table/page": "Table 3 (mix), Table 7 (tension)",
             "Conversions / notes": "B'28 traditional quartz-sand ECC (quartz sand 80-120 mesh, 0-565 µm). Same mix as YRS-ECC with quartz sand. fc not reported numerically."})

# =====================================================================================================
# 5 Lv et al. 2023 - PE-ECC with desert sand vs river sand of different sizes (Materials 16:697)
# =====================================================================================================
B = 617.2 + 411.4
base = {"Article Name": "Experimental Study on Toughness of Engineered Cementitious Composites with Desert Sand",
        "Author": "Lv Z., Han Y., Han G., Ge X., Wang H.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16020697",
        "OPC / Cement": R(617.2 / B), "GGBS": R(411.4 / B), "W / B": R(250 / B), "SP / B": R(6 / B, 5), "HPMC / B (hydroxypropyl methyl cellulose)": R(0.5 / B, 6),
        "Binder content (kg/m³)": R(B, 1), "Sand max size (µm)": 300,
        "PE fiber (vol%)": R(12 / 970 * 100, 2), "Total fiber (vol%)": R(12 / 970 * 100, 2), "PE length (mm)": 12, "PE diameter (µm)": 24,
        "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120,
        "Curing method": "demoulded 24 h, curing room 20±1 °C, RH 95%", "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
        "Tensile specimen": "dumbbell, test section 100x30x15", "Tensile gauge length (mm)": 100, "Tensile test type": "direct",
        "Source table/page": "Table 3 (mix), Table 2 (fibre), Sec. 3.1 text (tension)"}
for grp, col, desc, age, fcr, ft, eps, nn in [
        ("A", "Dune sand / B", "desert sand (Wuqia County, Kezhou), 0.075-0.3 mm", 7, 2.09, 4.47, 5.80, ""),
        ("A", "Dune sand / B", "desert sand (Wuqia County, Kezhou), 0.075-0.3 mm", 28, 2.51, 4.97, 6.78, "Conclusions state max strain 6.17% for desert-sand ECC (inconsistent with 6.78% in Sec. 3.1). "),
        ("B", "River sand / B", "ordinary river sand (Kashi), 0.075-0.3 mm", 7, 2.06, 4.06, 4.06, ""),
        ("B", "River sand / B", "ordinary river sand (Kashi), 0.075-0.3 mm", 28, 2.64, 4.57, 8.13, "")]:
    add(base, **{col: R(308.6 / B), "Curing time (days)": age, "Test age (days)": age, "First-cracking strength (MPa)": fcr,
                 "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                 "Conversions / notes": f"{nn}Group {grp}: {desc}. kg/m3 / binder {B:.1f} (cement 617.2 + S95 slag 411.4). PE 12 kg/m3 / 970 = 1.24 vol%. "
                                        "No fc reported. Groups C-E (river sand 0.3-0.6, 0.6-1.18, 0.075-1.18 mm) figure-only."})

# =====================================================================================================
# 6 Gyawali 2023 - high ductile mortar, crushed sand vs river sand (Heliyon 9:e14452)
# =====================================================================================================
base = {"Article Name": "Effect of sand types and mixing procedures on the flexural behaviour of the high ductile mortar in monotonic and cyclic loadings",
        "Author": "Gyawali T.R.", "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.heliyon.2023.e14452",
        "OPC / Cement": 1.0, "W / B": 0.32, "SP / B": 0.01, "VMA / B": 0.00128, "Binder content (kg/m³)": 1250,
        "Curing method": "air 24 h, then water tank until test", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
        "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100",
        "Tensile specimen": "beam 400x100x50, 4-point (JIS A 1106)", "Tensile test type": "flexural",
        "Source table/page": "Table 3 (mix), Table 5 (fc), Tables 6-7 (flexural, monotonic)"}
PVA = {"PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
       "PVA elastic modulus (GPa)": 41}
for name, sand, fib, fc, ft, fcr, nn in [
        ("PM", "C", False, 73.5, 4.78, 4.78, "Plain mortar (no fibre), crushed sand 499 kg/m3."),
        ("HDMPMC", "C", True, 75.0, 10.3, 4.86, "Crushed sand, pre-mixed mortar mixing method."),
        ("HDMPMR", "R", True, 75.5, 11.4, 5.16, "River sand, pre-mixed mortar mixing method."),
        ("HDMPPC", "C", True, 67.6, 8.2, 4.05, "Crushed sand, pre-mixed paste mixing method."),
        ("HDMPPR", "R", True, 70.2, 10.5, 4.14, "River sand, pre-mixed paste mixing method.")]:
    kw = dict(PVA) if fib else {"Total fiber (vol%)": 0}
    if sand == "C":
        kw.update({"M-sand / B": R((499 if name == "PM" else 489) / 1250), "Sand max size (µm)": 5000})
    else:
        kw.update({"River sand / B": R(476 / 1250), "Sand max size (µm)": 1200})
    kw.update({"Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr})
    add(base, **kw, **{"Conversions / notes": f"{name}: {nn} kg/m3 / cement 1250 (Type III OPC). W/C 0.32 (SP counted as water), SP 1.0% of C, "
                                              "viscosity agent 0.4% of W = 1.6 kg/m3 in VMA/B. Crushed sand FM 2.34 (Gmax 5 mm, entered as M-sand); river sand FM 1.83 (Gmax 1.2 mm). "
                                              "PVA REC15 26 kg/m3 = 2 vol% (paper). Tensile strength = max monotonic flexural stress, first-crack = flexural yield stress. "
                                              "Cyclic-loading values in Table 6 not entered."})

# =====================================================================================================
# 7 Long et al. 2019 - fibre-reinforced seawater coral sand mortar (Materials 13:118)
# =====================================================================================================
B = 727 + 182.0
base = {"Article Name": "Dynamic Mechanical Behavior of Fiber-Reinforced Seawater Coral Mortars",
        "Author": "Long W.J., Tang J., Li H.D., Wang Y., Luo Q.L.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma13010118",
        "OPC / Cement": R(727 / B), "FA (Fly ash)": R(182 / B), "W / B": R(364 / B), "HRWR / B": R(1.6 / B, 5),
        "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8,
        "Curing method": "demoulded, standard curing room 20 °C, RH 95%", "Curing time (days)": 28, "Curing temperature (°C)": 20,
        "Curing RH (%)": 95, "Test age (days)": 28, "Compressive specimen": "prism", "Compressive specimen size (mm)": "40x40x160",
        "Source table/page": "Table 5 (mix), Sec. 3.1 text (fc)"}
for name, river, coral, vf, fc, nn in [
        ("SCM-1", 1000, 0, 0, R(44.6 / (1 - 0.159), 1), "VERIFY fc derived: SCM-4 (44.6) is 15.9% below SCM-1 -> 44.6/0.841. "),
        ("SCM-2", 700, 300, 0, R(44.6 / (1 - 0.159) * (1 - 0.038), 1), "VERIFY fc derived from SCM-1 (derived) x (1-3.8%). "),
        ("SCM-3", 400, 600, 0, R(44.6 / (1 - 0.159) * (1 - 0.112), 1), "VERIFY fc derived from SCM-1 (derived) x (1-11.2%). "),
        ("SCM-4", 0, 1000, 0, 44.6, ""), ("SCM-5", 0, 1000, 0.25, 45.0, ""), ("SCM-6", 0, 1000, 0.5, 45.5, ""), ("SCM-7", 0, 1000, 1.0, 46.4, "")]:
    kw = {"Total fiber (vol%)": vf, "Compressive strength (MPa)": fc}
    if vf:
        kw["PVA fiber (vol%)"] = vf
    if river:
        kw["River sand / B"] = R(river / B)
    if coral:
        kw["Sea sand / B"] = R(coral / B)
    add(base, **kw, **{"Conversions / notes": f"{nn}{name}: batch masses (g) / binder 909 g (cement 727 + FA 182). Mixing water = South China Sea seawater for all mixes "
                                              "(Table 2 ions). Coral sand (South China Sea) entered as Sea sand/B; 'natural river sand' is ISO standard sand (Xiamen ISO Standard Co.). "
                                              "Flexural strengths only as % changes (figure). Specimen sizes per text: 40x40x160 (compression), 40x40x80 (flexure)."})

# =====================================================================================================
# 8 Wan et al. 2022 - PP-ECC with superfine river sand (SSPP-ECC) (Materials 15:2474)
# =====================================================================================================
add({"Article Name": "Preliminary Exploration of Economic Polypropylene-Fiber-Reinforced ECC with Superfine River Sand (SSPP-ECC) Applied to a Bridge Pavement Leveling Overlay",
     "Author": "Wan F., Zhu Z., Wang W., Tan G., Yang R., Zhang Z.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15072474"},
    **{"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.3, "River sand / B": 0.5, "Sand max size (µm)": 600, "HRWR / B": R(10 / 1040, 5),
       "Binder content (kg/m³)": 1040, "PP fiber (vol%)": 2.0, "PP length (mm)": 12, "PP diameter (µm)": 30, "Total fiber (vol%)": 2.0,
       "Curing method": "demoulded 24 h, standard curing 20±2 °C, RH >95%", "Curing time (days)": 28, "Curing temperature (°C)": 20,
       "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
       "Tensile specimen": "prism 100x100x400 (JTG 3420 T0558)", "Tensile test type": "flexural", "Tensile strength (MPa)": 6.59,
       "Source table/page": "Table 3 (mix), Table 2 (fibre), Sec. 3.1 text",
       "Conversions / notes": "SSPP-ECC: kg/m3 / binder 1040 (OPC 52.5R 520 + FA 520); superfine river sand 520 kg/m3 (max 0.6 mm). PP 18.2 kg/m3 / 910 = 2.0 vol%; "
                              "PP strength 500 MPa, modulus 3.5 GPa. fc (150 mm cubes) only in Fig. 7; Young's modulus 25.17 GPa."})

# =====================================================================================================
# 9 Ahmed et al. 2021 - dune sand RPC with steel fibres, hot air curing (Materials 15:41)
# =====================================================================================================
base = {"Article Name": "Microstructure and Mechanical Property Evaluation of Dune Sand Reactive Powder Concrete Subjected to Hot Air Curing",
        "Author": "Ahmed S., Mahaini Z., Abed F., Mannan M.A., Al-Samarai M., Cattaneo S.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma15010041",
        "Sand max size (µm)": 1180,
        "Steel fiber (vol%)": 1.8, "Steel length (mm)": 13, "Steel diameter (µm)": 160, "Steel tensile strength (MPa)": 3000, "Total fiber (vol%)": 1.8,
        "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50"}
amix = {"CNTRL": (818, 272, 0, 0), "GB30": (571, 272, 222, 0), "GB15FA15": (571, 272, 122, 122)}
amb = "demoulded 24 h, 24 h ambient"
# (mix, age d, curing method, heat h, curing time, fc, note)
ahm = [("CNTRL", 2, amb + " (before oven, 0 h HAC)", None, 2, 77, ""),
       ("CNTRL", 2.5, amb + ", then hot air 100 °C 12 h", 12, 2.5, 138, ""),
       ("CNTRL", 3, amb + ", then hot air 100 °C 24 h", 24, 3, 155, ""),
       ("CNTRL", 7, amb + ", hot air 100 °C 24 h, then ambient to test", 24, 7, 160, "Highest strength of HAC+ambient series (average over ages 152 MPa). "),
       ("GB30", 2, amb + " (before oven, 0 h HAC)", None, 2, 68, ""),
       ("GB30", 2.5, amb + ", then hot air 100 °C 12 h", 12, 2.5, R(68 * 1.72, 1), "VERIFY fc derived: 0 h value 68 MPa +72% after 12 h HAC. "),
       ("GB30", 4, amb + ", then hot air 100 °C 48 h", 48, 4, 140, ""),
       ("GB30", 90, amb + ", hot air 100 °C 24 h, then ambient to test", 24, 90, 155, ""),
       ("GB15FA15", 2, amb + " (before oven, 0 h HAC)", None, 2, 55, ""),
       ("GB15FA15", 2.5, amb + ", then hot air 100 °C 12 h", 12, 2.5, R(55 * 2.37, 1), "VERIFY fc derived: 0 h value 55 MPa +137% after 12 h HAC. "),
       ("GB15FA15", 4, amb + ", then hot air 100 °C 48 h", 48, 4, 145, ""),
       ("GB15FA15", 90, amb + ", hot air 100 °C 24 h, then ambient to test", 24, 90, 156, "")]
for mix, age, meth, hh, ct, fc, nn in ahm:
    c, sf, gg, fa = amix[mix]
    B = c + sf + gg + fa
    kw = {"OPC / Cement": R(c / B), "SF (Silica fume)": R(sf / B), "W / B": R(185 / B), "M-sand / B": R(633 / B), "Dune sand / B": R(458 / B),
          "Binder content (kg/m³)": B, "Curing method": meth, "Curing time (days)": ct, "Test age (days)": age, "Heat curing duration (h)": hh,
          "Curing temperature (°C)": 100 if hh else None, "Compressive strength (MPa)": fc}
    if gg:
        kw["GGBS"] = R(gg / B)
    if fa:
        kw["FA (Fly ash)"] = R(fa / B)
    add(base, **kw, **{"Source table/page": "Table 2 (mix), Sec. 3.2 text (fc)",
                       "Conversions / notes": f"{nn}{mix}: kg/m3 / binder {B} (cement+SF+GGBS+FA); crushed sand 633 (150 µm-1.18 mm, M-sand/B) + UAE dune sand 458 "
                                              "(ratio 1.38, a/b 1.0). W/B 0.17 per paper. Steel 141 kg/m3 = 1.8 vol% (paper); brass-coated, 13 x 0.16 mm. "
                                              "SP dosage not stated. HAC ages: 0 h = 2 d after casting; oven time added to age. Flexural values figure-only."})

# =====================================================================================================
# 10 Chu et al. 2020 - recycled-sand UHPC with graphene oxide (Nanomaterials 10:1718)
# =====================================================================================================
B = 690 + 345 + 115 + 34.5
base = {"Article Name": "Effect of Graphene Oxide on Mechanical Properties and Durability of Ultra-High-Performance Concrete Prepared from Recycled Sand",
        "Author": "Chu H., Zhang Y., Wang F., Feng T., Wang L., Wang D.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/nano10091718",
        "OPC / Cement": R(690 / B), "FA (Fly ash)": R(345 / B), "SF (Silica fume)": R(115 / B), "Other binder": R(34.5 / B), "W / B": R(207 / B),
        "Binder content (kg/m³)": B,
        "Steel fiber (vol%)": 2.5, "Steel length (mm)": 20, "Steel diameter (µm)": 350, "Steel tensile strength (MPa)": 3000, "Total fiber (vol%)": 2.5,
        "Curing method": "sealed in moulds 48 h at room temperature, then standard curing room 20±1 °C, RH >95% for 28 d",
        "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 2, "Test age (days)": 28,
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
        "Tensile specimen": "cube 100 (splitting)", "Tensile test type": "splitting",
        "Source table/page": "Table 4 (mix), Sec. 3.1-3.3 text"}
for name, wr, go, fc, fsp, fl in [("RU0", 23, 0, 156.21, 13.37, 15.89), ("RU25", 24.6, 0.2875, 169.08, 15.46, 17.68),
                                   ("RU50", 29.4, 0.575, 182.50, 17.32, 20.12), ("RU75", 36.1, 0.8625, 174.23, 16.39, 19.24)]:
    add(base, **{"SP / B": R(wr / B, 5), "Compressive strength (MPa)": fc, "Tensile strength (MPa)": fsp,
                 "Conversions / notes": f"{name}: kg/m3 / binder {B} (cement 690 + FA 345 + SF 115 + CaO-type expansive agent 34.5 in Other binder). "
                                        f"Fine aggregate = 100% recycled sand (C&D waste, FM 2.45, absorption 6.13%) 1265 kg/m3, RS/B = {1265 / B:.4f} (no column). "
                                        f"Graphene oxide {go} kg/m3 (GO/B = {go / B:.6f}, no column). Hooked steel fibre 195 kg/m3 = 2.5 vol% (paper). "
                                        f"Four-point flexural strength {fl} MPa (100x100x400) not entered."})

# =====================================================================================================
# 11 Luo et al. 2022 - RPC with coal gangue sand replacing river sand (Materials 15:1807)
# =====================================================================================================
B = 312 + 223 + 125 + 89.0
base = {"Article Name": "Mechanical Properties of Reactive Powder Concrete with Coal Gangue as Sand Replacement",
        "Author": "Luo W., Wang H., Li X., Wang X., Wu Z., Zhang Y., Lian X., Li X.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15051807",
        "OPC / Cement": R(312 / B), "FA (Fly ash)": R(223 / B), "SF (Silica fume)": R(125 / B), "Limestone powder": R(89 / B),
        "Binder content (kg/m³)": B, "Sand max size (µm)": 2000,
        "Steel fiber (vol%)": R(160 / 7850 * 100, 2), "Steel length (mm)": 10, "Steel tensile strength (MPa)": 3000, "Total fiber (vol%)": R(160 / 7850 * 100, 2),
        "Curing method": "48 h in moulds at 20±1 °C, RH 95%; steam 95±1 °C, RH 95% for 24 h after demoulding; then 20±1 °C, RH 95%",
        "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 2, "Heat curing duration (h)": 24,
        "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160",
        "Source table/page": "Table 4 (mix), Sec. 3.2 text, Conclusions"}
for name, rs, cg, age, fc, fl, wb, nn in [
        ("CG0", 1234, 0, 14, 67.23, None, 0.29, "VERIFY W/B: Fig. 5 says w/b rose continuously from 0.29 to 0.42 with CG ratio (0.29 assigned to CG0). "),
        ("CG25", 925, 309, 14, 52.53, None, None, ""), ("CG50", 617, 617, 14, 47.23, None, None, ""),
        ("CG75", 309, 925, 14, 43.91, None, None, ""),
        ("CG100", 0, 1234, 7, None, 11.18, 0.42, "VERIFY W/B: 0.42 = upper end of the w/b range (Fig. 5) assigned to CG100. "),
        ("CG100", 0, 1234, 14, 37.03, 14.09, 0.42, "VERIFY W/B: 0.42 = upper end of the w/b range (Fig. 5) assigned to CG100. "),
        ("CG100", 0, 1234, 28, 28.44, 6.42, 0.42, "VERIFY W/B: 0.42 = upper end of the w/b range (Fig. 5) assigned to CG100. ")]:
    kw = {"W / B": wb, "Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": fc}
    if rs:
        kw["River sand / B"] = R(rs / B)
    if fl is not None:
        kw.update({"Tensile specimen": "prism 40x40x160 (flexural)", "Tensile test type": "flexural", "Tensile strength (MPa)": fl})
    add(base, **kw, **{"Conversions / notes": f"{nn}{name}: kg/m3 / binder {B:.0f} (P.O 42.5 + FA + SF + limestone flour). Coal gangue sand (crushed, <2 mm) "
                                              f"CG/B = {cg / B:.4f} (no column); river sand crushed to <2 mm. Water/SP adjusted per mix for 200±10 mm flow "
                                              "(w/b 0.29-0.42, only in Fig. 5). Copper-coated steel fibre 160 kg/m3 / 7850 = 2.04 vol%, 10 mm long "
                                              "(diameter printed as 0.02 mm, not entered). Other ages/mixes figure-only."})

# =====================================================================================================
# 12 Xue et al. 2025 - coral sand UHPC with steel / PE fibres (Materials 18:2233)
# =====================================================================================================
base = {"Article Name": "Experimental Study on Uniaxial Compression Stress-Strain Relationship of Hybrid Fiber-Reinforced Coral Sand Ultra-High Performance Concrete",
        "Author": "Xue X., Li W., Hou D., Han H., Han Y.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma18102233",
        "OPC / Cement": R(0.7 / 0.85), "SF (Silica fume)": R(0.15 / 0.85), "W / B": R(0.23 / 0.85), "Sea sand / B": R(1 / 0.85),
        "HGM / B (Hollow glass microsphere)": R(0.15 / 0.85), "SP / B": R(0.015 / 0.85, 5), "Sand max size (µm)": 2500,
        "Steel length (mm)": 12, "Steel diameter (µm)": 220, "Steel tensile strength (MPa)": 3000,
        "Curing method": "sealed 24 h, demoulded, standard chamber 20±2 °C, RH ≥95%", "Curing time (days)": 28, "Curing temperature (°C)": 20,
        "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
        "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
        "Source table/page": "Table 3 (mix), Sec. 3.1 text"}
p0g0 = 131.9 / 1.934
for name, vf, fc, fsp, nn in [("P0G0", 0, R(p0g0, 1), None, "VERIFY fc derived: P0G3 (131.9) is +93.4% vs P0G0 -> 131.9/1.934. "),
                              ("P0G1", 1, R(p0g0 * 1.67, 1), None, "VERIFY fc derived: P0G0 (derived) x 1.67 (+67%). "),
                              ("P0G2", 2, R(p0g0 * 1.785, 1), None, "VERIFY fc derived: P0G0 (derived) x 1.785 (+78.5%). "),
                              ("P0G3", 3, 131.9, 18.5, "")]:
    kw = {"Total fiber (vol%)": vf, "Compressive strength (MPa)": fc}
    if vf:
        kw["Steel fiber (vol%)"] = vf
    if fsp is not None:
        kw.update({"Tensile specimen": "cube 100 (splitting)", "Tensile test type": "splitting", "Tensile strength (MPa)": fsp})
    add(base, **kw, **{"Conversions / notes": f"{nn}{name}: mass ratios relative to coral sand = 1 (W 0.23, cement 0.7, SF 0.15, glass microspheres 0.15, "
                                              "water reducer 0.015, defoamer 0.0015); B = cement + SF = 0.85. Coral sand (South China Sea, <2.5 mm, FM given) entered as Sea sand/B; "
                                              "mixing water fresh (not stated as seawater). Cylinder (50x100) peak stress for P0G3 = 111.9 MPa. PE-hybrid groups only as % changes."})

# =====================================================================================================
# 13 Wang et al. 2026 - UHP shotcrete with steel slag fine aggregate replacing manufactured sand (Materials 19:2779)
# =====================================================================================================
B = 1200.0
base = {"Article Name": "Microstructural Evolution and Mechanical Response of UHPS Incorporating Steel Slag Fine Aggregate and Different Morphology Steel Fibers",
        "Author": "Wang J., Yuan Z., Zhang Y., Qian X., Qu X.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19132779",
        "OPC / Cement": 0.7, "SF (Silica fume)": 0.1, "FA (Fly ash)": 0.1, "Metakaolin": 0.1, "W / B": 0.2, "Binder content (kg/m³)": B,
        "Sand max size (µm)": 1180,
        "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2950,
        "Steel elastic modulus (GPa)": 200, "Total fiber (vol%)": 2.0,
        "Curing method": "sprayed; standard curing 24 h, demoulded, outdoor natural curing 16-28 °C, RH ~65%", "Curing time (days)": 28,
        "Curing RH (%)": 65, "Demolding age (days)": 1, "Test age (days)": 28,
        "Tensile specimen": "prism 100x100x400, 4-point, span 300", "Tensile test type": "flexural",
        "Source table/page": "Table 3 (mix), Table 4 (flexural), Sec. 3.1 text (fc)"}
wmix = {"S7": (840, 8.4, 9.6, 10.8), "S8": (960, 8.4, 9.6, 10.8), "S9": (1080, 8.4, 9.6, 10.8)}
w_t4 = {"S7G0": (13.79, 15.58, 13.81, 15.83), "S7G25": (14.24, 16.20, 14.63, 17.24), "S7G50": (14.93, 17.11, 15.05, 19.21), "S7G75": (15.45, 18.33, 15.75, 20.00),
        "S8G0": (14.76, 15.67, 14.82, 18.35), "S8G25": (14.95, 18.07, 15.64, 19.10), "S8G50": (16.60, 18.39, 17.25, 20.69), "S8G75": (17.18, 19.01, 18.59, 22.75),
        "S9G0": (15.23, 16.55, 16.60, 19.31), "S9G25": (15.05, 18.70, 16.62, 19.85), "S9G50": (17.44, 19.23, 17.17, 21.92), "S9G75": (17.60, 20.72, 18.24, 23.81)}
for g, (sfc, sfp, hfc, hfp) in w_t4.items():
    s, rep = g[:2], int(g[3:])
    tot = wmix[s][0]
    sp = {0: 8.4, 25: 8.4, 50: 9.6, 75: 10.8}[rep]
    ssfa = tot * rep / 100
    ms = tot - ssfa
    for fib, fcr, fpk in [("S", sfc, sfp), ("H", hfc, hfp)]:
        fc = 124.08 if (fib == "H" and g == "S9G75") else None
        add(base, **{"M-sand / B": R(ms / B), "SP / B": R(sp / B, 5), "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fpk,
                     "Compressive strength (MPa)": fc,
                     "Compressive specimen": "cube" if fc else None, "Compressive specimen size (mm)": "100" if fc else None,
                     "Conversions / notes": (f"{fib}-{g}: {'straight' if fib == 'S' else 'hooked-end'} copper-plated steel fibres 156 kg/m3 (2 vol% per paper). "
                                             f"kg/m3 / binder 1200 (cement 840 + SF 120 + FA 120 + MK 120). Manufactured sand {ms:.0f} + steel slag fine aggregate "
                                             f"{ssfa:.0f} kg/m3 (SSFA/B = {ssfa / B:.4f}, no column; SSFA SG 3.38, 0.15-1.18 mm). "
                                             "Tensile = 4-point flexural peak strength, first-crack = flexural initial-crack strength (Table 4). "
                                             "VERIFY test age: flexural age not stated explicitly, taken as 28 d. "
                                             + ("fc 124.08 MPa (highest cube strength, H-S9G75); uniaxial prism 113.41 MPa. " if fc else "fc figure-only (Fig. 5)."))})

# =====================================================================================================
# 14 Ahmed et al. 2026 - self-curing PP-HPFRC with brick waste sand and ceramic waste powder (Sci Rep)
# =====================================================================================================
base = {"Article Name": "Synergistic use of brick and ceramic wastes with polyethylene glycol in high-performance fiber-reinforced composites",
        "Author": "Ahmed A.S., Youssf O., Yousry Elshikh M.M., Eltawil K.A., Ghalla M., Keshta M.M.", "Year": 2026,
        "DOI / URL": "https://doi.org/10.1038/s41598-026-58428-8", "Sand max size (µm)": 4750,
        "PP fiber (vol%)": R(27.3 / 910 * 100, 2), "PP length (mm)": 12, "Total fiber (vol%)": R(27.3 / 910 * 100, 2),
        "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
        "Source table/page": "Table 3 (mix), Table 4 (results)"}
# mix: RS, BWS, OPC, GGBFS, CWP, PEG ; results: fc7, fc28, fc56, 'splitting' 28, flexural 28
amx = [("C-A", 595, 0, 644, 577, 0, 0, 40, 47, 54, 6.7, 12.80), ("C-W", 595, 0, 644, 577, 0, 0, 45, 49, 50, 6.6, 15.00),
       ("P1", 595, 0, 644, 577, 0, 4.6, 37, 50, 57, 6.0, 15.18), ("P1.5", 595, 0, 644, 577, 0, 5.44, 32, 46, 48, 6.8, 12.56),
       ("P2.0", 595, 0, 644, 577, 0, 7.25, 27, 40, 42, 6.4, 11.81),
       ("P1.5B25", 446, 137, 644, 577, 0, 5.44, 34, 49, 54, 7.2, 15.18), ("P1.5B50", 297, 273, 644, 577, 0, 5.44, 40, 49, 61, 7.7, 10.83),
       ("P1.5B75", 149, 409, 644, 577, 0, 5.44, 48, 55, 66, 6.6, 9.75), ("P1.5B100", 0, 545, 644, 577, 0, 5.44, 42, 51, 60, 7.0, 11.25),
       ("P1.5B50C10", 297, 273, 579, 520, 98, 5.44, 44, 60, 63, 7.0, 15.89), ("P1.5B50C20", 297, 273, 514, 462, 196, 5.44, 40, 58, 60, 6.2, 9.66),
       ("P1.5B50C30", 297, 273, 450, 404, 294, 5.44, 31, 44, 46, 6.5, 10.97)]
for name, rs, bws, opc, gg, cwp, peg, f7, f28, f56, ft28, fl28 in amx:
    B = opc + gg + cwp
    water = name == "C-W"
    meth = ("demoulded 24 h, water immersion at 25 °C" if water else
            "demoulded 24 h, air curing in laboratory air at 25 °C (no external water" + (", PEG internal curing)" if peg else ")"))
    for age, fc in [(7, f7), (28, f28), (56, f56)]:
        kw = {"OPC / Cement": R(opc / B), "GGBS": R(gg / B), "W / B": R(330 / B), "SP / B": R(5 / B, 5), "Binder content (kg/m³)": B,
              "Curing method": meth, "Curing time (days)": age, "Curing temperature (°C)": 25, "Curing RH (%)": 100 if water else None,
              "Test age (days)": age, "Compressive strength (MPa)": fc}
        if cwp:
            kw["Other binder"] = R(cwp / B)
        if rs:
            kw["River sand / B"] = R(rs / B)
        if age == 28:
            kw.update({"Tensile specimen": "prism 40x40x160, 3-point", "Tensile test type": "flexural", "Tensile strength (MPa)": fl28})
        add(base, **kw, **{"Conversions / notes": (f"{name}: kg/m3 / binder {B} (OPC CEM II 42.5 + GGBFS" + (" + ceramic waste powder in Other binder" if cwp else "") + "). "
                                                   + (f"Brick waste sand (crushed clay brick, SG 2.60, <4.75 mm) BWS/B = {bws / B:.4f} (no column), replacing river sand by volume. " if bws else "")
                                                   + (f"PEG (internal curing agent) {peg} kg/m3, PEG/B = {peg / B:.5f} (no column). " if peg else "")
                                                   + "PP 27.3 kg/m3 / 910 = 3.0 vol% (paper text also says '3% by weight of binder', inconsistent with 27.3/1221 = 2.2 wt%). "
                                                   + (f"28 d tensile value {ft28} MPa not entered: Table 4 labels it splitting tensile strength while Methods describe JSCE dog-bone "
                                                      "uniaxial tension (gauge 80 mm, 30x13 mm) - test type ambiguous. " if age == 28 else "")
                                                   + ("Group 3 binder < 1221 kg/m3 although paper states constant binder content; table values used." if cwp else ""))})

# ----------------------------------------------------------------------------------------------------- drop DOIs already taken by other agents
DROP = set()
for f in os.listdir(D):
    if f.endswith(".csv") and f not in ("w3_aggregate.csv", "TEMPLATE.csv"):
        try:
            DROP |= set(pd.read_csv(os.path.join(D, f), encoding="utf-8-sig", usecols=["DOI / URL"])["DOI / URL"].dropna())
        except Exception:
            pass
DROP |= set(open(os.path.join(D, "existing_papers.txt"), encoding="utf-8").read().split())
dropped = sorted({r["DOI / URL"] for r in rows if r["DOI / URL"] in DROP})
rows = [r for r in rows if r["DOI / URL"] not in DROP]
print("dropped (already in other files):", dropped)

# ----------------------------------------------------------------------------------------------------- write
df = pd.DataFrame(rows)
df = df.reindex(columns=H)
out = os.path.join(D, "w3_aggregate.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(out, df.shape, df["DOI / URL"].nunique(), "papers")
