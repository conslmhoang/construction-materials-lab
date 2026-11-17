"""Wave 6, agent e38: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e38.csv (99-column TEMPLATE header).
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


# ---------- 1) Rawat et al. 2024: PE-steel ECC at elevated temperatures; 20 C reference rows (M4 GGBFS, M5 SF)
P = paper("Development of sustainable engineered cementitious composite with enhanced compressive performance at elevated temperatures using high volume GGBFS",
          "S. Rawat, Y.X. Zhang, D.J. Fanna, C.K. Lee", 2024, "10.1016/j.jclepro.2024.142011")
for nm, comp, B, sand, w, hr, fc in [("M4", {"OPC / Cement": 0.5, "GGBS": 0.5}, 2.0, 0.73, 0.40, 0.04, 143.7),
                                      ("M5", {"OPC / Cement": r4(1 / 1.11), "SF (Silica fume)": r4(0.11 / 1.11)}, 1.11, 0.44, 0.22, 0.02, 153.7)]:
    r = dict(P)
    r.update(comp)
    r.update({"W / B": r4(w / B), "River sand / B": r4(sand / B), "HRWR / B": r4(hr / B), "PE fiber (vol%)": 1.5, "Steel fiber (vol%)": 0.75,
              "Total fiber (vol%)": 2.25,
              "Curing method": "fog room 23 C / 95 % RH 28 d, then environmental room 20 C / 55 % RH 28 d (20 C control of residual-strength tests)",
              "Curing time (days)": 56, "Curing temperature (°C)": 23, "Curing RH (%)": 95, "Test age (days)": 56,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75 x 150", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix, weight ratio to cement), Table 2 (fc at 20 C), sect. 2.3",
              "Conversions / notes": f"{nm}. Weight ratios to cement (Table 1); B = {B}. PE / steel in vol% of mix (1.5 / 0.75). "
                                     "VERIFY: test age 56 d = 28 d fog room + 28 d drying room, derived from curing text (the 20 C specimens are not explicitly said to be tested at 56 d). "
                                     "Table 1 column layout is garbled (M4 read as cement 1, GGBFS 1.00, sand 0.73, water 0.40, HRWR 0.04). Sand = river sand (Table 3). "
                                     "M1-M3 skipped (dolomite powder). Fibre dimensions not given in text."})
    rows.append(r)

# ---------- 2) Yan et al. 2019: UHPC (steel microfibre 2 vol%) for UHPC-filled steel tubes, cube fcu at 28 d
P = paper("Axial behavior of ultra-high performance concrete (UHPC) filled stocky steel tubes with square sections",
          "Yanxiang Yan, Lihua Xu, Biao Li, Yin Chi, Min Yu, Kaikai Zhou, Yang Song", 2019, "10.1016/j.jcsr.2019.03.018")
for nm, w, c, sf, fa, fcu in [("UHPC-100", 200, 700, 150, 150, 102.4), ("UHPC-110", 180, 700, 100, 200, 111.0),
                              ("UHPC-120", 170, 750, 150, 100, 124.8), ("UHPC-140", 160, 800, 50, 150, 141.0)]:
    B = c + sf + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B),
              "River sand / B": r4(1220 / B), "SP / B": r4(30 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2.0,
              "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Total fiber (vol%)": 2.0,
              "Curing method": "covered with plastic membrane, self-cured under natural environment 28 d, then demoulded and tested",
              "Curing time (days)": 28, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Compressive strength (MPa)": fcu,
              "Source table/page": "Table 2 (mix, kg/m3), Table 3 (fcu), sect. 2.1.2 and 2.1.3",
              "Conversions / notes": f"{nm}. kg/m3 / B (C + SF + FA = {B}). Cube strength fcu (prism fck not used). Steel microfibre 2.0 vol%, 13 mm x 0.2 mm (text). "
                                     "Temperature / RH of 'natural environment' not stated. PS entered as SP / B. Natural river sand."})
    rows.append(r)

# ---------- 3) Al-Osta et al. 2021: UHPC, straight / hooked steel fibre hybrids, steam vs water curing
P = paper("Effect of hybridization of straight and hooked steel fibers and curing methods on the key mechanical properties of UHPC",
          "Mohammed A. Al-Osta, Abdulrahman Mohammed Sharif, Shamsad Ahmad, Saheed Kolawole Adekunle, Mohammed Al-Huri, Abdulla Mohammed Sharif",
          2021, "10.1016/j.jmrt.2021.10.005")
B = 900 + 220
for nm, hooked, fcs, fcw in [("U0H", 0, 159.50, 149.50), ("U30H", 30, 148.52, 131.48), ("U50H", 50, 148.40, 134.81),
                             ("U70H", 70, 144.32, 127.32), ("U100H", 100, 143.09, 127.77)]:
    for cur, fc in [("SC", fcs), ("WC", fcw)]:
        r = dict(P)
        r.update({"OPC / Cement": r4(900 / B), "SF (Silica fume)": r4(220 / B), "W / B": r4(163 / B), "Sand (type not stated) / B": r4(1005 / B),
                  "SP / B": r4(40 / B), "Binder content (kg/m³)": B, "Steel fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
                  "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2500, "Steel elastic modulus (GPa)": 200,
                  "Test age (days)": 28, "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 1 (mix, kg/m3), Table 5 (fibre split), Table 7 (fc), sect. 2.3",
                  "Conversions / notes": f"{nm}-{cur}. kg/m3 / B (cement + micro-silica = {B}). Total steel 157 kg/m3 = 2 vol%; {100 - hooked} % straight (13 mm) + {hooked} % hooked (25 mm), both 0.2 mm dia. "
                                         "Specimen shape for compression not stated. Test day 'after 28 days' in lab air following curing (text). Sand type not stated."})
        if hooked == 0:
            r["Steel length (mm)"] = 13
        if hooked == 100:
            r["Steel length (mm)"] = 25
        if cur == "WC":
            r.update({"Curing method": "water immersion 28 d at 23 +/- 2 C", "Curing time (days)": 28, "Curing temperature (°C)": 23})
        else:
            r.update({"Curing method": "steam (water vapour in oven) 90 C for 10 h, cooled, then laboratory air until test at 28 d", "Curing temperature (°C)": 90,
                      "Heat curing duration (h)": 10})
        rows.append(r)

# ---------- 4) Wang et al. 2023: high-strength PVA-ECC (control group PO only; carbon-fibre mixes skipped), 7 d and 28 d fc at room temperature
P = paper("Carbon fiber to improve the resistance of high strength PVA-ECC to elevated temperatures",
          "Qing Wang, Yuxuan Zhou, Mianheng Lai, Meixiang Gu, J.C.M. Ho", 2023, "10.1016/j.jobe.2023.106475")
B = 520 + 624
for age, fc in [(7, 57.3), (28, 83.1)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(520 / B), "FA (Fly ash)": r4(624 / B), "W / B": r4(229 / B), "SS / B (Silica sand)": r4(915 / B),
              "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 15, "PVA tensile strength (MPa)": 1780,
              "PVA elastic modulus (GPa)": 39, "Total fiber (vol%)": 2.0,
              "Curing method": "standard curing per ISO 679 (VERIFY: temperature / RH not given in text)", "Curing time (days)": age, "Test age (days)": age,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 2 (fibres), Table 4 (fc), sect. 2.2",
              "Conversions / notes": "Group PO (2.0 vol% PVA, no carbon fibre). kg/m3 / B (cement + FA = 1144); w/b 0.20, sand/binder 0.8. Quartz sand used as sand. "
                                     "VERIFY: curing only 'according to ISO 679'. No superplasticizer listed. PC I / PC II (carbon fibre) skipped. Heated specimens not used."})
    rows.append(r)

# ---------- 5) Tai & Lee 2025: UHPC with blended steel fibres, direct tension at 25 C (unheated reference)
P = paper("Tensile behavior and damage mechanisms of ultra-high-performance concrete with blended steel fibers under elevated temperatures",
          "Yuh-Shiou Tai, Ming-Hui Lee", 2025, "10.1016/j.jobe.2025.112742")
B = 0.5 + 0.5 + 0.25
for nm, s, m, scc, spc, epc in [("S2.0", 2.0, 0, 5.8, 9.3, 0.48), ("S1.5M0.5", 1.5, 0.5, 6.4, 8.3, 0.54),
                                ("S0.5M1.5", 0.5, 1.5, 7.6, 9.3, 0.43), ("M2.0", 0, 2.0, 7.0, 8.8, 0.36)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(0.5 / B), "GGBS": r4(0.5 / B), "SF (Silica fume)": r4(0.25 / B), "W / B": r4(0.2 / B), "SS / B (Silica sand)": r4(0.78 / B),
              "HRWR / B": r4(0.05 / B), "Steel fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 24 h room temperature, then water tank 27 d, then room temperature until test day (25 C series)",
              "Curing time (days)": 28, "Test age (days)": 28, "Tensile specimen": "dog-bone (25 x 25 mm section)", "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": scc, "Tensile strength (MPa)": spc, "Tensile strain capacity (%)": epc,
              "Source table/page": "Table 1 (mix, weight ratio), Table 2 (fibres), Table 3 (25 C row), sect. 2.2",
              "Conversions / notes": f"{nm} (S = straight smooth 25 mm x 0.3 mm, M = micro 13 mm x 0.2 mm; {s} vol% S + {m} vol% M). "
                                     "Weight ratios OPC 0.5 : GGBFS 0.5 : SF 0.25 : sand 0.78 : HRWR 0.05, w/c 0.2 on cement + GGBFS (=1), so B = 1.25 and W/B = 0.16. "
                                     "Tensile strength = post-cracking (peak) stress, strain = strain at that stress. "
                                     "VERIFY: test age 28 d derived from 1 d + 27 d water curing ('designated testing day' not stated); HRWR basis assumed as the same unit mass as the other ratios."})
    if s and not m:
        r.update({"Steel length (mm)": 25, "Steel diameter (µm)": 300, "Steel tensile strength (MPa)": 2850})
    if m and not s:
        r.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850})
    rows.append(r)

# ---------- 6) Zhang et al. 2022: reference ECC P0S0 (no SAP, no nano-silica) 28 d direct tension
P = paper("Mechanical property and durability of engineered cementitious composites (ECC) with nano-material and superabsorbent polymers",
          "Minghu Zhang, Xuezhen Zhu, Baoju Liu, Jinyan Shi, Osman Gencel, Togay Ozbakkaloglu", 2022, "10.1016/j.powtec.2022.117839")
r = dict(P)
r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.25, "SS / B (Silica sand)": 0.365, "SP / B": 0.0015,
          "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "Total fiber (vol%)": 2.0, "Test age (days)": 28,
          "Tensile test type": DIRECT, "First-cracking strength (MPa)": 4.17, "Tensile strength (MPa)": 5.11, "Tensile strain capacity (%)": 1.5,
          "Source table/page": "Table 3 (mix, ratio to PC), Table 4 (28-d tensile)",
          "Conversions / notes": "Reference mix P0S0 only (SAP / nano-silica mixes skipped). Ratios PC 1 : FA 1 : sand 0.73 : total water 0.5 : SP 0.003, B = 2. "
                                 "Curing method and specimen type for tension not described in the text (28-d stated in Table 4 title). VERIFY: Table 3 'Fiber 0.041' is mass ratio, entered 2 vol% from text. Fine silica sand."})
rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e38.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows", df["DOI / URL"].nunique(), "papers")
