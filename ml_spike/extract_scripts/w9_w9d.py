"""w9d: 5 Elsevier papers checked; only jobe_2021_103668 (GS(E), 7 d) qualifies. See w9_w9d_rejected.txt."""
import pandas as pd
cols = list(pd.read_csv(r"ml_spike/additions/TEMPLATE.csv", nrows=0).columns)
row = {
 "Article Name": "Utilization of lime-based alternative hydration to develop cementless UHPFRC",
 "Author": "Sung-Hoon Kang, Hyunuk Kang, Nankyoung Lee, Yang-Hee Kwon, Juhyuk Moon",
 "Year": 2021, "DOI / URL": "https://doi.org/10.1016/j.jobe.2021.103668",
 "GGBS": 0.56, "SF (Silica fume)": 0.20, "Ca(OH)2 / B": 0.24,
 "W / B": 0.20, "SS / B (Silica sand)": 0.88, "SP / B": 0.0096,
 "Steel fiber (vol%)": 2, "Steel length (mm)": 13, "Steel diameter (µm)": 200, "Total fiber (vol%)": 2,
 "Curing method": "sealed at 20 °C, steam curing at 60 °C for 3 days beginning the day after casting (sample GS(E)), then ambient 20 °C",
 "Curing time (days)": 7, "Curing temperature (°C)": 60, "Test age (days)": 7, "Heat curing duration (h)": 72,
 "Compressive strength (MPa)": 123,
 "Source table/page": "Table 2 (mix), Sec. 3.2 text (fc 123 MPa at 7 d)",
 "Conversions / notes": "Cementless binder B = GGBFS 56 + hydrated lime 24 + SF 20 (wt% of binder, Table 2; GGBS and SF as fractions of B, hydrated lime as Ca(OH)2 / B = 0.24; hydrated lime is 82.7% Ca(OH)2 by TG, value kept as dosed). Fine aggregate 88 wt% (silica sand), water 20 wt%, SP 0.96 wt% (solid content, not liquid). Steel fiber 2 vol% of mortar, 13 x 0.2 mm; tensile strength given only as >2500 MPa (left blank). fc = 'maximum strength of 123 MPa at 7 days' stated in text (Sec. 3.2); same stated as maintained to 91 d, so no 91 d row. Fc figure-only elsewhere (Fig. 4). Curing: ambient sealed 20 °C + 60 °C 3 d from the day after casting; strictly curing described as 'ambient curing including elevated temperature'. Cube size not stated in text (ASTM C109 cited).",
}
pd.DataFrame([row]).reindex(columns=cols).to_csv(r"ml_spike/additions_v2/w9_w9d.csv", index=False, encoding="utf-8-sig")
