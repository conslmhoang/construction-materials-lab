"""Wave 6, agent e33: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e33.csv (99-column TEMPLATE header).
Papers: cemconcomp.2011.03.009, 2020.103862, 2022.104507, 2022.104634, 2022.104681
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


# 1) Cheung & Leung 2011: PC-HSFRCC w/b 0.19 (no SRA), 28-d cube fc
P = paper("Shrinkage reduction of high strength fiber reinforced cementitious composites (HSFRCC) with various water-to-binder ratios",
          "Angus K.F. Cheung, Christopher K.Y. Leung", 2011, "10.1016/j.cemconcomp.2011.03.009")
B = 45 + 11 + 5
r = dict(P)
r.update({"OPC / Cement": r4(45 / B), "FA (Fly ash)": r4(11 / B), "SF (Silica fume)": r4(5 / B), "W / B": 0.19,
          "SS / B (Silica sand)": r4(39 / B), "SP / B": 0.0084, "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 160,
          "Total fiber (vol%)": 2,
          "Curing method": "cubes cast with the shrinkage specimens and cured under the same condition (25 C; 3 d water after demoulding for drying specimens)",
          "Curing time (days)": 28, "Curing temperature (°C)": 25, "Test age (days)": 28, "Compressive specimen": "cube",
          "Compressive strength (MPa)": 138,
          "Source table/page": "Table 1 (mix, % of total mass), Table 4 (28-d cube fc), sect. 2.1-2.3",
          "Conversions / notes": "PC-HSFRCC-0.19 only (SAC mixes and SRA mixes skipped). Mix given in % of total mass: cement 45, FA 11, SF 5, sand 6.3+14.1+18.6 = 39; "
                                 "B = cement + FA + SF = 61 (% of mass). SP/B 0.84 %. "
                                 "VERIFY: cube curing 'same condition' as shrinkage specimens, not clearly stated for 28 d; 25 C taken from the sealed shrinkage specimens. No tensile data."})
rows.append(r)

# 2) Hou et al. 2020: red mud UHPC, reference only, 1-d fc
P = paper("Sustainable use of red mud in ultra-high performance concrete (UHPC): Design and performance evaluation",
          "Dongshuai Hou, Di Wu, Xinpeng Wang, Song Gao, Rui Yu, Mengmeng Li, Pan Wang, Yanshuai Wang", 2020, "10.1016/j.cemconcomp.2020.103862")
B = 750 + 200 + 144
r = dict(P)
r.update({"OPC / Cement": r4(750 / B), "FA (Fly ash)": r4(200 / B), "SF (Silica fume)": r4(144 / B), "W / B": r4(211 / B),
          "River sand / B": r4(900 / B), "SP / B": r4(23 / B), "Binder content (kg/m³)": B,
          "Steel fiber (vol%)": r4(156 / 7850 * 100), "Steel length (mm)": 13, "Steel diameter (µm)": 200,
          "Total fiber (vol%)": r4(156 / 7850 * 100),
          "Curing method": "20 C lime-saturated water", "Curing time (days)": 1, "Curing temperature (°C)": 20, "Test age (days)": 1,
          "Compressive strength (MPa)": 65.7,
          "Source table/page": "Table 2 (mix, kg/m3), sect. 2.2.3 and 3.2.1 (1-d fc of reference)",
          "Conversions / notes": f"Reference mix Ref. only (red mud mixes skipped). kg/m3 / B (cement + FA + SF = {B}). Steel fibre 156 kg/m3 -> 1.99 vol% (7850). "
                                 "VERIFY: stated w/b 0.21 but 211 / 1094 = 0.193 (W/B entered from kg/m3). 28-d reference fc given only as percentages (not absolute), 200 C oven value has no age: not entered."})
rows.append(r)

# 3) Zhang et al. 2022: ECC at 20 C (before heating)
P = paper("Damage mechanism of engineered cementitious composites after exposed to elevated temperatures: Experimental and molecular dynamics study",
          "Jinrui Zhang, Tong Lv, Yu Zhu, Dongshuai Hou", 2022, "10.1016/j.cemconcomp.2022.104507")
B = 1272
r = dict(P)
r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.25, "Sand (type not stated) / B": r4(462 / B), "SP / B": r4(18 / B),
          "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2, "Total fiber (vol%)": 2,
          "Curing method": "demoulded 24 h, standard curing room 20 +/- 2 C, RH 95 +/- 2 % for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "prism 40 x 40 x 160 (halves)", "Compressive strength (MPa)": 95,
          "Source table/page": "Table 2 (mix, kg/m3), sect. 2.1.2-2.1.3, 3.3 (fc at 20 C)",
          "Conversions / notes": "Reference (20 C) row only. kg/m3 / B (OPC + FA = 1272). PVA 2 vol% (26 kg/m3). "
                                 "VERIFY: samples were dried at 100 C for 24 h after 28-d curing before heating tests; unclear whether the 20 C group was dried; fc 95 MPa quoted in text only. "
                                 "Tensile values for 20 C only in Fig. 8 (not entered)."})
rows.append(r)

# 4) Chan & Zhang 2022: SHGC ambient
P = paper("Behaviour of strain hardening geopolymer composites at elevated temperatures", "Choi Lin Chan, Mingzhong Zhang", 2022,
          "10.1016/j.cemconcomp.2022.104634")
naoh_frac = 400 / 1310
r = dict(P)
r.update({"FA (Fly ash)": 0.8, "GGBS": 0.2, "SS / B (Silica sand)": 0.2, "SP / B": 0.01, "WG / B (Water glass)": 0.27,
          "NaOH / B": r4(0.18 * naoh_frac), "NaOH molarity (M)": 10, "W / B": r4(0.18 * (1 - naoh_frac)), "Mixing liquid / B": 0.45,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560,
          "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2,
          "Curing method": "sealed 24 h at 20 +/- 2 C, demoulded, 20 +/- 2 C and 95 % RH for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone",
          "Tensile test type": DIRECT, "Compressive specimen": "cube", "Compressive strength (MPa)": 46.8, "Tensile strength (MPa)": 3.40,
          "First-cracking strength (MPa)": 2.38, "Tensile strain capacity (%)": 3.20,
          "Source table/page": "Table 4 (mix), Table 5 (ambient tensile), sect. 2.1-2.3, 3.2 (fc 46.8 MPa in text)",
          "Conversions / notes": "Ambient (unheated) SHGC only. Alkaline liquid (AL)/B = 0.45, Na2SiO3 sol : NaOH sol = 1.5 -> WG solution 0.27, NaOH solution 0.18 (VERIFY: ratio assumed by mass). "
                                 "WG solution (Na2O 8.5 %, SiO2 26.8 %, H2O 64.7 %) entered as WG / B, its water not counted in W/B. "
                                 "10 M NaOH = 400 g NaOH / L, SG 1.31 -> NaOH 30.5 % of solution: NaOH/B = 0.055, free water 0.125 (derived, VERIFY). Silica sand/B 0.2."})
rows.append(r)

# 5) Shao et al. 2022: dry UHPC with steel fibres, 1/7/28 d fc
P = paper("Investigation on the mechanical characteristics of multiscale mono/hybrid steel fibre-reinforced dry UHPC",
          "Ruizhe Shao, Chengqing Wu, Jun Li, Zhongxian Liu", 2022, "10.1016/j.cemconcomp.2022.104681")
B = 1 + 0.15 + 0.31 + 0.08
LEN = {"S": 6, "M": 10, "L": 13}
mono = {"S": [(0.5, (86.3, 95.9, 104.8)), (1.0, (93.2, 104.1, 113.1)), (1.5, (107.6, 112.4, 126.2)), (2.0, (117.9, 122.0, 135.3))],
        "M": [(0.5, (88.1, 98.3, 106.1)), (1.0, (98.5, 109.3, 120.4)), (1.5, (124.8, 132.5, 141.3)), (2.0, (130.4, 142.0, 152.3))],
        "L": [(0.5, (91.3, 101.1, 108.3)), (1.0, (105.3, 117.8, 128.9)), (1.5, (130.2, 142.3, 153.3)), (2.0, (133.2, 148.7, 162.7))]}
hyb = [("F05S10M", (122.5, 128.0, 139.9)), ("F10S05M", (110.8, 121.9, 133.3)), ("F05S10L", (123.2, 133.7, 144.9)),
       ("F10S05L", (112.6, 124.1, 135.8)), ("F05M10L", (127.8, 138.5, 148.4)), ("F10M05L", (126.2, 136.6, 145.2)),
       ("F05SML", (124.4, 135.6, 144.4))]


def dry_row(name, vol, length, fcs, i, age):
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.15 / B), "FA (Fly ash)": r4(0.31 / B), "GGBS": r4(0.08 / B),
              "W / B": r4(0.25 / B), "SS / B (Silica sand)": r4(2.84 / B), "SP / B": r4(0.03 / B),
              "Steel fiber (vol%)": vol, "Steel diameter (µm)": 120, "Total fiber (vol%)": vol,
              "Curing method": "covered 3 h, then moist/steam 50 C for 21 h, demoulded, then immersed in normal-temperature water until test",
              "Curing time (days)": age, "Curing temperature (°C)": 50, "Heat curing duration (h)": 21, "Test age (days)": age,
              "Compressive specimen": "cube", "Compressive strength (MPa)": fcs[i],
              "Source table/page": "Table 1 (mix, ratio to cement), Table 3 / Table 4 (fc), sect. 2.1-2.2",
              "Conversions / notes": f"{name}. Dry UHPC, mass ratios to cement = 1: SF 0.15, FA 0.31, GGBS 0.08, quartz sand 2.84, water 0.25, SP 0.03 (of cement); B = {r4(B)}; w/b 0.16 as stated. "
                                     "Copper-coated straight steel fibre d = 0.12 mm. Age 1 d = end of 24 h heat cycle. Split-tensile / flexural values not entered. Fibre-free control skipped. "
                                     "VERIFY: cube size not stated."})
    if length:
        r["Steel length (mm)"] = length
    else:
        r["Conversions / notes"] += " Hybrid fibre lengths mixed (6/10/13 mm), length left blank."
    return r


for k, lst in mono.items():
    for vol, fcs in lst:
        for i, age in enumerate((1, 7, 28)):
            rows.append(dry_row(f"F{int(vol * 10):02d}{k} ({vol} vol% of {LEN[k]} mm fibre)", vol, LEN[k], fcs, i, age))
for nm, fcs in hyb:
    for i, age in enumerate((1, 7, 28)):
        rows.append(dry_row(f"{nm} (hybrid, 1.5 vol% total)", 1.5, None, fcs, i, age))

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e33.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows", df["DOI / URL"].nunique(), "papers")
