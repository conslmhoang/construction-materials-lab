# -*- coding: utf-8 -*-
"""Builder for w2_alkali.csv - alkali-activated / geopolymer fibre composites (wave 2).
All numbers transcribed from full texts (Europe PMC fullTextXML). Ratios = kg/m3 / binder kg/m3.
"""
import csv, os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'additions')
hdr = next(csv.reader(open(os.path.join(D, 'TEMPLATE.csv'), encoding='utf-8-sig')))
rows = []
FIBS = ['PE fiber (vol%)', 'PVA fiber (vol%)', 'Steel fiber (vol%)', 'PP fiber (vol%)', 'PBO fiber (vol%)',
        'Glass fiber (vol%)', 'PET fiber (vol%)', 'Basalt fiber (vol%)', 'Carbon fiber (vol%)']


def add(base, **kw):
    r = dict(base)
    r.update(kw)
    for k in r:
        assert k in hdr, k
    if 'Total fiber (vol%)' not in r:
        tv = sum(float(r.get(k) or 0) for k in FIBS)
        if tv:
            r['Total fiber (vol%)'] = round(tv, 4)
    rows.append(r)


def R(x, n=4):
    return round(x, n)


WG = 'WG / B (Water glass)'

# =====================================================================================
# P1 Smirnova et al. 2022, Materials 15:1607 - PP microfibre alkali-activated slag
P = {'Article Name': 'Strain Hardening of Polypropylene Microfiber Reinforced Composite Based on Alkali-Activated Slag Matrix',
     'Author': 'Olga M. Smirnova, Ignacio Menendez Pidal, Aleksandr V. Alekseev, Dmitry N. Petrov, Mikhail G. Popov',
     'Year': 2022, 'DOI / URL': 'https://doi.org/10.3390/ma15041607', 'GGBS': 1.0,
     'Activator modulus Ms (SiO2/Na2O)': 1.5,
     'PP length (mm)': 6, 'PP diameter (µm)': 20, 'Sand max size (µm)': 2000,
     'Test age (days)': 28, 'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '70.7x70.7x70.7',
     'Tensile specimen': 'prism 40x40x160 (3-point bending)', 'Tensile test type': 'flexural',
     'Source table/page': 'Table 4 (mix), Table 2 (fibre), Tables 5-6 (fc, flexural)'}
for mid, B, qp, qs, wg, naoh, w, wb, fc, ffc, sh in [
        ('Mix 3', 1133, 224, 113, 120, 38, 338, 0.30, 42.37, 3.85, 0.0),
        ('Mix 4', 1275, 232, 120, 122, 41, 280, 0.22, 39.86, 3.45, 0.23)]:
    add(P, **{'QP / B (Quartz powder)': R(qp / B), 'SS / B (Silica sand)': R(qs / B), WG: R(wg / B),
              'NaOH / B': R(naoh / B), 'Extra water / B': R(w / B), 'W / B': wb, 'Binder content (kg/m³)': B,
              'PP fiber (vol%)': 3.5, 'Compressive strength (MPa)': fc,
              'First-cracking strength (MPa)': ffc, 'Tensile strength (MPa)': R(ffc + sh, 2),
              'Conversions / notes': (
                  f"{mid}. Table 4 kg/m3: GGBS {B}, ground quartz sand A4 (D50 4 µm) {qp}, quartz sand 0.06-2 mm {qs}, "
                  f"liquid glass (density 1.3 g/cm3, silicate modulus 1.5) {wg}, NaOH {naoh}, water {w}, PP 32 kg/m3 (=3.5 vol% per paper). "
                  f"Ratios = kg/m3 / GGBS. W/B = paper's water-to-slag ratio {wb} (free water / slag; liquid-glass water not included). "
                  f"Flexural (bending) strength at first microcrack = {ffc} MPa (Table 5); Tensile strength = first-crack + strain-hardening "
                  f"increment {sh} MPa (Table 6) = derived ultimate bending strength. Curing regime not reported; tested at 28 d. "
                  f"PP: 350 MPa, 5.7 GPa, 0.91 g/cm3.")})

# =====================================================================================
# P2 Yuan, Jia, Xu 2025, Polymers 17:175 - PP fibre high-FA AAFS concrete
P = {'Article Name': 'Study on the Improvement Effect of Polypropylene Fiber on the Mechanical Properties and Freeze–Thaw Degradation Performance of High Fly Ash Content Alkali-Activated Fly Ash Slag Concrete',
     'Author': 'Zhu Yuan, Yanmin Jia, Junming Xu', 'Year': 2025, 'DOI / URL': 'https://doi.org/10.3390/polym17020175',
     'FA (Fly ash)': 0.8, 'GGBS': 0.2, WG: R(81.7 / 430), 'NaOH / B': R(18.4 / 430), 'Na2O / B': 0.06,
     'Activator modulus Ms (SiO2/Na2O)': 1.0, 'W / B': R((105.3 + 0.5392 * 81.7) / 430, 3), 'Extra water / B': R(105.3 / 430),
     'Sand (type not stated) / B': R(655 / 430), 'Coarse aggregate / B': R(1165 / 430), 'HRWR / B': R(4.73 / 430),
     'Binder content (kg/m³)': 430, 'PP fiber (vol%)': 0.9, 'PP length (mm)': 12,
     'Curing method': 'covered with film in mould 24 h, demoulded, wrapped tightly in plastic film at room temperature 20±2 °C until test',
     'Curing temperature (°C)': 20, 'Demolding age (days)': 1,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '100x100x100'}
