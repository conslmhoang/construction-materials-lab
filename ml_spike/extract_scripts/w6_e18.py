"""Wave 6, agent e18: rows from Elsevier full texts. Writes additions_v2/w6_e18.csv (99-column header)."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []
DIRECT = "direct (uniaxial)"
r4 = lambda x: round(x, 4)

# 1) UHPC steel wool, only SW-0 (no steel wool) composite, fc stated in text
P = {"Article Name": "On enhancing the mechanical behavior of ultra-high performance concrete through multi-scale fiber reinforcement",
     "Author": "Ketan Ragalwar, William F. Heard, Brett A. Williams, Dhanendra Kumar, Ravi Ranade", "Year": 2019,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2019.103422"}
B = 1.9
r = dict(P)
r.update({"OPC / Cement": r4(1 / B), "SF (Silica fume)": r4(.3 / B), "GGBS": r4(.6 / B), "W / B": 0.21, "SP / B": r4(.029 / B),
          "M-sand / B": r4(1.72 / B), "Steel fiber (vol%)": 2.0, "Steel length (mm)": 30, "Steel diameter (µm)": 550,
          "Steel tensile strength (MPa)": 1345, "Steel elastic modulus (GPa)": 210, "Total fiber (vol%)": 2.0,
          "Curing method": "sealed moist 24 h, then water 90 C 4 d + air 90 C 2 d", "Curing time (days)": 7, "Curing temperature (°C)": 90,
          "Demolding age (days)": 1, "Test age (days)": 7, "Heat curing duration (h)": 144, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "51", "Compressive strength (MPa)": 130,
          "Source table/page": "Table 1 (mix SW-0), text sect. 4.2.1 (fc composite SW-0 = 130 MPa)",
          "Conversions / notes": "Ratios per cement 1 / SF 0.3 / slag 0.6 re-expressed per B = 1.9; paper's w/cm 0.21 used as W/B. "
          "Sand = washed manufactured sand. Hooked fibers 0.28 mass ratio = 2 vol% (paper). Steel-wool mixes skipped. No direct tension test. fc of SW-0 from text only."})
rows.append(r)

# 2) UHPGC steel fiber, Table 4 (28 d standard curing)
P = {"Article Name": "Development of ultra-high performance geopolymer concrete (UHPGC): Influence of steel fiber on mechanical properties",
     "Author": "Yiwei Liu, Zuhua Zhang, Caijun Shi, Deju Zhu, Ning Li, Yulin Deng", "Year": 2020,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2020.103670"}
B = 905.0
fib = {"SM": (8, 120, 2500), "SL": (13, 120, 2500), "SW": (13, 200, 2850)}
t4 = {"SM1": 142.1, "SM2": 158.9, "SM3": 168.5, "SL1": 145.9, "SL2": 161.6, "SL3": 170.4, "SW1": 131.5, "SW2": 141.6, "SW3": 150.8}
for mid, fc in t4.items():
    L, d, ts = fib[mid[:2]]
    v = int(mid[2])
    r = dict(P)
    r.update({"GGBS": r4(688 / B), "FA (Fly ash)": r4(172 / B), "SF (Silica fume)": r4(45 / B), "NaOH / B": r4(45 / B),
              "WG / B (Water glass)": r4(314 / B), "W / B": r4(97 / B), "River sand / B": r4(905 / B), "Na2O / B": 0.07,
              "Activator modulus Ms (SiO2/Na2O)": 1.5, "Binder content (kg/m³)": B, "Steel fiber (vol%)": v, "Steel length (mm)": L,
              "Steel diameter (µm)": d, "Steel tensile strength (MPa)": ts, "Total fiber (vol%)": v,
              "Curing method": "20 C covered 24 h, demoulded, 20 C RH 100% 27 d", "Curing time (days)": 28, "Curing temperature (°C)": 20,
              "Curing RH (%)": 100, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive strength (MPa)": fc,
              "Source table/page": "Table 3 (mix), Table 2 (fibres), Table 4 (fc 28 d)",
              "Conversions / notes": f"{mid}. B = slag+FA+SF = 905 kg/m3. W/B = free water 97/905 (paper states W/B 0.32 incl. water of water glass; "
              "WG water 64.5% x 314 = 202.5 kg/m3, WG = 8.35% Na2O + 27.15% SiO2); Na2O 7%, Ms 1.5 as stated. Steel vol% as stated (1/2/3). "
              "Mixes SS/H/C and steam-cured values have no numeric fc in text, skipped. No direct tension test."})
    rows.append(r)

# 3) 3D printing GLH-ECC, E1 cast
P = {"Article Name": "Combined printable and mechanical analysis of 3D-printed green high-strength, lightweight engineered cementitious composites",
     "Author": "Hongxiang Gou, Massoud Sofi, Zipeng Zhang, Mintao Zhu, Hongbo Zhu, Priyan Mendis", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2024.105506"}
r = dict(P)
r.update({"OPC / Cement": .45, "SF (Silica fume)": .1, "FA (Fly ash)": .45, "W / B": .18, "SS / B (Silica sand)": .3, "SP / B": .01,
          "PE fiber (vol%)": 1.2, "PE length (mm)": 12, "PE diameter (µm)": 40, "PE tensile strength (MPa)": 1600,
          "PE elastic modulus (GPa)": 38, "Total fiber (vol%)": 1.2,
          "Curing method": "in situ 24 h then standard curing room 20 C RH 95%", "Curing temperature (°C)": 20, "Curing RH (%)": 95,
          "Test age (days)": 28, "Tensile test type": DIRECT, "Tensile strength (MPa)": 10.26, "First-cracking strength (MPa)": 5.52,
          "Tensile strain capacity (%)": 2.2, "Source table/page": "Table 6 (E1), Table 5, Table 18 (E1-Cast)",
          "Conversions / notes": "VERIFY: test age 28 d (text: cubes extracted after 28 d; tensile age assumed same). QS = quartz sand taken as silica sand, mass ratio 0.3. "
          "E1 = mix without lightweight filler (LSF), cast control only; printed specimens and LSF mixes skipped. FVC 1.2 vol% as stated. fc of E1 only in figure, not entered."})
rows.append(r)

# 4) ECC, unheated 28 d reference
P = {"Article Name": "Specimen size effect on the residual properties of engineered cementitious composites subjected to high temperatures",
     "Author": "Tahir Kemal Erdem", "Year": 2014, "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2013.09.019"}
B = 558 + 669
r = dict(P)
r.update({"OPC / Cement": r4(558 / B), "FA (Fly ash)": r4(669 / B), "W / B": r4(326 / B), "SS / B (Silica sand)": r4(446 / B),
          "HRWR / B": r4(2.3 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0, "PVA length (mm)": 8, "PVA diameter (µm)": 39,
          "PVA tensile strength (MPa)": 1620, "PVA elastic modulus (GPa)": 42.8, "Total fiber (vol%)": 2.0, "Test age (days)": 28,
          "Tensile specimen": "coupon 152x76x13", "Tensile test type": DIRECT, "Tensile strength (MPa)": 5.1, "Tensile strain capacity (%)": 2.7,
          "Source table/page": "Table 1 (mix, 28 d tensile), sect. 2",
          "Conversions / notes": "Unheated ECC only. PVA 26 kg/m3 / 1300 = 2.0 vol%. Curing method not stated in text. fc of unheated ECC not given as number."})
rows.append(r)

# 5) TiO2-ECC, 0% TiO2 control
P = {"Article Name": "Self-cleaning engineered cementitious composites", "Author": "Aiqin Zhao, Jinglei Yang, En-Hua Yang", "Year": 2015,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2015.09.007"}
B = 1556
r = dict(P)
r.update({"OPC / Cement": 1.0, "W / B": r4(479 / B), "SP / B": r4(1.47 / B), "Binder content (kg/m³)": B, "PVA fiber (vol%)": 2.0,
          "PVA length (mm)": 12, "PVA diameter (µm)": 40, "Total fiber (vol%)": 2.0,
          "Curing method": "demoulded 1 d, laboratory air 25 C RH 65% to 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 25,
          "Curing RH (%)": 65, "Demolding age (days)": 1, "Test age (days)": 28, "Compressive specimen": "cube",
          "Compressive specimen size (mm)": "50", "Compressive strength (MPa)": 66.53,
          "Source table/page": "Table 1 (0% TiO2 mix), Table 2 (fc 28 d)",
          "Conversions / notes": "White Portland cement type I, no sand. Only the 0% TiO2 mix kept (nano TiO2 not allowed). Tensile strain in paper is back-calculated from flexure, not direct, not entered."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e18.csv"), index=False, encoding="utf-8-sig")
print(df.shape)
