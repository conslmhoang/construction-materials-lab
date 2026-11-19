# w8e2: all 6 assigned papers rejected (see w8_w8e2_rejected.txt); writes a header-only CSV.
import pandas as pd
D = r"ml_spike/additions_v2/"
cols = list(pd.read_csv("ml_spike/additions/TEMPLATE.csv", nrows=0).columns)
pd.DataFrame(columns=cols).to_csv(D + "w8_w8e2.csv", index=False, encoding="utf-8-sig")