N2 = ("Mix A6M1PPF0.90. Table 2 kg/m3: FA 344, slag 86, fine agg (medium sand FM 2.66) 655, coarse agg 5-20 mm 1165, sodium silicate 81.7 "
      "(32.35% SiO2, 13.73% Na2O, 53.92% water), NaOH solid 18.4, water 105.3, naphthalene water reducer 4.73, PPF 0.90 vol%. "
      "Ratios = kg/m3 / 430. Na2O/B = alkali equivalent 6%; Ms = activator modulus 1.0 (paper). W/B = (water + silicate water)/B; NaOH solid not counted. "
      "PP fibre properties only in ref [41]. ")
add(P, **{'Test age (days)': 365, 'Compressive strength (MPa)': 54.9, 'Source table/page': 'Table 2 (mix), Sect. 5.1 text (1-year fc)',
          'Conversions / notes': N2 + "1-year fc 54.9 MPa from text; 7/28/90 d fibre-mix fc only in Fig. 5 (not extracted)."})
add(P, **{'Test age (days)': 28, 'Tensile strength (MPa)': 3.92, 'Tensile test type': 'flexural',
          'Tensile specimen': 'prism (GB/T 50081-2019 flexural)', 'Source table/page': 'Table 2 (mix), Sect. 5.2 text (28 d flexural)',
          'Conversions / notes': N2 + "28 d flexural strength 3.92 MPa from text; 28 d fc of this mix only in Fig. 5."})

# =====================================================================================
# P3 Yuan et al. 2024, Materials 17:5668 - GF / PPF reinforced AAFS mortar
P = {'Article Name': 'Study on the Properties of High Fly Ash Content Alkali-Activated Fly Ash Slag Pastes and Fiber-Reinforced Mortar Under Normal Temperature Curing',
     'Author': 'Zhu Yuan, Yanmin Jia, Jinyu Sun, Xiaobo Zhang, Yaojie Hu, Xuhua Han', 'Year': 2024,
     'DOI / URL': 'https://doi.org/10.3390/ma17225668', 'FA (Fly ash)': 0.8, 'GGBS': 0.2, 'W / B': 0.42,
     'River sand / B': 3.0, 'Binder content (kg/m³)': 450,
     'Curing method': 'covered with plastic film at room temperature 24 h, demoulded, standard curing room until test',
     'Demolding age (days)': 1, 'Test age (days)': 28,
     'Compressive specimen': 'prism halves', 'Compressive specimen size (mm)': '40x40 (from 40x40x160 prisms)',
     'Tensile specimen': 'prism 40x40x160 (3-point bending, GB/T 17671)', 'Tensile test type': 'flexural'}
ACT = {1.0: (33.7, 147.5, 100.5), 1.2: (30.0, 167.6, 89.6), 1.4: (24.7, 197.0, 73.8)}
for mid, ms, fib, vf, fc, ft in [('M1.0-PPF0.45', 1.0, 'PP', 0.45, 45.7, 7.34), ('M1.0-GF0.90', 1.0, 'GF', 0.90, 42.2, 6.62),
                                  ('M1.2-GF0.45', 1.2, 'GF', 0.45, 38.5, None), ('M1.4-GF0.45', 1.4, 'GF', 0.45, 35.8, None)]:
    naoh, ss, w = ACT[ms]
    f = {'PP fiber (vol%)': vf, 'PP length (mm)': 12} if fib == 'PP' else {'Glass fiber (vol%)': vf}
    kw = dict(f, **{WG: R(ss / 450), 'NaOH / B': R(naoh / 450), 'Extra water / B': R(w / 450),
                    'Activator modulus Ms (SiO2/Na2O)': ms, 'Compressive strength (MPa)': fc,
                    'Source table/page': 'Table 4 (mortar mix), Table 2 (silicate), Sect. 5.8-5.9 text (28 d flexural, fc)'})
    if ft:
        kw['Tensile strength (MPa)'] = ft
    else:
        kw['Tensile test type'] = None
        kw['Tensile specimen'] = None
    add(P, **kw, **{'Conversions / notes': (
        f"Mix {mid}. Table 4 kg/m3: FA 360, slag 90, river sand 1350 (FM 2.66), NaOH {naoh}, sodium silicate {ss} (13.73% Na2O, 32.35% SiO2, Ms 2.43), water {w}. "
        f"Ratios = kg/m3 / 450. W/B = 0.42 as stated by paper ('water cement ratio'). Activator modulus {ms} (paper). "
        f"VERIFY: fibre dosage {vf}% 'calculated based on the volume fraction of the precursor' (paper) - entered as vol% unchanged. "
        f"{'Short-cut glass fibre (GF) 12 mm. ' if fib == 'GF' else 'PP fibre 12 mm. '}"
        f"Values from text (other mixes only in Figs. 12-13). Curing-room temperature/RH not stated.")})

# =====================================================================================
# P4 Al Bdairi et al. 2026, Polymers 18:2023 - one-part (Na2SiO3.5H2O + Na2CO3) GP mortar
P = {'Article Name': 'Fiber-Reinforced One-Part Geopolymer Mortars Incorporating Red Mud, Ceramic Powder, and MgO: Performance Under Different Curing Regimes and Curing-Based Environmental Assessment',
     'Author': 'Mohammed Dakhel Al Bdairi, Orhan Canpolat, Mucteba Uysal, Ömer Can Özen, Ömer Faruk Kuranlı, Aygül Zara Kebir',
     'Year': 2026, 'DOI / URL': 'https://doi.org/10.3390/polym18162023',
     'GGBS': 0.50, 'FA (Fly ash)': 0.25, 'Other binder': 0.20, 'Reactive MgO': 0.05,
     'SSM / B (Na2SiO3 anhydrous)': R(0.12 * 122.06 / 212.14, 5), 'Na2CO3 / B (anhydrous)': 0.04,
     'W / B': 0.32, 'SS / B (Silica sand)': 2.0, 'Demolding age (days)': 1,
     'Compressive specimen': 'prism halves', 'Compressive specimen size (mm)': '40x40 (from 40x40x160 prisms, EN 196-1)',
     'Tensile specimen': 'prism 40x40x160 (3-point bending, EN 196-1)', 'Tensile test type': 'flexural'}
