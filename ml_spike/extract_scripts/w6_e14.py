"""Wave 6, agent e14: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e14.csv (99-column TEMPLATE header).
Papers: cemconcomp.2024.105813 (0.0BE only), cemconcomp.2025.106009 (verification mixes), ceramint.2021.12.254,
        ceramint.2022.12.057, coco.2021.100992, compositesb.2012.07.038
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
DIRECT = "direct (uniaxial)"
AUTH = "(authors not in text dump)"


def r4(x):
    return round(x, 4)


# ---------------------------------------------- 1) biochar ECC, biochar-free mix 0.0BE only (105813)
P = {"Article Name": "Sustainable and mechanical properties of Engineered Cementitious Composites with biochar: Integrating micro- and macro-mechanical insight",
     "Author": AUTH, "Year": 2024, "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2024.105813"}
B = 1000 + 300
r = dict(P)
r.update({"OPC / Cement": r4(1000 / B), "FA (Fly ash)": r4(300 / B), "W / B": r4(470 / B), "Sand (type not stated) / B": r4(800 / B),
          "SP / B": r4(55 / B), "HPMC / B (hydroxypropyl methyl cellulose)": r4(2.6 / B), "Binder content (kg/m³)": B,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
          "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": 2,
          "Curing method": "demoulded 24 h, standard curing room 25 C RH 95 % (compression: 28 d water-cured per sect. 2.3.2)",
          "Curing time (days)": 28, "Curing temperature (°C)": 25, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dumbbell", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 52.9, "Tensile strength (MPa)": 3.91, "First-cracking strength (MPa)": 2.04,
          "Tensile strain capacity (%)": 2.08,
          "Source table/page": "Table 1 (mix 0.0 BE), Table 3 (PVA), Table 4 (tensile), sect. 3.3 text (fc 52.9)",
          "Conversions / notes": "Only biochar-free mix 0.0BE (OPC 1000, FA 300, sand 800, water 470, SP 55, HPMC 2.6 kg/m3; B = 1300). "
                                 "Biochar mixes skipped (not in 21 materials). fc 52.9 MPa for 0.0 % biochar stated in text (Fig. 9 only gives bars). "
                                 "VERIFY: SP/B 0.042 is high (as in Table 1); curing described as 95 % RH room and also as water curing."})
rows.append(r)

# ---------------------------------------------- 2) materials-genome ECC paper, experimental verification mixes (106009)
P = {"Article Name": "New opportunity: Materials genome strategy for engineered cementitious composites (ECC) design",
     "Author": AUTH, "Year": 2025, "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2025.106009"}
for sc, opc, fa, lp, gg, sf, s, wb, vf, lf, ft, eu in [
        (1, .31, .21, .15, .24, .10, .34, .27, 1.47, 12, 4.20, 4.30), (2, .33, .21, .13, .23, .10, .33, .21, 1.57, 18, 7.48, 8.33)]:
    r = dict(P)
    r.update({"OPC / Cement": opc, "FA (Fly ash)": fa, "Limestone powder": lp, "GGBS": gg, "SF (Silica fume)": sf, "W / B": wb,
              "SS / B (Silica sand)": s, "PE fiber (vol%)": vf, "PE length (mm)": lf, "PE diameter (µm)": 24,
              "Total fiber (vol%)": vf, "Curing method": "air curing (28 d)", "Curing time (days)": 28, "Test age (days)": 28,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eu,
              "Source table/page": f"Table 9 (design scenario {sc} mix), sect. 4.2.5 text (measured tensile properties)",
              "Conversions / notes": f"Experimental verification of design scenario {sc}; ratios as printed in Table 9 (rounded, binder fractions sum to "
                                     f"{r4(opc + fa + lp + gg + sf)}). No compressive strength. SP/HRWR and HPMC dosages not given (HRWR and HPMC used). "
                                     "Silica sand mean 110 um, PE fibre 24 um. VERIFY: air curing temperature/RH not stated."})
    rows.append(r)

# ---------------------------------------------- 3) PE fibre geopolymer (FA/slag/SF), compressive only (ceramint 2021)
P = {"Article Name": "Effect of fiber factor on the workability and mechanical properties of polyethylene fiber-reinforced geopolymer",
     "Author": AUTH, "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.ceramint.2021.12.254"}
mix = {
    "0.35": [("E0.25-6", 84.67, 606.00, 176.00, 42.00, 313.33, 106.00), ("E0.45-6", 84.67, 604.67, 175.33, 42.00, 312.67, 106.00),
             ("E0.65-6", 84.67, 603.33, 175.33, 41.33, 312.00, 106.00), ("E0.85-6", 84.00, 602.67, 174.67, 41.33, 311.33, 105.33),
             ("E1.05-6", 84.00, 601.33, 174.67, 41.33, 310.67, 105.33), ("E1.25-6", 84.00, 600.00, 174.00, 41.33, 310.67, 105.33),
             ("E0.25-12", 84.67, 606.00, 176.00, 42.00, 313.33, 106.00), ("E0.45-12", 84.67, 604.67, 175.33, 42.00, 312.67, 106.00),
             ("E0.65-12", 84.67, 603.33, 175.33, 41.33, 312.00, 106.00), ("E0.85-12", 84.00, 602.67, 174.67, 41.33, 311.33, 105.33),
             ("E1.05-12", 84.00, 601.33, 174.67, 41.33, 310.67, 105.33), ("E1.25-12", 84.00, 600.00, 174.00, 41.33, 310.67, 105.33)],
    "0.38": [("E0.25-6", 84.67, 606.00, 176.00, 48.00, 313.33, 132.00), ("E0.45-6", 84.67, 604.67, 175.33, 48.00, 312.67, 132.00),
             ("E0.65-6", 84.67, 603.33, 175.33, 48.00, 312.00, 132.00), ("E0.85-6", 84.00, 602.67, 174.67, 48.00, 311.33, 131.33),
             ("E1.05-6", 84.00, 601.33, 174.67, 48.00, 310.67, 131.33), ("E1.25-6", 84.00, 600.00, 174.00, 48.00, 310.67, 130.67),
             ("E0.25-12", 84.67, 606.00, 176.00, 48.00, 313.33, 132.00), ("E0.45-12", 84.67, 604.67, 175.33, 48.00, 312.67, 132.00),
             ("E0.65-12", 84.67, 603.33, 175.33, 48.00, 312.00, 132.00), ("E0.85-12", 84.00, 602.67, 174.67, 48.00, 311.33, 131.33),
             ("E1.05-12", 84.00, 601.33, 174.67, 48.00, 310.67, 131.33), ("E1.25-12", 84.00, 600.00, 174.00, 48.00, 310.67, 130.67)]}
fc3 = {"0.35": [43.37, 45.69, 46.40, 44.72, 49.67, 47.79, 46.39, 45.54, 46.58, 46.61, 46.57, 46.81],
       "0.38": [50.22, 49.60, 47.30, 46.57, 46.68, 46.55, 44.94, 45.56, 42.81, 42.01, 43.47, 41.74]}
for wb, lst in mix.items():
    for (mid, c1, c2, sf, na, wg, w), fc in zip(lst, fc3[wb]):
        vf = float(mid.split("-")[0][1:])
        ln = int(mid.split("-")[1])
        B = c1 + c2 + sf
        r = dict(P)
        r.update({"FA (Fly ash)": r4(c1 / B), "GGBS": r4(c2 / B), "SF (Silica fume)": r4(sf / B), "NaOH / B": r4(na / B),
                  "WG / B (Water glass)": r4(wg / B), "W / B": r4(w / B), "Binder content (kg/m³)": r4(B),
                  "PE fiber (vol%)": vf, "PE length (mm)": ln, "PE diameter (µm)": 21.7, "PE tensile strength (MPa)": 3360,
                  "PE elastic modulus (GPa)": 115, "Total fiber (vol%)": vf,
                  "Curing method": "covered with film 24 h, demoulded, humid curing 20 +/- 2 C RH > 95 %", "Curing time (days)": 28,
                  "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
                  "Compressive specimen": "half prism (40 x 40 mm loaded area)", "Compressive specimen size (mm)": "40x40",
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 3 (mix), Table 2 (fibre), Table 6 (fc)",
                  "Conversions / notes": f"Paper id {wb}-{mid}. Table 3 kg/m3 / B (B = sum of the three solid columns {r4(B)}); 'water' column = extra water, "
                                         f"paper W/B {wb} also counts the water of the sodium silicate solution (not added here); WG / B = sodium silicate solution as dosed. "
                                         "VERIFY: Table 3 column labels fly ash/slag look swapped versus text (text: 70 % FA, 10 % slag, 20 % SF) - table labels used as printed. "
                                         "VERIFY: test age 28 d taken from flexural test (28 d); compressive tested on the broken halves. "
                                         "Fibre length 6/12 mm; strength/modulus are lower bounds (>=). Compressive only; no direct tension test."})
        rows.append(r)

# ---------------------------------------------- 4) ED-AASC, GGBS + Ca(OH)2 + crumb rubber (ceramint 2022)
P = {"Article Name": "Extremely-ductile alkali-activated slag-based composite with a tensile strain capacity up to 22 %",
     "Author": AUTH, "Year": 2023, "DOI / URL": "https://doi.org/10.1016/j.ceramint.2022.12.057"}
for mid, fcr, fts, eps, fc, how in [("R5-S8-M0", 5.08, 7.92, 9.81, 54.6, "derived"), ("R5-S8-M1", 4.70, 7.63, 22.34, 53.6, "text"),
                                    ("R5-S8-M2", 4.12, 8.19, 20.89, 52.2, "derived")]:
    r = dict(P)
    note_fc = ("fc 53.6 MPa stated in abstract (Table 7 says 53.4). " if how == "text" else
               f"VERIFY: fc derived as fts / (fts/fc ratio of Table 5) = {fc}; Fig. 7 only gives bars. ")
    r.update({"GGBS": 0.90, "Ca(OH)2 / B": 0.10, "W / B": 0.18, "SS / B (Silica sand)": 0.8, "Crumb rubber / B": 0.05, "SP / B": 0.106,
              "PE fiber (vol%)": 1.75, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700,
              "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1.75,
              "Curing method": "air 23 C 11 d, demould, water 23 C 12 d, oven 80 C 24 h, then air 23 C to 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Demolding age (days)": 11, "Test age (days)": 28, "Heat curing duration (h)": 24,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dumbbell", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": fts, "First-cracking strength (MPa)": fcr,
              "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (mix), Table 3 (PE), Table 4 (tensile), Table 5 / abstract (fc)",
              "Conversions / notes": f"{mid}: same composition for M0-M2, only the mixing procedure differs. Mass ratios by weight of binder "
                                     "(GGBS 0.9 + Ca(OH)2 0.1 = 1; GGBS column = 0.9, Ca(OH)2 / B = 0.1). W/B 0.18 excludes SP water (0.26 incl. SP water); "
                                     "SP / B 0.106 liquid as dosed (solid 0.031); defoamer 0.001. " + note_fc})
    rows.append(r)

# ---------------------------------------------- 5) HS-UHTCC and UHS-UHTCC (coco 2021)
P = {"Article Name": "Development of ultrahigh-strength ultrahigh-toughness cementitious composites (UHS-UHTCC) using polyethylene and steel fibers",
     "Author": AUTH, "Year": 2021, "DOI / URL": "https://doi.org/10.1016/j.coco.2021.100992"}
for mid, c, sf, sl, sand, w, sp, pe, pel, st, cur, heat, fc, ft, eu in [
        ("HS-UHTCC", 630, 207, 675, 454, 272, 22, 2.0, 18, 0.0, "demoulded 24 h, 23 C RH 95 % 28 d", None, 108, 9.6, 10.3),
        ("UHS-UHTCC", 1101, 344, 193, 495, 244, 22, 2.0, 12, 1.0, "demoulded 24 h, 90 C water 24 h, then 23 C RH 95 % 28 d", 24, 183, 13.8, 4.7)]:
    B = c + sf + sl
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "SF (Silica fume)": r4(sf / B), "GGBS": r4(sl / B), "W / B": r4(w / B),
              "Sand (type not stated) / B": r4(sand / B), "SP / B": r4(sp / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": pe, "PE length (mm)": pel, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100,
              "Total fiber (vol%)": pe + st, "Curing method": cur, "Curing time (days)": 28, "Curing temperature (°C)": 23, "Curing RH (%)": 95,
              "Demolding age (days)": 1, "Test age (days)": 28, "Heat curing duration (h)": heat,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 80,
              "Tensile test type": DIRECT, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eu,
              "Source table/page": "Table 1 (mix), Table 2 (fibres), sect. 2.1, 3.1, 3.2 text",
              "Conversions / notes": f"{mid}; kg/m3 / B (cement + SF + slag = {B}). VERIFY: test age taken as 28 d (cured 28 d after demoulding)."})
    if st:
        r.update({"Steel fiber (vol%)": st, "Steel length (mm)": 8, "Steel diameter (µm)": 115, "Steel tensile strength (MPa)": 3000,
                  "Steel elastic modulus (GPa)": 200})
    rows.append(r)

# ---------------------------------------------- 6) high-volume slag ECC (compositesb 2012)
P = {"Article Name": "Dual effectiveness of freezing-thawing and sulfate attack on high-volume slag-incorporated ECC",
     "Author": AUTH, "Year": 2012, "DOI / URL": "https://doi.org/10.1016/j.compositesb.2012.07.038"}
for mid, w, pc, s, ss, pva, hr, fc in [("S/PC = 1.2", 380, 576, 691, 456, 26, 5.4, 61.7), ("S/PC = 2.2", 379, 395, 868, 455, 26, 5.2, 59.2),
                                       ("S/PC = 4.2", 378, 242, 1017, 454, 26, 4.5, 56.1)]:
    B = pc + s
    r = dict(P)
    r.update({"OPC / Cement": r4(pc / B), "GGBS": r4(s / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(ss / B), "HRWR / B": r4(hr / B),
              "Binder content (kg/m³)": B, "PVA fiber (vol%)": r4(pva / 1300 * 100), "Total fiber (vol%)": r4(pva / 1300 * 100),
              "Curing method": "demoulded 24 h, sealed bags 95 % RH 23 C 7 d, then air 50 % RH 23 C to 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix + 28 d strength), sect. 2.2 (curing)",
              "Conversions / notes": f"{mid}. kg/m3 / B (PC + slag = {B}). VERIFY: PVA vol% derived from 26 kg/m3 / 1300 (density assumed); fibre length/diameter not found in text. "
                                     "Reference (non-exposed) compressive specimens only; F-T / sulfate flexural data skipped."})
    rows.append(r)

df = pd.DataFrame(rows)
for c in cols:
    if c not in df.columns:
        df[c] = None
df = df[cols]
df.to_csv(os.path.join(out_dir, "w6_e14.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows", df["DOI / URL"].nunique(), "papers")
