import csv, collections
D = r"C:/Users/A/AppData/Local/Temp/claude/b2f7628fb08bc050/a3efc949-de1b-43db-a003-74458f673bb7/scratchpad/additions/"
hdr = next(csv.reader(open(D + "TEMPLATE.csv", encoding="utf-8-sig")))
rows = []
FIBS = ['PE fiber (vol%)', 'PVA fiber (vol%)', 'Steel fiber (vol%)', 'PP fiber (vol%)']


def add(base, **kw):
    r = dict(base); r.update(kw)
    for k in r:
        assert k in hdr, k
    pv = sum(float(r.get(k) or 0) for k in FIBS)
    if pv and 'Total fiber (vol%)' not in kw:
        r['Total fiber (vol%)'] = round(pv, 3)
    rows.append(r)


def R(x, n=4):
    return round(x, n)


# ---------- P1 Zhou 2024 Polymers ----------
P = {'Article Name': 'Mechanical Properties and Stress–Strain Relationship of PVA-Fiber-Reinforced Engineered Geopolymer Composite',
     'Author': 'Jian Zhou, Zhenjun Li, Xi Liu, Xinzhuo Yang, Jiaojiao Lv', 'Year': 2024, 'DOI / URL': 'https://doi.org/10.3390/polym16121685',
     'Activator modulus Ms (SiO2/Na2O)': 1.6, 'Sand max size (µm)': 200, 'PVA length (mm)': 12,
     'Curing method': '24 h in mould under plastic film; demould; 24 h at 60 °C; then 20±2 °C, 95±2% RH until test',
     'Curing temperature (°C)': 20, 'Curing RH (%)': 95, 'Demolding age (days)': 1, 'Heat curing duration (h)': 24,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '70.7x70.7x70.7', 'Tensile specimen': 'dog-bone (dims in Fig. 3)', 'Tensile gauge length (mm)': 80}
z = [('CG', 923.2, 230.8, 403.9, 86.5, 432.7, 'K', 76.53, 74.98, 72.37, (2.670, 3.732, 4.574)),
     ('S/B-0.3', 943.6, 235.9, 353.9, 88.5, 442.3, 'K', 74.92, 70.59, 68.12, (2.249, 3.409, 4.190)),
     ('S/B-0.4', 903.6, 225.9, 451.8, 84.7, 423.5, 'K', 79.08, 76.08, 73.29, (2.579, 3.652, 4.008)),
     ('W/B-0.28', 945.0, 236.2, 413.4, 65.0, 443.0, 'K', 86.50, 82.86, 80.95, (2.934, 3.554, 3.736)),
     ('W/B-0.32', 902.3, 225.6, 394.8, 107.2, 423.0, 'K', 71.57, 67.80, 66.71, (2.375, 3.826, 5.929)),
     ('EGC-G', 923.2, 230.8, 403.9, 86.5, 432.7, 'G', 80.91, 72.81, 67.98, (2.096, 3.501, 2.724))]
for mid, fa, gg, qs, w, act, ft, f28, f7, f3, (fcr, ftu, eps) in z:
    B = fa + gg
    if ft == 'K':
        fib = {'PVA diameter (µm)': 39, 'PVA tensile strength (MPa)': 1620, 'PVA elastic modulus (GPa)': 42.8}
    else:
        fib = {'PVA diameter (µm)': 38, 'PVA tensile strength (MPa)': 1600, 'PVA elastic modulus (GPa)': 40}
    base = dict(P, **fib, **{'FA (Fly ash)': R(fa / B), 'GGBS': R(gg / B), 'SS / B (Silica sand)': R(qs / B),
                             'W / B': R((w + 0.6 * act) / B, 3), 'Extra water / B': R(w / B), 'Binder content (kg/m³)': round(B, 1)})
    note = (f"Mix {mid}. Table 4 kg/m3: FA {fa}, GGBS {gg}, quartz sand {qs} (100–200 µm), water {w}, alkali activator {act}, PVA 26.0 kg/m3 "
            f"({'Kuraray REC15' if ft == 'K' else 'Yingjia domestic'}). Ratios = kg/m3 ÷ B (FA+GGBS={B:.1f}). Activator = Na2SiO3 (Ms 2.8) and NaOH flakes each "
            f"dissolved to 40 wt% and blended to Ms 1.6; activator solution/B = {act / B:.4f}; WG/NaOH split and NaOH molarity not reported (columns blank). "
            f"W/B AI-derived = (water + 0.6×activator)/B; matches the paper's nominal W/B label. PVA vol% blank: paper gives only 26.0 kg/m3 and no fibre density "
            f"(VERIFY: ≈2 vol% if density 1.3). Quartz sand entered in SS/B.")
    for age, fc in [(3, f3), (7, f7), (28, f28)]:
        add(base, **{'Test age (days)': age, 'Compressive strength (MPa)': fc,
                     'Source table/page': 'Table 4 (mix), Table 2 (fibre), Table 6 (fc)', 'Conversions / notes': note})
    add(base, **{'Tensile test type': 'direct', 'Tensile strength (MPa)': ftu, 'First-cracking strength (MPa)': fcr, 'Tensile strain capacity (%)': eps,
                 'Source table/page': 'Table 4 (mix), Table 8 (uniaxial tension)',
                 'Conversions / notes': note + ' Tensile test age NOT stated in paper (left blank); fc given on separate rows.'})

