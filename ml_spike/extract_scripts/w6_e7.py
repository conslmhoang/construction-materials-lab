"""Wave 6, agent e7: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e7.csv (99-column TEMPLATE header).
Papers: 10.1016/j.jobe.2024.109854 (random-fiber reference cubes), 10.1016/j.matpr.2022.06.448
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []

# ---------------- 1) Aligned steel fiber UHPC, T-random (conventional) cubes only (109854)
P = {"Article Name": "Anisotropic behavior in the flexural properties of aligned steel fiber UHPC produced by electromagnetic field",
     "Author": "Yongming Xiong, Ming Yang, Yan Yuan, Yan Liu, Jiankai Zhao, Heng Shi", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2024.109854"}
B = 1 + 0.34 + 0.28
for name, L, vf, fc in [("S13-V1.0", 13, 1.0, 133.5), ("S13-V1.5", 13, 1.5, 140.9), ("S13-V2.0", 13, 2.0, 146.6),
                        ("S10-V1.5", 10, 1.5, 136.7), ("S16-V1.5", 16, 1.5, 141.6)]:
    r = dict(P)
    r.update({"OPC / Cement": round(1 / B, 4), "SF (Silica fume)": round(.34 / B, 4), "FA (Fly ash)": round(.28 / B, 4),
              "W / B": 0.17, "Sand (type not stated) / B": round(1.1 / B, 3), "SP / B": round(.018 / B, 4),
              "Steel fiber (vol%)": vf, "Steel length (mm)": L, "Steel diameter (µm)": 200, "Total fiber (vol%)": vf,
              "Curing method": "covered 24 h, demolded, steam curing 90 C RH>=95 % 48 h, then tested",
              "Curing time (days)": 2, "Curing temperature (°C)": 90, "Curing RH (%)": 95, "Demolding age (days)": 1,
              "Test age (days)": 3, "Heat curing duration (h)": 48, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix), Table 2 (cube fc, T-random column), sect. 3.1-3.3 (curing, W/B)",
              "Conversions / notes": f"{name} straight steel fiber (0.2 mm dia, >1800 MPa). Only the T-random (conventional, no magnetic alignment) cubes are used; aligned specimens skipped. "
                                     "Mix by weight ratio to cement 1:0.34:0.28 (cement:SF:FA), sand 1.1 (80 % coarse silica sand + 20 % fine sand), SP 0.018; re-expressed per B = 1.62. "
                                     "VERIFY: test age 3 d derived (24 h mold + 48 h steam, tested after). Sibling paper 10.1016/j.jobe.2024.111092 reports identical cube values with sand 1.7 and water 0.32 (W/B 0.198); W/B 0.17 of this paper used."})
    rows.append(r)

# ---------------- 2) PE-ECC with 60 % GGBS (matpr 448)
P = {"Article Name": "An overview of mechanical properties of engineered cementitious composite (ECC) with different percentages of GGBS",
     "Author": "Fardin Mahmoudi, Jamal A. Abdalla, Rami A. Hawileh, Zhigang Zhang", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.matpr.2022.06.448"}
B = 592 + 888 + 125
r = dict(P)
r.update({"OPC / Cement": round(592 / B, 4), "GGBS": round(888 / B, 4), "SF (Silica fume)": round(125 / B, 4),
          "W / B": round(294 / B, 3), "Sand (type not stated) / B": round(440 / B, 3), "SP / B": round(25 / B, 4),
          "Binder content (kg/m³)": B, "PE fiber (vol%)": 2.06, "Total fiber (vol%)": 2.06,
          "Curing method": "demolded 24 h, then room-temperature curing, tested one year after demolding",
          "Curing time (days)": 365, "Demolding age (days)": 1, "Test age (days)": 366,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dogbone", "Tensile gauge length (mm)": 80,
          "Tensile test type": "direct (uniaxial)", "Compressive strength (MPa)": 59.1, "Tensile strength (MPa)": 7.03,
          "Tensile strain capacity (%)": 6.4,
          "Source table/page": "Table 2 (mix g/l), Table 3 (fc), sect. 3.2/4/5 text (ft, strain, age)",
          "Conversions / notes": "Mix in g/l treated as kg/m3: cement 592, GGBS 888 (60 % of cement+slag), SF 125 (SF added on top), sand 440, water 294, SP 25, PE 20; B = 1605. "
                                 "VERIFY: PE 20 kg/m3 -> 2.06 vol% at 970 kg/m3 (volume not stated in text); test age 'a year after demolding' -> 366 d (approx.); "
                                 "ft 7.03 MPa in sect. 4/5 but abstract says up to 6.6 MPa; sand type/size not stated; short paper partly a review, one own mix."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e7.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e7.csv"))
