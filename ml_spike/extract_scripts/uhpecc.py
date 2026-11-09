import csv
D = r"C:/Users/A/AppData/Local/Temp/claude/b2f7628fb08bc050/a3efc949-de1b-43db-a003-74458f673bb7/scratchpad/additions"
with open(D + "/TEMPLATE.csv", encoding="utf-8-sig") as f:
    header = next(csv.reader(f))
assert len(header) == 99, len(header)
rows = []
def r4(x): return round(x, 5)
def add(base, **kw):
    d = dict(base); d.update(kw)
    for k in d: assert k in header, k
    rows.append(d)

# ---------- A: Zhou et al. 2018 Materials ----------
B = 700 + 230 + 750
A = {"Article Name": "Mechanical Properties of Hybrid Ultra-High Performance Engineered Cementitious Composites Incorporating Steel and Polyethylene Fibers",
     "Author": "Zhou Y., Xi B., Yu K., Sui L., Xing F.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/ma11081448",
     "OPC / Cement": r4(700/B), "SF (Silica fume)": r4(230/B), "GGBS": r4(750/B),
     "W / B": r4(230/B), "SS / B (Silica sand)": r4(500/B), "HRWR / B": r4(45/B), "Binder content (kg/m³)": B,
     "PE length (mm)": 18, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
     "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2750, "Steel elastic modulus (GPa)": 200,
     "Total fiber (vol%)": 2, "Curing method": "standard curing room 23±3°C, 95% RH", "Curing time (days)": 28,
     "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "40x40x40", "Tensile specimen": "JSCE dog-bone",
     "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
nA = "Table 3 kg/m3 (OPC 700, SF 230, GGBS 750, sand 500, water 230, HRWRA 45) divided by B=1680; W/B not stated in paper (computed); fibre props Table 2 (PE density 0.97, steel 7.85 g/cm3)."
add(A, **{"PE fiber (vol%)": 2.0, "Steel fiber (vol%)": 0, "Compressive strength (MPa)": 99.5, "Tensile strength (MPa)": 15.5,
    "First-cracking strength (MPa)": 12.5, "Tensile strain capacity (%)": 9.1,
    "Source table/page": "Table 3 (mix), Sec 3.4 text (fc), Sec 3.2.2 text (ft, fcr, strain)", "Conversions / notes": nA + " Mix HUHP-ECC-2.0-0; Sec 3.2.1 says strain ~9%."})
add(A, **{"PE fiber (vol%)": 1.5, "Steel fiber (vol%)": 0.5, "Compressive strength (MPa)": 110.6, "Tensile strength (MPa)": 12.4,
    "Tensile strain capacity (%)": 8.1,
    "Source table/page": "Table 3 (mix), Sec 3.4 text (fc), Sec 3.2.1 text (ft approx 12.4), Sec 3.2.2/Conclusions (strain)", "Conversions / notes": nA + " Mix HUHP-ECC-1.5-0.5; ft given as 'approximately 12.4 MPa'. DOUBT: one sentence in 3.2.2 gives 2.2% for this mix, but 8.1% is stated twice (3.2.2 and Conclusions)."})
add(A, **{"PE fiber (vol%)": 1.0, "Steel fiber (vol%)": 1.0, "Tensile strength (MPa)": 9.9, "Tensile strain capacity (%)": 2.2,
    "Source table/page": "Table 3 (mix), Sec 3.2.2 text (ft, strain)", "Conversions / notes": nA + " Mix HUHP-ECC-1.0-1.0; fc only in Fig. 14 (left empty). DOUBT: strain 2.2% (3.2.2), another sentence gives 1.6%; 3.2.1 says ~2%."})
add(A, **{"PE fiber (vol%)": 0.5, "Steel fiber (vol%)": 1.5, "Compressive strength (MPa)": 135.5, "Tensile strength (MPa)": 11.3, "Tensile strain capacity (%)": 1.5,
    "Source table/page": "Table 3 (mix), Sec 3.4 text (fc), Sec 3.2.2 text (ft), Conclusions (strain)", "Conversions / notes": nA + " Mix HUHP-ECC-0.5-1.5; Sec 3.2.1 says strain ~2%."})
add(A, **{"PE fiber (vol%)": 0, "Steel fiber (vol%)": 2.0, "Compressive strength (MPa)": 150.5, "Tensile strength (MPa)": 8.5,
    "First-cracking strength (MPa)": 8.4, "Tensile strain capacity (%)": 0.41,
    "Source table/page": "Table 3 (mix), Sec 3.4 text (fc), Sec 3.2.2 text (ft, fcr, strain)", "Conversions / notes": nA + " Mix HUHP-ECC-0-2.0 (mono steel)."})

# ---------- B: Kim, Kim, Yoo 2018 Polymers ----------
B = 788.5 + 197.1
Kb = {"Article Name": "Hybrid Effect of Twisted Steel and Polyethylene Fibers on the Tensile Performance of Ultra-High-Performance Cementitious Composites",
      "Author": "Kim M.-J., Kim S., Yoo D.-Y.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/polym10080879",
      "OPC / Cement": r4(788.5/B), "SF (Silica fume)": r4(197.1/B), "W / B": 0.2, "SS / B (Silica sand)": r4(867.4/B),
      "Sand max size (µm)": 300, "QP / B (Quartz powder)": r4(236.6/B), "SP / B": r4(52.6/B), "Binder content (kg/m³)": round(B, 1),
      "PE diameter (µm)": 30, "PE tensile strength (MPa)": 3030, "PE elastic modulus (GPa)": 88,
      "Steel length (mm)": 30, "Steel diameter (µm)": 300, "Steel tensile strength (MPa)": 2428, "Steel elastic modulus (GPa)": 200,
      "Total fiber (vol%)": 2, "Curing method": "24 h at room (20°C, 60% RH) under plastic sheet, demould, steam 90°C for 72 h",
      "Curing time (days)": 3, "Curing temperature (°C)": 90, "Demolding age (days)": 1, "Test age (days)": 7, "Heat curing duration (h)": 72,
      "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "Φ100x200", "Tensile specimen": "dog-bone (gauge section 30x13 mm)",
      "Tensile gauge length (mm)": 80, "Tensile test type": "direct"}
nK = "Table 1 kg/m3 / B=985.6 (cement 788.5, SF 197.1, silica sand 867.4 [0.2-0.3 mm], silica flour 236.6 [10 µm], water 160.3 + 36.8 in SP); W/B=0.2 stated (incl. SP water). SP/B = liquid SP 52.6 kg/m3 (30% solids) base value; actual SP varied per mix (Table 3, grams per batch). Twisted steel fibre (T) strength 2428 MPa per Table 4 (text says 2788). PE density 0.97, steel 7.9 g/cm3."
def kim(name, st, pe, L, **kw):
    note = kw.pop("note", "")
    add(Kb, **{"Steel fiber (vol%)": st, "PE fiber (vol%)": pe, "PE length (mm)": L, **kw,
               "Conversions / notes": nK + f" Mix {name}." + (" " + note if note else "")})
kim("T2.0", 2.0, 0, None, **{"Compressive strength (MPa)": 204.4, "Tensile strength (MPa)": 15.5, "Tensile strain capacity (%)": 0.52,
    "Source table/page": "Table 1 (mix), Sec 3.1 text (fc), Sec 3.2.2 text (ft, strain)"})
kim("T1.5-LLPE0.5", 1.5, 0.5, 36, **{"Tensile strength (MPa)": 10.4, "Tensile strain capacity (%)": 0.83,
    "Source table/page": "Table 1 (mix), Sec 3.2.2 text (ft, strain)", "note": "Text attributes values to T1.5 series with 36-mm LLPE fibres; fc only in Fig. 2."})
kim("T1.0-SPE1.0", 1.0, 1.0, 12, **{"Tensile strength (MPa)": 14.3,
    "Source table/page": "Table 1 (mix), Sec 3.2.2 text (ft)", "note": "DOUBT: ft from sentence 'tensile strength decreased from 14.3 MPa to 10.5 MPa' (SPE->LLPE) in T1.0 series; strain not given individually."})
kim("T1.0-LPE1.0", 1.0, 1.0, 27, **{"Tensile strength (MPa)": 11.6, "Tensile strain capacity (%)": 0.84,
    "Source table/page": "Table 1 (mix), Sec 3.2.2 text (ft, strain)"})
kim("T1.0-LLPE1.0", 1.0, 1.0, 36, **{"Tensile strength (MPa)": 10.5, "Tensile strain capacity (%)": 1.01,
    "Source table/page": "Table 1 (mix), Sec 3.2.2 text (ft, strain)"})
kim("T0.5-SPE1.5", 0.5, 1.5, 12, **{"Compressive strength (MPa)": 139.3, "Tensile strength (MPa)": 11.9, "Tensile strain capacity (%)": 1.66,
    "Source table/page": "Table 1 (mix), Sec 3.1 text (fc), Sec 3.2.3 text (ft, strain)"})
kim("T0.5-MPE1.5", 0.5, 1.5, 18, **{"Tensile strength (MPa)": 11.5, "Tensile strain capacity (%)": 1.16,
    "Source table/page": "Table 1 (mix), Sec 3.2.3 text (ft, strain)"})
kim("SPE2.0", 0, 2.0, 12, **{"Tensile strength (MPa)": 7.8, "Tensile strain capacity (%)": 0.94,
    "Source table/page": "Table 1 (mix), Sec 3.2.3 text (ft, strain)"})
kim("MPE2.0", 0, 2.0, 18, **{"Tensile strength (MPa)": 9.7, "Tensile strain capacity (%)": 0.79,
    "Source table/page": "Table 1 (mix), Sec 3.2.3 text (ft, strain)"})
kim("LLPE2.0", 0, 2.0, 36, **{"Tensile strength (MPa)": 12.2, "Tensile strain capacity (%)": 1.35,
    "Source table/page": "Table 1 (mix), Sec 3.2.2 text (ft), Sec 3.2.4 text (strain)", "note": "ft from 'proportionally increased from 7.8 to 12.2 MPa' for SPE2.0->LLPE2.0."})

# ---------- C: Zhao et al. 2022 Materials ----------
B = 1000 + 200 + 100
Z = {"Article Name": "Mechanical Properties of Polyethylene Fiber Reinforced Ultra High Performance Concrete (UHPC)",
     "Author": "Zhao X., Cai L., Ji X., Zeng W., Liu J.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15248734",
     "OPC / Cement": r4(1000/B), "SF (Silica fume)": r4(200/B), "GGBS": r4(100/B), "W / B": r4(240/B),
     "SS / B (Silica sand)": r4(1200/B), "SP / B": r4(20/B), "Binder content (kg/m³)": B,
     "PE fiber (vol%)": 2, "Total fiber (vol%)": 2, "Curing method": "standard curing 20±2°C, RH>95%", "Curing time (days)": 28,
     "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7x70.7x70.7",
     "Tensile specimen": "dog-bone 290 mm long, 40x50 mm middle section", "Tensile test type": "direct",
     "Source table/page": "Table 3 (mix), Table 4 (fibre), Table 5 (fcr, ft, strain)"}
nZ = "Table 3 kg/m3 / B=1300 (cement 1000, SF 200, slag S105 100, silica sand 1200, SP 20, defoamer 3, water 240); W/B computed. fc only in Fig. 5 (fibred mixes ~110 MPa) -> left empty. Strain = ultimate tensile strain εtu (Table 5 mean). PE density not given."
for name, L, dmu, E, s, fcr, ft, eps in [("PA", 6, 13.5, 82, 2640, 4.75, 5.51, 0.5095), ("PB", 12, 13.5, 82, 2640, 5.71, 6.15, 0.2736),
                                          ("PC", 12, 15, 117, 3312, 4.68, 5.23, 0.6114), ("PD", 12, 27, 117, 2976, 4.69, 6.13, 0.9148),
                                          ("PF", 15, 27, 117, 2976, 5.30, 6.28, 1.1550)]:
    add(Z, **{"PE length (mm)": L, "PE diameter (µm)": dmu, "PE elastic modulus (GPa)": E, "PE tensile strength (MPa)": s,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Conversions / notes": nZ + f" Mix {name}."})

# ---------- D: Sui et al. 2018 Polymers (fatigue) ----------
B = 700 + 100 + 750 + 150
S = {"Article Name": "Flexural Fatigue Properties of Ultra-High Performance Engineered Cementitious Composites (UHP-ECC) Reinforced by Polymer Fibers",
     "Author": "Sui L., Zhong Q., Yu K., Xing F., Li P., Zhou Y.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/polym10080892",
     "OPC / Cement": r4(700/B), "Limestone powder": r4(100/B), "GGBS": r4(750/B), "SF (Silica fume)": r4(150/B),
     "W / B": r4(230/B), "SS / B (Silica sand)": r4(500/B), "HRWR / B": r4(30/B), "Binder content (kg/m³)": B,
     "PE fiber (vol%)": 2, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2,
     "Curing method": "standard curing room 20±2°C, 95% RH", "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
     "Source table/page": "Table 1 (mix), Table 3 (fibre), Sec 2.2 text (fc)"}
nS = "Table 1 kg/m3 / B=1700 (OPC 700, LP 100, GGBS 750, SF 150, quartz sand 500, HRWR 30, PE 20, water 230); W/B computed. PE aspect ratio 480, density 970 kg/m3. Direct tension (dog-bone) only summarised in abstract as 'up to 12 MPa' and '>8%' strain -> not entered (compression-only row)."
add(S, **{"Curing time (days)": 28, "Test age (days)": 28, "Compressive strength (MPa)": 102.8, "Conversions / notes": nS + " SD 1.1 MPa."})
add(S, **{"Curing time (days)": 90, "Test age (days)": 90, "Compressive strength (MPa)": 120.7, "Conversions / notes": nS + " SD 0.75 MPa."})

# ---------- E: Wang, Li, Luo 2026 Materials (wollastonite) ----------
W = {"Article Name": "Influence of Natural Wollastonite Microfibers on the Mechanical Behavior of Ultra-High-Toughness Cementitious Composites Containing Polyethylene Fibers",
     "Author": "Wang S., Li G., Luo F.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19091717",
     "W / B": 0.25, "SS / B (Silica sand)": r4(250/750), "Sand max size (µm)": 400, "SP / B": 0.005,
     "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0,
     "Curing method": "standard curing 20±2°C, RH>95%", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
     "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 50, "Tensile test type": "direct",
     "Source table/page": "Table 2 (mix), Table 3 (fcr, ft, strain)"}
nW = "Table 2 batch masses in g; B = cement + wollastonite = 750 g (wollastonite replaces cement by mass, entered as 'Other binder'). Water 187.5 g, sand 250 g, SP 3.75 g (solid PCE), PE 10.3 g (2.0 vol% stated). fc reported only as % change vs reference (absolute value not given) -> empty."
for name, w, fcr, ft, eps in [("WS-0", 0, 6.4, 8.4, 3.3), ("WS-C-2", 15, 6.3, 8.7, 4.9), ("WS-C-4", 30, 6.4, 9.2, 5.1), ("WS-C-6", 45, 6.2, 9.5, 5.7),
                               ("WS-C-8", 60, 5.8, 9.1, 4.2), ("WS-C-10", 75, 5.5, 8.6, 4.3), ("WS-F-2", 15, 6.6, 8.9, 3.8), ("WS-F-4", 30, 6.8, 9.4, 4.2),
                               ("WS-F-6", 45, 6.7, 9.9, 4.6), ("WS-F-8", 60, 6.5, 10.0, 5.5), ("WS-F-10", 75, 5.8, 9.1, 4.6)]:
    kind = "" if w == 0 else (" coarse wollastonite CW (d 8-10 µm, L/D 5-10)" if "-C-" in name else " fine wollastonite FW (d 4-6 µm, L/D 20-30)")
    add(W, **{"OPC / Cement": r4((750-w)/750), "Other binder": r4(w/750), "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps, "Conversions / notes": nW + f" Mix {name}." + kind})

# ---------- F: Zhang et al. 2026 Polymers (FAC) ----------
B = 718 + 575 + 115
F = {"Article Name": "Crack-Width Threshold-Guided Design of Self-Healing Polyethylene Fiber-Reinforced Engineered Cementitious Composites (ECCs)",
     "Author": "Zhang Z., Lei X., Abdalla J.A., Hawileh R.A., Shen Q., Chen Y.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/polym18192345",
     "OPC / Cement": r4(718/B), "FA (Fly ash)": r4(575/B), "SF (Silica fume)": r4(115/B), "W / B": r4(338/B), "SP / B": r4(18/B),
     "Binder content (kg/m³)": B, "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 26, "PE tensile strength (MPa)": 3000,
     "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2, "Curing method": "air 25±3°C, 65±10% RH", "Curing temperature (°C)": 25,
     "Curing RH (%)": 65, "Demolding age (days)": 1, "Curing time (days)": 28, "Test age (days)": 28, "Tensile specimen": "dumbbell",
     "Tensile test type": "direct", "Source table/page": "Table 2 (mix), Sec 3 text / Fig. 9 discussion (ft, strain)"}
nF = "Table 2 kg/m3 / B=1408. DOUBT: text states W/B=0.2 and S/B=0.3, but Table 2 water 338 gives 0.240 (entered); SP 18 kg/m3. Compressive strength not reported. Text gives 'matrix cracking strength' 5.82/4.53 MPa - not entered as composite first-crack strength. Not UHP (moderate-strength PE-ECC)."
add(F, **{"SS / B (Silica sand)": r4(442/B), "Tensile strength (MPa)": 7.88, "Tensile strain capacity (%)": 2.75, "Conversions / notes": nF + " Mix Ref.-ECC."})
add(F, **{"SS / B (Silica sand)": r4(282/B), "FA cenosphere / B": r4(36/B), "Tensile strength (MPa)": 7.42, "Tensile strain capacity (%)": 7.14,
          "Conversions / notes": nF + " Mix FAC-ECC (20 vol% of silica sand replaced by fly-ash cenospheres, 36 kg/m3)."})

# ---------- G: Gong et al. 2020 Materials (HS-SHCC reference) ----------
B = 1460 + 292
add({}, **{"Article Name": "Tensile Behavior of High-Strength, Strain-Hardening Cement-Based Composites (HS-SHCC) Reinforced with Continuous Textile Made of Ultra-High-Molecular-Weight Polyethylene",
    "Author": "Gong T., Curosu I., Liebold F., Vo D.M.P., Zierold K., Maas H.-G., Cherif C., Mechtcherine V.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13245628",
    "OPC / Cement": r4(1460/B), "SF (Silica fume)": r4(292/B), "W / B": 0.18, "SS / B (Silica sand)": r4(145/B), "Sand max size (µm)": 200,
    "SP / B": r4(45/B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2, "PE length (mm)": 6, "Total fiber (vol%)": 2,
    "Curing method": "demoulded at 24 h, sealed in plastic, 20°C / 65% RH for 27 d", "Curing time (days)": 27, "Curing temperature (°C)": 20,
    "Curing RH (%)": 65, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "plate 700 mm long, 60x20 mm section",
    "Tensile gauge length (mm)": 150, "Tensile test type": "direct", "Tensile strength (MPa)": 6.7, "First-cracking strength (MPa)": 2.7,
    "Tensile strain capacity (%)": 1.4, "Source table/page": "Table 2 (mix), Table 5 (fcr, ft, strain; plain SHCC without textile)",
    "Conversions / notes": "Table 2 kg/m3 / B=1752 (CEM I 52.5R 1460, SF 292, quartz sand 0.06-0.2 mm 145, SP 45, water 315, UHMWPE SK62 20 kg/m3 = 2 vol%); W/B 0.18 stated. Only the short-fibre reference SHCC row (textile-reinforced composites excluded). Test age taken as 28 d (1 d + 27 d storage). fc not measured in this paper (cites ~140 MPa at 14 d from earlier work) -> empty. PE fibre strength/modulus not given."})

# ---------- H: Ai et al. 2025 Materials ----------
B = 824 + 357 + 51
H = {"Article Name": "Research on the Effects of the Water-Binder Ratio and Fiber Content on the Tensile and Bending Mechanical Properties of ECCs",
     "Author": "Ai J., Qiu K., Yang B., Peng S., Zhang Q., Jiang J.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma18030509",
     "OPC / Cement": r4(824/B), "FA (Fly ash)": r4(357/B), "SF (Silica fume)": r4(51/B), "SS / B (Silica sand)": r4(703/B), "SP / B": 0.001,
     "Binder content (kg/m³)": B, "PE length (mm)": 18, "PE diameter (µm)": 25, "PE elastic modulus (GPa)": 116,
     "Curing method": "standard curing 20±2°C, RH>=96%", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 96,
     "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": "direct",
     "Source table/page": "Table 7 (mix), Table 2 (fibre), Table 9 (ft)"}
nH = "Table 7 kg/m3 / B=1232 (cement 824, FA 357, SF 51, quartz sand 703); W/B as designed (water 234/271/308). SP 0.1% of binder (text). PE density 0.97. Strain values in text could not be unambiguously assigned to mixes -> empty; fc not reported. Not UHP (moderate-strength PE-ECC)."
for wb, pe, ft in [(0.19, 1, 6.23), (0.19, 1.5, 6.54), (0.19, 2, 5.92), (0.22, 1, 6.54), (0.22, 1.5, 7.87), (0.22, 2, 7.30),
                   (0.25, 1, 5.24), (0.25, 1.5, 6.57), (0.25, 2, 6.34)]:
    add(H, **{"W / B": wb, "PE fiber (vol%)": pe, "Total fiber (vol%)": pe, "Tensile strength (MPa)": ft,
              "Conversions / notes": nH + f" Mix P{pe}W{wb}."})

# ---------- I: Park et al. 2022 Materials ----------
P = {"Article Name": "Comparison of Mechanical and Crack-Healing Properties of PE-PVA Hybrid Fiber-Reinforced SHCCs in Natural and Underwater Conditions",
     "Author": "Park S.-E., Nguyen H.H., Choi J.-I., Lee B.Y., Kim Y.Y.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15186339",
     "OPC / Cement": 0.5, "GGBS": 0.5, "W / B": 0.4, "Crumb rubber / B": 0.1, "SS / B (Silica sand)": 0.5, "SP / B": 0.002, "VMA / B": 0.001,
     "PE fiber (vol%)": 1.25, "PE length (mm)": 12, "PE diameter (µm)": 16, "PE tensile strength (MPa)": 2700, "PE elastic modulus (GPa)": 88,
     "PVA fiber (vol%)": 0.1, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41,
     "Total fiber (vol%)": 1.35, "Demolding age (days)": 2, "Test age (days)": 28, "Compressive specimen": "cube",
     "Compressive specimen size (mm)": "50x50x50", "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 80, "Tensile test type": "direct",
     "Source table/page": "Table 3 (mix), Table 2 (fibre), Table 5 (fcr, ft, strain)"}
nP = "Table 3 given as mass ratios to binder (cement Type I + GGBS); expansive agent EA/B=0.05 and defoamer 0.001 not in binder (no column). CR = 40-mesh crumb rubber powder. fc only in Fig. 3 (M-O 10% lower than M-W) -> empty. Not UHP (W/B 0.4)."
add(P, **{"Curing method": "2 d at 23±3°C in mould, then underwater curing to 28 d", "Curing time (days)": 26, "Curing temperature (°C)": 23,
          "First-cracking strength (MPa)": 3.74, "Tensile strength (MPa)": 7.93, "Tensile strain capacity (%)": 8.00,
          "Conversions / notes": nP + " Mix M-W (underwater)."})
add(P, **{"Curing method": "2 d at 23±3°C in mould, then natural outdoor exposure (Gwangju; avg 28.5°C, 75.2% RH, 8 rain days) to 28 d",
          "Curing time (days)": 26, "Curing temperature (°C)": 28.5, "Curing RH (%)": 75.2,
          "First-cracking strength (MPa)": 3.13, "Tensile strength (MPa)": 7.60, "Tensile strain capacity (%)": 7.74,
          "Conversions / notes": nP + " Mix M-O (natural outdoor)."})

# binder sum check
bcols = header[4:22]
for d in rows:
    s = sum(float(d.get(c) or 0) for c in bcols)
    assert abs(s - 1) < 0.002, (d["Article Name"], s)
with open(D + "/uhpecc.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader()
    for d in rows:
        w.writerow({k: ("" if v is None else v) for k, v in d.items()})
print(len(rows), "rows;", len({d['DOI / URL'] for d in rows}), "papers")
print(bcols)
