# Builder for w2_uhpc_ambient.csv -- fibre-reinforced UHPC / RPC / HS mortars with SCMs, ambient/standard curing
# All numbers transcribed from the papers' full text (Europe PMC fullTextXML).
import os, csv
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
with open(os.path.join(D, "TEMPLATE.csv"), encoding="utf-8-sig") as f:
    H = next(csv.reader(f))

BINDER_COLS = ["OPC / Cement", "SAC (Calcium sulfoaluminate cement)", "CAC (Calcium aluminate cement)", "GGBS",
               "FA (Fly ash)", "SF (Silica fume)", "Metakaolin", "Limestone powder", "Diatomite", "Nano-SiO2",
               "Recycled powder (C&D waste)", "Dolomite powder", "Pond ash (PA)", "Other binder", "RHA (Rice husk ash)",
               "EAFD (Electric arc furnace dust)", "Reactive MgO", "CKD (Cement kiln dust)"]
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
    rows.append({k: r4(v) for k, v in d.items()})


# ---------------------------------------------------------------- P1 Yuan et al. 2023 (recycled brick powder UHPC)
B = 1000.0
p1 = {"Article Name": "The Basic Mechanical Properties and Shrinkage Properties of Recycled Micropowder UHPC",
      "Author": "Yuan C.; Chen Y.; Liu D.; Lv W.; Zhang Z.", "Year": 2023, "DOI / URL": "https://doi.org/10.3390/ma16041570",
      "FA (Fly ash)": 100 / B, "SF (Silica fume)": 200 / B, "W / B": 170 / B, "River sand / B": 1000 / B, "Sand max size (µm)": 1250,
      "SP / B": 30 / B, "Binder content (kg/m³)": B,
      "Steel fiber (vol%)": 2, "Steel length (mm)": 12, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2000, "Total fiber (vol%)": 2,
      "Curing method": "Not described in detail; specimens made and tested per T/CCPA 7-2018 and GB/T 50081-2019",
      "Compressive specimen": "cube", "Tensile specimen": "cube (splitting)", "Tensile test type": "splitting",
      "Source table/page": "Table 3 (mix), Table 4 (fc), Table 5 (flexural), Table 6 (splitting)"}
fc1 = {0: (120.8, 131.0, 139.1, 149.9), 10: (120.3, 128.0, 135.6, 141.3), 20: (121.7, 125.1, 129.8, 135.2),
       30: (122.2, 124.9, 127.4, 133.6), 40: (121.5, 121.1, 120.6, 124.7), 50: (119.6, 119.4, 121.5, 123.1)}
ff1 = {0: (20.0, 21.8, 23.5, 23.5), 10: (18.6, 20.0, 22.7, 22.7), 20: (16.7, 19.0, 21.0, 21.0),
       30: (17.2, 18.3, 20.0, 20.0), 40: (17.6, 17.7, 18.6, 18.6), 50: (17.0, 17.7, 17.9, 17.9)}
st1 = {0: (10.90, 12.24, 13.09, 13.94), 10: (10.82, 11.99, 12.50, 13.77), 20: (10.61, 11.66, 12.41, 13.43),
       30: (10.20, 11.90, 12.24, 13.18), 40: (10.37, 11.31, 12.24, 12.78), 50: (9.98, 10.38, 10.82, 11.50)}
for i, rr in enumerate([0, 10, 20, 30, 40, 50]):
    rbp = 70 * i
    for j, age in enumerate([3, 7, 14, 28]):
        add(p1, **{"OPC / Cement": (700 - rbp) / B, "Recycled powder (C&D waste)": rbp / B, "Test age (days)": age,
                   "Compressive strength (MPa)": fc1[rr][j], "Tensile strength (MPa)": st1[rr][j],
                   "Conversions / notes": f"Mix R{i} ({rr}% cement replaced by recycled clay-brick powder). kg/m3 / binder (cement {700 - rbp} + brick powder {rbp} + FA 100 + SF 200 = 1000). Steel fibre 156 kg/m3 = 2 vol% (paper; density 7.8). Fibre strength '>2000 MPa'. Tensile strength = splitting (Table 6). Flexural strength at this age = {ff1[rr][j]} MPa (Table 5; note 14-d and 28-d flexural values are identical in Table 5). Specimen sizes and curing regime not reported."})