# ---------- P2 Hossain & Sood 2023 ----------
P = {'Article Name': 'The Strength and Fracture Characteristics of One-Part Strain-Hardening Green Alkali-Activated Engineered Composites',
     'Author': 'Khandaker M. Anwar Hossain, Dhruv Sood', 'Year': 2023, 'DOI / URL': 'https://doi.org/10.3390/ma16145077',
     'PVA fiber (vol%)': 2, 'PVA length (mm)': 8, 'PVA diameter (µm)': 38, 'PVA tensile strength (MPa)': 1610, 'PVA elastic modulus (GPa)': 41,
     'Curing method': 'demoulded at 24 h, then 23±3 °C and 95±5% RH', 'Curing temperature (°C)': 23, 'Curing RH (%)': 95, 'Demolding age (days)': 1,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '50x50x50',
     'Tensile specimen': 'dog-bone 300 mm long, 100x25x25 mm control region', 'Tensile gauge length (mm)': 50.8}
mixes = [('CSM1-F', 0.55, 0, 0.45, 1, (46.5, 52.0, 49.8), (1.2, 3.8, 2.4), (4.0, 7.0, 2.6)),
         ('CSM1N-F', 0.50, 0, 0.50, 1, (34.1, 47.0, 48.6), (4.8, 4.9, 3.2), (5.9, 6.0, 3.0)),
         ('CFSM1-F', 0.25, 0.35, 0.40, 1, (44.3, 45.2, 47.0), (1.0, 3.6, 2.5), (4.0, 5.0, 3.2)),
         ('CFSM1N-F', 0.25, 0.25, 0.50, 1, (36.5, 39.1, 41.2), (5.8, 6.5, 3.7), (4.3, 5.4, 2.5)),
         ('CSM2-F', 0.55, 0, 0.45, 2, (41.2, 56.8, 55.8), (2.1, 5.0, 3.7), (4.5, 6.4, 2.9)),
         ('CSM2N-F', 0.50, 0, 0.50, 2, (40.8, 48.0, 47.8), (6.7, 7.5, 2.8), (4.2, 5.9, 2.7)),
         ('CFSM2-F', 0.25, 0.35, 0.40, 2, (42.0, 46.4, 45.6), (2.1, 3.0, 2.5), (4.3, 6.0, 2.8)),
         ('CFSM2N-F', 0.25, 0.25, 0.50, 2, (39.2, 45.5, 46.2), (4.2, 4.7, 3.2), (3.6, 4.8, 3.0))]
for mid, fac, faf, gg, rt, (c28, c56, c365), t28, t365 in mixes:
    if rt == 1:
        act = {'Ca(OH)2 / B': R(0.09 / 3.5, 5), 'SSM / B (Na2SiO3 anhydrous)': R(0.09 * 2.5 / 3.5 * 122.06 / 212.14, 5), 'W / B': 0.35}
        an = ("Reagent 1 = Ca(OH)2 : Na2SiO3·5H2O = 1:2.5 (powders), reagent/B = 0.09 (Table 1a). AI-derived: Ca(OH)2/B = 0.09/3.5 = 0.0257; "
              "Na2SiO3·5H2O/B = 0.0643 → anhydrous Na2SiO3/B = 0.0643×122.06/212.14 = 0.0370.")
    else:
        act = {'Ca(OH)2 / B': R(0.12 * 2.5 / 3.5, 5), 'Na2SO4 / B': R(0.12 / 3.5, 5), 'W / B': 0.375}
        an = "Reagent 2 = Ca(OH)2 : Na2SO4 = 2.5:1 (powders), reagent/B = 0.12 (Table 1a). AI-derived: Ca(OH)2/B = 0.0857; Na2SO4/B = 0.0343."
    base = dict(P, **act, **{'FA (Fly ash)': R(fac + faf, 3), 'GGBS': gg, 'SS / B (Silica sand)': 0.3, 'HRWR / B': 0.02})
    note = (f"Mix {mid} (one-part AAEC). B = FA-C + FA-F + GGBFS (=1; FA column = Class C FA {fac} + Class F FA {faf}). " + an +
            " Reagent not counted in B. Table 1a values are mass ratios of binder.")
    add(base, **{'Test age (days)': 28, 'Compressive strength (MPa)': c28, 'Tensile test type': 'direct', 'First-cracking strength (MPa)': t28[0],
                 'Tensile strength (MPa)': t28[1], 'Tensile strain capacity (%)': t28[2],
                 'Source table/page': 'Table 1a (mix), Table 3 (fc composite), Table 6 (tension 28 d)', 'Conversions / notes': note})
    add(base, **{'Test age (days)': 56, 'Compressive strength (MPa)': c56,
                 'Source table/page': 'Table 1a (mix), Table 3 (fc composite 56 d)', 'Conversions / notes': note})
    add(base, **{'Test age (days)': 365, 'Compressive strength (MPa)': c365, 'Tensile test type': 'direct', 'First-cracking strength (MPa)': t365[0],
                 'Tensile strength (MPa)': t365[1], 'Tensile strain capacity (%)': t365[2],
                 'Source table/page': 'Table 1a (mix), Table 3 (fc 365 d), Table 6 (tension 365 d)', 'Conversions / notes': note})