FIB4 = {'PVA': {'PVA length (mm)': 8, 'PVA diameter (µm)': 39, 'PVA tensile strength (MPa)': 1620},
        'MS': {'Steel length (mm)': 6, 'Steel diameter (µm)': 150, 'Steel tensile strength (MPa)': 2100},
        'BF': {}}
FCOL = {'PVA': 'PVA fiber (vol%)', 'MS': 'Steel fiber (vol%)', 'BF': 'Basalt fiber (vol%)'}
# (mix, flex7 amb, flex7 heat, flex28 amb, flex28 heat, fc7 amb, fc7 heat, fc28 amb, fc28 heat, split amb, split heat)
D4 = [('0.4PVA', 3.2, 5.0, 4.8, 6.2, 34.9, 52.5, 38.0, 53.0, 3.5, 4.4),
      ('0.8PVA', 3.5, 5.0, 5.5, 7.5, 28.8, 46.0, 37.5, 54.0, 3.5, 4.4),
      ('0.4BF', 2.4, 4.2, 3.0, 6.7, 30.8, 49.0, 35.0, 59.0, 3.6, 4.5),
      ('0.8BF', 2.8, 6.2, 3.7, 6.4, 32.1, 48.0, 37.5, 55.0, 3.4, 4.1),
      ('0.4MS', 2.4, 5.3, 3.2, 7.5, 39.5, 56.8, 46.7, 73.0, 3.5, 4.2),
      ('0.8MS', 2.0, 4.8, 3.4, 7.0, 40.8, 64.8, 44.0, 72.0, 3.4, 4.4)]
for mid, f7a, f7h, f28a, f28h, c7a, c7h, c28a, c28h, sa, shh in D4:
    vf = float(mid[:3])
    ft = mid[3:]
    fib = dict(FIB4[ft], **{FCOL[ft]: vf})
    for cur, (f7, f28, c7, c28, sp) in {'ambient': (f7a, f28a, c7a, c28a, sa), 'heat': (f7h, f28h, c7h, c28h, shh)}.items():
        if cur == 'ambient':
            cm = {'Curing method': 'sealed 24 h at room temperature, demoulded, ambient curing 20±2 °C until test',
                  'Curing temperature (°C)': 20}
        else:
            cm = {'Curing method': 'sealed 24 h at room temperature, demoulded, 80 °C for 24 h in sealed heat-resistant bags, then stored (humidity-controlled) until test',
                  'Curing temperature (°C)': 80, 'Heat curing duration (h)': 24}
        for age, fl, fc in [(7, f7, c7), (28, f28, c28)]:
            add(P, **fib, **cm, **{'Test age (days)': age, 'Compressive strength (MPa)': fc, 'Tensile strength (MPa)': fl,
                                   'Source table/page': f"Table 3 (mix), Table 1 (fibre), Table {7 if age == 7 else 8} (flexural), Table {9 if age == 7 else 10} (fc)",
                                   'Conversions / notes': (
                                       f"Mix {mid}, {cur} curing. One-part GP: binder (Table 3, % of B) = GGBFS 50, FA 25, ceramic powder 10 + red mud 10 "
                                       f"(both in 'Other binder' = 0.20), MgO 5 (Reactive MgO). Solid activator (not in B): Na2SiO3·5H2O 12% of B -> anhydrous "
                                       f"Na2SiO3/B = 0.12x122.06/212.14 = 0.0690; Na2CO3 4% of B. W/B 0.32, EN 196-1 standard sand / B = 2.0. "
                                       f"Fibre {vf} vol% ({'basalt 12 mm/20 µm, 4100 MPa' if ft == 'BF' else 'PVA 8 mm/39 µm, 1620 MPa' if ft == 'PVA' else 'micro-steel 6 mm/0.15 mm, 2100 MPa'}). "
                                       f"Splitting tensile (Table 11, Ø100x200 cylinders, test age not stated) = {sp} MPa - not entered. "
                                       f"Heat-cured specimens: post-heat storage condition only described as humidity-controlled.")})

# =====================================================================================
# P5 Kim et al. 2015, Materials 8:7309 (ma8115383) - steel fibre AAS concrete
P = {'Article Name': 'Mechanical Properties and Eco-Efficiency of Steel Fiber Reinforced Alkali-Activated Slag Concrete',
     'Author': 'Sun-Woo Kim, Seok-Joon Jang, Dae-Hyun Kang, Kyung-Lim Ahn, Hyun-Do Yun', 'Year': 2015,
     'DOI / URL': 'https://doi.org/10.3390/ma8115383', 'GGBS': 1.0, 'W / B': 0.55,
     'River sand / B': R(756 / 373), 'Coarse aggregate / B': R(924 / 373), 'Sand max size (µm)': 5000, 'Binder content (kg/m³)': 373,
     'Steel length (mm)': 30, 'Steel diameter (µm)': 500, 'Steel tensile strength (MPa)': 1100, 'Demolding age (days)': 1,
     'Compressive specimen': 'cylinder', 'Compressive specimen size (mm)': '100x200'}
