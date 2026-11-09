# Builder for w4_mdpi_new.csv: MDPI (Materials / Polymers) 2023-2026 ECC / SHCC / strain-hardening composites
# with DIRECT (uniaxial, dog-bone / dumbbell / coupon) tension data.
# Every number below was read from the cited paper's tables/text (full text via Europe PMC fullTextXML).
import csv, os, re, glob
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
DIRECT = {"Tensile test type": "direct"}

# ---------------------------------------------------------------- 1 Chen et al. 2024 Polymers - PET aggregate PE-ECC
B = 937 + 401
b = {"Article Name": "Effects of Polyethylene Terephthalate Particle Size on the Performance of Engineered Cementitious Composites",
     "Author": "Chen S., Liu R., Liu L., Huang X., Lin J.", "Year": 2024, "DOI / URL": "https://doi.org/10.3390/polym16152143",
     "OPC / Cement": R(937 / B), "FA (Fly ash)": R(401 / B), "W / B": R(335 / B), "HRWR / B": R(5.4 / B, 5), "VMA / B": R(0.21 / B, 5),
     "Binder content (kg/m³)": B,
     "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 116,
     "Total fiber (vol%)": 2.0, "Curing method": "sealed (film) at room temperature 24 h, demoulded, water curing 28 d",
     "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
     "Tensile specimen": "dog-bone 330x60x13 mm (JSCE)", "Tensile gauge length (mm)": 80, **DIRECT}
T = [("ECC", 401, 0, None, 98.2, 8.53, 5.29, 3.71), ("P-S", 341, 31.4, "PET-S D50 21 µm", 89.9, 10.07, 4.10, 5.98),
     ("P-M", 341, 31.4, "PET-M D50 107 µm", 89.2, 9.12, 3.37, 6.16), ("P-L", 341, 31.4, "PET-L D50 244 µm", 81.5, 7.97, 3.42, 3.47)]
for g, qp, pet, petd, fc, ft, fcr, eps in T:
    add(b, **{"QP / B (Quartz powder)": R(qp / B), "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (fibre), Table 3 (aggregates), Table 4 (mix, kg/m3), Table 6 (fc), Table 8 (uniaxial tension)",
              "Conversions / notes": f"{g}: kg/m3 cement 937, FA 401 (binder 1338), QP {qp}, water 335, HRWRA 5.4, VMA 0.21, defoamer 1.61, PE 19.4 kg/m3 (=2.0 vol% at 970 kg/m3). "
                                     "QP (quartz powder, D50 120 µm) is the only aggregate -> QP/B. "
                                     + ("No PET." if pet == 0 else f"PET plastic aggregate {pet} kg/m3 (PET/B={R(pet / B)}, 15 vol% replacement of QP; {petd}) - no PET-aggregate column.")
                                     + " P.II 52.5R cement. Mean of 3 specimens."})

