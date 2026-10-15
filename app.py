import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

CSV_PATH = "nhanes_health.csv"
# sex is text and is only a filter, so it is never in this list.
NUMERIC_COLS = [
    "age", "bmi", "waist_cm", "systolic_bp", "diastolic_bp",
    "hba1c", "total_chol", "hdl_chol", "sleep_hours", "sedentary_minutes",
]
THRESHOLDS = {
    "SBP ≥ 130": ("systolic_bp", 130),
    "DBP ≥ 80": ("diastolic_bp", 80),
    "BMI ≥ 30": ("bmi", 30),
    "HbA1c ≥ 6.5": ("hba1c", 6.5),
    "Total cholesterol ≥ 240": ("total_chol", 240),
}
MIN_ROWS = 30


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


def corr_with_n(df, cols, method):
    """Pairwise-complete correlation matrix and matching n matrix."""
    present = df[cols].notna().astype(int)
    n = present.T.dot(present)
    r = df[cols].corr(method=method, min_periods=3)
    return r, n


def heatmap(r, n, method):
    annot = np.empty(r.shape, dtype=object)
    for i, a in enumerate(r.index):
        for j, b in enumerate(r.columns):
            v = r.loc[a, b]
            annot[i, j] = "" if pd.isna(v) else f"{v:.2f}\nn={int(n.loc[a, b])}"
    fig, ax = plt.subplots(figsize=(11, 8))
    sns.heatmap(r.astype(float), annot=annot, fmt="", cmap="RdBu_r",
                vmin=-1, vmax=1, center=0, linewidths=0.5,
                annot_kws={"fontsize": 7}, ax=ax,
                cbar_kws={"label": f"{method.capitalize()} r"})
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    fig.tight_layout()
    return fig


def scatter(pair, x, y, r, n, trend, flag, method):
    fig, ax = plt.subplots(figsize=(7, 5))
    if flag is None:
        ax.scatter(pair[x], pair[y], s=12, alpha=0.3, color="steelblue")
    else:
        label, mask = flag
        ax.scatter(pair.loc[~mask, x], pair.loc[~mask, y], s=12, alpha=0.3,
                   color="steelblue", label=f"not {label}")
        ax.scatter(pair.loc[mask, x], pair.loc[mask, y], s=12, alpha=0.5,
                   color="crimson", label=label)
        ax.legend()
    if trend == "Linear trend line":
        slope, intercept = np.polyfit(pair[x], pair[y], 1)
        xs = np.array([pair[x].min(), pair[x].max()])
        ax.plot(xs, slope * xs + intercept, color="black", lw=2)
    else:
        bins = pd.cut(pair[x], bins=10)
        means = pair.groupby(bins, observed=True).agg(bx=(x, "mean"), by=(y, "mean"))
        ax.plot(means["bx"], means["by"], color="black", marker="o", lw=2)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{y} vs {x}: {method} r = {r:.2f}, n = {n}")
    fig.tight_layout()
    return fig


st.set_page_config(page_title="NHANES correlations", layout="wide")
st.title("NHANES health measures: correlation explorer")

data = load_data()

# Filters: df is computed once and passed to every view below.
st.sidebar.header("Filters")
sex_choice = st.sidebar.selectbox("Sex", ["All", "Male", "Female"])
age_min, age_max = int(data["age"].min()), int(data["age"].max())
age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))
method = st.sidebar.radio("Correlation method", ["pearson", "spearman"],
                          format_func=str.capitalize)

df = data[data["age"].between(age_range[0], age_range[1])]
if sex_choice != "All":
    df = df[df["sex"] == sex_choice]

# 1. Data preview
st.header("Data preview")
st.write(
    "4,433 adults aged 20+ from the CDC's 2017-2018 NHANES. Each row is one "
    "participant. NHANES oversamples some groups, so these correlations describe "
    "this sample, not the US population."
)
st.caption(f"{len(df):,} of {len(data):,} rows after filters "
           f"(sex: {sex_choice}, age {age_range[0]}-{age_range[1]}, "
           f"method: {method.capitalize()})")

if len(df) < MIN_ROWS:
    st.warning(f"Only {len(df)} rows match these filters. Need at least {MIN_ROWS}. "
               "Widen the filters.")
    st.stop()

st.dataframe(df, width="stretch", hide_index=True)

# 2. Pairwise view
st.header("Pairwise view")
c1, c2 = st.columns(2)
x = c1.selectbox("X axis", NUMERIC_COLS, index=NUMERIC_COLS.index("age"))
y = c2.selectbox("Y axis", NUMERIC_COLS, index=NUMERIC_COLS.index("systolic_bp"))
o1, o2 = st.columns(2)
trend = o1.radio("Trend", ["Linear trend line", "Binned means"], horizontal=True)
use_thr = o2.checkbox("Color points by a health threshold")
thr_label = None
if use_thr:
    thr_label = o2.selectbox("Threshold", list(THRESHOLDS))

if x == y:
    st.info("Pick two different columns.")
else:
    cols = [x, y] + ([THRESHOLDS[thr_label][0]] if use_thr else [])
    pair = df[list(dict.fromkeys(cols))].dropna()
    n = len(pair)
    if n < 3:
        st.warning("Not enough overlapping data for these columns.")
    else:
        r = pair[x].corr(pair[y], method=method)
        m1, m2 = st.columns(2)
        m1.metric(f"{method.capitalize()} r", f"{r:.2f}")
        m2.metric("n (participants)", f"{n:,}")
        flag = None
        if use_thr:
            col, cut = THRESHOLDS[thr_label]
            flag = (thr_label, pair[col] >= cut)
        fig = scatter(pair, x, y, r, n, trend, flag, method)
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Caution: an r near zero does not mean 'no relationship'. "
                   "A U-shaped curve (like sleep hours vs. health) can have r ≈ 0. "
                   "Always look at the scatter plot.")

# 3. Heatmap
st.header("Correlation heatmap")
chosen = st.multiselect("Variables to include", NUMERIC_COLS, default=NUMERIC_COLS)
if len(chosen) < 2:
    st.info("Pick at least two variables.")
else:
    r_mat, n_mat = corr_with_n(df, chosen, method)
    fig = heatmap(r_mat, n_mat, method)
    st.pyplot(fig)
    plt.close(fig)
    st.caption("Color scale is fixed from -1 to 1 so colors are comparable across filters.")
