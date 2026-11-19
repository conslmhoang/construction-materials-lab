"""w8m2: all 5 assigned MDPI papers were rejected; writes header-only CSV."""
import pandas as pd
cols = list(pd.read_csv(r"ml_spike/additions/TEMPLATE.csv", nrows=0, encoding="utf-8-sig").columns)
pd.DataFrame(columns=cols).to_csv(r"ml_spike/additions_v2/w8_w8m2.csv", index=False, encoding="utf-8-sig")
