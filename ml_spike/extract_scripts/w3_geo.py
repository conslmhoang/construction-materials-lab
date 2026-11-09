# -*- coding: utf-8 -*-
"""Builder for w3_geo.csv - geopolymer / alkali-activated fibre mortars & composites (wave 3).
Full texts read as text: Europe PMC fullTextXML (PMC papers) and Frontiers HTML (fmats papers).
Ratios = kg/m3 / binder kg/m3 unless stated otherwise in the notes.
"""
import csv, os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'additions')
hdr = next(csv.reader(open(os.path.join(D, 'TEMPLATE.csv'), encoding='utf-8-sig')))
rows = []
FIBS = ['PE fiber (vol%)', 'PVA fiber (vol%)', 'Steel fiber (vol%)', 'PP fiber (vol%)', 'PBO fiber (vol%)',
        'Glass fiber (vol%)', 'PET fiber (vol%)', 'Basalt fiber (vol%)', 'Carbon fiber (vol%)']
WG = 'WG / B (Water glass)'


def add(base, **kw):
    r = dict(base)
    r.update(kw)
    for k in r:
        assert k in hdr, k
    if 'Total fiber (vol%)' not in r:
        r['Total fiber (vol%)'] = round(sum(float(r.get(k) or 0) for k in FIBS), 4)
    rows.append(r)


def R(x, n=4):
    return round(x, n)


# =====================================================================================
# P1 Abousnina et al. 2021, Polymers 13:3008 - short fibres in FA geopolymer mortar with oil-contaminated sand
P = {'Article Name': 'Effect of Short Fibres in the Mechanical Properties of Geopolymer Mortar Containing Oil-Contaminated Sand',
     'Author': 'Rajab Abousnina, Haifa Ibrahim Alsalmi, Allan Manalo, Rochstad Lim Allister, Omar Alajarmeh, Wahid Ferdous, Khouloud Jlassi, Luciano Feo',
     'Year': 2021, 'DOI / URL': 'https://doi.org/10.3390/polym13173008',
     'FA (Fly ash)': 1.0, 'Mixing liquid / B': 0.5, 'NaOH molarity (M)': 10, 'Fine sand / B': 3.0,
     'Curing method': 'sealed plastic moulds, oven 60 °C for 24 h, then ambient laboratory condition until test',
     'Curing temperature (°C)': 60, 'Heat curing duration (h)': 24, 'Test age (days)': 28,
     'Compressive specimen': 'cylinder', 'Compressive specimen size (mm)': '50x100',
     'Tensile specimen': 'cylinder 50x100 (splitting)', 'Tensile test type': 'splitting'}
N1 = ("Mix design (Sect. 2.6, AS 2350.12): fly ash : sand : alkaline solution = 1 : 3 : 0.5 by mass (class F FA). Sand = fine sand "
      "(Libyan-desert-like grading) pre-mixed with 6% light crude oil by weight of sand (oil/B ~0.18, not a column). Alkaline liquid = 10 M NaOH "
      "solution + sodium silicate solution (Na2SiO3:NaOH split not reported -> only Mixing liquid / B = 0.5). Fibre dosages are vol% of mortar "
      "(paper). ")
FIB1 = {'straight PP': {'PP fiber (vol%)': None, 'PP length (mm)': 45, 'PP diameter (µm)': 800},
        'twisted PP': {'PP fiber (vol%)': None, 'PP length (mm)': 38, 'PP diameter (µm)': 800},
        'short glass': {'Glass fiber (vol%)': None},
        'steel': {'Steel fiber (vol%)': None, 'Steel length (mm)': 35, 'Steel diameter (µm)': 1000,
                  'Steel tensile strength (MPa)': 1300}}
FCOL1 = {'straight PP': 'PP fiber (vol%)', 'twisted PP': 'PP fiber (vol%)', 'short glass': 'Glass fiber (vol%)',
         'steel': 'Steel fiber (vol%)'}
