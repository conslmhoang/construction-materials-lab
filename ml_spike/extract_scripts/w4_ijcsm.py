# Builder for w4_ijcsm.csv -- ECC / SHCC / UHPC / HPFRCC / fibre-reinforced AAM papers from the SpringerOpen journal
# "International Journal of Concrete Structures and Materials" (IJCSM, DOI 10.1186/s40069-... / 10.1007/s40069-...).
# All numbers transcribed from the article HTML + table pages (ijcsm.springeropen.com/articles/<doi>/tables/<n>).
import os, csv, re, glob
import pandas as pd

NAME = "w4_ijcsm"
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
with open(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig") as f:
    H = next(csv.reader(f))

BINDER_COLS = ["OPC / Cement", "SAC (Calcium sulfoaluminate cement)", "CAC (Calcium aluminate cement)", "GGBS",
               "FA (Fly ash)", "SF (Silica fume)", "Metakaolin", "Limestone powder", "Diatomite", "Nano-SiO2",
               "Recycled powder (C&D waste)", "Dolomite powder", "Pond ash (PA)", "Other binder", "RHA (Rice husk ash)",
               "EAFD (Electric arc furnace dust)", "Reactive MgO", "CKD (Cement kiln dust)"]
FIB = ["PE fiber (vol%)", "PVA fiber (vol%)", "Steel fiber (vol%)", "PBO fiber (vol%)", "PP fiber (vol%)", "Glass fiber (vol%)",
       "PET fiber (vol%)", "Basalt fiber (vol%)", "Carbon fiber (vol%)"]
rows = []


def r4(x):
    return round(x, 4) if isinstance(x, float) else x


def add(base, **kw):
    d = dict(base)
    d.update(kw)
    for k in d:
        assert k in H, k
    s = sum(float(d.get(k) or 0) for k in BINDER_COLS)
    assert abs(s - 1) < 0.002, (d["Article Name"], s)
    if d.get("Total fiber (vol%)", "") == "":
        d["Total fiber (vol%)"] = sum(float(d.get(k) or 0) for k in FIB)
    rows.append({k: r4(v) for k, v in d.items()})


def doi(x):
    return "https://doi.org/" + x


# ---------------------------------------------------------------- P1 Hashim et al. 2020 (UHPFRC, 3 fibre types, dog-bone)
p = {"Article Name": "Simplified Constitutive and Damage Plasticity Models for UHPFRC with Different Types of Fiber",
     "Author": "Hashim D.T.; Hejazi F.; Lei V.Y.", "Year": 2020, "DOI / URL": doi("10.1186/s40069-020-00418-9"),
     "OPC / Cement": 850 / 1050, "SF (Silica fume)": 200 / 1050, "W / B": 140 / 1050, "SS / B (Silica sand)": (695 + 295) / 1050,
     "Binder content (kg/m³)": 1050, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75x150",
     "Tensile specimen": "un-notched dog-bone, 200 mm long, ends 50x50, narrow section 26x50 (prismatic length 126 or 76 mm)",
     "Tensile test type": "direct", "Curing method": "not described (tested at 7/14/28 'curing days')",
     "Source table/page": "Table 1 (mix), Tables 3/5/7 (tension + compression); Sect. 3 text (fibres, specimens)"}
B1 = ("Table 1 kg/m3: cement 850, densified SF 200, dry silica fine sand 30/100 695 + coarse sand 16/30 295, 'Silica VC2644' 40 "
      "(product not identified -> not entered; possibly Sika ViscoCrete SP), free water 140 (+30.93 '3% moisture', not added). "
      "B = cement+SF = 1050; W/B = free water/B. Tensile strain = strain at max tensile stress (Table, µε/10^4 -> %); strain "
      "taken over the tapered-section length. ")
for mid, fib, kw, data in [
    ("T1", "Copper-coated micro steel (20 mm, 0.2 mm, >2300 MPa) + hooked-end steel (25 mm, 0.3 mm, >2500 MPa), total 158 kg/m3 -> 158/7850 = 2.01 vol% (split not given).",
     {"Steel fiber (vol%)": 158 / 7850 * 100}, [(7, 5.68, 2775, 211.27), (14, 7.75, 1028, 219.38), (28, 9.34, 3126, 242.61)]),
    ("T2", "Bekaert Dramix 5D steel 60 kg/m3 -> 60/7850 = 0.76 vol%; 60 mm, 0.9 mm dia.",
     {"Steel fiber (vol%)": 60 / 7850 * 100, "Steel length (mm)": 60, "Steel diameter (µm)": 900},
     [(7, 5.48, 1473, 125.63), (14, 5.61, 4523, 126.84), (28, 7.75, 4665, 133.59)]),
    ("T3", "Forta-Ferro macro synthetic (virgin PP + copolymer, 54 mm, 570-660 MPa) 1 kg/m3 -> 1/910 = 0.11 vol% (PP density assumed).",
     {"PP fiber (vol%)": 1 / 910 * 100, "PP length (mm)": 54}, [(7, 5.42, 3727, 101.85), (14, 5.64, 4072, 118.47), (28, 6.509, 2867, 126.84)]),
]:
    for age, ft, eps, fc in data:
        add(p, **kw, **{"Test age (days)": age, "Curing time (days)": age, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
                        "Tensile strain capacity (%)": eps / 1e4, "Conversions / notes": f"Mix {mid}. " + B1 + fib})

# ---------------------------------------------------------------- P2 Lee et al. 2026 (UHPC Vf 0/1/2 %, notched dog-bone)
p = {"Article Name": "Tension Stiffening Effect of Reinforced Ultra-high-Performance Concrete Members in Tension with Thin Cover Thickness",
     "Author": "Lee M.-S.; Bae B.-I.; Son D.-H.; Song S.H.; Bae S.-C.; Choi C.-S.", "Year": 2026, "DOI / URL": doi("10.1186/s40069-026-00894-5"),
     "OPC / Cement": 780 / 1200, "GGBS": 240 / 1200, "SF (Silica fume)": 180 / 1200, "W / B": 0.2,
     "Sand (type not stated) / B": 1020 / 1200, "SP / B": 18.4 / 1200, "Binder content (kg/m³)": 1200,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
     "Tensile specimen": "dog-bone with mid-span notch", "Tensile test type": "direct",
     "Source table/page": "Table 1 (mix), Table 2 (fc), Table 3 (direct tension)"}
for vf, fc, fcr, ft in [(0, 129.0, 4.04, 4.04), (1, 125.6, 4.95, 6.76), (2, 119.1, 7.03, 9.95)]:
    add(p, **{"Steel fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr,
              "Conversions / notes": f"Vf = {vf}%. Table 1 kg/m3: W 210, C 780, slag 240, SF 180, sand 1020, SP 18.4 -> /B (1200). "
                                     "Paper states W/B 0.2 (210/1200 = 0.175; entered as stated). Steel fibre column in Table 1 lists 24.5 / 49.0 for Vf 1 / 2 % "
                                     "(units unclear); vol% as stated. Fibre geometry, curing regime and test age not given. Averages of 3 specimens; "
                                     "first-cracking = f'dt,initial avg; peak = f'dt,peak avg (Vf 0 brittle, initial = peak)."})

# ---------------------------------------------------------------- P3 Lim et al. 2025 (SHCC + alkali-activated slag fibre composite)
p = {"Article Name": "Structural Performances of Reinforced Alkali-Activated Slag Fiber Composite Walls",
     "Author": "Lim H.-J.; Cho C.-G.; Lee S.-J.; Kang J.-W.", "Year": 2025, "DOI / URL": doi("10.1186/s40069-025-00811-2"),
     "Sand max size (µm)": "", "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 37,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "50x50x50", "Tensile specimen": "dog-bone (Kim et al. 2007)",
     "Tensile test type": "direct", "Test age (days)": 28, "Demolding age (days)": 3,
     "Source table/page": "Table 1 (mix), Table 3 (fibre), Table 4 (fc), Table 5 (direct tension)"}
add(p, **{"OPC / Cement": 0.6, "GGBS": 0.2, "FA (Fly ash)": 0.2, "W / B": 0.45, "SS / B (Silica sand)": 0.83, "PVA fiber (vol%)": 2.0,
          "Compressive strength (MPa)": 38.40, "Tensile strength (MPa)": 4.14, "First-cracking strength (MPa)": 2.86, "Tensile strain capacity (%)": 3.22,
          "Curing method": "not stated for SHCC200 (ASFC: water 23+/-3 C, 28 d)",
          "Conversions / notes": "Mix SHCC200. Table 1 mass ratios of binder. Sand assumed silica sand (avg 100 µm, described for ASFC). "
                                 "HRWRA/VMA/defoamer used, dosages not given. SHCC data originally from Kim et al. 2021 / Lim et al. 2022."})
add(p, **{"GGBS": 1.0, "Ca(OH)2 / B": 0.075 / 0.895, "Na2SO4 / B": 0.03 / 0.895, "W / B": 0.338 / 0.895, "SS / B (Silica sand)": 0.40 / 0.895,
          "PVA fiber (vol%)": 1.5, "Curing method": "water 23+/-3 C until 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23,
          "Compressive strength (MPa)": 33.70, "Tensile strength (MPa)": 3.80, "First-cracking strength (MPa)": 2.76, "Tensile strain capacity (%)": 4.93,
          "Conversions / notes": "Mix ASFC150. Paper binder = GGBS 0.895 + Ca(OH)2 0.075 + Na2SO4 0.03, W/(total) 0.338, sand 0.40; re-based on GGBS "
                                 "(B = GGBS): Ca(OH)2/B = 0.0838, Na2SO4/B = 0.0335, W/B = 0.378, SS/B = 0.447. Silica sand avg 100 µm. "
                                 "HRWRA/VMA/defoamer dosages not given."})

# ---------------------------------------------------------------- P4 Wang et al. 2021 (ECC matrix of HSSSWR-reinforced ECC)
p = {"Article Name": "Tensile Behavior of High-Strength Stainless Steel Wire Rope (HSSSWR)-Reinforced ECC",
     "Author": "Wang X.; Yang G.; Qian W.; Li K.; Zhu J.", "Year": 2021, "DOI / URL": doi("10.1186/s40069-021-00480-x"),
     "OPC / Cement": 1 / 5.08, "FA (Fly ash)": 4 / 5.08, "SF (Silica fume)": 0.08 / 5.08, "W / B": 1 / 5.08, "SS / B (Silica sand)": 0.3 / 5.08,
     "SP / B": 0.06 / 5.08, "PVA fiber (vol%)": 2.0, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7x70.7x70.7",
     "Tensile specimen": "thin plate 280x40x15", "Tensile test type": "direct",
     "Source table/page": "Table 2 (mix), Table 3 (ECC properties)"}
N4 = ("Table 2 mass ratios to cement: cement 1, silica sand 0.3, FA 4, SF 0.08, water 1, SP 0.06, thickener {t}; PVA 2 vol%. "
      "B = 1+4+0.08 = 5.08; ratios /5.08. PVA geometry, curing and test age not given.")
add(p, **{"Compressive strength (MPa)": 44.65, "Tensile strength (MPa)": 3.53, "First-cracking strength (MPa)": 2.19, "Tensile strain capacity (%)": 2.79,
          "Conversions / notes": "Formula 1. " + N4.format(t=0)})
add(p, **{"VMA / B": 0.006 / 5.08, "Compressive strength (MPa)": 36.05, "Tensile strength (MPa)": 3.46, "First-cracking strength (MPa)": 1.92,
          "Tensile strain capacity (%)": 2.97, "Conversions / notes": "Formula 2 (with thickener, entered as VMA). " + N4.format(t=0.006)})

# ---------------------------------------------------------------- P5 Hou et al. 2019 (hybrid / PP fibre RPC, steam cured)
p = {"Article Name": "Effects of Temperature and Stress on Creep Behavior of PP and Hybrid Fiber Reinforced Reactive Powder Concrete",
     "Author": "Hou X.; Abid M.; Zheng W.; Hussain R.R.", "Year": 2019, "DOI / URL": doi("10.1186/s40069-019-0357-9"),
     "W / B": 0.16, "PP length (mm)": 19, "PP diameter (µm)": 45,
     "Curing method": "24 h at 25 C / 70% RH, demoulded, steam cured 72 h at 90 C, then lab conditions 60 d",
     "Curing temperature (°C)": 90, "Heat curing duration (h)": 72, "Demolding age (days)": 1,
     "Source table/page": "Table 2 (mix), Table 5 (room-temperature fc); Sect. 2 text (materials, curing)"}
add(p, **{"OPC / Cement": 815.18 / 1180.57, "SF (Silica fume)": 245.31 / 1180.57, "GGBS": 120.08 / 1180.57,
          "SS / B (Silica sand)": 960.64 / 1180.57, "SP / B": 35.40 / 1180.57, "Binder content (kg/m³)": 1180.57,
          "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 220, "Steel tensile strength (MPa)": 2850,
          "Steel elastic modulus (GPa)": 200, "PP fiber (vol%)": 0.2, "Compressive strength (MPa)": 151.1,
          "Conversions / notes": "HRPC (paper label HPRPC in Table 2). kg/m3: OPC 815.18, SF 245.31, slag 120.08, quartz coarse + fine sand 480.32+480.32, "
                                 "water reducer 35.40, PP 1.82 (0.2%), steel 157 (2%), water 188.81; w/b 0.16 (paper). fc = room-temperature "
                                 "compressive strength (Table 5); specimen size / test age not stated. PP length 18-20 mm (mid 19 entered)."})
add(p, **{"OPC / Cement": 816.42 / 1182.91, "SF (Silica fume)": 244.33 / 1182.91, "GGBS": 122.16 / 1182.91,
          "SS / B (Silica sand)": 980.64 / 1182.91, "SP / B": 35.47 / 1182.91, "Binder content (kg/m³)": 1182.91,
          "PP fiber (vol%)": 0.3, "Compressive strength (MPa)": 97.0,
          "Conversions / notes": "PRPC. kg/m3: OPC 816.42, SF 244.33, slag 122.16, quartz sand 490.32+490.32, water reducer 35.47, PP 2.73 (0.3%), "
                                 "water 189.20; w/b 0.16. fc = room-temperature compressive strength (Table 5). PP length 18-20 mm."})

# ---------------------------------------------------------------- P6 Hu & Du 2026 (UHPC, ambient curing, age series)
p = {"Article Name": "Experimental Study and Theoretical Analysis on Shrinkage Properties of UHPC under Different Constraint Conditions",
     "Author": "Hu A.; Du J.", "Year": 2026, "DOI / URL": doi("10.1186/s40069-026-00960-y"),
     "OPC / Cement": 750 / 1112.5, "SF (Silica fume)": 250 / 1112.5, "FA (Fly ash)": 112.5 / 1112.5, "W / B": 170 / 1112.5,
     "SS / B (Silica sand)": (256.3 + 388.3 + 455.4) / 1112.5, "Sand max size (µm)": 850, "SP / B": 9.875 / 1112.5,
     "Binder content (kg/m³)": 1112.5, "Steel fiber (vol%)": 78 / 7850 * 100, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
     "Steel tensile strength (MPa)": 2850, "Steel elastic modulus (GPa)": 200, "Curing method": "normal (ambient lab) temperature curing",
     "Tensile test type": "direct", "Source table/page": "Table 1 (mix), Table 2 (fc, ft); Sect. 2.1 text (fibre)"}
for age, fc, ft in [(1, 42.51, 2.06), (3, 91.05, 5.31), (5, "", 5.92), (7, 96.09, 6.40), (14, "", 7.54), (28, 128.37, 8.17)]:
    add(p, **{"Test age (days)": age, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Conversions / notes": "Table 1 kg/m3: cement 750, water 170, SF 250, quartz sand 70-120 mesh 256.3 + 40-70 mesh 388.3 + 20-40 mesh 455.4, "
                                     "PCE water reducer 9.875, steel fibre 78 (78/7850 = 0.99 vol%), FA 112.5; B = 1112.5. Steel 13 mm hooked-end copper-coated, "
                                     "l/d 65 -> d = 0.2 mm. Tensile = uniaxial tensile test (Fig. 15); specimen sizes not given. Sand max 20 mesh = 850 µm."})

# ---------------------------------------------------------------- P7 Wasef et al. 2025 (PP-SHCC and PP-SHGC bonding mortars)
p = {"Article Name": "Flexural Behaviour of Reinforced Concrete Beams Strengthened with Textile-Reinforced Strain Hardening Geopolymer Composites (TR-SHGC)",
     "Author": "Wasef M.; Hassan A.; Kassem N.M.", "Year": 2025, "DOI / URL": doi("10.1186/s40069-025-00774-4"),
     "PP fiber (vol%)": 2.0, "PP length (mm)": 12, "PP diameter (µm)": 25, "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "50x100",
     "Tensile specimen": "plate 500 mm long, 20x100 section (Shaikh et al. 2018)", "Tensile test type": "direct",
     "Source table/page": "Tables 2-3 (mix), Table 4 (fc, tension); Sect. 2 text"}
add(p, **{"OPC / Cement": 1342 / 1579, "SF (Silica fume)": 237 / 1579, "W / B": 0.20, "Fine sand / B": 157.9 / 1579, "Sand max size (µm)": 200,
          "SP / B": 31.6 / 1579, "Binder content (kg/m³)": 1579,
          "Compressive strength (MPa)": 55.81, "Tensile strength (MPa)": 6.62, "First-cracking strength (MPa)": 4.54,
          "Conversions / notes": "SHCC. Table 2 kg/m3: cement 1342, SF 237, fine sand 157.9 (NMS 0.2 mm), water 312.1, SP 31.6, high-strength PP fibre "
                                 "16.20 kg/m3 = 2.0 vol% (stated). W/B 0.20 stated (312.1/1579 = 0.198). Curing of material specimens and test age not "
                                 "stated (strengthened SHCC beams wet-cured 14 d)."})
add(p, **{"GGBS": 0.4, "FA (Fly ash)": 0.6, "WG / B (Water glass)": 0.25, "NaOH / B": 0.10, "NaOH molarity (M)": 16, "Extra water / B": 0.10,
          "SS / B (Silica sand)": "", "Sand (type not stated) / B": 0.15, "SP / B": 0.01, "Binder content (kg/m³)": 1000,
          "Compressive strength (MPa)": 48.20, "Tensile strength (MPa)": 7.21, "First-cracking strength (MPa)": 5.15,
          "Curing method": "not stated for material specimens (SHGC-strengthened beams ambient cured ~32 C for 28 d)",
          "Conversions / notes": "SHGC. Table 3 kg/m3: slag 400, FA 600, sand 150, water 100, NaOH 100 (16 M solution), Na2SiO3 250 (solution), SP 10, "
                                 "fibre 16.20 kg/m3 = 2.0 vol% (same PP assumed as SHCC - table does not name fibre type for SHGC). Ratios / B (1000). "
                                 "Test age not stated."})

# ---------------------------------------------------------------- P8 Saghafi et al. 2019 (HPFRCC steel / hybrid)
p = {"Article Name": "Seismic Behavior of High-Performance Fiber-Reinforced Cement Composites Beam-Column Connection with High Damage Tolerance",
     "Author": "Saghafi M.H.; Shariatmadar H.; Kheyroddin A.", "Year": 2019, "DOI / URL": doi("10.1186/s40069-019-0334-3"),
     "OPC / Cement": 1 / 1.1, "SF (Silica fume)": 0.1 / 1.1, "W / B": 0.28 / 1.1, "Sand (type not stated) / B": 1 / 1.1, "Sand max size (µm)": 4750,
     "SP / B": 0.0014, "Steel length (mm)": 35, "Steel diameter (µm)": 800, "Steel tensile strength (MPa)": 1100, "Steel elastic modulus (GPa)": 212,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200", "Tensile specimen": "30x30x330 (JSCE-N82-2008)",
     "Tensile test type": "direct", "Source table/page": "Tables 1-3 (mix, fibres), Table 4 (specimens), Table 7 (results)"}
N8 = ("Table 1 mass ratio cement 1 : SF 0.1 : water 0.28 : crushed sand 1 (0.1-4.75 mm), SP 0.14% of binder; B = 1.1. "
      "Water ratio assumed relative to cement as tabulated (W/B = 0.255). Curing / test age not stated. ")
add(p, **{"Steel fiber (vol%)": 1, "PP fiber (vol%)": 1, "PP length (mm)": "", "Compressive strength (MPa)": 41.47, "Tensile strength (MPa)": 6.2,
          "Tensile strain capacity (%)": 0.733,
          "Conversions / notes": "HPFRCC-A: 1% hooked steel + 1% macro synthetic. " + N8 +
                                 "Macro synthetic fibre = blend of PP twist, PP mesh and PE fibres (text), entered under PP. Strain = strain at tensile strength."})
add(p, **{"Steel fiber (vol%)": 2, "Compressive strength (MPa)": 50.57, "Tensile strength (MPa)": 6.7, "Tensile strain capacity (%)": 0.760,
          "Conversions / notes": "HPFRCC-B: 2% hooked steel. " + N8 + "Strain = strain at tensile strength."})

# ---------------------------------------------------------------- P9 Paul & van Zijl 2017 (PVA-SHCC, fine vs coarse sand)
p = {"Article Name": "Corrosion Deterioration of Steel in Cracked SHCC", "Author": "Paul S.C.; van Zijl G.P.A.G.", "Year": 2017,
     "DOI / URL": doi("10.1007/s40069-017-0205-8"), "OPC / Cement": 392 / 1066, "FA (Fly ash)": 674 / 1066, "W / B": 392 / 1066,
     "SP / B": 1.99 / 1066, "VMA / B": 0.54 / 1066, "Binder content (kg/m³)": 1066, "PVA fiber (vol%)": 2.01, "PVA length (mm)": 12,
     "PVA diameter (µm)": 40, "Source table/page": "Table 1 (mix), Table 3 (properties)"}
N9 = ("Table 1 kg/m3: CEM 42.5 392, FA 674, sand 553, water 392, PVA 2.01%, SP 1.99, VMA 0.54, AEA 0.54 (air entrainer, no column). "
      "fcu (cube) at 28 d; direct tension on dumbbells at 14 d. Mixes FS31/FS32 (CEM 52.5) reported only as ranges -> not entered. ")
for mid, sand_col, fc, ft, fcr, eu, sn in [("FS2", "Fine sand / B", 25, 2.6, 2.0, 2.2, "fine sand FM 1.9"),
                                           ("CS2", "Local sand / B", 23, 2.01, 1.8, 1.2, "local natural coarse sand FM 3.3")]:
    add(p, **{sand_col: 553 / 1066, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive strength (MPa)": fc,
              "Conversions / notes": f"Mix {mid} ({sn}). " + N9})
    add(p, **{sand_col: 553 / 1066, "Test age (days)": 14, "Tensile specimen": "dumbbell", "Tensile test type": "direct",
              "Tensile strength (MPa)": ft, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eu,
              "Conversions / notes": f"Mix {mid} ({sn}). " + N9})

# ---------------------------------------------------------------- P10 dapped-end beams 2019 (self-compacting PVA-ECC)
p = {"Article Name": "Structural Performance of RC and R-ECC Dapped-End Beams Based on the Role of Hanger or Diagonal Reinforcements Combined by ECC",
     "Author": "Mohammed B.S.; Aswin M.; Liew M.S.; Zawawi N.A.W.A.", "Year": 2019, "DOI / URL": doi("10.1186/s40069-019-0356-x"), "PVA length (mm)": 18, "Test age (days)": 28,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200", "Source table/page": "Table 2 (mix), Table 4 (properties)"}
for mid, c, fa, sf, w, s, sp, vf, kg, fc, fst, ft, et in [
        ("ECC-1", 583, 700, 0, 187.32, 467.01, 14.11, 2.0, 26.0, 85.72, 6.42, 4.88, 2.93),
        ("ECC-2", 590, 354, 94.4, 165.20, 472.00, 15.10, 1.5, 19.5, 105.26, 7.84, 5.73, 4.09)]:
    b = c + fa + sf
    base = dict(p, **{"OPC / Cement": c / b, "FA (Fly ash)": fa / b, "SF (Silica fume)": sf / b, "W / B": w / b, "River sand / B": s / b,
                      "SP / B": sp / b, "Binder content (kg/m³)": b, "PVA fiber (vol%)": vf})
    note = (f"Mix {mid}. Table 2 kg/m3: OPC {c}, FA {fa}, SF {sf}, water {w}, washed river sand {s}, PCE SP {sp}, PVA {kg} kg/m3 = {vf} vol% (stated). "
            "Ratios / B. Averages of 3 samples; specimens tested at 28 d (curing regime not detailed).")
    add(base, **{"Tensile specimen": "prism dog-bone (ASTM D2936)", "Tensile test type": "direct", "Compressive strength (MPa)": fc,
                 "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": et, "Conversions / notes": note})
    add(base, **{"Tensile specimen": "cylinder 100x200 (ASTM C496)", "Tensile test type": "splitting", "Tensile strength (MPa)": fst,
                 "Conversions / notes": note})

# ---------------------------------------------------------------- P11 Han et al. 2018 (PVA-HPFRCC, CaCO3 filler, no sand)
b = 489 + 374.9 + 32.6 + 684.6
p = {"Article Name": "Cyclic Behavior of HPFRCC Coupling Beams with Bundled Diagonal Bars",
     "Author": "Han S.W.; Kang J.-W.; Jee H.-W.; Shin M.; Lee K.", "Year": 2018, "DOI / URL": doi("10.1186/s40069-018-0271-6"),
     "OPC / Cement": 489 / b, "FA (Fly ash)": 374.9 / b, "SF (Silica fume)": 32.6 / b, "Limestone powder": 684.6 / b, "W / B": 366.8 / b,
     "SP / B": 3.3 / b, "Binder content (kg/m³)": b, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
     "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 25, "Test age (days)": 28, "Curing time (days)": 28,
     "Curing method": "same condition as coupling beam specimens (not detailed)", "Compressive specimen": "cylinder",
     "Compressive specimen size (mm)": "100x200", "Tensile specimen": "dog-bone (Michigan type, Parra-Montesinos 2005)",
     "Tensile test type": "direct", "Compressive strength (MPa)": 41, "Tensile strength (MPa)": 4.3, "Tensile strain capacity (%)": 2.5,
     "Source table/page": "Table 2 (mix), Table 3 (fibre), Table 4 (properties)",
     "Conversions / notes": "Table 2 kg/m3: cement 489, FA 374.9, SF 32.6, water 366.8, CaCO3 filler 684.6, SP 3.3; no sand. CaCO3 filler counted in B "
                            "(Limestone powder) since it is the only fine solid; B = 1581.1. Excluding filler: B = 896.5, W/B = 0.409, filler/B = 0.764."}
add(p)

# ---------------------------------------------------------------- P12 Wu et al. 2018 (UHPFRC tube, steam cured)
p = {"Article Name": "Axial Load Testing of Hybrid Concrete Columns Consisting of UHPFRC Tube and Normal-Strength Concrete Core",
     "Author": "Wu X.; Kang T.H.-K.; Mpalla I.B.; Kim C.-S.", "Year": 2018, "DOI / URL": doi("10.1186/s40069-018-0275-2"),
     "Sand max size (µm)": 2000, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2500,
     "Curing method": "steam cured at 100 C for 48 h (panels), then room temperature", "Curing temperature (°C)": 100,
     "Heat curing duration (h)": 48, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
     "Tensile specimen": "notched dog-bone, reduced section 20x150x190 (text: 'wire-meshed and notched dog-bone specimens')",
     "Tensile test type": "direct", "Source table/page": "Table 2 (mix); Sect. 2.2.1 text (fcu, fct, fibre, curing)"}
for vf, c, sf, qf, s, sp, w, st, fc, ft, eps in [(1.5, 769.8, 192.5, 231.0, 846.8, 30.8, 192.5, 89.5, 92.6, 4.56, 0.026),
                                                (2.0, 766.9, 191.7, 230.1, 843.6, 30.7, 191.7, 118.9, 143.3, 6.23, 0.020)]:
    b = c + sf
    add(p, **{"OPC / Cement": c / b, "SF (Silica fume)": sf / b, "W / B": w / b, "QP / B (Quartz powder)": qf / b, "River sand / B": s / b,
              "SP / B": sp / b, "Binder content (kg/m³)": b, "Steel fiber (vol%)": vf, "Compressive strength (MPa)": fc,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Conversions / notes": f"{vf}% Vf UHPFRC. Table 2 kg/m3: cement {c}, SF {sf}, silica flour {qf} (-> QP/B), washed river sand 0-2 mm {s}, "
                                     f"SP {sp}, expansive agent 3.8, defoaming agent 3.8, steel fibre {st}, water {w} (W/B 0.2 stated). fcu = 28-d 100 mm cube; "
                                     "ft and strain at peak from text (strain-softening after peak). VERIFY: tension specimens described as 'wire-meshed and notched "
                                     "dog-bone' - wire mesh may contribute; authors note low strengths due to insufficient mixing/initial curing."})

# ---------------------------------------------------------------- P13 Nam et al. 2017 (PVA / PE / steel / hybrid FRCC blast panels)
b = 960 + 169
p = {"Article Name": "Experimental Investigation on the Blast Resistance of Fiber-Reinforced Cementitious Composite Panels Subjected to Contact Explosions",
     "Author": "Nam J.; Kim H.; Kim G.", "Year": 2017, "DOI / URL": doi("10.1007/s40069-016-0179-y"),
     "OPC / Cement": 960 / b, "FA (Fly ash)": 169 / b, "W / B": 452 / b, "SS / B (Silica sand)": 395 / b, "Binder content (kg/m³)": b,
     "Curing method": "environmental chamber 23+/-2 C, RH 60+/-5%", "Curing temperature (°C)": 23, "Curing RH (%)": 60, "Curing time (days)": 28,
     "Test age (days)": 28, "Compressive specimen": "cylinder", "Source table/page": "Tables 2-4 (mix, fibres), Table 5 (fc)"}
PVA = {"PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1300}
PE = {"PE length (mm)": 15, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700}
ST = {"Steel length (mm)": 30, "Steel diameter (µm)": 700, "Steel tensile strength (MPa)": 1140}
N13 = ("Table 2/4 kg/m3: cement 960, class-F FA 169, water 452 (W/B 0.4), class-7 silica sand 395, HRWR {h}. Fibre total 2 vol%. "
       "PVA 12 mm/0.040 mm/1300 MPa; PE 15 mm/0.012 mm/2700 MPa; hooked-end steel 30 mm/0.7 mm/1140 MPa. ")
for mid, h, fk, fc in [("NCC", 0.0, {}, 43.7), ("PVACC", 16.9, dict(PVA, **{"PVA fiber (vol%)": 2}), 28.5),
                       ("PECC", 22.6, dict(PE, **{"PE fiber (vol%)": 2}), 27.9), ("SCC", 5.6, dict(ST, **{"Steel fiber (vol%)": 2}), 34.7),
                       ("PVASCC", 11.3, dict(PVA, **ST, **{"PVA fiber (vol%)": 1, "Steel fiber (vol%)": 1}), 35.8),
                       ("PESCC", 16.9, dict(PE, **ST, **{"PE fiber (vol%)": 1, "Steel fiber (vol%)": 1}), 36.7)]:
    extra = "Hybrid listed as '2 (1)' in Table 4 (footnote not rendered): 1% micro synthetic + 1% steel assumed per text. " if "S" in mid[-3:] and mid != "SCC" else ""
    add(p, **fk, **{"SP / B": h / b, "Compressive strength (MPa)": fc,
                    "Conversions / notes": f"Mix {mid}. " + N13.format(h=h) + extra + "Plain NHC (coarse aggregate) not entered. Static fracture energy also reported (Table 5)."})

# ---------------------------------------------------------------- P14 Yousef et al. 2025 (UHPFRC ledge beams)
b = 900 + 225
p = {"Article Name": "Minimum Ledge Tie Reinforcement for UHPFRC Ledge Beams", "Author": "Yousef A.M.; El Madawy M.E.; Abd El-Hady K.", "Year": 2025,
     "DOI / URL": doi("10.1186/s40069-025-00761-9"), "OPC / Cement": 900 / b, "SF (Silica fume)": 225 / b, "W / B": 168 / b,
     "Sand (type not stated) / B": 775 / b, "QP / B (Quartz powder)": 270 / b, "SP / B": 36 / b, "Binder content (kg/m³)": b,
     "Steel fiber (vol%)": 1.5, "Steel length (mm)": 25, "Steel diameter (µm)": 1000, "Steel tensile strength (MPa)": 828.3,
     "Curing method": "cured at 21+/-2 C (medium not stated)", "Curing temperature (°C)": 21, "Test age (days)": 28,
     "Source table/page": "Table 6 (mix), Table 7 (properties); Sect. 3 text"}
N14 = ("Table 6 kg/m3: cement 900, SF 225, sand 775, quartz powder 270, SP (ViscoCrete 3425) 36, water 168, steel fibre 120 "
       "(120/7850 = 1.53 vol%; paper states 1.5%). Hooked-end steel 25 mm x 1 mm, ultimate 828.3 MPa. ")
add(p, **{"Compressive specimen": "cube", "Compressive specimen size (mm)": "50x50x50", "Compressive strength (MPa)": 146.10,
          "Tensile specimen": "cylinder 50x100", "Tensile test type": "splitting", "Tensile strength (MPa)": 12.40,
          "Conversions / notes": N14 + "fcu (cube); cylinder 50x100 fc' = 133.40 MPa."})
add(p, **{"Tensile specimen": "prism 40x40x160, centre-point loading", "Tensile test type": "flexural", "Tensile strength (MPa)": 28.60,
          "Conversions / notes": N14 + "Flexural strength row (fc on splitting row)."})

# ---------------------------------------------------------------- P15 Qiu et al. 2020 (UHPC with 4 steel fibre types, steam cured)
p = {"Article Name": "Experimental Investigation on Flexural Behavior of Reinforced Ultra High Performance Concrete Low-Profile T-Beams",
     "Author": "Qiu M.; Shao X.; Wille K.; Yan B.; Wu J.", "Year": 2020, "DOI / URL": doi("10.1186/s40069-019-0380-x"),
     "OPC / Cement": 1 / 1.3, "SF (Silica fume)": 0.2 / 1.3, "FA (Fly ash)": 0.1 / 1.3, "W / B": 0.18 * 1.5 / 1.3, "SS / B (Silica sand)": 1.1 / 1.3,
     "Sand max size (µm)": 900, "QP / B (Quartz powder)": 0.2 / 1.3, "SP / B": 0.02 * 1.5 / 1.3, "Steel fiber (vol%)": 2,
     "Curing method": "covered at normal temperature 48 h, then steam cured 90-100 C for 48 h", "Curing temperature (°C)": 95,
     "Heat curing duration (h)": 48, "Demolding age (days)": 2, "Tensile specimen": "prism 100x100x400, four-point bending (GB/T 31387)",
     "Tensile test type": "flexural", "Source table/page": "Table 1 (mix), Table 2 (fibres), Table 4 (properties)"}
for mid, L, dmm, fc, flop, fmor, ft in [("S65", 13, 0.20, 131.6, 13.0, 25.2, 7.98), ("S81", 13, 0.16, 126.2, 13.1, 25.9, 8.05),
                                        ("S83", 10, 0.12, 129.6, 13.0, 25.8, 8.02), ("H65 (hooked-end)", 13, 0.20, 139.2, 13.0, 27.9, 8.02)]:
    add(p, **{"Steel length (mm)": L, "Steel diameter (µm)": dmm * 1000, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": fmor,
              "First-cracking strength (MPa)": flop,
              "Conversions / notes": f"Fibre {mid}. Table 1 mass ratio cement 1 : SF 0.2 : FA 0.1 : quartz sand 1.1 : silica powder 0.2, HRWRA 2% of binder, "
                                     "w/b 0.18 (paper counts silica powder as binder, B' = 1.5). Here B = C+SF+FA = 1.3, silica powder -> QP/B; W/B = 0.18*1.5/1.3 = 0.208, SP/B = 0.02*1.5/1.3. "
                                     f"Tensile strength = fMOR, first-cracking = fLOP (flexure). Direct tensile strength from inverse analysis ft = {ft} MPa "
                                     "(not a test, not entered). Compressive specimen and test age not stated. Curing temperature 90-100 C (95 entered)."})

# ---------------------------------------------------------------- P16 Shin et al. 2018 (UHPFRC for strand bond)
p = {"Article Name": "Bond Behavior of Pretensioned Strand Embedded in Ultra-High-Performance Fiber-Reinforced Concrete",
     "Author": "Shin H.-O.; Lee S.-J.; Yoo D.-Y.", "Year": 2018, "DOI / URL": doi("10.1186/s40069-018-0249-4"),
     "OPC / Cement": 1 / 1.25, "SF (Silica fume)": 0.25 / 1.25, "W / B": 0.2, "SS / B (Silica sand)": 1.1 / 1.25, "QP / B (Quartz powder)": 0.3 / 1.25,
     "Steel fiber (vol%)": 2, "Steel tensile strength (MPa)": 2500, "Steel elastic modulus (GPa)": 200,
     "Curing method": "moist ambient 24 h, steam 90+/-2 C for 72 h after demoulding, then moist ambient until testing",
     "Curing temperature (°C)": 90, "Heat curing duration (h)": 72, "Demolding age (days)": 1, "Source table/page": "Table 1 (mix), Table 2 (properties)"}
N16 = ("Table 1 ratios to cement: water 0.227, cement 1, SF 0.25, silica sand 1.1, silica flour 0.3, SP 0.16 (as printed; implausibly high, not entered), "
       "steel fibre 2 vol%; W/B 0.2 as stated (0.227/1.25 = 0.18). Straight micro steel l/d 65, 2500 MPa. Average of 3 batches; test age not stated. ")
add(p, **{"Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200", "Compressive strength (MPa)": 183.3,
          "Tensile specimen": "prism 100x100x400 (ASTM C1609)", "Tensile test type": "flexural", "Tensile strength (MPa)": 26.7,
          "Conversions / notes": N16})

# ---------------------------------------------------------------- P17 Kim et al. 2024 (UHPFRC precast joints)
b = 783 + 180
p = {"Article Name": "Assessing the Seismic Performance of Exterior Precast Concrete Joints with Ultra-High-Performance Fiber-Reinforced Concrete",
     "Author": "Kim S.; Shin J.; Kim W.", "Year": 2024, "DOI / URL": doi("10.1186/s40069-023-00646-9"),
     "OPC / Cement": 783 / b, "SF (Silica fume)": 180 / b, "W / B": 180 / b, "SS / B (Silica sand)": 470 / b, "River sand / B": 470 / b,
     "Sand max size (µm)": 850, "QP / B (Quartz powder)": 235 / b, "SP / B": 42 / b, "Binder content (kg/m³)": b,
     "Steel fiber (vol%)": 77.5 / 7850 * 100, "Steel length (mm)": 17, "Steel diameter (µm)": 200, "Tensile test type": "flexural",
     "Compressive strength (MPa)": 121.0, "Tensile strength (MPa)": 32.3, "Source table/page": "Table 2 (mix), Table 3 (strength)",
     "Conversions / notes": "Table 2 kg/m3: water 180, cement 783, SF 180, quartz sand 470, river sand 470 (20-40 mesh), silica flour 235 (12.4 µm, QP), "
                            "SP 42, steel fibre 77.5 (77.5/7850 = 0.99 vol%). Steel 0.2 mm dia., 16 and 19 mm lengths mixed 2:1 (weighted mean 17 mm entered). "
                            "Tensile = bending strength (specimen not given). Curing, specimen sizes and test age not given."}
add(p)

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows).reindex(columns=H)
seen = set()
with open(os.path.join(D, "existing_papers.txt"), encoding="utf-8-sig") as f:
    for l in f:
        m = re.search(r"10\.\d+/\S+", l)
        if m:
            seen.add(m.group(0).lower().rstrip("/.,"))
for fn in glob.glob(os.path.join(D, "*.csv")):
    if os.path.basename(fn) in ("TEMPLATE.csv", NAME + ".csv"):
        continue
    for v in pd.read_csv(fn, encoding="utf-8-sig", usecols=["DOI / URL"])["DOI / URL"].dropna().unique():
        m = re.search(r"10\.\d+/\S+", str(v))
        if m:
            seen.add(m.group(0).lower())
dois = df["DOI / URL"].str.extract(r"(10\.\d+/\S+)")[0].str.lower()
dup = sorted(set(dois[dois.isin(seen)]))
if dup:
    print("DROPPING already-collected DOIs:", dup)
df = df[~dois.isin(seen)]
df.to_csv(os.path.join(D, NAME + ".csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers")
