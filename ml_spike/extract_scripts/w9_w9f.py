# w9f: all 4 papers rejected (see additions_v2/w9_w9f_rejected.txt); writes a header-only CSV.
import pandas as pd
cols = list(pd.read_csv(r"ml_spike/additions/TEMPLATE.csv", nrows=0, encoding="utf-8-sig").columns)
pd.DataFrame(columns=cols).to_csv(r"ml_spike/additions_v2/w9_w9f.csv", index=False, encoding="utf-8-sig")