# ---------------------------------------------------------------- 2 Tan et al. 2023 Polymers - CCCW in PE-ECC
B = 593.0 + 711.6
b = {"Article Name": "Effect of Cementitious Capillary Crystalline Waterproofing Materials on the Mechanical and Impermeability Properties of Engineered Cementitious Composites with Microscopic Analysis",
     "Author": "Tan Y., Zhao B., Yu J., Xiao H., Long X., Meng J.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/polym15041013",
     "OPC / Cement": R(593.0 / B), "FA (Fly ash)": R(711.6 / B), "W / B": R(387.1 / B), "Fine sand / B": R(474.4 / B), "Sand max size (µm)": 210,
     "HRWR / B": R(4.0 / B, 5), "Binder content (kg/m³)": R(B, 1),
     "PE fiber (vol%)": 1.5, "PE length (mm)": 12, "PE diameter (µm)": 25, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 1.5,
     "Curing method": "demoulded after 1 d, constant temperature and humidity container (values not stated) to 28 d",
     "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
     "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, **DIRECT}
mixnote = ("Table 2 kg/m3: cement 593.0, FA 711.6 (binder 1304.6), ultra-fine sand 474.4 (70-110 mesh, max 0.21 mm), water 387.1, HRWR 4.0, PE 14.7 (1.5 vol% stated). "
           "CCCW (cementitious capillary crystalline waterproofing admixture) {c} kg/m3 = {p}% of cementitious material - no CCCW column. PII 52.5 cement.")
T = [("PE-ECC (reference)", "none", 0, "0", R(53.8 / 1.3795, 1), R(5.56 / 1.1417, 2), R(7.53 / 1.2165, 2),
      "VERIFY: reference values back-calculated from text % increases (fc: X1.0 53.8 MPa = +37.95%; ft: 5.56 MPa = +14.17%; strain: 7.53% = +21.65%); cross-check S1.0 5.28/1.0842 = 4.87 MPa. "),
     ("CCCW-PE-ECC(X1.0%)", "XYPEX", 13.05, "1.0", 53.8, 5.56, 7.53, ""),
     ("CCCW-PE-ECC(S1.0%)", "SY1000", 13.05, "1.0", 51.3, 5.28, 7.11, ""),
     ("CCCW-PE-ECC(X2.0%)", "XYPEX", 26.09, "2.0", None, 4.15, 5.43, "fc only in Fig. 8 (blank). "),
     ("CCCW-PE-ECC(S2.0%)", "SY1000", 26.09, "2.0", None, 4.27, 5.33, "fc only in Fig. 8 (blank). ")]
for g, typ, c, p, fc, ft, eps, extra in T:
    add(b, **{"Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Sec. 3.1-3.2 text (fc, ultimate tensile stress/strain)",
              "Conversions / notes": f"{g} (CCCW type {typ}): " + extra + mixnote.format(c=c, p=p)
                                     + " 0.5% and 1.5% dosages only in Fig. 10-11 (not extracted)."})

# ---------------------------------------------------------------- 3 Yang et al. 2023 Materials - SMA fibre pull-out in PVA-ECC (ECC tension)
r = 2.4
add({"Article Name": "Bonding Mechanical Properties between SMA Fiber and ECC Matrix under Direct Pullout Loads",
     "Author": "Yang Z., Gong X., Wu Q., Fan L.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16072672",
     "OPC / Cement": R(1 / (1 + r)), "FA (Fly ash)": R(r / (1 + r)), "W / B": 0.26, "SS / B (Silica sand)": 0.36, "SP / B": R(0.0082 / (1 + r), 5),
     "PVA fiber (vol%)": 2.0, "PVA length (mm)": 9, "PVA diameter (µm)": 31, "PVA tensile strength (MPa)": 1500, "PVA elastic modulus (GPa)": 42,
     "Total fiber (vol%)": 2.0, "Curing method": "standard curing box, demoulded 24 h, then water tank (standard curing) 28 d",
     "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
     "Tensile specimen": "dumbbell, 13 mm thick (JC/T 2461-2018)", **DIRECT,
     "Tensile strength (MPa)": 4.25, "Tensile strain capacity (%)": 3.12,
     "Source table/page": "Table 1 (mix), Sec. 2.1 text (tension)",
     "Conversions / notes": "Table 1 mass ratios cement 1.0, FA 2.4, silica sand 0.36, water 0.26, PS (polycarboxylate) 0.0082, PVA 2 vol% (mix from ref [37]). "
                            "Sand and water taken as ratios to binder (W/cement would be implausible); SP assumed per unit cement and divided by (1+2.4) - ambiguous. "
                            "Strain 3.12% is defined as strain when stress drops to 85% of peak (post-peak), not strain at peak. Quartz sand 100-200 mesh. Type I OPC. fc of ECC not reported."})

# ---------------------------------------------------------------- 4 Khan et al. 2023 Materials - SHCC layers on RC beams
B = 555 + 666
add({"Article Name": "Structural Performance Improvement of Reinforced Concrete Beams by Strain-Hardening Cementitious Composite Layers",
     "Author": "Khan M.I., Sial S.U., Abbas Y.M., Fares G.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16145135",
     "OPC / Cement": R(555 / B), "FA (Fly ash)": R(666 / B), "W / B": R(315 / B), "Dune sand / B": R(466 / B), "Sand max size (µm)": 300,
     "Binder content (kg/m³)": B,
     "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 42,
     "Total fiber (vol%)": 2.0, "Curing method": "standard moist curing to 28 d", "Curing time (days)": 28, "Test age (days)": 28,
     "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 80, **DIRECT,
     "Compressive strength (MPa)": 58, "Tensile strength (MPa)": 4.35, "First-cracking strength (MPa)": 4.0, "Tensile strain capacity (%)": 2.0,
     "Source table/page": "Table 3 (mix, kg/m3), Sec. 2.1/3 text (fc, ft, strain), Sec. 4 model parameters (first crack)",
     "Conversions / notes": "Table 3 kg/m3 cement 555, class F FA 666 (binder 1221), dune sand 466, water 315 (W/B stated 0.26), PVA 2 vol%. "
                            "Text calls the sand fine silica sand ~200 µm passing 300 µm; table labels it dune sand. PCE SP dosage not given. "
                            "First-crack stress 4 MPa (strain 0.0326%) from the analytical-model parameter list (SHCC). Mean of 3 specimens; fc specimen not stated."})

# ---------------------------------------------------------------- 5 Zou et al. 2023 Materials - HSSSW lap splices in ECC
c = 1.0; fa = 2.5; B = c + fa
add({"Article Name": "Experimental Study on Lap-Spliced Performance of High-Strength Stainless Steel Wire Mesh in Engineering Cementitious Composites",
     "Author": "Zou X., Zhang X., Li Z., Zhu J.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16113959",
     "OPC / Cement": R(c / B), "FA (Fly ash)": R(fa / B), "W / B": R(1.15 / B), "SS / B (Silica sand)": R(0.4 / B), "QP / B (Quartz powder)": R(0.093 / B),
     "SP / B": R(0.058 / B, 5),
     "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0, "Curing method": "standard curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
     "Tensile specimen": "plate 280x40x15 mm", **DIRECT,
     "Compressive strength (MPa)": 32.5, "Tensile strength (MPa)": 3.1, "First-cracking strength (MPa)": 1.8, "Tensile strain capacity (%)": 1.96,
     "Source table/page": "Table 1 (mix ratios), Sec. 2.1 text (fc, tension)",
     "Conversions / notes": "Table 1 mass ratios: FA 2.5, silica powder 0.093, cement 1, silica sand 0.4, PVA 0.02, water 1.15, SP 0.058. Binder taken as cement+FA (3.5); "
                            "'silica powder' (type unspecified, could be silica fume) put in QP/B - VERIFY. PVA 0.02 interpreted as 2 vol% (not stated). "
                            "Preparation per ref [12]. Fibre properties not given."})

# ---------------------------------------------------------------- 6 Long et al. 2024 Polymers - ECC-GFRP spiral-confined RC column
B = 528 + 74 + 111 + 566
add({"Article Name": "Seismic Performance of Corroded ECC-GFRP Spiral-Confined Reinforced-Concrete Column",
     "Author": "Long X., Chen Z., Li P.", "Year": 2024, "DOI / URL": "https://doi.org/10.3390/polym16152110",
     "OPC / Cement": R(528 / B), "Limestone powder": R(74 / B), "SF (Silica fume)": R(111 / B), "GGBS": R(566 / B),
     "W / B": R(388 / B), "SS / B (Silica sand)": R(466 / B), "HRWR / B": R(3 / B, 5), "Binder content (kg/m³)": B,
     "PE fiber (vol%)": R(20 / 970 * 100, 2), "Total fiber (vol%)": R(20 / 970 * 100, 2),
     "Curing method": "demoulded 48 h, wrapped in wet geotextile + plastic film, water curing 14 d, tested at 28 d",
     "Curing time (days)": 14, "Demolding age (days)": 2, "Test age (days)": 28,
     "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "150x300",
     "Tensile specimen": "dog-bone (JSCE)", **DIRECT,
     "Compressive strength (MPa)": 49.6, "Tensile strength (MPa)": 7.4, "Tensile strain capacity (%)": 3.8,
     "Source table/page": "Table 1 (mix, kg/m3), Sec. 2.2 text (fc, tension)",
     "Conversions / notes": "Table 1 kg/m3 LP 74, SF 111, GGBFS 566, silica sand 466, cement 528, water 388, HRWR 3, PE fibre 20 kg/m3; paper defines W/(cement+LP+SF+GGBFS)=0.303 -> binder 1279 incl. LP. "
                            "PE vol% = 20/970 (assumed PE density). Mix after Li et al. [21]. Mean of 3 specimens; specimen curing assumed same as ECC tube (14 d wet)."})

# ---------------------------------------------------------------- 7 Zhang et al. 2026 Materials - fly ash tailoring of lightweight PVA-ECC (FAC)
b = {"Article Name": "Interfacial Friction-Controlled Fiber Failure Modes for Toughness Enhancement of Engineered Cementitious Composites",
     "Author": "Zhang D., Yang Y., Wang Z., Wang L.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19081643",
     "SF (Silica fume)": 0.05, "W / B": 0.25, "FA cenosphere / B": 0.3,
     "PVA fiber (vol%)": 1.2, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 1.2,
     "Curing method": "sealed under plastic 48 h, demoulded, fog room 20±2°C RH>90% until testing",
     "Curing temperature (°C)": 20, "Curing RH (%)": 90, "Demolding age (days)": 2,
     "Tensile specimen": "dog-bone / uniaxial tension (geometry in paper figures)", **DIRECT}
T = [("FA0", 0.95, 0, 0.03, 60.7, 3.73, 2.85, 1.92), ("FA12.5", 0.825, 0.125, 0.025, 63.7, 3.77, 2.84, 1.89),
     ("FA25", 0.70, 0.25, 0.025, 62.3, 4.08, 2.55, 2.76), ("FA37.5", 0.575, 0.375, 0.02, 48.2, 3.90, 2.51, 3.07),
     ("FA50", 0.45, 0.50, 0.02, 40.2, 3.54, 2.12, 2.84)]
for g, cem, fa, wra, fc, ft, fcr, eps in T:
    add(b, **{"OPC / Cement": cem, "FA (Fly ash)": fa, "SP / B": wra, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix, mass ratio of binder; fc), Table 7 (uniaxial tension, cited [36])",
              "Conversions / notes": f"{g}: Table 4 binder cement {cem} / FA {fa} / SF 0.05, water 0.25, FAC (fly ash cenosphere, inert lightweight filler) 0.3, WRA {wra}, PVA 1.2 vol% (Kuraray K-II, length not stated). "
                                     "No sand. Tension values in Table 7 are referenced to [36] (same mixes, authors' companion data). Test age not explicitly stated for tension/compression (left blank). CEM I 52.5 N."})