base = dict(P, **{'OPC / Cement': 0.45, 'FA (Fly ash)': 0.55, 'SS / B (Silica sand)': 0.36, 'W / B': 0.27, 'HRWR / B': 0.006})
note = "Control ECC (FP_CM/ECC): cement + Class F fly ash, no activator. Sand 0.36 as printed in Table 1a."
add(base, **{'Test age (days)': 28, 'Compressive strength (MPa)': 52.5, 'Tensile test type': 'direct', 'First-cracking strength (MPa)': 4.5,
             'Tensile strength (MPa)': 5.7, 'Tensile strain capacity (%)': 2.3, 'Source table/page': 'Table 1a, Table 3, Table 6', 'Conversions / notes': note})
add(base, **{'Test age (days)': 56, 'Compressive strength (MPa)': 56.2, 'Source table/page': 'Table 1a, Table 3', 'Conversions / notes': note})
add(base, **{'Test age (days)': 365, 'Compressive strength (MPa)': 60.4, 'Tensile test type': 'direct', 'First-cracking strength (MPa)': 4.4,
             'Tensile strength (MPa)': 7.4, 'Tensile strain capacity (%)': 3.0, 'Source table/page': 'Table 1a, Table 3, Table 6', 'Conversions / notes': note})

# ---------- P3 Wang 2023 ----------
P = {'Article Name': 'Bonding Properties between Fly Ash/Slag-Based Engineering Geopolymer Composites and Concrete',
     'Author': 'Baogui Wang, Hu Feng, Hao Huang, Aofei Guo, Yiming Zheng, Yang Wang', 'Year': 2023, 'DOI / URL': 'https://doi.org/10.3390/ma16124232',
     'Activator modulus Ms (SiO2/Na2O)': 1.4, 'W / B': 0.32,
     'Curing method': 'demoulded after 1 d indoors; 20±1 °C, 90±5% RH', 'Curing temperature (°C)': 20, 'Curing RH (%)': 90, 'Demolding age (days)': 1,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '50x50x50', 'Tensile specimen': 'dog-bone (dims in Fig. 3)', 'Tensile gauge length (mm)': 80}
PVA = {'PVA fiber (vol%)': 2, 'PVA length (mm)': 12, 'PVA diameter (µm)': 40, 'PVA tensile strength (MPa)': 1560, 'PVA elastic modulus (GPa)': 41}
PE = {'PE fiber (vol%)': 2, 'PE length (mm)': 12, 'PE diameter (µm)': 24, 'PE tensile strength (MPa)': 3000, 'PE elastic modulus (GPa)': 110}
an = ("Activator = NaOH (99%) + sodium silicate solution (SiO2 27.7%, Na2O 8.8%, H2O 63.5%), NaOH:silicate mass ratio 0.15, Ms 1.4; paper states "
      "'mass ratio of activator to binder (FA+GGBS) was 4%' (basis unclear; not entered in WG/NaOH columns). W/B 0.32 as in Table 3 "
      "(unclear whether silicate-solution water is included). No sand.")
for fa, (s8, e8), (s28, e28), fc in [(0, (4.30, 1.8), (3.65, 1.7), {8: 75, 28: 89}), (0.2, (4.17, 2.5), (4.34, 1.6), {}),
                                      (0.4, (3.55, 2.7), (3.34, 1.3), {}), (0.6, (3.50, 1.7), (4.01, 0.6), {})]:
    base = dict(P, **PVA, **{'FA (Fly ash)': fa, 'GGBS': R(1 - fa, 2)})
    mid = f"FA{int(fa * 100)}%-W0.32-PVA"
    for age, s, e in [(8, s8, e8), (28, s28, e28)]:
        add(base, **{'Test age (days)': age, 'Curing time (days)': age, 'Compressive strength (MPa)': fc.get(age, ''), 'Tensile test type': 'direct',
                     'Tensile strength (MPa)': s, 'Tensile strain capacity (%)': e,
                     'Source table/page': 'Table 3 (mix); Section 3 text (uniaxial tension values' + ('; fc text)' if fc else ')'),
                     'Conversions / notes': f"Mix {mid}. " + an + ("" if fc else " fc for this mix only in Fig. 6 (not entered).")})
add(dict(P, **PE, **{'FA (Fly ash)': 0.2, 'GGBS': 0.8}),
    **{'Test age (days)': 28, 'Curing time (days)': 28, 'Compressive strength (MPa)': 79, 'Source table/page': 'Table 3 (mix); Section 3.1 text (fc)',
       'Conversions / notes': "Mix FA20%-W0.32-PE. " + an + " PE tensile values reported only as % differences / figures (not entered)."})

# ---------- P4 Luo 2024 ----------
B = 924 + 280 + 76.0
P = {'Article Name': 'Study on High-Ductility Geopolymer Concrete: The Influence of Oven Heat Curing Conditions on Mechanical Properties and Microstructural Development',
     'Author': 'Ruihao Luo, Runan Liu, Guang Qin, Minyang Jiang, Yixian Wu, Yongchang Guo', 'Year': 2024, 'DOI / URL': 'https://doi.org/10.3390/ma17164011',
     'GGBS': R(924 / B, 5), 'FA (Fly ash)': R(280 / B, 5), 'SF (Silica fume)': R(76 / B, 5), 'WG / B (Water glass)': R(439 / B), 'NaOH / B': R(105 / B),
     'Activator modulus Ms (SiO2/Na2O)': 1.5, 'NaOH molarity (M)': 14, 'Extra water / B': R(78.8 / B), 'SS / B (Silica sand)': R(453 / B),
     'Sand max size (µm)': 400, 'Binder content (kg/m³)': B,
     'PE fiber (vol%)': 2, 'PE diameter (µm)': 20, 'PE tensile strength (MPa)': 3000, 'PE elastic modulus (GPa)': 110,
     'Compressive specimen': 'cylinder', 'Compressive specimen size (mm)': '50x100', 'Tensile specimen': 'dumbbell (JC/T 2461-2018)', 'Tensile gauge length (mm)': 80,
     'Tensile test type': 'direct'}
