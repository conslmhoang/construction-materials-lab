"""Wave 5 - agent 'steel': steel-fiber UHPC / HPFRCC without quartz powder.
Writes ml_spike/additions_v2/w5_steel.csv (99-column TEMPLATE header) and prints checks.
All values from the papers' tables/text; derived values are flagged VERIFY in the notes.
Binder B = binder as the paper defines it; kg/m3 values divided by B.
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
STEEL = 7850.0


def r4(x):
    return round(x, 4)


# ---------------------------------------------------------------- 1) Tai, El-Tawil, Belcher (2019)
P = {"Article Name": "Durability properties of a generic ultra-high performance concrete mixed in the field",
     "Author": "Yuh-Shiou Tai, Sherif El-Tawil, John A. Belcher II", "Year": 2019,
     "DOI / URL": "https://doi.org/10.21838/uhpc.9666"}
# Table 1 (by weight, OPC + slag = 1.0): water 0.22, OPC 0.5, slag 0.5, SF 0.25, sand A 0.30, sand B 1.21 (1.20 mix 4)
# Table 2: fc 7/14/28/56 d (cubes, ASTM C109), tensile strength & strain at peak (AASHTO T 132 coupons)
mixes = [  # id, HRWRA, sandB, fiber L, fc7, fc14, fc28, fc56, ft, eps
    ("Mix 1", 0.02, 1.21, 19, 121.3, 149.1, 175.7, 196.2, 12.9, 0.41),
    ("Mix 2", 0.02, 1.21, 13, 118.2, 147.8, 169.2, 187.4, 11.1, 0.17),
    ("Mix 3", 0.03, 1.21, 13, 118.8, 143.5, 159.0, 176.4, 9.5, 0.18),
    ("Mix 4", 0.035, 1.20, 13, 113.4, 137.1, 151.9, None, 9.6, 0.14),
    ("Field batch (Mix 3)", 0.03, 1.21, 13, 108.9, 127.0, 148.1, None, 8.3, 0.13),
]
B = 0.5 + 0.5 + 0.25
for mid, sp, sb, L, f7, f14, f28, f56, ft, eps in mixes:
    for age, fc in ((7, f7), (14, f14), (28, f28), (56, f56)):
        if fc is None:
            continue
        r = dict(P)
        r.update({"OPC / Cement": 0.4, "GGBS": 0.4, "SF (Silica fume)": 0.2,
                  "W / B": r4(0.22 / B), "SS / B (Silica sand)": r4((0.30 + sb) / B), "SP / B": r4(sp / B),
                  "Steel fiber (vol%)": 2.0, "Steel length (mm)": L, "Total fiber (vol%)": 2.0,
                  "Test age (days)": age, "Compressive specimen": "cube (ASTM C109)",
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 1 (mix), Table 2 (fc, ft, strain), p.2-3",
                  "Conversions / notes": f"{mid}. Binder B = OPC + slag + SF (paper normalises OPC+slag = 1.0; SF 0.25). "
                  "Ratios divided by 1.25. Blank cells of Table 1 for mixes 2-4 taken as equal to mix 1 (water, OPC, slag, SF, sand A 0.30) - VERIFY. "
                  "Curing not stated. Fiber diameter not given."})
        if mid.startswith("Field"):
            r["Conversions / notes"] += " Field batch: mixture 3 selected for the field (text p.3); VERIFY mix = Mix 3, field pan-mixed."
        if age == 28:
            r.update({"Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
                      "Tensile specimen": "coupon (AASHTO T 132-87 briquette)",
                      "Tensile test type": "direct (uniaxial)"})
            r["Conversions / notes"] += " VERIFY: tensile test age not stated, attached to the 28-d row; strain = strain at peak tensile stress."
        rows.append(r)

# ---------------------------------------------------------------- 2) Li & Rangaraju (2016)
P = {"Article Name": "Development of UHPC Using Ternary Blends of Ultra-Fine Class F Fly Ash, Meta-kaolin and Portland Cement",
     "Author": "Zhengqi Li, Prasada Rao Rangaraju", "Year": 2016,
     "DOI / URL": "https://doi.org/10.21838/uhpc.2016.64"}
# Table 4 (kg/m3): cement, SFU, MK, FA, sand, SMF, water, HRWRA ; Table 5: fc 1 d, 28 d
mixes = [("UHPC1 (MF2)", 808, 0, 81, 81, 1212, 156, 194, 9.7, 66, 142),
         ("UHPC2 (MF3)", 743, 0, 37, 186, 1208, 156, 193, 9.7, 58, 150),
         ("UHPC3 (S2)", 804, 161, 0, 0, 1206, 156, 193, 9.6, 74, 160)]
for mid, c, sf, mk, fa, s, fib, w, sp, f1, f28 in mixes:
    B = c + sf + mk + fa
    for age, fc in ((1, f1), (28, f28)):
        r = dict(P)
        r.update({"OPC / Cement": r4(c / B), "SF (Silica fume)": r4(sf / B), "Metakaolin": r4(mk / B),
                  "FA (Fly ash)": r4(fa / B), "W / B": r4(w / B), "SS / B (Silica sand)": r4(s / B),
                  "SP / B": r4(sp / B), "Binder content (kg/m³)": B,
                  "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
                  "Steel tensile strength (MPa)": 2000, "Total fiber (vol%)": 2.0,
                  "Curing method": "moist room 100% RH, 23 °C (ASTM C511), demolded at 24 h",
                  "Curing temperature (°C)": 23, "Curing RH (%)": 100, "Demolding age (days)": 1,
                  "Curing time (days)": age, "Test age (days)": age,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
                  "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 4 (mix), Table 5 (fc), p.2-4 (materials, curing)",
                  "Conversions / notes": f"{mid}. kg/m3 / binder (cement+SF+MK+FA = {B} kg/m3). Steel fiber 156 kg/m3 = 2 vol% (paper). "
                  "Natural siliceous sand (ASTM C33). HRWRA powder (polycarboxylic ester). Ultra-fine class F FA. "
                  "VERIFY: curing text written for paste specimens, assumed same for UHPC."})
        rows.append(r)

# ---------------------------------------------------------------- 3) Kim et al. (2019) HP-SIFRCC tension
P = {"Article Name": "Tensile Behavior Characteristics of High-Performance Slurry-Infiltrated Fiber-Reinforced Cementitious Composite with Respect to Fiber Volume Fraction",
     "Author": "Seungwon Kim, Dong Joo Kim, Sung-Wook Kim, Cheolwoo Park", "Year": 2019,
     "DOI / URL": "https://doi.org/10.3390/ma12203335"}
W, C, S, SF, SP = 407.4, 962.8, 566.4, 169.9, 28.3
B = C + SF
for vf, fib, fc, ft, eps in ((4, 312, 66, 11.0, None), (5, 390, 75, 14.2, 0.70), (6, 468, 83, 15.5, 0.53)):
    r = dict(P)
    r.update({"OPC / Cement": r4(C / B), "SF (Silica fume)": r4(SF / B), "W / B": r4(W / B),
              "Sand (type not stated) / B": r4(S / B), "SP / B": r4(SP / B), "Binder content (kg/m³)": round(B, 1),
              "Steel fiber (vol%)": vf, "Steel length (mm)": 60, "Steel diameter (µm)": 750,
              "Steel tensile strength (MPa)": 1200, "Total fiber (vol%)": vf,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200",
              "Tensile specimen": "specimen with 25x50 mm gauge section (wire mesh outside gauge)", "Tensile gauge length (mm)": 50,
              "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix), text sec. 3 (fc, ft, strain)",
              "Conversions / notes": f"SIFCON (fibers pre-placed, slurry infiltrated), double-hooked steel fibers {fib} kg/m3 = {vf} vol% (paper). "
              f"kg/m3 / (cement + SF). Paper states W/B = 35%; computed water/(C+SF) = {W/B:.3f}. fc, ft, strain are 'approximately' "
              "values from the text (figures). Strain = strain at direct tensile strength; 4% strain not given. Curing / test age not stated."})
    rows.append(r)

# ---------------------------------------------------------------- 4) Liu et al. (2022)
P = {"Article Name": "Research on the Relation between Slump Flow and Yield Stress of Ultra-High Performance Concrete Mixtures",
     "Author": "Jizhong Liu, Mingzhe An, Yue Wang, Song Han, Ziruo Yu", "Year": 2022,
     "DOI / URL": "https://doi.org/10.3390/ma15228104"}
mixes = [("A1", 706, 160, 357 + 714 + 178, 164, 15.59, 107.3), ("A2", 706, 160, 357 + 714 + 178, 162, 18.19, 111.5),
         ("A3", 706, 160, 357 + 714 + 178, 161, 20.78, 112.1), ("A4", 706, 160, 357 + 714 + 178, 159, 23.38, 106.4),
         ("B1", 1050, 276, 225 + 449 + 113, 231, 13.26, 106.1), ("B2", 1050, 276, 225 + 449 + 113, 230, 14.59, 109.3),
         ("B3", 1050, 276, 225 + 449 + 113, 229, 15.91, 105.2), ("B4", 1050, 276, 225 + 449 + 113, 228, 17.24, 104.6)]
for mid, c, sf, s, w, sp, fc in mixes:
    B = c + sf
    r = dict(P)
    r.update({"OPC / Cement": r4(c / B), "SF (Silica fume)": r4(sf / B), "W / B": r4(w / B),
              "SS / B (Silica sand)": r4(s / B), "SP / B": r4(sp / B), "Sand max size (µm)": 2500,
              "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": round(160 / STEEL * 100, 2), "Steel length (mm)": 13, "Steel diameter (µm)": 220,
              "Steel tensile strength (MPa)": 2800, "Total fiber (vol%)": round(160 / STEEL * 100, 2),
              "Curing method": "standard curing 20 ± 2 °C, RH > 95%", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
              "Curing time (days)": 28, "Test age (days)": 28, "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix), Table 2 (fc 28 d), sec. 2 (materials, curing)",
              "Conversions / notes": f"{mid}. kg/m3 / (cement + SF = {B}). Quartz sand coarse/medium/fine (0.315-2.5 mm) summed. "
              "Steel fiber 160 kg/m3 -> vol% with 7850 (paper says 2 vol%). Copper-plated straight fiber. "
              "Paper's W/B 0.2 (A) / 0.18 (B) differs slightly from table water/B (SP water). Specimen size not stated."})
    rows.append(r)

# ---------------------------------------------------------------- 5) Liu et al. (2025) Joule heating paper, RT-cured reference
P = {"Article Name": "Gradient Joule Heating Curing Performance of Steel-Fiber-Reinforced High-Performance Concrete in Severe Cold Environments: A Preliminary Attempt for Deep-Cold Concrete Construction",
     "Author": "Xinyu Liu, Jinghui Wang, Zheng Zhou, Lei Zhang, Qiang Fu", "Year": 2025,
     "DOI / URL": "https://doi.org/10.3390/ma18122909"}
r = dict(P)
r.update({"OPC / Cement": 0.8, "SF (Silica fume)": 0.2, "W / B": 0.20, "SS / B (Silica sand)": 1.0, "SP / B": 0.025,
          "Sand max size (µm)": 2000, "Steel fiber (vol%)": 2.5, "Steel length (mm)": 13, "Steel diameter (µm)": 220,
          "Total fiber (vol%)": 2.5, "Curing method": "room-temperature curing 20 ± 2 °C, RH > 95% (reference to Joule-heated series)",
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Curing time (days)": 3, "Test age (days)": 3,
          "Compressive strength (MPa)": 84.3,
          "Source table/page": "Table 2 (mix), sec. 2 & 3 text (curing, fc)",
          "Conversions / notes": "RT-cured reference only (Joule-heated subzero series excluded). SF 20 wt% of binder, sand:binder 1:1 "
          "(quartz sand 0.84-2 mm), PCE-SP 2.5 wt% of binder. 28-d values only in figures."})
rows.append(r)

# ---------------------------------------------------------------- 6) Vacca et al. (2025)
P = {"Article Name": "Rheological Evaluation of Ultra-High-Performance Concrete as a Rehabilitation Alternative for Pavement Overlays",
     "Author": "Hermes Vacca, Yezid A. Alvarado, Daniel M. Ruiz, Andres M. Nuñez", "Year": 2025,
     "DOI / URL": "https://doi.org/10.3390/ma18153700"}
B = 740 + 310 + 210
r = dict(P)
r.update({"OPC / Cement": r4(740 / B), "Limestone powder": r4(310 / B), "SF (Silica fume)": r4(210 / B),
          "W / B": r4(219.0 / B), "SS / B (Silica sand)": r4(802 / B), "SP / B": 0.0196, "Sand max size (µm)": 600,
          "Binder content (kg/m³)": B, "Steel fiber (vol%)": round(153 / STEEL * 100, 2), "Steel diameter (µm)": 200,
          "Steel length (mm)": 13, "Total fiber (vol%)": round(153 / STEEL * 100, 2),
          "Test age (days)": 28, "Compressive strength (MPa)": 137,
          "Source table/page": "Table 2 (mix), sec. 3.5 text (fc SP-0 at 28 d)",
          "Conversions / notes": "SP-0 reference mix only (SP-1..3 fc only in Fig. 18). Binder b = cement (type III) + calcium carbonate + SF "
          "(SP/b = 24.7/1260 = 0.0196 matches paper). Calcium carbonate stored as limestone powder. Effective water 219.0 kg/m3. "
          "Steel 153 kg/m3 -> vol% with 7850. VERIFY: fiber length = 65 x 0.20 mm (aspect ratio) = 13 mm, derived. Curing not stated."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
out = os.path.join(out_dir, "w5_steel.csv")
df.to_csv(out, index=False, encoding="utf-8-sig")
print(len(df), "rows,", df["DOI / URL"].nunique(), "papers ->", out)

# ---- checks
bcols = ["OPC / Cement", "GGBS", "FA (Fly ash)", "SF (Silica fume)", "Metakaolin", "Limestone powder"]
s = df[bcols].fillna(0).sum(axis=1)
print("binder sum range:", s.min(), s.max())
print("W/B range:", df["W / B"].min(), df["W / B"].max())
print("fc range:", df["Compressive strength (MPa)"].min(), df["Compressive strength (MPa)"].max())
print("strain range:", df["Tensile strain capacity (%)"].min(), df["Tensile strain capacity (%)"].max())
print("fiber range:", df["Total fiber (vol%)"].min(), df["Total fiber (vol%)"].max())
print("QP filled:", df["QP / B (Quartz powder)"].notna().sum())
assert list(df.columns) == cols
