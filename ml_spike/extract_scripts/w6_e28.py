"""Wave 6, agent e28: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e28.csv (99-column TEMPLATE header).
Papers: cemconcomp.2023.105234, cemconres.2025.108049, clema.2022.100121, clema.2024.100240,
        cemconcomp.2026.106585, cemconcomp.2019.103416, compstruct.2016.12.022
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


# ---------- 1) Huo et al.: PE + steel hybrid SHCC (steam cured)
P = {"Article Name": "Dynamic tensile properties of steel fiber reinforced polyethylene fiber-engineered/strain-hardening cementitious composites (PE-ECC/SHCC) at high strain rate",
     "Author": "Yanlin Huo, Tianan Liu, Dong Lu, Xiaoyu Han, Huayang Sun, Jinguang Huang, Xiaobin Ye, Chenchen Zhang, Zhitao Chen, Yingzi Yang",
     "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2023.105234"}
B = 1 + 1 + 0.22
for nm, st, scr, smax, eps in [("PE1.5ST0", 0, 6.5, 10.89, 4.42), ("PE1.5ST0.5", 0.5, 8.49, 11.67, 5.11),
                               ("PE1.5ST1.0", 1.0, 10.05, 11.17, 3.13), ("PE1.5ST1.5", 1.5, 11.34, 12.4, 2.04)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(1 / B), "SF (Silica fume)": r4(.22 / B), "W / B": 0.18,
              "Sand (type not stated) / B": r4(0.89 / B), "SP / B": 0.0033,
              "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 3800, "PE elastic modulus (GPa)": 113,
              "Total fiber (vol%)": 1.5 + st,
              "Curing method": "demoulded after 1 d, steam curing chamber 90 C for 3 d", "Curing time (days)": 3, "Curing temperature (°C)": 90,
              "Demolding age (days)": 1, "Test age (days)": 4, "Heat curing duration (h)": 72,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dumbbell", "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": smax, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, weight ratio), Table 2 (fibres), Table 4 (quasi-static tension), sect. 2.2",
              "Conversions / notes": f"{nm}. Weight ratios taken with cement = 1 (cement 1, FA 1, SF 0.22 -> B = 2.22). VERIFY: aggregate 0.89 (called sand in text) is divided by B = 2.22, "
                                     "SP 0.33 % entered as 0.0033 of binder; W/B 0.18 as stated. Defoamer 0.007 % (noted). "
                                     "VERIFY: test age 4 d derived (1 d + 3 d steam), test date not stated. fc only in Fig. 7, not entered. Quasi-static rate tests only (impact tests skipped). "
                                     "Steel fibre 160 um x 13 mm, 2500 MPa, 210 GPa."})
    if st:
        r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 13, "Steel diameter (µm)": 160, "Steel tensile strength (MPa)": 2500, "Steel elastic modulus (GPa)": 210})
    rows.append(r)

# ---------- 2) Hao et al.: HS-UHTCC uniaxial compression (confining pressure 0)
P = {"Article Name": "Triaxial compressive behavior of high-strength strain-hardening fiber-reinforced cementitious composites: Fiber hybridization effect and constitutive relations",
     "Author": "Yanxin Hao, Xing Yin, Qinghua Li, Shilang Xu", "Year": 2025, "DOI / URL": "https://doi.org/10.1016/j.cemconres.2025.108049"}
B = 1101 + 344 + 193
for nm, st, pe, fc in [("S1P2", 1, 2, 133.42), ("S2P1", 2, 1, 135.11)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1101 / B), "SF (Silica fume)": r4(344 / B), "GGBS": r4(193 / B), "W / B": r4(244 / B),
              "Sand (type not stated) / B": r4(495 / B), "SP / B": r4(22 / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": pe, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100,
              "Steel fiber (vol%)": st, "Steel length (mm)": 8, "Steel diameter (µm)": 115, "Steel tensile strength (MPa)": 3000, "Steel elastic modulus (GPa)": 200,
              "Total fiber (vol%)": 3,
              "Curing method": "sealed 24 h, demoulded, water bath 90 C 24 h, then 23 C RH 95 % for 90 d",
              "Curing time (days)": 92, "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 92, "Heat curing duration (h)": 24,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix, kg/m3), Table 4 (fibres), Table A.1/A.2 (fr = 0 average), sect. 2.1",
              "Conversions / notes": f"{nm} (steel {st} vol% + PE {pe} vol%). kg/m3 / B (cement + SF + slag = 1638). fc = average uniaxial (confining pressure 0) strength of 3 cylinders. "
                                     "VERIFY: test age 92 d derived (1 d + 24 h hot water + 90 d standard curing); steel tensile strength given as >= 3000. No tensile test."})
    rows.append(r)

# ---------- 3) Sridhar: hybrid PVA / steel ECC, 28 d water cured
P = {"Article Name": "Durability study on engineered cementitious composites with hybrid fibers under sulfate and chloride environments",
     "Author": "Radhika Sridhar", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.clema.2022.100121"}
B = 967 + 251
for nm, pva, st, fc, ft in [("ECC-SF-M2", 0, 2, 57.01, 7.88), ("ECC-PVA-M3", 2, 0, 54.14, 8.2), ("ECC-HY1-M4", 1, 1, 59.13, 8.45),
                            ("ECC-HY2-M5", 1.5, 0.5, 61.95, 9.45), ("ECC-HY3-M6", 0.5, 1.5, 58.05, 8.55)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(967 / B), "SF (Silica fume)": r4(251 / B), "W / B": r4(365.4 / B), "SS / B (Silica sand)": r4(675 / B),
              "Sand max size (µm)": 500, "SP / B": r4(7 / B), "Binder content (kg/m³)": B, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded after 24 h, water curing 28 d", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.6", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Source table/page": "Table 2 (mix, kg/m3), Table 3 (fibre dosage), Table 1 (fibres), Table 4 (fc, tensile)",
              "Conversions / notes": f"{nm}. kg/m3 / B (cement + micro-silica = 1218). Silica sand 405 (0.5 mm) + 270 (0.2 mm) = 675 kg/m3. HRWRA 7 kg/m3 entered as SP. "
                                     "Control without fibre skipped. Tensile curing temperature / RH not stated; no strain reported. Tensile strength values are high for a 51-54 MPa matrix: VERIFY."})
    if pva:
        r.update({"PVA fiber (vol%)": pva, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 41})
    if st:
        r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 35, "Steel diameter (µm)": 500, "Steel tensile strength (MPa)": 1100, "Steel elastic modulus (GPa)": 210})
    rows.append(r)

# ---------- 4) Rawat et al.: HSECC M4 (cement + GGBFS) and M5 (cement + SF); fc at 56 d, M5 strain at 20 C
P = {"Article Name": "Green engineered cementitious composites with enhanced tensile and flexural properties at elevated temperatures",
     "Author": "S. Rawat, C.K. Lee, Y.X. Zhang", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.clema.2024.100240"}
common = {"PE fiber (vol%)": 1.5, "Steel fiber (vol%)": 0.75, "Total fiber (vol%)": 2.25,
          "Curing method": "fog room 23 C RH 95 % 28 d, then 20 C RH 55 % for 28 d (reference, no heating)", "Curing time (days)": 56, "Curing temperature (°C)": 20,
          "Curing RH (%)": 55, "Test age (days)": 56, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75x150"}
r = dict(P)
r.update(common)
r.update({"OPC / Cement": 0.5, "GGBS": 0.5, "W / B": r4(0.40 / 2), "Sand (type not stated) / B": r4(0.73 / 2), "HRWR / B": r4(0.04 / 2),
          "Compressive strength (MPa)": 143.7, "Source table/page": "Table 1 (mix M4, 56-d fc), sect. 2.2-2.3",
          "Conversions / notes": "M4 (cement : GGBFS = 1 : 1). Ratios in Table 1 are by mass of cement (cement 1, GGBFS 1.00, sand 0.73, water 0.40, HRWR 0.04) -> divided by B = 2. "
                                 "Mixes M1-M3 skipped (dolomite powder). Only fc entered (tensile data of M4 only in figures). Fibre dimensions not given in the extracted text."})
rows.append(r)
r = dict(P)
r.update(common)
r.update({"OPC / Cement": r4(1 / 1.11), "SF (Silica fume)": r4(0.11 / 1.11), "W / B": r4(0.22 / 1.11), "Sand (type not stated) / B": r4(0.44 / 1.11),
          "HRWR / B": r4(0.02 / 1.11), "Compressive strength (MPa)": 153.7, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Tensile strain capacity (%)": 3.67,
          "Source table/page": "Table 1 (mix M5, 56-d fc), sect. 3.2.4 (strain at 20 C)",
          "Conversions / notes": "M5 (cement + silica fume 0.11). Ratios by mass of cement -> divided by B = 1.11 (W/B 0.198, text says 0.2). "
                                 "VERIFY: strain 3.67 % is the highest room-temperature value quoted in text (range 2.12 to 3.67 % with M5 highest); the 20 C specimens are the 56-d reference. "
                                 "Tensile strength only in figures. Fibre dimensions not given in the extracted text."})
rows.append(r)

# ---------- 5) Zhu et al.: UHS-ECC, silica-sand reference C0.30
P = {"Article Name": "Rate-dependent flaw effect and cracking behavior of Ultra-High-Strength Engineered Cementitious Composites (UHS-ECC) with seawater and sea-sand",
     "Author": "Ji-Xiang Zhu, Zhi-Liang Zhang, Wei-He Liu, Ling-Yu Xu, Ke-Fan Weng, Shi-Wen Han, Yi-Xin Zhang, Bo-Tao Huang", "Year": 2026,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2026.106585"}
B = 1.25
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(.25 / B), "W / B": r4(.2 / B), "SS / B (Silica sand)": r4(.375 / B), "Sand max size (µm)": 300,
          "SP / B": r4(.014 / B), "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100,
          "Total fiber (vol%)": 2.0, "Curing method": "20 C for 24 h, demoulded, 28 d moist curing", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": 152.1,
          "Source table/page": "Table 1 (mix, weight ratio), Table 3 (C0.30), sect. 3.1 (28-d fc), sect. 2.2",
          "Conversions / notes": "Reference series C0.30 (silica sand <= 0.3 mm); sea-sand / seawater series skipped. Weight ratio with cement = 1 -> B = cement + SF = 1.25. "
                                 "SP given in solid (0.014 of cement). VERIFY: water of C0.30 assumed fresh water (Table 1 reads Seawater/Fresh Water). "
                                 "Strain values only in Fig. 4, not entered."})
rows.append(r)

# ---------- 6) Chen et al.: high-strength PE-SHCC control M5
P = {"Article Name": "Experimental study on the shrinkage reduction of high strength strain-hardening cementitious composites",
     "Author": "Yixin Chen, Jie Yao, Zeyu Lu, Christopher K.Y. Leung", "Year": 2019, "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2019.103416"}
base = {"OPC / Cement": 0.8, "SF (Silica fume)": 0.2, "W / B": 0.145, "Sand (type not stated) / B": 0.3, "SP / B": 0.025, "PE fiber (vol%)": 2.2, "Total fiber (vol%)": 2.2,
        "Source table/page": "Table 1 (mix M5 control), Table 6 (14 d / 28 d fc, 14 d tension)"}
note = ("M5 control only (SRA / CSA-cement mixes skipped). Mix ratios by weight of binder (cement 0.8 + silica fume 0.2 = 1). SP in solution (30 % solids) as dosed. "
        "Curing conditions of the mechanical specimens not stated in the text (test age only).")
r = dict(P)
r.update(base)
r.update({"Test age (days)": 14, "Compressive strength (MPa)": 123, "Tensile specimen": "dumbbell", "Tensile test type": DIRECT, "Tensile strength (MPa)": 10.58,
          "Tensile strain capacity (%)": 1.65, "Conversions / notes": "M5, 14 d. " + note + " Strain capacity = strain at tensile strength (JSCE definition)."})
rows.append(r)
r = dict(P)
r.update(base)
r.update({"Test age (days)": 28, "Compressive strength (MPa)": 136, "Conversions / notes": "M5, 28 d (fc only). " + note})
rows.append(r)

# ---------- 7) Park et al.: M1 / M2 matrices, steel SH-FRCC at static rate
P = {"Article Name": "Matrix-strength-dependent strain-rate sensitivity of strain-hardening fiber-reinforced cementitious composites under tensile impact",
     "Author": "Jun Kil Park, Sung-Wook Kim, Dong Joo Kim", "Year": 2016, "DOI / URL": "https://doi.org/10.1016/j.compstruct.2016.12.022"}
for nm, c, fa, sf, w, sp, smax, eps, matfc in [("M1", 1.00, 0.15, 0.0, 0.35, 0.009, 10.9, 0.8, 56), ("M2", 0.80, 0.20, 0.07, 0.26, 0.04, 11.6, 0.6, 81)]:
    B = c + fa + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B) if sf else None, "W / B": r4(w / B), "SS / B (Silica sand)": r4(1.0 / B), "SP / B": r4(sp / B),
              "Steel fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 1-2 d, demoulded, water curing 20 C for 14 d", "Curing time (days)": 14, "Curing temperature (°C)": 20, "Demolding age (days)": 1,
              "Test age (days)": 16, "Tensile specimen": "bell-shaped (gauge 50 mm, 50 x 25 mm)", "Tensile gauge length (mm)": 50, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": smax, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (matrix, weight ratio), Table 1 (fibres), Table 3 (static rate 0.000333/s, average), sect. 4.1",
              "Conversions / notes": f"{nm} + 1 vol% long hooked (30 x 0.375 mm, 2311 MPa) + 1 vol% short smooth (13 x 0.2 mm, 2788 MPa) steel fibres; fibre dims left blank (two types). "
                                     f"Ratios taken literally as masses (cement type III {c}, FA {fa}, SF {sf}, sand 1.0, water {w}): VERIFY base of the ratios. SP type A (25 % solids) as listed. "
                                     f"Tensile strength = post-cracking strength; matrix fc {matfc} MPa is matrix only (no fibres), not entered. "
                                     "VERIFY: test age 16 d derived (1-2 d before demoulding + 14 d water curing). M3 (UHPC with silica powder) skipped."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e28.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
