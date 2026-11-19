"""w9c: 8 Elsevier papers checked; none qualifies -> header-only CSV (see w9_w9c_rejected.txt)."""
import pandas as pd
cols = list(pd.read_csv(r"ml_spike/additions/TEMPLATE.csv", nrows=0).columns)
pd.DataFrame(columns=cols).to_csv(r"ml_spike/additions_v2/w9_w9c.csv", index=False, encoding="utf-8-sig")
