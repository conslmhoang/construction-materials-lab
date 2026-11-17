"""Wave 6, agent e15: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e15.csv (99-column TEMPLATE header).
Papers: compositesb.2019.107446, conbuildmat.2011.08.032, 2012.04.031, 2012.08.003, 2013.03.088
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


# ---------------------------------------------------------------- 1) ozonated PE fibre SHCC (compositesb 107446)
P = {"Article Name": "Surface modification of polyethylene fiber by ozonation and its influence on the mechanical properties of Strain-Hardening Cementitious Composites",
     "Author": "Zeyu Lu, Ran Yin, Jie Yao, Christopher K.Y. Leung", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.compositesb.2019.107446"}
B = 1.25
for mid, fu, eps in [("PE-SHCC (untreated PE)", 7.5, 2.1), ("O3(30 min)/PE-SHCC", 5.8, 3.2), ("O3(60 min)/PE-SHCC", 6.2, 4.8)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(0.25 / B), "W / B": r4(0.20 / B), "SS / B (Silica sand)": r4(0.375 / B),
              "SP / B": r4(0.03 / B), "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 24,
              "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 120, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 24 h ambient, demoulded, curing room 25 C RH 95 % for 13 d", "Curing time (days)": 14,
              "Curing temperature (°C)": 25, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 14,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 1 (PE), Table 5 (tensile, average of 2 representative specimens), sect. 2.3 (curing)",
              "Conversions / notes": f"{mid}. Table 2 ratios by weight of cement: cement 1, SF 0.25, sand 0.375, w/c 0.20, PCE 0.03; B = cement + SF = 1.25, so all "
                                     "ratios divided by 1.25 (W/B 0.16). Silica sand 150 um. SP = polycarboxylate liquid (28 % solids) as dosed. "
                                     "Ozone-treated PE fibres (surface oxidised) counted as PE. fc not reported. Strength/strain = average of the 2 representative "
                                     "specimens of 3 tested. VERIFY: test age 14 d derived (24 h + 13 d stated)."})
    rows.append(r)

# ---------------------------------------------------------------- 2) SAP in ECC, SAP-free mixes (conbuildmat 2011.08.032)
P = {"Article Name": "Incorporation superabsorbent polymer (SAP) particles as controlling pre-existing flaws to improve the performance of engineered cementitious composites (ECC)",
     "Author": "Yan Yao, Yu Zhu, Yingzi Yang", "Year": 2012,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2011.08.032"}
B = 1272
for mid, c, fa, hr, eps, fu, fcs in [("ECC1-0", 636, 636, 17.4, 1.80, 5.00, {3: 33.0, 28: 65.7, 90: 77.6}),
                                      ("ECC2-0", 382, 890, 16.0, 2.50, 4.66, {3: 23.0, 28: 52.0, 90: 69.0})]:
    for age, fc in fcs.items():
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(318 / B), "SS / B (Silica sand)": r4(462 / B),
                  "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA tensile strength (MPa)": 1600,
                  "PVA elastic modulus (GPa)": 42, "Total fiber (vol%)": 2.0,
                  "Curing method": "demoulded 24 h, standard curing room 20 C RH 90 % 7 d, then laboratory 20 C RH 55 % until test",
                  "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": age,
                  "Compressive specimen": "prism halves (broken in bending)", "Compressive specimen size (mm)": "40x40",
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 2 (mix), Table 1 (PVA), Table 6 (fc), Table 4 (tensile 28 d), sect. 2.2/2.3",
                  "Conversions / notes": f"{mid} (SAP-free control; SAP mixes skipped). kg/m3 / B (cement + FA = 1272, Table 2 gives 382 + 890 for ECC2-0); fibre 26 kg/m3 / 1300 = 2.0 vol%. "
                                         "Sand = microsilica sand 150 um. HRWR = polycarboxylate. fc on 160x40x40 prism halves left after four-point bending (cross-section loaded 40x40). "
                                         "Tensile test only at 28 d (irregular-shaped specimens, six per mix)."})
        if age == 28:
            r.update({"Tensile specimen": "dumbbell/irregular shaped coupon", "Tensile test type": DIRECT, "Tensile strength (MPa)": fu,
                      "Tensile strain capacity (%)": eps})
            if mid == "ECC1-0":
                r["Conversions / notes"] += " VERIFY: Table 4 strain 1.80 % used; running text quotes 1.57 % for the 50 % FA SAP-free mix."
        rows.append(r)

# ---------------------------------------------------------------- 3) slag + FA ECC (conbuildmat 2012.04.031)
P = {"Article Name": "Use of slag to improve mechanical properties of engineered cementitious composites (ECCs) with high volumes of fly ash",
     "Author": "Yu Zhu, Yingzi Yang, Yan Yao", "Year": 2012,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2012.04.031"}
B = 1272
mixes = [("ECC70-0", 381.6, 890.4, 0, {28: (3.20, 4.66), 90: (2.79, 4.83)}),
         ("ECC60-10", 381.6, 763.2, 127.2, {28: (3.76, 4.88), 90: (3.28, 5.02)}),
         ("ECC50-20", 381.6, 636.0, 254.4, {28: (3.56, 5.04), 90: (3.30, 5.41)}),
         ("ECC40-30", 381.6, 508.8, 381.6, {28: (3.36, 5.33), 90: (2.51, 5.76)})]
for mid, c, fa, sl, d in mixes:
    for age, (eps, fu) in d.items():
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "GGBS": r4(sl / B) if sl else None, "W / B": r4(318 / B),
                  "SS / B (Silica sand)": r4(462 / B), "HRWR / B": r4(15.3 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0,
                  "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "Total fiber (vol%)": 2.0,
                  "Curing method": "demoulded 24 h, standard curing room 20 C RH 90 % 7 d, then laboratory 20 C RH 55 % until test",
                  "Curing time (days)": age, "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": age,
                  "Tensile specimen": "dog-bone", "Tensile test type": DIRECT, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 2 (mix), Table 3 (tensile), sect. 2.1/2.2 (materials, curing)",
                  "Conversions / notes": f"{mid}. kg/m3 / B (PC + FA + SL = 1272). PVA 26 kg/m3 / 1300 = 2.0 vol%. Sand = microsilica 150 um. HRWR polycarboxylate (15.3 kg/m3 in all). "
                                         "fc measured at 3/14/28/90 d but only in a figure, not entered. Tensile strain/strength = mean values (Table 3)."})
        rows.append(r)

# ---------------------------------------------------------------- 4) POFA ECC, POFA-free controls (conbuildmat 2012.08.003)
P = {"Article Name": "Flexural performance of green engineered cementitious composites containing high volume of palm oil fuel ash",
     "Author": "Nurdeen M. Altwair, M.A. Megat Johari, S.F. Saiyid Hashim", "Year": 2012,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2012.08.003"}
for mid, wb, sp, fc, eps in [("Ma1", 0.33, 0.022, 39.52, 1.52), ("Mb1", 0.36, 0.019, 37.35, None), ("Md1", 0.38, 0.015, 36.65, None)]:
    r = dict(P)
    r.update({"OPC / Cement": 1.0, "W / B": wb, "SS / B (Silica sand)": 0.8, "Sand max size (µm)": 200, "SP / B": sp,
              "HPMC / B (hydroxypropyl methyl cellulose)": 0.001,
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40,
              "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded 24 h (27 C), sealed plastic bags 6 d, then air at room temperature 27 +/- 3 C until 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 27, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix, 28-day fc), Table 3 (PVA), sect. 2.1/2.2, conclusions (strain 1.52 % for Ma1)",
              "Conversions / notes": f"{mid}: POFA-free control (mixes with POFA skipped). Ratios by mass of cement (B = cement). Fibre 0.02 = 2 vol% PVA (REC15 x 8). "
                                     "Silica sand 110 um mean / 200 um max. SP = HRWR Type F. Compressive specimen shape not stated."})
    if eps is not None:
        r.update({"Tensile specimen": "dog-bone 14x30 mm section", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT, "Tensile strain capacity (%)": eps})
        r["Conversions / notes"] += " VERIFY: strain 1.52 % quoted in the conclusion text for Ma1 (lowest of the series); tensile curves otherwise only in figures."
    rows.append(r)

# ---------------------------------------------------------------- 5) iron ore tailings ECC, silica sand mixes (conbuildmat 2013.03.088)
P = {"Article Name": "Development of green engineered cementitious composites using iron ore tailings as aggregates",
     "Author": "Xiaoyan Huang, Ravi Ranade, Wen Ni, Victor C. Li", "Year": 2013,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2013.03.088"}
for mid, fac, hr, fcr, fu, eps in [("C8", 2.2, 0.43, 3.3, 5.4, 3.2), ("C7", 4.4, 0.42, 2.4, 4.8, 4.7)]:
    B = 1 + fac
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fac / B), "W / B": 0.26, "SS / B (Silica sand)": 0.36, "HRWR / B": r4(hr / 100),
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded 1 d, plastic bag at room temperature 23 +/- 3 C for 27 d", "Curing time (days)": 28, "Curing temperature (°C)": 23,
              "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 100, "Tensile test type": DIRECT,
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix, ratios), Table 6 (tensile 28 d), sect. 2 (curing)",
              "Conversions / notes": f"{mid}: micro-silica sand (SS, ~110 um) reference mix; iron-ore-tailings mixes skipped. Ratios by mass: C 1, FA {fac}, SS/(FA+C) 0.36, "
                                     "water/(FA+C) 0.26, HRWRA/(FA+C) in % (0.42-0.43 %). PVA 2 vol%, 12 mm, 39 um oil coated 1.2 %. fc only in Fig. 13, not entered. "
                                     "Cement type not stated."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e15.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e15.csv"))