# ---------------------------------------------------------------- P2 Liao et al. 2025 (slag UHPC, steel fibre 0-3 %)
B = 1000.0
p2 = {"Article Name": "Influence of Steel Fiber Content on the Long-Term Stability of Slag-Containing UHPC Under Different Environments",
      "Author": "Liao G.; Xu Y.; Wang D.; Wu L.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma18051068",
      "OPC / Cement": 550 / B, "SF (Silica fume)": 200 / B, "GGBS": 250 / B, "W / B": 164 / B, "River sand / B": 1100 / B,
      "Sand max size (µm)": 2360, "SP / B": 20 / B, "Binder content (kg/m³)": B,
      "Curing method": "24 h in moulds in standard curing room, demoulded, then immersed in tap water (ambient) until test",
      "Demolding age (days)": 1, "Compressive specimen": "per GB/T 17671-1999 (mortar prism halves; size not stated)",
      "Source table/page": "Table 3 (mix), Sec. 3.2 text (tap-water fc at 1, 28, 120, 720 d)"}
fc2 = {0: (99.7, 104.7, 120.0, 148.0), 1: (103.4, 109.3, 129.0, 153.0), 2: (129.0, 138.0, 148.0, 163.0), 3: (132.9, 143.6, 157.4, 166.6)}
for vf, kg in [(0, 0.0), (1, 78.5), (2, 157.0), (3, 235.5)]:
    for j, age in enumerate([1, 28, 120, 720]):
        kw = {"Steel fiber (vol%)": vf, "Total fiber (vol%)": vf, "Test age (days)": age, "Compressive strength (MPa)": fc2[vf][j],
              "Conversions / notes": f"Mix K{vf}. kg/m3 / binder (PC 550 + SF 200 + BFS 250 = 1000; w/b 0.18). Steel fibre {kg} kg/m3 = {vf} vol% (paper; = kg/7850). Tap-water exposure series only (outdoor and seawater values only in Fig. 4). Ages are exposure durations as stated in text (specimens were 24 h in moulds before exposure). DOUBTFUL: 1-d strengths of ~100-133 MPa are very high but are as printed."}
        if vf:
            kw.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2800})
        add(p2, **kw)

# ---------------------------------------------------------------- P3 Ahmad et al. 2014 (waste materials in UHPC, Saudi)
p3 = {"Article Name": "Development of UHPC Mixtures Utilizing Natural and Industrial Waste Materials as Partial Replacements of Silica Fume and Sand",
      "Author": "Ahmad S.; Hakeem I.; Maslehuddin M.", "Year": 2014, "DOI / URL": "https://doi.org/10.1155/2014/713531",
      "Steel fiber (vol%)": 157 / 7850 * 100, "Total fiber (vol%)": 157 / 7850 * 100,
      "Curing method": "Covered with plastic sheet 24 h in laboratory (22+/-3 C), then submerged in water tank 28 d",
      "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
      "Source table/page": "Table 7 (mix), Table 8 (28-d fc), Table 9 (flexural)"}
mix3 = [  # id, MS, repl material, repl kg, sand kg, fc, flex
    ("BMWR", 220, None, 0, 1005, 161, 31),
    ("NP40RMS", 132, "NP", 88, 1030, 147, None), ("NP60RMS", 88, "NP", 132, 1042, 154, 29), ("NP80RMS", 44, "NP", 176, 1055, 136, None),
    ("FA40RMS", 132, "FA", 88, 1005, 150, None), ("FA60RMS", 88, "FA", 132, 1005, 158, 32), ("FA80RMS", 44, "FA", 176, 1005, 143, None),
    ("LSP05RMS", 209, "LSP", 11, 1000, 159, None), ("LSP10RMS", 198, "LSP", 22, 995, 146, None), ("LSP20RMS", 176, "LSP", 44, 985, 152, 31),
    ("CKD05RMS", 209, "CKD", 11, 1008, 144, None), ("CKD10RMS", 198, "CKD", 22, 1010, 142, None), ("CKD20RMS", 176, "CKD", 44, 1015, 152, 25),
    ("PSS05RMS", 209, "PSS", 11, 1010, 134, None), ("PSS10RMS", 198, "PSS", 22, 1015, 140, None), ("PSS20RMS", 176, "PSS", 44, 1025, 161, 25),
    ("LSP05RSAND", 220, "LSP", 47, 931, 125, None), ("LSP10RSAND", 220, "LSP", 87, 868, 163, 29), ("LSP20RSAND", 220, "LSP", 153, 764, 132, None),
    ("CKD05RSAND", 220, "CKD", 48, 962, 153, 26), ("CKD10RSAND", 220, "CKD", 92, 922, 135, None), ("CKD20RSAND", 220, "CKD", 170, 851, 100, None),
    ("PSS05RSAND", 220, "PSS", 49, 972, 161, 24), ("PSS10RSAND", 220, "PSS", 94, 942, 153, 23), ("PSS20RSAND", 220, "PSS", 177, 886, 160, 24)]
