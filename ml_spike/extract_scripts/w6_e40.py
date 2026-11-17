"""Wave 6, agent e40: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e40.csv (99-column TEMPLATE header).
Papers: conbuildmat.2017.07.193, 2018.01.166, 2018.03.243, 2019.07.047
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


# ---------- 1) Huang et al. 2017: PVA-ECC, 28-d properties (Table 4)
P = paper("Experimental study on crack bridging in engineered cementitious composites under fatigue tensile loading",
          "Ting Huang, Y.X. Zhang, S.R. Lo, C.K. Lee", 2017, "10.1016/j.conbuildmat.2017.07.193")
B = 1 + 1.2
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(1.2 / B), "W / B": r4(0.65 / B), "Sand (type not stated) / B": r4(0.8 / B),
          "HRWR / B": r4(0.01 / B), "PVA fiber (vol%)": 2.2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
          "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2.2,
          "Curing method": "demoulded after 24 h, then 100 % RH and 23 C until testing", "Curing time (days)": 28, "Curing temperature (°C)": 23,
          "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Compressive strength (MPa)": 56, "Tensile strength (MPa)": 5.26,
          "Tensile strain capacity (%)": 1.01, "Source table/page": "Table 3 (mix, weight ratios), Table 2 (PVA), Table 4 (28 d properties), sect. 2.1-2.2",
          "Conversions / notes": "Weight ratios C : FA : sand : water : HRWRA = 1 : 1.2 : 0.8 : 0.65 : 0.01, B = 2.2. Fine sand max 300 um. "
                                 "VERIFY: curing (24 h, 100 % RH 23 C until test) is stated for the fatigue dog-bone specimens, assumed for the 28-d property specimens of Table 4."})
rows.append(r)

# ---------- 2) Khan et al. 2018: ambient-cured FA/slag geopolymer, plain and hybrid-fibre (FRGC)
P = paper("Experimental evaluation of quasi-static and dynamic compressive properties of ambient-cured high-strength plain and fiber reinforced geopolymer composites",
          "Musaad Zaheer Nazir Khan, Yifei Hao, Hong Hao, Faiz Uddin Ahmed Shaikh", 2018, "10.1016/j.conbuildmat.2018.01.166")
B = 412 + 276
naoh_sol = 117.72
naoh_solid = naoh_sol * 480 / 1370   # 12 M NaOH: 480 g/L, assumed density 1.37 g/mL
for nm, fib, vals in [("Plain geopolymer matrix", False, {28: 95, 60: 112}),
                      ("FRGC (spiral steel 0.8 + hooked steel 0.8 + HSPE 0.4 vol%)", True, {28: 88, 60: 114})]:
    for age, fc in vals.items():
        r = dict(P)
        r.update({"FA (Fly ash)": r4(412 / B), "GGBS": r4(276 / B), "WG / B (Water glass)": r4(294.3 / B), "NaOH / B": r4(naoh_solid / B),
                  "NaOH molarity (M)": 12, "W / B": r4((naoh_sol - naoh_solid) / B), "SS / B (Silica sand)": r4(1100 / B),
                  "Binder content (kg/m³)": B,
                  "Curing method": "sealed with cling sheet, ambient curing room 23 +/- 2 C, RH 50 +/- 5 %; cylinders cut after ~21 d",
                  "Curing time (days)": age, "Curing temperature (°C)": 23, "Curing RH (%)": 50, "Test age (days)": age,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "76 x 154", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 3 (mix), Table 2 (fibres), sect. 2.1-2.2, 3.1 (fc 60 d and 28 d reference)"})
        if fib:
            r.update({"Steel fiber (vol%)": 1.6, "Steel length (mm)": 25, "Steel diameter (µm)": 300, "Steel tensile strength (MPa)": 2500,
                      "Steel elastic modulus (GPa)": 200, "PE fiber (vol%)": 0.4, "PE length (mm)": 12, "PE diameter (µm)": 12,
                      "PE tensile strength (MPa)": 3500, "PE elastic modulus (GPa)": 123, "Total fiber (vol%)": 2.0})
        r["Conversions / notes"] = (
            f"{nm}, {age} d. B = FA + slag = {B} kg/m3. Water glass D-grade (SiO2 29.4 %, Na2O 14.7 %, H2O 55.9 %, Ms 2.0) as dosed 294.3 kg/m3, its water not in W/B. "
            "12 M NaOH solution 117.72 kg/m3. VERIFY (derived): NaOH solid = 480 g/L / assumed density 1.37 g/mL, i.e. 35 % of solution = 41.2 kg/m3; "
            "W/B = water of the NaOH solution only (paper w/s = 0.28 is defined differently). "
            "Steel fibres: two types (spiral 25 mm x 550 um 2000 MPa; hooked 25 mm x 300 um 2500 MPa), 0.8 vol% each; hooked-end dimensions entered. "
            "60 d = age of the quasi-static tests, 28 d = reference strength quoted in text (95 / 88 MPa), curing assumed identical. "
            "No SP, no extra water. Silica sand FM 2.77, SSD.")
        rows.append(r)

# ---------- 3) Azreen et al. 2018: UHPC with silica sand (SS-UHPC), steel fibres
P = paper("Radiation shielding of ultra-high-performance concrete with silica sand, amang and lead glass",
          "N.M. Azreen, Raizal S.M. Rashid, M. Haniza, Y.L. Voo, Y.H. Mugahed Amran", 2018, "10.1016/j.conbuildmat.2018.03.243")
B = 825 + 200
r = dict(P)
r.update({"OPC / Cement": r4(825 / B), "SF (Silica fume)": r4(200 / B), "W / B": r4(164 / B), "SS / B (Silica sand)": r4(1000 / B),
          "SP / B": r4(40 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": r4(120 / 7840), "Steel length (mm)": 20, "Steel diameter (µm)": 200,
          "Steel tensile strength (MPa)": 2500, "Total fiber (vol%)": r4(120 / 7840),
          "Curing method": "curing compound, demoulded after 24 h, 90 C hot-water tank 3 d; then until test (not stated)", "Curing time (days)": 4,
          "Curing temperature (°C)": 90, "Demolding age (days)": 1, "Test age (days)": 28, "Heat curing duration (h)": 72,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": 165.7,
          "Source table/page": "Table 2 (mix), Table 3 (W/B), Table 4 (fc 28 d), sect. 2-3",
          "Conversions / notes": "SS-UHPC only (amang and lead-glass mixes skipped, not allowed aggregates). kg/m3 / B (OPC + SF = 1025). "
                                 "Free water 164 kg/m3 (+30 kg/m3 moisture of sand listed separately, not in W/B). "
                                 "VERIFY: steel fibre 120 kg/m3 = 1.53 vol% (table says 0.75 % straight + 0.75 % hooked-end), while the text says 0.5 + 0.5 vol%; "
                                 "fibres 20 x 0.2 mm straight and 25 x 0.3 mm hooked, dimensions of the straight type entered. Silica sand as sand."})
rows.append(r)

# ---------- 4) Song et al. 2019: UHPFRC, SF vs metakaolin, 28-d compressive strength
P = paper("Physical and chemical coupling effect of metakaolin induced chloride trapping capacity variation for Ultra High Performance Fibre Reinforced Concrete (UHPFRC)",
          "Qiulei Song, Rui Yu, Zhonghe Shui, Yunyao Wang, Suduan Rao, Shuo Wu, Yongjia He", 2019, "10.1016/j.conbuildmat.2019.07.047")
B = 754 + 306 + 90
for nm, sf, mk, fc in [("MK0", 90, 0, 151.3), ("MK40", 54, 36, 159.4), ("MK100", 0, 90, 155.3)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(754 / B), "FA (Fly ash)": r4(306 / B), "SF (Silica fume)": r4(sf / B), "Metakaolin": r4(mk / B),
              "W / B": r4(198 / B), "Sand (type not stated) / B": r4((565 + 386) / B), "SP / B": r4(33 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": r4(156 / 7850), "Total fiber (vol%)": r4(156 / 7850), "Test age (days)": 28, "Curing time (days)": 28,
              "Compressive strength (MPa)": fc, "Source table/page": "Table 2 (recipe kg/m3 and 28 d compressive strength)",
              "Conversions / notes": f"{nm}. kg/m3 / B (C + FA + SF + MK = {B}); sand = sand 0-0.6 mm 565 + sand 0.6-1.25 mm 386. "
                                     "VERIFY: steel fibre 156 kg/m3 converted to vol% with 7850 kg/m3 (straight steel fibres, dimensions not given); "
                                     "curing regime and specimen type of the 28 d compressive test not stated (7 d at 20 C only for RCM samples); "
                                     "MK40 = 40 % of SF replaced by MK."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e40.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