# ---------------------------------------------------------------- 8 Cao et al. 2025 Materials - SMAF-ECC joints (ECC material test)
B = 5.0
add({"Article Name": "Research on Seismic and Self-Centering Performance of SMAF-ECC Prefabricated Self-Centering Frame Joints Based on Finite Element Simulation",
     "Author": "Cao Y., Wu Q., Yang Z.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma19010110",
     "OPC / Cement": 0.2, "FA (Fly ash)": 0.8, "W / B": R(1.0 / B), "SS / B (Silica sand)": R(1.0 / B), "SP / B": R(0.0079 / B, 5),
     "PVA fiber (vol%)": 2.0, "Total fiber (vol%)": 2.0,
     "Curing method": "standard curing chamber 24 h, demoulded, standard curing room 28 d", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
     "Compressive specimen": "cube (standard)", "Tensile specimen": "dog-bone thin plate", **DIRECT,
     "Compressive strength (MPa)": 35.7, "Tensile strength (MPa)": 4.27, "First-cracking strength (MPa)": 2.57, "Tensile strain capacity (%)": 6.13,
     "Source table/page": "Table 3 (mix mass ratios), Table 4 (ECC mechanical properties)",
     "Conversions / notes": "Table 3 mass proportion cement 1.00, FA 4.00, quartz sand 1.00, water 1.00, water reducer 0.0079, PVA 2 vol%; ratios divided by binder 5.0. "
                            "First-crack strain 0.36%. Paper is mainly FE simulation, but Table 4 values are measured material tests. PVA properties not given."})