note0 = ("Table 3 kg/m3: GGBS 924, FA 280, SF 76.0, medium sand MS (0.15–0.40 mm) 68.0, fine sand FS (0.076–0.15 mm) 385, NaOH solution (14 M) 105, "
         "sodium silicate solution 439 (Ms 2.25; blended activator Ms 1.5), extra water 78.8, PE 21.9, BaCl2 12.7 (retarder, BaCl2/B = 0.0099). "
         f"B = GGBS+FA+SF = {B:.0f}; ratios = kg/m3 ÷ B. NaOH/B and WG/B are SOLUTION masses. SS/B = (MS+FS)/B (quartz sands). PE strength '>3000' and "
         "modulus '>110' entered as 3000/110; PE length not stated (6/12/18 mm available). Tension = 'axial tensile' dumbbell test. ")
for name, age, fc, (a, b, c) in [('D-7', 7, 49.9, (3.88, 7.19, 6.34)), ('D-28', 28, 78.5, (3.77, 7.64, 9.27))]:
    add(P, **{'Curing method': 'sealed indoor curing at room temperature (20±3 °C)', 'Curing temperature (°C)': 20, 'Curing time (days)': age, 'Test age (days)': age,
              'Compressive strength (MPa)': fc, 'First-cracking strength (MPa)': a, 'Tensile strength (MPa)': b, 'Tensile strain capacity (%)': c,
              'Source table/page': 'Table 3 (mix), Table 4 (fc), Table 5 (tension)', 'Conversions / notes': note0 + f"Group {name}."})
fc28 = {('45', 1): 60.4, ('45', 3): 75.9, ('45', 5): 104, ('45', 7): 97.8, ('60', 1): 62.5, ('60', 3): 60.2, ('60', 5): 65.2, ('60', 7): 56.4}
fc7 = {('45', 5): 67.7, ('60', 3): 91.979}
ten = {'T45-1-7': (4.08, 6.23, 8.24), 'T45-3-7': (4.17, 9.19, 8.48), 'T45-5-7': (4.17, 9.21, 9.74), 'T45-7-7': (3.71, 7.25, 4.71),
       'T60-1-7': (3.35, 8.09, 8.22), 'T60-3-7': (4.17, 10.0, 9.25), 'T60-5-7': (6.16, 9.06, 9.38), 'T60-7-7': (3.91, 9.29, 8.85),
       'T45-1-28': (4.87, 9.99, 7.54), 'T45-3-28': (5.40, 6.67, 5.62), 'T45-5-28': (2.54, 8.60, 8.45), 'T45-7-28': (3.61, 10.8, 7.76),
       'T60-1-28': (4.63, 7.25, 5.41), 'T60-3-28': (3.99, 7.28, 8.21), 'T60-5-28': (5.86, 9.10, 7.44), 'T60-7-28': (5.78, 10.7, 7.88)}
for t in ['45', '60']:
    for x in [1, 3, 5, 7]:
        for age in [7, 28]:
            nm = f"T{t}-{x}-{age}"
            a, b, c = ten[nm]
            fc = fc28.get((t, x)) if age == 28 else fc7.get((t, x), '')
            extra = ''
            if nm == 'T45-5-28':
                extra = ' Text quotes 103 MPa vs Table 4 104 MPa (table used).'
            if nm == 'T60-3-28':
                extra = ' Text quotes 60.1 MPa vs Table 4 60.2 MPa (table used).'
            add(P, **{'Curing method': f'drying-oven curing at {t} °C for {x} d, then indoor room-temperature curing to test age',
                      'Curing temperature (°C)': int(t), 'Heat curing duration (h)': x * 24, 'Curing time (days)': age, 'Test age (days)': age,
                      'Compressive strength (MPa)': fc, 'First-cracking strength (MPa)': a, 'Tensile strength (MPa)': b, 'Tensile strain capacity (%)': c,
                      'Source table/page': 'Table 3 (mix), Table 4 (fc), Table 5 (tension)', 'Conversions / notes': note0 + f"Group {nm}." + extra})

# ---------- P5 Guo 2024 ----------
B = 849.7 + 364.1
P = {'Article Name': 'Evaluation of Axial Compressive and Tensile Properties of PE/PVA Hybrid Fiber Reinforced Strain-Hardening Geopolymer Composites',
     'Author': 'Jingen Guo, Ji Shi, Liuhuo Wang, Chengyong Huang, Xiongwu Tao, Chaosen Li, Zhanbiao Chen', 'Year': 2024, 'DOI / URL': 'https://doi.org/10.3390/ma17174356',
     'GGBS': R(849.7 / B), 'FA (Fly ash)': R(364.1 / B), 'SS / B (Silica sand)': R(242.8 / B), 'Extra water / B': R(72.8 / B), 'NaOH molarity (M)': 10,
     'Binder content (kg/m³)': round(B, 1),
     'PE length (mm)': 12, 'PE diameter (µm)': 20, 'PE tensile strength (MPa)': 2500, 'PE elastic modulus (GPa)': 120,
     'PVA length (mm)': 12, 'PVA diameter (µm)': 15, 'PVA tensile strength (MPa)': 1830, 'PVA elastic modulus (GPa)': 40,
     'Curing method': '24 h room temperature under plastic film, then water-tank curing 28 d', 'Curing time (days)': 28, 'Demolding age (days)': 1,
     'Compressive specimen': 'cylinder (dims in Fig. 3)', 'Tensile specimen': 'dumbbell (JSCE 2008; dims in Fig. 3)', 'Tensile gauge length (mm)': 80,
     'Tensile test type': 'direct'}
