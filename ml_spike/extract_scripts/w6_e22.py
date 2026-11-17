"""Wave 6, agent e22: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e22.csv (99-column TEMPLATE header).
Papers: conbuildmat.2021.124482, 2022.127093, 2022.127933, jobe.2022.105518, jobe.2023.107455,
        matdes.2013.06.034, matpr.2023.05.024
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


# ---------------------------------------------- 1) green UHPC low cement (124482)
P = {"Article Name": "Green ultra-high performance concrete with very low cement content",
     "Author": "Ye Shi, Guangcheng Long, Xiaohui Zeng, Youjun Xie, Huihui Wang", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.124482"}
# id: opc, ggbs, sf, fa, na2so4, water, sp, sand, fc, fcr, post
t = {"U": (856, 0, 214, 0, 0, 182, 24.6, 1177, 158.4, 7.3, 8.7),
     "G1": (577, 105, 210, 157, 0, 178, 15.7, 1154, 166.7, 4.7, 7.7),
     "G2": (364, 312, 208, 156, 0, 177, 8.8, 1145, 148.9, 4.2, 5.9),
     "G2-SS": (362, 311, 207, 155, 5.2, 177, 13.5, 1145, 164.3, 6.8, 7.5)}
for mid, (c, g, sf, fa, ss, w, sp, sa, fc, fcr, post) in t.items():
    B = c + g + sf + fa + ss
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "GGBS": r4(g / B) or None, "SF (Silica fume)": r4(sf / B), "FA (Fly ash)": r4(fa / B) or None,
              "Na2SO4 / B": r4(ss / B) or None, "W / B": r4(w / B), "SP / B": r4(sp / B), "SS / B (Silica sand)": r4(sa / B),
              "Binder content (kg/m³)": round(B, 1), "Steel fiber (vol%)": r4(160 / 7850 * 100), "Total fiber (vol%)": r4(160 / 7850 * 100),
              "Curing method": "covered 24 h lab, demoulded, standard curing room 20 +/- 2 C RH > 95 %", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "prism (40x40x160)", "Compressive specimen size (mm)": "40x40x160",
              "Tensile specimen": "dog-bone (clip gauge)", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "First-cracking strength (MPa)": fcr,
              "Source table/page": "Table 2 (mix), Table 3 (fc, first cracking), sect. 3.2/3.3",
              "Conversions / notes": f"{mid}. kg/m3 / B (OPC+GGBS+SF+FA+Na2SO4; nano mixes G2-NS/G2-NA skipped). Steel fiber 160 kg/m3 / 7850 = 2.04 vol% "
                                     f"(density assumed; fibre geometry not given). Post-cracking strength {post} MPa not entered as tensile strength. "
                                     "Sand = quartz sand (Table 6). No tensile strain value in paper (curves only). "
                                     "VERIFY: compressive strength test on 40x40x160 prism at 28 d stated in sect. 3.3; fibre assumed steel (text 'steel fiber')."})
    rows.append(r)

# ---------------------------------------------- 2) cost-effective green ECC, PVA only mixes (127093)
P = {"Article Name": "Effects of different mixing ratio parameters on mechanical properties of cost-effective green engineered cementitious composites (ECC)",
     "Author": "Mingzheng Zhu, Bing Chen, Meng Wu, Jiaxing Han", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2022.127093"}
# id, S/b, W/b, size, fcr, fu, eps
t = [("P-1", .36, .35, 150, 3.08, 3.75, 2.67), ("P-2", .36, .35, 300, 1.67, 2.34, 2.58), ("P-3", .36, .35, 850, 1.52, 1.92, 1.36),
     ("P-4", .36, .35, 1180, 0.71, 0.82, 0.71), ("P-5", .50, .35, 300, 2.03, 3.21, 1.11), ("P-6", .64, .35, 300, 1.37, 3.13, 0.45),
     ("P-7", .36, .30, 300, 2.4, 3.02, 1.82), ("P-8", .36, .25, 300, 1.27, 2.75, 0.85)]
for mid, sb, wb, sz, fcr, fu, eps in t:
    r = dict(P)
    r.update({"OPC / Cement": 0.2, "FA (Fly ash)": 0.6, "SF (Silica fume)": 0.2, "W / B": wb, "River sand / B": sb, "Sand max size (µm)": sz,
              "SP / B": 0.005, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 40, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded 1 d, then water tank until test", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone (JSCE)", "Tensile test type": DIRECT, "First-cracking strength (MPa)": fcr,
              "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, by weight), Table 2 (PVA), Table 5 (tensile 28 d), sect. 3.2/3.3",
              "Conversions / notes": f"{mid}. Ratios by weight to binder (cement 0.2, FA 0.6, SF 0.2 = 1); S/b {sb}. Basalt hybrid mixes PH-9..12 skipped. "
                                     "fc only in Fig. 7 (not entered). Curing water temperature not stated. Binder kg/m3 not given."})
    rows.append(r)

# ---------------------------------------------- 3) ECC with FA / GGBS, own experiments (127933)
P = {"Article Name": "Prediction on compressive strength of Engineered Cementitious composites using Machine learning approach",
     "Author": "N. Shanmugasundaram, S. Praveenkumar, K. Gayathiri, S. Divya", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2022.127933"}
for mid, fa, gg, fc in [("MA-0", 0, 0, 31.073), ("FA-10", .1, 0, 39.900), ("FA-20", .2, 0, 34.336), ("FA-30", .3, 0, 30.743),
                        ("GGBS-10", 0, .1, 37.283), ("GGBS-20", 0, .2, 37.286), ("GGBS-30", 0, .3, 36.956)]:
    B = 1 + fa + gg
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "FA (Fly ash)": r4(fa / B) or None, "GGBS": r4(gg / B) or None, "W / B": 0.3, "M-sand / B": 0.8,
              "HRWR / B": 0.012, "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
              "Curing method": "24 h room temperature, demoulded, water curing 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 7 (fc), sect. 4.2/4.3",
              "Conversions / notes": f"{mid}. Table 3 gives cement 1, FA/GGBS x (ratio to cement); B = cement + FA/GGBS; W/B 0.3, S/B 0.8, HRWR/B 0.012 as stated. "
                                     "Only the own 7 mixes entered (literature database of the ANN not used). "
                                     "VERIFY: 'Fibres 2 %' taken as vol% PVA; ratios assumed relative to total binder."})
    rows.append(r)

# ---------------------------------------------- 4) fibre orientation ECC, random-cast tension (105518)
P = {"Article Name": "Influence of fiber orientation on the mechanical responses of engineering cementitious composite (ECC) under various loading conditions",
     "Author": "Abdullah M. Tawfek, Zhi Ge, Huaqiang Yuan, Ning Zhang, Hongzhi Zhang, Yifeng Ling, Yanhua Guan, Branko Savija", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2022.105518"}
B = 568 + 682
r = dict(P)
r.update({"OPC / Cement": r4(568 / B), "FA (Fly ash)": r4(682 / B), "W / B": r4(325 / B), "SS / B (Silica sand)": r4(455 / B),
          "HRWR / B": r4(6.25 / B), "VMA / B": r4(0.57 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": r4(26 / 1300 * 100),
          "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1650, "PVA elastic modulus (GPa)": 39.5,
          "Total fiber (vol%)": r4(26 / 1300 * 100), "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
          "First-cracking strength (MPa)": 2.67, "Tensile strength (MPa)": 4.55, "Tensile strain capacity (%)": 3.51,
          "Source table/page": "Table 1 (mix), Table 3 (PVA), Table 9 (T-R, 28 d)",
          "Conversions / notes": "T-R = conventionally (random) cast dog-bone; flow-induced aligned specimens skipped. kg/m3 / B (cement + FA). "
                                 "PVA 26 kg/m3 / 1300 = 2.0 vol%. Quartz sand. Curing method not stated. Compressive strength 51.4 MPa (C-R, Table 6) "
                                 "not entered: age (7 or 28 d) ambiguous. VERIFY: test age 28 d from Table 9 caption."})
rows.append(r)

# ---------------------------------------------- 5) gold tailings ECC, quartz-sand mixes only (107455)
P = {"Article Name": "Preparation of low-cost green engineered cementitious composites (ECC) using gold tailings and unoiled PVA fiber",
     "Author": "Yanhua Guan, Yifan Li, Hongzhi Zhang, Renjuan Sun, Jun Tian, Yongwei Yang", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.jobe.2023.107455"}
fib = {"REC-15": (40, 41, 1560), "CAS-FT701": (41, 39.5, 1650)}
t = [("Q1T0J2.0", 553.5, 664.2, 438.4, 341.0, .55, 5.48, 26.0, "REC-15", 3.81, 4.08, 5.37),
     ("Q1T0C1.6", 555.8, 667.0, 440.2, 342.4, .56, 5.50, 20.8, "CAS-FT701", 1.83, 2.62, 4.32),
     ("Q1T0C1.8", 554.7, 665.6, 439.3, 341.7, .55, 5.49, 23.4, "CAS-FT701", 3.19, 2.95, 4.73),
     ("Q1T0C2.0", 553.5, 664.2, 438.4, 341.0, .55, 5.48, 26.0, "CAS-FT701", 2.83, 3.94, 4.99)]
for mid, c, fa, qs, w, vma, sp, fk, ft, fcr, eps, fu in t:
    B = c + fa
    d, e, s = fib[ft]
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(qs / B), "SP / B": r4(sp / B),
              "VMA / B": r4(vma / B), "Binder content (kg/m³)": round(B, 1), "PVA fiber (vol%)": r4(fk / 1300 * 100), "PVA length (mm)": 12,
              "PVA diameter (µm)": d, "PVA tensile strength (MPa)": s, "PVA elastic modulus (GPa)": e, "Total fiber (vol%)": r4(fk / 1300 * 100),
              "Curing method": "sealed 20 C 24 h, demoulded, curing room 20 +/- 2 C RH 95 %", "Curing time (days)": 28, "Curing temperature (°C)": 20,
              "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28, "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80,
              "Tensile test type": DIRECT, "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": fu, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix), Table 2 (PVA), Table 5 (tensile 28 d), sect. 2.2",
              "Conversions / notes": f"{mid}, fibre {ft} (unoiled PVA). kg/m3 / B (cement + FA). PVA {fk} kg/m3 / 1300 = vol% (nominal 1.6/1.8/2.0). "
                                     "Gold-tailings mixes skipped. fc of ECC not reported (mortar only). sigma_fc = first cracking, sigma_p = peak stress."})
    rows.append(r)

# ---------------------------------------------- 6) UHP-FRC final optimised mix (matdes 2013)
P = {"Article Name": "Evaluation of ultra-high-performance-fiber reinforced concrete binder content using the response surface method",
     "Author": "M.A.A. Aldahdooh, N. Muhamad Bunnori, M.A. Megat Johari", "Year": 2013,
     "DOI / URL": "https://doi.org/10.1016/j.matdes.2013.06.034"}
B = 720.49 + 214.25
for age, fc, ft in [(7, 175.75, 11.31), (14, 179.53, None), (28, 181.41, 12.49)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(720.49 / B), "SF (Silica fume)": r4(214.25 / B), "W / B": r4(168.30 / B), "Sand (type not stated) / B": r4(1057.31 / B),
              "SP / B": r4(50.43 / B), "Binder content (kg/m³)": round(B, 2), "Steel fiber (vol%)": r4(468 / 7850 * 100),
              "Steel diameter (µm)": 160, "Steel tensile strength (MPa)": 2850, "Total fiber (vol%)": r4(468 / 7850 * 100),
              "Curing method": "demoulded 24 h, steam 90 C 100 % RH 48 h, then water 27 +/- 2 C", "Curing time (days)": age,
              "Curing temperature (°C)": 90, "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": age, "Heat curing duration (h)": 48,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "100", "Tensile specimen": "dog-bone 16x30 mm section",
              "Tensile gauge length (mm)": 80, "Compressive strength (MPa)": fc,
              "Source table/page": "Table 5 (final mix and properties), sect. 2.4/2.5",
              "Conversions / notes": "Final RSM mix. kg/m3 / B (OPC + SF = 934.74). Mining sand 100-1180 um. Steel fibres 390 (6 mm) + 78 (13 mm) = 468 kg/m3 / 7850 = 5.96 vol%; "
                                     "two lengths (6 and 13 mm), diameter 0.16 mm. Naphthalene SP. Direct tensile strength " + (f"{ft} MPa" if ft else "not tested at 14 d") +
                                     " (stored in Tensile strength). No strain capacity. Other 9 RSM mixes: fc only in Fig. 2, not entered. "
                                     "VERIFY: test age counted from casting."})
    if ft:
        r.update({"Tensile strength (MPa)": ft, "Tensile test type": DIRECT})
    rows.append(r)

# ---------------------------------------------- 7) ECC with manufactured sand gradation (matpr 2023)
P = {"Article Name": "Influence of manufactured sand gradation and water cement ratios on compressive strength of engineered cementitious composites",
     "Author": "N. Shanmugasundaram, S. Praveenkumar", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.matpr.2023.05.024"}
fcs = {("FS-0.38", .38): (9.840, 15.745, 27.554), ("FS-0.33", .33): (26.570, 33.458, 46.251),
       ("MS-0.38", .38): (14.761, 21.649, 35.426), ("MS-0.34", .34): (26.570, 36.410, 48.219),
       ("CS-0.38", .38): (29.522, 40.347, 54.124), ("CS-0.37", .37): (None, 47.235, 58.060)}
mx = {"FS": 600, "MS": 1180, "CS": 4750}
for (mid, wc), vals in fcs.items():
    for age, fc in zip((3, 7, 28), vals):
        if fc is None:
            continue
        r = dict(P)
        r.update({"OPC / Cement": 1.0, "W / B": wc, "M-sand / B": r4(456 / 1254), "Binder content (kg/m³)": 1254, "Sand max size (µm)": mx[mid[:2]],
                  "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "Total fiber (vol%)": 2.0,
                  "Curing method": "demoulded 24 h, water curing until test", "Curing time (days)": age, "Demolding age (days)": 1, "Test age (days)": age,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.6", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 2 (mix), Table 1 (fibre, sand), Table 3 (min/max fc)",
                  "Conversions / notes": f"{mid}. Cement-only binder 1254 kg/m3, M-sand 456 kg/m3, water = w/c x 1254; PVA 26 kg/m3 (2 %). "
                                         "Only the min and max strength mixes of each sand grading are tabulated (6 mixes). "
                                         "VERIFY: curing age counted from casting; Table 3 duplicates 26.570 MPa (3 d) for FS-0.33 and MS-0.34; "
                                         "conclusions quote CS 3-d max 34.410 vs 36.410 in Table 3, so CS-0.37 3-d value omitted."})
        rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e22.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e22.csv"))
