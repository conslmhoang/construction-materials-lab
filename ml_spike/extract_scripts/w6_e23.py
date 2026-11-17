"""Wave 6, agent e23: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e23.csv (99-column TEMPLATE header).
Papers: cemconcomp.2017.10.011, ceramint.2021.09.285, ceramint.2021.11.232, cemconres.2017.08.018
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


# ---------- 1) Hybrid steel + HSPE fibre ambient-cured geopolymer (FA + slag), fc at 28 d
P = {"Article Name": "Mechanical properties of ambient cured high strength hybrid steel and synthetic fibers reinforced geopolymer composites",
     "Author": "Musaad Zaheer Nazir Khan, Yifei Hao, Hong Hao, Faiz Uddin Ahmed Shaikh", "Year": 2018,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2017.10.011"}
FA, SL, SA, NAOH, WG = 412, 276, 1100, 117.72, 294.30
B = FA + SL
naoh_solid = NAOH * 480 / 1370           # 12 M NaOH, density assumed 1.37 g/cm3 -> 35 % NaOH
naoh_water = NAOH - naoh_solid
mixes = {"G-2": (0.50, 0.50, 0, 75.15), "G-3": (0.75, 0.75, 0, 74.66), "G-4": (1.00, 1.00, 0, 82.05),
         "G-5": (0.40, 0.40, 0.20, 68.88), "G-6": (0.80, 0, 0.20, 72.10), "G-7": (0.90, 0.90, 0.20, 72.87),
         "G-8": (0.80, 0.80, 0.40, 70.66)}
for mid, (sp, hk, pe, fc) in mixes.items():
    r = dict(P)
    r.update({"FA (Fly ash)": r4(FA / B), "GGBS": r4(SL / B), "WG / B (Water glass)": r4(WG / B), "NaOH / B": r4(naoh_solid / B),
              "NaOH molarity (M)": 12, "W / B": r4(naoh_water / B), "SS / B (Silica sand)": r4(SA / B), "Binder content (kg/m³)": B,
              "Total fiber (vol%)": round(sp + hk + pe, 2),
              "Curing method": "covered 24 h at 22 C / 50 % RH, then unwrapped in the same ambient lab environment (22 +/- 2 C, 50 +/- 5 % RH)",
              "Curing time (days)": 28, "Curing temperature (°C)": 22, "Curing RH (%)": 50, "Demolding age (days)": 1, "Test age (days)": 28,
              "Compressive specimen": "cylinder", "Compressive specimen size (mm)": "100x200", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix, fibres), Table 4 (fc), sect. 2.1-2.2 (activator, curing)",
              "Conversions / notes": f"{mid}. kg/m3 / B (FA + slag = {B}). Plain matrix G-1 skipped (no fibre). WG = D-grade sodium silicate solution 294.3 kg/m3 "
                                     "(Ms 2.0, SiO2 29.4 %, Na2O 14.7 %, H2O 55.9 %; its water not added to W/B). "
                                     "VERIFY: NaOH 117.72 kg/m3 taken as 12 M solution mass; NaOH solid 35 % (density 1.37 g/cm3 assumed) -> W/B = water of NaOH solution only; "
                                     "test age 28 d from 'at 28 days of ambient curing' (compressive tests). Silica sand 1100 kg/m3. "
                                     "Fibres: spiral steel (25 mm, 0.55 mm, 1400 MPa) / hooked-end steel (25 mm, 0.30 mm, 2500 MPa) / HSPE (12 mm, 12 um, 3500 MPa, 123 GPa); "
                                     "steel diameter and strength left empty when the two steel types are mixed."})
    st = sp + hk
    if st:
        r.update({"Steel fiber (vol%)": round(st, 2), "Steel length (mm)": 25, "Steel elastic modulus (GPa)": 200})
        if hk == 0:
            r.update({"Steel diameter (µm)": 550, "Steel tensile strength (MPa)": 1400})
    if pe:
        r.update({"PE fiber (vol%)": pe, "PE length (mm)": 12, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 3500, "PE elastic modulus (GPa)": 123})
    rows.append(r)

# ---------- 2) Red-mud alkali-activated PE composite: only the red-mud-free reference (0%Mix)
P = {"Article Name": "Mechanical properties of high ductile alkali-activated fiber reinforced composites incorporating red mud under different curing conditions",
     "Author": "Lili Kan, Fei Wang et al.", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.ceramint.2021.09.285"}
B = 44.8 + 10.3
for tag, ts, fcr, eps in [("0%RM-A", 4.79, 2.94, 1.77), ("0%RM-H", 4.00, 1.95, 4.52)]:
    r = dict(P)
    heat = tag.endswith("H")
    r.update({"GGBS": r4(44.8 / B) , "SF (Silica fume)": r4(10.3 / B), "WG / B (Water glass)": r4(13.7 / B), "NaOH / B": r4(3.0 / B),
              "Activator modulus Ms (SiO2/Na2O)": 3.2, "W / B": r4(12.6 / B), "River sand / B": r4(14.5 / B),
              "PE fiber (vol%)": 1.9, "PE length (mm)": 12, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000, "PE elastic modulus (GPa)": 110,
              "Total fiber (vol%)": 1.9, "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 70,
              "Demolding age (days)": 1, "Test age (days)": 28,
              "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": DIRECT,
              "Tensile strength (MPa)": ts, "First-cracking strength (MPa)": fcr, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 3 (mix, wt%), Table 4 (tensile), sect. 2.2 (curing)",
              "Conversions / notes": f"{tag}. Reference Mix-0%RM only (red mud mixes skipped). Mix in wt% of total, B = GGBS 44.8 + SF 10.3 = 55.1. "
                                     "Na2SiO3 solution 13.7 wt% (composition not given, only activator Ms = 3.2; its water not added to W/B); water 12.6 wt% as in Table 3. "
                                     "Compressive strength only in Fig. 8 (not entered). "
                                     "VERIFY: test age 28 d from 'curing age was 28 d'; 20 C / 70 % RH only for the first 24 h (lab), later 'room temperature'; "
                                     "PE vol% 1.9 as in Table 3."})
    if heat:
        r.update({"Curing method": "24 h lab (20 C, 70 % RH), sealed in film and oven 80 C 2 h, then ambient about 27 d", "Heat curing duration (h)": 2})
    else:
        r.update({"Curing method": "24 h lab (20 C, 70 % RH), demoulded, then air at room temperature to 28 d"})
    rows.append(r)

# ---------- 3) Steel-fibre FA-GGBFS geopolymer mortar (ST mixes), fc at 28 d
P = {"Article Name": "Influence of steel and PP fibers on mechanical and microstructural properties of fly ash-GGBFS based geopolymer composites",
     "Author": "Ramamohana Reddy Bellum et al.", "Year": 2022, "DOI / URL": "https://doi.org/10.1016/j.ceramint.2021.11.232"}
FA, SL, SA, WG, NAOH = 327.19, 140.23, 1168.55, 133.55, 53.42
B = FA + SL
naoh_solid = NAOH * 320 / 1253           # 8 M, density assumed 1.253 g/cm3 -> 25.5 % NaOH
naoh_water = NAOH - naoh_solid
for mid, vf, fc in [("ST0.5", 0.5, 55.2), ("ST1", 1.0, 56.47), ("ST1.5", 1.5, 57.7), ("ST2", 2.0, 59.64), ("ST2.5", 2.5, 61.5)]:
    r = dict(P)
    r.update({"FA (Fly ash)": r4(FA / B), "GGBS": r4(SL / B), "WG / B (Water glass)": r4(WG / B), "NaOH / B": r4(naoh_solid / B),
              "NaOH molarity (M)": 8, "W / B": r4(naoh_water / B), "River sand / B": r4(SA / B), "Binder content (kg/m³)": r4(B),
              "Steel fiber (vol%)": vf, "Steel length (mm)": 6, "Steel diameter (µm)": 150, "Steel tensile strength (MPa)": 2050, "Total fiber (vol%)": vf,
              "Curing method": "ambient curing (temperature not stated)", "Curing time (days)": 28, "Test age (days)": 28,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 4 (fc 28 d), sect. 2.1-2.3",
              "Conversions / notes": f"{mid}. Control GC and PP mixes skipped. kg per Table 3 / B (FA + GGBFS = {B:.2f}). Na2SiO3 solution 133.55 (27.8 % SiO2, 8 % Na2O, 64.5 % H2O) "
                                     "as WG (water not added); NaOH 53.42 = 8 M solution (Na2SiO3 : NaOH = 2.5 : 1). "
                                     "VERIFY: fibre volume fraction nominal (0.5-2.5 vol% stated in text) although the kg amounts in Table 3 correspond to 0.5-2.5 wt% of binder (steel 2.34-11.69 kg); "
                                     "NaOH solid 25.5 % (8 M, density 1.253 assumed) so W/B = water of NaOH solution only (low, 0.085); 7-d strength only in figure."})
    rows.append(r)

# ---------- 4) UHPC with 2 vol% steel fibre, reference mixture LWS00 (no lightweight sand)
P = {"Article Name": "Effects of saturated lightweight sand content on key characteristics of ultra-high-performance concrete",
     "Author": "Weina Meng, Kamal Khayat", "Year": 2017, "DOI / URL": "https://doi.org/10.1016/j.cemconres.2017.08.018"}
C, FAC, SFm, MS, NS = 663, 367, 42, 308, 703
B = C + FAC + SFm
for age, fc in [(1, 80), (7, 122), (28, 130), (91, 138)]:
    r = dict(P)
    r.update({"OPC / Cement": r4(C / B), "FA (Fly ash)": r4(FAC / B), "SF (Silica fume)": r4(SFm / B), "W / B": 0.20,
              "River sand / B": r4(NS / B), "Sand (type not stated) / B": r4(MS / B), "SP / B": r4(0.01 / 0.23), "Binder content (kg/m³)": B,
              "Steel fiber (vol%)": 2.0, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Steel tensile strength (MPa)": 1900,
              "Steel elastic modulus (GPa)": 203, "Total fiber (vol%)": 2.0,
              "Curing method": "wet burlap + plastic sheet, demoulded after 1 d, lime-saturated water at room temperature until test",
              "Curing time (days)": age, "Demolding age (days)": 1, "Test age (days)": age,
              "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": fc,
              "Source table/page": "Table 2 (mix, LWS00), Table 3 (fc), sect. 2.2, 3.1",
              "Conversions / notes": f"Reference mixture LWS00 only (LWS mixes skipped: expanded shale lightweight sand). kg/m3 / B (cement + class C fly ash + SF = {B}). "
                                     "Sand = masonry sand 308 (type-not-stated column) + Missouri river sand 703. Type III cement. "
                                     "VERIFY: SP/B = HRWR solid 1 % of binder / 0.23 solids = 4.35 % liquid as dosed; air de-training admixture 0.8 % of binder (defoamer, not entered). "
                                     "Steel fibre strength '1.9' read as 1.9 GPa; fibre 2 vol% from text."})
    rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e23.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows;", df["DOI / URL"].nunique(), "papers")