# ---------------------------------------------------------------- 9 Liu et al. 2026 Materials - HSSWM-ECC strengthened joints
B = 1 + 3 + 0.073
add({"Article Name": "Flexural Capacity Calculation Method for Pre-Damaged RC Beam-Column Joints Strengthened with High-Strength Steel Strand Mesh-Reinforced ECC",
     "Author": "Liu S., Wei Y., Li Z., Hu J., Li K., Li W., Xu S.", "Year": 2026, "DOI / URL": "https://doi.org/10.3390/ma19184002",
     "OPC / Cement": R(1 / B), "FA (Fly ash)": R(3 / B), "SF (Silica fume)": R(0.073 / B), "W / B": R(1.02 / B), "Fine sand / B": R(0.4 / B),
     "HRWR / B": R(0.0407 / B, 5), "HPMC / B (hydroxypropyl methyl cellulose)": R(0.0018 / B, 5),
     "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8,
     "Total fiber (vol%)": 2.0, "Curing method": "demoulded after 3 d, water-sprayed twice daily at room temperature to 28 d",
     "Curing time (days)": 28, "Demolding age (days)": 3, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7", "Tensile specimen": "dog-bone (JC/T 2461-2018)", **DIRECT,
     "Compressive strength (MPa)": 46.2, "Tensile strength (MPa)": 4.24, "Tensile strain capacity (%)": 3.83,
     "Source table/page": "Table 3 (mix mass ratios), Sec. 2.2 text (fc, tension means); Table 2",
     "Conversions / notes": "Table 3 mass ratios cement 1, sand 0.4, FA 3, SF 0.073, water 1.02, PVA 0.072, WR 0.0407, HPMC 0.0018; binder = cement+FA+SF = 4.073 (W/B 0.25 stated). "
                            "PVA 2.0 vol% stated. ft/strain = mean of 21 dog-bone tests; fc = overall batch mean 46.20 (range 43.33-48.87). Table 2 lists ECC fc 48.87, ft 4.60, strain 3.85 (not used)."})

