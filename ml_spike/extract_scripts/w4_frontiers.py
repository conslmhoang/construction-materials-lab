# Builder for w4_frontiers.csv -- Frontiers in Materials / Frontiers in Built Environment (10.3389/...) papers on
# UHPC / RPC / ECC-SHCC / UHP geopolymer / fibre-reinforced mortars. All numbers transcribed from the publisher HTML
# full text (frontiersin.org/articles/<doi>/full). No direct (uniaxial) tension data was found in the new Frontiers
# papers that had tabulated results; tensile values are flexural or splitting as labelled.
import os, csv, re, glob
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "additions")
OUT = "w4_frontiers.csv"
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


# ---------------------------------------------------------------- P1 Wang et al. 2022 (UHPC rehydration; 0-preload reference values)
p1 = {"Article Name": "Effect of Rehydration on the Performance of Mechanically Loaded UHPC", "Author": "Wang Y.; An M.; Lu J.; Huang H.",
      "Year": 2022, "DOI / URL": "https://doi.org/10.3389/fmats.2022.836201", "Sand max size (µm)": 1250,
      "Curing method": "Demoulded at 24 h, steam cured 75 C for 68 h (15 C/h ramps), then standard curing room for 28 d",
      "Curing time (days)": 28, "Curing temperature (°C)": 75, "Heat curing duration (h)": 68, "Demolding age (days)": 1, "Test age (days)": 28,
      "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
      "Tensile specimen": "cube 100 (splitting, GB/T 50081)", "Tensile test type": "splitting",
      "Source table/page": "Table 1 (mix), Table 2 (fc, splitting; preload level 0)"}
B1 = 706 + 160
for mid, sand, st, vf, fc, ft in [("UHPC-0", 1409, 0, 0, 102.3, 5.11), ("UHPC-2", 1249, 160, 2.0, 130.4, 8.74)]:
    d = {"OPC / Cement": 706 / B1, "SF (Silica fume)": 160 / B1, "W / B": 160 / B1, "SS / B (Silica sand)": sand / B1, "SP / B": 21 / B1,
         "Binder content (kg/m³)": B1, "Steel fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
         "Conversions / notes": f"Mix {mid}. kg/m3 / binder (P.O42.5 cement 706 + micro-silica 160 = {B1}). Quartz sand 0.16-1.25 mm. Steel fibre {st} kg/m3 = {vf} vol% (paper). Unloaded (0% preload) reference specimens, before the 30 C water re-curing series. Test age taken as 28 d (preload referenced to the 28-d ultimate load)."}
    if vf:
        d.update({"Steel length (mm)": 13, "Steel diameter (µm)": 220, "Steel tensile strength (MPa)": 2800})
    add(p1, **d)

# ---------------------------------------------------------------- P2 Huang et al. 2026 (UHP geopolymer concrete, silica fume)
p2 = {"Article Name": "Properties of ultra-high performance geopolymer concrete: influence of silica fume",
      "Author": "Huang H.; Yang L.; Pan K.; Jiang W.; Chen Y.; Hou X.", "Year": 2026, "DOI / URL": "https://doi.org/10.3389/fmats.2026.1784090",
      "NaOH / B": 33.8 / 1056, "WG / B (Water glass)": 501.9 / 1056, "Na2O / B": 0.07, "Activator modulus Ms (SiO2/Na2O)": 2.0,
      "W / B": 0.32, "Sand max size (µm)": 2360, "River sand / B": 1.0, "Binder content (kg/m³)": 1056,
      "Curing method": "24 h in moulds at 20 C / 65% RH under film, demoulded, steam cured 80 C for 24 h",
      "Curing temperature (°C)": 80, "Heat curing duration (h)": 24, "Demolding age (days)": 1,
      "Compressive specimen": "prism halves after 3-point bending", "Compressive specimen size (mm)": "40x40 (from 40x40x160 prisms)",
      "Tensile specimen": "prism 40x40x160 (3-point bending)"}