FC5 = {0.5: (15.5, 24.8, 23.0, 35.9, 39.3), 1.0: (15.8, 23.4, 25.5, 34.6, 34.7), 1.5: (17.5, 27.8, 28.5, 38.1, 42.3),
       2.0: (23.5, 31.8, 34.6, 40.1, 41.4)}  # 3d wet, 7d dry, 7d wet, 28d dry, 28d wet
FL5 = {0.5: (4.674, 6.638), 1.0: (5.249, 11.615), 1.5: (5.910, 11.714), 2.0: (4.180, 13.262)}
N5 = ("AAS binder = GGBS activated with Ca(OH)2 (primary) + Na2SiO3 and Na2CO3 (auxiliary) - activator dosages NOT reported, so activator columns left empty. "
      "Table 2 kg/m3: water 205, AAS binder 373, sand 756 (river, max 5 mm), coarse 924 (granite, max 20 mm). VERIFY: fibre dosage given as Vf (%) in Table 3 "
      "but text says 'by weight of the binder' - entered as vol% per Table 3. Hooked-end steel fibre 30 mm, 0.5 mm, 1100 MPa. ")
for vf in [0.5, 1.0, 1.5, 2.0]:
    w3, d7, w7, d28, w28 = FC5[vf]
    wet = {'Curing method': 'mist room 23 °C/95% RH 24 h, demoulded, water curing at 23 °C until test', 'Curing temperature (°C)': 23,
           'Curing RH (%)': 100}
    dry = {'Curing method': 'mist room 23 °C/95% RH 24 h, demoulded, air curing at 23±5 °C, 50±5% RH until test', 'Curing temperature (°C)': 23,
           'Curing RH (%)': 50}
    for cm, age, fc, cname in [(wet, 3, w3, 'wet'), (wet, 7, w7, 'wet'), (dry, 7, d7, 'dry'), (dry, 28, d28, 'dry'), (wet, 28, w28, 'wet')]:
        kw = {'Steel fiber (vol%)': vf, 'Test age (days)': age, 'Compressive strength (MPa)': fc,
              'Source table/page': 'Table 2 (mix), Table 3 (variables), Table 4 (fc)'}
        if cname == 'wet' and age == 28:
            ff, fu = FL5[vf]
            kw.update({'First-cracking strength (MPa)': ff, 'Tensile strength (MPa)': fu, 'Tensile test type': 'flexural',
                       'Tensile specimen': 'prism 100x100x400 (ASTM C78)',
                       'Source table/page': 'Table 2 (mix), Table 3 (variables), Table 4 (fc), Table 5 (flexural)'})
        add(P, **cm, **kw, **{'Conversions / notes': N5 + f"AAS-{vf} {cname}-cured. RH 100 entered for water immersion."})

# =====================================================================================
# P6 Ding & Bai 2018, Materials 11:1445 - steel fibre slag geopolymer mortar / concrete
P = {'Article Name': 'Fracture Properties and Softening Curves of Steel Fiber-Reinforced Slag-Based Geopolymer Mortar and Concrete',
     'Author': 'Yao Ding, Yu-Lei Bai', 'Year': 2018, 'DOI / URL': 'https://doi.org/10.3390/ma11081445', 'GGBS': 1.0,
     'Steel length (mm)': 13, 'Steel diameter (µm)': 212, 'Steel tensile strength (MPa)': 2850, 'Steel elastic modulus (GPa)': 210,
     'Curing method': 'covered with plastic sheet 24 h, demoulded, environmental chamber 21±1 °C, 90±5% RH for 28 d',
     'Curing time (days)': 28, 'Curing temperature (°C)': 21, 'Curing RH (%)': 90, 'Demolding age (days)': 1, 'Test age (days)': 28,
     'Compressive specimen': 'cube', 'Tensile test type': 'splitting',
     'Source table/page': 'Table 3 (mix), Table 2 (fibre), Table 4 (fc, splitting)'}
for typ, B, sand, ca, w, wg, naoh, n, ms, wb, size, data in [
        ('SGM', 783, 1174, None, 254, 182, 30, 0.05, 1.5, 0.44, '70.7x70.7x70.7', [(1.0, 78.0, 9.34), (1.5, 78.2, 10.8), (2.0, 84.6, 13.1)]),
        ('SGC', 420, 694, 1041, 117, 117, 11, 0.045, 2.0, 0.45, '150x150x150', [(1.0, 81.1, 7.47), (1.5, 85.6, 8.37), (2.0, 78.9, 8.06)])]:
    for vf, fc, fst in data:
        kw = {'Sand (type not stated) / B': R(sand / B), WG: R(wg / B), 'NaOH / B': R(naoh / B), 'Extra water / B': R(w / B),
              'Na2O / B': n, 'Activator modulus Ms (SiO2/Na2O)': ms, 'W / B': wb, 'Binder content (kg/m³)': B,
              'Steel fiber (vol%)': vf, 'Compressive specimen size (mm)': size, 'Tensile specimen': f'cube {size}',
              'Compressive strength (MPa)': fc, 'Tensile strength (MPa)': fst}
        if ca:
            kw['Coarse aggregate / B'] = R(ca / B)
        add(P, **kw, **{'Conversions / notes': (
            f"{typ}-SF{vf}. Table 3 kg/m3: slag {B}, fine agg (medium sand FM 2.81) {sand}, {'coarse agg (gravel max 10 mm) ' + str(ca) + ', ' if ca else ''}"
            f"water {w}, Na-silicate solution {wg} (59% water, modulus 3.7), NaOH {naoh}. n = Na2O % of slag = {n * 100:g}%, activator Ms {ms}. "
            f"W/B {wb} as stated (Table 3 w/b; includes silicate-solution water). Splitting on cubes (same size as compression).")})

