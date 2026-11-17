"""Wave 6, agent e49: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e49.csv (99-column TEMPLATE header).
Papers: jobe.2026.115921, jobe.2021.102652, jobe.2023.107953, istruc.2021.01.063, engstruct.2018.05.036
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


# ---------- 1) Zhang et al. 2026: HS-ECC with PE (2 vol%) + steel fibre, ambient (30 C) reference
P = paper("Mechanical performance and thermal spalling resistance of PE-steel hybrid fiber-reinforced high strength ECC at elevated temperatures",
          "Zhigang Zhang, Tengxiang Kong, Jianqiao Yu, Rami A. Hawileh, Jamal A. Abdalla, Fengjiang Qin", 2026, "10.1016/j.jobe.2026.115921")
B = 644 + 644 + 112
for nm, st, fc, fcr, ts, eps in [("Ref-ECC", 0, 81.3, 4.48, 6.86, 4.92), ("P2.0S0.2", 0.2, 87.9, 4.62, 7.06, 4.21),
                                 ("P2.0S0.35", 0.35, 92.7, 4.69, 7.15, 4.13), ("P2.0S0.5", 0.5, 96.5, 4.75, 7.24, 4.03)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(644 / B), "FA (Fly ash)": r4(644 / B), "SF (Silica fume)": r4(112 / B), "W / B": r4(280 / B),
              "SS / B (Silica sand)": r4(420 / B), "SP / B": r4(18 / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 26, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120,
              "Total fiber (vol%)": 2.0 + st,
              "Curing method": "sealed in mould 24 h, demoulded, then 20 +/- 2 C and 55 +/- 5 % RH for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 55, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50.8", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 2 (fibres), Table 3 (tensile, 30 C), sect. 3.1 text (fc 30 C), sect. 2.1",
              "Conversions / notes": f"{nm}. Mix in g/L (as in paper), B = cement + FA + SF = {B}. Reference rows = 30 C (ambient) from the elevated-temperature series; "
                                     "VERIFY: 30 C exposure treated as no heating, test age taken as 28 d (end of curing). "
                                     "PE 20 g/L stated as 2.0 vol% (PE-ECC dosage in text)."})
    if st:
        r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850,
                  "Steel elastic modulus (GPa)": 210})
    rows.append(r)

# ---------- 2) Kim et al. 2021: HS-SHCC and dHS-SHCC (2 vol% PE), 28 d; RPC skipped (silica flour)
P = paper("Development of impact resistant high-strength strain-hardening cementitious composites (HS-SHCC) superior to reactive powder concrete (RPC) under flexure",
          "Min-Jae Kim, Hong-Joon Choi, Wonsik Shin, Taekgeun Oh, Doo-Yeol Yoo", 2021, "10.1016/j.jobe.2021.102652")
for nm, pc, bfs, sf, ss, w, sp, fc, ts, eps in [("HS-SHCC", 1201.3, 0, 180.2, 690.7, 257.1, 20.7, 110.9, 10.9, 3.8),
                                                ("dHS-SHCC", 881.5, 440.8, 220.4, 462.8, 249.5, 40.1, 114.6, 10.9, 5.9)]:
    B = pc + bfs + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(pc / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(ss / B),
              "SP / B": r4(sp / B), "Binder content (kg/m³)": round(B, 1),
              "PE fiber (vol%)": 2.0, "PE length (mm)": 19, "PE diameter (µm)": 30, "PE tensile strength (MPa)": 3000, "Total fiber (vol%)": 2.0,
              "Curing method": "covered, 20 C / 60 % RH for 48 h, demoulded, same conditions (air) until 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 60, "Demolding age (days)": 2, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix, kg/m3), Table 2 (fibres), Table A1 (tensile), sect. 3.2-3.3",
              "Conversions / notes": f"{nm}. kg/m3 / B (binder = PC + BFS + SF = {round(B,1)}); BFS = GGBS. Free water only. "
                                     "VERIFY: paper's stated W/B (0.20 / 0.18) matches (water + SP)/B for HS-SHCC (0.201) but not exactly for dHS-SHCC (0.188). "
                                     "Silica-flour column is empty for both SHCC mixes. Fibre 2 vol% PE (text: identical fibre volume fraction 2 %). RPC mix skipped (silica flour = quartz)."})
    if bfs:
        r["GGBS"] = r4(bfs / B)
    rows.append(r)

# ---------- 3) Zhao et al. 2023: PE-HSHDC, static properties
P = paper("Dynamic compressive behavior of polyethylene fiber reinforced high strength and high ductility concrete over wide ranges of strain rate",
          "Xin Zhao, Fei Zhou, Weisheng Wang, Deyu Kong, Jintao Liu, Hao Wu", 2023, "10.1016/j.jobe.2023.107953")
B = 1100 + 310 + 200
r = dict(P)
r.update({"OPC / Cement": r4(1100 / B), "FA (Fly ash)": r4(310 / B), "GGBS": r4(200 / B), "W / B": r4(300 / B),
          "Sand (type not stated) / B": r4(500 / B), "SP / B": r4(25 / B), "Binder content (kg/m³)": B,
          "PE fiber (vol%)": r4(22 / 970 * 100), "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": r4(22 / 970 * 100),
          "Curing method": "20 +/- 3 C for 24 h, demoulded, standard curing room 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
          "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 90, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 123.3, "Tensile strength (MPa)": 9.1, "Tensile strain capacity (%)": 6.6,
          "Source table/page": "Table 3 (matrix mix, kg/m3), Table 4 (PE), sect. 2.1-2.2 text (fc 123.3, ft 9.1, strain 6.6)",
          "Conversions / notes": f"kg/m3 / B (cement + FA + slag = {B}). VERIFY: PE volume = 22 kg/m3 / 970 kg/m3 = 2.27 vol% (derived; not stated as vol%). "
                                 "fc = 70.7 mm cube; tensile at static strain rate 4.8e-5 /s (dumbbell 40 x 50 mm section, 90 mm gauge). Sand type not stated."})
rows.append(r)

# ---------- 4) Hassan et al. 2021: UHPFRC (steel 2 vol%), 2-day strengths given in text
P = paper("The influence of normal curing temperature on the compressive strength development and flexural tensile behaviour of UHPFRC with vipulanandan model quantification",
          "A.M.T. Hassan, G.H. Mahmud, A.S. Mohammed, S.W. Jones", 2021, "10.1016/j.istruc.2021.01.063")
B = 657 + 418 + 119
for T, fc in [(20, 63.1), (30, 83.5)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(657 / B), "GGBS": r4(418 / B), "SF (Silica fume)": r4(119 / B), "W / B": r4(185 / B),
              "SS / B (Silica sand)": r4(1051 / B), "SP / B": r4(40 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Total fiber (vol%)": 2.0,
              "Curing method": f"wrapped in moulds (cling film), submerged in water tank at {T} C; demoulded at 1 d", "Curing time (days)": 2,
              "Curing temperature (°C)": T, "Demolding age (days)": 1, "Test age (days)": 2, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix), sect. 2 (steel fibre), sect. 3.2.1 text (2-d strengths 63.1 and 83.5 MPa)",
              "Conversions / notes": f"kg/m3 / B (cement + GGBS + SF = {B}). Only the 2-d values stated in the text are used (other ages only in Fig. 4). "
                                     "Age counted from mixing. Water curing at the stated temperature (20 or 30 C)."})
    rows.append(r)

# ---------- 5) Hou et al. 2018: steel fibre RPC, quasi-static compression (Table 4)
P = paper("Experimental study on dynamic compressive properties of fiber-reinforced reactive powder concrete at high strain rates",
          "Xiaomeng Hou, Shaojun Cao, Wenzhong Zheng, Qin Rong, Gang Li", 2018, "10.1016/j.engstruct.2018.05.036")
B = 800.5 + 240.2 + 120.1
for nm, st, fc in [("SFRPC2", 2, 108.2), ("SFRPC5", 5, 124.6)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(800.5 / B), "SF (Silica fume)": r4(240.2 / B), "GGBS": r4(120.1 / B), "W / B": r4(232.2 / B),
              "SS / B (Silica sand)": r4(960.6 / B), "SP / B": r4(46.4 / B), "Binder content (kg/m³)": round(B, 1),
              "Steel fiber (vol%)": st, "Steel length (mm)": 13, "Steel diameter (µm)": 220, "Steel tensile strength (MPa)": 2250, "Steel elastic modulus (GPa)": 200,
              "Total fiber (vol%)": st,
              "Curing method": "24 h ambient, then 90 C steam 3 d", "Curing time (days)": 4, "Curing temperature (°C)": 90, "Demolding age (days)": 1,
              "Test age (days)": 4, "Heat curing duration (h)": 72, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "36 x 36",
              "Compressive strength (MPa)": fc, "Source table/page": "Table 1 (mix, kg/m3), Table 4 (quasi-static fc), sect. 2",
              "Conversions / notes": f"{nm}. kg/m3 / B (OPC + SF + GGBS = {round(B,1)}). Quartz sand 0.18-0.6 mm (>99.6 % SiO2) entered as silica sand. "
                                     "VERIFY: test age not stated; set to 4 d = 1 d ambient + 3 d steam; specimens trimmed to 36 mm cylinders before testing. "
                                     "Fibre fraction 2 % / 5 % read as vol%. PRPC (no fibre) and SPFRPC (PP fibre) skipped."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e49.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
