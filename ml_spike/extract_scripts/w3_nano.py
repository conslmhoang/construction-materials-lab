# Builder for nano-/admixture-modified ECC / SHCC / fibre mortar additions (w3_nano.csv)
# Every number below was read from the cited paper's tables/text (full text via Europe PMC fullTextXML).
import csv, os
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
with open(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig") as f:
    H = next(csv.reader(f))
assert len(H) == 99
rows = []


def add(base, **kw):
    r = dict(base)
    r.update({k: v for k, v in kw.items() if v is not None})
    r = {k: v for k, v in r.items() if v is not None}
    for k in r:
        assert k in H, k
    rows.append(r)


R = lambda x, n=4: round(x, n)

# ---------------------------------------------------------------- 1 Peng et al. 2026 (MWCNT-coated PE fibres, PE-ECC)
B = 1432 + 143
b = {"Article Name": "Interfacial Enhancement of Polyethylene Fiber-Reinforced ECC via Multi-Walled Carbon Nanotubes Functionalization",
     "Author": "Peng B., Pan C., Huang Y., Wang H., Geng J., Chen Y., Meng X., Duan Y.", "Year": 2026,
     "DOI / URL": "https://doi.org/10.3390/nano16120714",
     "OPC / Cement": R(1432 / B), "FA (Fly ash)": R(143 / B), "W / B": R(300 / B), "Fine sand / B": R(420 / B), "Sand max size (µm)": 600,
     "SP / B": R(22 / B, 5), "Binder content (kg/m³)": B,
     "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 116,
     "Total fiber (vol%)": 1.5, "Curing method": "cured to test age (regime not stated)",
     "Tensile specimen": "dog-bone 330x60x30 mm", "Tensile test type": "direct"}
T6 = [("PE", None, 0, 3.81, 2.94, 4.70, 4.70), ("M-PE-A-2", "A", 2, 4.08, 3.41, 5.03, 5.91), ("M-PE-A-4", "A", 4, 4.21, 3.78, 5.22, 6.77),
      ("M-PE-A-8", "A", 8, 4.36, 4.09, 5.34, 7.02), ("M-PE-A-24", "A", 24, 4.37, 4.14, 5.38, 7.08), ("M-PE-OH-2", "OH", 2, 4.17, 3.33, 5.10, 5.72),
      ("M-PE-OH-4", "OH", 4, 4.23, 3.8, 5.25, 6.63), ("M-PE-OH-8", "OH", 8, 4.38, 4.12, 5.43, 6.98), ("M-PE-OH-24", "OH", 24, 4.43, 4.21, 5.46, 7.03),
      ("M-PE-COOH-2", "COOH", 2, 4.12, 3.48, 5.06, 5.97), ("M-PE-COOH-4", "COOH", 4, 4.28, 3.71, 5.31, 6.58),
      ("M-PE-COOH-8", "COOH", 8, 4.39, 4.17, 5.44, 7.07), ("M-PE-COOH-24", "COOH", 24, 4.41, 4.23, 5.42, 7.12)]
for g, typ, h, f7, e7, f28, e28 in T6:
    for age, ft, eps in [(7, f7, e7), (28, f28, e28)]:
        add(b, **{"Test age (days)": age, "Curing time (days)": age, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                  "Source table/page": "Table 1 (fibre), Table 3 (mix, kg/m3), Table 4 (groups), Table 6 (uniaxial tension)",
                  "Conversions / notes": f"{g}: matrix kg/m3 cement 1432, sand 420, FA 143, water 300, PCE SP 22; binder = cement+FA = {B}. "
                                         "P.O 42.5 cement, class F FA, natural fine sand FM 1.5 max 0.6 mm. PE fibre 1.5 vol% "
                                         + ("unmodified." if typ is None else f"pre-coated by immersion in MWCNTs-{typ} aqueous suspension for {h} h (no MWCNT dosage in matrix reported; nano modification is at fibre surface).")
                                         + " Compressive strength only in Fig. 6 (left blank). 3-point bending (40x40x160) strength in Table 7. Curing regime not stated."})

# ---------------------------------------------------------------- 2/3 Mohammed group 2020: GO-modified rubberized PVA-ECC (two papers, same Table 5 mixes)
B = 570 + 684
common = {"OPC / Cement": R(570 / B), "FA (Fly ash)": R(684 / B), "W / B": R(269.61 / B), "Sand (type not stated) / B": R(451.44 / B),
          "SP / B": R(2.51 / B, 5), "Binder content (kg/m³)": B,
          "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 41,
          "Total fiber (vol%)": 2.0, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50"}
mixnote = ("Table 5 kg/m3: cement 570, FA 684, sand 451.44, water 269.61, SP 2.51, PVA 2% (25.08 kg/m3); binder = cement+FA = 1254. "
           "Crumb rubber (CR) {cr}% replacement of fine aggregate ({crg} g listed; sand mass in Table 5 unchanged, so CR/B not computed). "
           "Graphene oxide {go}% by volume ({gog} g listed) - no GO column. Type I OPC, class F FA.")
GOg = {0.05: 9.59, 0.03: 5.76, 0.01: 1.92}
CRg = {0: 0.0, 5: 759.83, 10: 1519.67}
b = dict(common, **{"Article Name": "Acid and Sulphate Attacks on a Rubberized Engineered Cementitious Composite Containing Graphene Oxide",
                    "Author": "Sabapathy L., Mohammed B.S., Al-Fakih A., Wahab M.M.A., Liew M.S., Amran Y.H.M.", "Year": 2020,
                    "DOI / URL": "https://doi.org/10.3390/ma13143125", "Curing method": "water curing tank 28 d", "Curing time (days)": 28, "Test age (days)": 28})
for m, cr, go, fc in [(1, 0, 0.05, 62.39), (2, 0, 0.03, 54.98), (3, 0, 0.01, 55.71), (4, 5, 0.05, 50.98), (5, 5, 0.03, 53.48), (6, 5, 0.03, 52.38),
                      (7, 5, 0.03, 52.71), (8, 5, 0.03, 50.63), (9, 5, 0.03, 49.95), (10, 5, 0.01, 49.18), (11, 10, 0.05, 49.51), (12, 10, 0.03, 43.55),
                      (13, 10, 0.01, 41.54)]:
    add(b, **{"Compressive strength (MPa)": fc, "Source table/page": "Table 2 (PVA), Table 5 (mix), Table 6 (fc 28 d)",
              "Conversions / notes": f"Mix {m}: " + mixnote.format(cr=cr, crg=CRg[cr], go=go, gog=GOg[go]) + (" RSM centre-point replicate." if cr == 5 and go == 0.03 else "")})
b = dict(common, **{"Article Name": "Deformation Properties of Rubberized ECC Incorporating Nano Graphene Using Response Surface Methodology",
                    "Author": "Hau Hong D.L., Mohammed B.S., Al-Fakih A., Wahab M.M.A., Liew M.S., Amran Y.H.M.", "Year": 2020,
                    "DOI / URL": "https://doi.org/10.3390/ma13122831"})
for m, cr, go, fc, E in [(1, 0, 0.05, 45.81, 22.8), (2, 0, 0.01, 38.2, 15.08), (3, 0, 0.03, 42.26, 19.7), (4, 5, 0.03, 40.8, 20), (5, 5, 0.03, 44.21, 23.4),
                         (6, 5, 0.03, 39.5, 25.13), (7, 5, 0.05, 43.3, 28), (8, 5, 0.01, 40, 18.1), (9, 5, 0.03, 41.67, 20.45), (10, 5, 0.03, 40.19, 23),
                         (11, 10, 0.05, 40.1, 30.7), (12, 10, 0.03, 38.4, 22.4), (13, 10, 0.01, 35.18, 20.7)]:
    add(b, **{"Compressive strength (MPa)": fc, "Source table/page": "Table 2 (PVA), Table 5 (mix), Table 6 (fc, E)",
              "Conversions / notes": f"Mix {m}: " + mixnote.format(cr=cr, crg=CRg[cr], go=go, gog=GOg[go])
                                     + f" Elastic modulus {E} GPa. Curing regime and test age not stated in this paper (left blank). "
                                       "Same mixes as Sabapathy et al. 2020 (10.3390/ma13143125) but different reported fc - treat with care."})

# ---------------------------------------------------------------- 4 Liu et al. 2020 (nano-SiO2 + PVA, 19 mixes)
b = {"Article Name": "Compressive Strength Prediction of PVA Fiber-Reinforced Cementitious Composites Containing Nano-SiO2 Using BP Neural Network",
     "Author": "Liu T.Y., Zhang P., Wang J., Ling Y.F.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13030521",
     "FA (Fly ash)": 0.35, "W / B": 0.38, "SS / B (Silica sand)": 0.5, "HRWR / B": 0.003, "Binder content (kg/m³)": 1000}
for m, cem, pva, ns, fc in [(1, 650, 0, 0, 62.3), (2, 650, 2.73, 0, 64.8), (3, 650, 5.46, 0, 67.3), (4, 650, 8.19, 0, 61.8), (5, 650, 10.92, 0, 64.2),
                            (6, 650, 13.65, 0, 62.7), (7, 637, 0, 13, 59.5), (8, 637, 2.73, 13, 61.8), (9, 637, 5.46, 13, 64.3), (10, 637, 8.19, 13, 56.3),
                            (11, 637, 10.92, 13, 58.0), (12, 637, 13.65, 13, 54.9), (13, 643.5, 8.19, 6.5, 71.7), (14, 640.25, 8.19, 9.75, 69.5),
                            (15, 633.75, 8.19, 16.25, 55.4), (16, 637, 8.19, 13, 70.6), (17, 637, 8.19, 13, 57.5), (18, 637, 8.19, 13, 57.3),
                            (19, 637, 0, 13, 58.2)]:
    v = R(pva / 1300 * 100, 3)
    d = {"OPC / Cement": R(cem / 1000), "Nano-SiO2": R(ns / 1000), "PVA fiber (vol%)": v, "Total fiber (vol%)": v, "Compressive strength (MPa)": fc,
         "Source table/page": "Table 1 (mix, kg/m3 and fc)",
         "Conversions / notes": f"Mix {m}: water 380, cement {cem}, quartz sand 500, FA 350, PVA {pva}, nano-SiO2 {ns}, water reducer 3 kg/m3; "
                                f"binder = cement+FA+NS = 1000 kg/m3. PVA {pva} kg/m3 / 1300 (default density, not given) -> {v} vol%. "
                                "Curing, test age and specimen not stated in this paper (left blank)."
                                + (" Same composition as other mixes in Table 1 but different fc (as reported)." if m in (16, 17, 18, 19) else "")}
    add(b, **d)

# ---------------------------------------------------------------- 5 Ling et al. 2020 (sand size, PVA + 2% nano-SiO2)
b = {"Article Name": "Effect of Sand Size on Mechanical Performance of Cement-Based Composite Containing PVA Fibers and Nano-SiO2",
     "Author": "Ling Y.F., Zhang P., Wang J., Shi Y.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13020325",
     "OPC / Cement": 0.63, "FA (Fly ash)": 0.35, "Nano-SiO2": 0.02, "W / B": 0.38, "SS / B (Silica sand)": 0.5, "HRWR / B": 0.003,
     "Binder content (kg/m³)": 1000, "PVA fiber (vol%)": 0.9, "PVA length (mm)": 9, "PVA diameter (µm)": 20, "PVA tensile strength (MPa)": 1400,
     "Total fiber (vol%)": 0.9, "Curing method": "demoulded at 1 d, then 20 °C / 95% RH room to 28 d", "Curing time (days)": 28,
     "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28}
cn = ("Table 5 kg/m3: cement 630, FA 350, NS 20, sand 500, water 380, HRWR 3, PVA 0.9 vol%; binder = 1000. Silica sand fraction {s} µm. "
      "Other results (fc of mixes b-d, direct tension) only in figures.")
add(b, **{"Sand max size (µm)": 830, "Compressive strength (MPa)": 70.6, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
          "Source table/page": "Tables 2-5 (materials, mix), Sec. 3 text (fc of Mix a)", "Conversions / notes": "Mix a: " + cn.format(s="380-830")})
add(b, **{"Sand max size (µm)": 830, "Tensile strength (MPa)": 8.3, "Tensile specimen": "prism 40x40x160", "Tensile test type": "flexural",
          "Source table/page": "Tables 2-5 (materials, mix), Sec. 3 text (flexural, Mix a)", "Conversions / notes": "Mix a flexural: " + cn.format(s="380-830")})
add(b, **{"Sand max size (µm)": 120, "Tensile strength (MPa)": 6.6, "Tensile specimen": "prism 40x40x160", "Tensile test type": "flexural",
          "Source table/page": "Tables 2-5 (materials, mix), Sec. 3 text (flexural, Mix d)", "Conversions / notes": "Mix d flexural: " + cn.format(s="75-120")})

# ---------------------------------------------------------------- 6 Lee et al. 2023 (MWCNT + PVA, with SRA)
B = 412 + 220 + 412
b = {"Article Name": "Bond Behavior of Steel Rebar Embedded in Cementitious Composites Containing Polyvinyl Alcohol (PVA) Fibers and Carbon Nanotubes (CNTs)",
     "Author": "Lee D., Lee S.C., Yoo S.W.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/polym15040884",
     "OPC / Cement": R(412 / B), "GGBS": R(220 / B), "FA (Fly ash)": R(412 / B), "W / B": R(343 / B), "Sand (type not stated) / B": R(275 / B),
     "Sand max size (µm)": 1700, "SP / B": R(1.92 / B, 5), "Binder content (kg/m³)": B,
     "PVA fiber (vol%)": 2.07, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "Total fiber (vol%)": 2.07,
     "Curing method": "dry-cured 28 d", "Curing time (days)": 28, "Test age (days)": 28,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200"}
for g, cnt, fc in [("CNT-0.0", 0.0, 33.1), ("CNT-0.1", 0.1, 27.8), ("CNT-0.2", 0.2, 39.2), ("CNT-0.3", 0.3, 40.6)]:
    add(b, **{"Compressive strength (MPa)": fc, "Source table/page": "Table 2 (mix), Table 3 (PVA), Table 6 (fc average)",
              "Conversions / notes": f"{g}: MWCNT {cnt} wt.% (no CNT column). Table 2 kg/m3 OPC 412, BFS 220, FA 412, quartzite sand 275 (0.1-1.7 mm), "
                                     f"lightweight aggregate 14 (LA/B = {R(14 / B)}), SP 1.92, shrinkage-reducing admixture 0.4 (SRA/B = {R(0.4 / B, 5)}), water 343; "
                                     "W/B 32.9% as stated. CNTs dispersed as 3% aqueous solution with 5% PCE (extra SP not quantified). Peak strain and E also in Table 6."})

# ---------------------------------------------------------------- 7 Huang et al. 2022 (nano-SiO2 + PVA, HVFA mortar)
b = {"Article Name": "Effect of Nano-SiO2/PVA Fiber on Sulfate Resistance of Cement Mortar Containing High-Volume Fly Ash",
     "Author": "Huang J., Wang Z., Li D., Li G.", "Year": 2022, "DOI / URL": "https://doi.org/10.3390/nano12030323",
     "PVA length (mm)": 12, "PVA diameter (µm)": 38, "PVA tensile strength (MPa)": 1092, "PVA elastic modulus (GPa)": 30,
     "Curing method": "demoulded at 24 h, then air at 25 ± 2 °C (watered daily for first 7 d) to 28 d", "Curing time (days)": 28,
     "Curing temperature (°C)": 25, "Demolding age (days)": 1, "Test age (days)": 28}
for g, ns, pva, ff, fc in [("NS0-PVA0", 0, 0, 4.00, 13.00), ("NS0-PVA0.2", 0, 0.2, 3.65, 11.35), ("NS0-PVA0.5", 0, 0.5, 4.43, 14.98), ("NS0-PVA1.0", 0, 1.0, 5.73, 19.56),
                           ("NS0.5-PVA0", 0.5, 0, 5.21, 22.95), ("NS0.5-PVA0.2", 0.5, 0.2, 4.74, 23.33), ("NS0.5-PVA0.5", 0.5, 0.5, 5.21, 24.81),
                           ("NS0.5-PVA1.0", 0.5, 1.0, 6.16, 25.00), ("NS1.0-PVA0", 1.0, 0, 5.00, 19.68), ("NS1.0-PVA0.2", 1.0, 0.2, 4.98, 17.90),
                           ("NS1.0-PVA0.5", 1.0, 0.5, 5.50, 20.46), ("NS1.0-PVA1.0", 1.0, 1.0, 6.28, 22.58), ("NS1.5-PVA0", 1.5, 0, 5.59, 20.00),
                           ("NS1.5-PVA0.2", 1.5, 0.2, 5.60, 15.63), ("NS1.5-PVA0.5", 1.5, 0.5, 6.30, 19.59), ("NS1.5-PVA1.0", 1.5, 1.0, 7.59, 20.10)]:
    nsm = 550 * ns / 100
    B = 550 + nsm
    base = {"OPC / Cement": R(220 / B), "FA (Fly ash)": R(330 / B), "Nano-SiO2": R(nsm / B), "W / B": R(220 / B), "Sand (type not stated) / B": R(1100 / B),
            "SP / B": R(0.01 * 550 / B, 5), "Binder content (kg/m³)": R(B, 2), "PVA fiber (vol%)": pva, "Total fiber (vol%)": pva}
    if not pva:
        base.update({"PVA length (mm)": None, "PVA diameter (µm)": None, "PVA tensile strength (MPa)": None, "PVA elastic modulus (GPa)": None})
    note = (f"{g}: Table 3 kg/m3 water 220, cement 220, FA 330 (60% FA), standard sand 1100 (FM 2.85); NS {ns} wt.%, SP 1 wt.%. "
            f"VERIFY: NS and SP % basis not stated - assumed by mass of cement+FA, NS added on top (NS = {R(nsm, 2)} kg/m3, binder = cement+FA+NS). "
            "Flexural span 100 mm.")
    r = dict(b); r.update(base)
    add(r, **{"Compressive strength (MPa)": fc, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Source table/page": "Tables 2-3 (PVA, mix), Table 4 (28-d strengths)", "Conversions / notes": note})
    add(r, **{"Tensile strength (MPa)": ff, "Tensile specimen": "prism 40x40x160", "Tensile test type": "flexural",
              "Source table/page": "Tables 2-3 (PVA, mix), Table 4 (28-d strengths)", "Conversions / notes": note + " Flexural row."})

# ---------------------------------------------------------------- 8 Ivaniuk et al. 2022 (printable PE-SHCC with starch ether + cellulose ether)
for g, cem, fa, sus, w, sp, se, ce, wb, frac in [("Ref", 907, 378, 454, 74, 29.77, 0, 0, 0.212, (0.60, 0.25, 0.15)),
                                                ("SE-CE", 1013, 217, 434, 125, 28.50, 0.33, 1.09, 0.250, (0.70, 0.15, 0.15))]:
    B = cem / frac[0]
    b = {"Article Name": "Application-Driven Material Design of Printable Strain Hardening Cementitious Composites (SHCC)",
         "Author": "Ivaniuk E., Ivanova I., Sokolov D., Tošić Z., Eichenauer M.F., Lordick D., Mechtcherine V.", "Year": 2022,
         "DOI / URL": "https://doi.org/10.3390/ma15051631",
         "OPC / Cement": frac[0], "FA (Fly ash)": frac[1], "SF (Silica fume)": frac[2], "W / B": wb,
         "Fine sand / B": R(304 / B), "Sand max size (µm)": 1000, "SP / B": R(sp / B, 5), "Binder content (kg/m³)": R(B, 1),
         "PE fiber (vol%)": 1.5, "PE length (mm)": 6, "Total fiber (vol%)": 1.5,
         "Curing method": "3D-printed; wrapped in plastic film next day, climate chamber 20 °C / 65% RH", "Curing temperature (°C)": 20, "Curing RH (%)": 65}
    if se:
        b["VMA / B"] = R(se / B, 6)
        b["HPMC / B (hydroxypropyl methyl cellulose)"] = R(ce / B, 6)
    note = (f"{g}: Table 1 kg/m3 CEM I 52.5R {cem}, FA {fa}, microsilica suspension {sus}, sand 0.06-0.2 mm 91 + 0-1 mm 213, water {w}, SP {sp}, "
            f"PE (Dyneema SK60, 6 mm) 15.46 kg/m3, starch ether {se}, cellulose ether {ce}. Binder fractions and w/b as stated in text (microsilica as solids); "
            f"binder = cement/{frac[0]} = {R(B, 1)} kg/m3. Fibre 1.5 vol% as stated (15.46/970 = 1.59%). "
            + ("Starch ether (Starvis SE 35 F, 0.023% of binder) in VMA/B; cellulose ether Tylose MH 300 P2 (methyl-hydroxyethyl cellulose, 0.075% of binder) put in HPMC/B column. " if se else ""))
    for age, fcs, ffs in [(2, (66.5, 60.2, 68.4) if g == "Ref" else (65.5, 58.6, 70.0), (18.0, 16.4) if g == "Ref" else (16.4, 14.9)),
                          (7, (82.1, 63.8, 79.1) if g == "Ref" else (71.4, 64.7, 76.5), (21.9, 17.1) if g == "Ref" else (17.9, 15.2)),
                          (28, (83.2, 73.0, 82.2) if g == "Ref" else (80.9, 80.1, 79.5), (22.0, 18.5) if g == "Ref" else (21.4, 17.4))]:
        add(b, **{"Test age (days)": age, "Compressive strength (MPa)": R(sum(fcs) / 3, 2), "Compressive specimen": "cube (cut from print)",
                  "Compressive specimen size (mm)": "40", "Source table/page": "Table 1 (mix), Table 2 (fc), Sec. 2 text",
                  "Conversions / notes": note + f"fc = mean of directions D1/D2/D3 = {fcs} MPa."})
        add(b, **{"Test age (days)": age, "Tensile strength (MPa)": R(sum(ffs) / 2, 2), "Tensile specimen": "prism 160x40x40 (span 120)", "Tensile test type": "flexural",
                  "Source table/page": "Table 1 (mix), Table 3 (flexural), Sec. 2 text",
                  "Conversions / notes": note + f"Flexural = mean of directions D1/D3 = {ffs} MPa."})
    add(b, **{"Tensile strength (MPa)": 5.4 if g == "Ref" else 4.1, "Tensile specimen": "dumbbell (printed 600x40x20 mm layer)", "Tensile test type": "direct",
              "Source table/page": "Sec. 3 text (tension)",
              "Conversions / notes": note + "Average ultimate tensile strength from text; strain capacity 'between 2 and 3%' (Fig. 17, left blank). Test age not stated."})

# ---------------------------------------------------------------- 9 Yang et al. 2023 (PE + CaCO3 whisker + CNT multiscale ECC, Box-Behnken)
b = {"Article Name": "Optimisation of the Mechanical Properties and Mix Proportion of Multiscale-Fibre-Reinforced Engineered Cementitious Composites",
     "Author": "Yang B., Wang C., Chen S., Qiu K., Jiang J.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/polym15173531",
     "OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.3, "Sand (type not stated) / B": 0.5, "SP / B": 0.01,
     "PE length (mm)": 12, "PE diameter (µm)": 20,
     "Curing method": "standard curing room 20 ± 2 °C, RH 95 ± 5%", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95,
     "Test age (days)": 28, "Tensile specimen": "dog-bone (JSCE 2008)", "Tensile test type": "direct"}
lv = {"A": {-1: 1, 0: 1.5, 1: 2}, "B": {-1: 1, 0: 2, 1: 3}, "C": {-1: 0.1, 0: 0.15, 1: 0.2}}
T5 = [(1, -1, -1, 0, 57.38, 9.33, 3.92), (2, 1, -1, 0, 57.74, 11.02, 4.76), (3, -1, 1, 0, 62.11, 10.41, 4.41), (4, 1, 1, 0, 61.31, 11.46, 5.02),
      (5, -1, 0, -1, 62.22, 10.17, 4.68), (6, 1, 0, -1, 61.58, 11.63, 5.52), (7, -1, 0, 1, 62.45, 10.71, 4.85), (8, 1, 0, 1, 62.84, 11.56, 5.51),
      (9, 0, -1, -1, 56.26, 11.27, 6.22), (10, 0, 1, -1, 61.1, 12.08, 6.49), (11, 0, -1, 1, 57.33, 11.76, 6.32), (12, 0, 1, 1, 60.85, 12.31, 6.47),
      (13, 0, 0, 0, 65.54, 13.32, 7.32), (14, 0, 0, 0, 64.89, 13.53, 7.11), (15, 0, 0, 0, 66.87, 13.68, 7.25), (16, 0, 0, 0, 66.32, 13.42, 7.35),
      (17, 0, 0, 0, 65.21, 13.67, 7.37)]
for n, a, bb, c, fc, ff, ft in T5:
    pe, cw, cnt = lv["A"][a], lv["B"][bb], lv["C"][c]
    add(b, **{"PE fiber (vol%)": pe, "Total fiber (vol%)": pe, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Source table/page": "Table 2 (fibres), Table 3 (base mix), Table 4 (levels), Table 5 (results)",
              "Conversions / notes": f"Run {n}: PE {pe}%, CaCO3 whisker {cw}%, MWCNT {cnt}% (no CW/CNT columns; text calls CW/CNT 'mass replacement proportions', basis not fully clear). "
                                     "Base mix (Table 3, units as printed) cement 1350, FA 1350, ISO standard sand 1350, water 810, SP 27 -> W/B 0.30, sand/B 0.5, SP/B 0.01. "
                                     f"PE 12 mm, aspect ratio 600 (-> 20 µm), density 0.97. Flexural strength {ff} MPa." + (" Box-Behnken centre-point replicate." if (a, bb, c) == (0, 0, 0) else "")})

# ---------------------------------------------------------------- 10 Park et al. 2020 (PE-HPCC with shrinkage-reducing admixture)
B = 707.33 + 70.73 + 141.47
b = {"Article Name": "High-Performance Photocatalytic Cementitious Materials Containing Synthetic Fibers and Shrinkage-Reducing Admixture",
     "Author": "Park J.J., Kim S., Shin W., Choi H.J., Park G.J., Yoo D.Y.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13081828",
     "OPC / Cement": R(707.33 / B), "SF (Silica fume)": R(70.73 / B), "FA (Fly ash)": R(141.47 / B), "W / B": 0.28,
     "SS / B (Silica sand)": R(848.80 / B), "QP / B (Quartz powder)": R(141.47 / B), "SP / B": R(11.12 / B, 5), "VMA / B": R(3.33 / B, 5),
     "Binder content (kg/m³)": R(B, 2),
     "Curing method": "hot water 90 °C for 48 h (FHWA)", "Curing temperature (°C)": 90, "Heat curing duration (h)": 48,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200"}
note = ("Table 3 kg/m3: water 249.46, OPC 707.33, SF 70.73, FA 141.47, silica flour 141.47, silica sand 848.80, SP 11.12 (30% solids), viscosity agent 3.33, "
        "antifoam 2.00; W/B 0.28 as stated; binder = OPC+SF+FA. PE fibre 18 mm, 30-32 µm, 2900-3160 MPa, 88 GPa. "
        "fc values from text (Sec. 3.1); tension only in figures. Test age not stated. {x}")
add(b, **{"Total fiber (vol%)": 0, "Compressive strength (MPa)": 83.4, "Source table/page": "Table 2-3 (mix), Sec. 3 text (fc)",
          "Conversions / notes": "OP (plain, no fibre, no SRA): " + note.format(x="")})
for g, sra, fc in [("OP-P1", 0, 71.6), ("OP-P1S1", 1, 75.6)]:
    add(b, **{"PE fiber (vol%)": 1, "PE length (mm)": 18, "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1, "Compressive strength (MPa)": fc,
              "Source table/page": "Tables 1-3 (fibre, variables, mix), Sec. 3 text (fc)",
              "Conversions / notes": f"{g}: 1 vol% PE, SRA {sra}% (basis not stated; no SRA column). " + note.format(
                  x="Text: fc fell to 53.4 MPa with 2% and 3% SRA (not assigned to a single mix, not entered).")})

# ---------------------------------------------------------------- 11 Yu et al. 2026 (cellulose nanofibres + POM fibres in UHPC)
B = 1.25
b = {"Article Name": "Cross-Scale Synergistic Reinforcement of Ultra-High-Performance Concrete by Cellulose Nanofibers and Polyoxymethylene Fibers: Mechanical Behavior and Microstructural Mechanisms",
     "Author": "Yu P., Han X., Zheng P., Liu X.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19184005",
     "OPC / Cement": R(1 / B), "SF (Silica fume)": R(0.25 / B), "W / B": 0.18, "QP / B (Quartz powder)": None, "Sand (type not stated) / B": R(1.1 / B),
     "SP / B": R(0.015 / B, 5),
     "Curing method": "in mould 24 h, then standard curing chamber 20 ± 2 °C, RH ≥ 90%", "Curing time (days)": 28, "Curing temperature (°C)": 20,
     "Curing RH (%)": 90, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100"}
for g, pom, cnf, fc in [("P0C0", 0, 0, 117.47), ("P2C0", 2, 0, 115.33), ("P2C0.2", 2, 0.2, 128.89)]:
    add(b, **{"Total fiber (vol%)": pom, "Compressive strength (MPa)": fc, "Source table/page": "Tables 1-2 (materials, mix by weight), Sec. 3.1 text (fc)",
              "Conversions / notes": f"{g}: mix by weight OPC 1 : SF 0.25 : quartz sand 1.1 : SP 0.015, W/B 0.18; binder = OPC+SF. "
                                     f"Polyoxymethylene (POM) fibre {pom} vol% (28.2 kg/m3, 12 mm, 0.2 mm, E >= 8.8 GPa; no POM column - only Total fiber). "
                                     f"Cellulose nanofibre {cnf} wt% (cellulose solids/OPC = {cnf / 100}). Other CNF dosages and flexural values only in figures."})

df = pd.DataFrame(rows, columns=H)
out = os.path.join(D, "w3_nano.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", out)