col3 = {"NP": "Other binder", "FA": "FA (Fly ash)", "LSP": "Limestone powder", "CKD": "CKD (Cement kiln dust)", "PSS": "Other binder"}
name3 = {"NP": "natural pozzolana (volcanic)", "FA": "fly ash", "LSP": "limestone powder", "CKD": "cement kiln dust", "PSS": "pulverized steel slag"}
for mid, ms, mat, rep, sand, fc, fl in mix3:
    B = 900 + ms + rep
    kw = {"OPC / Cement": 900 / B, "SF (Silica fume)": ms / B, "W / B": 162 / B, "Dune sand / B": sand / B, "SP / B": 40 / B,
          "Binder content (kg/m³)": B, "Compressive strength (MPa)": fc}
    note = f"Mix {mid}. kg/m3 / binder, binder = cement 900 + microsilica {ms}"
    if mat:
        kw[col3[mat]] = rep / B
        note += f" + {name3[mat]} {rep} = {B:.0f}"
        if mat in ("NP", "PSS"):
            note += f" ({name3[mat]} put in 'Other binder')"
        if mid.endswith("RSAND"):
            note += f". NOTE: here the {name3[mat]} replaces dune SAND, not microsilica; counted in binder as a powder (the paper keeps binder = cement+MS = 1120 constant, so paper w/b = 0.145)"
    note += ". Water 162 kg/m3 (Table 7; Table 6 base mix lists 163). Superplasticizer Glenium 51 40 kg/m3. Steel fibre 157 kg/m3 -> vol% with 7850 kg/m3 (assumed, fibre properties not reported). Specimen size not reported."
    if fl is not None:
        kw.update({"Tensile strength (MPa)": fl, "Tensile test type": "flexural"})
        note += " Tensile strength = 28-d flexural tensile strength (Table 9)."
    kw["Conversions / notes"] = note
    add(p3, **kw)

# ---------------------------------------------------------------- P4 Zhang et al. 2019 (RPC, FA + slag powder, steel 0-5 %, 3 curing regimes)
B = 1400.0
p4 = {"Article Name": "Reactive Powder Concrete Mix Ratio and Steel Fiber Content Optimization under Different Curing Conditions",
      "Author": "Zhang Y.; Wu B.; Wang J.; Liu M.; Zhang X.", "Year": 2019, "DOI / URL": "https://doi.org/10.3390/ma12213615",
      "SF (Silica fume)": 0.13, "GGBS": 0.05, "River sand / B": 0.70, "Sand max size (µm)": 180, "SP / B": 0.015, "Binder content (kg/m³)": B,
      "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
      "Tensile specimen": "cube 100x100x100 (splitting)"}
cur4 = {"SC": dict(m="Standard curing (20+/-2 C, 95% RH) after demoulding at 1 d", T=20, RH=95, h=""),
        "NC": dict(m="Indoor natural curing (15+/-2 C) after demoulding at 1 d", T=15, RH="", h=""),
        "CC": dict(m="Compound: demould 1 d, hot water 60+/-1 C for 36 h, then indoor natural curing (15+/-2 C)", T=60, RH="", h=36)}
