"""Wave 6, agent e43: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e43.csv (99-column TEMPLATE header).
Papers: jobe.2024.110793, jobe.2025.114039, jobe.2025.114110, jobe.2026.116100, jobe.2026.116398, jobe.2026.117165,
        powtec.2023.118853, jobe.2024.110339, jobe.2025.113705, rineng.2025.108304, rineng.2026.111075
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


# ---------- 1) Dry-/wet-spun UHMWPE ECC, 3 strength grades (jobe.2024.110793)
P = paper("Comparative analysis of spinning techniques on the performance of full-strength-grade engineered cementitious composites: "
          "Mechanical characteristics, pore structure, fiber distribution, micromorphology",
          "Minjin Cai, Hehua Zhu, Timon Rabczuk, Xiaoying Zhuang", 2024, "10.1016/j.jobe.2024.110793")
mixes = {
    "L": dict(c=0.4, fa=0.6, ggbs=0, lp=0, sf=0, w=0.27, sp=0.005),
    "M": dict(c=0.5, fa=0.3, ggbs=0, lp=0.2, sf=0, w=0.19, sp=0.01),
    "H": dict(c=0.6, fa=0, ggbs=0.2, lp=0.1, sf=0.1, w=0.16, sp=0.012),
}
# dry-spun values stated in text; wet-spun = stated % increase over dry (derived -> VERIFY)
# order: fc, first-cracking, tensile strength, strain
dry = {"L": (40.74, 2.11, 6.46, 8.53), "M": (70.89, 4.76, 11.43, 8.16), "H": (109.25, 6.63, 14.08, 2.74)}
inc = {"L": (0.001, 0.104, 0.046, 0.011), "M": (0.006, 0.426, 0.097, 0.007), "H": (0.008, 0.19, 0.227, 1.92)}
for g in "LMH":
    m = mixes[g]
    for typ in ("D", "W"):
        v = dry[g]
        if typ == "W":
            v = tuple(a * (1 + b) for a, b in zip(v, inc[g]))
        fc, fcr, ts, eps = [round(x, 3) for x in v]
        r = dict(P)
        r.update({"OPC / Cement": m["c"], "W / B": m["w"], "SS / B (Silica sand)": 0.3, "SP / B": m["sp"],
                  "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 15, "PE tensile strength (MPa)": 3000,
                  "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2,
                  "Curing method": "24 h room temperature in mould, demoulded, 20 +/- 2 C and 95 +/- 2 % RH for 28 d",
                  "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
                  "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
                  "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts,
                  "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 1 (mix, mass ratio), Table 2 (PE fibre), sect. 3.2-3.3 text (fc, tensile)"})
        if m["fa"]:
            r["FA (Fly ash)"] = m["fa"]
        if m["ggbs"]:
            r["GGBS"] = m["ggbs"]
        if m["lp"]:
            r["Limestone powder"] = m["lp"]
        if m["sf"]:
            r["SF (Silica fume)"] = m["sf"]
        note = (f"{g}{typ} ({'dry' if typ == 'D' else 'wet'}-spun UHMWPE fibre). Mix in mass ratios to binder = 1 (Table 1); quartz sand 0.3 entered as silica sand. "
                "Limestone = limestone powder. Water ratio taken as W/B. Values come from text (figures not used). "
                "VERIFY: tensile specimen type/test age not stated explicitly (28 d curing; direct tension assumed); cube size 100 mm.")
        if typ == "W":
            note += " VERIFY: wet-spun fc, first-cracking, tensile strength, strain are DERIVED from the stated % increases vs dry-spun."
        r["Conversions / notes"] = note
        rows.append(r)

# ---------- 2) Steel slag powder ECC: reference FA-0 only (jobe.2025.114039)
P = paper("Synergistic effect of waste steel slag powder and fly ash in sustainable high strength engineered cementitious composites: "
          "From microstructure to macro-performance",
          "Chenyu Lu, Qiang Shen, Zhigang Zhang, Xiaoyue Zhang, Rami A. Hawileh", 2025, "10.1016/j.jobe.2025.114039")
r = dict(P)
r.update({"OPC / Cement": 0.395, "FA (Fly ash)": 0.555, "SF (Silica fume)": 0.05, "W / B": 0.2, "SS / B (Silica sand)": 0.27,
          "Crumb rubber / B": 0.014, "SP / B": 0.01, "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 26,
          "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2,
          "Curing method": "sealed with film 24 h at 25 C, demoulded, then 25 +/- 3 C and 55 +/- 5 % RH for 27 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 25, "Curing RH (%)": 55, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 3.83, "Tensile strength (MPa)": 7.25, "Tensile strain capacity (%)": 4.48,
          "Source table/page": "Table 1 (mix, by weight), Table 2 (PE), Table 4 (tensile)",
          "Conversions / notes": "Mix FA-0 only (steel slag powder mixes FA-25..FA-100 skipped). Ratios by weight to binder (Table 1: cement + FA + SF = 1). "
                                 "Crumb rubber 0.014 per binder. fc of FA-0 only in Fig. 11 (not entered). "
                                 "VERIFY: test age 28 d derived from 24 h + 27 d curing; tensile test age not stated explicitly."})
rows.append(r)

# ---------- 3) Eco-efficient HS-ECC, ordinary and ultrafine FA (jobe.2025.114110)
P = paper("Eco-efficient high-strength engineered cementitious composites: mechanical and self-healing behaviors influenced by fly ash content and particle size",
          "Jianqiao Yu, Zhigang Zhang, Yuanchuan Chen, Jamal A. Abdalla, Xiaoyue Zhang", 2025, "10.1016/j.jobe.2025.114110")
t3 = [("OFA/C-0.8", 717, 574, 115, 422, 281, 85.52, 4.52, 7.74, 4.72),
      ("OFA/C-1.2", 582, 698, 112, 418, 278, 78.99, 4.17, 7.06, 5.14),
      ("OFA/C-1.6", 489, 783, 111, 415, 276, 67.42, 3.95, 6.25, 5.47),
      ("UFA/C-0.8", 717, 574, 115, 422, 281, 93.17, 5.14, 8.37, 5.33),
      ("UFA/C-1.2", 582, 698, 112, 418, 278, 81.32, 4.78, 8.04, 5.81),
      ("UFA/C-1.6", 489, 783, 111, 415, 276, 75.83, 4.32, 7.62, 6.24)]
for nm, c, fa, sf, ss, w, fc, fcr, ts, eps in t3:
    B = c + fa + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B),
              "SS / B (Silica sand)": r4(ss / B), "SP / B": r4(20 / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 26, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2,
              "Curing method": "24 h in mould, demoulded, standard conditions 28 d (temperature/RH not stated)", "Curing time (days)": 28,
              "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80,
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts,
              "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix kg/m3), sect. 2.1 (PE), Table 5 (tensile), sect. 3.3 text (fc)",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + FA + SF = {B}). OFA = ordinary FA, UFA = ultrafine FA (both entered as fly ash). "
                                     "SP 20 kg/m3 as dosed. Fiber 2 vol% as stated. fc from text of sect. 3.3 (Fig. 9 not used); cube size not stated."})
    rows.append(r)

# ---------- 4) Sprayable lightweight ECC: cast reference without cenosphere (jobe.2026.116100)
P = paper("Rheology- and fracture-guided design of lightweight spray-applied engineered cementitious composites achieving structural-grade strength and high tensile ductility",
          "Dawei Gu, Yuqin Sun, Junxiu Hu, Ruyang Lu, Jinlong Pan", 2026, "10.1016/j.jobe.2026.116100")
B = 444.6 + 889.3 + 44.5
r = dict(P)
r.update({"OPC / Cement": r4(444.6 / B), "FA (Fly ash)": r4(889.3 / B), "SF (Silica fume)": r4(44.5 / B), "W / B": r4(444.6 / B),
          "HPMC / B (hydroxypropyl methyl cellulose)": r4(13.8 / B), "SP / B": r4(13.8 / B), "Binder content (kg/m³)": r4(B),
          "PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 38, "PVA tensile strength (MPa)": 1620,
          "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
          "Curing method": "covered with film, demoulded 24 h, cured at 20 +/- 3 C for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "100", "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80,
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 41.7, "Tensile strength (MPa)": 5.84,
          "First-cracking strength (MPa)": 2.78, "Tensile strain capacity (%)": 1.99,
          "Source table/page": "Table 4 (mix, kg/m3), Table 5 (tensile), sect. 3.5 / 4 text (fc 41.7), Table 2 (PVA)",
          "Conversions / notes": f"C-FAC-0% (cast, no cenosphere). kg/m3 / B (cement + FA + SF = {r4(B)}). PVA 26 kg/m3 = 2 vol% (1.3 g/cm3). "
                                 "Spray reference S-FAC-0% has no fibre (skipped); cenosphere mixes skipped. "
                                 "VERIFY: PVA length 8 mm is the length of the selected mix (mechanical stage length not stated explicitly); "
                                 "fc age not stated (28 d curing assumed); HPMC 1 % and SP 1 % of binder as in Table 4."})
rows.append(r)

# ---------- 5) PVA agglomeration ECC: PFA-0 control (jobe.2026.116398)
P = paper("Defect-driven mechanical deterioration and rheological evolution of engineered cementitious composites induced by fiber agglomeration: "
          "Cross-scale mechanisms and strength prediction",
          "Zheng Chen, Guoxin Zhao, Shengzhao Chen, Ben Chen, Yunchao Tang", 2026, "10.1016/j.jobe.2026.116398")
B = 435 + 783
r = dict(P)
r.update({"OPC / Cement": r4(435 / B), "FA (Fly ash)": r4(783 / B), "W / B": r4(365 / B), "SS / B (Silica sand)": r4(438 / B),
          "SP / B": 0.0125, "HPMC / B (hydroxypropyl methyl cellulose)": 0.005, "Binder content (kg/m³)": B,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "Total fiber (vol%)": 2,
          "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 4.09, "Tensile strength (MPa)": 5.80, "Tensile strain capacity (%)": 8.37,
          "Source table/page": "Table 4 (mix), Table 5 (tensile)",
          "Conversions / notes": f"PFA-0 control only (artificially agglomerated PFA-20..80 skipped). kg/m3 / B (cement + FA = {B}). Quartz sand 80-120 mesh as sand. "
                                 "SP 1.25 % and HPMC 5 per mille of binder (Table 4). "
                                 "VERIFY: curing regime not described in the text; tensile test age assumed 28 d (28-day compressive stated). fc only in Fig. 4."})
rows.append(r)

# ---------- 6) Recycled brick powder ECC: NRBP0 control (jobe.2026.117165)
P = paper("Effects of recycled brick powder content and particle size on the performance of engineered cementitious composites (ECC) and the associated multiscale mechanisms",
          "Tong Mou, Duo Liu, Yiwen Cao, Maodian Feng, Jinxu Wang, Jiandong Zhang", 2026, "10.1016/j.jobe.2026.117165")
B = 1065 + 304 + 152
r = dict(P)
r.update({"OPC / Cement": r4(1065 / B), "GGBS": r4(304 / B), "SF (Silica fume)": r4(152 / B), "W / B": r4(304 / B),
          "SS / B (Silica sand)": r4(456 / B), "HRWR / B": r4(19.4 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": 0.94, "PE length (mm)": 18, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 3100,
          "PE elastic modulus (GPa)": 122, "Total fiber (vol%)": 0.94,
          "Curing method": "24 h covered at room temperature, demoulded, standard curing room 20 +/- 2 C, 95 % RH, 28 d",
          "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 71.4, "Tensile strain capacity (%)": 4.17,
          "Source table/page": "Table 3 (mix), Table 2 (PE), sect. 3.3-3.4 text (fc 71.4, strain 4.17)",
          "Conversions / notes": f"NRBP0 control only (brick powder mixes skipped). kg/m3 / B (OPC + GGBS + SF = {B}). "
                                 "VERIFY: fc 71.4 MPa is the ECC value read from a sentence 'mortar and ECC ... 90.6 MPa to 71.4 MPa' (NRBP0 mortar 90.6, ECC 71.4); "
                                 "PE 9.1 kg/m3 converted to 0.94 vol% with SG 0.97 (vol% not stated); HRWRA is powder. Tensile strength of NRBP0 only in Fig. 12 (not entered)."})
rows.append(r)

# ---------- 7) Diatomite HSECC: reference C50D0 (powtec.2023.118853)
P = paper("Feasibility of using high-volume pozzolanic fillers to develop sustainable engineered cementitious composites (ECC)",
          "Minghu Zhang, Xuezhen Zhu, Sukhoon Pyo, Yuanxia Yang, Baoju Liu, Jinyan Shi", 2023, "10.1016/j.powtec.2023.118853")
r = dict(P)
r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.45, "SF (Silica fume)": 0.05, "W / B": 0.2, "SS / B (Silica sand)": 0.35, "SP / B": 0.006,
          "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 15.6, "PE tensile strength (MPa)": 3980, "Total fiber (vol%)": 2,
          "Curing method": "20 C for 24 h, demoulded, standard curing room 20 +/- 2 C, RH > 95 % until test", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "40", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 86, "First-cracking strength (MPa)": 5.613, "Tensile strength (MPa)": 10.248,
          "Tensile strain capacity (%)": 3.67,
          "Source table/page": "Table 1 (mix, wt ratio), sect. 3 text (fc 86, strain 3.67, tensile derived)",
          "Conversions / notes": "C50D0 reference only (diatomite mixes skipped). Mass ratios to binder = 1. "
                                 "VERIFY: first-cracking 5.613 and tensile strength 10.248 MPa are DERIVED from the text (C35D15 = 2.06 / 5.37 MPa, i.e. 63.3 % / 47.6 % lower than C50D0); "
                                 "SP 0.006 taken as ratio to binder (unit not stated); tensile test age taken as 28 d (fc 28 d stated)."})
rows.append(r)

# ---------- 8) Waste glass ECC: ECC-Ref (jobe.2024.110339)
P = paper("Development of eco-friendly engineered cementitious composites (ECC) with both waste glass powder and aggregate: A comprehensive investigation",
          "Chaofeng Liang, Xin Liu, Youchao Zhang, Zhiyu Zhang, Zhiming Ma", 2024, "10.1016/j.jobe.2024.110339")
r = dict(P)
r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.4, "SF (Silica fume)": 0.1, "W / B": 0.2, "SS / B (Silica sand)": 0.25,
          "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 25, "PE tensile strength (MPa)": 3100, "PE elastic modulus (GPa)": 42.8,
          "Total fiber (vol%)": 2,
          "Curing method": "24 h at 20 C in mould, then constant temperature and RH (values not stated)", "Curing time (days)": 28,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
          "Tensile test type": DIRECT, "Compressive strength (MPa)": 93.35, "Tensile strength (MPa)": 8.33,
          "First-cracking strength (MPa)": 4.73, "Tensile strain capacity (%)": 5.82,
          "Source table/page": "Table 2 (mix, weight ratio), Table 1 (PE), sect. 3 text (ECC-Ref values)",
          "Conversions / notes": "ECC-Ref only (glass powder / glass aggregate mixes skipped). Table 2 gives cement 100 : FA 80 : SF 20 : silica sand 50 (by weight, cement = 100) -> B = 200. "
                                 "VERIFY: sand 50/200 = 0.25 of binder assumes the same basis; SP dosage not given (empty); curing temperature/RH not stated; "
                                 "fc 28 d stated, tensile age assumed 28 d."})
rows.append(r)

# ---------- 9) UHP-ECC with recycled powder/aggregate: plain UHP-ECC (jobe.2025.113705)
P = paper("Understanding the micro-characteristics and mechanical behavior of more sustainable UHP-ECC with both recycled aggregate and recycled powder from concrete waste",
          "Zhiming Ma, Yuanhui Wu, Bo Wang, Chaofeng Liang, Youchao Zhang, Changqing Wang", 2025, "10.1016/j.jobe.2025.113705")
B = 800 + 700 + 200
r = dict(P)
r.update({"OPC / Cement": r4(800 / B), "GGBS": r4(700 / B), "SF (Silica fume)": r4(200 / B), "W / B": r4(306 / B),
          "SS / B (Silica sand)": r4(500 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 25,
          "PE tensile strength (MPa)": 3100, "PE elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
          "Curing method": "24 h standard conditions, demoulded, curing chamber 20 +/- 2 C, RH >= 95 % to 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile test type": DIRECT,
          "Tensile strain capacity (%)": 6.5,
          "Source table/page": "Table 3 (mix, kg/m3), Table 2 (PE), sect. 3 text (strain 6.5 %)",
          "Conversions / notes": f"Plain UHP-ECC only (recycled powder / aggregate mixes skipped). kg/m3 / B (cement + GGBS + SF = {B}); W/B 0.18 stated. "
                                 "SP present but dosage not given (empty). Fiber 2.0 vol% as stated (20 kg/m3). fc and tensile strength only in figures (not entered). "
                                 "VERIFY: tensile specimen shape / age not stated explicitly (28 d curing)."})
rows.append(r)

# ---------- 10) MPCW-ECC high temperature: ECC at 20 C (rineng.2025.108304)
P = paper("Mechanical properties of ECC incorporated with micro-powder of construction waste after elevated-temperature exposure",
          "Long Liu, Ziyi Song, Liang Cui, Jinqiu Dai, Yu Wang, Chong Liu, et al.", 2025, "10.1016/j.rineng.2025.108304")
B = 656 + 118 + 604
r = dict(P)
r.update({"OPC / Cement": r4(656 / B), "SF (Silica fume)": r4(118 / B), "FA (Fly ash)": r4(604 / B), "W / B": r4(363 / B),
          "Sand (type not stated) / B": r4(410 / B), "HRWR / B": r4(2 / B), "Binder content (kg/m³)": B,
          "PVA fiber (vol%)": 1.15, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
          "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": 1.15,
          "Curing method": "24 h room temperature, curing chamber 20 +/- 1 C, RH >= 95 % for 28 d (specimen at 20 C, no heating)",
          "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": 41.89,
          "Source table/page": "Table 2 (mix), Table 1 (PVA), Table 3 (20 C row, ultimate strength)",
          "Conversions / notes": "ECC at 20 C (unheated reference) only; heated and MPCW mixes skipped. Quartz sand 410 kg/m3 entered as sand. "
                                 "kg/m3 / B (OPC + SF + FA = 1378). PVA 15 kg/m3 -> 1.15 vol% with 1.3 g/cm3 (VERIFY derived). "
                                 "fc = 'ultimate strength' of Table 3 at 20 C. Tensile table starts at 100 C (no ambient tensile value)."})
rows.append(r)

# ---------- 11) PVA-FRCC with FA and MK: FRCC15 fully wet (rineng.2026.111075)
P = paper("Enhancing mechanical and durability properties of polyvinyl alcohol fiber-reinforced cement composites with fly ash and metakaolin: "
          "The compensating role of metakaolin under insufficient curing",
          "Farhad Masoumparast catik lahijani, Iman Sadrinejad, Mir Alimohammad Mirgozar Langaroudi, Morteza Mansouri Sarvandani", 2026,
          "10.1016/j.rineng.2026.111075")
B = 565 + 576 + 102
r = dict(P)
r.update({"OPC / Cement": r4(565 / B), "FA (Fly ash)": r4(576 / B), "Metakaolin": r4(102 / B), "W / B": r4(335.6 / B),
          "SS / B (Silica sand)": r4(446 / B), "SP / B": r4(12.4 / B), "Binder content (kg/m³)": B,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 6, "PVA diameter (µm)": 13, "PVA tensile strength (MPa)": 1600,
          "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": 2,
          "Curing method": "fully wet (water) curing (temperature not stated)", "Curing time (days)": 28, "Test age (days)": 28,
          "Compressive strength (MPa)": 68.6,
          "Source table/page": "Table 3 (mix FRCC15), abstract and conclusions (68.6 MPa)",
          "Conversions / notes": f"FRCC15 (15 % MK replacing FA) only; other mixes/curing regimes only in figures. kg/m3 / B (cement + FA + MK = {B}); W/B 0.27 stated. "
                                 "VERIFY: 68.6 MPa is the 28-d value under full wet curing as given in the abstract; specimen shape not checked."})
rows.append(r)

df = pd.DataFrame(rows)
df = df.reindex(columns=cols)
out = os.path.join(out_dir, "w6_e43.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows ->", out)