DESC1 = {'straight PP': 'straight monofilament PP 45 mm / ~0.8 mm, SG 0.91, 750-850 MPa',
         'twisted PP': 'twisted-bundle PP 38 mm / ~0.8 mm, SG 0.91, 570-660 MPa',
         'short glass': 'short glass fibre 19 mm, SG 2.55 (VERIFY: Table 3 lists its material as "virgin homopolymer polypropylene" '
                        'although SG 2.55 indicates glass; entered as Glass)',
         'steel': 'hooked-end low-carbon steel 35 mm / 1 mm, SG 7.93, 1250-1350 MPa (1300 = mid-range entered)'}
# Stage 1: 0.1 vol% of each fibre type + control (Tables 6, 7)
for ft, fc, st in [('control', 11.6, 0.6), ('twisted PP', 19.0, 1.5), ('short glass', 12.1, 1.6), ('steel', 14.5, 1.6)]:
    if ft == 'control':
        add(P, **{'Compressive strength (MPa)': fc, 'Tensile strength (MPa)': st,
                  'Source table/page': 'Sect. 2.6 (mix), Table 6 (fc), Table 7 (splitting)',
                  'Conversions / notes': N1 + "Control (no fibre). Splitting 0.6 MPa from Table 7 (Table 10 lists 0.7 MPa for 0% fibre)."})
    else:
        f = dict(FIB1[ft]); f[FCOL1[ft]] = 0.1
        add(P, **f, **{'Compressive strength (MPa)': fc, 'Tensile strength (MPa)': st,
                       'Source table/page': 'Sect. 2.6 (mix), Table 3 (fibre), Table 6 (fc), Table 7 (splitting)',
                       'Conversions / notes': N1 + f"Stage 1: 0.1 vol% {DESC1[ft]}."})
# Stage 2: straight PP 0.1-0.5 vol% (Tables 8, 9). Stage-1 straight PP 0.1% gave fc 17.3 / ft 2.3 (other batch).
for vf, fc, st in [(0.1, 19.1, 2.3), (0.2, 24.4, 2.9), (0.3, 25.0, 2.8), (0.4, 31.1, 4.1), (0.5, 32.2, 5.4)]:
    f = dict(FIB1['straight PP']); f['PP fiber (vol%)'] = vf
    add(P, **f, **{'Compressive strength (MPa)': fc, 'Tensile strength (MPa)': st,
                   'Source table/page': 'Sect. 2.6 (mix), Table 5 (dosage), Table 8 (fc), Table 9 (splitting)',
                   'Conversions / notes': N1 + f"Stage 2: {vf} vol% {DESC1['straight PP']}. Paper's kg/m3 column (Tables 5/8) is "
                                               f"inconsistent with vol% (e.g. 0.2% listed as 15.86 kg/m3); vol% used."
                                               + (" Stage-1 replicate of this mix (Table 6/7): fc 17.3, splitting 2.3 MPa." if vf == 0.1 else "")})

# =====================================================================================
# P2 Briki et al. 2026, Sci Rep - slag geopolymer mortar with PP (and treated date-palm) fibres
P = {'Article Name': 'Performance of geopolymer composites reinforced with treated date palm and polypropylene fibers',
     'Author': 'Leila Briki, Oussama Kessal, Ahmed Abderraouf Belkadi, Eyad Alsuhaibani, Abdellah Douadi, S. O. Bamaga',
     'Year': 2026, 'DOI / URL': 'https://doi.org/10.1038/s41598-026-50457-7',
     'GGBS': 1.0, 'Binder content (kg/m³)': 580, WG: R(326 / 580), 'NaOH / B': R(108 / 580), 'NaOH molarity (M)': 10,
     'Mixing liquid / B': 0.75, 'Dune sand / B': R(429 / 580), 'M-sand / B': R(859 / 580),
     'Compressive specimen': 'cube', 'Compressive specimen size (mm)': '30x30x30',
     'Tensile specimen': 'prism 40x40x160 (3-point bending)', 'Tensile test type': 'flexural'}
