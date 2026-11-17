"""Wave 6, agent e12: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e12.csv (99-column TEMPLATE header).
Papers: conbuildmat.2021.122263, 124157, 124453, 124742, jclepro.2020.121113, jobe.2020.101613, engstruct.2018.05.037
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


# ---------- 1) 122263: SHCC with PE fiber, pristine-fiber control only
P = {"Article Name": "Tailoring of polyethylene fiber surface by coating silane coupling agent for strain hardening cementitious composite",
     "Author": "Tianan Liu, Ruixiang Bai, Zhitao Chen, Yazhao Li, Yingzi Yang", "Year": 2021, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.122263"}
B = 779.3 + 495.9 + 141.7
r = dict(P)
r.update({"OPC / Cement": r4(779.3 / B), "FA (Fly ash)": r4(495.9 / B), "SF (Silica fume)": r4(141.7 / B), "W / B": r4(255.1 / B),
          "SS / B (Silica sand)": r4(566.8 / B), "SP / B": r4(21.2 / B), "Binder content (kg/m³)": round(B, 1),
          "PE fiber (vol%)": 1.5, "PE length (mm)": 18, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 3800,
          "PE elastic modulus (GPa)": 113, "Total fiber (vol%)": 1.5,
          "Curing method": "20 C for 24 h, demolded, then steam curing 90 C for 3 days", "Curing time (days)": 4,
          "Curing temperature (°C)": 90, "Demolding age (days)": 1, "Test age (days)": 4, "Heat curing duration (h)": 72,
          "Tensile specimen": "dumbbell (JSCE)", "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 118.32, "First-cracking strength (MPa)": 4.6, "Tensile strength (MPa)": 9.08,
          "Tensile strain capacity (%)": 4.42,
          "Source table/page": "Table 3 (mix, fc), Table 5 (tensile), sect. 2.3 (curing)",
          "Conversions / notes": "Control SHCC with pristine PE fiber; silane-coated (M-SHCC) mix skipped (surface-treated fiber). Silica sand 150 um; defoamer 0.2 kg/m3. "
                                 "VERIFY: test age not stated; 4 d = 24 h + 3 d steam curing. Specimen shape/size of compression test not stated. Binder 55/35/10 wt% stated."})
rows.append(r)

# ---------- 2) 124157: SHCC, room-temperature reference specimens (no heating)
P = {"Article Name": "Influence of matrix-modification and fiber-hybridization on high-temperature residual mechanical performance of strain-hardening cementitious composites",
     "Author": "Dhanendra Kumar, Ravi Ranade", "Year": 2021, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.124157"}
# id: (cement, slag, fa, cc, sand, water, hrwra, vma, steel, pvaLen)
mx = {"HFR-SC": (1, 2, 0, 2.2, 0, 1.65, .003, .025, 1, 8),
      "HFR-FA": (1, 0, 1.2, 0, .8, .68, .010, .018, 1, 12),
      "PVA-SC": (1, 2, 0, 2.2, 0, 1.65, .003, .025, 0, 8),
      "PVA-FA": (1, 0, 1.2, 0, .8, .68, .010, .018, 0, 12)}
res = {"HFR-SC": (47.2, 5.4, 49.9), "HFR-FA": (40.8, 5.8, 30.7), "PVA-SC": (40.1, 3.6, 46.8), "PVA-FA": (40.9, 5.2, 53.0)}
for mid, (c, sl, fa, cc, sa, w, hr, vm, stv, pl) in mx.items():
    Bm = c + sl + fa + cc
    for age in (28, 112):
        fc = res[mid][0] if age == 28 else res[mid][2]
        r = dict(P)
        r.update({"OPC / Cement": r4(c / Bm), "GGBS": r4(sl / Bm) or None, "FA (Fly ash)": r4(fa / Bm) or None,
                  "Limestone powder": r4(cc / Bm) or None, "W / B": r4(w / Bm), "SS / B (Silica sand)": r4(sa / Bm) or None,
                  "HRWR / B": r4(hr / Bm), "VMA / B": r4(vm / Bm),
                  "PVA fiber (vol%)": 2, "PVA length (mm)": pl, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
                  "PVA elastic modulus (GPa)": 42.8,
                  "Steel fiber (vol%)": stv or None, "Steel length (mm)": 25 if stv else None, "Steel diameter (µm)": 500 if stv else None,
                  "Steel tensile strength (MPa)": 1700 if stv else None, "Steel elastic modulus (GPa)": 200 if stv else None,
                  "Total fiber (vol%)": 2 + stv,
                  "Curing method": "demolded at 24 h, water 14 d, then air lab 22 C RH 50 %", "Curing temperature (°C)": 22,
                  "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": age,
                  "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "76x152", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 1 (mix), Table 3 (fibers), Table 7 (28 d, Batch A), Table 8 (112 d, Batch B), sect. 3.1 (curing)"})
        note = (f"{mid}, room-temperature reference (no heating). Mixes given as mass ratios to cement. B re-expressed as cement+slag/FA+CC powder; "
                "paper w/cm excludes CC powder. CC powder = calcium carbonate powder used as inert fine filler (mapped to limestone powder). "
                "VERIFY: HRWRA and VMA ratios assumed relative to cement mass (paper does not say); binder content (kg/m3) not given.")
        if age == 28:
            r.update({"Tensile specimen": "dogbone, 12.7 mm thick", "Tensile gauge length (mm)": 125, "Tensile test type": DIRECT,
                      "Tensile strength (MPa)": res[mid][1]})
            note += " Uniaxial tensile strength from Batch A; tensile strain at room temperature not given in a table."
        else:
            note += " Batch B (112 d), compressive strength only."
        r["Conversions / notes"] = note
        rows.append(r)

# ---------- 3) 124453: PVA mortar for 3D printing, cast mixes 2 and 3 (no activated carbon)
P = {"Article Name": "Development of fibre reinforced engineered cementitious composite using polyvinyl alcohol fibre and activated carbon powder for 3D concrete printing",
     "Author": "Yifan Zhang, Farhad Aslani", "Year": 2021, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.124453"}
Bm = 1 + 1.33 + 0.11
for mid, pv, sp, f7, f28 in (("C_PVA1%", 1.0, 0.0081, 30.0, 37.7), ("C_PVA1.5%", 1.5, 0.011, 21.4, 29.9)):
    for age, fc in ((7, f7), (28, f28)):
        r = dict(P)
        r.update({"OPC / Cement": r4(1 / Bm), "FA (Fly ash)": r4(1.33 / Bm), "SF (Silica fume)": r4(0.11 / Bm), "W / B": r4(0.65 / Bm),
                  "SS / B (Silica sand)": r4(0.89 / Bm), "SP / B": r4(sp / Bm),
                  "PVA fiber (vol%)": pv, "PVA length (mm)": 12, "PVA diameter (µm)": 39, "PVA tensile strength (MPa)": 1600,
                  "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": pv,
                  "Curing time (days)": age, "Test age (days)": age,
                  "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
                  "Source table/page": "Table 5 (mix), Table 6 (fc)",
                  "Conversions / notes": f"{mid}, cast mix (mixes with activated carbon powder and the fibre-free control skipped). Mass ratios to cement -> per binder (cement+FA+SF = 2.44). "
                                         "45/50 silica sand. VERIFY: curing method/temperature not stated (age in days of curing); SP dosage as given in Table 5 (basis assumed cement mass); "
                                         "text also mentions VMA/retarder as admixtures but none listed in Table 5 for cast mixes; PVA vol% from mix names."})
        rows.append(r)

# ---------- 4) 124742: ECC with fine silica sand control (FSS-ECC) only
P = {"Article Name": "Development of engineered cementitious composites (ECC) using artificial fine aggregates",
     "Author": "Ling-Yu Xu, Bo-Tao Huang, Jian-Guo Dai", "Year": 2021, "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2021.124742"}
r = dict(P)
r.update({"OPC / Cement": 0.8, "SF (Silica fume)": 0.2, "W / B": 0.182, "SS / B (Silica sand)": 0.298, "SP / B": 0.013,
          "PE fiber (vol%)": 2, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 100,
          "Total fiber (vol%)": 2,
          "Curing method": "covered 20 C 24 h, demolded, water 20 C for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
          "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
          "Tensile specimen": "dumbbell (JSCE)", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
          "Compressive strength (MPa)": 154.3, "First-cracking strength (MPa)": 7.5, "Tensile strength (MPa)": 11.7, "Tensile strain capacity (%)": 4.1,
          "Source table/page": "Table 5 (mix), Table 6 (results, averages)",
          "Conversions / notes": "FSS-ECC (fine silica sand, dry mass 0.298); GPA-ECC and CBA-ECC skipped (artificial aggregates). Weight ratios as given (cement 0.8 + SF 0.2 = B 1.0). "
                                 "SP given as solid content."})
rows.append(r)

# ---------- 5) jclepro 121113: ECC with glass aggregate, 0 GL control only (silica sand)
P = {"Article Name": "Mechanical performance of engineered cementitious composite incorporating glass as aggregates",
     "Author": "Adeyemi Adesina, Sreekanta Das", "Year": 2020, "DOI / URL": "https://doi.org/10.1016/j.jclepro.2020.121113"}
B = 380 + 840
for age, ft, eps in ((28, 2.99, 2.74), (90, 4.02, 3.82)):
    r = dict(P)
    r.update({"OPC / Cement": r4(380 / B), "FA (Fly ash)": r4(840 / B), "W / B": r4(305 / B), "SS / B (Silica sand)": r4(460 / B),
              "SP / B": r4(2 / B), "Binder content (kg/m³)": B,
              "PVA fiber (vol%)": 2, "PVA length (mm)": 8, "PVA diameter (µm)": 40, "PVA tensile strength (MPa)": 1600,
              "PVA elastic modulus (GPa)": 41, "Total fiber (vol%)": 2,
              "Curing method": "demolded ~24 h, water curing until test", "Curing time (days)": age, "Demolding age (days)": 1, "Test age (days)": age,
              "Tensile specimen": "dog-bone (JSCE-like)", "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 4 (mix), Table 7 (tensile)",
              "Conversions / notes": "Mix 0 GL (ultrafine silica sand USS) only; glass-aggregate mixes skipped. kg/m3 / B = 1220. PVA 26 kg/m3 = 2 vol% (stated 2 %). "
                                     "Compressive strength only in Fig. 7 (not entered). Water curing temperature not stated."})
    rows.append(r)

# ---------- 6) jobe 101613: UHPFRC steel fiber 0.5-3 vol%, cylinders at 5 d
P = {"Article Name": "Experimental relationships between steel fiber volume fraction and mechanical properties of ultra-high performance fiber-reinforced concrete",
     "Author": "Ghasem Dehghani Ashkezari, Farzan Fotouhi, Mehrdad Razmara", "Year": 2020, "DOI / URL": "https://doi.org/10.1016/j.jobe.2020.101613"}
B = 1050 + 350
cyl = {0.5: (100.2, 9.17, 119.9), 1.0: (110.8, 9.88, 126.6), 1.5: (112.0, 14.36, 140.0), 2.0: (115.2, 14.45, 163.4),
       2.5: (128.7, 14.69, 171.7), 3.0: (133.9, 16.34, 178.1)}
for v, (fc, fsp, fcube) in cyl.items():
    r = dict(P)
    r.update({"OPC / Cement": r4(1050 / B), "SF (Silica fume)": r4(350 / B), "W / B": 0.16, "M-sand / B": r4(678 / B), "SP / B": r4(42 / B),
              "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": v, "Steel length (mm)": 12, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 2850, "Total fiber (vol%)": v,
              "Curing method": "demolded 24 h, water 80 C for 4 d, then ambient to equilibrium", "Curing time (days)": 4, "Curing temperature (°C)": 80,
              "Demolding age (days)": 1, "Test age (days)": 5, "Heat curing duration (h)": 96,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "75x150", "Compressive strength (MPa)": fc,
              "Tensile strength (MPa)": fsp, "Tensile specimen": "cylinder 150x300", "Tensile test type": "splitting",
              "Source table/page": "Table 2 (mix), Table 4 (cylinder fc), Table 6 (splitting)",
              "Conversions / notes": f"Compressive strength of 100 mm cubes at same mix: {fcube} MPa (Table 5), not entered. kg/m3 / B = 1400; SP liquid (50 % conc.). "
                                     "Fiber-free reference (0 %) skipped. VERIFY: basalt crushed aggregate < 4.75 mm treated as manufactured sand (M-sand); "
                                     "tensile strength is SPLITTING (not direct); no strain."})
    rows.append(r)

# ---------- 7) engstruct 2018.05.037: UHDCC-A/B/C
P = {"Article Name": "Feasibility of using ultra-high ductility cementitious composites for concrete structures without steel rebar",
     "Author": "Kequan Yu, Lingzhi Li, Jiangtao Yu, Jianzhuang Xiao, Junhong Ye, Yichao Wang", "Year": 2018, "DOI / URL": "https://doi.org/10.1016/j.engstruct.2018.05.037"}
u = {"UA": dict(sand=601, c=936, fa=201, sl=0, sf=0, w=361, hr=4.2, age=180, desc="6 months after curing (derived 180 d)", eps=11.98, ft=6.07, fc=45.86,
                spec="cube", size="50"),
     "UB": dict(sand=474, c=592, fa=711, sl=0, sf=0, w=413, hr=5.0, age=28, desc="28 days after curing", eps=13.55, ft=4.97, fc=12.85,
                spec="cylinder", size="50x100"),
     "UC": dict(sand=700, c=500, fa=0, sl=650, sf=150, w=230, hr=25, age=28, desc="28 days after curing", eps=8.70, ft=19.20, fc=118.50,
                spec="cylinder", size="100x200")}
for mid, d in u.items():
    B = d["c"] + d["fa"] + d["sl"] + d["sf"]
    note = (f"UHDCC-{mid[1]} (kg/m3 / B). HRWR as dosed. Curing method not described (only 'after curing'). "
            "Compressive specimen shape per mix in the order given in sect. 3.1 (cube / cylinder / cylinder). ")
    if mid == "UA":
        note += "VERIFY: UA age = 6 months converted to 180 d. "
    if mid == "UB":
        note += "VERIFY: Table 1 columns Fly ash-1/Fly ash-2 for UB ambiguous (711 kg/m3 taken as fly ash; w/b 0.32 matches). "
    note += "PE length not given in text."
    r = dict(P)
    r.update({"OPC / Cement": r4(d["c"] / B), "FA (Fly ash)": r4(d["fa"] / B) or None, "GGBS": r4(d["sl"] / B) or None,
              "SF (Silica fume)": r4(d["sf"] / B) or None, "W / B": r4(d["w"] / B), "SS / B (Silica sand)": r4(d["sand"] / B),
              "SP / B": r4(d["hr"] / B), "Binder content (kg/m³)": B,
              "PE fiber (vol%)": 2, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 2900, "PE elastic modulus (GPa)": 116, "Total fiber (vol%)": 2,
              "Curing method": d["desc"], "Curing time (days)": d["age"], "Test age (days)": d["age"],
              "Compressive specimen": d["spec"], "Compressive specimen size (mm)": d["size"],
              "Tensile specimen": "dogbone, 13 mm thick", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Compressive strength (MPa)": d["fc"], "Tensile strength (MPa)": d["ft"], "Tensile strain capacity (%)": d["eps"],
              "Source table/page": "Table 1 (mix), Table 2 (PE), Table 6 (results), sect. 4.1 (ages)",
              "Conversions / notes": note})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e12.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e12.csv"))