# ---------------------------------------------------------------- 10 Wang et al. 2023 Materials - sprayed PVA mortar thin plates (short-fibre series)
B = 452 + 198 + 45 + 50
add({"Article Name": "Toughening Mechanism of Directional Fabric Woven Net and/or Non-Directional Short-Cut Fiber-Reinforced Sprayed Cement Mortar Thin-Plates",
     "Author": "Wang J., Yu D., Mu F., Ji X., Peng Y.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16124418",
     "OPC / Cement": R(452 / B), "FA (Fly ash)": R(198 / B), "SF (Silica fume)": R(45 / B), "Metakaolin": R(50 / B), "W / B": 0.25,
     "Fine sand / B": R(1400 / B), "SP / B": R(5 / B, 5), "Binder content (kg/m³)": B,
     "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600, "PVA elastic modulus (GPa)": 40,
     "Total fiber (vol%)": 2.0, "Curing method": "mould 24 h, standard curing room 20°C RH 95% for 7 d, cut, continued curing to 28 d",
     "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
     "Tensile specimen": "sprayed thin plate 15x50x350 mm", "Tensile gauge length (mm)": 150, **DIRECT,
     "Tensile strength (MPa)": 2.62, "First-cracking strength (MPa)": 2.24, "Tensile strain capacity (%)": 2.02,
     "Source table/page": "Table 1 (mix, kg/m3), Table 2 (fibre), Table 7 (FRCM-SP-T)",
     "Conversions / notes": "FRCM-SP (short-cut PVA only) series: kg/m3 cement 452, FA 198, SF 45, metakaolin 50 (binder 745), fine sand 1400, thixotropic agent 1.0, SP 5 (raised from 3.5 for PVA mix); W/B 0.25 stated. "
                            "Sprayed. Textile-reinforced series (CN, PN) not included. Matrix (plain sprayed mortar) fc 57.3 MPa reported - not the fibre mix, left blank. First-crack strain 0.026%."})

