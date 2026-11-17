"""Wave 6, agent e26: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e26.csv (99-column TEMPLATE header).
Papers: conbuildmat.2026.145330, dibe.2023.100150, cscm.2024.e03165
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


# ---------- 1) Su et al.: UHPGC with straight steel fibre, 100 mm cube fc
P = {"Article Name": "Shape and size effect on the compressive strength of ultra-high performance geopolymer concrete: Effects of steel fiber and binder material composition",
     "Author": "Jie Su, Wei Huang, Yiwei Liu, Zhi Fang, Caijun Shi", "Year": 2026,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2026.145330"}
# id: (FA, slag, SF, fibre vol%, fc 100 mm cube)
mixes = {"UHPGC-1": (172, 688, 45, 1, 132.1), "UHPGC-2": (172, 688, 45, 2, 144.2), "UHPGC-3": (172, 688, 45, 3, 157.1),
         "UHPGC-4": (154, 615, 136, 2, 123.3), "UHPGC-5": (134, 543, 226, 2, 146.5), "UHPGC-6": (135, 725, 45, 2, 141.6),
         "UHPGC-7": (226, 634, 45, 2, 124.6)}
for mid, (fa, sl, sf, vf, fc) in mixes.items():
    B = fa + sl + sf
    r = dict(P)
    r.update({"GGBS": r4(sl / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B),
              "WG / B (Water glass)": r4(314 / B), "NaOH / B": r4(45 / B), "W / B": r4(87 / B),
              "SS / B (Silica sand)": r4(905 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": vf, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2500,
              "Total fiber (vol%)": vf,
              "Curing method": "24 h in lab 20 C RH 65 %, demoulded, steam chamber 80 C 24 h, then tested",
              "Curing time (days)": 1, "Curing temperature (°C)": 80, "Demolding age (days)": 1, "Test age (days)": 2,
              "Heat curing duration (h)": 24, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix, kg/m3), Table 4/5 (fc, 100 mm cube), sect. 2.2-2.3",
              "Conversions / notes": f"{mid}. kg/m3 / B (FA + slag + SF = {B}). Water-glass (314 kg/m3, modulus/solids not given) and NaOH (45) as dosed; "
                                     "W/B = free water 87 / B only (paper's stated W/B 0.32 includes water of the water glass). Sand 905 natural quartz sand. "
                                     "Fibre: straight 13 mm x 0.2 mm, vol% as stated (78/156/234 kg/m3). Fibre-free UHPGC-0 skipped. "
                                     "VERIFY: test age 2 d derived (24 h precure + 24 h steam, then 'removed for further testing'); "
                                     "other specimen sizes (70, 150 mm cube; prisms) not entered."})
    rows.append(r)

# ---------- 2) Oh et al.: UHP-SHCC, curing RH 30/60/100 % x 7/28/91 d, direct tension (Table A1)
P = {"Article Name": "Influence of curing conditions on mechanical and microstructural properties of ultra-high-performance strain-hardening cementitious composites with strain capacity up to 17.3%",
     "Author": "Taekgeun Oh, Min-Jae Kim, Nemkumar Banthia, Doo-Yeol Yoo", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.dibe.2023.100150"}
B = 926.6 + 463.3 + 154.7
tens = {(30, 7): (9.4, 17.3), (60, 7): (9.8, 14.9), (100, 7): (8.7, 8.9), (30, 28): (8.8, 11.6), (60, 28): (11.4, 10.1),
        (100, 28): (13.3, 6.3), (30, 91): (9.2, 11.5), (60, 91): (10.5, 11.8), (100, 91): (7.8, 6.0)}
for (rh, age), (ts, eps) in tens.items():
    r = dict(P)
    r.update({"OPC / Cement": r4(926.6 / B), "GGBS": r4(463.3 / B), "SF (Silica fume)": r4(154.7 / B),
              "W / B": r4(256.7 / B), "Sand (type not stated) / B": r4(463.4 / B), "SP / B": r4(30.1 / B),
              "Binder content (kg/m³)": round(B, 1), "PE fiber (vol%)": 2.0, "PE tensile strength (MPa)": 3000, "Total fiber (vol%)": 2.0,
              "Curing method": f"sealed 48 h at 20 C, demoulded, then {rh} % RH chamber at 20 C for {age} d, then 24 h at 30 % RH before test",
              "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": rh, "Demolding age (days)": 2, "Test age (days)": age,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dog-bone",
              "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table A1 (direct tension), sect. 2.2",
              "Conversions / notes": f"{rh}%{age}d. kg/m3 / B (OPC + GGBS + SF = {B:.1f}). W/B = free water 256.7 / B (paper's W/B 0.18 apparently includes water of the SP, "
                                     "30.1 kg/m3 SP as dosed). Sand type not stated. UHMWPE fibre 2 vol%, aspect ratio 633 (length/diameter not given). "
                                     "Compressive strength only in figure (not entered). 'Tensile stress' of Table A1 entered as tensile strength. "
                                     "VERIFY: test age = stated 'curing age' (7/28/91 d); unclear whether counted from casting or from demoulding at 48 h."})
    rows.append(r)

# ---------- 3) Cahyati et al.: ECC-control (no bacteria), fc 28 d
P = {"Article Name": "Improving properties of Engineered Cementitious Composite (ECC) using Bacillus subtilis immobilized in silica gel",
     "Author": "Martyana Dwi Cahyati, Wei-Hsing Huang, Hsieh-Lung Hsu, Irfan Prasetyo Loekito", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.cscm.2024.e03165"}
B = 432 + 864
r = dict(P)
r.update({"OPC / Cement": r4(432 / B), "FA (Fly ash)": r4(864 / B), "W / B": r4(298 / B), "SS / B (Silica sand)": r4(467 / B),
          "Sand max size (µm)": 300, "SP / B": r4(9 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 1.6, "PVA length (mm)": 8,
          "PVA diameter (µm)": 40, "Total fiber (vol%)": 1.6, "Curing method": "water curing 28 d", "Curing time (days)": 28,
          "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Compressive strength (MPa)": 30.04,
          "Source table/page": "Table 1 (mix), sect. 3.4 text (fc of ECC-control)",
          "Conversions / notes": f"ECC-control only (Bio-ECC mixes with bacteria skipped). kg/m3 / B (cement + FA = {B}); stated W/B 0.23. "
                                 "Tensile strain (1.37 %) not entered: methods say tensile tests at 56 d, results say 28 d (conflict). "
                                 "VERIFY: water curing temperature not stated; PVA properties in paper look inconsistent (E 1.4 GPa, strength 36 GPa) so not entered."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e26.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