note0 = ("Table 3 kg/m3: GGBS 849.7, FA 364.1, quartz sand 242.8, alkali activator 242.8 (activator solution/B = 0.20), water 72.8, BaCl2 12.1 (retarder, /B = 0.01). "
         "Activator = 10 M NaOH solution + sodium silicate (Ms 2.25, SiO2:Na2O:H2O 29.99:13.75:56.26); WG:NaOH split not reported. Quartz sand entered in SS/B. "
         "Test age not explicitly stated (tested after 28 d water curing; left blank). VERIFY: the same group's Ling et al. 2024 (10.3390/ma17153778) reports "
         "identical fc/tension results for these mixes with FA:GGBS = 7:3 and activator/B = 0.40, so GGBS/FA (and activator) in this table may be swapped/misprinted; "
         "values entered as printed here.")
for mid, pe, pva, fc, (a, b, c) in [('U1.0-P0.0', 1.0, 0, 93.9, (2.50, 4.92, 4.74)), ('U1.5-P0.0', 1.5, 0, 87.0, (2.47, 5.74, 6.16)),
                                     ('U2.0-P0.0', 2.0, 0, 77.1, (2.98, 6.26, 6.07)), ('U1.5-P0.5', 1.5, 0.5, 83.2, (3.46, 7.04, 4.70)),
                                     ('U1.0-P1.0', 1.0, 1.0, 84.7, (4.30, 5.64, 3.80)), ('U0.5-P1.5', 0.5, 1.5, 87.0, (3.74, 4.19, 0.80)),
                                     ('U0.0-P2.0', 0, 2.0, 93.4, (3.10, 3.10, 0.52))]:
    add(P, **{'PE fiber (vol%)': pe, 'PVA fiber (vol%)': pva, 'Compressive strength (MPa)': fc, 'First-cracking strength (MPa)': a,
              'Tensile strength (MPa)': b, 'Tensile strain capacity (%)': c,
              'Source table/page': 'Table 3 (mix), Table 2 (fibres), Table 4 (fc), Table 5 (tension)', 'Conversions / notes': f"Mix {mid}. " + note0})

# ---------- P6 Xu 2026 red mud ----------
P = {'Article Name': 'A Study on the Mechanical Properties of Engineered Geopolymer Composites Based on Red Mud, Fly Ash, and Slag',
     'Author': 'Shuo Xu, Yu Ling, Xin Luo, Jingyuan Wang, Yicong Zhong, Gai Chen', 'Year': 2026, 'DOI / URL': 'https://doi.org/10.3390/polym18182271',
     'WG / B (Water glass)': R(485.52 * 2 / 3 / 1213.8), 'NaOH / B': R(485.52 / 3 / 1213.8), 'Na2O / B': 0.068, 'Activator modulus Ms (SiO2/Na2O)': 1.2,
     'NaOH molarity (M)': 10, 'W / B': 0.32, 'Extra water / B': R(93.4 / 1213.8), 'SS / B (Silica sand)': 0.2, 'Binder content (kg/m³)': 1213.8,
     'PE fiber (vol%)': 2, 'PE length (mm)': 12, 'PE diameter (µm)': 24, 'PE tensile strength (MPa)': 3000, 'PE elastic modulus (GPa)': 120,
     'Curing method': 'sealed 24 h, demoulded, standard curing room 20±2 °C, ≥90% RH', 'Curing time (days)': 28, 'Curing temperature (°C)': 20,
     'Curing RH (%)': 90, 'Demolding age (days)': 1, 'Test age (days)': 28,
     'Compressive specimen': 'cylinder', 'Compressive specimen size (mm)': '50x100', 'Tensile specimen': 'dog-bone (JSCE; dims in Fig. 4b)',
     'Tensile gauge length (mm)': 80, 'Tensile test type': 'direct'}
note0 = ("B = GGBS+FA+RM (red mud, entered as Other binder) = 1213.8 kg/m3. Table 2 kg/m3: quartz sand 242.76, activator 485.52 (10 M NaOH solution : water glass "
         "= 1:2 by mass; water glass Ms 2.25, Na2O 13.75%, SiO2 29.99%; final Ms 1.2), water 93.40, BaCl2 12.14 (retarder, 1%), PE 19.40. AI-derived: "
         "WG/B = 485.52×2/3/1213.8, NaOH/B = 485.52/3/1213.8 (SOLUTION masses). W/B 0.32 and alkali content 6.8% (Na2O/B) as stated in text. Quartz sand in SS/B.")
