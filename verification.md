# Verification

"App shows" values were read from the app's own displayed r and n (via Streamlit's headless test runner running `app.py`, not a browser). For row 6 the value is the annotation the app passes to the heatmap. pandas values were computed separately from `nhanes_health.csv`.

| # | Check | App shows | pandas gives | Match? |
|---|-------|-----------|--------------|--------|
| 1 | r, age vs systolic_bp, all | r 0.46, n 4,433 | 0.4627 (n=4433) | Yes |
| 2 | r, bmi vs waist_cm, all | r 0.90, n 4,433 | 0.9026 (n=4433) | Yes |
| 3 | r, waist_cm vs hdl_chol, all | r -0.33, n 4,433 | -0.3350 (n=4433) | Yes |
| 4 | r and n, age vs systolic_bp, Female | r 0.56, n 2,263 | 0.5553, n=2263 | Yes |
| 5 | r and n, age vs systolic_bp, Male | r 0.35, n 2,170 | 0.3507, n=2170 | Yes |
| 6 | Heatmap age/systolic_bp square with Female filter matches row 4? | 0.56, n=2263 | 0.5553, n=2263 | Yes |

The heatmap color scale was also confirmed as vmin=-1, vmax=1.

## M9 trap
An r near 0 does not mean "no relationship": a U-shaped relationship (like sleep hours vs. health outcomes) can have r close to 0 because the rising and falling halves cancel out. Check the scatter plot or binned means, not just r. A heatmap is only honest if its colors run from -1 to 1; the app fixes the scale so colors mean the same thing under every filter.

## Code check
```python
import pandas as pd
df = pd.read_csv("nhanes_health.csv")
def r_n(d, x, y):
    p = d[[x, y]].dropna()
    return round(p[x].corr(p[y]), 4), len(p)

r_n(df, "age", "systolic_bp")                         # (0.4627, 4433)
r_n(df, "bmi", "waist_cm")                            # (0.9026, 4433)
r_n(df, "waist_cm", "hdl_chol")                       # (-0.335, 4433)
r_n(df[df.sex == "Female"], "age", "systolic_bp")     # (0.5553, 2263)
r_n(df[df.sex == "Male"], "age", "systolic_bp")       # (0.3507, 2170)
```