mixnote4 = "Binder 1400 kg/m3 ('gelled material'); fractions from Table 8 (mineral powder S95 slag 5 %, put in GGBS). SP 1.5 % of binder. River sand < 0.18 mm, sand/binder 0.70."
# Table 11: plain matrix, 7-d fc (28-d values of the same plain mixes taken from Tables 12/13)
for c, w, fa, fc7 in [("CC", 0.16, 0.10, 103.54), ("SC", 0.18, 0.20, 80.76), ("NC", 0.18, 0.20, 78.67)]:
    add(p4, **{"OPC / Cement": 1 - 0.13 - fa - 0.05, "FA (Fly ash)": fa, "W / B": w, "Steel fiber (vol%)": 0, "Total fiber (vol%)": 0,
               "Curing method": cur4[c]["m"], "Curing temperature (°C)": cur4[c]["T"], "Curing RH (%)": cur4[c]["RH"], "Heat curing duration (h)": cur4[c]["h"],
               "Test age (days)": 7, "Compressive strength (MPa)": fc7, "Tensile specimen": "",
               "Source table/page": "Tables 8, 10 (mix), Table 11 (7-d fc)",
               "Conversions / notes": f"Optimum plain RPC matrix for {c} (w/b {w}, SF 13 %, FA {int(fa*100)} %). " + mixnote4 + (" Cement 72 % assumes mineral powder stays at 5 % as in all Table 8 mixes." if c == "CC" else " Same as orthogonal mix B5.") + f" Table 11 also gives 28-d fc {dict(CC=106.19, SC=94.82, NC=91.90)[c]} MPa (different batch from Table 12/13 fibre-0 mix; not duplicated)."})
t12 = [(0, 92.83, 11.89, 90.90, 10.34), (1, 99.54, 14.46, 94.00, 12.85), (2, 105.94, 18.01, 100.23, 15.16),
       (3, 111.32, 20.33, 105.22, 17.30), (4, 123.59, 27.60, 113.13, 24.67), (5, 116.55, 25.18, 108.90, 21.90)]
t13 = [(0, 106.19, 12.12), (1, 116.86, 17.21), (2, 123.23, 21.19), (3, 127.40, 22.25), (4, 140.14, 29.10), (5, 136.40, 27.87)]
fibre4 = {"Steel length (mm)": 12, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850}


def p4row(c, vf, fc, ft, w, fa, src, mid):
    kw = {"OPC / Cement": 1 - 0.13 - fa - 0.05, "FA (Fly ash)": fa, "W / B": w, "Steel fiber (vol%)": vf, "Total fiber (vol%)": vf,
          "Curing method": cur4[c]["m"], "Curing temperature (°C)": cur4[c]["T"], "Curing RH (%)": cur4[c]["RH"], "Heat curing duration (h)": cur4[c]["h"],
          "Test age (days)": 28, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile test type": "splitting",
          "Source table/page": src,
          "Conversions / notes": f"Mix {mid}, steel fibre {vf} vol% (copper-plated, 12 mm). " + mixnote4 + (" CC matrix: w/b 0.16, FA 10 %; cement 72 % assumes mineral powder 5 % as in Table 8." if c == "CC" else " Matrix = orthogonal mix B5 (w/b 0.18, SF 13 %, FA 20 %, cement 62 %).")}
    if vf:
        kw.update(fibre4)
    add(p4, **kw)


for vf, fsc, tsc, fnc, tnc in t12:
    p4row("SC", vf, fsc, tsc, 0.18, 0.20, "Tables 8, 10 (mix), Table 12 (28-d fc, splitting)", f"B{vf}")
    p4row("NC", vf, fnc, tnc, 0.18, 0.20, "Tables 8, 10 (mix), Table 12 (28-d fc, splitting)", f"B{vf}")
for vf, fc, ft in t13:
    p4row("CC", vf, fc, ft, 0.16, 0.10, "Table 10 (mix), Table 13 (28-d fc, splitting)", f"B{vf}{vf}")