# =====================================================================================
# P7 Junior et al. 2021, Materials 14:4447 - mono/hybrid fibre FA geopolymer mortar (heat cured)
P = {'Article Name': 'Workability and Flexural Properties of Fibre-Reinforced Geopolymer Using Different Mono and Hybrid Fibres',
     'Author': 'Jacob Junior, Ashish Kumer Saha, Prabir Kumar Sarker, Alokesh Pramanik', 'Year': 2021,
     'DOI / URL': 'https://doi.org/10.3390/ma14164447', 'FA (Fly ash)': 1.0, WG: R(213 / 497), 'NaOH / B': R(85 / 497),
     'NaOH molarity (M)': 10, 'Mixing liquid / B': R((213 + 85) / 497), 'Fine sand / B': R(1367 / 497), 'Sand max size (µm)': None,
     'SP / B': R(6 / 497), 'Binder content (kg/m³)': 497,
     'Curing method': 'heat cured 70 °C for 24 h in mould, demoulded, ambient until test at 7 d', 'Curing temperature (°C)': 70,
     'Heat curing duration (h)': 24, 'Demolding age (days)': 1, 'Test age (days)': 7,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '50x50x50',
     'Tensile specimen': 'plate 300x75x20 (flexural)', 'Tensile test type': 'flexural'}
FP = {'S': {'Steel length (mm)': 10, 'Steel diameter (µm)': 120, 'Steel tensile strength (MPa)': 2500, 'Steel elastic modulus (GPa)': 200},
      'PVA': {'PVA length (mm)': 8, 'PVA diameter (µm)': 38, 'PVA tensile strength (MPa)': 1600, 'PVA elastic modulus (GPa)': 40},
      'PP': {'PP length (mm)': 6, 'PP diameter (µm)': 32}, 'ARG': {}}
FC7 = {'S': 'Steel fiber (vol%)', 'PVA': 'PVA fiber (vol%)', 'PP': 'PP fiber (vol%)', 'ARG': 'Glass fiber (vol%)'}
for mid, comp, fcr, fu, fc in [('S1.0', {'S': 1.0}, 3.22, 4.37, 52), ('ARG1.0', {'ARG': 1.0}, 6.03, 6.04, 48),
                               ('PVA1.5', {'PVA': 1.5}, 4.53, 4.54, 45), ('PP1.5', {'PP': 1.5}, 3.19, 3.19, 30),
                               ('ARG0.5-S0.5', {'ARG': 0.5, 'S': 0.5}, 4.56, 5.29, 45), ('PVA1.0-S0.5', {'PVA': 1.0, 'S': 0.5}, 4.02, 4.70, 35),
                               ('PVA1.0-ARG0.5', {'PVA': 1.0, 'ARG': 0.5}, 4.89, 4.89, 38), ('PP1.0-S0.5', {'PP': 1.0, 'S': 0.5}, 5.67, 5.69, 55),
                               ('PP1.0-ARG0.5', {'PP': 1.0, 'ARG': 0.5}, 4.70, 4.70, 42)]:
    kw = {}
    for k, v in comp.items():
        kw.update(FP[k])
        kw[FC7[k]] = v
    add(P, **kw, **{'Compressive strength (MPa)': fc, 'First-cracking strength (MPa)': fcr, 'Tensile strength (MPa)': fu,
                    'Source table/page': 'Table 1 (mix), Table 2 (fibres), Table 3 (designations), Table 4/5 (flexural), Sect. 3.2 text (fc)',
                    'Conversions / notes': (
                        f"Mix {mid}. Table 1 per m3: fine sand 1367 (mean size 1.18 mm), class F FA 497, Na2SiO3 solution 213 (58.5% water, 30% SiO2, 11.5% Na2O), "
                        f"10 M NaOH solution 85, naphthalene SP 6. Liquid/FA = 0.6 (paper). W/B not computed (NaOH solution water not given). "
                        f"AR-glass fibre (13 mm, 18 µm, 1500 MPa, 74 GPa) -> Glass fiber column. PP 450 MPa / 3.5 GPa. fc read from text (Figure 4 values quoted in text).")})

# =====================================================================================
# P8 Eskandarinia et al. 2022, Materials 15:6623 - recycled tyre steel fibre AAS concrete
P = {'Article Name': 'Optimized Alkali-Activated Slag-Based Concrete Reinforced with Recycled Tire Steel Fiber',
     'Author': 'Milad Eskandarinia, Mina Esmailzade, Ata Hojatkashani, Aida Rahmani, Soheil Jahandari', 'Year': 2022,
     'DOI / URL': 'https://doi.org/10.3390/ma15196623', 'GGBS': 1.0, WG: 0.35, 'NaOH / B': 0.20, 'NaOH molarity (M)': 14,
     'SP / B': 0.01, 'Binder content (kg/m³)': 400, 'Steel length (mm)': 16.2, 'Steel diameter (µm)': 230,
     'Curing method': 'in moulds under wet hessian 24 h at 20-23 °C, demoulded, sealed in plastic bags until test',
     'Demolding age (days)': 1, 'Test age (days)': 28, 'Compressive specimen': 'cylinder', 'Compressive specimen size (mm)': '100x200',
     'Source table/page': 'Table 3/Table 8 (mix TM17 basis), Sect. 4.2.3 text (fc)'}