# ---------------------------------------------------------------- 11 Lu et al. 2025 Materials - precast monolithic ECC composite beams
B = 659.71 * 2
add({"Article Name": "Investigation on Shear Behavior of Precast Monolithic ECC Composite Beams",
     "Author": "Lu T., Wen Y., Wang B.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma18133081",
     "OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": R(445 / B), "SS / B (Silica sand)": R(480.59 / B), "Sand max size (µm)": 1180,
     "SP / B": R(16 / B, 5), "Binder content (kg/m³)": R(B, 2),
     "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560, "PVA elastic modulus (GPa)": 41,
     "Total fiber (vol%)": 2.0, "Curing method": "standard curing 28 d", "Curing time (days)": 28, "Test age (days)": 28,
     "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
     "Tensile specimen": "dog-bone", **DIRECT,
     "Compressive strength (MPa)": 50.0, "Tensile strength (MPa)": 4.16,
     "Source table/page": "Table 2 (fibre), Table 3 (mix, kg/m3), Table 4 (fc, ft)",
     "Conversions / notes": "Table 3 kg/m3 cement 659.71, FA 659.71 (binder 1319.42), water 445, quartz sand 480.59 (0.125-1.18 mm), SP 16, PVA 26 (2 vol% stated). "
                            "Axial (prism 100x100x300) compressive strength 43.2 MPa. Tensile strain not reported. P.O 42.5 cement."})

# ---------------------------------------------------------------- 12 Ling et al. 2025 Polymers - SFCB-reinforced ECC-concrete beams
B = 1200
add({"Article Name": "Experimental Study on Flexural Performance of SFCB-Reinforced ECC-Concrete Composite Beams",
     "Author": "Ling Y., Xu S., Bi C., Feng Z., Liang D., Cai Y.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/polym17202794",
     "OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": R(348 / B), "QP / B (Quartz powder)": R(432 / B), "SP / B": R(1.8 / B, 5),
     "HPMC / B (hydroxypropyl methyl cellulose)": R(1.8 / B, 5), "Binder content (kg/m³)": B,
     "PE fiber (vol%)": 2.0, "PE length (mm)": 12, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 2500, "PE elastic modulus (GPa)": 120,
     "Total fiber (vol%)": 2.0, "Curing method": "not stated for ECC coupons",
     "Tensile specimen": "dumbbell 330x60x13 mm (JC/T 2461-2018)", **DIRECT,
     "Tensile strength (MPa)": 8.04, "First-cracking strength (MPa)": 2.89, "Tensile strain capacity (%)": 5.5,
     "Source table/page": "Table 1 (mix, kg/m3), Table 2 (PE fibre), Sec. 2.1 text (tension)",
     "Conversions / notes": "Table 1 kg/m3 cement 600, FA 600 (binder 1200), QP 432, water 348, SP 1.8, PE 19.4 (=2.0 vol% at 970 kg/m3), VMA (HPMC) 1.8, defoamer 1.2. "
                            "Strain 0.055 mm/mm -> 5.5%; first-crack strain 0.04%. ECC compressive strength not reported. Test age not stated."})

# ---------------------------------------------------------------- 13 Liao et al. 2025 Materials - KOH-activated green UHPC (GUHPC), steel fibre
b = {"Article Name": "A Study on the Effect of Different Cementitious Materials on the Mechanical Properties and Microscopic Characteristics of Alkali-Activated Green Ultra-High Performance Concrete (GUHPC)",
     "Author": "Liao Z., Xue W., Liao L., Hao R., Shen L., Cui D.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma18092163",
     "Sand max size (µm)": 425,
     "Steel fiber (vol%)": R(156 / 7850 * 100, 2), "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2300,
     "Total fiber (vol%)": R(156 / 7850 * 100, 2),
     "Curing method": "sealed 24 h at 20±2°C, demoulded, standard moist curing 20±2°C RH>95% to 28 d",
     "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
     "Tensile specimen": "dog-bone", **DIRECT}