mix2 = {"A0": (845, 211, 0), "A1": (802, 201, 53), "A2": (760, 190, 106), "A3": (676, 169, 211), "A4": (591, 148, 317)}
res2 = {  # (fc, fc_note, flexural ultimate, first crack)
    "A0": (98.8, "fc 98.8 MPa from Sec. 3.5 text (porosity discussion).", "", ""),
    "A1": (110.7, "fc 110.7 MPa from Sec. 3.3 text.", "", ""),
    "A2": ("", "", 4.6, ""),
    "ZA0": (156.5, "VERIFY: fc derived from text (ZA1 157.0 MPa is 0.32% higher than ZA0) -> 157.0/1.0032.", 24.1, 23.1),
    "ZA1": (157.0, "fc 157.0 MPa from Sec. 3.3 text.", 19.7, 19.0),
    "ZA2": (130.6, "fc 130.6 MPa from Sec. 3.3 text.", 12.2, 10.8),
    "ZA3": ("", "", 17.5, 15.1),
    "ZA4": ("", "", 19.4, 18.2),
}
for mid, (fc, fnote, ff, f1) in res2.items():
    g, fa, sf = mix2[mid.replace("Z", "")]
    d = {"GGBS": g / 1056, "FA (Fly ash)": fa / 1056, "SF (Silica fume)": sf / 1056, "Compressive strength (MPa)": fc,
         "Tensile strength (MPa)": ff, "First-cracking strength (MPa)": f1, "Tensile test type": "flexural" if ff != "" else "",
         "Source table/page": "Table 2 (mix), Sec. 3.3-3.5 text (fc), Table 3 / Sec. 3.4.1 text (flexural)"}
    if mid.startswith("Z"):
        d.update({"Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 120, "Steel tensile strength (MPa)": 2500})
    d["Conversions / notes"] = (f"Mix {mid}. kg/m3 / binder (GGBFS {g} + FA {fa} + SF {sf} = 1056). Activator: NaOH pellets 33.8 + sodium silicate solution 501.9 "
                                f"(8.3% Na2O, 26.5% SiO2, 65.2% H2O) + water 26.7 kg/m3; paper design Ms 2.0, Na2O 7% of binder, W/B 0.32 (paper). "
                                f"Steel fibre 156 kg/m3 = 2 vol% (paper). Test age after steam curing not stated. {fnote} "
                                f"Tensile strength = ultimate 3-point flexural strength; First-cracking = first-crack flexural strength. Other fc values only in Fig. 3.")
    add(p2, **d)

# ---------------------------------------------------------------- P3 Liu et al. 2023 (PE-ECC, static fc)
p3 = {"Article Name": "Experimental study on compressive behavior of PE-ECC under impact load", "Author": "Liu L.; Xiao J.; Wu Z.", "Year": 2023,
      "DOI / URL": "https://doi.org/10.3389/fmats.2023.1204083", "OPC / Cement": 0.5, "FA (Fly ash)": 0.5, "SS / B (Silica sand)": 0.33,
      "Sand max size (µm)": 150, "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 19, "PE tensile strength (MPa)": 3000,
      "PE elastic modulus (GPa)": 110, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
      "Source table/page": "Table 2 (mix), Table 3 (static fc)"}
for mid, w, sp, vma, fc, fcyl in [("M1", 0.36, 0.0040, 0.000482, 41.6, 41.9), ("M2", 0.34, 0.0058, 0.000477, 44.5, 47.7),
                                  ("M3", 0.32, 0.0066, 0.000471, 51.2, 54.7)]:
    add(p3, **{"W / B": w, "SP / B": sp, "VMA / B": vma, "Compressive strength (MPa)": fc,
               "Conversions / notes": f"Mix {mid}. Mass ratios to binder (cement P.O42.5R 0.5 + class-I fly ash 0.5) from Table 2. 100-mesh quartz sand (~150 um). Thickener in VMA/B. PE fibre REC15 (table lists 18 mm length, 19 um). Cube fc (JC/T 2461-2018); cylinder 70x140 fc = {fcyl} MPa. Curing regime and test age not stated."})

# ---------------------------------------------------------------- P4 Buegger et al. 2024 (PVA-ECC, 4-point bending at 56 d)
p4 = {"Article Name": "Assessment of the self-healing capacity of PVA fiber-reinforced composites by chloride permeability and stiffness recovery",
      "Author": "Buegger U.; Carvalho E.B.; Jänicke R.; Tofeti Lima T.", "Year": 2024, "DOI / URL": "https://doi.org/10.3389/fmats.2024.1443216",
      "Sand max size (µm)": 2000, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 12, "PVA diameter (µm)": 200, "PVA tensile strength (MPa)": 975,
      "PVA elastic modulus (GPa)": 27, "Curing method": "Covered with foil, demoulded at 48 h, water tank", "Curing time (days)": 28,
      "Demolding age (days)": 2, "Test age (days)": 56, "Tensile specimen": "beam 250x40x40, 4-point bending (support 230, load span 70)",
      "Tensile test type": "flexural", "Source table/page": "Table 1 (mix), Table 3 (fibre), Sec. 3.1 text (4PBT peak stress)"}
for mid, c, fa, w, sp, s1, s2, strn in [("M1.5", 468, 702, 351, 6, 4.7, 4.5, "0.6-1.0%"), ("M2.0", 386, 772, 347, 4.8, 3.7, 6.7, "1-2%")]:
    B = c + fa
    add(p4, **{"OPC / Cement": c / B, "FA (Fly ash)": fa / B, "W / B": w / B, "SS / B (Silica sand)": 440 / B, "SP / B": sp / B,
               "Binder content (kg/m³)": B, "Tensile strength (MPa)": round((s1 + s2) / 2, 2),
               "Conversions / notes": f"Mix {mid} (FA/C ratio). kg/m3 / binder (CEM I 52.5R {c} + fly ash {fa} = {B}; paper w/b 0.3). Silica sand 0/2. PVA RF400 26 kg/m3 = 2 vol%. Tensile strength = mean of two 4PBT peak stresses ({s1} and {s2} MPa) reached at {strn} strain on the 100 mm tensile-face gauge (bending, not uniaxial; strain not entered). No fc reported."})

# ---------------------------------------------------------------- P5 Wang et al. 2021 (RPC, delay period before 90 C steam)
p5 = {"Article Name": "Mechanism Analysis of the Influence of Delay Period on Mechanical Properties of Reactive Powder Concrete",
      "Author": "Wang X.; Zhao Q.; He X.; Zhang S.", "Year": 2021, "DOI / URL": "https://doi.org/10.3389/fmats.2020.563234"}
B5 = 584 + 90 + 224
base5 = {**p5, "OPC / Cement": 584 / B5, "SF (Silica fume)": 90 / B5, "GGBS": 224 / B5, "W / B": 162 / B5, "River sand / B": 1347 / B5,
         "SP / B": 27 / B5, "Binder content (kg/m³)": B5, "Sand max size (µm)": 2360, "Steel fiber (vol%)": round(157 / 7850 * 100, 2),
         "Steel length (mm)": 12.5, "Steel diameter (µm)": 175, "Curing temperature (°C)": 90,
         "Compressive specimen": "prism (40x40x160) halves", "Compressive specimen size (mm)": "40x40x160 prisms",
         "Source table/page": "Table 3 (mix), Table 4 (fc)"}
fc5 = {18: (184.46, 182.18, 179.28), 24: (189.05, 186.95, 184.95), 30: (186.06, 188.20, 186.71)}
for dp, vals in fc5.items():
    for age, fc in zip((7, 28, 90), vals):
        add(base5, **{"Curing method": f"Delay period {dp} h (standard curing from moulding) then steam curing at 90 C (duration in Fig. 1, not in text)",
                      "Test age (days)": age, "Compressive strength (MPa)": fc,
                      "Conversions / notes": f"Delay period {dp} h. kg/m3 / binder (P.II52.5 cement 584 + SF 90 + slag 224 = {B5}). River sand 0.16-2.36 mm. Steel fibre 157 kg/m3 -> 2.0 vol% at 7850 kg/m3 (copper-plated, 12-13 mm x 0.15-0.20 mm; mid values entered). fc mean of Table 4."})

# ---------------------------------------------------------------- P6 Ji et al. 2021 (RPC from local materials)
p6 = {"Article Name": "Mechanical Behavior of Reactive Powder Concrete Made From Local Material Subjected to Axial Pressure",
      "Author": "Ji J.; Kang W.; Jiang L.; Li Y.; Ren H.; Hao S.; He L.; Lin Y.; Yu C.", "Year": 2021,
      "DOI / URL": "https://doi.org/10.3389/fmats.2021.737646", "Sand max size (µm)": 380, "Test age (days)": 28,
      "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7x70.7x70.7", "Source table/page": "Table 1 (mix ratios), Table 4 (fc)"}
mix6 = [("A1", .22, .3, .25, 1.2, 0, 84.83), ("A2", .20, .3, .25, 1.2, 0, 93.42), ("A3", .18, .3, .25, 1.2, 0, 95.43), ("A4", .16, .3, .25, 1.2, 0, 99.74),
        ("B1", .2, .2, .25, 1.2, 0, 73.82), ("B2", .2, .4, .25, 1.2, 0, 77.23), ("B3", .2, .5, .25, 1.2, 0, 87.58),
        ("C1", .2, .3, .15, 1.2, 0, 85.20), ("C2", .2, .3, .35, 1.2, 0, 91.39), ("C3", .2, .3, .4, 1.2, 0, 76.16),
        ("D1", .2, .3, .25, 1.4, 0, 80.36), ("D2", .2, .3, .25, 1.6, 0, 83.99), ("D3", .2, .3, .25, 1.8, 0, 75.23),
        ("E1", .2, .3, .25, 1.2, 1, 130.45), ("E2", .2, .3, .25, 1.2, 2, 154.18), ("E3", .2, .3, .25, 1.2, 3, 167.02),
        ("F0", .2, .3, .25, 1.2, 0, 56.35), ("G0", .16, .3, .25, 1.2, 0, 60.53), ("H0", .2, .3, .25, 1.2, 2, 82.50),
        ("F6", .2, .3, .25, 1.2, 0, 74.16), ("G6", .16, .3, .25, 1.2, 0, 84.18), ("H6", .2, .3, .25, 1.2, 2, 159.96)]
for mid, wb, s, p, q, f, fc in mix6:
    B = 1 + s + p
    if mid[1] == "0":
        cm, hc, ver = "No steam curing; water-spray curing at room temperature to 28 d", "", ""
    elif mid[1] == "6":
        cm, hc, ver = "Steam cured 80 C for 6 d, then water-spray curing at room temperature to 28 d", 144, ""
    else:
        cm, hc, ver = "Steam curing regime for series A-E not stated explicitly (paper: some specimens steam cured 80 C for 3 or 6 d, others not); then water-spray curing to 28 d", "", " VERIFY curing of series A-E (likely 3-d steam at 80 C)."
    d = {"OPC / Cement": 1 / B, "SF (Silica fume)": s / B, "GGBS": p / B, "W / B": wb, "SS / B (Silica sand)": q / B,
         "Steel fiber (vol%)": f, "Curing method": cm, "Heat curing duration (h)": hc, "Compressive strength (MPa)": fc,
         "Conversions / notes": f"Mix {mid}. Paper gives ratios to cement: SF/c {s}, slag/c {p}, quartz sand/c {q}; converted to binder (cement+SF+S95 slag). w/b as given. Quartz sand 40-140 mesh. FDN superplasticizer dosage not given per mix. Steel fibre vol% of mixture (13 mm x 0.22 mm).{ver}"}
    if mid[1] in "06":
        d["Curing temperature (°C)"] = 80 if mid[1] == "6" else ""
    if f:
        d.update({"Steel length (mm)": 13, "Steel diameter (µm)": 220})
    add(p6, **d)

# ---------------------------------------------------------------- P7 Weng & Liao 2024 (UHPC + CaO expansive agent + steel fibres)
p7 = {"Article Name": "Autogenous shrinkage prediction models and microstructure of UHPC with single or binary addition of an expansive agent and steel fibers",
      "Author": "Weng J.; Liao W.", "Year": 2024, "DOI / URL": "https://doi.org/10.3389/fmats.2024.1427230", "Sand max size (µm)": 700,
      "Curing method": "Under plastic film 24 h, demoulded, standard curing room 20+/-2 C, >95% RH", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
      "Demolding age (days)": 1, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
      "Tensile specimen": "prism 100x100x515 (GB/T 50081)", "Tensile test type": "flexural", "Source table/page": "Table 3 (mix), Table 4 (fc/flexural)"}
mix7 = [("G1", 0, 0, 0, (81.4, 16.9), (106.4, 22.1), (130.3, 27.0)), ("G2", 0, 0, 0.5, (90.5, 19.4), (117.8, 25.3), (134.2, 28.5)),
        ("G3", 0, 1.0, 1.5, (104.2, 25.5), (136.9, 33.6), (157.8, 38.5)), ("G4", 3, 0, 0.5, (87.3, 17.9), (115.3, 23.6), (133.1, 27.1)),
        ("G5", 3, 1.0, 1.5, (101.8, 23.8), (134.2, 31.5), (155.7, 36.3)), ("G6", 6, 0, 0, (75.7, 15.1), (100.4, 20.1), (128.1, 25.8)),
        ("G7", 6, 0, 0.5, (83.4, 16.3), (112.5, 21.9), (132.3, 27.1)), ("G8", 6, 1.0, 1.0, (94.2, 20.8), (125.1, 27.4), (150.3, 34.2)),
        ("G9", 6, 1.0, 1.5, (98.2, 21.9), (131.7, 29.5), (153.6, 35.7)), ("G10", 6, 1.5, 1.0, (100.6, 23.2), (133.9, 30.7), (154.3, 37.3)),
        ("G11", 6, 1.5, 1.5, (106.2, 26.7), (138.3, 34.3), (159.7, 40.7))]
for mid, cea, hk, stv, r3, r7, r28 in mix7:
    B0 = 790 + 198
    ea = cea / 100 * B0
    B = B0 + ea
    for age, (fc, ff) in zip((3, 7, 28), (r3, r7, r28)):
        d = {"OPC / Cement": 790 / B, "SF (Silica fume)": 198 / B, "Other binder": ea / B, "W / B": 0.18 * B0 / B,
             "QP / B (Quartz powder)": 198 / B, "SS / B (Silica sand)": 870 / B, "SP / B": 52.3 / B, "Binder content (kg/m³)": round(B, 1),
             "Steel fiber (vol%)": hk + stv, "Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
             "Conversions / notes": f"Mix {mid}. kg/m3: cement 790, SF 198, quartz powder 198, quartz sand 870 (0.21-0.70 mm), SP 52.3, W/B 0.18 (paper, on cement+SF). CaO-based expansive agent {cea}% by mass of binder ({ea:.1f} kg/m3) entered as 'Other binder' and binder renormalised (W/B recomputed). Steel fibres: hooked-end {hk} vol% + straight {stv} vol% (both 13 mm x 0.2 mm; 2850 / 3010 MPa). Tensile strength = flexural strength."}
        if hk + stv:
            d.update({"Steel length (mm)": 13, "Steel diameter (µm)": 200})
        add(p7, **d)

# ---------------------------------------------------------------- P8 Lande et al. 2025 (UHPFRC full-scale RMC production)
B8 = 719 + 143
p8 = {"Article Name": "Full-scale production and material properties of ultra-high-performance fiber-reinforced concrete (UHPFRC) for rehabilitation of bridge decks in Norway",
      "Author": "Lande I.; Thorstensen R.T.; Petersen B.G.; Kanstad T.", "Year": 2025, "DOI / URL": "https://doi.org/10.3389/fbuil.2025.1570920",
      "OPC / Cement": 719 / B8, "SF (Silica fume)": 143 / B8, "W / B": 0.22, "Local sand / B": 1069 / B8, "Sand max size (µm)": 8000,
      "SP / B": 20 / B8, "Binder content (kg/m³)": B8, "Steel fiber (vol%)": round(225 / 7850 * 100, 2), "Steel length (mm)": 12.5,
      "Steel diameter (µm)": 175, "Steel tensile strength (MPa)": 2800, "Steel elastic modulus (GPa)": 210,
      "Curing method": "Water curing at 20 C", "Curing temperature (°C)": 20, "Compressive specimen": "cube", "Compressive specimen size (mm)": "100x100x100",
      "Source table/page": "Table 4 (mix UHPC-RMC 3 vol%), Sec. 4.1.2 text (fc)"}
for age, fc in [(1, 42), (14, 147), (28, 170)]:
    add(p8, **{"Curing time (days)": age, "Test age (days)": age, "Compressive strength (MPa)": fc,
               "Conversions / notes": "Mix UHPC-RMC 3 vol% (ready-mix plant). kg/m3 / binder (CEM II/A-V 52.5N 719 + silica fume 143 = 862; paper w/b 0.22 with k=1). Limestone filler 159 kg/m3 (LF/B 0.184) is not binder per paper and has no template column. SRA 7.2 and retarder 3.7 kg/m3 not entered. Natural sand 0-8 mm. Steel fibre 225 kg/m3 -> 2.87 vol% at 7850 (paper: ~3 vol%). Values from text; 7-d and other series only in Fig. 7-8."})

# ---------------------------------------------------------------- P9 Fu et al. 2022 (UHPC grouting material)
B9 = 1086 + 81 + 206
p9 = {"Article Name": "Experimental Study on UHPC-Based Grouting Materials and Mechanical Performance of Grouted Splice Sleeve Joints",
      "Author": "Fu T.; Hou J.; Zhu Z.; Meng L.; Sun Z.; Wang K.; Ren X.", "Year": 2022, "DOI / URL": "https://doi.org/10.3389/fmats.2022.912509",
      "OPC / Cement": 1086 / B9, "SF (Silica fume)": 81 / B9, "FA (Fly ash)": 206 / B9, "W / B": 198 / B9, "SS / B (Silica sand)": 1511 / B9,
      "Sand max size (µm)": 425, "SP / B": 45 / B9, "Binder content (kg/m³)": B9, "Compressive specimen": "prism halves (GB/T 17671)",
      "Compressive specimen size (mm)": "40x40x160 prisms", "Tensile specimen": "prism 40x40x160 (3-point, GB/T 17671)", "Tensile test type": "flexural",
      "Source table/page": "Table 7 (mix), Table 8 (fc, flexural)"}
for mid, st, fc, ff in [("GA", 0, 119.6, 9.4), ("GB", 236, 128.4, 17.6)]:
    d = {"Steel fiber (vol%)": round(st / 7850 * 100, 2), "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ff,
         "Conversions / notes": f"Mix {mid}. kg/m3 / binder (cement 1086 + SF 81 + FA 206 = {B9}). Quartz sand 0.18-0.425 mm. Steel fibre {st} kg/m3 -> vol% at 7850. Fibre listed as 6 mm x '2 mm' (aspect ratio 3; diameter likely misprint, not entered), 2850 MPa. Curing and test age not stated. Tensile strength = flexural strength."}
    if st:
        d.update({"Steel length (mm)": 6, "Steel tensile strength (MPa)": 2850})
    add(p9, **d)

# ---------------------------------------------------------------- P10 Song et al. 2026 (hybrid steel-PP UHPC, unconfined columns)
B10 = 630 + 262 + 158
p10 = {"Article Name": "Axial compression performance of GFRP-confined hybrid fiber-reinforced UHPC columns",
       "Author": "Song S.; You P.; Wang X.; Zhang B.; Zhu B.", "Year": 2026, "DOI / URL": "https://doi.org/10.3389/fmats.2026.1774141",
       "OPC / Cement": 630 / B10, "GGBS": 262 / B10, "FA (Fly ash)": 158 / B10, "W / B": 220 / B10, "SS / B (Silica sand)": 1050 / B10,
       "SP / B": 21 / B10, "Binder content (kg/m³)": B10, "Sand max size (µm)": 2360,
       "Curing method": "Wooden formwork, covered with film and watered; demoulded at 24 h; natural curing 28 d", "Curing time (days)": 28,
       "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "unconfined column (cylinder)",
       "Compressive specimen size (mm)": "200x1100", "Source table/page": "Table 7 (mix), Tables 5-6 (fibres), Table 9 (unconfined peak stress)"}
for mid, sv, pv, fc in [("S0P10", 0, .10, 60.4), ("S10P0", 1.0, 0, 70.8), ("S10P05", 1.0, .05, 70.1), ("S10P10", 1.0, .10, 75.4), ("S10P15", 1.0, .15, 79.9),
                        ("S15P05", 1.5, .05, 79.4), ("S15P10", 1.5, .10, 77.5), ("S15P15", 1.5, .15, 78.0), ("S20P05", 2.0, .05, 81.3),
                        ("S20P10", 2.0, .10, 80.3), ("S20P15", 2.0, .15, 78.0)]:
    d = {"Steel fiber (vol%)": sv, "PP fiber (vol%)": pv, "Compressive strength (MPa)": fc,
         "Conversions / notes": f"Mix G0{mid} (unconfined). kg/m3 / binder (P.O42.5 630 + S105 slag 262 + FA 158 = {B10}; paper w/b 0.2). 'Quartz sand' per Table 7 (described as 20-40 mesh river sand in text). fc = peak axial stress of a single 200x1100 mm unconfined UHPC column (one specimen; slenderness 5.5), not a standard cube/cylinder strength."}
    if sv:
        d.update({"Steel length (mm)": 12, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850})
    if pv:
        d.update({"PP length (mm)": 8, "PP diameter (µm)": 48})
    add(p10, **d)

# ---------------------------------------------------------------- P11 Glanz et al. 2023 (AAM-UHPC vs PC-UHPC, no fibres)
p11 = {"Article Name": "Comparative environmental footprint analysis of ultra-high-performance concrete using Portland cement and alkali-activated materials",
       "Author": "Glanz D.; Sameer H.; Göbel D.; Wetzel A.; Middendorf B.; Mostert C.; Bringezu S.", "Year": 2023,
       "DOI / URL": "https://doi.org/10.3389/fbuil.2023.1196246",
       "Curing method": "Covered at 20 C / 65% RH, demoulded at 1 d, stored sealed in plastic bags at 20 C", "Curing temperature (°C)": 20,
       "Demolding age (days)": 1, "Source table/page": "Table 1 (mix, fc 7 d and 28 d)"}
mix11 = [("M2", 0, 538, 299, 400, 0, 996, 159, 0, .23, 162.9, 194.2), ("M3", 0, 571, 317, 324, 0, 1057, 169, 0, .175, 188.4, 211.8),
         ("M4", 0, 769, 62, 238, 114, 989, 158, 0, .275, 124.9, 155.3), ("PC-ref", 801, 0, 170, 0, 199, 970, 193, 24, .21, 138.2, 176.7)]
for mid, c, g, sf, wg, w, qs, qp, sp, wb, f7, f28 in mix11:
    B = c + g + sf
    d = {"OPC / Cement": c / B, "GGBS": g / B, "SF (Silica fume)": sf / B, "W / B": wb, "SS / B (Silica sand)": qs / B, "QP / B (Quartz powder)": qp / B,
         "Binder content (kg/m³)": B}
    if wg:
        d.update({"WG / B (Water glass)": wg / B, "Activator modulus Ms (SiO2/Na2O)": 1.0})
        note = f"Mix {mid} (AAM-UHPC). kg/m3 / binder (GGBFS {g} + SF {sf} = {B}). Activator = POTASSIUM waterglass K57 (SiO2:K2O = 1, 52% solids) {wg} kg/m3 entered in WG/B; Ms column holds SiO2:K2O. Additional water {w} kg/m3. w/b from paper (excludes activator solids)."
    else:
        d.update({"SP / B": sp / B})
        note = f"Mix {mid}. kg/m3 / binder (CEM I 52.5R 801 + SF 170 = {B}); water 199, PCE 24 kg/m3; w/b 0.21 (paper)."
    note += " No fibres. Quartz sand and quartz powder as SS/B and QP/B. Specimen geometry not stated. Mix M1 (KOH + K28 waterglass) excluded: KOH has no template column."
    for age, fc in ((7, f7), (28, f28)):
        add(p11, **d, **{"Test age (days)": age, "Compressive strength (MPa)": fc, "Conversions / notes": note})

# ---------------------------------------------------------------- P12 Zhang et al. 2020 (AR-glass short fibre fine-grained concrete matrix)
p12 = {"Article Name": "Study on Flexural Properties of Basalt Fiber Textile Reinforced Concrete (BTRC) Sheets Including Short AR-Glass Fibers",
       "Author": "Zhang Q.; Li S.; Gong S.; Zhang G.; Xi G.; Wu Y.", "Year": 2020, "DOI / URL": "https://doi.org/10.3389/fmats.2020.00277",
       "OPC / Cement": 1.0, "W / B": 0.34, "River sand / B": 1.36, "SP / B": 0.016,
       "Curing method": "Demoulded at 24 h, water curing at room temperature", "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
       "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7x70.7x70.7", "Tensile specimen": "cube 70.7 (splitting)",
       "Tensile test type": "splitting", "Source table/page": "Sec. 2 text (mix 1:1.36:0.34:0.016), Table 1 (fibre), Table 2 (fcu, ffu, ftu)"}
for mid, L, wt, fc, ffl, ft in [("PC", "", 0, 38.5, 9.3, 3), ("GF6-2", 6, 2, 37.5, 9.8, 3.7), ("GF6-5", 6, 5, 38.6, 11.9, 4.6), ("GF6-8", 6, 8, 38.8, 14, 4.1),
                                ("GF12-2", 12, 2, 38, 11.4, 3.8), ("GF12-5", 12, 5, 39, 14, 3.9), ("GF12-8", 12, 8, 40.3, 14.4, 4.6),
                                ("GF18-2", 18, 2, 39.7, 12.3, 5.2), ("GF18-5", 18, 5, 41.5, 13.3, 5.4), ("GF18-8", 18, 8, 41, 15, 4.7)]:
    vf = {0: 0, 2: 0.6, 5: 1.5, 8: 2.5}[wt]
    add(p12, **{"Glass fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
                "Conversions / notes": f"Mix {mid}. OPC 42.5R : river sand : water : PCA water reducer = 1 : 1.36 : 0.34 : 0.016 (by mass). AR-glass short fibre {L} mm x 15 um, {wt} wt% -> {vf} vol% (paper's conversion). Tensile strength = splitting; flexural strength (40x40x160) = {ffl} MPa."})

# ---------------------------------------------------------------- P13 Abusogi et al. 2023 (PP fibre mortar / paste, 3 d)
p13 = {"Article Name": "Effect of polypropylene fibre on cementitious mortar early shrinkage cracking using the eccentric-ring test",
       "Author": "Abusogi M.A.; Muda Z.C.; Hafez M.A.; Bakri M.", "Year": 2023, "DOI / URL": "https://doi.org/10.3389/fmats.2022.1052870",
       "OPC / Cement": 1.0, "Binder content (kg/m³)": 1200, "PP length (mm)": 20, "PP diameter (µm)": 100,
       "Curing method": "24 h in curing chamber 20 C / 98% RH, then 20 C / 45% RH environmental chamber (ASTM C192)",
       "Demolding age (days)": 1, "Curing time (days)": 3, "Test age (days)": 3, "Compressive specimen": "cube (ASTM C109)",
       "Compressive specimen size (mm)": "40x40x40", "Tensile specimen": "prism 160x40x40, 3-point bending (ASTM C1609)", "Tensile test type": "flexural",
       "Source table/page": "Table 3 (mix), Tables 4-5 (fibre), Tables 6-7 (3-d tensile, fc)"}
res13 = {"M1": (0.3, 1.0, [(0, 2.95, 39.72), (.4, 3.21, 40.51), (.6, 3.50, 41.25), (.8, 4.40, 57.90)]),
         "M2": (0.4, 2.0, [(0, 1.13, 24.65), (.4, 1.60, 32.35), (.6, 1.90, 37.35), (.8, 2.09, 39.66)]),
         "M3": (0.5, 2.0, [(0, .73, 21.35), (.4, .93, 22.25), (.6, 1.02, 24.90), (.8, 1.13, 24.50)]),
         "M4": (0.3, 0.0, [(0, 1.9, 45.8), (.4, 2.5, 46.8), (.6, 2.8, 47.0), (.8, 3.2, 48.1)]),
         "M5": (0.4, 0.0, [(0, 1.7, 34.9), (.4, 1.9, 35.7), (.6, 2.1, 38.7), (.8, 2.5, 38.0)]),
         "M6": (0.5, 0.0, [(0, 1.1, 25.2), (.4, 1.2, 26.3), (.6, 1.5, 27.0), (.8, 1.45, 27.3)])}
for m, (wc, sb, lst) in res13.items():
    for vf, ft, fc in lst:
        spn = " Naphthalene SP 0.1-0.25% of cement used for w/c 0.3 mixes (increasing with fibre dosage; exact per-mix value not tabulated, not entered)." if wc == 0.3 else ""
        add(p13, **{"W / B": wc, "River sand / B": sb, "PP fiber (vol%)": vf, "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft,
                    "Conversions / notes": f"Series {m}, Vf {vf}%. OPC 1200 kg/m3, sand/cement {sb} ({'mortar' if sb else 'cement paste'}), w/c {wc}. PP monofilament 20 mm, 100+/-50 um. 'Tensile strength' in paper = ASTM C1609 3-point bending on 40x40x160 prisms (entered as flexural).{spn}"})

# ---------------------------------------------------------------- P14 Snoeck & De Belie 2019 (PVA-SHCC with SAP, first-cracking strength up to 8 years)
p14 = {"Article Name": "Autogenous Healing in Strain-Hardening Cementitious Materials With and Without Superabsorbent Polymers: An 8-Year Study",
       "Author": "Snoeck D.; De Belie N.", "Year": 2019, "DOI / URL": "https://doi.org/10.3389/fmats.2019.00048", "Sand max size (µm)": "",
       "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "Curing method": "Demoulded at 24 h, stored at 95+/-5% RH and 20+/-2 C until testing",
       "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 1,
       "Tensile specimen": "plate 160x40x10, 4-point bending", "Tensile test type": "flexural", "Source table/page": "Table 1 (mix), Table 3 (first-cracking strength), Table 2 (ductility)"}
fcs14 = {"REF": (608, 608, 426, 365, 0, 11.8, 0, [4.5, 4.8, 5.4, 6.0, 6.3, 6.4], [5.4, 2.9, 2.4, 1.8, 1.4, 1.2]),
         "0.5A": (554, 554, 388, 332, 85, 10.7, 2.77, [4.9, 4.9, 5.3, 5.6, 5.9, 6.1], [5.1, 3.5, 2.6, 2.2, 1.8, 1.6]),
         "0.5B": (590, 590, 413, 354, 26, 11.4, 2.95, [4.6, 5.1, 5.2, 5.5, 5.8, 6.0], [4.9, 3.5, 2.8, 2.5, 2.1, 1.9]),
         "1B": (572, 572, 400, 343, 51, 11.1, 5.72, [4.7, 4.9, 5.3, 5.5, 5.7, 5.9], [5.5, 3.8, 3.1, 2.6, 2.2, 2.0])}
ages14 = [(7, "7 days"), (28, "28 days"), (91, "3 months"), (365, "1 year"), (1095, "3 years"), (2920, "8 years")]
for mid, (c, fa, s, w, wadd, spl, sap, f1s, duct) in fcs14.items():
    B = c + fa
    for (age, lab), f1, du in zip(ages14, f1s, duct):
        add(p14, **{"OPC / Cement": c / B, "FA (Fly ash)": fa / B, "W / B": (w + wadd) / B, "Extra water / B": wadd / B,
                    "Fine sand / B": s / B, "SP / B": spl / B, "Binder content (kg/m³)": B, "Test age (days)": age, "Curing time (days)": age,
                    "First-cracking strength (MPa)": f1,
                    "Conversions / notes": f"Mix {mid}, age {lab} (days approximated: 3 months=91, 1 yr=365, 3 yr=1095, 8 yr=2920). kg/m3 / binder (CEM I 52.5N {c} + FA {fa} = {B}). Fine quartz sand M34 (D50 170 um). W/B includes additional water {wadd} kg/m3 for SAP (in 'Extra water / B'). SAP {sap} kg/m3 (SAP/B {sap / B:.4f}; no template column). PVA 2 vol% (26 kg/m3; 15 dtex, 8 mm) per text - Table 1 shows '-' for REF PVA, VERIFY. First-cracking strength = 4PBT first kink, uncracked virgin specimens. 4PBT bottom-fibre ductility (multiple-cracking amount) = {du}% (flexural, not uniaxial; not entered as strain capacity). No fc reported."})

# ---------------------------------------------------------------- write
df = pd.DataFrame(rows).reindex(columns=H)
seen = set()
with open(os.path.join(D, "existing_papers.txt"), encoding="utf-8-sig") as f:
    for l in f:
        m = re.search(r"10\.\d+/\S+", l)
        if m:
            seen.add(m.group(0).lower().rstrip("/.,"))
for fn in glob.glob(os.path.join(D, "*.csv")):
    if os.path.basename(fn) in ("TEMPLATE.csv", OUT):
        continue
    for v in pd.read_csv(fn, encoding="utf-8-sig", usecols=["DOI / URL"])["DOI / URL"].dropna().unique():
        m = re.search(r"10\.\d+/\S+", str(v))
        if m:
            seen.add(m.group(0).lower())
doi = df["DOI / URL"].str.extract(r"(10\.\d+/\S+)")[0].str.lower()
dup = sorted(set(doi[doi.isin(seen)]))
if dup:
    print("DROPPING already-collected DOIs:", dup)
df = df[~doi.isin(seen)]
df.to_csv(os.path.join(D, OUT), index=False, encoding="utf-8-sig")
print(len(df), df["DOI / URL"].nunique())