for vf, pct in [(0.2, 7.4), (0.4, 23.1), (0.6, 29.3)]:
    add(P, **{'Steel fiber (vol%)': vf, 'Compressive strength (MPa)': R(44.67 * (1 + pct / 100), 2),
              'Conversions / notes': (
                  f"Mix S{vf} (= optimal AASC TM17 + {vf} vol% RTSF). Binder slag 400 kg/m3, alkaline solution/binder 0.55, SS/SH 1.75 -> "
                  f"SS 140 (WG/B 0.35; 28.3% SiO2, 11.7% Na2O, 60% water), SH 80 kg/m3 of 14 M solution (NaOH/B 0.20 = solution). "
                  f"Water/alkali-activated solids ratio 0.4 (paper's W/S); extra water and aggregate masses for TM17 not tabulated -> left empty "
                  f"(coarse aggregate = 50% of aggregate, max 12.5 mm). SP 1% of binder. VERIFY: fc derived = 44.67 MPa (S0, text) x (1 + {pct}%) "
                  f"from text percentages. Flexural: fcr ~3.53 MPa average of fibre mixes, fMOR S0.6 = 3.46 MPa (text) - not entered per-mix. "
                  f"Recycled tyre steel fibre avg 16.2 mm x 0.23 mm (E, strength not measured).")})

# =====================================================================================
# P9 Zhang et al. 2022, Polymers 14:3765 - PVA + nano-SiO2 MK/FA geopolymer
P = {'Article Name': 'Effect of Single and Synergistic Reinforcement of PVA Fiber and Nano-SiO2 on Workability and Compressive Strength of Geopolymer Composites',
     'Author': 'Peng Zhang, Shiyao Wei, Yuanxun Zheng, Fei Wang, Shaowei Hu', 'Year': 2022,
     'DOI / URL': 'https://doi.org/10.3390/polym14183765', WG: R(445.4 / 613.6), 'NaOH / B': R(71 / 613.6),
     'Activator modulus Ms (SiO2/Na2O)': 1.3, 'W / B': 0.65, 'Extra water / B': R(106.2 / 613.6), 'SS / B (Silica sand)': 1.0,
     'Sand max size (µm)': 120, 'SP / B': R(3.07 / 613.6, 5), 'Binder content (kg/m³)': 613.6,
     'PVA length (mm)': 12, 'PVA diameter (µm)': 40, 'PVA tensile strength (MPa)': 1560,
     'Curing method': 'demoulded after 24 h, standard curing box until 28 d', 'Curing time (days)': 28, 'Demolding age (days)': 1,
     'Test age (days)': 28, 'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '70.7x70.7x70.7',
     'Source table/page': 'Table 2 (mix), Table 1 (fibre), Sect. 3.3 text (fc)'}
for mid, pva, ns, fc in [('P-0.6', 0.6, 0, 58.5), ('P-0.8', 0.8, 0, 60.3), ('P-1.2', 1.2, 0, 50.8), ('PN-0.8-1.0', 0.8, 1.0, 63.1),
                         ('PN-1.2-1.0', 1.2, 1.0, 57.6), ('PN-0.6-1.5', 0.6, 1.5, 63.6), ('PN-0.6-2.5', 0.6, 2.5, 59.8)]:
    s = ns / 100
    kw = {'Metakaolin': R(0.7 * (1 - s)), 'FA (Fly ash)': R(0.3 * (1 - s)), 'PVA fiber (vol%)': pva, 'Compressive strength (MPa)': fc}
    if ns:
        kw['Nano-SiO2'] = R(s)
    add(P, **kw, **{'Conversions / notes': (
        f"Mix {mid}. Table 2 kg/m3: waterglass 445.4 (modulus tuned to 1.3 with NaOH, Na2O adjusted to 15% with water), NaOH 71, water 106.2, "
        f"quartz sand 613.6 (75-120 µm), MK+FA ~613.6 (FA:MK = 3:7), SP 3.07. B = MK+FA(+NS); NS {ns}% of cementing materials; "
        f"binder fractions computed from FA:MK = 3:7 and NS % (Table 2 MK/FA kg values vary slightly between NS rows). Ratios / 613.6. "
        f"W/B 0.65 as stated. fc from text (Fig. 9 values quoted): P-x series = 0% NS; PN-0.6-x series = 0.6% PVA. Curing box T/RH not stated.")})

# =====================================================================================
# P10 Monfardini, Facconi, Minelli 2019, Materials 12:3356 - FR alkali-activated FA concrete
P = {'Article Name': 'Experimental Tests on Fiber-Reinforced Alkali-Activated Concrete Beams Under Flexure: Some Considerations on the Behavior at Ultimate and Serviceability Conditions',
     'Author': 'Linda Monfardini, Luca Facconi, Fausto Minelli', 'Year': 2019, 'DOI / URL': 'https://doi.org/10.3390/ma12203356',
     'FA (Fly ash)': 1.0, WG: R(119 / 472), 'NaOH / B': R(48 / 472), 'NaOH molarity (M)': 8, 'Activator modulus Ms (SiO2/Na2O)': 1.99,
     'Extra water / B': R(35 / 472), 'Mixing liquid / B': 0.43, 'Sand (type not stated) / B': R(615 / 472), 'Sand max size (µm)': 4000,
     'Coarse aggregate / B': R(1141 / 472), 'Binder content (kg/m³)': 472,
     'Curing method': '2 d in moulds, demoulded, wrapped in PE sheet, climate chamber heated up to 60 °C and held 24 h, then stored at 15-25 °C to 28 d',
     'Curing temperature (°C)': 60, 'Heat curing duration (h)': 24, 'Demolding age (days)': 2, 'Test age (days)': 28,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '100x100x100',
     'Tensile specimen': 'notched prism 150x150x500 (EN 14651)', 'Tensile test type': 'flexural',
     'Source table/page': 'Sect. 2.2 (mix), Table 1 (fibre), Table 3 (Rcm, fcm, fL, fR)'}
