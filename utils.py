# utils.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# -----------------------------
# 라벨 매핑 (영어 → 한글)
# -----------------------------
map_spending_segment = {"Minnow": "소과금", "Dolphin": "중과금", "Whale": "핵과금"}
map_play_intensity = {"Low": "낮음", "Mid": "중간", "High": "높음"}


# -----------------------------
# 공통 스타일 (여백 최소화 + 한글 폰트)
# -----------------------------
def apply_page_style():
    # 한글 폰트(윈도우)
    plt.rcParams["font.family"] = "Malgun Gothic"
    plt.rcParams["axes.unicode_minus"] = False

    # Streamlit 기본 여백 줄이기 (스크롤 완화)
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2.75rem; padding-bottom: 1rem; }
        div[data-testid="stMetric"] { padding: 0.35rem 0.6rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_ax(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))


def add_bar_labels(ax):
    for p in ax.patches:
        h = p.get_height()
        ax.annotate(
            f"{h:,.0f}",
            (p.get_x() + p.get_width() / 2, h),
            ha="center",
            va="bottom",
            fontsize=9,
            xytext=(0, 3),
            textcoords="offset points",
        )


@st.cache_data
def load_data(path="data/processed.csv"):
    df = pd.read_csv(path)

    required = [
        "UserID",
        "Device",
        "AgeGroup",
        "PlayIntensity",
        "SpendingSegment",
        "InAppPurchaseAmount",
        "SessionCount",
        "AverageSessionLength",
        "FirstPurchaseDaysAfterInstall",
        "IsPayer",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()

    return df


def filter_block(df: pd.DataFrame) -> pd.DataFrame:
    """대표 화면에서 스크롤을 덜 유발하도록 '접힌 필터' 형태로 공통 제공."""
    with st.expander("필터", expanded=False):
        col1, col2, col3 = st.columns(3)

        device_opts = ["전체"] + sorted([x for x in df["Device"].dropna().unique()])
        age_opts = ["전체"] + sorted([x for x in df["AgeGroup"].dropna().unique()])

        genre_col = "GameGenre" if "GameGenre" in df.columns else None
        genre_opts = (
            ["전체"] + sorted([x for x in df[genre_col].dropna().unique()])
            if genre_col
            else ["전체"]
        )

        device_sel = col1.selectbox("디바이스", device_opts, index=0)
        age_sel = col2.selectbox("연령대", age_opts, index=0)
        _ = col3.selectbox("장르", genre_opts, index=0, disabled=(genre_col is None))

    filtered = df.copy()
    if device_sel != "전체":
        filtered = filtered[filtered["Device"] == device_sel]
    if age_sel != "전체":
        filtered = filtered[filtered["AgeGroup"] == age_sel]

    # GameGenre는 데이터셋에 없을 수 있어서 실제 필터링은 제외(표시만)
    return filtered


def kpi_overview(df):
    total_users = df["UserID"].nunique()
    payer_rate = df["IsPayer"].mean()
    revenue_sum = df["InAppPurchaseAmount"].sum()
    arppu_mean = df.loc[df["IsPayer"] == 1, "InAppPurchaseAmount"].mean()
    arppu_median = df.loc[df["IsPayer"] == 1, "InAppPurchaseAmount"].median()

    return {
        "total_users": total_users,
        "payer_rate": payer_rate,
        "revenue_sum": revenue_sum,
        "arppu_mean": arppu_mean,
        "arppu_median": arppu_median,
    }
