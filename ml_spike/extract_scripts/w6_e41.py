"""Wave 6, agent e41: rows from Elsevier full texts. Writes ml_spike/additions_v2/w6_e41.csv
Papers: conbuildmat.2024.136473, 2025.141594, 2026.146380, 2026.146654"""
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


# 1) Zhang et al. 2024: FA/GGBS engineered geopolymer composite, control and Na2SO4 (Table 2, stage 1)
P = paper("Setting time and mechanical properties of chemical admixtures modified FA/GGBS-based engineered geopolymer composites",
          "Yi Zhang, Wen-hua Liu, Ming-hui Liu et al.", 2024, "10.1016/j.conbuildmat.2024.136473")
for nm, na2so4, fc, ts, eps in [("Control", 0, 41, 5.42, 5.34), ("Anhydrous Na2SO4 3 %", 0.03, 49, 4.62, 6.08)]:
    r = dict(P)
    r.update({"FA (Fly ash)": 0.6, "GGBS": 0.4, "WG / B (Water glass)": r4(0.4 * 2 / 3), "NaOH molarity (M)": 8,
              "NaOH / B": 0.034, "W / B": 0.315, "VMA / B": 0.00015,
              "PE fiber (vol%)": 2, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2800,
              "Total fiber (vol%)": 2,
              "Curing method": "room temperature 1 d in mould, demoulded, curing box up to 28 d (temperature/RH not stated)",
              "Curing time (days)": 28, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "70.7",
              "Tensile specimen": "uniaxial tensile (JSCE), 70.7 mm section, 60 mm gauge", "Tensile gauge length (mm)": 60,
              "Tensile test type": DIRECT,
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ts, "Tensile strain capacity (%)": eps,
              "Source table/page": "Sect. 2.2.1 (mix), Table 2 (fc, ts, strain)"})
    if na2so4:
        r["Na2SO4 / B"] = na2so4
    r["Conversions / notes"] = (
        f"{nm}. Precursor B = FA 0.6 + GGBS 0.4. VERIFY: activator:precursor = 1:0.4 and NaOH:Na2SiO3 = 1:2 (by weight of solutions) -> "
        "WG / B = 0.4 x 2/3 (water glass solution as dosed, modulus 3.3); NaOH / B = 0.4 x 1/3 x ~0.256 (8 M NaOH solution, solids fraction ~25.6 wt%, derived by me); "
        "w/b 0.315 as stated by the paper (not stated whether it includes water of the activator solutions). Thickener 0.015 % of precursor entered as VMA / B. "
        "Test age VERIFY: 'curing box for up to 28 days', 28 d taken. Table 6 repeats the Control with slightly different values (40.1 / 2.78 / 5.41 / 5.37); Table 2 values used for both rows. "
        "Other chemical admixtures of the paper skipped (not in the 21).")
    rows.append(r)

# 2) Cao et al. 2025: PVA-ECC, salt freeze-thaw; ECC-0 = 0 cycles
P = paper("Durability evaluation of engineered cementitious composite subjected to salt freeze-thaw cycles",
          "Jincheng Cao, Haipeng Lei, Fangwen Wu, Wenrui Wang, Lanqing He, Zirun Li et al.", 2025, "10.1016/j.conbuildmat.2025.141594")
B = 370 + 864
r = dict(P)
r.update({"OPC / Cement": r4(370 / B), "FA (Fly ash)": r4(864 / B), "W / B": r4(296 / B), "Sand (type not stated) / B": r4(444 / B),
          "SP / B": r4(2.6 / B), "Binder content (kg/m³)": B,
          "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1620,
          "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2,
          "Curing method": "demoulded after 48 h, curing box 20 +/- 2 C, 95 +/- 5 % RH for 28 d", "Curing time (days)": 28,
          "Curing temperature (°C)": 20, "Curing RH (%)": 95, "Demolding age (days)": 2, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "100",
          "Compressive strength (MPa)": 51.62, "Source table/page": "Table 1 (mix), Table 4 (ECC-0 peak strength), sect. 2.2",
          "Conversions / notes": f"ECC-0 = specimens with 0 salt freeze-thaw cycles (reference). kg/m3 / B (cement + FA = {B}). "
                                 "Water reducer entered as SP / B. VERIFY: test age 28 d derived from stated 28 d curing."})
