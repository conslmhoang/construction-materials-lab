"""Wave 6, agent e27: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e27.csv (99-column TEMPLATE header).
Papers: jobe.2024.109332, jobe.2024.110251, jobe.2026.115972, matdes.2020.109371, matdes.2022.110553, tafmec.2022.103503
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


# ---------- 1) Yang et al.: HSHDC, w/b 0.16 matrices M1-M3, PE / PVA fibres
P = {"Article Name": "Uniaxial tensile test of high-strength high-ductility concrete (HSHDC): Mechanical response and toughness evaluation",
     "Author": "Jiasheng Yang, Mingke Deng, Yitong Wang, Yangxi Zhang", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2024.109332"}
mats = {"M1": (.70, .15, .15), "M2": (.65, .15, .20), "M3": (.60, .15, .25)}
# name, matrix, w/b, fibre, d(um), vol%, eps_p(%), sigma_cr, sigma_p
t = [("M1-0.16-PE22-1.5", "M1", .16, "PE", 22, 1.5, 3.561, 3.06, 6.06), ("M1-0.16-PE22-2.0", "M1", .16, "PE", 22, 2.0, 3.839, 3.52, 6.99),
     ("M1-0.16-PE22-2.5", "M1", .16, "PE", 22, 2.5, 4.647, 3.96, 7.69), ("M1-0.16-PE30-2.0", "M1", .16, "PE", 30, 2.0, 3.156, 3.60, 6.73),
     ("M1-0.16-PE35-2.0", "M1", .16, "PE", 35, 2.0, 2.294, 3.36, 5.11), ("M1-0.16-PE40-2.0", "M1", .16, "PE", 40, 2.0, 0.345, 3.15, 4.52),
     ("M1-0.14-PE22-2.0", "M1", .14, "PE", 22, 2.0, 0.811, 3.58, 5.94), ("M1-0.18-PE22-2.0", "M1", .18, "PE", 22, 2.0, 1.888, 3.09, 5.72),
     ("M1-0.16-PVA39-2.0", "M1", .16, "PVA", 39, 2.0, 0.228, 3.53, 4.78), ("M2-0.16-PE22-2.0", "M2", .16, "PE", 22, 2.0, 4.853, 2.83, 6.45),
     ("M2-0.16-PVA39-2.0", "M2", .16, "PVA", 39, 2.0, 0.250, 3.48, 5.28), ("M3-0.16-PE22-2.0", "M3", .16, "PE", 22, 2.0, 6.483, 2.77, 6.76),
     ("M3-0.16-PVA39-2.0", "M3", .16, "PVA", 39, 2.0, 0.300, 3.32, 5.54)]
fc_pva = {"M1": (85.9, 96.4, 114.5), "M2": (85.1, 91.6, 108.6), "M3": (84.0, 94.0, 100.8)}


def hshdc(name, m, wb, fib, d, vol):
    o, s, f = mats[m]
    r = dict(P)
    r.update({"OPC / Cement": o, "SF (Silica fume)": s, "FA (Fly ash)": f, "W / B": wb, "SS / B (Silica sand)": 0.36,
              "Sand max size (µm)": 500, "SP / B": 0.02, "Total fiber (vol%)": vol,
              "Curing method": "covered 24 h, demoulded, standard curing room 20 +/- 2 C RH 95 %", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Compressive specimen": "cube",
              "Compressive specimen size (mm)": "100", "Tensile specimen": "dog-bone", "Tensile test type": DIRECT})
    if fib == "PE":
        r.update({"PE fiber (vol%)": vol, "PE length (mm)": 12, "PE diameter (µm)": d, "PE tensile strength (MPa)": 2300, "PE elastic modulus (GPa)": 90})
    else:
        r.update({"PVA fiber (vol%)": vol, "PVA length (mm)": 12, "PVA diameter (µm)": d, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40})
    note = (f"{name}. Table 4 gives binder mass ratios, sand/b 0.36 (graded quartz sand <= 0.5 mm), SP/b 2.0 %, defoamer 3.0 % of binder (DA, noted). "
            "Tensile and 28-d values: Table 6 (tensile), Table 5 (fc, PVA mixes only).")
    if wb != .16:
        note += " VERIFY: Table 4 lists only w/b 0.16; sand, SP and DA assumed unchanged for w/b 0.14 / 0.18."
    return r, note


for name, m, wb, fib, d, vol, ep, scr, sp in t:
    r, note = hshdc(name, m, wb, fib, d, vol)
    r.update({"Test age (days)": 28, "First-cracking strength (MPa)": scr, "Tensile strength (MPa)": sp, "Tensile strain capacity (%)": ep,
              "Source table/page": "Table 4 (mix), Table 3 (fibres), Table 6 (tensile), sect. 2.3 (curing)"})
    if fib == "PVA":
        r["Compressive strength (MPa)"] = fc_pva[m][1]
        r["Source table/page"] += ", Table 5 (fc 28 d)"
        note += " fc of the PVA-2.0 % composite at 28 d."
    else:
        note += " No fc reported for PE composites (only matrix 60-d fc in Table 4, not used)."
    r["Conversions / notes"] = note
    rows.append(r)
# extra ages: fc of the PVA composites at 7 d and 60 d (compression only)
for m in ("M1", "M2", "M3"):
    for k, age in ((0, 7), (2, 60)):
        r, note = hshdc(f"{m}-0.16-PVA39-2.0", m, .16, "PVA", 39, 2.0)
        r.update({"Test age (days)": age, "Curing time (days)": age, "Compressive strength (MPa)": fc_pva[m][k],
                  "Source table/page": "Table 4 (mix), Table 5 (fc 7 / 60 d)",
                  "Conversions / notes": note + f" fc only at {age} d; curing time = test age (standard curing room until test)."})
        r["Tensile specimen"] = None
        r["Tensile test type"] = None
        rows.append(r)

# ---------- 2) Wang et al.: ECC reference (no graphene), strain only
P = {"Article Name": "Effect of mechanochemistry on graphene dispersion and its application in improving the mechanical properties of engineered cementitious composites",
     "Author": "Siyu Wang, Yan Zhuge, Yue Liu, Yiyan Lu", "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.jobe.2024.110251"}
B = 430 + 816
r = dict(P)
r.update({"OPC / Cement": r4(430 / B), "FA (Fly ash)": r4(816 / B), "W / B": r4(374 / B), "Sand (type not stated) / B": r4(448 / B),
          "SP / B": r4(3.74 / B), "Binder content (kg/m³)": B, "PE fiber (vol%)": 1.96, "Total fiber (vol%)": 1.96,
          "Curing method": "covered 24 h, demoulded, standard curing room 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
          "Test age (days)": 28, "Tensile test type": DIRECT, "First-cracking strength (MPa)": 2.52, "Tensile strength (MPa)": 2.99,
          "Tensile strain capacity (%)": 2.12, "Source table/page": "Table 1 (mix), Table 2 (tensile, sample 'ECC')",
          "Conversions / notes": "Plain ECC control only (graphene mixes skipped). kg/m3 / B (cement + FA = 1246). PE fibre 19 kg/m3 -> 1.96 vol% with density 970 (VERIFY: vol% derived). "
                                 "Curing temperature and RH not stated. fc of control only in Fig. 6, not entered. Table 1 lists graphene 0.43 kg/m3 which belongs to the graphene mixes."})
rows.append(r)

# ---------- 3) Chen et al.: PVA/PP HDCC, PVA-only mix BF-0%PP
P = {"Article Name": "Deciphering the positive hybrid effect in PVA/PP hybrid fiber-reinforced cementitious composites: A synergistic study on rheology, mechanics, microstructure, and techno-economic performance",
     "Author": "Hai-Tao Chen, Li-Ping Guo, Guo-Tai Zhao, Jia-Yi Li, Zhen-Hao Liu", "Year": 2026, "DOI / URL": "https://doi.org/10.1016/j.jobe.2026.115972"}
r = dict(P)
r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.8, "W / B": 0.25, "Sand (type not stated) / B": 0.30, "SP / B": 0.0025, "HPMC / B (hydroxypropyl methyl cellulose)": 0.0004,
          "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1250, "PVA elastic modulus (GPa)": 30,
          "Total fiber (vol%)": 2.0, "Curing method": "demoulded after 24 h, standard curing until 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
          "Test age (days)": 28, "Tensile test type": DIRECT, "First-cracking strength (MPa)": 2.68, "Tensile strength (MPa)": 3.88,
          "Tensile strain capacity (%)": 2.88, "Source table/page": "Table 4 (mix BF-0%PP), Table 5 (tensile), Table 2 (fibre), sect. 2.2",
          "Conversions / notes": "BF-0%PP (PVA 2 vol%, no PP). Mixes in wt% of binder (C 20 : FA 80). Water reducer (WR, powder PCE) entered as SP; HPMC 0.04 % of binder. "
                                 "VERIFY: 'BF' mix proportions assumed to use the 0.25 W/B row of Table 4. Mixes with PP fibre skipped. Curing temperature / RH not stated."})
rows.append(r)

# ---------- 4) Figueiredo et al.: PVA-SHCC and PE-SHCC under uniaxial tension (LC1)
P = {"Article Name": "Mechanical behavior of strain-hardening cement-based composites (SHCC) subjected to torsional loading and to combined torsional and axial loading",
     "Author": "Tathiana Caram S.P. Figueiredo, Iurie Curosu, Giancarlo L.G. Gonzales, Marcus Hering, Flavio de Andrade Silva, Manfred Curbach, Viktor Mechtcherine",
     "Year": 2020, "DOI / URL": "https://doi.org/10.1016/j.matdes.2020.109371"}
B = 505 + 621
for nm, w, sp, fib, esig1, smax, emax in [("PVA-SHCC", 338, 10, "PVA", 3.7, 4.3, 1.0), ("PE-SHCC", 333, 25, "PE", 4.1, 5.2, 2.5)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(505 / B), "FA (Fly ash)": r4(621 / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(536 / B),
              "Sand max size (µm)": 200, "SP / B": r4(sp / B), "VMA / B": r4(4.8 / B), "Binder content (kg/m³)": B, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded 24 h, sealed in plastic sheets, 20 C RH 65 % for 14 d, then lab storage until test",
              "Curing time (days)": 14, "Curing temperature (°C)": 20, "Curing RH (%)": 65, "Demolding age (days)": 1, "Test age (days)": 65,
              "Tensile specimen": "dumbbell", "Tensile test type": DIRECT, "First-cracking strength (MPa)": esig1, "Tensile strength (MPa)": smax,
              "Tensile strain capacity (%)": emax, "Source table/page": "Table 2 (mix, kg/m3), Table 1 (fibres), Table 4 (LC1 uniaxial tension), sect. 2.1",
              "Conversions / notes": f"{nm}. Load case LC1 only (torsion cases skipped). kg/m3 / B (cement + FA = 1126). Fibre 2 vol% as stated. "
                                     "Quartz sand 60-200 um used as sand. Test age 'average 65 d' (text). VERIFY: storage after the 14 d sealed period not described."})
    if fib == "PVA":
        r.update({"PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600})
    else:
        r.update({"PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 2500})
    rows.append(r)

# ---------- 5) Lu et al.: reference UHPC1 (normal-weight, river sand)
P = {"Article Name": "Mix design and performance of lightweight ultra high-performance concrete",
     "Author": "Jian-Xin Lu, Peiliang Shen, Hafiz Asad Ali, Chi Sun Poon", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.matdes.2022.110553"}
B = 907 + 246
r = dict(P)
r.update({"OPC / Cement": r4(907 / B), "SF (Silica fume)": r4(246 / B), "W / B": r4(180 / B), "River sand / B": r4(1153 / B), "SP / B": r4(34 / B),
          "Binder content (kg/m³)": B, "Steel fiber (vol%)": 1.5, "Steel length (mm)": 13, "Steel diameter (µm)": 220, "Total fiber (vol%)": 1.5,
          "Curing method": "24 h lab (23 C, 50 % RH), demoulded, steam 90 C 48 h", "Curing time (days)": 2, "Curing temperature (°C)": 90, "Demolding age (days)": 1,
          "Test age (days)": 3, "Heat curing duration (h)": 48, "Compressive specimen": "prism halves", "Compressive specimen size (mm)": "40x40x160 prism",
          "Compressive strength (MPa)": 186.4, "Source table/page": "Table 2 (reference UHPC1), sect. 2.3-2.4",
          "Conversions / notes": "Reference UHPC1 only (lightweight L-UHPC mixes skipped: LWA / hollow glass microspheres). kg/m3 / B (cement + SF = 1153). "
                                 "SP 34 kg/m3 (80 % water, as dosed); W/B = water 180 / B = 0.156 free water (the stated w/b 0.18 includes SP water). Steel 117 kg/m3 = 1.5 vol%. "
                                 "VERIFY: test age 3 d derived (1 d + 48 h steam), test time after steam curing not stated (cooled to ambient)."})
rows.append(r)

# ---------- 6) Keskinates et al.: PVA-ECC with GBFS or FA, W/B 0.24 / 0.34
P = {"Article Name": "A comprehensive experimental study on the role of matrix structure on the multiple cracking behavior of PVA-ECC",
     "Author": "Muhammer Keskinates, Burak Felekoglu, Eren Godek", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.tafmec.2022.103503"}
for nm, c, g, fa, w, sp, scr, smax, eps in [("GBFS-0.24-1.79%", 482, 1206, 0, 395, 8.6, 2.04, 3.17, 0.71), ("GBFS-0.34-0.22%", 406, 1016, 0, 488, 0.9, 1.89, 3.35, 2.13),
                                            ("FA-0.24-1.65%", 437, 0, 1093, 358, 5.9, 2.51, 3.91, 0.44), ("FA-0.34-0.0%", 374, 0, 935, 449, 0.0, 2.43, 4.49, 2.11)]:
    B = c + g + fa
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "W / B": r4(w / B), "SP / B": r4(sp / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0,
              "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded after 2 d, water 20 +/- 2 C until 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Demolding age (days)": 2,
              "Test age (days)": 28, "Tensile specimen": "dog-bone (unnotched)", "Tensile test type": DIRECT, "First-cracking strength (MPa)": scr,
              "Tensile strength (MPa)": smax, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix, kg/m3), Table 4 (tensile, averages of 6 specimens), sect. 3.2",
              "Conversions / notes": f"{nm}. No sand (paste matrix). kg/m3 / B (cement + {'GBFS' if g else 'FA'} = {B}); W/B computed from the theoretical mix (paper names 0.24 / 0.34). "
                                     "PVA 26 kg/m3 = 2 vol% as stated. fc only in Fig. 19, not entered. Tensile values = Average row of Table 4."})
    if g:
        r["GGBS"] = r4(g / B)
    else:
        r["FA (Fly ash)"] = r4(fa / B)
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e27.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