for mid, g, f, r, fc, (a, b, c) in [('G50F50R0', 606.90, 606.90, 0, 111.7, (3.24, 10.47, 5.16)), ('G35F65R0', 424.83, 788.97, 0, 93.7, (3.25, 7.88, 4.97)),
                                    ('G20F80R0', 242.76, 971.04, 0, 77.0, (2.52, 6.12, 3.54)), ('G40F55R5', 485.52, 667.59, 60.69, 95.3, (2.91, 9.06, 6.90)),
                                    ('G25F70R5', 303.45, 849.66, 60.69, 85.4, (1.75, 7.19, 5.56)), ('G30F60R10', 364.14, 728.28, 121.38, 89.0, (1.64, 7.26, 5.81)),
                                    ('G35F50R15', 424.83, 606.90, 182.07, 93.2, (1.61, 7.06, 5.98)), ('G20F65R15', 242.76, 788.97, 182.07, 66.6, (2.29, 6.38, 5.58)),
                                    ('G25F55R20', 303.45, 667.59, 242.76, 77.3, (2.50, 6.90, 5.61)), ('G20F50R30', 242.76, 606.90, 364.14, 70.3, (2.03, 5.60, 5.51))]:
    add(P, **{'GGBS': R(g / 1213.8, 3), 'FA (Fly ash)': R(f / 1213.8, 3), 'Other binder': R(r / 1213.8, 3) if r else '',
              'Compressive strength (MPa)': fc, 'First-cracking strength (MPa)': a, 'Tensile strength (MPa)': b, 'Tensile strain capacity (%)': c,
              'Source table/page': 'Table 2 (mix), Table 3 (fc), Table 5 (axial tension)', 'Conversions / notes': f"Mix {mid}. " + note0})

# ---------- P7 Huang 2025 ----------
P = {'Article Name': 'Fracture Properties of High-Performance High-Ductility Alkali-Activated Concrete Under Thermo-Mechanical Coupling: Effect of Fiber Hybrid Ratio',
     'Author': 'Tao Huang, Bo-Yuan Huang, Zhi-Feng Zhan, Yu-Wen Huang, Lei Wang, Meng Li, Zhi-Hong Xie, Jian-Fa Li, Jia-Ying Su', 'Year': 2025,
     'DOI / URL': 'https://doi.org/10.3390/polym17192568',
     'FA (Fly ash)': 0.7, 'GGBS': 0.3, 'WG / B (Water glass)': R(0.4 * 2 / 3), 'NaOH / B': R(0.4 / 3), 'Extra water / B': 0.06, 'SS / B (Silica sand)': 0.2,
     'PE length (mm)': 12, 'PE diameter (µm)': 20, 'PE tensile strength (MPa)': 3000, 'PE elastic modulus (GPa)': 120, 'PP length (mm)': 12, 'PP diameter (µm)': 100,
     'Curing method': 'sealed 24 h at ambient lab conditions, demoulded, water-immersed 28 d, then air-dried in shade; tested at 30 °C',
     'Curing time (days)': 28, 'Demolding age (days)': 1,
     'Compressive specimen': 'cylinder', 'Compressive specimen size (mm)': '50x100', 'Tensile specimen': 'dumbbell (dims in Fig. 2)', 'Tensile gauge length (mm)': 80,
     'Tensile test type': 'direct'}
note0 = ("Table 3 ratios to binder: QS 0.20 (quartz sand → SS/B), AAS 0.40 (sodium silicate : NaOH solution = 2:1 → AI-derived WG/B 0.2667, NaOH-solution/B 0.1333), "
         "water 0.06, BaCl2 0.01. Sodium silicate Ms 2.25 (SiO2:Na2O:H2O 29.99:13.75:56.26). NaOH molarity conflicting in paper (14 M in Sec. 2.1 vs 10 M in Sec. 2.2) "
         "– left blank. Test age not explicitly stated (after 28 d water curing; left blank). Mechanical tests performed at 30 °C. PP strength 400 MPa, modulus 13.5 GPa.")
for mid, pe, pp, fc, (a, b, c) in [('R0', 2.0, 0, 100.5, (4.4, 7.7, 5.5)), ('R25', 1.5, 0.5, 102.8, (3.5, 7.3, 7.4)), ('R50', 1.0, 1.0, 82.4, (2.7, 7.7, 5.3))]:
    add(P, **{'PE fiber (vol%)': pe, 'PP fiber (vol%)': pp, 'Compressive strength (MPa)': fc, 'First-cracking strength (MPa)': a, 'Tensile strength (MPa)': b,
              'Tensile strain capacity (%)': c, 'Source table/page': 'Table 3 (mix), Table 2 (fibres), Table 5 (fc), Table 6 (direct tension)',
              'Conversions / notes': f"Mix {mid}-30°C. " + note0})

# ---------- P8 Lim 2022 ----------
P = {'Article Name': 'Mechanical Properties of Alkali-Activated Slag Fiber Composites Varying with Fiber Volume Fractions',
     'Author': 'Hyeon-Jin Lim, Chang-Geun Cho, Jang-Yeol You, Jong-Jin Jeong', 'Year': 2022, 'DOI / URL': 'https://doi.org/10.3390/ma15186444',
     'GGBS': 0.895, 'Ca(OH)2 / B': 0.075, 'Na2SO4 / B': 0.03, 'W / B': 0.338, 'Sand (type not stated) / B': 0.40, 'VMA / B': 0.0007,
     'PVA length (mm)': 12, 'PVA diameter (µm)': 40, 'PVA tensile strength (MPa)': 1600, 'PVA elastic modulus (GPa)': 37,
     'Curing method': 'covered in air 1 d, demoulded, water curing at 23±3 °C', 'Curing time (days)': 28, 'Curing temperature (°C)': 23, 'Demolding age (days)': 1,
     'Test age (days)': 28, 'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '50x50x50', 'Tensile specimen': 'dog-bone (dims in Fig. 3)',
     'Tensile gauge length (mm)': 150, 'Tensile test type': 'direct'}