rows.append(r)

# 3) Lee et al. 2026: UHPC steel fibre, quasi-static (S1) direct tension + 28 d fc
P = paper("Dynamic tensile behavior of ultra-high performance concrete reinforced with steel fibers under quasistatic to high strain rates",
          "Ming-Hui Lee, Yuan-Jung Hsu, Huang Hsing Pan, Yi-Chun Lai, You-Shen Cheng", 2026, "10.1016/j.conbuildmat.2026.146380")
B = 607 + 607 + 303
for nm, vf, fc, ts, ics, ps in [("F1", 1, 160.1, 6.80, 5.44, 0.38), ("F2", 2, None, 7.71, 6.10, 0.40),
                                ("F3", 3, 192.3, 8.86, 7.59, 0.50)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(607 / B), "GGBS": r4(607 / B), "SF (Silica fume)": r4(303 / B), "W / B": r4(231 / B),
              "SS / B (Silica sand)": r4(561 / B), "SP / B": r4(18 / B), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": vf, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2800,
              "Total fiber (vol%)": vf,
              "Curing method": "24 h room temperature in mould, then water 90 C for 72 h, then air until 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 90, "Demolding age (days)": 1, "Test age (days)": 28,
              "Heat curing duration (h)": 72, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dog-bone", "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ts, "First-cracking strength (MPa)": ics, "Tensile strain capacity (%)": ps,
              "Source table/page": "Table 1 (mix), sect. 3.2 (fc), Table 3 (S1: PCS, ICS, PS)"})
    if fc is not None:
        r["Compressive strength (MPa)"] = fc
    r["Conversions / notes"] = (
        f"{nm}. kg/m3 / B (cement + GGBFS + silica fume = {B}); paper states w/b 0.19, which equals water / (cement + GGBFS); here W/B uses all three. "
        "Sand = quartz sand (kept as sand). Steel fibre 13 mm x 0.2 mm straight. Tensile = quasi-static rate S1 (1.43e-6 1/s) of the strain-rate series; "
        "tensile strength = peak cracking strength PCS, first cracking = ICS, strain = PS (VERIFY: taken as strain at peak stress). "
        + ("Compressive strength of F2 not given in text (only F0, F1, F3); left empty. " if fc is None else "")
        + "F0 (no fibre) skipped.")
    rows.append(r)

# 4) Tao et al. 2026: ECC with GGBFS filler replacing water, 28 d fc
P = paper("Regulating interface crack path between Engineered Cementitious Composites (ECC) and solid substrate",
          "Jiacheng Tao, Duo Zhang et al.", 2026, "10.1016/j.conbuildmat.2026.146654")
for nm, gg, wat, hr, fc in [("ECC-GGBFS 15 %", 201, 393, 4.2, 30.5), ("ECC-GGBFS 20 %", 268, 370, 6.8, 39.3),
                            ("ECC-GGBFS 25 %", 335, 347, 8.5, 42.1)]:
    B = 315 + 1007 + gg
    r = dict(P)
    r.update({"OPC / Cement": r4(315 / B), "FA (Fly ash)": r4(1007 / B), "GGBS": r4(gg / B), "W / B": r4(wat / B),
              "HRWR / B": r4(hr / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1560,
              "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2,
              "Curing method": "24 h in mould, then saturated Ca(OH)2 solution at 20 +/- 5 C for 28 d", "Curing time (days)": 28,
              "Curing temperature (°C)": 20, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive strength (MPa)": fc, "Source table/page": "Table 2 (mix), sect. 3.2 (28-d fc)",
              "Conversions / notes": f"{nm}. kg/m3 / B (OPC + FA + GGBFS = {B}); no sand. VERIFY: PVA 26 kg/m3 -> 2.0 vol% with SG 1.3 (volume % not stated in text). "
                                     "Tensile curves only in Fig. 4 (no strain value in text); fc only. Benchmark (no filler) and ground-quartz mixes skipped (no fc / QP)."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
assert list(df.columns) == cols
df.to_csv(os.path.join(out_dir, "w6_e41.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")