N2 = ("Table 3 kg/m3: slag 580, dune sand 429, crushed sand 859 (M-sand column), NaOH 108 (10 M SOLUTION mass), sodium silicate 326 "
      "(solution, SiO2/Na2O modulus 2.6, 40% concentration), activator/binder 0.75. Ratios = kg/m3 / 580. Curing regime only shown in Fig. 8 "
      "(not described in text) -> left empty. Date-palm-fibre mixes (MDP1-6) not entered (no column for natural fibres). ")
D2 = [('MC (control)', None, None, None, [(7, 24.05, 4.25), (14, 28.43, 5.80), (28, 33.56, 6.69), (90, 38.23, 7.09)]),
      ('MPP1', 0.15, 6, 1.3, [(7, 26.44, 4.45), (14, 32.06, 5.10), (28, 37.41, 7.51), (90, 38.73, 7.87)]),
      ('MPP2', 0.30, 6, 2.7, [(7, 26.68, 4.35), (14, 31.26, 5.94), (28, 38.32, 7.62), (90, 43.02, 8.09)]),
      ('MPP3', 0.15, 12, 1.3, [(7, 26.93, 4.58), (14, 30.80, 6.22), (28, 32.04, 7.91), (90, 37.96, 8.24)]),
      ('MPP4', 0.30, 12, 2.7, [(7, 28.52, 4.75), (14, 30.90, 6.31), (28, 37.46, 8.61), (90, 38.28, 8.56)])]
for mid, vf, L, kg, res in D2:
    f = {} if vf is None else {'PP fiber (vol%)': vf, 'PP length (mm)': L, 'PP diameter (µm)': 31}
    for age, fc, fl in res:
        add(P, **f, **{'Test age (days)': age, 'Compressive strength (MPa)': fc, 'Tensile strength (MPa)': fl,
                       'Source table/page': 'Table 3 (mix), Table 2 (fibre), Table 4 (fc), Table 5 (flexural)',
                       'Conversions / notes': N2 + (f"Mix {mid}: PP {vf} vol% ({kg} kg/m3), {L} mm, 30-32 µm, density 0.91, "
                                                    f"427-548 MPa." if vf else f"Mix {mid}: no fibre.")})

# =====================================================================================
# P3 Huang et al. 2026, Frontiers in Materials - ultra-high-strength GGBFS/FA/SF geopolymer mortar with steel fibres
P = {'Article Name': 'Ultra-high-strength geopolymer concrete influenced by mixture proportion and steel fiber: flowability, compressive strength, and flexural performance',
     'Author': 'Haonan Huang, Liu Yang, Wen Jiang, Yu Chen, Xianghua Hou',
     'Year': 2026, 'DOI / URL': 'https://doi.org/10.3389/fmats.2026.1781306',
     'Binder content (kg/m³)': 1056, 'NaOH / B': R(33.8 / 1056), WG: R(501.9 / 1056), 'Extra water / B': R(26.7 / 1056),
     'Na2O / B': 0.07, 'Activator modulus Ms (SiO2/Na2O)': 2.0, 'W / B': 0.335, 'Sand (type not stated) / B': 1.0,
     'Demolding age (days)': 1,
     'Compressive specimen': 'prism halves', 'Compressive specimen size (mm)': '40x40x40 (from 40x40x160 prisms)',
     'Tensile specimen': 'prism 40x40x160 (3-point bending, span 100 mm)', 'Tensile test type': 'flexural'}
N3 = ("Table 2 kg/m3: B = GGBFS + FA + SF = 1056; sand 1056 (SSD, type not stated); NaOH pellets 33.8 (solid); sodium silicate solution 501.9 "
      "(8.3% Na2O, 26.5% SiO2, 65.2% H2O); added water 26.7. Activator Na2O = 7% of B, Ms 2.0; effective W/B 0.335 (paper, incl. silicate water). "
      "Ratios = kg/m3 / 1056. Steel fibre 156 kg/m3 = 2 vol% (paper). No coarse aggregate despite the word 'concrete' in title. ")
