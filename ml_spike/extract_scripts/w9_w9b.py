# w9b: all 4 papers rejected (see additions_v2/w9_w9b_rejected.txt); writes header-only CSV.
import pandas as pd
cols = list(pd.read_csv(r"ml_spike/additions/TEMPLATE.csv", nrows=0).columns)
pd.DataFrame(columns=cols).to_csv(r"ml_spike/additions_v2/w9_w9b.csv", index=False, encoding="utf-8-sig")
