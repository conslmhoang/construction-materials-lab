"""w8m3: all 5 assigned MDPI papers rejected (see additions_v2/w8_w8m3_rejected.txt). Writes a header-only CSV."""
import os
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
cols = list(pd.read_csv(os.path.join(here, "..", "additions", "TEMPLATE.csv"), encoding="utf-8-sig", nrows=0).columns)
out = os.path.join(here, "..", "additions_v2", "w8_w8m3.csv")
pd.DataFrame(columns=cols).to_csv(out, index=False, encoding="utf-8-sig")
print(len(cols), "columns, 0 rows")