FIB3 = {'Z': {'Steel length (mm)': 13, 'Steel diameter (µm)': 120, 'Steel tensile strength (MPa)': 2500},
        'S': {'Steel length (mm)': 13, 'Steel diameter (µm)': 220, 'Steel tensile strength (MPa)': 2500},
        'D': {'Steel length (mm)': 13, 'Steel diameter (µm)': 220, 'Steel tensile strength (MPa)': 2500}}
FDESC = {'Z': 'straight 13 mm / 0.12 mm', 'S': 'straight 13 mm / 0.22 mm', 'D': 'hooked-end 13 mm / 0.22 mm'}
BIN = {'A': (845, 211), 'B': (528, 528), 'C': (211, 845)}
SFk = {0: 0, 1: 53, 2: 106, 3: 211, 4: 317}
# (mix, fibre, steam fc, steam flex, std fc, std flex)
D3 = [('A0', None, 98.8, 5.4, None, None), ('A1', None, 110.7, 3.9, None, None), ('A2', None, 115.9, 2.7, None, None),
      ('A3', None, 80.9, 3.7, None, None), ('A4', None, 93.3, 5.3, None, None),
      ('ZA0', 'Z', 156.5, 14.2, 132.6, 14.5), ('ZA1', 'Z', 157.0, 11.6, 133.9, 11.9), ('ZA2', 'Z', 130.6, 7.2, 102.1, 9.0),
      ('ZA3', 'Z', 126.7, 10.3, None, None), ('ZA4', 'Z', 127.8, 11.4, None, None),
      ('DA0', 'D', 154.3, 10.6, 126.4, 9.8), ('SA0', 'S', 152.6, 7.6, 117.9, 6.4),
      ('B0', None, 77.4, 3.4, None, None), ('B1', None, 67.4, 2.6, None, None), ('B2', None, 61.9, 2.3, None, None),
      ('B3', None, 67.6, 2.6, None, None), ('B4', None, 77.2, 5.6, None, None), ('ZB0', 'Z', 134.2, 12.3, None, None),
      ('C0', None, 39.0, 1.4, None, None), ('C1', None, 25.7, 1.4, None, None), ('C2', None, 25.9, 1.5, None, None),
      ('C3', None, 34.0, 3.1, None, None), ('C4', None, 42.5, 4.5, None, None), ('ZC0', 'Z', 38.2, 2.9, None, None)]
for mid, fib, sfc, sfl, cfc, cfl in D3:
    grp = mid[-2]
    k = int(mid[-1])
    g0, f0 = BIN[grp]
    sf = SFk[k]
    scale = (1056 - sf) / 1056
    gg, fa = (g0 * scale, f0 * scale)
    bnd = {'GGBS': R(gg / 1056), 'FA (Fly ash)': R(fa / 1056), 'SF (Silica fume)': R(sf / 1056)}
    f = {} if fib is None else dict(FIB3[fib], **{'Steel fiber (vol%)': 2.0})
    base_note = N3 + (f"Mix {mid}: GGBFS/FA {'4:1' if grp == 'A' else '1:1' if grp == 'B' else '1:4'}, SF {sf} kg/m3 "
                      f"(binder fractions from Table 2 kg/m3, rounded). "
                      + (f"Steel fibre {fib} = {FDESC[fib]}, >2500 MPa (entered 2500). " if fib else "No fibre. "))
    cur = {'steam': {'Curing method': 'sealed in mould 24 h at 20 °C / 65% RH, demoulded, steam curing 80 °C for 24 h',
                     'Curing temperature (°C)': 80, 'Heat curing duration (h)': 24},
           'std': {'Curing method': 'sealed in mould 24 h at 20 °C / 65% RH, demoulded, standard curing 20 °C, RH > 90% to 28 d',
                   'Curing temperature (°C)': 20, 'Curing RH (%)': 90, 'Curing time (days)': 28, 'Test age (days)': 28}}
    add(P, **bnd, **f, **cur['steam'], **{'Compressive strength (MPa)': sfc, 'Tensile strength (MPa)': sfl,
                                          'Source table/page': 'Table 2 (mix), Sect. 2.1 (fibres), Table 3 (fc, flexural)',
                                          'Conversions / notes': base_note + "Steam-cured; VERIFY: test age after steam curing not stated (left empty)."})
    if cfc is not None:
        add(P, **bnd, **f, **cur['std'], **{'Compressive strength (MPa)': cfc, 'Tensile strength (MPa)': cfl,
                                            'Source table/page': 'Table 2 (mix), Sect. 2.1 (fibres), Table 3 (fc, flexural)',
                                            'Conversions / notes': base_note + "28 d standard curing."})