for mid, typ, rcm, fcm, fl, frs in [('SFRAAC-1', 'S', 45.0, 27.0, 3.6, '3.3/3.2/2.9/2.6'), ('SFRAAC-2', 'S', 34.0, 24.0, 3.9, '3.3/3.3/3.0/2.7'),
                                    ('PFRAAC-1', 'P', 40.0, 24.0, 3.8, '0.7/0.7/0.8/0.8'), ('PFRAAC-2', 'P', 36.0, 24.0, 3.6, '0.9/0.9/1.0/1.0')]:
    kw = {'Total fiber (vol%)': 0.3}
    if typ == 'S':
        kw.update({'Steel fiber (vol%)': 0.3, 'Steel length (mm)': 30, 'Steel diameter (µm)': 350, 'Steel tensile strength (MPa)': 2200})
    add(P, **kw, **{'Compressive strength (MPa)': rcm, 'Tensile strength (MPa)': fl, 'Conversions / notes': (
        f"{mid} material (companion specimens of beam {mid}). Mix kg/m3: class F FA 472, 8 M NaOH 48, Na-silicate 119, extra water 35, sand 0-4 mm 615, "
        f"coarse 4-10 mm 1141; liquid/FA 0.43, alkaline solution/FA 0.35, SS/SH 2.5, activator SiO2/Na2O 1.99. "
        f"{'Hooked-end steel 30 mm/0.35 mm, 2200 MPa, 25 kg/m3 = 0.3 vol%.' if typ == 'S' else 'Synthetic embossed macro-fibre 54 mm/0.80 mm, 585 MPa, 3 kg/m3 = 0.3 vol% (polymer type not stated -> only Total fiber filled).'} "
        f"fc = mean cube strength Rcm; cylinder fcm (100x200) = {fcm} MPa. Tensile = limit of proportionality fL (notched 3-point bending, EN 14651); "
        f"residual fR1-4 = {frs} MPa. Beam -1/-2 are separate castings of the same mix.")})

# =====================================================================================
# P11 Li et al. 2022, Materials 15:3958 - HMGC (MK + quartz powder + steel fibre), curing temperature
P = {'Article Name': 'Effect of Curing Temperature on High-Strength Metakaolin-Based Geopolymer Composite (HMGC) with Quartz Powder and Steel Fibers',
     'Author': 'Qiang Li, Shikun Chen, Yajun Zhang, Yunjin Hu, Quanlin Wang, Quan Zhou, Yongmao Yan, Yi Liu, Dongming Yan', 'Year': 2022,
     'DOI / URL': 'https://doi.org/10.3390/ma15113958', 'Metakaolin': 1.0, WG: R(590.4 / 450), 'NaOH / B': R(94.9 / 450),
     'Na2O / B': R((0.082 * 590.4 + 0.96 * 94.9 * 62 / 80) / 450), 'Activator modulus Ms (SiO2/Na2O)': R(0.26 * 590.4 / (0.082 * 590.4 + 0.96 * 94.9 * 62 / 80), 2),
     'W / B': R((1 - 0.26 - 0.082) * 590.4 / 450, 3), 'QP / B (Quartz powder)': 1.5,
     'Steel fiber (vol%)': 1.5, 'Steel length (mm)': 15, 'Steel diameter (µm)': 200, 'Steel tensile strength (MPa)': 2850,
     'Steel elastic modulus (GPa)': 200, 'Demolding age (days)': R(5 / 24, 3),
     'Compressive specimen': 'prism halves', 'Compressive specimen size (mm)': '40x40 (from 40x40x160 prisms)',
     'Tensile specimen': 'prism 40x40x160 (GB/T 17671)', 'Source table/page': 'Table 4 (mix No. 4), Table 2 (fibre), Sect. 3.4-3.5 text'}
for T, age, fc, fl in [(20, 1, 54.3, 9.97), (60, 1, 71.9, 12.5), (60, 7, None, 21.7), (90, 1, 80.6, 22.3), (90, 3, 97.5, None), (90, 7, None, 18.19)]:
    cm = ('5 h in curing room (20±2 °C, >90% RH), demoulded, kept in curing room until test' if T == 20 else
          f'5 h in curing room, demoulded, sealed box (>90% RH) in oven at {T} °C until test')
    kw = {'Curing method': cm, 'Curing temperature (°C)': T, 'Curing RH (%)': 90, 'Test age (days)': age, 'Curing time (days)': age}
    if T != 20:
        kw['Heat curing duration (h)'] = age * 24 - 5
    if fc is not None:
        kw['Compressive strength (MPa)'] = fc
    if fl is not None:
        kw.update({'Tensile strength (MPa)': fl, 'Tensile test type': 'flexural'})
    extra = ' VERIFY: text says 90 °C/3 d fc 97.5 MPa for fibre HMGC "but the same result was obtained with the HMGC without fibers" (ambiguous).' if (T, age) == (90, 3) else ''
    add(P, **kw, **{'Conversions / notes': (
        "HMGC with 1.5 vol% copper-coated steel fibre (Table 4 No. 4, g): water glass 590.4 (26% SiO2, 8.2% Na2O, rest water), NaOH flakes 94.9 (>=96%), "
        "MK 450, quartz powder 675, steel 91.0. Ratios / MK. W/B = water-glass water / MK (no extra water). Na2O/B and Ms computed from activator "
        "composition (NaOH purity 0.96, Na2O = 0.775 NaOH). Heat curing duration = age x 24 h - 5 h pre-curing (continuous oven curing). "
        f"Values from Sect. 3.4-3.5 text (Figs. 5-6).{extra}")})