# ---------------------------------------------------------------- P5 Zhong et al. 2020 (hybrid PP-steel RPC, standard curing)
B = 1400.0
p5 = {"Article Name": "Study on Mechanical Properties of Hybrid Polypropylene-Steel Fiber RPC and Computational Method of Fiber Content",
      "Author": "Zhong C.; Liu M.; Zhang Y.; Wang J.; Liang D.; Chang L.", "Year": 2020, "DOI / URL": "https://doi.org/10.3390/ma13102243",
      "OPC / Cement": 980 / B, "FA (Fly ash)": 280 / B, "SF (Silica fume)": 140 / B, "W / B": 0.18, "River sand / B": 0.75, "Sand max size (µm)": 1180,
      "Binder content (kg/m³)": B, "Curing method": "Standard curing box 20 C, 95% RH; demoulded after 24 h, standard curing until test",
      "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
      "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100", "Tensile specimen": "cube 100x100x100 (splitting)", "Tensile test type": "splitting"}
pp = {"PP length (mm)": 18, "PP diameter (µm)": 34}
st = {"Steel length (mm)": 20, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850}
data5 = [("P0", 0, 0, 78.26, 84.86, 6.5, 9.78, "Table 7 (mix), Table 8"), ("P1", 0.15, 0, 85.12, 96.12, 8.52, 12.89, "Table 7 (mix), Table 8"),
         ("P2", 0.30, 0, 83.64, 91.33, 10.02, 11.48, "Table 7 (mix), Table 8"), ("P3", 0.45, 0, 81.34, 89.27, 8.29, 10.71, "Table 7 (mix), Table 8"),
         ("P4", 0.60, 0, 79.03, 87.65, 6.73, 8.45, "Table 7 (mix), Table 8"),
         ("SP1", 0.15, 1.0, 88.39, 102.72, 11.26, 16.77, "Tables 7, 9 (mix), Table 10"), ("SP2", 0.15, 1.25, 89.01, 109.08, 12.87, 19.83, "Tables 7, 9 (mix), Table 10"),
         ("SP3", 0.15, 1.5, 95.26, 112.71, 13.56, 20.31, "Tables 7, 9 (mix), Table 10"), ("SP4", 0.15, 1.75, 100.96, 123.92, 16.19, 25.49, "Tables 7, 9 (mix), Table 10"),
         ("SP5", 0.15, 2.0, 94.85, 117.39, 19.42, 22.5, "Tables 7, 9 (mix), Table 10")]
for mid, vpp, vst, f7, f28, t7, t28, src in data5:
    for age, fc, ft in [(7, f7, t7), (28, f28, t28)]:
        kw = {"PP fiber (vol%)": vpp, "Steel fiber (vol%)": vst, "Total fiber (vol%)": vpp + vst, "Curing time (days)": age, "Test age (days)": age,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Source table/page": src,
              "Conversions / notes": f"Mix {mid}: PP {vpp} vol% + steel {vst} vol%. kg/m3 / binder (cement 980 + FA 280 + SF 140 = 1400); w/b 0.18, river-sand/binder 0.75 (< 1.18 mm). SP dosage not reported. PP fibre strength 358 MPa; copper-plated steel fibre. Table 10 SP0 (PP 0.15 %, no steel) repeats P1 values - not duplicated."}
        if vpp:
            kw.update(pp)
        if vst:
            kw.update(st)
        add(p5, **kw)

# ---------------------------------------------------------------- P6 He et al. 2021 (glass + HPP fibre UHPC, standard curing, direct tension)
B = 840.0
p6 = {"Article Name": "The Mechanical Properties and Damage Evolution of UHPC Reinforced with Glass Fibers and High-Performance Polypropylene Fibers",
      "Author": "He J.; Chen W.; Zhang B.; Yu J.; Liu H.", "Year": 2021, "DOI / URL": "https://doi.org/10.3390/ma14092455",
      "OPC / Cement": 750 / B, "SF (Silica fume)": 90 / B, "W / B": 191 / B, "SS / B (Silica sand)": (306 + 714) / B, "Sand max size (µm)": 600,
      "QP / B (Quartz powder)": 263 / B, "SP / B": 12 / B, "Binder content (kg/m³)": B,
      "Curing method": "1 d at 20+/-5 C, >50% RH in moulds, then curing room 20+/-2 C, >95% RH; tested after 28 d curing",
      "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1, "Test age (days)": 28,
      "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100", "Tensile specimen": "dog-bone (T/CBMF 37-2018)", "Tensile test type": "direct",
      "Source table/page": "Table 2 (mix), Tables 1, 4 (fibres), Table 5 (results)"}