note0 = ("Binder as defined by paper = GGBS 0.895 + Ca(OH)2 0.075 + Na2SO4 0.03 (=1; same convention as existing 'Tensile Behavior of Polyetylene Fiber-Reinforced "
         "Cementless Composite' rows). Ratios as in Table 3. VMA = methyl cellulose; HRWRA = polycarboxylate.")
for mid, v, hr, fc, (a, b, c) in [('ASFC000', 0, 0.005, 30.95, (2.06, 2.06, 0.02)), ('ASFC100', 1.0, 0.012, 34.25, (2.27, 2.90, 2.71)),
                                   ('ASFC125', 1.25, 0.015, 35.50, (2.60, 3.43, 3.89)), ('ASFC150', 1.5, 0.018, 33.70, (2.76, 3.80, 4.93)),
                                   ('ASFC200', 2.0, 0.020, 32.60, (3.86, 4.88, 4.68))]:
    add(P, **{'PVA fiber (vol%)': v, 'HRWR / B': hr, 'Compressive strength (MPa)': fc, 'First-cracking strength (MPa)': a, 'Tensile strength (MPa)': b,
              'Tensile strain capacity (%)': c, 'Total fiber (vol%)': v,
              'Source table/page': 'Table 3 (mix), Table 2 (fibre), Table 5 (fc), Table 6 (direct tension)', 'Conversions / notes': f"Mix {mid}. " + note0})

# ---------- P9 Choi 2019 ----------
P = {'Article Name': 'Strain-Hardening and High-Ductile Behavior of Alkali-Activated Slag-Based Composites with Added Zirconia Silica Fume',
     'Author': 'Jeong-Il Choi, Se-Eon Park, Huy Hoang Nguyen, Sang Lyul Cha, Bang Yeon Lee', 'Year': 2019, 'DOI / URL': 'https://doi.org/10.3390/ma12213523',
     'W / B': 0.21, 'PE fiber (vol%)': 2, 'PE length (mm)': 18, 'PE diameter (µm)': 12, 'PE tensile strength (MPa)': 2700, 'PE elastic modulus (GPa)': 88,
     'Curing method': 'covered with plastic sheet at room temperature 2 d, demoulded, water curing at 23±3 °C to 28 d', 'Curing time (days)': 28,
     'Curing temperature (°C)': 23, 'Demolding age (days)': 2, 'Test age (days)': 28,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '50x50x50', 'Tensile specimen': 'dumbbell (JSCE), gauge section 30x13 mm',
     'Tensile gauge length (mm)': 80, 'Tensile test type': 'direct'}
note0 = ("Binder as defined by paper (=1) includes Ca(OH)2 and Na2SO4 activators; SF column = zirconia silica fume (ZSF, SiO2 94.51%, ZrO2 1.51%). "
         "Defoamer/B 0.001 (no column). HRWRA entered in HRWR/B. ")
add(P, **{'GGBS': 0.85, 'SF (Silica fume)': 0.05, 'Ca(OH)2 / B': 0.071, 'Na2SO4 / B': 0.029, 'HRWR / B': 0.030, 'Compressive strength (MPa)': 53.5,
          'Tensile strength (MPa)': 14.9, 'Tensile strain capacity (%)': 6.1,
          'Source table/page': 'Table 2 (mix); Section 3 text and Table 3 (fc, ft, strain)',
          'Conversions / notes': "Mix W21-S5. " + note0 + "First-cracking strength and mixes W25-S5/W30-S5 only in Figs. 3 and 6 (not entered)."})
add(P, **{'GGBS': 0.895, 'Ca(OH)2 / B': 0.075, 'Na2SO4 / B': 0.03, 'HRWR / B': 0.025, 'Compressive strength (MPa)': R(53.5 / 1.188, 1),
          'Tensile strength (MPa)': R(14.9 / 1.265, 2), 'Tensile strain capacity (%)': R(6.1 / 1.137, 2),
          'Source table/page': 'Table 2 (mix); outputs AI-derived from text % differences vs W21-S5',
          'Conversions / notes': "Mix W21-S0. " + note0 + "VERIFY (AI-derived): text says W21-S5 is +18.8% fc, +26.5% ft, +13.7% strain vs W21-S0 → "
                                  "fc = 53.5/1.188, ft = 14.9/1.265, strain = 6.1/1.137. Not directly tabulated."})

# ---------- P10 Ling 2024 ----------
P = {'Article Name': 'Evaluation of Bonding Behavior between Engineered Geopolymer Composites with Hybrid PE/PVA Fibers and Concrete Substrate',
     'Author': 'Yu Ling, Xiafei Zhang, Yanwei Wu, Weiyu Zou, Chuang Wang, Chaosen Li, Wen Li', 'Year': 2024, 'DOI / URL': 'https://doi.org/10.3390/ma17153778',
     'QP / B (Quartz powder)': 0.2, 'WG / B (Water glass)': R(0.4 * 2 / 3), 'NaOH / B': R(0.4 / 3), 'NaOH molarity (M)': 10, 'Extra water / B': 0.06,
     'PE fiber (vol%)': 2, 'PE length (mm)': 12,
     'Curing method': 'covered with plastic film indoors 24 h, demoulded, water curing 28 d', 'Curing time (days)': 28, 'Demolding age (days)': 1,
     'Compressive specimen': 'cylinder', 'Compressive specimen size (mm)': '50x100', 'Tensile specimen': 'dumbbell (JSCE; dims in Fig. 3b)',
     'Tensile gauge length (mm)': 80, 'Tensile test type': 'direct'}