# =====================================================================================
# P12 Zhang, Chen, Xia 2022, Materials 16:181 - slag/MK/SF UHPGC with steel fibre
P = {'Article Name': 'Compressive Strength and Chloride Resistance of Slag/Metakaolin-Based Ultra-High-Performance Geopolymer Concrete',
     'Author': 'Yufei Zhang, Jiejing Chen, Jin Xia', 'Year': 2022, 'DOI / URL': 'https://doi.org/10.3390/ma16010181',
     'GGBS': R(641 / 1069), 'Metakaolin': R(321 / 1069), 'SF (Silica fume)': R(107 / 1069), WG: R(279 / 1069),
     'River sand / B': R(388 / 1069), 'Sand max size (µm)': 2360, 'Binder content (kg/m³)': 1069,
     'Steel length (mm)': 14, 'Steel diameter (µm)': 200, 'Steel tensile strength (MPa)': 2880,
     'Curing method': 'covered with plastic film, demoulded after 24 h, laboratory curing 20±2 °C, 72±3% RH',
     'Curing temperature (°C)': 20, 'Curing RH (%)': 72, 'Demolding age (days)': 1,
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '70.7x70.7x70.7',
     'Source table/page': 'Table 2 (mix), Table 3 (fc)'}
for M, vf, fc in [(4, 1, 93.4), (4, 2, 99.8), (8, 1, 105.9), (8, 2, 125.6), (12, 1, 130.6), (12, 2, 136.3)]:
    add(P, **{'NaOH molarity (M)': M, 'Steel fiber (vol%)': vf, 'Compressive strength (MPa)': fc, 'Conversions / notes': (
        f"Mix M{M}-{vf}%. Table 2 kg/m3: slag 641, MK 321, SF 107, river sand 388, waterglass 279 (modulus 2.23); NaOH solution ({M} mol/L) mixed with "
        f"an EQUAL VOLUME of sodium silicate - its mass not given, so NaOH/B and W/B left empty. VERIFY: test age not stated in the paper "
        f"(cured in laboratory conditions until testing). Copper-plated steel fibre 14 mm/0.2 mm, 2880 MPa.")})

# =====================================================================================
# P13 Xiong et al. 2025, Materials 18:3572 - K-silicate FA/MK geopolymer, wollastonite + steel fibre
P = {'Article Name': 'Residual Flexural Behavior of Hybrid Fiber-Reinforced Geopolymer After High Temperature Exposure',
     'Author': 'Yiyang Xiong, Ruiwen Jiang, Yi Li, Peipeng Li', 'Year': 2025, 'DOI / URL': 'https://doi.org/10.3390/ma18153572',
     'FA (Fly ash)': 0.7, 'Metakaolin': 0.3, WG: R(252.4 / 652.6), 'Activator modulus Ms (SiO2/Na2O)': 1.0,
     'W / B': R(((1 - 0.4909) * 252.4 + 99.9) / 652.6, 3), 'Extra water / B': R(99.9 / 652.6),
     'Sand (type not stated) / B': R(1762 / 652.6), 'Binder content (kg/m³)': 652.6,
     'Steel length (mm)': 13, 'Steel diameter (µm)': 200,
     'Curing method': 'covered with plastic film 24 h, demoulded, 20±2 °C, RH >=95% for 28 d; tested at ambient (20 °C, unheated)',
     'Curing time (days)': 28, 'Curing temperature (°C)': 20, 'Curing RH (%)': 95, 'Demolding age (days)': 1, 'Test age (days)': 28,
     'Tensile specimen': 'prism 40x40x160 (3-point bending)', 'Tensile test type': 'flexural',
     'Source table/page': 'Table 2 (mix), Sect. 3.2 text (flexural at 20 °C)'}
for mid, vf, sf, fl in [('W5S1', 1, 78.5, 16.1), ('W5S2', 2, 157, 28.3)]:
    add(P, **{'Steel fiber (vol%)': vf, 'Tensile strength (MPa)': fl, 'Conversions / notes': (
        f"Mix {mid}. Table 2 kg/m3: FA 456.8, MK 195.8, corundum aggregate 1762 (entered as sand-type-not-stated), potassium water glass 252.4 "
        f"(49.09 wt% K2O·SiO2, modulus 1.0 - K-based activator in WG column), tap water 99.9, wollastonite micro-fibre 32.6 (5% of precursors; no column), "
        f"steel {sf} kg/m3 = {vf} vol%. W/B = (water-glass water 50.91% + tap water)/B. Ambient (unheated, 20 °C) flexural value from text; "
        f"residual values after 200-1000 °C exposure not entered.")})

# =====================================================================================
df = pd.DataFrame(rows)
df = df.reindex(columns=hdr)
out = os.path.join(D, 'w2_alkali.csv')
df.to_csv(out, index=False, encoding='utf-8-sig')
print('rows', len(df), 'papers', df['DOI / URL'].nunique())