T = [("UHPC (control)", 820, 111, 111, 111, 0, 0, 0, 5.8, 187, 170.1, 7.9, 0.28),
     ("G1", 264, 111, 111, 111, 275, 275, 3.3, 5.6, 170, 155.2, 7.6, 0.39),
     ("G2", 264, 111, 0, 111, 330.5, 330.5, 3.3, 5.6, 170, 159.6, 7.6, 0.43),
     ("G3", 264, 111, 111, 0, 330.5, 330.5, 3.3, 5.6, 170, 151.4, 7.1, 0.50),
     ("G4", 264, 111, 111, 111, 219.5, 330.5, 3.3, 5.6, 170, 154.3, 7.7, 0.51),
     ("G5", 264, 111, 111, 111, 330.5, 219.5, 3.3, 5.6, 170, 165.3, 7.8, 0.32)]
for g, cem, sf, lp, qs, gg, fa, koh, sp, w, fc, ft, eps in T:
    B = cem + sf + lp + gg + fa
    add(b, **{"OPC / Cement": R(cem / B), "SF (Silica fume)": R(sf / B), "Limestone powder": R(lp / B), "GGBS": R(gg / B), "FA (Fly ash)": R(fa / B),
              "W / B": R(w / B), "SS / B (Silica sand)": R(1100 / B), "QP / B (Quartz powder)": R(qs / B), "SP / B": R(sp / B, 5),
              "Binder content (kg/m³)": R(B, 1),
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix, kg/m3), Table 4 / Sec. 3.1.1 (fc), Sec. 3.1.2 text (direct tension)",
              "Conversions / notes": f"{g}: kg/m3 cement {cem}, SF {sf}, LP {lp}, GGBS {gg}, FA {fa} (binder incl. LP = {R(B, 1)}), QS (2000-mesh quartz powder) {qs}, "
                                     f"quartz sand S1 550 + S2 220 + S3 330 = 1100 (0.106-0.425 mm), steel fibre 156 kg/m3 (=1.99 vol% at 7850), KOH {koh} (KOH/B={R(koh / B, 5) if koh else 0}; no KOH column), "
                                     f"SP {sp}, expansive agent {0.2 if koh == 0 else 0.16}, defoamer {1.7 if koh == 0 else 1.5}, water {w}. Strain = strain at ultimate tensile strength. fc specimen size not extracted."})

df = pd.DataFrame(rows).reindex(columns=H)

# checks
known = set()
for l in open(os.path.join(D, "existing_papers.txt"), encoding="utf-8-sig"):
    l = l.strip().lower()
    if l and not l.startswith("#"):
        known.add(re.sub(r"^https?://(dx\.)?doi\.org/", "", l))
for f in glob.glob(os.path.join(D, "*.csv")):
    if os.path.basename(f) in ("w4_mdpi_new.csv", "TEMPLATE.csv"):
        continue
    try:
        for x in pd.read_csv(f, encoding="utf-8-sig", usecols=["DOI / URL"])["DOI / URL"].dropna():
            known.add(re.sub(r"^https?://(dx\.)?doi\.org/", "", str(x).strip().lower()))
    except Exception:
        pass
dois = set(df["DOI / URL"].str.lower().str.replace("https://doi.org/", "", regex=False))
dup = dois & known
assert not dup, dup
bc = ["OPC / Cement", "SAC (Calcium sulfoaluminate cement)", "CAC (Calcium aluminate cement)", "GGBS", "FA (Fly ash)", "SF (Silica fume)", "Metakaolin",
      "Limestone powder", "Diatomite", "Nano-SiO2", "Recycled powder (C&D waste)", "Dolomite powder", "Pond ash (PA)", "Other binder", "RHA (Rice husk ash)",
      "EAFD (Electric arc furnace dust)", "Reactive MgO", "CKD (Cement kiln dust)"]
s = df[bc].fillna(0).sum(axis=1)
assert ((s - 1).abs() < 0.01).all(), s
assert df["W / B"].between(0.1, 0.7).all()
assert df["Compressive strength (MPa)"].dropna().between(2, 250).all()
assert df["Tensile strength (MPa)"].dropna().between(0.5, 25).all()
assert df["Tensile strain capacity (%)"].dropna().between(0, 15).all()
assert df["Total fiber (vol%)"].between(0, 6).all()
assert df["Total fiber (vol%)"].notna().all()

out = os.path.join(D, "w4_mdpi_new.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", out)