note0 = ("Table 3 ratios: QP 0.20, AAS 0.40 (sodium silicate : 10 M NaOH solution = 2:1 → AI-derived WG/B 0.2667, NaOH-solution/B 0.1333; silicate Ms 2.25), "
         "water 0.06, BaCl2 0.01, defoamer 0.001. Fibre property table (Table 2) appears to have PE/PVA labels swapped – only length entered. Test age not "
         "explicitly stated (after 28 d water curing; left blank). First-crack stress not reported. M1-series rows not entered: identical to Guo et al. 2024 "
         "(10.3390/ma17174356).")
for mid, fa, gg, fc, e, s in [('M2-U2.0P0.0', 0.6, 0.4, 97.5, 6.62, 7.83), ('M3-U2.0P0.0', 0.5, 0.5, 108.9, 6.31, 9.29)]:
    add(P, **{'FA (Fly ash)': fa, 'GGBS': gg, 'Compressive strength (MPa)': fc, 'Tensile strength (MPa)': s, 'Tensile strain capacity (%)': e,
              'Source table/page': 'Table 3 (mix), Table 7 (fc), Table 10 (σc, εtu, σtu)', 'Conversions / notes': f"Mix {mid}. " + note0})

# ---------- P11 Li 2026 ----------
S = 1700.0
P = {'Article Name': 'Enhancing Tensile Performance of Lithium Slag Geopolymers Using Hybrid Fibers and Modified Multi-Walled Carbon Nanotubes',
     'Author': 'Qing Li, Chong Deng, Yali Hu, Mingxing Luo, Daopei Zhu, Cai Wu', 'Year': 2026, 'DOI / URL': 'https://doi.org/10.3390/ma19010213',
     'FA (Fly ash)': R(1000 / S), 'Metakaolin': R(75 / S), 'SF (Silica fume)': R(75 / S), 'Other binder': R(550 / S), 'Na2O / B': 0.07,
     'Activator modulus Ms (SiO2/Na2O)': 1.4, 'W / B': 0.4, 'Binder content (kg/m³)': S,
     'PVA length (mm)': 12, 'PVA diameter (µm)': 60, 'PVA tensile strength (MPa)': 1720, 'PVA elastic modulus (GPa)': 52.6,
     'Curing method': 'demoulded at 24 h, then 20±2 °C, 95% RH for 28 d', 'Curing time (days)': 28, 'Curing temperature (°C)': 20, 'Curing RH (%)': 95,
     'Demolding age (days)': 1, 'Test age (days)': 28, 'Tensile specimen': 'dog-bone (dims in Fig. 5b)', 'Tensile gauge length (mm)': 80, 'Tensile test type': 'direct'}
note0 = ("B = all solids as used by paper for W/S and alkali equivalent = 1700 kg/m3 (FA 1000, MK 75, SF 75, lithium slag LS 300, fly-ash microsphere FAC 250). "
         "Other binder = LS + FAC (LS/B 0.1765, FAC/B 0.1471; FAC described as lightweight filler). Activator: waterglass (Na2O 8.98%, SiO2 27.2%, Ms 3.24) "
         "adjusted with solid NaOH to Ms 1.4; alkali equivalent 7% (119 kg Na2O); water/solids 0.4 (680 kg). No sand. PVA strength column printed as "
         "'Dissociation' (MPa). Compressive strength not reported in accessible text.")
for mid, cnt, pva, st, (a, b, c) in [('FL-EGC-U', 0, 2, 0, (1.49, 2.44, 3.44)), ('FL-EGC-K1', 0.10, 2, 0, (1.67, 2.57, 4.39)),
                                      ('FL-EGC-K2', 0.15, 2, 0, (1.87, 2.75, 5.82)), ('FL-EGC-K3', 0.2, 2, 0, (1.52, 2.45, 5.12)),
                                      ('FL-EGC-N1', 0.15, 2, 0.5, (2.51, 3.36, 1.01)), ('FL-EGC-N2', 0.15, 2, 1, (2.91, 3.24, 1.42)),
                                      ('FL-EGC-N3', 0.15, 2, 1.5, (2.78, 3.12, 0.89)), ('FL-EGC-N4', 0.15, 2.5, 0.5, (2.79, 2.96, 1.67)),
                                      ('FL-EGC-N5', 0.15, 2.5, 1, (2.29, 2.99, 3.02)), ('FL-EGC-N6', 0.15, 2.5, 1.5, (2.31, 3.11, 2.68))]:
    extra = {'Steel fiber (vol%)': st, 'Steel length (mm)': 13, 'Steel diameter (µm)': 220, 'Steel tensile strength (MPa)': 3000,
             'Steel elastic modulus (GPa)': 214} if st else {}
    add(P, **extra, **{'PVA fiber (vol%)': pva, 'First-cracking strength (MPa)': a, 'Tensile strength (MPa)': b, 'Tensile strain capacity (%)': c,
                       'Source table/page': 'Tables 4–5 (mix), Table 3 (fibres), Table 7/9 (tension)',
                       'Conversions / notes': f"Mix {mid}. Modified MWCNT = {cnt} wt% (no column). " + note0})

with open(D + "geopolymer.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=hdr)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in hdr})
print(len(rows), len(hdr))
print(collections.Counter(r['DOI / URL'] for r in rows))
