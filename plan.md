# Plan: bring the NHANES app in line with the M9 spec

## Context
The folder already has a draft `app.py`, `plan.md` and `prompts.md` from an earlier attempt that used a different feature list (ranked-pairs table, text summary). The M9 exercise requires different features. The draft is missing: data preview, threshold coloring, trend/binned means choice, user-picked heatmap variables, and the Pearson/Spearman toggle. It also never uses `scipy`. Its `plan.md` has no Spearman and lists wrong features.

## Changes to app.py (one file, streamlit/pandas/seaborn/matplotlib/numpy only)
1. Keep: `load_data()` (relative path `nhanes_health.csv`), `NUMERIC_COLS` without sex, one filtered `df` computed once at the top, and the `< 30 rows` warning.
2. Sidebar: sex (All/Male/Female), age range slider, and a **method radio (Pearson/Spearman)**. All views take `df` and `method`.
3. **Data preview**: dataset description (4,433 NHANES 2017-18 adults, sample not population caveat), `st.dataframe(df)` with row count.
4. **Pairwise view**: X and Y dropdowns. Drop NaN pairs, compute `r = pair[x].corr(pair[y], method=method)` and `n = len(pair)`. Scatter plus a trend line (`regplot` for Pearson, binned means for Spearman, or a "Trend: line / binned means" radio). A "Color by threshold" checkbox with a preset selectbox (SBP ≥ 130, DBP ≥ 80, BMI ≥ 30, HbA1c ≥ 6.5, total chol ≥ 240) that colors points by that column. Show r and n via `st.metric`, plus the caution that r near 0 does not mean no relationship (U-shaped sleep).
5. **Heatmap**: `st.multiselect` for variables (default all 10, need ≥ 2). r matrix with `df[cols].corr(method=method)`, n matrix by pairwise counts, `vmin=-1, vmax=1, center=0`, annotated with r and n in every cell. Caption stating the color scale is fixed to -1..1.
6. Remove the ranked-pairs table and the auto summary (not required). Remove them to keep the file simple.
7. Use `width="stretch"` as in the draft; keep matplotlib figures closed after use.

## Other deliverables
- `requirements.txt`: streamlit, pandas, seaborn, matplotlib, scipy (scipy needed for Spearman in pandas).
- `plan.md`: rewrite to match this plan (the approved version).
- `prompts.md`: keep Prompt 1 and append each follow-up prompt, including the revision prompt.
- `verification.md`: the 6-row table, the M9 trap paragraph, and the code check. Values read from the running app and computed independently in pandas by the user (I can supply the pandas numbers, but the user must read the app side).
- GitHub repo and Streamlit Cloud deploy: needs the user's account, so I will give exact steps and only run `git init`/commit/push if they ask.

## Verification
- Run: `uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py`
- Compute checks 1-6 in pandas, then compare with the app for All, Female and Male, and for the heatmap with Female. Also check Spearman against `df.corr(method="spearman")`.
- Confirm the heatmap colorbar spans -1..1 for every filter setting.
- Confirm n changes with filters in every view.

## Open questions (assumed)
- Pearson default, trend line for Pearson and binned means as an option, and a 30-row minimum.
