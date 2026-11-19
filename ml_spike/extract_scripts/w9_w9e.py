# w9e: all 5 papers rejected (see additions_v2/w9_w9e_rejected.txt); writes a header-only CSV.
import pandas as pd
cols = list(pd.read_csv(r"ml_spike/additions/TEMPLATE.csv", nrows=0, encoding="utf-8-sig").columns)
pd.DataFrame(columns=cols).to_csv(r"ml_spike/additions_v2/w9_w9e.csv", index=False, encoding="utf-8-sig")
