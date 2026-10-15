# Prompts

## Prompt 1 (plan mode, no code yet)

Don't write any code yet. I want a plan first.

I want to build a Streamlit app, app.py, that explores correlations between health measures in nhanes_health.csv. Read the CSV first (header, a sample of rows, and a count of missing values per column) instead of relying on me to retype the data dictionary. Every numeric column except sex is a candidate for correlation: age, bmi, waist_cm, systolic_bp, diastolic_bp, hba1c, total_chol, hdl_chol, sleep_hours and sedentary_minutes. The sex column holds text (Male/Female). It must never go into any correlation, heatmap, or scatter axis. It is only a filter.

The app needs five features:
1. Data preview: a short description of the dataset and a table of the rows.
2. Pairwise view: two dropdowns pick X and Y. The app shows a scatter plot, the correlation r, and the number of participants n. The scatter plot has a trend line or binned means, and an option to color points by a health threshold such as SBP >= 130.
3. Correlation heatmap: the user picks which numeric variables to include. Every square shows its coefficient, and the color scale is fixed from -1 to 1.
4. Filters: sidebar controls for sex (All, Male, Female) and an age range slider. Both must update every view: the table, the scatter plot, r, n and the heatmap. Nothing may use the unfiltered data once a filter is set. If the filters leave fewer than 30 rows, show a warning instead of a chart.
5. Correlation method: a toggle between Pearson and Spearman that applies to both the pairwise view and the heatmap.

Rules for the numbers:
- Missing values: use pairwise deletion, so each r uses only the rows where both columns are present. Do not fill, impute or drop whole rows globally.
- Heatmap color scale: diverging, centered at 0, fixed to run from -1 to 1 (not auto-scaled), with the r value annotated in each cell.
- Show n (the number of rows used) next to every r: in the pairwise view, in the heatmap annotations, and in the scatter plot title.
- Round r to 2 decimals.
- Add a caution that an r near zero does not mean "no relationship" (for example a U-shaped sleep curve).

Constraints: Python and Streamlit, with pandas and seaborn (or plotly). Everything goes in one file called app.py. Do not use any other packages without asking me first.

Please give me a plan, not code. It should cover:
- The build order, step by step, starting with the data and filters.
- How the filters feed every view (for example, one filtered DataFrame computed once and passed to everything).
- The exact command to run the app.
- Anything in my request that is unclear or that you would need to assume. Ask me about it instead of guessing.

## Prompt 2 (build)

Plan approved. Leave plan mode and build app.py to match the plan: data preview, pairwise view (X/Y dropdowns, scatter, trend line or binned means, threshold coloring, r and n), heatmap with user-picked variables and a fixed -1 to 1 scale, sidebar sex and age filters feeding every view, and a Pearson/Spearman toggle. Add requirements.txt listing every package app.py imports.

## Prompt 3 (verify)

I checked the app against pandas for the six checks in verification.md (all participants, Female only, Male only, and the Female heatmap square). Everything matched. Please confirm that app.py loads the CSV with the relative path nhanes_health.csv and that requirements.txt lists every import so the app can be deployed on Streamlit Community Cloud.
