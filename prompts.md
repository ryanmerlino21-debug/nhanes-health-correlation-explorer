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

---

# Full conversation prompt log (follow-up prompts to the coding agent)

Note: I switched to doing this part with Claude in my terminal because it is much less cluttered and easier to use.

Every message I sent in the working session, in order. Image attachments are noted in brackets.

1. `/Users/ryanmerlino/Desktop/untitled\ folder\ 3`
2. complete everything
3. [Image #1] how do i get to the point where i can host the app
4. can you do number 3 for me
5. can you do the next steps now
6. yes, create it
7. `/Users/ryanmerlino/Downloads/M9\ Exercise\ -\ Health\ Correlation\ App.md /Users/ryanmerlino/Downloads/untitled\ folder\ 3` can you verify everything is correct in this
8. [Image #2] where do i pick age vs systolic bp
9. can you fix all of the problems and then put them into github
10. do i need to create a new app to update this one?
11. [Image #3] [Image #4] [Image #5] does this all look how its supposed to look
12. [Image #6] does this look fine
13. can you give me the stuff i need to submit
14. not sure where or how to submit this. `/Users/ryanmerlino/Desktop/M9\ In-class\ Activity.pdf` read this and let me know
15. so in the marimo notebook i add the links?
16. ok what were the 2 links again
17. can you confirm everything in the app and github is 100% correct and these links work fine
18. what do i click on the app
19. [Image #7] this look good for #1
20. [Image #8] this look good?
21. can you make a list of every single prompt i said here
22. can you add all of these prompts into the prompts.md file at the bottom. separate it from the other prompts
