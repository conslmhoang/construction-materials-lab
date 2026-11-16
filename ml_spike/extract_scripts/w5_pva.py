"""Wave 5, agent 'pva': PVA-fiber ECC / SHCC with cement + fly ash (+ slag / silica fume / limestone ...).
Writes ml_spike/additions_v2/w5_pva.csv (99-column TEMPLATE header) and w5_pva_rejected.txt.
Every value is from the paper text/tables; derived values are flagged with VERIFY in the notes.
Binder B = the paper's binder (cement + FA [+ SF ...]); all "X / B" ratios are per that B.
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []


def paper(title, authors, year, doi):
    return {"Article Name": title, "Author": authors, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------------------------------------------------------------------------------------------
# 1) Thangavel et al. (2026) Sci Rep 16, 33871 - hybrid ECC; only the mono-PVA mix "ECC" qualifies
#    (HECC1 has PP, HECC2 has glass fiber). Table 2 (fiber), Table 3 (mix, kg/m3), Table 5 (fc), Table 6 (tension)
P = paper("Experimental investigation of fiber hybridized ECC using PVA, polypropylene, and high-modulus glass fibers with class F Fly ash and OPC",
          "Pradeep Thangavel, Warit Wipulanusat, Ammapalyam Ramasamy Krishnaraja, Shankar Karuppannan, Yuvaraj Kandasamy",
          2026, "10.1038/s41598-026-73191-6")
B = 570 + 810
base = dict(P, **{"OPC / Cement": round(570 / B, 4), "FA (Fly ash)": round(810 / B, 4), "W / B": round(483 / B, 4),
                  "SS / B (Silica sand)": round(980 / B, 4), "SP / B": 0.01, "Binder content (kg/m³)": B,
                  "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
                  "PVA elastic modulus (GPa)": 42.5, "Total fiber (vol%)": 2.0,
                  "Curing method": "demoulded after 24 h, water curing (temperature not stated)", "Demolding age (days)": 1,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7"})
for age, fc in [(3, 9.4), (7, 22.5), (14, 35.8), (28, 51.0)]:
    r = dict(base)
    r.update({"Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (fiber), Table 3 (mix), Table 5 (fc)" + (", Table 6 (tension), text (fcr)" if age == 28 else ""),
              "Conversions / notes": "Mix ECC (2.0% PVA). Class F FA, OPC 53, silica sand; kg/m3 / binder (C+FA=1380). "
                                     "HRWR (PCE) 1.0% of binder."})
    if age == 28:
        r.update({"Tensile specimen": "dog-bone coupon (30x30 mm gauge section)", "Tensile gauge length (mm)": 80,
                  "Tensile test type": "direct (uniaxial)", "Tensile strength (MPa)": 5.53,
                  "First-cracking strength (MPa)": 4.05, "Tensile strain capacity (%)": 1.89})
    rows.append(r)

# ---------------------------------------------------------------------------------------------
# 2) Keskin, Tas, Kasap Keskin (2020) Mugla J. Sci. Technol. - HVFA ECC; ratios by cement mass (Table 3).
#    Only the two control mixes with commercial quartz sand (0-200 um) are used; the 'W' mixes use
#    0-70 um quartz quarry waste (= quartz flour, not allowed). Compression only (no direct tension).
P = paper("Utilization of Muğla fly ash and quartz dust in engineered cementitious composites production at high volumes",
          "Süleyman Bahadır Keskin, Olkan İlter Taş, Özlem Kasap Keskin", 2020, "10.22531/muglajsci.673036")
for mid, fa, w, ss, sp, fcs in [("1.2", 1.2, 0.6, 0.79, 0.014, (39.3, 63.3, 75.2)),
                                ("2.2", 2.2, 0.864, 1.152, 0.020, (30.9, 51.7, 70.3))]:
    Bm = 1 + fa
    for age, fc in zip((7, 28, 90), fcs):
        r = dict(P)
        r.update({"OPC / Cement": round(1 / Bm, 4), "FA (Fly ash)": round(fa / Bm, 4), "W / B": round(w / Bm, 4),
                  "SS / B (Silica sand)": round(ss / Bm, 4), "Sand max size (µm)": 200, "SP / B": round(sp / Bm, 5),
                  "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
                  "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2.0,
                  "Curing method": "covered with plastic 1 d, then sealed in plastic bags with wet fabric at 23 °C",
                  "Curing time (days)": age, "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": age,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 2 (fiber), Table 3 (mix), Table 4 (fc), p.66 (curing)",
                  "Conversions / notes": f"Mix {mid} (FA/C = {fa}). Ratios by cement mass re-expressed per B = C + FA. "
                                         "CEM I 42.5R, class F FA, commercial quartz sand 0-200 um (silica sand), PCE HRWR."})
        rows.append(r)

# ---------------------------------------------------------------------------------------------
# 3) Arivusudar & Suresh Babu (2020) Cement Wapno Beton 25(4) - ECC + silica fume additions.
#    Table 3: cement 1, SF x, FA 0.3, river sand 0.8 (by weight), W/B 0.35, SP 1 %, PVA 2 vol%.
#    fc and direct tensile strength (28 d) only in the text (p. 285-286).
P = paper("Mechanical properties of engineered cementitious composites developed with silica fume",
          "N. Arivusudar, S. Suresh Babu", 2020, "10.32047/cwb.2020.25.4.3")
fcs = [51.2, 52.9, 54.6, 54.5, 55.2, 53.8, 53.6, 53.9]
fts = [5.46, 6.95, 6.86, 7.21, 7.96, 8.15, 6.98, 6.86]
for i, (fc, ft) in enumerate(zip(fcs, fts)):
    sf = i / 10
    Bm = 1 + sf + 0.3
    r = dict(P)
    r.update({"OPC / Cement": round(1 / Bm, 4), "FA (Fly ash)": round(0.3 / Bm, 4), "SF (Silica fume)": round(sf / Bm, 4),
              "W / B": 0.35, "River sand / B": round(0.8 / Bm, 4), "SP / B": 0.01,
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 38, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 42.5, "Total fiber (vol%)": 2.0,
              "Curing method": "in moulds 24 h, then water curing", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
              "Tensile specimen": "dog-bone 350x60x30 mm (30x30 mm gauge section)", "Tensile gauge length (mm)": 80,
              "Tensile test type": "direct (uniaxial)", "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "Source table/page": "Table 2 (fiber), Table 3 (mix), text p.285-286 (fc, ft)",
              "Conversions / notes": f"Mix {'ECC' if i == 0 else 'ECC-SF%d' % i}. Table 3 proportions by weight relative to cement = 1 "
                                     "(SF added on top); B = cement + SF + FA as the paper's W/B. OPC 53, class F FA, river sand zone III. "
                                     "VERIFY: SP 1 % assumed per binder (base not stated); sand ratio assumed per cement mass."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------
# 4) Li & Li (2013) Mater. Struct. 46:405-420 - M45-type ECC with 7 VMA dosages.
#    Table 2: C 1, silica sand 0.8, FA 1.2, W 0.66, SP "0.013 %", PVA 2 %, VMA x % of cement weight.
#    Table 3: tensile strain capacity of the 5 specimens per mix (mean taken here).
P = paper("Rheology, fiber dispersion, and robust properties of Engineered Cementitious Composites",
          "Mo Li, Victor C. Li", 2013, "10.1617/s11527-012-9909-z")
t3 = {0: [0.44, 0.06, 0.13, 0.09, 0.03], 0.01: [0.34, 0.32, 1.19, 0.69, 0.52], 0.015: [1.97, 0.76, 0.85, 0.75, 1.38],
      0.02: [3.5, 3.1, 2.87, 3.2, 3.0], 0.025: [3.35, 3.27, 2.94, 3.01, 2.68], 0.03: [3.25, 3.18, 2.82, 3.12, 2.71],
      0.04: [3.33, 3.27, 3.30, 2.83, 3.23]}
for vma, eps in t3.items():
    r = dict(P)
    r.update({"OPC / Cement": round(1 / 2.2, 4), "FA (Fly ash)": round(1.2 / 2.2, 4), "W / B": 0.3,
              "SS / B (Silica sand)": round(0.8 / 2.2, 4), "Sand max size (µm)": 250, "SP / B": round(0.013 / 2.2, 5),
              "VMA / B": round(vma / 100 / 2.2, 7),
              "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620,
              "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
              "Curing method": "covered 24 h, moist cured in plastic bags 95 % RH 20 °C to 7 d, then air 50 % RH 20 °C to 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "plate 228.6x76.2x12.7 mm", "Tensile gauge length (mm)": 101.6,
              "Tensile test type": "direct (uniaxial)", "Tensile strain capacity (%)": round(sum(eps) / len(eps), 2),
              "Source table/page": "Table 1 (fiber), Table 2 (mix), Table 3 (strain), Sect. 4.2 (curing)",
              "Conversions / notes": f"Mix ECC_{vma}% VMA (of cement weight; VMA/B = x/100/2.2). Type I OPC, class F FA, F-110 silica sand. "
                                     f"VERIFY: strain = mean of the 5 specimen values in Table 3 {eps}; SP given as '0.013 %' in Table 2, "
                                     "taken as 0.013 by cement mass (M45 practice) -> /2.2."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------
# 5) Kasap Keskin, Keskin, Tekin (2023) JACT 21:735-747 - ECC with FA or slag (SCM/C 1.2 and 2.2), maturity method.
#    Table 2 (mix kg/m3), Table 3 (50 mm cubes at 10/20/40 °C, 1-90 d), Table 8 (cylinders 28 d, 1 yr NC, AC 60 °C).
P = paper("Predicting the Ultimate Properties of Engineered Cementitious Composites by Maturity Method",
          "Özlem Kasap Keskin, Süleyman Bahadır Keskin, K. Tekin", 2023, "10.3151/jact.21.735")
mixes5 = {"F 1.2": (560, 672, 0, 333, 442, 3), "F 2.2": (377, 830, 0, 326, 435, 5),
          "S 1.2": (592, 0, 711, 352, 469, 5), "S 2.2": (405, 0, 890, 350, 466, 4)}
ages5 = [1, 3, 5, 7, 14, 28, 56, 90]
t35 = {"F 1.2": {10: [2.8, 12.8, None, 25.9, 36.8, 42.0, 48.6, 54.2], 20: [6.1, 24.2, None, 35.7, 41.1, 48.0, 53.2, 63.5],
                 40: [20.1, 35.4, None, 41.1, 50.0, 54.8, 56.0, 58.0]},
       "F 2.2": {10: [None, 4.8, 8.6, 16.4, 23.9, 30.7, 33.7, 42.0], 20: [None, 7.8, 18.1, 22.8, 31.7, 36.4, 40.9, 54.5],
                 40: [None, 14.6, 24.2, 28.6, 33.2, 36.8, 40.0, 40.6]},
       "S 1.2": {10: [3.9, 17.7, None, 30.0, 42.5, 58.4, 61.7, 72.8], 20: [9.9, 28.1, None, 49.5, 65.4, 73.8, 75.2, 80.8],
                 40: [29.7, 52.8, None, 65.2, 73.8, 77.8, 80.5, 81.3]},
       "S 2.2": {10: [1.4, 6.7, None, 14.9, 20.4, 34.7, 46.6, 52.3], 20: [5.3, 15.6, None, 24.4, 45.8, 62.1, 64.6, 66.3],
                 40: [14.7, 39.1, None, 43.1, 49.1, 57.8, 63.3, 67.6]}}
t85 = {"F 1.2": (52.2, 66.8, 60.3), "F 2.2": (38.0, 51.6, 49.3), "S 1.2": (71.4, 84.0, 74.2), "S 2.2": (59.5, 77.4, 68.6)}
ac_days = {"F 1.2": 81.6, "F 2.2": 48.3, "S 1.2": 51.0, "S 2.2": 31.2}
for mid, (c, fa, sl, w, s, sp) in mixes5.items():
    Bm = c + fa + sl
    base5 = dict(P, **{"OPC / Cement": round(c / Bm, 4), "FA (Fly ash)": round(fa / Bm, 4) if fa else 0,
                       "GGBS": round(sl / Bm, 4) if sl else 0, "W / B": round(w / Bm, 4), "SS / B (Silica sand)": round(s / Bm, 4),
                       "SP / B": round(sp / Bm, 5), "Binder content (kg/m³)": Bm,
                       "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620,
                       "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0})
    note = (f"Mix {mid}. kg/m3 / binder (C + FA or slag = {Bm}). CEM I 42.5R, fine quartz sand, PCE SP (40 % solids, as dosed). "
            "Paper states w/b 0.27, s/b 0.36.")
    for T, vals in t35[mid].items():
        for age, fc in zip(ages5, vals):
            if fc is None:
                continue
            r = dict(base5)
            r.update({"Curing method": f"maturity series: 50 mm cubes cured at constant {T} °C (moisture condition not stated)",
                      "Curing time (days)": age, "Curing temperature (°C)": T, "Test age (days)": age,
                      "Heat curing duration (h)": age * 24 if T == 40 else None,
                      "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
                      "Source table/page": "Table 2 (mix), Table 3 (fc), Sect. 2.1 (fiber)", "Conversions / notes": note})
            rows.append(r)
    for (cond, age, T, meth), fc in zip([("28 days", 28, 23, "standard curing at 23 °C, 28 d"),
                                         ("NC", 365, 23, "normal curing at 23 °C for 1 year"),
                                         ("AC", ac_days[mid], 60, f"accelerated curing at 60 °C, 95 % RH for {ac_days[mid]} d (equivalent to 1 yr at 23 °C)")],
                                        t85[mid]):
        r = dict(base5)
        r.update({"Curing method": meth, "Curing time (days)": age, "Curing temperature (°C)": T,
                  "Curing RH (%)": 95 if cond == "AC" else None, "Test age (days)": age,
                  "Heat curing duration (h)": round(age * 24, 1) if cond == "AC" else None,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 2 (mix), Table 8 (fc), Sect. 3.3-3.4 (curing)",
                  "Conversions / notes": note + f" Table 8 condition '{cond}'."})
        rows.append(r)

# ---------------------------------------------------------------------------------------------
# 6) Chen, Yang, Yang, Yao (2014) JACT 12:510-519 - latex (EVA) modified ECC; only the control L-ECC0 (no EVA) qualifies.
#    Table 1 (mix kg/m3), Table 3 (fiber), Table 5 (direct tension); fc only plotted (Fig. 2) -> not given.
P = paper("Latex-modified Engineered Cementitious Composites (L-ECC)", "Zhitao Chen, En-Hua Yang, Yingzhi Yang, Yan Yao",
          2014, "10.3151/jact.12.510")
r = dict(P)
r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.25, "SS / B (Silica sand)": round(446 / 1272, 4),
          "SP / B": round(8.0 / 1272, 5), "Binder content (kg/m³)": 1272,
          "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
          "PVA elastic modulus (GPa)": 42, "Total fiber (vol%)": 2.0,
          "Curing method": "demoulded at 24 h, standard room 20 °C, 95 % RH", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
          "Tensile specimen": "coupon 150x45x20 mm", "Tensile gauge length (mm)": 100, "Tensile test type": "direct (uniaxial)",
          "Tensile strength (MPa)": 5.27, "First-cracking strength (MPa)": 4.18, "Tensile strain capacity (%)": 1.15,
          "Source table/page": "Table 1 (mix), Table 3 (fiber), Table 5 (tension), Sect. 2.2 (curing)",
          "Conversions / notes": "Mix L-ECC0 (no EVA). kg/m3 / binder (C 636 + FA 636). Silica sand. Fiber 26 kg/m3 = 2 vol%. "
                                 "fc only in Fig. 2 (not extracted)."})
rows.append(r)

# ---------------------------------------------------------------------------------------------
# 7) Özbay et al. (2013) JACT 11:167-179 - ECC with FA/C 1.2 and 2.2; Table 1 (mix), Table 3 (fc of uncracked specimens, 28 d).
P = paper("Effect of Sustained Flexural Loading on Self-Healing of Engineered Cementitious Composites",
          "Erdoğan Özbay, Mustafa Şahmaran, Hasan Erhan Yücel, Tahir Kemal Erdem, Mohamed Lachemi, Victor C. Li",
          2013, "10.3151/jact.11.167")
for mid, c, fa, w, s, sp, fc in [("ECC-1", 558, 669, 326, 446, 5.1, 69.3), ("ECC-2", 375, 823, 318, 435, 3.0, 46.1)]:
    Bm = c + fa
    r = dict(P)
    r.update({"OPC / Cement": round(c / Bm, 4), "FA (Fly ash)": round(fa / Bm, 4), "W / B": round(w / Bm, 4),
              "SS / B (Silica sand)": round(s / Bm, 4), "Sand max size (µm)": 400, "SP / B": round(sp / Bm, 5),
              "Binder content (kg/m³)": Bm, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39,
              "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded at 24 h, moist cured in plastic bags 95 % RH 23 °C to 7 d, then air 50 % RH 23 °C to 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix), Table 3 (fc), p.169 (fiber, curing)",
              "Conversions / notes": f"Mix {mid} (uncracked reference). kg/m3 / binder (C+FA). CEM I 42.5, class F FA, silica sand "
                                     "(max 400 um), HRWR; fiber 26 kg/m3 = 2 vol%."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------
# 8) Zhou, Wang, Lai, Ho (2023) JACT 21:748-761 - high-strength ECC, PVA and PVA+steel hybrids.
#    Only the unheated (30 °C) results of Table 5 are used. Table 2 (fibers), Table 3 (mix kg/m3).
P = paper("Steel Fiber to Improve Thermal Resistance of High Strength PVA-ECC after Exposure to Elevated Temperature",
          "Y. Zhou, Q. Wang, M. Lai, J. C. M. Ho", 2023, "10.3151/jact.21.748")
for mid, pva, st, fc in [("PO", 2.0, 0.0, 83.1), ("PS-I", 1.5, 0.5, 75.1), ("PS-II", 1.0, 1.0, 93.8)]:
    r = dict(P)
    r.update({"OPC / Cement": round(520 / 1144, 4), "FA (Fly ash)": round(624 / 1144, 4), "W / B": round(229 / 1144, 4),
              "SS / B (Silica sand)": round(915 / 1144, 4), "SP / B": round(10.296 / 1144, 5), "Binder content (kg/m³)": 1144,
              "PVA fiber (vol%)": pva, "PVA length (mm)": 12, "PVA diameter (µm)": 15, "PVA tensile strength (MPa)": 1780,
              "PVA elastic modulus (GPa)": 39, "Steel fiber (vol%)": st if st else None,
              "Steel length (mm)": 13 if st else None, "Steel diameter (µm)": 220 if st else None,
              "Steel tensile strength (MPa)": 2800 if st else None, "Steel elastic modulus (GPa)": 200 if st else None,
              "Total fiber (vol%)": 2.0,
              "Curing method": "wrapped in PE film 1 d, then standard curing chamber 20 °C, >95 % RH",
              "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (fibers), Table 3 (mix), Table 5 (fc, unheated 30 °C column)",
              "Conversions / notes": f"Mix {mid}, unheated reference only (heated specimens excluded). kg/m3 / binder (C 520 + FA 624). "
                                     "Quartz sand as aggregate (s/b 0.80); copper-coated steel fiber."})
    rows.append(r)

# ---------------------------------------------------------------------------------------------
# 9) Li, Li, Wang, Zhang, Alselwi (2022) Buildings 12, 1934 - HDCC with PVA partly replaced by steel fiber.
#    Table 2 (fibers), Table 3 (mix kg/m3), Table 4 (tension, 14 d); fc of S1-S4 in text p.7, JZ derived.
P = paper("Effects of Hybrid PVA–Steel Fibers on the Mechanical Performance of High-Ductility Cementitious Composites",
          "L. Li, B. Li, Z. Wang, Z. Zhang, O. Alselwi", 2022, "10.3390/buildings12111934")
for mid, pva, st, fcr, ft, eps, fc in [("JZ", 2.0, 0.0, 1.85, 3.35, 1.37, 24.1), ("S1", 1.5, 0.5, 2.32, 3.36, 0.88, 31.3),
                                       ("S2", 1.0, 1.0, 2.05, 3.38, 0.62, 24.4), ("S3", 0.5, 1.5, 1.55, 3.56, 1.13, 20.8),
                                       ("S4", 0.0, 2.0, 1.55, 3.42, 1.23, 20.6)]:
    r = dict(P)
    r.update({"OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "W / B": 0.3, "River sand / B": 0.5, "Sand max size (µm)": 1180,
              "SP / B": 0.005, "Binder content (kg/m³)": 1100,
              "PVA fiber (vol%)": pva if pva else None, "PVA length (mm)": 12 if pva else None, "PVA diameter (µm)": 39 if pva else None,
              "PVA tensile strength (MPa)": 1550 if pva else None, "PVA elastic modulus (GPa)": 39.5 if pva else None,
              "Steel fiber (vol%)": st if st else None, "Steel length (mm)": 13 if st else None,
              "Steel diameter (µm)": 220 if st else None, "Steel tensile strength (MPa)": 2850 if st else None,
              "Total fiber (vol%)": 2.0,
              "Curing method": "demoulded at 48 h, standard curing box 20 °C, 95 % RH (tension specimens: water) to 14 d",
              "Curing time (days)": 14, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 2,
              "Test age (days)": 14, "Compressive specimen": "prism (axial)", "Compressive specimen size (mm)": "40x40x160",
              "Tensile specimen": "dumbbell (JSCE), 30x13 mm section", "Tensile gauge length (mm)": 80,
              "Tensile test type": "direct (uniaxial)", "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
              "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (fibers), Table 3 (mix), Table 4 (tension), p.7 text (fc)",
              "Conversions / notes": f"Mix {mid}. kg/m3 / binder (C 550 + FA 550). PC 42.5R, river sand (max 1.18 mm), PCE SP. "
                                     "PVA properties given as ranges (1500-1600 MPa, 38-41 GPa, 38-40 um): mid values. "
                                     + ("VERIFY: JZ fc derived from S1 = 31.3 MPa being +29.8 % over the reference." if mid == "JZ" else "")})
    rows.append(r)

# ---------------------------------------------------------------------------------------------
# 10) Keshta, Elshikh, Youssf, Abd El-Mohsen (2026) Constr. Mater. 6, 67 - ECC with volcanic materials.
#     Only the F-R mixes (OPC + FA + SF + river sand) qualify; volcanic ash / volcanic sand mixes excluded.
#     Table 2 (fibers), Table 3 (mix kg/m3), Table 4 (fc 3/7/28 d, tension 28 d).
P = paper("A Novel Strategy for Developing Engineered Cementitious Composites: Synergistic Incorporation of Volcanic Materials and PE-PVA Fibers",
          "Mostafa M. Keshta, Mohamed M. Yousry Elshikh, Osama Youssf, Ibrahim Abd El-Mohsen", 2026, "10.3390/constrmater6050067")
B10 = 646 + 451 + 100
for mid, pe, pva, fcs, ft, eps in [("F-R-PE", 2, 0, (38, 46, 66), 6.03, 5.84), ("F-R-PVA", 0, 2, (33, 40, 59), 3.57, 2.00),
                                   ("F-R-PE-PVA", 1, 1, (44, 48, 58), 3.53, 2.90)]:
    for age, fc in zip((3, 7, 28), fcs):
        r = dict(P)
        r.update({"OPC / Cement": round(646 / B10, 4), "FA (Fly ash)": round(451 / B10, 4), "SF (Silica fume)": round(100 / B10, 4),
                  "W / B": round(300 / B10, 4), "River sand / B": round(560 / B10, 4), "SP / B": round(5 / B10, 5),
                  "Binder content (kg/m³)": B10,
                  "PE fiber (vol%)": pe if pe else None, "PE length (mm)": 12 if pe else None,
                  "PE tensile strength (MPa)": 3120 if pe else None, "PE elastic modulus (GPa)": 126 if pe else None,
                  "PVA fiber (vol%)": pva if pva else None, "PVA length (mm)": 12 if pva else None,
                  "PVA tensile strength (MPa)": 1810 if pva else None, "PVA elastic modulus (GPa)": 40 if pva else None,
                  "Total fiber (vol%)": 2.0,
                  "Curing method": "demoulded at 24 h, water curing tank", "Curing time (days)": age, "Demolding age (days)": 1,
                  "Test age (days)": age, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 2 (fibers), Table 3 (mix), Table 4 (fc" + (", tension)" if age == 28 else ")"),
                  "Conversions / notes": f"Mix {mid}. kg/m3 / binder (OPC 646 + FA 451 + SF 100). River sand; PCE SP. "
                                         "Fiber vol% as stated in Table 3 (PE 20 kg/m3 = 2 %, PVA 26 kg/m3 = 2 %)."})
        if age == 28:
            r.update({"Tensile specimen": "dog-bone (JSCE), 13x30 mm section", "Tensile gauge length (mm)": 80,
                      "Tensile test type": "direct (uniaxial)", "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps})
        rows.append(r)

# ---------------------------------------------------------------------------------------------
df = pd.DataFrame(rows).reindex(columns=cols)
# drop papers that meanwhile appear in existing_dois.txt (e.g. 10.1038/s41598-026-73191-6 was added there during this wave)
existing = set(l.strip().lower() for l in open(os.path.join(out_dir, "existing_dois.txt"), encoding="utf-8") if l.strip())
df = df[~df["DOI / URL"].str.replace("https://doi.org/", "").str.lower().isin(existing)]
# drop very-early-age rows below the 5 MPa plausibility floor (1-3 d at 10 °C in the maturity series)
df = df[~(df["Compressive strength (MPa)"] < 5)]
df.to_csv(os.path.join(out_dir, "w5_pva.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", os.path.join(out_dir, "w5_pva.csv"))

rejected = """10.1007/s41062-024-01802-0 | ECC uses glass fiber only (not allowed); EGC mixes alkali + glass fiber
10.1007/s42452-025-08160-1 | review paper (no own mixes)
10.1016/j.cemconcomp.2022.104790 | PP fiber + LC3 (calcined clay) only; no PVA/allowed fiber mix
10.1016/j.conbuildmat.2023.130672 | PVA control mix fc, ft and strain only in figures (Fig. 9, 13); others contain recycled tyre polymer fibres
10.4236/msa.2018.93021 | quartz powder in all mixes (not allowed)
10.17515/resm2022.491me0804 | zeolite in some mixes; all strength results only in figures
10.1016/j.conbuildmat.2018.04.152 | Table 1 internally inconsistent (W/(C+FA) and FA/C do not match kg/m3); results mostly in figures
10.1016/j.cemconcomp.2022.104677 | PE fiber with sulfoaluminate cement (not allowed)
10.1016/j.jobe.2024.109733 | coral sand composites (not a standard ECC sand; uniaxial compression study)
10.21533/pen.v9.i4.1005 | steel/carbon fiber mixes; all results only in figures
10.17222/mit.2022.669 | cement kiln dust and foundry sand; no strength results (shrinkage only)
10.3390/ma19173781 | foamed concrete with calcium formate and foaming agent (not an ECC; not allowed admixtures)
10.3151/jact.13.241 | compressive strength only in a figure; no direct tension (bending only)
10.12677/hjce.2026.159219 | cement/fly ash split not reported (only w/b and s/b); iron oxide pigments
10.28948/ngumuh.1186020 | ECC strength results only in figures; EGC mixes alkali-activated with FA+lime
10.3151/jact.11.301 | air-entraining agent in all mixes (not allowed admixture)
10.3151/jact.11.35 | mix incomplete (cement/fly ash split not given); creep study
10.33261/jaaru.2022.29.2.003 | PP fiber + PVA polymer powder (not PVA fiber); limestone cement only
10.48084/etasr.6731 | polyvinyl alcohol solution admixture in all mixes; PP/PVA fibers; no direct tension
10.3390/buildings12050691 | CaCO3 whisker and air-entraining agent in all mixes (not allowed)
10.3390/buildings13082018 | graphene oxide in all tabulated mixes; control M0 only in figures
10.1007/s44416-026-00075-3 | PVA-film based hybrid 'fibers' (not standard PVA fibers); nano additions
10.37934/araset.31.2.6270 | results only in figures; splitting tension only
10.30880/ijie.2022.14.09.021 | no fly ash; NaOH-treated rubber; results only in figures
10.24191/jmeche.v20i2.22060 | no fly ash; treated crumb rubber; results only in figures
10.3989/mc.2022.06021 | CaCO3 whisker in hybrid mixes; PVA-SHCC compressive results only in figures
"""
with open(os.path.join(out_dir, "w5_pva_rejected.txt"), "w", encoding="utf-8") as f:
    f.write(rejected)
