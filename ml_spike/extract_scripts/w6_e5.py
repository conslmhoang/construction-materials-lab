"""Wave 6, agent e5: Elsevier full texts. Only 10.1016/j.conbuildmat.2022.126879 qualified (1 row)."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
add = os.path.join(here, "..", "additions")
out_dir = os.path.join(here, "..", "additions_v2")
cols = list(pd.read_csv(os.path.join(add, "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
r = {"Article Name": "Theoretical modification of the laboratory-determined tensile stress-strain relationship of strain hardening cementitious composites (SHCCs) for large-scale specimens",
     "Author": "Chang Wu, Jie Yao, Mingkang Chen, Chenhua Jin, Christopher K.Y. Leung", "Year": 2022,
     "DOI / URL": "https://doi.org/10.1016/j.conbuildmat.2022.126879",
     "OPC / Cement": 0.18, "FA (Fly ash)": 0.8, "SF (Silica fume)": 0.02, "W / B": 0.22,
     "SS / B (Silica sand)": 0.2, "PVA fiber (vol%)": 2, "PVA length (mm)": 12, "PVA diameter (µm)": 39,
     "Total fiber (vol%)": 2, "Curing method": "standard maintenance room, 28 d", "Curing time (days)": 28,
     "Test age (days)": 28, "Tensile specimen": "dog bone (W = 30 mm)", "Tensile test type": "direct (uniaxial)",
     "First-cracking strength (MPa)": 2.5, "Tensile strength (MPa)": 3.75, "Tensile strain capacity (%)": 2,
     "Source table/page": "Sect. 4 text (mix, 28 d curing), Table 6 (tensile), Table 1 (fiber)",
     "Conversions / notes": "VERIFY: mass ratio text '0.18:0.02:0.8:0.2:0.22' read as cement:SF:FA:silica sand:water (order from the sentence). "
                            "Superplasticizer used, dosage not stated. PVA diameter 39 um (Table 1; sect. 4 text says 40 um). "
                            "Table 6 values come from the companion dog-bone tests of the beam study; same mix as the tensile tests. "
                            "Compressive strength (cube 50.5 MPa) not entered: test age not stated."}
df = pd.DataFrame([r]).reindex(columns=cols)
df.to_csv(os.path.join(out_dir, "w6_e5.csv"), index=False, encoding="utf-8-sig")
print(len(df), "rows")
