# Plan: NHANES Health Correlation Explorer

## Goal
One Streamlit file, `app.py`, that explores correlations in `nhanes_health.csv` (4,433 adults, NHANES 2017-2018) with the five M9 features: data preview, pairwise view, correlation heatmap, sidebar filters, and a Pearson/Spearman toggle.

## Data rules
- Numeric columns: age, bmi, waist_cm, systolic_bp, diastolic_bp, hba1c, total_chol, hdl_chol, sleep_hours, sedentary_minutes.
- `sex` is text. It is used only as a filter and never enters a correlation, heatmap or scatter axis.
- Missing values: pairwise deletion, so each r uses only rows where both columns are present. No imputation.
- Packages: streamlit, pandas, seaborn, matplotlib, numpy, scipy. Nothing else without asking.

## Build order
1. **Data and filters.** Load the CSV with the relative path `nhanes_health.csv` (cached). Sidebar: sex (All/Male/Female), age range slider, and the method radio (Pearson/Spearman). Compute one filtered DataFrame `df` once at the top and pass it to every view. If fewer than 30 rows remain, show a warning and stop.
2. **Data preview.** Short dataset description (including the caveat that NHANES oversamples some groups, so results describe this sample), the filtered row count, and a table of the filtered rows.
3. **Pairwise view.** X and Y dropdowns. Drop rows missing either column, compute `r = x.corr(y, method=method)` and `n = len(pair)`, and show both with `st.metric`. Scatter plot with a linear trend line or binned means (user choice), an optional checkbox to color points by a health threshold (SBP >= 130, DBP >= 80, BMI >= 30, HbA1c >= 6.5, total cholesterol >= 240), and r and n in the plot title. Include the caution that an r near zero does not mean "no relationship" (the U-shaped sleep curve).
4. **Heatmap.** Multiselect for variables (default all ten, at least two). r matrix with `df[cols].corr(method=method)` and a pairwise n matrix. Every cell is annotated with r and n. Colors are diverging, centered at 0 and fixed to -1..1 for every filter setting. A caption states the fixed scale.
5. **Deliverables.** `requirements.txt` listing every import, `prompts.md`, `plan.md`, `verification.md`.

## How the filters feed every view
The sex and age filters produce one `df`. The preview table, the pairwise r and n, the scatter plot and the heatmap all read from that same `df`, so none of them can use unfiltered data. The method radio is passed to both the pairwise correlation and the heatmap.

## Run command
```bash
uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py
```

## Assumptions
- Pearson is the default method.
- The linear trend line is always a straight-line fit, even under Spearman. Binned means are offered for non-linear patterns.
- Minimum of 30 rows after filtering.

## Verification
Read r and n from the app and compute them independently in pandas for: all participants (age vs systolic_bp, bmi vs waist_cm, waist_cm vs hdl_chol), Female only, Male only, and the Female heatmap square. Also check Spearman against `df.corr(method="spearman")` and confirm the heatmap colorbar spans -1 to 1. Results are in `verification.md`.
