"""Wave 6, agent e48: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e48.csv (99-column TEMPLATE header).
Papers: conbuildmat.2024.136312, conbuildmat.2023.131990
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


def paper(name, author, year, doi):
    return {"Article Name": name, "Author": author, "Year": year, "DOI / URL": "https://doi.org/" + doi}


# ---------- 1) Liao et al. 2024: PE-ECC with 0.5-2.0 vol% PE fibre, air curing 28 d
P = paper("Tension-shear characteristics, cost and environmental impact of polyethylene fiber reinforced engineered cementitious composites: The role of fiber content",
          "Qiao Liao, Jiang-Tao Yu, Fang-Yuan Dong, Roman Fediuk, Ke-Quan Yu", 2024, "10.1016/j.conbuildmat.2024.136312")
B = 656 + 118 + 246
for vf, ts, eps, fc in [(0.5, 1.92, 0.71, 30.94), (1.0, 4.04, 6.24, 36.07), (1.5, 4.54, 6.46, 32.01), (2.0, 3.99, 5.06, 30.85)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(656 / B), "FA (Fly ash)": r4(118 / B), "SF (Silica fume)": r4(246 / B), "W / B": r4(448 / B),
              "SS / B (Silica sand)": r4(604 / B), "Crumb rubber / B": r4(57 / B), "HRWR / B": r4(5 / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": vf, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900, "Total fiber (vol%)": vf,
              "Curing method": "air: 24 h in plastic mould, demoulded, stored in air for 28 d", "Curing time (days)": 28, "Demolding age (days)": 1,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (matrix mix), sect. 2.1 (fibre), Table 2 (fc, tensile)",
              "Conversions / notes": f"ECC-{vf}%. kg/m3 / B (cement + FA + SF = {B}). Silica sand 604, crumb rubber 57, HRWR 5, water 448 kg/m3. "
                                     "Tensile = dogbone, uniaxial, 2 mm/min (JSCE); strength = peak, strain = tensile strain capacity of Table 2. "
                                     "VERIFY: test age taken as 28 d (stated curing: 24 h mould + 28 d air). Cube 70.7 mm. ECC-0.5% is not strain-hardening (1 crack)."})
    rows.append(r)

# ---------- 2) Soliman et al. 2023: UHPC SF (steel) and PE (UHMWPE), 6 weeks water curing
P = paper("Effects of the tensile properties of UHPC on the bond behavior", "Amr Ashraf Soliman, William F. Heard, Brett A. Williams, Ravi Ranade",
          2023, "10.1016/j.conbuildmat.2023.131990")
# name, cement, SF, slag, sand, w/cm, HRWRA, fibre kind, fc, ts, eps
for nm, sf, sl, sand, wcm, hr, kind, fc, ts, eps in [("SF (steel 2 vol%)", 0.20, 0.52, 1.40, 0.21, 0.012, "steel", 151, 7.4, 0.20),
                                                      ("PE (PE 2 vol%)", 0.28, 0.38, 0.82, 0.20, 0.050, "pe", 119, 6.1, 6.60)]:
    B = 1 + sf + sl
    r = dict(P)
    r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(sf / B), "GGBS": r4(sl / B), "W / B": wcm, "HRWR / B": r4(hr / B),
              "Total fiber (vol%)": 2,
              "Curing method": "24 h in covered mould, demoulded, water 6 weeks, then 50 C oven 24 h, air 24 h", "Curing time (days)": 42,
              "Demolding age (days)": 1, "Test age (days)": 45, "Compressive specimen": "cube", "Compressive specimen size (mm)": "51",
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 1 (weight proportions), sect. 2.1-2.3, Table 3 (fc, tensile)"})
    note = (f"{nm}. Table 1 weight proportions (taken as ratios to cement = 1; B = cement + SF + slag = {r4(B)}); W/B = w/cm as defined in Table 1 note; HRWRA / cement ratio / B. "
            "Tensile = dogbone uniaxial, strain = strain at peak stress (strain capacity). "
            "VERIFY: ratios assumed relative to cement; test age = 1 d mould + 6 wk water + 1 d oven + 1 d air = about 45 d (age of tests not stated explicitly, same curing as bond specimens); "
            "50 C oven drying before tests. SFW mix (steel wool, amount not given) skipped.")
    if kind == "steel":
        r.update({"Sand (type not stated) / B": r4(sand / B), "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 200,
                  "Steel tensile strength (MPa)": 2750, "Steel elastic modulus (GPa)": 200})
        note += " Natural sand (max 2.38 mm); Type III cement."
    else:
        r.update({"SS / B (Silica sand)": r4(sand / B), "PE fiber (vol%)": 2, "PE length (mm)": 13, "PE diameter (µm)": 39,
                  "PE tensile strength (MPa)": 2570, "PE elastic modulus (GPa)": 114})
        note += " Silica sand (max 0.42 mm); Type I cement."
    r["Conversions / notes"] = note
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e48.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")
