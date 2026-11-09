# Builder for lightweight / rubberised fibre-composite additions (w2_lightweight.csv)
# All numbers transcribed from the papers' full text (Europe PMC fullTextXML). See per-row notes.
import os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
H = list(pd.read_csv(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
assert len(H) == 99
rows = []


def add(base, **kw):
    r = dict(base)
    r.update({k: v for k, v in kw.items() if v is not None})
    for k in r:
        assert k in H, k
    rows.append(r)


R = lambda x, n=4: round(x, n)

# ---------------------------------------------------------------- 1 Wang et al. 2019 (RP + crumb rubber PE-ECC)
b = {"Article Name": "Using Green Supplementary Materials to Achieve More Ductile ECC",
     "Author": "Wang Y., Zhang Z., Yu J., Xiao J., Xu Q.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12060858",
     "OPC / Cement": 0.45, "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 2900,
     "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2, "Curing method": "air, room temperature 20±3°C, RH 40±5% (covered with plastic until demoulding)",
     "Curing time (days)": 27, "Curing temperature (°C)": 20, "Curing RH (%)": 40, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100", "Tensile specimen": "dog-bone (JSCE)",
     "Tensile gauge length (mm)": 80, "Tensile test type": "direct",
     "Source table/page": "Table 1 (fibre), Table 3 (mix), Table 4 (tension)"}
for mid, fa, rp, cr, size, sand, w, ftc, ftu, eps in [
        ("R5040C13", 0.275, 0.275, 0.04, 40, 0.27, 0.35, 2.22, 4.62, 7.37),
        ("R5040C30", 0.275, 0.275, 0.08, 40, 0.23, 0.37, 1.97, 4.24, 7.42),
        ("R5080C13", 0.275, 0.275, 0.04, 80, 0.27, 0.40, 2.12, 6.00, 7.45),
        ("R5080C30", 0.275, 0.275, 0.08, 80, 0.23, 0.36, 1.72, 5.63, 7.68),
        ("R10040C13", 0, 0.55, 0.04, 40, 0.27, 0.34, 2.23, 4.59, 7.71),
        ("R10040C30", 0, 0.55, 0.08, 40, 0.23, 0.37, 1.72, 4.38, 8.55),
        ("R10080C13", 0, 0.55, 0.04, 80, 0.27, 0.39, 1.96, 5.54, 8.81),
        ("R10080C30", 0, 0.55, 0.08, 80, 0.23, 0.34, 2.21, 5.07, 12.26)]:
    add(b, **{"FA (Fly ash)": fa, "Recycled powder (C&D waste)": rp, "Crumb rubber / B": cr, "SS / B (Silica sand)": sand, "W / B": w,
              "First-cracking strength (MPa)": ftc, "Tensile strength (MPa)": ftu, "Tensile strain capacity (%)": eps,
              "Conversions / notes": f"{mid}-ECC: Table 3 gives all constituents as mass ratio to binder (cement 0.45 + FA + recycled C&D powder = 1). "
              f"Crumb rubber {size}-mesh replaces silica sand by mass (sand+CR = 0.31). Water/B as printed ({w}; varies between mixes). "
              "PE fibre 2 vol% (text); Table 3 lists PE 0.015 by mass of binder. HRWR used, dosage not reported. "
              "Compressive strength only in Fig. 11 (not transcribed). First-cracking = initial cracking stress."})

# ---------------------------------------------------------------- 2 Fu et al. 2022 (fly-ash cenosphere PE-ECC)
B = 913 + 391.5
b = {"Article Name": "Green-Engineered Cementitious Composite Production with High-Strength Synthetic Fiber and Aggregate Replacement",
     "Author": "Fu C., Chen M., Guo R., Qi R.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15093047",
     "OPC / Cement": R(913 / B), "FA (Fly ash)": R(391.5 / B), "W / B": R(251.7 / B), "FA cenosphere / B": R(195.8 / B),
     "SP / B": R(101.7 / B), "Binder content (kg/m³)": B, "PE length (mm)": 12, "PE diameter (µm)": 26,
     "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
     "Curing method": "standard curing 20±3°C, RH 95% after demoulding at 1 d", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
     "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
     "Tensile specimen": "dog-bone (Fig. 7a)", "Tensile test type": "direct",
     "Source table/page": "Table 3 (mix), Table 2 (fibre), Sec. 4.2 and 4.4 text (fc, ft, strain)"}
for vf, fc, ft, eps in [(2, 47.5, 7.2, 5.6), (1, 52.8, 5.6, 2.5)]:
    add(b, **{"PE fiber (vol%)": vf, "Total fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Tensile strain capacity (%)": eps,
              "Conversions / notes": f"FAC0.15-PE{vf}: Table 3 kg/m3 cement 913, FA 391.5, FACs 195.8, water 251.7, WR 101.7 (WR value as printed, looks high); "
              "binder = cement+FA = 1304.5. FACs (SG 0.53, 0.01-0.5 mm) used as the fine aggregate. PE diameter derived from length 12 mm / aspect ratio 460. "
              "Test age not stated in paper (left blank). Values from text; other 9 mixes only in Figs. 12-15."})

# ---------------------------------------------------------------- 3 Sun et al. 2022 (EPS concrete + PP/glass/carbon fibres)
B = 508.91 + 127.23
b = {"Article Name": "An Investigation of the Properties of Expanded Polystyrene Concrete with Fibers Based on an Orthogonal Experimental Design",
     "Author": "Sun Y., Li C., You J., Bu C., Yu L., Yan Z., Liu X., Zhang Y., Chen X.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15031228",
     "OPC / Cement": R(508.91 / B), "SF (Silica fume)": R(127.23 / B), "W / B": R(152.67 / B), "River sand / B": R(407.12 / B),
     "SP / B": R(4.07 / B), "EPS / B": R(10 / B), "Binder content (kg/m³)": R(B, 2), "Test age (days)": 28,
     "Curing method": "not stated (tests per GB/T 50081-2019 at 28 d curing age)", "Tensile test type": "splitting",
     "Source table/page": "Table 6 (mix), Table 4 (fibre), Table 7 (fc, splitting, density)"}
for mid, typ, L, vf, fc, ft, rho in [
        ("CC", None, None, 0, 8.58, 0.91, 1036.60), ("P0605", "PP", 6, 0.5, 9.41, 0.88, 1043.71), ("G0905", "GF", 9, 0.5, 9.19, 1.17, 1083.38),
        ("C1205", "CF", 12, 0.5, 12.35, 2.04, 1045.44), ("C0910", "CF", 9, 1.0, 12.16, 2.04, 1151.20), ("G0610", "GF", 6, 1.0, 10.08, 1.23, 1069.16),
        ("P1210", "PP", 12, 1.0, 8.41, 1.30, 1118.93), ("P0915", "PP", 9, 1.5, 7.53, 1.06, 986.42), ("G1215", "GF", 12, 1.5, 6.12, 0.89, 1085.07),
        ("C0615", "CF", 6, 1.5, 8.43, 2.35, 1097.71)]:
    d = {"Total fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft}
    if typ == "PP": d.update({"PP fiber (vol%)": vf, "PP length (mm)": L})
    if typ == "GF": d["Glass fiber (vol%)"] = vf
    if typ == "CF": d["Carbon fiber (vol%)"] = vf
    d["Conversions / notes"] = (f"{mid}: Table 6 kg/m3 cement 508.91, SF 127.23, water 152.67, river sand 407.12 (FM 1.73), SP 4.07, EPS beads 10 "
                                f"(apparent density 25.1 kg/m3); fibre {typ or 'none'} {L or ''} mm at {vf}% (fibre kg/m3 in Table 6 consistent with vol% and Table 4 densities). "
                                f"Dry density {rho} kg/m3. Specimen sizes not stated. Splitting tensile strength.")
    add(b, **d)

# ---------------------------------------------------------------- 4 Chen & Huang 2019 (cenosphere PVA LTCC)
b = {"Article Name": "Experimental Study of the Mechanical Properties and Microstructures of Lightweight Toughness Cement-Based Composites",
     "Author": "Chen W., Huang Z.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12233891",
     "W / B": 0.32, "SP / B": 0.002, "PVA fiber (vol%)": 1, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
     "Total fiber (vol%)": 1, "Curing method": "demoulded after 24 h at room temperature, then 20°C, RH 95%", "Curing temperature (°C)": 20,
     "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Curing time (days)": 27,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile specimen": "dog-bone (13x30 mm section)",
     "Tensile gauge length (mm)": 80, "Tensile test type": "direct",
     "Source table/page": "Table 2 (mix), Table 3 (fc), Table 4 (tension)"}
for mid, cs, fc, ft, fcr, eps, rho in [("S-0", 0, 58.87, 1.64, 1.10, 0.40, 1.870), ("C-1", 0.1, 56.35, 2.56, 2.25, 0.50, 1.724),
                                       ("C-2", 0.2, 53.86, 2.00, 1.83, 0.61, 1.592), ("C-3", 0.3, 50.06, 1.88, 1.56, 0.25, 1.477)]:
    add(b, **{"FA cenosphere / B": cs, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr,
              "Tensile strain capacity (%)": eps,
              "Conversions / notes": f"{mid}: Table 2 weight ratios to cementitious binder (= Type II 52.5R cement + silica fume; cement:SF split NOT reported, "
              "so binder-composition columns left blank). Cenosphere (45-300 µm) {cs}; polycarboxylate powder 0.002; SRA 0.002 (no column); "
              f"CSA expansive agent 0.05 of binder (no column). PVA Kuralon K-II REC15 (paper prints diameter '39 mm', taken as 39 µm). Density {rho} g/cm3. Flexural/4-pt bending in Tables 3-4."})

# ---------------------------------------------------------------- 5 Liang et al. 2025 (basalt fibre EPS geopolymer)
B = 348.8 * 2
wg, naoh, w = 216.9, 45.2, 118
b = {"Article Name": "Multi-Performance Evolution and Elasto-Plastic Damage Modeling of Basalt Fiber-Reinforced EPS Geopolymer Lightweight Concrete",
     "Author": "Liang F., Yang Q., Tao J.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/polym17182471",
     "GGBS": 0.5, "FA (Fly ash)": 0.5, "WG / B (Water glass)": R(wg / B), "NaOH / B": R(naoh / B),
     "Na2O / B": R((naoh * 62 / 80 + wg * 0.0854) / B), "Activator modulus Ms (SiO2/Na2O)": R(wg * 0.273 / (naoh * 62 / 80 + wg * 0.0854), 3),
     "W / B": R((w + wg * 0.6416) / B), "Extra water / B": R(w / B), "SP / B": R(10.5 / B), "Binder content (kg/m³)": B,
     "Curing method": "demoulded after 24 h at room temperature, then curing chamber 22±2°C, RH 50±5% for 28 d", "Curing time (days)": 28,
     "Curing temperature (°C)": 22, "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "prism (40x40x160, halves)", "Compressive specimen size (mm)": "40x40x160",
     "Tensile specimen": "cylinder 50x100", "Tensile test type": "splitting",
     "Source table/page": "Table 4 (mix), Table 3 (sodium silicate), Sec. 5 text (fc, splitting, flexural)"}
for mid, sand, eps_kg, bf, fc, ft, note in [
        ("GC00BF00", 1011.8, 0, 0, 44.1, None, ""),
        ("LEGC10BF04", 811.8, 1.8, 0.4, None, 3.39, "Flexural 5.63 MPa (text)."),
        ("LEGC10BF06", 811.8, 1.8, 0.6, 40.80, 3.57, "Flexural 6.61 MPa (text)."),
        ("LEGC10BF08", 811.8, 1.8, 0.8, None, 4.78, "Flexural 6.43 MPa (text)."),
        ("LEGC20BF06", 611.8, 3.7, 0.6, 40.87, None, "Text elsewhere says this mix (density 1747.6 kg/m3) has fc 'exceeding 17 MPa'; 40.87 taken from the series values and abstract."),
        ("LEGC20BF08", 611.8, 3.7, 0.8, None, 4.15, ""),
        ("LEGC30BF06", 411.8, 5.5, 0.6, 23.99, None, ""),
        ("LEGC40BF06", 211.8, 7.3, 0.6, 11.94, None, ""),
        ("LEGC40BF08", 211.8, 7.3, 0.8, None, 2.62, "")]:
    add(b, **{"Sand (type not stated) / B": R(sand / B), "EPS / B": R(eps_kg / B, 5), "Basalt fiber (vol%)": bf, "Total fiber (vol%)": bf,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Conversions / notes": f"{mid}: Table 4 kg/m3 slag 348.8, FA 348.8, NaOH pellets 45.2, Na2SiO3 solution 216.9 (8.54% Na2O, 27.30% SiO2, 64.16% H2O, Ms 3.30), "
              f"sand {sand} (uniformly graded river sand), water 118, EPS {eps_kg} kg ({mid[4:6] if mid != 'GC00BF00' else '0'} vol%, 2-4 mm, 16 kg/m3), basalt fibre 9 mm, SP 10.5. "
              "W/B = (118 + water in silicate)/binder; Na2O/B and blended Ms computed from NaOH (Na2O = 62/80 of NaOH) and silicate composition. "
              "Text says fc series at 'basalt fiber content fixed at 6%' (read as 0.6%). Other mixes only in Figs. 11-16. " + note})

# ---------------------------------------------------------------- 6 Loganathan & Mohammed 2021 (rubberised PVA-ECC with nano-silica, RSM)
b = {"Article Name": "Properties of Rubberized Engineered Cementitious Composites Containing Nano-Silica",
     "Author": "Loganathan R., Mohammed B.S.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14133765",
     "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 41,
     "Curing method": "24 h in mould (curing room), then water tank 23°C", "Curing time (days)": 27, "Curing temperature (°C)": 23,
     "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
     "Tensile specimen": "dog-bone (Rokugo/JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": "direct",
     "Source table/page": "Table 4 (mix), Table 5 (fc, direct tensile)"}
mix = {"M1": (260, 0, 210.60, 0, 5.85, 0), "M2": (130, 130, 205.34, 1.89, 5.85, 2.6), "M3": (130, 130, 210.60, 0, 0, 5.2), "M4": (195, 65, 200.07, 3.75, 5.85, 2.6),
       "M5": (195, 65, 205.34, 1.89, 5.85, 2.6), "M6": (260, 0, 210.60, 0, 11.70, 5.2), "M7": (260, 0, 205.34, 1.89, 5.85, 2.6), "M8": (130, 130, 210.60, 0, 11.70, 5.2),
       "M9": (130, 130, 200.07, 3.75, 0, 0), "M10": (195, 65, 210.60, 0, 5.85, 2.6), "M11": (195, 65, 205.34, 1.89, 5.85, 2.6), "M12": (130, 130, 210.60, 0, 0, 0),
       "M13": (195, 65, 205.34, 1.89, 5.85, 2.6), "M14": (260, 0, 210.60, 0, 11.70, 0), "M15": (195, 65, 205.34, 1.89, 5.85, 2.6), "M16": (130, 130, 200.07, 3.75, 11.70, 0),
       "M17": (195, 65, 205.34, 1.89, 5.85, 2.6), "M18": (195, 65, 205.34, 1.89, 5.85, 0), "M19": (130, 130, 200.07, 3.75, 11.70, 5.2), "M20": (195, 65, 205.34, 1.89, 5.85, 2.6),
       "M21": (130, 130, 210.60, 0, 11.70, 0), "M22": (195, 65, 205.34, 1.89, 11.70, 2.6), "M23": (195, 65, 205.34, 1.89, 5.85, 5.2), "M24": (260, 0, 200.07, 3.75, 0, 0),
       "M25": (130, 130, 200.07, 3.75, 0, 5.2), "M26": (260, 0, 200.07, 3.75, 0, 5.2), "M27": (260, 0, 210.60, 0, 0, 5.2), "M28": (260, 0, 200.07, 3.75, 11.70, 5.2),
       "M29": (195, 65, 205.34, 1.89, 0, 2.6), "M30": (260, 0, 200.07, 3.75, 11.70, 0)}
res = {"M1": (87.17, 2.63), "M2": (57.11, 2.82), "M3": (69.91, 3.13), "M4": (48.17, 2.58), "M5": (64.29, 2.70), "M6": (82.44, 3.40), "M7": (65.05, 2.76),
       "M8": (83.42, 3.36), "M9": (52.44, 2.91), "M10": (83.57, 2.73), "M11": (65.22, 2.91), "M12": (83.80, 3.74), "M13": (60.45, 2.82), "M14": (86.81, 2.59),
       "M15": (63.07, 2.50), "M16": (44.96, 3.81), "M17": (68.45, 2.72), "M18": (67.63, 2.62), "M19": (54.86, 3.81), "M20": (59.10, 2.89), "M21": (80.36, 2.99),
       "M22": (85.68, 2.97), "M23": (48.69, 2.97), "M24": (57.66, 2.81), "M25": (48.93, 2.70), "M26": (51.17, 2.39), "M27": (69.55, 2.92), "M28": (59.10, 3.19),
       "M29": (81.63, 3.12), "M30": (48.09, 3.55)}
for m, (opc, fa, sand, cr, pva, ns) in mix.items():
    B = opc + fa + ns
    fc, ft = res[m]
    add(b, **{"OPC / Cement": R(opc / B), "FA (Fly ash)": R(fa / B), "Nano-SiO2": R(ns / B), "W / B": R(39 / B),
              "Sand (type not stated) / B": R(sand / B), "Crumb rubber / B": R(cr / B, 5), "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Conversions / notes": f"{m}: Table 4 quantities OPC {opc}, FA {fa}, fine aggregate {sand}, CR {cr}, PVA {pva}, nano-silica {ns}, water 39 "
              "(labelled kg/m3 but sum ~520 kg, i.e. batch quantities; only ratios used). Binder here = OPC+FA+nano-silica; w/cm 0.15 of OPC+FA. "
              "CR replaces fine aggregate by volume at 0/2.5/5%. PVA fibre content NOT filled: design factor stated as 0/1/2% 'by weight of cementitious', "
              f"but Table 4 gives PVA {pva} per 260 cementitious ({pva/260*100:.2f}% by mass) and the kg/m3 basis is not real, so vol% cannot be derived reliably. "
              "SP used, dose not reported. Centre-point replicates (M5, M11, M13, M15, M17, M20) are separate batches of the same mix."})

# ---------------------------------------------------------------- 7 Huang et al. 2018 (floatable HGM PE composite)
b = {"Article Name": "A Novel, Multifunctional, Floatable, Lightweight Cement Composite: Development and Properties",
     "Author": "Huang Z., Wang F., Zhou Y., Sui L., Krishnan P., Liew J.Y.R.", "Year": 2018, "DOI / URL": "https://doi.org/10.3390/ma11102043",
     "OPC / Cement": 0.85, "SF (Silica fume)": 0.15, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116,
     "Curing method": "moist curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "50 (Table 6 lists 50 and 40 mm cubes)",
     "Tensile specimen": "prism 40x40x160 (3-point bending, BS EN 196-1)", "Tensile test type": "flexural",
     "Source table/page": "Table 5 (mix), Table 4 (microspheres), Table 7 (fc, flexural)"}
for mid, gm, wb, hgm, sp, vf, fc, ff, rho in [
        ("FL40", "GM40", 0.60, 0.56, 0.02, 0, 41.0, 3.5, 970), ("FL46", "GM46", 0.60, 0.59, 0.02, 0, 39.5, 3.2, 940),
        ("FL60", "GM60", 0.60, 0.66, 0.02, 0, 31.1, 2.2, 890), ("FL46-35", "GM46", 0.35, 0.59, 0.05, 0, 32.1, 2.7, 880),
        ("FL46PE05", "GM46", 0.65, 0.59, 0.02, 0.5, 26.9, 4.0, 940), ("FL46PE10", "GM46", 0.65, 0.59, 0.04, 1.0, 27.3, 7.2, 940),
        ("FL46PE15", "GM46", 0.65, 0.59, 0.05, 1.5, 31.0, 9.5, 930)]:
    add(b, **{"W / B": wb, "HGM / B (Hollow glass microsphere)": hgm, "SP / B": sp, "PE fiber (vol%)": vf if vf else None, "Total fiber (vol%)": vf,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
              "Conversions / notes": f"{mid}: Table 5 C 0.85, SF 0.15, W/B {wb}, {gm} glass microspheres/B {hgm}, SP/B {sp}, PE {vf}%. "
              "Table 5 header reads 'by Volume of Total Binder' but text says microspheres used at a 'mass ratio of 0.6' and a mass basis reproduces the "
              f"~940 kg/m3 fresh density, so ratios taken as mass ratios (VERIFY). Fresh density {rho} kg/m3. Tensile value = 3-point FLEXURAL strength; "
              "direct tension (PE 1-1.5%) only described as strain >3%, up to 5-6% (Fig. 9) - not transcribed. PE aspect ratio 720, length not stated."})

# ---------------------------------------------------------------- 8 Huo & Zhang 2022 (steel fibre EPS concrete)
B = 487.2 + 54.1
b = {"Article Name": "Research and Statistical Analysis on Impact Resistance of Steel Fiber Expanded Polystyrene Concrete and Expanded Polystyrene Concrete",
     "Author": "Huo W., Zhang S.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/ma15124216",
     "OPC / Cement": R(487.2 / B), "SF (Silica fume)": R(54.1 / B), "W / B": R(238.2 / B), "River sand / B": R(230 / B),
     "Coarse aggregate / B": R(536 / B), "SP / B": R(2.8 / B, 5), "Binder content (kg/m³)": B, "Test age (days)": 28,
     "Curing method": "not stated", "Compressive specimen": "not stated (fcu)",
     "Source table/page": "Table 3 (mix), Sec. 2.1-2.2 text (fc)"}
for mid, sf, eps, fc, rho in [("S0E0", 0, 0, 48.7, 1568), ("S1E10", 1, 2.8, 49.1, 1495), ("S1E20", 1, 3.1, 44.2, 1320), ("S1E30", 1, 10.7, 37.9, 1174),
                              ("S1E40", 1, 16.7, 26.5, 1016), ("S1E50", 1, 25, 16.6, 857), ("S0E10", 0, 2.8, 46.7, 1413), ("S0E20", 0, 3.1, 41.3, 1257),
                              ("S0E30", 0, 10.7, 33.4, 1115), ("S0E40", 0, 16.7, 19.8, 958), ("S0E50", 0, 25, 12.1, 805)]:
    d = {"EPS / B": R(eps / B, 5), "Total fiber (vol%)": sf, "Compressive strength (MPa)": fc,
         "Conversions / notes": f"{mid}: Table 3 kg/m3 PC 487.2, microsilica 54.1 (10% cement replacement), water 238.2, river sand 230, limestone CA 536 (<10 mm), "
         f"PCE 2.8, EPS {eps} kg ({mid[3:] if mid != 'S0E0' else '0'} vol% of concrete; EPS 25 kg/m3, 3-5 mm). EPS kg/m3 as printed (10% and 20% mixes 2.8/3.1 kg look inconsistent - VERIFY). "
         f"Dry density {rho} kg/m3. Steel 78.5 kg/m3 / 7810 (paper density) = 1.0 vol%. 28-d fcu from text."}
    if sf:
        d.update({"Steel fiber (vol%)": 1, "Steel length (mm)": 48, "Steel tensile strength (MPa)": 610})
    add(b, **d)

# ---------------------------------------------------------------- 9 Liu et al. 2020 (crumb rubber basalt fibre concrete)
b = {"Article Name": "Mechanical Properties and Fracture Behavior of Crumb Rubber Basalt Fiber Concrete Based on Acoustic Emission Technology",
     "Author": "Liu H., Li W., Luo G., Liu S., Lyu X.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/s20123513",
     "OPC / Cement": 1, "Curing method": "standard curing room 20±2°C, RH 95%", "Curing time (days)": 27, "Curing temperature (°C)": 20,
     "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
     "Tensile specimen": "prism 100x100x400 (3-point bending, span 300)", "Tensile test type": "flexural",
     "Source table/page": "Table 6 (mix), Table 3 (fibre), Table 7 (fc, flexural)"}
for mid, wb, c, sand, ca, bf, cr, fc, ff, mod in [
        ("A1", 0.43, 418.60, 563.78, 1204.88, 2, 12.46, 40.6, 3.82, 1), ("A2", 0.43, 418.60, 534.11, 1204.88, 4, 24.92, 39.8, 3.79, 1),
        ("A3", 0.43, 418.60, 504.43, 1204.88, 6, 37.37, 33.7, 3.37, 1), ("A4", 0.46, 391.30, 541.24, 1220.97, 2, 25.25, 43.4, 4.16, 1),
        ("A5", 0.46, 391.30, 511.17, 1220.97, 4, 37.37, 37.4, 3.87, 1), ("A6", 0.46, 391.30, 571.31, 1220.97, 6, 12.62, 38.9, 3.25, 1),
        ("A7", 0.49, 367.35, 517.08, 1235.10, 2, 39.31, 39.5, 3.98, 1), ("A8", 0.49, 367.35, 577.91, 1235.10, 4, 12.77, 38.1, 3.40, 1),
        ("A9", 0.49, 367.35, 547.50, 1235.10, 6, 25.54, 38.3, 3.56, 1), ("B1", 0.43, 418.60, 504.43, 1204.88, 6, 37.37, 31.8, 2.78, 0),
        ("C1", 0.43, 418.60, 593.45, 1204.88, 0, 0, 29.6, 2.94, 0), ("C2", 0.46, 391.30, 601.38, 1220.97, 0, 0, 31.5, 3.02, 0),
        ("C3", 0.49, 367.35, 608.33, 1235.10, 0, 0, 31.1, 2.81, 0)]:
    add(b, **{"W / B": wb, "River sand / B": R(sand / c), "Coarse aggregate / B": R(ca / c), "Crumb rubber / B": R(cr / c, 5),
              "Binder content (kg/m³)": c, "Total fiber (vol%)": 0 if bf == 0 else None, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
              "Conversions / notes": f"{mid}: Table 6 kg/m3 water 180, cement {c}, river sand {sand}, coarse agg {ca} (5-25 mm), basalt fibre {bf} kg/m3, crumb rubber {cr} "
              f"(0.1-4.75 mm, replaces fine aggregate). CR {'pre-treated with 0.25 M NaOH' if mod else 'untreated'}. Basalt fibre (22 mm, 23 µm, 2836 MPa, 62 GPa) "
              "vol% NOT filled: fibre density not given in paper (2/4/6 kg/m3). Tensile value = 3-point FLEXURAL strength."})

# ---------------------------------------------------------------- 10 Lim et al. 2025 (foamed rubberised PP fibre concrete)
b = {"Article Name": "An Investigation of the Mechanical Properties and Thermal Insulation of Foamed Rubberised Polypropylene Fibre Concrete That Incorporates a High Quantity of Crumb Rubber Granules",
     "Author": "Lim Z.H., Lee F.W., Mo K.H., Chin R.J., Yeap K.H., Yew M.K.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/polym17070967",
     "OPC / Cement": 1, "PP length (mm)": 12, "PP diameter (µm)": 34, "Curing method": "water curing 28 d", "Curing time (days)": 28,
     "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "cylinder 100x200",
     "Tensile test type": "splitting", "Source table/page": "Table 4 (mix), Table 1 (fibre), Table 3 (CR), Table 6 (fc, splitting, flexural)"}
mixes = [("0.5:0", 306.85, 306.85, 153.42, 4.60, 0.00, 28.27), ("0.5:20", 322.26, 257.81, 161.13, 4.61, 26.75, 27.45), ("0.5:40", 339.30, 203.58, 169.65, 4.61, 56.34, 26.53),
         ("0.5:60", 358.24, 143.29, 179.12, 4.62, 89.22, 25.51), ("0.5:80", 379.42, 75.88, 189.71, 4.63, 125.99, 24.37), ("0.5:100", 403.26, 0.00, 201.63, 4.63, 167.39, 23.09),
         ("0.55:0", 300.97, 300.97, 165.54, 4.60, 0.00, 27.91), ("0.55:20", 315.78, 252.63, 173.68, 4.61, 26.22, 27.08), ("0.55:40", 332.13, 199.28, 182.67, 4.62, 55.15, 26.17),
         ("0.55:60", 350.25, 140.10, 192.64, 4.62, 87.23, 25.15), ("0.55:80", 370.47, 74.09, 203.76, 4.63, 123.03, 24.02), ("0.55:100", 393.17, 0.00, 216.24, 4.64, 163.20, 22.75),
         ("0.60:0", 295.32, 295.32, 177.19, 4.61, 0.00, 27.56), ("0.60:20", 309.56, 247.65, 185.74, 4.61, 25.70, 26.73), ("0.60:40", 325.25, 195.15, 195.15, 4.62, 54.00, 25.82),
         ("0.60:60", 342.62, 137.05, 205.57, 4.62, 85.33, 24.81), ("0.60:80", 361.94, 72.39, 217.17, 4.63, 120.19, 23.68), ("0.60:100", 383.58, 0.00, 230.15, 4.64, 159.22, 22.42),
         ("0.65:0", 289.87, 289.87, 188.42, 4.61, 0.00, 27.23), ("0.65:20", 303.58, 242.87, 197.33, 4.61, 25.20, 26.40), ("0.65:40", 318.66, 191.20, 207.13, 4.62, 52.91, 25.49),
         ("0.65:60", 335.31, 134.12, 217.95, 4.63, 83.51, 24.48), ("0.65:80", 353.80, 70.76, 229.97, 4.63, 117.49, 23.36), ("0.65:100", 374.44, 0.00, 243.38, 4.64, 155.43, 22.11)]
res = {"0.5:0": (2.64, 0.41, 1.61, 788), "0.55:0": (2.88, 0.45, 1.76, 803), "0.60:0": (2.38, 0.36, 1.50, 804), "0.65:0": (2.19, 0.33, 1.38, 794),
       "0.5:20": (2.59, 0.38, 1.55, 774), "0.55:20": (3.01, 0.45, 1.90, 776), "0.60:20": (2.34, 0.33, 1.43, 791), "0.65:20": (2.55, 0.37, 1.56, 781),
       "0.5:40": (3.08, 0.34, 2.00, 791), "0.55:40": (2.75, 0.41, 1.68, 788), "0.60:40": (2.56, 0.38, 1.54, 799), "0.65:40": (2.61, 0.40, 1.62, 791),
       "0.5:60": (3.51, 0.51, 2.11, 816), "0.55:60": (3.14, 0.48, 1.88, 792), "0.60:60": (2.93, 0.44, 1.82, 782), "0.65:60": (2.53, 0.38, 1.57, 780),
       "0.5:80": (4.10, 0.64, 2.46, 785), "0.55:80": (3.25, 0.47, 2.05, 783), "0.60:80": (2.88, 0.45, 1.73, 802), "0.65:80": (2.68, 0.40, 1.69, 772),
       "0.5:100": (3.89, 0.57, 2.49, 802), "0.55:100": (3.68, 0.58, 2.21, 792), "0.60:100": (2.95, 0.44, 1.86, 800), "0.65:100": (2.85, 0.42, 1.80, 801)}
for mid, c, sand, w, pp, cr, foam in mixes:
    fc, ft, ff, rho = res[mid]
    vf = R(pp / 910 * 100, 3)
    add(b, **{"W / B": R(w / c, 3), "Sand (type not stated) / B": R(sand / c), "Crumb rubber / B": R(cr / c), "Binder content (kg/m³)": c,
              "PP fiber (vol%)": vf, "Total fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Conversions / notes": f"FRPFC{mid}: Table 4 kg/m3 cement {c}, sand {sand}, water {w}, PP {pp}, CR granules {cr} (1-4 mm, 950 kg/m3), pre-formed foam {foam} kg/m3 "
              f"(no column); target density 800 kg/m3, hardened density {rho} kg/m3. CR replaces sand by volume. PP vol% = {pp}/910 (paper density 0.91, printed 'g/mm3'); "
              f"text says '0.6% PP added' - basis unclear. Flexural strength {ff} MPa (ASTM C293, 40x40x160). Splitting tensile strength."})

# ---------------------------------------------------------------- 11 Luo et al. 2020 (steel fibre rubber concrete, 0 freeze-thaw cycles)
B = 318
b = {"Article Name": "Experimental Investigation on the Freeze–Thaw Resistance of Steel Fibers Reinforced Rubber Concrete",
     "Author": "Luo T., Zhang C., Sun C., Zheng X., Ji Y., Yuan X.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13051260",
     "OPC / Cement": R(300 / B), "FA (Fly ash)": R(18 / B), "W / B": R(150 / B), "River sand / B": R(534 / B), "Coarse aggregate / B": R(1240 / B),
     "SP / B": R(0.032 / B, 6), "Crumb rubber / B": R(10 / B), "Binder content (kg/m³)": B, "Curing method": "cured 28 d (conditions not stated)",
     "Curing time (days)": 28, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
     "Source table/page": "Table 6 (mix), Sec. 3.1 text (fc at 0 freeze-thaw cycles)"}
for mid, sfkg, vf, fc in [("S1", 0, 0, 34.6), ("S4", 156, 2, 43.8)]:
    d = {"Total fiber (vol%)": vf, "Compressive strength (MPa)": fc,
         "Conversions / notes": f"{mid}: Table 6 kg/m3 cement 300, FA 18, river sand 534 (FM 2.53), coarse 1240 (5-20 mm), water 150, air-entraining water reducer 0.64 (no column), "
         f"PCE SP 0.032, steel fibre {sfkg}, rubber powder 10 (0.125 mm). Steel 156/7850 = 1.99 -> 2 vol% (paper states 2%). fc before freeze-thaw (0 FTC) from text; "
         "1.0/1.5% mixes and FTC results only in Fig. 8."}
    if vf:
        d.update({"Steel fiber (vol%)": 2, "Steel length (mm)": 38, "Steel diameter (µm)": 500, "Steel tensile strength (MPa)": 801})
    add(b, **d)

# ---------------------------------------------------------------- 12 Su et al. 2021 (basalt + PVA hybrid fibre rubber concrete)
b = {"Article Name": "Mechanical Properties of Hybrid Fiber Reinforced Rubber Concrete",
     "Author": "Su Q., Xu J.-M., Wang Y.-D.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14206028",
     "OPC / Cement": 1, "W / B": R(155 / 465), "River sand / B": R(600 / 465), "Coarse aggregate / B": R(1242 / 465), "SP / B": R(5.15 / 465),
     "Binder content (kg/m³)": 465, "Curing method": "saturated Ca(OH)2 solution, 20±2°C", "Curing time (days)": 28, "Curing temperature (°C)": 20,
     "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "cube 100 (splitting)",
     "Tensile test type": "splitting", "Source table/page": "Table 3 (mix), Table 1 (fibres), Table 4 (fc, splitting, flexural)"}
for mid, vb, vp, vr, fc, ft, ff in [("C", 0, 0, 0, 34.2, 4.65, 6.54), ("H-1", 0.1, 0.1, 5, 37.9, 5.25, 7.6), ("H-2", 0.1, 0.2, 10, 38.2, 5.21, 7.56),
                                    ("H-3", 0.1, 0.3, 15, 34.5, 4.72, 7.05), ("H-4", 0.2, 0.1, 10, 42.8, 6.19, 8.54), ("H-5", 0.2, 0.2, 15, 42.5, 5.65, 8.0),
                                    ("H-6", 0.2, 0.3, 5, 43.2, 5.58, 7.93), ("H-7", 0.3, 0.1, 15, 44.3, 5.96, 8.31), ("H-8", 0.3, 0.2, 5, 47.9, 6.63, 8.98),
                                    ("H-9", 0.3, 0.3, 10, 46.8, 6.24, 8.59)]:
    crkg = vr * 10.5
    d = {"Crumb rubber / B": R(crkg / 465, 5), "Basalt fiber (vol%)": vb, "Total fiber (vol%)": R(vb + vp, 2), "Compressive strength (MPa)": fc,
         "Tensile strength (MPa)": ft,
         "Conversions / notes": f"{mid}: Table 3 kg/m3 cement 465, coarse 1242, river sand 600, water 155, HPWR 5.15, basalt {vb*28:g}, 'PVA' {vp*9.1:g}, rubber {crkg:g} "
         f"(20 mesh, 1050 kg/m3; {vr} vol%). Fibre vol% from Table 2 levels (consistent with Table 1 densities 2.8 / 0.91). NOTE: 'PVA' fibre properties in Table 1 "
         "(0.91 g/cm3, 600 MPa, 5.75 GPa, 8 µm) look like polypropylene - recorded as PVA as stated (VERIFY). Sodium CMC 0.7% of cement as dispersant (no column). "
         f"Strengths converted by authors to standard size (fc x0.95). Flexural {ff} MPa. Splitting tensile on 100 mm cubes. Basalt 18 mm, 12 µm, 3500 MPa, 100 GPa."}
    if vp:
        d.update({"PVA fiber (vol%)": vp, "PVA length (mm)": 12, "PVA diameter (µm)": 8, "PVA tensile strength (MPa)": 600, "PVA elastic modulus (GPa)": 5.75})
    add(b, **d)

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows, columns=H)
df.to_csv(os.path.join(D, "w2_lightweight.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers")
