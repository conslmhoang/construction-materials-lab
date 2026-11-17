"""Wave 6, agent e17: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e17.csv (99-column TEMPLATE header).
Papers: conbuildmat.2021.124562, 2021.124833, istruc.2022.10.008, engstruct.2023.117193,
        matdes.2015.07.125, resconrec.2021.106136
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


# ------------------------------------------------ 1) seawater sea-sand ECC, fibre type/length (124562)
P = {"Article Name": "Experimental study on the mechanical properties of different fiber-reinforced seawater sea-sand engineered cementitious composites",
     "Author": "Chenlong Lin, Siyu Wang, Miao Chen, Yiyan Lu", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.124562"}
B = 472.96 + 141.89 + 614.85
# id, fibre, length, first-crack stress, ultimate stress, ultimate strain (%), all means of Table 5a
for mid, fib, ln, fcr, ult, eps in [("PVA6", "PVA", 6, 2.623, 2.623, 0.014), ("PVA9", "PVA", 9, 3.000, 3.947, 0.903),
                                    ("PVA12", "PVA", 12, 2.405, 3.998, 2.083), ("PVA18", "PVA", 18, 2.448, 2.448, 0.010),
                                    ("PE", "PE", 12, 2.314, 4.047, 3.023)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(472.96 / B), "SF (Silica fume)": r4(141.89 / B), "GGBS": r4(614.85 / B),
              "W / B": r4(368.91 / B), "Sea sand / B": r4(662.15 / B), "HRWR / B": r4(9.84 / B), "Binder content (kg/m³)": r4(B),
              "Curing method": "1 d room temperature, demoulded, standard curing 20+/-2 C RH>=90 % for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": 29,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ult, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Total fiber (vol%)": 1.6, "Source table/page": "Table 3 (mix), Table 2 (fibres), Table 5a (tension), sect. 2.2",
              "Conversions / notes": f"{mid}. kg/m3 / B (cement + SF + GBFS = {B:.2f}). Mixing water is seawater (counted as water); sand is sea-sand. "
                                     "Strength and strain = mean of 3 dog-bone specimens (Table 5a). Compressive strength only in Fig. 6 (not entered). "
                                     "PP-fibre mix skipped. Test age 29 d = 1 d + 28 d curing. "
                                     "VERIFY: PVA6, PVA18 show no strain hardening (ultimate = first-crack values)."})
    if fib == "PVA":
        r.update({"PVA fiber (vol%)": 1.6, "PVA length (mm)": ln, "PVA diameter (µm)": 20, "PVA tensile strength (MPa)": 1300, "PVA elastic modulus (GPa)": 37})
    else:
        r.update({"PE fiber (vol%)": 1.6, "PE length (mm)": ln, "PE diameter (µm)": 14.5, "PE tensile strength (MPa)": 3500, "PE elastic modulus (GPa)": 130})
    rows.append(r)

# ------------------------------------------------ 2) high ductile alkali-activated PE composite, ages 1-120 d (124833)
P = {"Article Name": "Mechanical properties of high ductile alkali-activated fiber reinforced composites with different curing ages",
     "Author": "Lili Kan, Fei Wang, Zhi Zhang, Wilson Kabala, Yujing Zhao", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.124833"}
B = 48.46 + 5.38
# age, ft, strain, first crack, fc (text, only 1 d)
for age, ft, eps, fcr, fc in [(1, 2.92, 2.68, 1.49, 69.7), (3, 3.55, 3.67, 2.08, None), (7, 5.05, 5.74, 2.47, None),
                              (28, 5.77, 5.81, 2.73, None), (56, 5.99, 6.14, 3.04, None), (120, 5.91, 5.99, 2.79, None)]:
    r = dict(P)
    r.update({"GGBS": r4(48.46 / B), "FA (Fly ash)": r4(5.38 / B), "WG / B (Water glass)": r4(13.21 / B), "NaOH / B": r4(2.94 / B),
              "W / B": r4(12.92 / B), "SS / B (Silica sand)": r4(16.15 / B), "PE fiber (vol%)": 2.0, "PE length (mm)": 12,
              "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110, "Total fiber (vol%)": 2.0,
              "Curing method": "24 h room (20 C, RH 70 %), demoulded, 80 C oven 2 h (sealed), then room conditions until test",
              "Curing temperature (°C)": 20, "Curing RH (%)": 70, "Demolding age (days)": 1, "Test age (days)": age, "Heat curing duration (h)": 2,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps, "First-cracking strength (MPa)": fcr,
              "Source table/page": "Table 1 (mix, wt%), Table 3 (PE), Table 5 (tension), sect. 2.2, sect. 3.1 text (fc 1 d)",
              "Conversions / notes": f"Age {age} d. Mix given in wt% of total mix: B = GGBS + FA = {B:.2f}; ratios to B. Na2SiO3 entered as water glass (solution; solids content not stated) "
                                     "and NaOH as given (solid mass assumed); W/B = the 'Water' entry only. fc of other ages only in Fig. 8 (not entered); 1 d fc 69.7 MPa from text. "
                                     "VERIFY: Na2SiO3 is a solution of unstated modulus/solids; sand described as silica sand in text."})
    rows.append(r)

# ------------------------------------------------ 3) HS-ECC with limestone powder, 28 d and 360 d (istruc)
P = {"Article Name": "Long-term stable and sustainable high-strength engineered cementitious composite incorporating limestone powder",
     "Author": "Kequan Yu, Manfang Lin, Likang Tian, Yao Ding", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.istruc.2022.10.008"}
mixes = {"Reference": dict(c=800, lp=0, sf=150, sl=750, sd=500, w=230, ps=25),
         "LP-12.5%": dict(c=700, lp=90, sf=150, sl=750, sd=500, w=230, ps=20),
         "LP-25%": dict(c=600, lp=180, sf=150, sl=750, sd=500, w=230, ps=16),
         "LP-50%": dict(c=400, lp=360, sf=150, sl=750, sd=500, w=230, ps=12)}
# mix, age, fc, ft, strain
for mid, age, fc, ft, eps in [("Reference", 28, 143, 15.16, 6.11), ("Reference", 360, 154, 18.93, None),
                              ("LP-25%", 28, None, None, 8.29), ("LP-50%", 28, 131, 14.83, None), ("LP-50%", 360, 135, None, None)]:
    m = mixes[mid]
    B = m["c"] + m["lp"] + m["sf"] + m["sl"]
    wtot = m["w"] + 0.6 * m["ps"]
    r = dict(P)
    r.update({"OPC / Cement": r4(m["c"] / B), "GGBS": r4(m["sl"] / B), "SF (Silica fume)": r4(m["sf"] / B),
              "Limestone powder": r4(m["lp"] / B) if m["lp"] else None, "W / B": r4(wtot / B), "Sand (type not stated) / B": r4(m["sd"] / B),
              "SP / B": r4(m["ps"] / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 24,
              "PE tensile strength (MPa)": 2400, "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0,
              "Curing method": "not stated (tested at curing age 28 d or 360 d)", "Curing time (days)": age, "Test age (days)": age,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 2 (PE), sect. 3.2 (fc), sect. 3.3-3.4 text (tension)",
              "Conversions / notes": f"HS-ECC-{mid}, {age} d. kg/m3 / B (cement + LP + SF + slag = {B}). W = water 230 + water in PS (60 % of PS) = {wtot:.1f} kg/m3 "
                                     "(reproduces the paper's w*/c). SP = PS as dosed (40 % solids). Numbers from running text only (figures not read). "
                                     "VERIFY: tensile strength 15.7 MPa (ref) / 14.3 MPa (LP-50) in sect. 3.3.1 vs 15.16 / 14.83 in sect. 3.4.1 - the latter used; curing conditions not stated."})
    rows.append(r)

# ------------------------------------------------ 4) UHS-ECC fresh water / seawater (engstruct 117193)
P = {"Article Name": "Ultra-High-Strength Engineered Cementitious Composites (UHS-ECC) panel reinforced with FRP bar/grid: Development and flexural performance",
     "Author": "Ji-Xiang Zhu, Ke-Fan Weng, Bo-Tao Huang, Ling-Yu Xu, Jian-Guo Dai", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.engstruct.2023.117193"}
B = 1.3
for wat, cube, cyl in [("fresh water", 150.4, 130.0), ("seawater", 151.0, 130.8)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.3 / B), "W / B": r4(0.26 / B), "SS / B (Silica sand)": r4(1 / B),
              "SP / B": r4(0.018 / B), "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0, "Curing method": "water 23 C, 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Compressive strength (MPa)": cube,
              "Source table/page": "Table 1 (mix, weight ratio), Table 2 (PE), sect. 2.1, 2.4 (fc)",
              "Conversions / notes": f"UHS-ECC mixed with {wat} (seawater counted as water). Weight ratios to cement; B = cement + SF = 1.3 units. SP is solid content. "
                                     f"Cube fc entered; cylinder (100x200) fc {cyl} MPa. Tensile strain >3 % / strength >6 MPa only stated as inequalities (not entered). "
                                     "VERIFY: test age = 28 d curing (text: all specimens cured 28 d)."})
    rows.append(r)

# ------------------------------------------------ 5) PE-ECC cubes, 7 d (matdes 2015)
P = {"Article Name": "The effect of synthetic polyethylene fiber on the strain hardening behavior of engineered cementitious composite (ECC)",
     "Author": "Shwan H. Said, Hashim Abdul Razak", "Year": 2015,
     "DOI / URL": "https://doi.org/10.1016/j.matdes.2015.07.125"}
B = 820 + 205
for mid, d, vf, fc in [("PE1", 38, 1.0, 65.72), ("PE2", 38, 1.5, 60.52), ("PE3", 38, 2.0, 47.53), ("PE4", 38, 2.5, 43.74),
                       ("PE5", 24, 1.0, 53.44), ("PE6", 24, 1.5, 45.69), ("PE7", 24, 2.0, 41.17), ("PE8", 24, 2.5, 38.36)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(820 / B), "FA (Fly ash)": r4(205 / B), "W / B": r4(379.25 / B), "Sand (type not stated) / B": r4(656 / B),
              "SP / B": 0.00325, "Binder content (kg/m³)": B, "PE fiber (vol%)": vf, "PE length (mm)": 12, "PE diameter (µm)": d,
              "PE tensile strength (MPa)": 1950 if d == 38 else 2700, "PE elastic modulus (GPa)": 39 if d == 38 else 82, "Total fiber (vol%)": vf,
              "Curing method": "not stated", "Test age (days)": 7, "Compressive specimen": "cube",
              "Compressive strength (MPa)": fc, "Source table/page": "Table 1 (fibres), Table 3 (mix), Table 4 (fc), sect. 4.1",
              "Conversions / notes": f"{mid} (fibre diameter {d} um, A.R. {316 if d == 38 else 500}). kg/m3 / B (cement + FA = 1025). fc = mean of 4 cubes at 7 d. "
                                     "VERIFY: SP/B given as 0.3-0.35 %, midpoint 0.325 % entered; cube size and curing not stated; "
                                     "direct tension results only in Figs. 4-5 (not entered)."})
    rows.append(r)

# ------------------------------------------------ 6) UHPC with off-spec fly ash: OSFA-free control with steel fibre (106136)
P = {"Article Name": "Utilization of off-specification fly ash in preparing ultra-high-performance concrete (UHPC): Mixture design, characterization, and life-cycle assessment",
     "Author": "Jiang Du, Zhuo Liu, Christos Christodoulatos, Matthew Conway, Yi Bao, Weina Meng", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.resconrec.2021.106136"}
for age, fc in [(1, 73.4), (28, 104.7)]:
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": r4(260.8 / 1133.1), "Sand (type not stated) / B": r4(953.2 / 1133.1), "HRWR / B": r4(5.8 / 1133.1),
              "Binder content (kg/m³)": 1133.1, "Steel fiber (vol%)": 1.99, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
              "Steel tensile strength (MPa)": 1900, "Steel elastic modulus (GPa)": 203, "Total fiber (vol%)": 1.99,
              "Curing method": "wet burlap + plastic 1 d, demoulded, lime-saturated water 23+/-2 C until test", "Curing temperature (°C)": 23,
              "Demolding age (days)": 1, "Curing time (days)": age, "Test age (days)": age, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (Control mix), sect. 4.2 text (fc 1 d, 28 d)",
              "Conversions / notes": "Control mix (no OSFA, no slag) only; OSFA mixes skipped (off-spec fly ash not in material list). kg/m3 / cement 1133.1. "
                                     "Steel 156 kg/m3 / 7850 = 1.99 vol% (density assumed). HRWR as dosed. fc from running text (control values), figures not read. "
                                     "VERIFY: sand type not stated."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e17.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e17.csv"))
