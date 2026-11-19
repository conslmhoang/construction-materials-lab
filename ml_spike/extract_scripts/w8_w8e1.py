import pandas as pd
D = r"ml_spike/additions_v2/"
cols = list(pd.read_csv(r"ml_spike/additions/TEMPLATE.csv", nrows=0, encoding="utf-8-sig").columns)
# All six assigned papers were rejected (see w8_w8e1_rejected.txt); no rows extracted.
pd.DataFrame(columns=cols).to_csv(D + "w8_w8e1.csv", index=False, encoding="utf-8-sig")