data6 = [("G1", 1, 0, 115.1, 7.19, 164.15, 7.01, 8.98), ("G2", 1.5, 0, 114.1, 7.41, 166.81, 6.69, 8.68), ("G3", 2, 0, 131.7, 7.51, 180.41, 6.77, 7.70),
         ("H1", 0, 1, 101.2, 5.19, 132.79, 5.77, 6.14), ("H2", 0, 1.5, 95.1, 5.59, 140.72, 5.50, 6.08), ("H3", 0, 2, 108.2, 5.81, 138.52, 5.63, 6.16),
         ("GH1", 0.25, 0.75, 101.8, 5.69, 140.50, 6.06, 6.73), ("GH2", 0.5, 0.5, 100.6, 5.78, 149.35, 6.24, 7.06), ("GH3", 0.75, 0.25, 102.3, 7.03, 165.30, 6.95, 8.29)]
for mid, g, h, fc, ft, eps, fcr, ff in data6:
    kw = {"Glass fiber (vol%)": g, "PP fiber (vol%)": h, "Total fiber (vol%)": g + h, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
          "Tensile strain capacity (%)": eps / 1e4,
          "Conversions / notes": f"Mix {mid}: glass fibre {g} vol% (6 mm, 15 um, 1500 MPa) + high-performance PP {h} vol%. kg/m3 / binder (cement 750 + SF 90). Quartz powder 263 in QP/B; quartz sand I 306 (0.15-0.2 mm) + II 714 (0.3-0.6 mm). Strain = peak tensile strain {eps} microstrain (strain-softening, not a strain-hardening capacity). 4-point bending: initial crack {fcr} MPa, flexural strength {ff} MPa (Table 5)."}
    if h:
        kw.update({"PP length (mm)": 30})
    add(p6, **kw)

# ---------------------------------------------------------------- P7 Lv et al. 2025 (aeolian sand UHPC, slag, curing regimes)
B = 774.7 + 166.0 + 166.0
p7 = {"Article Name": "The Preparation and Properties of Ultra-High-Performance Concrete with Aeolian Sand: A Lab Study on the Effect of the Curing Method",
      "Author": "Lv Y.; Zhao B.; Zhu J.; He C.; Ge Y.; Wu Y.; Zhu Y.; Dan J.; Zhou Y.; Li X.", "Year": 2025, "DOI / URL": "https://doi.org/10.3390/ma18092031",
      "OPC / Cement": 774.7 / B, "SF (Silica fume)": 166.0 / B, "GGBS": 166.0 / B, "W / B": 210.3 / B, "SP / B": 22.1 / B, "Sand max size (µm)": 1180,
      "Binder content (kg/m³)": B, "Steel fiber (vol%)": 0.65, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2929,
      "Total fiber (vol%)": 0.65, "Compressive specimen": "cube", "Compressive specimen size (mm)": "40x40x40", "Tensile specimen": "prism 40x40x160, three-point bending",
      "Tensile test type": "flexural", "Source table/page": "Table 2 (mix), Table 3 (curing), Sec. 3.2 text (fc, flexural)"}
cur7 = {"M1": dict(m="Standard curing 20+/-2 C, >=95% RH, 28 d", T=20, RH=95, t=28, age=28, h=""),
        "M2": dict(m="Steam curing 90 C, >=95% RH, 2 d", T=90, RH=95, t=2, age="", h=48),
        "M3": dict(m="Steam 90 C for 2 d, then standard curing (20 C, >=95% RH) for 5 d (7 d total)", T=90, RH=95, t=7, age=7, h=48)}
for mid, rs1, aS, vals in [("UHPC-4", 383.8, 575.7, {"M1": (94.7, 12.7), "M2": (113.7, 14.6), "M3": (132.4, 18.5)}),
                           ("UHPC-5", 191.9, 767.7, {"M1": (92.9, 13.1), "M2": (108.6, 15.1), "M3": (130.8, 17.7)})]:
    for c, (fc, ff) in vals.items():
        add(p7, **{"River sand / B": (rs1 + 169.3) / B, "Dune sand / B": aS / B, "Curing method": cur7[c]["m"], "Curing temperature (°C)": cur7[c]["T"],
                   "Curing RH (%)": cur7[c]["RH"], "Curing time (days)": cur7[c]["t"], "Test age (days)": cur7[c]["age"], "Heat curing duration (h)": cur7[c]["h"],
                   "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
                   "Conversions / notes": f"Mix {mid} ({'60' if mid == 'UHPC-4' else '80'} % of fine river sand RS1 replaced by aeolian sand; aeolian sand put in Dune sand/B). kg/m3 / binder (cement 774.7 + SF 166 + V800 slag 166 = 1106.7). River sand = RS1 {rs1} (0-0.6 mm) + RS2 169.3 (0.6-1.18 mm). Curing {c}. Tensile strength = flexural (3-point, 40x40x160). Only the 60 % and 80 % mixes have numbers in the text; other mixes only in Figs. 5-6." + (" Test age after M2 not stated (left blank)." if c == "M2" else "")})

