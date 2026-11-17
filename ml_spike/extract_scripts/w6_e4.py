"""Wave 6, agent e4: rows from Elsevier full texts (Papers/Paper news/elsevier_txt).
Writes ml_spike/additions_v2/w6_e4.csv (99-column TEMPLATE header).
Papers: 10.1016/j.cemconcomp.2021.104133, 2022.104676, 2023.105051, 2024.105598
"""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
rows = []

# ---------------------------------------------------------- 1) UD-EGC (104133)
P = {"Article Name": "Ultra-ductile behavior of fly ash-based engineered geopolymer composites with a tensile strain capacity up to 13.7%",
     "Author": "Huy Hoang Nguyen, Quang-Hieu Luong, Jeong-Il Choi, Ravi Ranade, Victor C. Li, Bang Yeon Lee", "Year": 2021,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2021.104133"}
# mix: (FA, SH(NaOH), SMP, water, SP, VMA, defoamer, fc, fcr, ft, eps); ratios of total binder (FA+SH+SMP = 1)
mx = {"UD-EGC10": (.80, .10, .10, .345, .009, .001, .001, 15.7, 2.13, 7.11, 12.49),
      "UD-EGC15": (.75, .10, .15, .345, .003, .001, .001, 19.3, 3.70, 6.79, 13.68),
      "UD-EGC20": (.70, .10, .20, .345, .003, .001, .001, 22.4, 4.63, 8.10, 12.26),
      "UD-EGC25": (.65, .10, .25, .345, 0, .005, .001, 16.2, 4.99, 7.18, 10.88)}
for mid, (fa, sh, smp, w, sp, vma, df, fc, fcr, ft, eps) in mx.items():
    r = dict(P)
    r.update({"FA (Fly ash)": 1.0, "NaOH / B": round(sh / fa, 4), "SSM / B (Na2SiO3 anhydrous)": round(0.575 * smp / fa, 4),
              "W / B": round((w + 0.425 * smp) / fa, 4), "SP / B": round(sp / fa, 4) if sp else None, "VMA / B": round(vma / fa, 4),
              "PE fiber (vol%)": 1.75, "PE length (mm)": 18, "PE diameter (µm)": 12, "PE tensile strength (MPa)": 2700,
              "PE elastic modulus (GPa)": 88, "Total fiber (vol%)": 1.75,
              "Curing method": "5 d air 23 C, then oven 80 C 36 h, then curing chamber 23 C to 28 d",
              "Curing time (days)": 28, "Curing temperature (°C)": 23, "Demolding age (days)": 5, "Test age (days)": 28,
              "Heat curing duration (h)": 36, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dumbbell", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "First-cracking strength (MPa)": fcr, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Compressive strength (MPa)": fc,
              "Source table/page": "Table 1 (mix), Table 4 (tensile), Table 5 + text sect. 3.1 (fc)",
              "Conversions / notes": f"{mid}. Paper binder = FA + SH + SMP (mass ratios of total, water 0.345 for all, w/b stated 0.345); re-expressed per FA (B = fly ash): NaOH/B = SH/FA. "
                                     "SMP (sodium metasilicate pentahydrate) x0.575 as anhydrous, 0.425 of it added to water. SH = 7.2 M NaOH solution (its water assumed inside the 0.345). "
                                     "Defoamer 0.001 of total binder. PE 1.75 vol% listed in first mix row only, assumed for all. "
                                     "VERIFY: text states fc of UD-EGC20 = 22.4 MPa (+42.6 % vs EGC10, +16.1 % vs EGC15, EGC25 27.6 % lower); fc of the other mixes derived from these percentages (consistent with Table 5 ratios fts/fc); fc itself is in Fig. 4."})
    rows.append(r)

# ---------------------------------------------------------- 2) FSS-ECC control (104676)
r = {"Article Name": "Enhancing long-term tensile performance of Engineered Cementitious Composites (ECC) using sustainable artificial geopolymer aggregates",
     "Author": "Ling-Yu Xu, Bo-Tao Huang, Lan-Ping Qian, Jian-Guo Dai", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2022.104676"}
r.update({"OPC / Cement": 0.8, "SF (Silica fume)": 0.2, "W / B": 0.171, "SS / B (Silica sand)": 0.248, "SP / B": 0.013,
          "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 24, "PE tensile strength (MPa)": 3000,
          "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": 2.0,
          "Curing method": "water 23 C for 28 d", "Curing time (days)": 28, "Curing temperature (°C)": 23, "Test age (days)": 28,
          "Compressive specimen": "cube", "Compressive specimen size (mm)": "50", "Tensile specimen": "dumbbell",
          "Tensile test type": "direct (uniaxial)", "Compressive strength (MPa)": 152.4, "Tensile strength (MPa)": 12.9,
          "Tensile strain capacity (%)": 4.20, "Source table/page": "Table 1 (mix), Table 4 (short-term values), sect. 2.3 (curing)",
          "Conversions / notes": "FSS-ECC short-term (28 d) only; accelerated-aging (60 C hot water) values and GPA mixes (artificial geopolymer aggregate) not used. "
                                 "Weight ratios of binder (cement + SF = 1); dry fine silica sand 0.248; SP in solid. Tensile 'ductility' 4.20 % entered as strain capacity. "
                                 "Gauge length and demolding age not stated."})
rows.append(r)

# ---------------------------------------------------------- 3) FA-ECC reference mixes (105051)
P = {"Article Name": "Engineered cementitious composites (ECC) with a high volume of volcanic ash: Rheological, mechanical, and micro performance",
     "Author": "He Zhu, Wei-Hsiu Hu, Mohammed Mehthel, Thibault Villette, Oscar Salazar Vidal, Waleed N. Nasser, Victor C. Li", "Year": 2023,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2023.105051"}
for mid, opc, fa, wat, wr, fc, ft, eps in [("FA06", 800, 480, 320, 2.0, 54.1, 7.0, 6.8), ("FA12", 600, 720, 330, 1.8, 53.9, 7.7, 6.6),
                                          ("FA22", 400, 880, 320, 1.8, 39.2, 5.3, 5.4)]:
    b = opc + fa
    r = dict(P)
    r.update({"OPC / Cement": round(opc / b, 4), "FA (Fly ash)": round(fa / b, 4), "W / B": round(wat / b, 3),
              "Dune sand / B": 0.3, "SP / B": round(wr / b, 5), "Binder content (kg/m³)": b,
              "PE fiber (vol%)": round(20 / 970 * 100, 2), "PE length (mm)": 12, "PE diameter (µm)": 20, "PE tensile strength (MPa)": 3000,
              "PE elastic modulus (GPa)": 100, "Total fiber (vol%)": round(20 / 970 * 100, 2),
              "Curing method": "air 20 C, RH 40 %", "Curing time (days)": 28, "Curing temperature (°C)": 20, "Curing RH (%)": 40,
              "Test age (days)": 28, "Compressive specimen": "cube", "Compressive specimen size (mm)": "50",
              "Tensile specimen": "dogbone", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
              "Compressive strength (MPa)": fc, "Tensile strength (MPa)": ft, "Tensile strain capacity (%)": eps,
              "Source table/page": "Table 2 (mix), Table 4 (WR), Table 5 (tensile), sect. 3.2.1 text (fc), sect. 2.2 (curing)",
              "Conversions / notes": f"{mid} (conventional FA-ECC reference; volcanic-ash mixes skipped). kg/m3 divided by binder {b}. Desert sand 0.3 of binder (stored as dune sand). "
                                     "VERIFY: PE 20 kg/m3 -> vol% with 970 kg/m3 (derived). WR (MasterGlenium 7920) stored as SP, no HPMC in FA mixes. Tensile ductility = deformation at peak load / gauge length."})
    rows.append(r)

# ---------------------------------------------------------- 4) cementless SHCC reference (105598)
b = 792.8 + 198.2 + 98.0
r = {"Article Name": "Novel treatment method of coal bottom ash for strain-hardening alkali-activated composite",
     "Author": "Min-Chang Kang, Suhawn Ju, Taekgeun Oh, Doo-Yeol Yoo, Sukhoon Pyo", "Year": 2024,
     "DOI / URL": "https://doi.org/10.1016/j.cemconcomp.2024.105598"}
r.update({"GGBS": round(792.8 / b, 4), "FA (Fly ash)": round(198.2 / b, 4), "SF (Silica fume)": round(98.0 / b, 4),
          "NaOH / B": round(137.4 / b, 4), "W / B": round(429.2 / b, 3), "SS / B (Silica sand)": round((137 + 58.7) / b, 3),
          "Binder content (kg/m³)": round(b, 1), "PE fiber (vol%)": 2.0, "PE length (mm)": 18, "PE diameter (µm)": 31,
          "PE tensile strength (MPa)": 3000, "Total fiber (vol%)": 2.0,
          "Curing method": "7 d room temp covered, demolded, oven 80 C 24 h, then 7 d room temp", "Curing temperature (°C)": 80,
          "Heat curing duration (h)": 24, "Demolding age (days)": 7, "Test age (days)": 15,
          "Tensile specimen": "dog-bone", "Tensile gauge length (mm)": 80, "Tensile test type": "direct (uniaxial)",
          "Tensile strength (MPa)": 3.43, "Tensile strain capacity (%)": 1.07,
          "Source table/page": "Table 4 (mix, Ref), sect. 4.2 text (ft, strain), sect. 3.1 (curing)",
          "Conversions / notes": "Ref mix only (no coal bottom ash; CBA mixes skipped). kg/m3 divided by B = GGBS + FA + SF (silica fume is listed in the activator column as silica source; included in B so fractions sum to 1). "
                                 "Sand = No.6 137 + No.8 58.7. NaOH 137.4 kg/m3. VERIFY: test age 15 d derived (7 d + 1 d oven + 7 d); SP content '7%' in Table 4 unclear, SP not entered; PE diameter 30-32 um (31 used); "
                                 "fc only in Fig. 9 (text: Ref < 60 MPa), not entered."})
rows.append(r)

df = pd.DataFrame(rows).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e4.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows ->", os.path.join(out_dir, "w6_e4.csv"))
