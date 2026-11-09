# Builder for Scientific Reports (Nature portfolio) additions -> additions/w4_scirep.csv
# Every number below was read from the cited paper's HTML tables / text on nature.com
# (article page + /tables/N pages). Values taken from approximate text statements or derived
# from % changes are flagged with VERIFY in "Conversions / notes".
import os, glob, re
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
NAME = "w4_scirep"
COLS = list(pd.read_csv(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []


def add(**kw):
    r = {}
    for k, v in kw.items():
        col = MAP.get(k, k)
        assert col in COLS, col
        r[col] = v
    rows.append(r)


MAP = {
    "title": "Article Name", "author": "Author", "year": "Year", "doi": "DOI / URL",
    "OPC": "OPC / Cement", "GGBS": "GGBS", "FA": "FA (Fly ash)", "SF": "SF (Silica fume)",
    "LP": "Limestone powder", "other": "Other binder", "RHA": "RHA (Rice husk ash)",
    "WB": "W / B", "SS": "SS / B (Silica sand)", "sand": "Sand (type not stated) / B",
    "msand": "M-sand / B", "maxsize": "Sand max size (µm)", "QP": "QP / B (Quartz powder)",
    "SP": "SP / B", "binder": "Binder content (kg/m³)",
    "steel": "Steel fiber (vol%)", "steel_L": "Steel length (mm)", "steel_d": "Steel diameter (µm)",
    "steel_ft": "Steel tensile strength (MPa)", "PET": "PET fiber (vol%)", "basalt": "Basalt fiber (vol%)",
    "carbon": "Carbon fiber (vol%)", "total": "Total fiber (vol%)",
    "cure": "Curing method", "cure_t": "Curing time (days)", "cure_T": "Curing temperature (°C)",
    "RH": "Curing RH (%)", "demold": "Demolding age (days)", "age": "Test age (days)",
    "heat_h": "Heat curing duration (h)", "c_spec": "Compressive specimen",
    "c_size": "Compressive specimen size (mm)", "t_spec": "Tensile specimen",
    "gauge": "Tensile gauge length (mm)", "t_type": "Tensile test type",
    "fc": "Compressive strength (MPa)", "ft": "Tensile strength (MPa)",
    "src": "Source table/page", "note": "Conversions / notes",
}

# ---------------------------------------------------------------- 1. Huang et al. 2021
P = dict(title="Flexural behaviour and evaluation of ultra-high-performance fibre reinforced concrete beams cured at room temperature",
         author="Huang J., He Z., Khan M.B.E., Zheng X., Luo Z.", year=2021,
         doi="https://doi.org/10.1038/s41598-021-98502-x")
# Table 2 (mass ratio to cement): cement 1.0, water 0.18, SSA 0.30, SSB 0.80, silica flour 0.30, SF 0.30, SP 0.02, steel 2 vol%
B = 1.0 + 0.30
base = dict(P, OPC=round(1.0 / B, 4), SF=round(0.30 / B, 4), WB=round(0.18 / B, 4), SS=round(1.10 / B, 4),
            maxsize=840, QP=round(0.30 / B, 4), SP=round(0.02 / B, 5),
            steel=2.0, steel_L=13, steel_d=200, steel_ft=2850, total=2.0, demold=1, age=28,
            c_spec="cube", c_size="100x100x100")
n0 = ("Table 2 mass ratios to cement (cement 1.0, water 0.18, silica sand 360-600 µm 0.30 + 600-840 µm 0.80, "
      "silica flour 50 µm 0.30 -> QP, silica fume 0.30, SP 0.02); B = cement+SF = 1.30, all /B. Dramix straight steel "
      "fibre 13 mm x 0.2 mm, 2850 MPa is the manufacturer 'yield strength'. ")
add(**base, cure="covered 24 h, demoulded, fog room 20±0.5 °C to 28 d", cure_t=28, cure_T=20,
    t_spec="dog-bone, 50x100 mm cross-section, 368 mm long", t_type="direct", fc=102.90, ft=8.38,
    src="Table 2 (mix), Table 3 (fc, ft)",
    note=n0 + "Mean of 3. ft = axial tension on dog-bone (0.05 mm/min, DIC). Same 20 °C batch: 100x100x300 prism fc 79.08 MPa, "
              "flexural strength (100x100x400) 17.7 MPa (Table 3).")
for T, fc in ((60, 119.92), (90, 156.46)):
    add(**base, cure=f"demoulded at 24 h, steam curing {T}±0.5 °C for 48 h, then fog room 20 °C to 28 d",
        cure_t=28, cure_T=T, heat_h=48, fc=fc, src="Table 2 (mix), Table 3 (fc)",
        note=n0 + "Mean of 3 cubes. Curing temperature column = steam temperature; tensile only tested for 20 °C.")

# ---------------------------------------------------------------- 2. Vicente et al. 2025
P = dict(title="Numerical and experimental study of the optimal specimen geometry for direct tension strength tests in high tensile strength fiber reinforced concrete",
         author="Vicente M.A., Mena-Alonso Á., González D.C., Ruiz G., Cifuentes H., Leiva C., Yu R., Mínguez J.", year=2025,
         doi="https://doi.org/10.1038/s41598-025-94471-7")
B = 540 + 310 + 210
cf_vol = round(15 / 1800 * 100, 2)
add(**P, OPC=round(540 / B, 4), GGBS=round(310 / B, 4), SF=round(210 / B, 4), WB=0.19, SS=round(940 / B, 4),
    maxsize=800, SP=round(42 / B, 4), binder=B, carbon=cf_vol, total=cf_vol,
    cure="demoulded at 24 h, submerged in water 28 d; tested at 56 d", cure_t=28, demold=1, age=56,
    t_spec="revolution bone-shaped (dog-bone) cylinder, 150 mm high, 54 mm max dia., 40 mm neck dia., resin-bonded ends",
    t_type="direct", ft=8.5, src="Table 3 (mix), Table 4 (ft), Sec. 'Materials'",
    note="Table 3 kg/m3: cement I 52.5R/SR 540, GGBS 310, SF 210, quartz sand <800 µm 470 + <315 µm 470, SP 42; "
         "w/b 0.19 (paper). B = 1060. Carbon fibre (Teijin) 6 mm, 7 µm, 4200 MPa, E 230 GPa, 15 kg/m3; fibre density "
         "NOT given -> vol% = 15/1800 assuming 1.80 g/cm3 (VERIFY). ft = mean of 6 specimens (Table 4: 9.2, 8.3, 7.8, 8.8, "
         "8.1, 8.5 MPa; paper reports 8.5 [0.5]). 0.5 mm/min. No compressive strength reported.")

# ---------------------------------------------------------------- 3. Zahran et al. 2026 (WHA / magnetized water UHPC)
P = dict(title="Sustainable UHPC incorporating water hyacinth ash and magnetized water with enhanced mechanical and durability performance",
         author="Zahran D., Yousry Elshikh M.M., Youssf O.", year=2026,
         doi="https://doi.org/10.1038/s41598-026-58832-0")
# Table 3 kg/m3: OPC, SF, RHA, WHA, QP, S, MP, GP, Water, SP, Steel
mixes = {"C": (880, 0, 0, 920, 0, 0), "RHA10": (792, 53.08, 0, 920, 0, 0), "RHA20": (704, 106.16, 0, 920, 0, 0),
         "WHA10": (792, 0, 67.05, 920, 0, 0), "GP10": (880, 0, 0, 828, 0, 86.73), "GP20": (880, 0, 0, 736, 0, 173.58),
         "MP10": (880, 0, 0, 828, 92, 0), "MP20": (880, 0, 0, 736, 184, 0)}
fcTW = {"C": (94.6, 118.4, 140.9, 153.0), "RHA10": (106.3, 131.8, 153.0, 162.6), "RHA20": (109.5, 135.0, 155.2, 164.7),
        "WHA10": (105.2, 132.2, 155.2, 162.6), "GP10": (117.3, 140.3, 156.2, 166.9), "GP20": (122.7, 143.5, 160.5, 169.0),
        "MP10": (102.0, 126.5, 148.8, 160.5), "MP20": (104.2, 128.6, 149.9, 162.6)}
fcMW = {"C": (112.2, 130.3, 152.0, 164.7), "RHA10": (126.9, 145.6, 164.7, 180.7), "RHA20": (130.7, 147.7, 165.8, 177.5),
        "WHA10": (128.6, 144.5, 165.8, 182.8), "GP10": (139.7, 155.2, 175.4, 187.1), "GP20": (143.5, 158.4, 174.3, 183.9),
        "MP10": (125.4, 142.4, 160.5, 174.3), "MP20": (122.2, 140.3, 159.4, 171.1)}
split = {"C": 13.8, "RHA10": 14.8, "RHA20": 14.6, "WHA10": 15.1, "GP10": 16.5, "GP20": 16.2, "MP10": 14.7, "MP20": 14.5}
for m, (opc, rha, wha, s, mp, gp) in mixes.items():
    B = opc + 170 + rha + wha
    for water, tab in (("TW", fcTW), ("MW", fcMW)):
        for age, fc in zip((7, 28, 56, 90), tab[m]):
            r = dict(P, OPC=round(opc / B, 4), SF=round(170 / B, 4), RHA=round(rha / B, 4) if rha else 0,
                     other=round(wha / B, 4) if wha else 0, WB=round(180 / B, 4), SS=round(s / B, 4), maxsize=2000,
                     QP=round(210 / B, 4), SP=round(30 / B, 4), binder=round(B, 2), steel=1.5, steel_L=13, steel_d=200,
                     total=1.5, cure="covered 24 h, demoulded, water immersion 20±2 °C until test", cure_t=age, cure_T=20,
                     demold=1, age=age, c_spec="cube", c_size="50x50x50", fc=fc,
                     src="Table 3 (mix), Table 4 (fc)")
            note = (f"Mix {m}, {'tap water' if water == 'TW' else 'magnetized water (MW)'}. Table 3 kg/m3 / B (OPC+SF+RHA+WHA = {B:.2f}). "
                    "WHA (water hyacinth ash) in 'Other binder'. Quartz powder 210, SP 30, water 180 kg/m3. "
                    f"Sand replaced by volume with glass powder {gp} kg/m3 (GP/B={gp / B:.4f}) and marble powder {mp} kg/m3 "
                    f"(MP/B={mp / B:.4f}) - treated as sand replacements by the paper, not binder (no template column). "
                    "Hooked-end steel 117 kg/m3 / 7800 (paper SG 7.80) = 1.5 vol%.")
            if age == 28 and water == "TW":
                r.update(t_spec="cylinder 100x200", t_type="splitting", ft=split[m])
                note += (" Splitting ft from text (Fig. 16 discussion); text does not say TW or MW - assumed TW group "
                         "(VERIFY).")
                r["src"] = "Table 3 (mix), Table 4 (fc), text Sec. splitting tensile (ft)"
            r["note"] = note
            add(**r)

# ---------------------------------------------------------------- 4. Murali et al. 2026 (natural fibres + BLA)
P = dict(title="Valorization of slag and banana leaf ash in five natural fiber-reinforced sustainable cementitious composites: early age mechanical and microstructural insights",
         author="Murali G., Thapa S., Wong L.S., Kurpińska M., Korol E., Abdelgader H.S., Ramkumar V.R., Avudaiappan S.", year=2026,
         doi="https://doi.org/10.1038/s41598-026-64977-9")
fib = {"RS": ("none", 0, None), "BF": ("banana", 0.5, "1.0 mm dia., 700 MPa"), "KF": ("kenaf", 0.5, "0.25 mm, 800 MPa"),
       "PF": ("pineapple", 0.5, "0.35 mm, 1000 MPa"), "SF": ("sisal", 0.5, "0.35 mm, 600 MPa"),
       "JF": ("jute", 0.5, "0.2 mm, 500 MPa")}
fc4 = {"A-RS": (39.84, 50.89), "A-BF": (43.91, 54.12), "A-KF": (52.09, 65.43), "A-PF": (53.84, 68.61),
       "A-SF": (49.81, 60.85), "A-JF": (44.09, 55.75), "B-RS": (41.35, 51.56), "B-BF": (44.87, 56.71),
       "B-KF": (52.04, 68.27), "B-PF": (56.39, 71.04), "B-SF": (49.32, 62.11), "B-JF": (47.79, 58.31)}
for m, (f14, f28) in fc4.items():
    ser, code = m.split("-")
    cem, bla = (1000, 0) if ser == "A" else (950, 50)
    B = cem + 250 + bla
    name, vf, prop = fib[code]
    for age, fc in ((14, f14), (28, f28)):
        add(**P, OPC=round(cem / B, 4), GGBS=round(250 / B, 4), other=round(bla / B, 4), WB=round(525 / B, 4),
            msand=round(3000 / B, 4), total=vf, age=age, c_spec="cube", c_size="50x50x50", fc=fc,
            src="Table 3 (mix), Table 4 (fc)",
            note=(f"Mix {m}: batch g cement {cem}, GGBS 250, banana leaf ash (BLA, 'Other binder') {bla}, M-sand 3000, "
                  f"water 525 ml, SP 20 ml (SP density not given -> SP/B left empty); all /B={B} g. Natural fibre: {name}"
                  + (f", 20 mm, {prop} (Table 2), 0.5 vol% of composite (no template column)" if vf else "")
                  + ". Curing regime not described in text. Mean of 3 cubes."))

# ---------------------------------------------------------------- 5. Ozturk 2026 (basalt fibre, red mud mortar)
P = dict(title="Mechanical performance of basalt fiber reinforced cementitious mortars incorporating calcined red mud",
         author="Ozturk M.", year=2026, doi="https://doi.org/10.1038/s41598-026-63669-8")
fc5 = {("-", 0): {0: 47.45, 0.15: 52.41, 0.30: 53.35},
       ("RM-23", 10): {0: 44.11, 0.15: 45.73, 0.30: 46.94}, ("RM-23", 20): {0: 36.20, 0.15: 36.82, 0.30: 37.16},
       ("RM-600", 10): {0: 39.64, 0.15: 40.16, 0.30: 41.58}, ("RM-600", 20): {0: 34.15, 0.15: 35.48, 0.30: 36.36},
       ("RM-800", 10): {0: 33.46, 0.15: 34.72, 0.30: 35.13}, ("RM-800", 20): {0: 28.76, 0.30: 32.05}}
for (rm, pct), d in fc5.items():
    for bf, fc in d.items():
        add(**P, OPC=round(1 - pct / 100, 2), other=round(pct / 100, 2), WB=0.485, msand=2.75, maxsize=4000,
            basalt=bf, total=bf, cure="demoulded at 24 h, water curing at ambient temperature to 28 d", cure_t=28,
            demold=1, age=28, c_spec="cube", c_size="50x50x50", fc=fc,
            src="Table 1 (mix), Sec. 'Compressive strength' text (fc)",
            note=(f"Red mud {rm} ({'untreated' if rm == 'RM-23' else 'calcined ' + rm[3:] + ' °C' if rm != '-' else 'none'}) "
                  f"{pct}% of binder in 'Other binder'. Binder:calcareous crushed aggregate (max 4 mm, M-sand column):water = "
                  "1:2.75:0.485 by mass. Basalt fibre 10 mm, 9-23 µm, 4.84 GPa, E 89 GPa. fc = mean of 6 cubes, values from text "
                  "(Fig. 3). 800 °C-20R-0.15B not given in text (omitted)."))

# ---------------------------------------------------------------- 6. Wang et al. 2025 (PET fibre mortar)
P = dict(title="Experimental design and analysis of toughness and modulus of rupture (MOR) of cement mortar reinforced with PET fibers",
         author="Wang X., Liu T., Yue J., Teimortashlu A., Jalal M., Xu W.", year=2025,
         doi="https://doi.org/10.1038/s41598-025-21250-9")
t6 = [("D0", 0.45, 19, 0, 47.6, 6.88), ("D1", 0.35, 16, 0.5, 45.02, 7.67), ("D2", 0.40, 19, 0.5, 38.93, 7.44),
      ("D3", 0.45, 22, 0.5, 26.74, 5.81), ("D4", 0.35, 19, 1, 47.17, 7.67), ("D5", 0.40, 22, 1, 25.22, 5.74),
      ("D6", 0.45, 16, 1, 25.50, 5.74)]
for m, wb, sp, vf, fc, mor in t6:
    add(**P, OPC=0.9, other=0.1, WB=wb, binder=700, PET=vf, total=vf,
        cure="covered with plastic, curing room 20 °C / 95% RH, demoulded after 28 d", cure_t=28, cure_T=20, RH=95,
        demold=28, age=28, c_spec="cube", c_size="50x50x50", t_spec="prism 25x25x285 (ASTM C78)", t_type="flexural",
        fc=fc, ft=mor, src="Tables 3-4 (mix), Table 5 (fc), Table 6 (MOR)",
        note=(f"Design {m}. Binder 700 kg/m3 = cement with 10 wt% 'lime powder' replacement (type not specified -> Other binder). "
              f"SP level '{sp}' (unitless in Table 3; Table 4 gives SP g per batch of unknown size) -> SP/B left empty. "
              "Sand content NOT reported (SSD fine aggregate, SG 2.65). PET fibre 6 mm, density 1.26, 526 MPa. "
              "MOR = modulus of rupture." + (" D5 fc single value (no SD)." if m == "D5" else "")))

# ---------------------------------------------------------------- 7. Culgatay & Ozturk 2026 (PAN fibre mortar)
P = dict(title="Role of polyacrylonitrile fiber diameter and aspect ratio on mechanical performance and pore structure of cementitious mortars",
         author="Culgatay V.G., Ozturk M.", year=2026, doi="https://doi.org/10.1038/s41598-026-56745-6")
pan = [("REF", None, 0, 54.01, 8.30, ""),
       ("PAN-6-15-0.2", 15, 0.2, 54.51, 8.64, ""), ("PAN-6-15-0.4", 15, 0.4, 59.87, 8.82, ""),
       ("PAN-6-15-0.6", 15, 0.6, 71.67, 8.94, ""),
       ("PAN-6-35-0.2", 35, 0.2, None, 7.81, " fc not reported in text."),
       ("PAN-6-35-0.4", 35, 0.4, 53.55, 8.39, ""), ("PAN-6-35-0.6", 35, 0.6, 53.48, 8.72, ""),
       ("PAN-6-40-0.2", 40, 0.2, round(54.01 * 1.037, 2), 7.32, " VERIFY fc derived: text '+3.7%' vs REF 54.01."),
       ("PAN-6-40-0.4", 40, 0.4, round(54.01 * 1.041, 2), 7.34, " VERIFY fc derived: text '+4.1%' vs REF 54.01."),
       ("PAN-6-40-0.6", 40, 0.6, 62.36, 7.79, "")]
for m, dia, vf, fc, fl, extra in pan:
    add(**P, OPC=1.0, WB=0.485, msand=2.75, maxsize=4000, total=vf,
        cure="demoulded at 24 h, water tank at ambient temperature to 28 d", cure_t=28, demold=1, age=28,
        c_spec="cube", c_size="50x50x50", t_spec="prism 40x40x160 (3-point, ASTM C348)", t_type="flexural",
        fc=fc, ft=fl, src="Table 1 (fibre), Table 2 (mix), text Secs. flexural & compressive (Figs. 3-4)",
        note=(f"Mix {m}. Cement CEM I 42.5R : calcareous crushed aggregate (max 4 mm, M-sand column) : water = 1:2.75:0.485. "
              + (f"Polyacrylonitrile (PAN) fibre 6 mm, ~{dia} µm, density 1.17-1.18, {vf} vol% (no template column). "
                 if dia else "No fibre. ") + "Values from text." + extra))

# ---------------------------------------------------------------- 8. Ozturk & Arpaci 2026 (steel + carbon fibre mortar)
P = dict(title="Hybrid steel and carbon fiber reinforcement enhances mechanical performance and sustainability of cementitious composites",
         author="Ozturk M., Arpaci S.S.", year=2026, doi="https://doi.org/10.1038/s41598-026-60833-y")
h = [("0SF-0CF", 0, 0, 64, 5.6), ("0.50SF-0CF", 0.5, 0, 69, 7.1), ("0.75SF-0CF", 0.75, 0, 70, 8.1),
     ("1.00SF-0CF", 1.0, 0, 70, 8.6), ("0SF-0.10CF", 0, 0.10, 60, 7.5), ("0SF-0.20CF", 0, 0.20, 62, 8.0),
     ("0SF-0.30CF", 0, 0.30, 58, 8.4), ("0.37SF-0.10CF", 0.375, 0.10, None, 9.1)]
for m, sf, cf, fc, fl in h:
    add(**P, OPC=1.0, WB=round(263 / 542, 4), msand=round(1490 / 542, 4), maxsize=4000, binder=542,
        steel=sf, steel_L=10 if sf else None, steel_d=100 if sf else None, steel_ft=2500 if sf else None,
        carbon=cf, total=round(sf + cf, 3), cure="demoulded at 24 h, water curing at ambient temperature to 28 d",
        cure_t=28, demold=1, age=28, c_spec="cube", c_size="50x50x50", t_spec="prism 40x40x160 (3-point, ASTM C348)",
        t_type="flexural", fc=fc, ft=fl, src="Table 1 (mix), text Secs. flexural & compressive (Figs. 1-2)",
        note=(f"Mix {m}. Table 1 kg/m3: cement CEM I 42.5R 542, calcareous crushed aggregate (max 4 mm) 1490, water 263; "
              "/cement. Steel fibre Dramix 10 mm x 0.1 mm, ~2500 MPa; carbon fibre 10 mm, 7 µm, ~4200 MPa (vol% from paper). "
              + ("VERIFY: fc given in text only as 'approximately' (read from Fig. 2). " if fc else
                 "Hybrid: fc only as range 57-61 MPa in text -> left empty. ")
              + "Flexural values from text."))

# ---------------------------------------------------------------- 9. Sunantha et al. 2026 (banana/kenaf fibre bacterial mortar)
P = dict(title="Optimization of natural fibre length in bacterial cement mortar using TOPSIS for enhanced mechanical properties",
         author="Sunantha B., Nagarajan P., Sudhakumar J., Thomas B.S., Das S., Svajlenka J., Berhe M.A.", year=2026,
         doi="https://doi.org/10.1038/s41598-026-48095-0")
t2 = {0.5: (38.23, 42.25, 43.97, 46.35, 4.71, 5.65, 4.84, 5.87, 3.52, 4.22, 3.73, 4.38),
      1.0: (39.72, 43.68, 44.85, 48.21, 4.97, 5.83, 5.07, 5.96, 3.55, 4.28, 3.79, 4.47),
      1.5: (41.64, 44.66, 45.76, 50.09, 5.02, 5.89, 5.26, 6.05, 3.62, 4.35, 3.86, 4.56),
      2.0: (42.67, 45.28, 46.23, 52.16, 5.22, 5.97, 5.42, 6.26, 3.68, 4.42, 3.92, 4.62),
      2.5: (43.83, 47.54, 47.21, 55.89, 5.4, 6.3, 5.67, 6.43, 3.79, 4.61, 4.1, 4.92),
      3.0: (41.12, 44.77, 45.67, 50.79, 5.32, 5.94, 5.53, 6.32, 3.6, 4.33, 3.94, 4.61),
      3.5: (39.51, 43.03, 44.43, 48.67, 5.28, 5.72, 5.42, 6.28, 3.61, 4.21, 3.83, 4.51)}
vol_c = 1 / 2.76 + 3 / 2.60 + 0.45  # litres per kg cement (cement SG 2.76, M-sand SG 2.60, w/c 0.45)
for L, v in t2.items():
    for fi, (fname, dens) in enumerate((("banana", 1.45), ("kenaf", 1.6))):
        fvol = 0.02 / dens
        vf = round(fvol / (vol_c + fvol) * 100, 2)
        for bi, bact in enumerate(("without bacteria", "with bacteria")):
            fc = v[fi * 2 + bi]
            fl = v[4 + fi * 2 + bi]
            st = v[8 + fi * 2 + bi]
            base9 = dict(P, OPC=1.0, WB=0.45, msand=3.0, total=vf,
                         cure="demoulded at 24 h, water curing (3, 7, 28 d tested)", demold=1, c_spec="cube",
                         c_size="50x50x50", fc=fc, src="Table 1 (fibre), Table 2 (results), Sec. 'Mortar mix preparation'")
            nt = (f"{fname} fibre {L} cm long, 2% by mass of cement, {bact}"
                  + (" (Bacillus cereus + Vibrio natriegens consortium 3%, calcium acetate nutrient)" if bi else "")
                  + f". Binder = Portland pozzolana cement (PPC, SG 2.76) in OPC column. cement:M-sand = 1:3, w/c 0.45. "
                  f"VERIFY fibre vol% derived: 0.02/{dens} (paper density) over absolute volume of cement+sand+water+fibre "
                  "(air ignored). Test age of Table 2 not stated (specimens tested at 3, 7, 28 d; values likely 28 d) -> "
                  "left empty. Natural fibre (no template column). ")
            add(**base9, t_spec="prism 40x40x160 (3-point, ASTM C348)", t_type="flexural", ft=fl,
                note=nt + f"Splitting tensile strength (100x200 cylinder, ASTM C496) = {st} MPa (Table 2).")

df = pd.DataFrame(rows).reindex(columns=COLS)

# ---------------------------------------------------------------- checks / dedupe
ex = open(os.path.join(D, "existing_papers.txt"), encoding="utf-8").read().lower()
others = ""
for f in glob.glob(os.path.join(D, "w*_*.csv")):
    if os.path.basename(f) != NAME + ".csv":
        others += open(f, encoding="utf-8-sig", errors="ignore").read().lower()
for doi in df["DOI / URL"].unique():
    key = doi.replace("https://doi.org/", "").lower()
    if key in ex or key in others:
        print("DROP duplicate", doi)
        df = df[df["DOI / URL"] != doi]

bcols = COLS[4:22]
s = df[bcols].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1)
assert ((s - 1).abs() < 0.01).all(), df.loc[(s - 1).abs() >= 0.01, ["DOI / URL"]]
assert df["W / B"].between(0.1, 0.7).all()
fc = df["Compressive strength (MPa)"].dropna(); assert fc.between(2, 250).all()
assert df["Total fiber (vol%)"].notna().all() and df["Total fiber (vol%)"].between(0, 6).all()
dt = df.loc[df["Tensile test type"] == "direct", "Tensile strength (MPa)"]; assert dt.between(0.5, 25).all()

df.to_csv(os.path.join(D, NAME + ".csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers")
print(df.groupby("DOI / URL").size())