# ---------------------------------------------------------------- P8 Wang et al. 2024 (low-heat cement + FA UHPC, titanium-slag sand)
B = 515.19 + 85.8 + 257.66
p8 = {"Article Name": "Mechanical and Drying Shrinkage Performance Study of Ultra-High-Performance Concrete Prepared from Titanium Slag under Different Curing Conditions",
      "Author": "Wang J.; Li J.; Gao Y.; Lu Z.; Hou L.", "Year": 2024, "DOI / URL": "https://doi.org/10.3390/ma17174201",
      "OPC / Cement": 515.19 / B, "SF (Silica fume)": 85.8 / B, "FA (Fly ash)": 257.66 / B, "W / B": 0.2, "SP / B": 13 / B, "Binder content (kg/m³)": B,
      "Demolding age (days)": 1, "Tensile specimen": "prism 40x40x160 (GB/T 17671)", "Tensile test type": "flexural",
      "Source table/page": "Table 4 (mix), Sec. 3.1 text (flexural strengths)"}
cur8 = {"SD": dict(m="Under film 1 d at 20 C, then standard curing 20+/-2 C, 97+/-2% RH", T=20, RH=97, age=28, h="", t=28),
        "SM": dict(m="Under film 1 d at 20 C, then steam curing 80+/-2 C for 48 h", T=80, RH="", age="", h=48, t=2)}
for agg, c, sf, ff in [("SS", "SD", 0, 18.3), ("SS", "SD", 1, 25.4), ("TS", "SD", 0, 24.1), ("TS", "SD", 1, 29.8),
                       ("SS", "SM", 0, 17.3), ("SS", "SM", 1, 29.1), ("TS", "SM", 0, 21.3), ("TS", "SM", 1, 32.8)]:
    kw = {"Curing method": cur8[c]["m"], "Curing temperature (°C)": cur8[c]["T"], "Curing RH (%)": cur8[c]["RH"], "Curing time (days)": cur8[c]["t"],
          "Test age (days)": cur8[c]["age"], "Heat curing duration (h)": cur8[c]["h"], "Tensile strength (MPa)": ff,
          "Steel fiber (vol%)": 120 / 7850 * 100 if sf else 0, "Total fiber (vol%)": 120 / 7850 * 100 if sf else 0,
          "Conversions / notes": f"Mix L-{'SF-' if sf else ''}{c}-{agg}. kg/m3 / binder (low-heat Portland cement 515.19 [in OPC column] + SF 85.8 + FA 257.66 = 858.65). Paper gives 'W/C 0.2' (water mass not tabulated; entered as W/B). Aggregate 1683.52 kg/m3 = " + ("ISO standard sand (SS/B)" if agg == "SS" else "high-titanium slag sand < 4.75 mm (put in M-sand/B; no slag-sand column)") + ". " + ("Steel fibre 120 kg/m3 -> vol% with 7850 kg/m3 (assumed; fibre geometry not reported). " if sf else "") + "Tensile strength = flexural strength from text; compressive strengths only in Fig. 3." + (" Test age after steam curing not stated (left blank)." if c == "SM" else "")}
    kw["SS / B (Silica sand)" if agg == "SS" else "M-sand / B"] = 1683.52 / B
    add(p8, **kw)

df = pd.DataFrame(rows).reindex(columns=H)
df.to_csv(os.path.join(D, "w2_uhpc_ambient.csv"), index=False, encoding="utf-8-sig")
print(len(df), df["DOI / URL"].nunique())