# =====================================================================================
# P4 Batista et al. 2019, Frontiers in Materials 6:77 - MK/SF alkali-activated mortar with 2 vol% PVA (direct tension)
P = {'Article Name': 'Silica Fume as Precursor in the Development of Sustainable and High-Performance MK-Based Alkali-Activated Materials Reinforced With Short PVA Fibers',
     'Author': 'Raquel P. Batista, Ana Carolina C. Trindade, Paulo H. R. Borges, Flávio de A. Silva',
     'Year': 2019, 'DOI / URL': 'https://doi.org/10.3389/fmats.2019.00077',
     'SS / B (Silica sand)': 1.0, 'Sand max size (µm)': 600,
     'PVA fiber (vol%)': 2.0, 'PVA length (mm)': 8, 'PVA diameter (µm)': 40, 'PVA tensile strength (MPa)': 1600,
     'PVA elastic modulus (GPa)': 41,
     'Curing method': 'cast and kept at ambient temperature (~28 °C); demoulded at 24 h, sealed in plastic bags until 28 d',
     'Curing temperature (°C)': 28, 'Demolding age (days)': 1, 'Test age (days)': 28,
     'Tensile specimen': 'dumbbell, 24x40 mm central section, 250 mm long', 'Tensile gauge length (mm)': 100,
     'Tensile test type': 'direct'}
for mid, mk, sf, sol, ssr, ms in [('3.0 100MK-00SF', 1.0, 0.0, 1.05, 0.66, 1.29), ('3.8 82MK-18SF', 0.82, 0.18, 1.02, 0.48, 1.83)]:
    fcr = 3.78 if mid.startswith('3.0') else 4.22
    add(P, **{'Metakaolin': mk, 'SF (Silica fume)': sf, 'Mixing liquid / B': sol, WG: R(sol * ssr),
              'Activator modulus Ms (SiO2/Na2O)': ms, 'First-cracking strength (MPa)': fcr,
              'Source table/page': 'Table 1 (mix), Sect. 2.1 (materials), Table 5 (first-crack strength), Sect. Behavior in Direct Tensile Test',
              'Conversions / notes': (
                  f"Formulation {mid}. Table 1: MK:SF {int(mk * 100)}:{int(sf * 100)}, activating solution/binder {sol} (NaOH solution + "
                  f"sodium silicate [31.79% SiO2, 15.00% Na2O] + extra water; SF pre-dissolved in NaOH solution), sodium silicate/solution "
                  f"mass ratio {ssr} -> WG/B = {sol}x{ssr}. Ms = [SiO2]/[Na2O] of activator ({ms}, includes SF silica for 18SF). "
                  f"Molar Na2O/SiO2 0.26, H2O/Na2O 12.80. Fine quartz sand (<0.6 mm, FM 1.03), aggregate/binder 1. "
                  f"PVA REC15 (Kuraray). First-crack strength sigma_cc from direct tension (Table 5, mean of 4 dumbbells). "
                  f"Ultimate tensile strength not tabulated (curve only, Fig. 10); paper states deformation capacity 0.20-0.30% for the two "
                  f"composites (not per mix -> strain left empty). fc only in Fig. 5 (not extracted).")})

df = pd.DataFrame(rows, columns=hdr)
out = os.path.join(D, 'w3_geo.csv')
df.to_csv(out, index=False, encoding='utf-8-sig')
print(len(df), 'rows,', df['DOI / URL'].nunique(), 'papers ->', out)
