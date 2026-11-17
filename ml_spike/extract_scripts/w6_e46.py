"""Wave 6, agent e46: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e46.csv (99-column TEMPLATE header).
Papers: conbuildmat.2024.138131 (N-ECC only), 2025.142082, 2025.143600 (slag-filler mixes), 2026.145243 (control), 2026.145605.
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
DIRECT = "direct (uniaxial)"


def r4(x):
    return round(x, 4)


def paper(name, author, year, doi):
    return {"Article Name": name, "Author": author, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------- 1) Wang et al. 2024: recycled-powder ECC, only the quartz-sand control N-ECC
P = paper("Strategies for reusing multiple recycled powders: Evaluating the mechanical performance and sustainability of Engineered Cementitious Composites (ECC)",
          "Peiying Wang, Zhanqi Cheng, Xiangxi Jia, Jinlong Pan, Jiajia Zhou", 2024, "10.1016/j.conbuildmat.2024.138131")
B = 357 + 893
r = dict(P)
r.update({"OPC / Cement": r4(357 / B), "FA (Fly ash)": r4(893 / B), "W / B": r4(375 / B), "Sand (type not stated) / B": r4(375 / B),
          "SP / B": r4(1.5 / B), "VMA / B": r4(0.8 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2,
          "Curing method": "24 h in mould, demoulded, standard curing room 20 +/- 1 C, 95 % RH for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80,
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 47.40, "Tensile strength (MPa)": 6.662,
          "First-cracking strength (MPa)": 1.517, "Tensile strain capacity (%)": 7.919,
          "Source table/page": "Table 6 (mix, g/L), Table 1 (PE), Table 8 (fc), Table 9 (tensile), sect. 2.2",
          "Conversions / notes": "N-ECC (quartz-sand control) only; all other mixes use recycled brick/concrete powder or recycled glass powder (not allowed). "
                                 "Table 6 in g/L, treated as kg/m3; B = cement + FA = 1250. Quartz sand 375 used as sand. Water reducer 1.5 and thickener 0.8 g/L entered as SP / B and VMA / B. "
                                 "Strain = ultimate strain (Table 9). VERIFY: PE tensile strength printed as 3.0 without unit (left empty); 28 d curing after 24 h, so age could be 29 d."})
rows.append(r)

# ---------- 2) Lv et al. 2025: ternary EGC (GGBS-FA-SF, PE 1.5 vol%), 20 C reference, 7 d
P = paper("Investigation of mechanical properties and microstructural evolution of ternary high-temperature resistant engineered geopolymer composite (EGC)",
          "Luohao Lv, Yuanqiao Gan, Bo Wen, Lanqing Dai, Jiayu Chen, Lili Kan, Zhigang Zhang", 2025, "10.1016/j.conbuildmat.2025.142082")
r = dict(P)
r.update({"GGBS": 0.445, "FA (Fly ash)": 0.445, "SF (Silica fume)": 0.11, "WG / B (Water glass)": 0.18, "NaOH / B": 0.04, "W / B": 0.29,
          "Sand (type not stated) / B": 0.44,
          "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 1.5,
          "Curing method": "24 h in mould (20 C, 75 % RH, covered), demoulded, wrapped and oven heat cured 80 C 24 h, then lab room temperature until 7 d",
          "Curing time (days)": 7, "Curing temperature (°C)": 80, "Demolding age (days)": 1, "Test age (days)": 7, "Heat curing duration (h)": 24,
          "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Tensile strength (MPa)": 5.47, "First-cracking strength (MPa)": 2.72, "Tensile strain capacity (%)": 5.39,
          "Source table/page": "Table 3 (mix), Table 2 (PE), Table 4 (tensile, 20 C), sect. 2.2",
          "Conversions / notes": "Room-temperature (20 C) reference EGC only; heated groups skipped. Mass ratios to binder (GGBS + FA + SF = 1). "
                                 "Na2SiO3 solution (water content 64.16 %, modulus 3.3) entered as WG / B = 0.18; water 0.29 is the added water, water of the solution not added. "
                                 "Compressive strength only in Fig. 10, not entered. VERIFY: sand type not stated."})
rows.append(r)

# ---------- 3) Li, Li, Zhang 2025: PVA-ECC with ground slag filler (reactive), 28 d
P = paper("Inert particles enhance strength-ductility relationship for Engineered Cementitious Composites based on PVA fibers",
          "Junsheng Li, Victor C. Li, Duo Zhang", 2025, "10.1016/j.conbuildmat.2025.143600")
# slag mass (to OPC = 1), water, HRWRA, VMA, first crack, strength, strain
for nm, sl, w, hr, vm, fcr, ts, eps in [("S10", 0.42, 1.32, 0.008, 0.005, 2.82, 3.04, 2.85), ("S15", 0.63, 1.25, 0.013, 0.002, 2.84, 3.70, 3.13),
                                         ("S20", 0.84, 1.18, 0.021, 0.0, 3.66, 4.16, 2.45), ("S25", 1.05, 1.11, 0.027, 0.0, 4.43, 4.63, 1.86)]:
    B = 1 + 3.2 + sl
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(3.2 / B), "GGBS": r4(sl / B), "W / B": r4(w / B), "HRWR / B": r4(hr / B),
              "VMA / B": r4(vm / B),
              "PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2,
              "Curing method": "standard curing 28 d (conditions not detailed)", "Curing time (days)": 28, "Test age (days)": 28,
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Tensile strength (MPa)": ts, "First-cracking strength (MPa)": fcr,
              "Tensile strain capacity (%)": eps, "Source table/page": "Table 2 (mix, by mass), Table 1 (PVA), Table 5 (tensile), sect. 3.2",
              "Conversions / notes": f"{nm} (ground slag filler). Mix by mass to OPC = 1 (OPC 1 : FA 3.2 : slag {sl} : water {w}); B = OPC + FA + slag = {r4(B)}. "
                                     "HRWRA entered as HRWR / B, thickener as VMA / B (VMA 0 for S20, S25: dash in table). No sand in the mix. "
                                     "Composite compressive strength only in Fig. 11, not entered. Ground-quartz mixes skipped (quartz powder). "
                                     "VERIFY: cured for standard 28 d, temperature / RH not stated; direct tension (JSCE-recommended dog-bone) test."})
    rows.append(r)

# ---------- 4) Ma et al. 2026: UHDFRCC with recycled ceramic, control mix only
P = paper("Multi-mechanical performance evaluation of a more sustainable ultra-high-ductile fiber-reinforced cementitious composite with recycled ceramic sand and waste ceramic powder",
          "Zhiming Ma, Yuanhui Wu, Bo Wang, Youchao Zhang, Changqing Wang", 2026, "10.1016/j.conbuildmat.2026.145243")
B = 100 + 88 + 25
r = dict(P)
r.update({"OPC / Cement": r4(100 / B), "GGBS": r4(88 / B), "SF (Silica fume)": r4(25 / B), "W / B": r4(38.3 / B), "SS / B (Silica sand)": r4(62 / B),
          "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2,
          "Curing method": "24 h ambient in mould, demoulded, standard curing chamber 20 +/- 2 C, >= 95 % RH until 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "40", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 96.3, "Tensile strength (MPa)": 12.4, "Tensile strain capacity (%)": 6.1,
          "Source table/page": "Table 3 (mix, g), Table 2 (PE), sect. 3.3 (fc), sect. 3.4 (tensile)",
          "Conversions / notes": "Control UHDFRCC only (waste ceramic powder and recycled ceramic sand mixes skipped). Mix in g: cement 100, slag 88, SF 25, sand 62, water 38.3; B = 213 (W/B 0.18 as stated). "
                                 "Superplasticizer used but dose not given (not entered). Values from text (tensile strength 12.4 MPa, strain 6.1 %). VERIFY: 28 d curing after 24 h, so age could be 29 d."})
rows.append(r)

# ---------- 5) Li et al. 2026: pre-pressed UHPC, 180 C cured, non-preloaded (PP0) steel-fibre mixes
P = paper("Effects of steel fiber content and pre-setting pressure on the dynamic compressive behavior of UHPC",
          "Yongze Li, Chunxiao Zhang, Aiguo Dang, Jize Mao, Jingbiao Liu, Gang Wang, Shaohua Cao, Junlei Wang, Jiaqi Huang", 2026, "10.1016/j.conbuildmat.2026.145605")
B = 1248.9 + 287.2 + 124.8
for nm, sf, st, fc, ts in [("SF2-PP0", 2, 156, 201.5, 5.2), ("SF4-PP0", 4, 312, 227.5, 7.5)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1248.9 / B), "FA (Fly ash)": r4(124.8 / B), "SF (Silica fume)": r4(287.2 / B), "W / B": r4(249.1 / B),
              "Sand (type not stated) / B": r4(624.4 / B), "SP / B": r4(28 / B), "Binder content (kg/m³)": r4(B),
              "Steel fiber (vol%)": sf, "Total fiber (vol%)": sf,
              "Curing method": "24 h in mould, demoulded, dry heat curing in oven at 180 C for 3 d", "Curing time (days)": 3, "Curing temperature (°C)": 180,
              "Demolding age (days)": 1, "Test age (days)": 4, "Heat curing duration (h)": 72,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts,
              "Source table/page": "Table 2 (mix, kg/m3), Table 4 (fc, axial tension), sect. 2.2-2.3",
              "Conversions / notes": f"{nm}: non-preloaded (0 MPa) specimens only. kg/m3 / B (cement + FA + SF = {r4(B)}). Quartz sand 624.4 used as sand. Water-reducer 28 kg/m3 entered as SP / B. "
                                     f"Steel fibre {st} kg/m3 = {sf} vol% as stated (copper-plated; length / diameter not given). fc = cube strength; tensile = axial tensile strength (T/CBMF 37-2018, direct tension, specimen shape not stated). "
                                     "VERIFY: test age derived = 24 h mould + 3 d at 180 C (no age stated). The same specimens are also reported in conbuildmat.2025.140099 (not added separately)."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e46.csv"), index=False, encoding="utf-8-sig")
print(df.shape)
