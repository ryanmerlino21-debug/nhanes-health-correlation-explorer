# Prompts

## Prompt 1 (plan mode, no code yet)

Don't write any code yet. I want a plan first.

I want to build a Streamlit app, app.py, that explores correlations between health measures in nhanes_health.csv. Read the CSV first (header and a sample of rows, plus a count of missing values per column) instead of relying on me to retype the data dictionary. Every numeric column except sex is a candidate for correlation: age, bmi, waist_cm, systolic_bp, diastolic_bp, hba1c, total_chol, hdl_chol, sleep_hours and sedentary_minutes. The sex column holds text (Male/Female), and it must never go into any correlation, heatmap, or scatter axis. It is only a filter.

The app needs five features:
1. A correlation heatmap of all numeric columns.
2. A ranked table of the strongest correlated pairs, sorted by absolute r.
3. A scatter plot for any two columns I pick, with a trend line and its r.
4. A pair of dropdowns (x and y) that drive the scatter plot.
5. A short plain-language summary that states the strongest pair in the current filtered data and warns that correlation is not causation.

There are two filters in the sidebar: a sex selector (All, Male, Female) and an age range slider. Both filters must feed every view: the heatmap, the ranked table, the scatter plot and the summary. Nothing may use the unfiltered data once a filter is set. If the filters leave too few rows (fewer than 30), show a warning instead of a chart.

Rules for the numbers:
- Missing values: use pairwise deletion, so each r uses only the rows where both columns are present. Do not fill, impute or drop whole rows globally.
- Heatmap color scale: diverging, centered at 0, fixed to run from -1 to 1 (not auto-scaled), with the r value annotated in each cell.
- Show n (the number of rows used) next to every r, in the heatmap annotations, the ranked table and the scatter plot title.
- Round r to 2 decimals.

Constraints: Python and Streamlit, with pandas and seaborn (or plotly). Everything goes in one file called app.py. Do not use any other packages without asking me first.

Please give me a plan, not code. It should cover:
- The build order, step by step.
- How the filters feed every view (for example, one filtered DataFrame computed once and passed to everything).
- The exact command to run the app.
- Anything in my request that is unclear or that you would need to assume. Ask me about it instead of guessing.

## Prompt 2 (build)

Plan approved. Leave plan mode and rewrite app.py to match the M9 spec: data preview, pairwise view (X/Y dropdowns, scatter, trend line or binned means, threshold coloring, r and n), heatmap with user-picked variables and a fixed -1 to 1 scale, sidebar sex and age filters feeding every view, and a Pearson/Spearman toggle. Remove the ranked-pairs table and summary. Add requirements.txt.
