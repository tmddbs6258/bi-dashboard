# 1_overview.py
import streamlit as st
import matplotlib.pyplot as plt

from utils import (
    load_data,
    kpi_overview,
    apply_page_style,
    filter_block,
    style_ax,
    add_bar_labels,
    map_spending_segment,
    map_play_intensity,
)

st.set_page_config(page_title="Overview | Game BI", layout="wide")
apply_page_style()

df = load_data()
filtered = filter_block(df)

st.title("전체 유저 개요")
st.caption("게임의 유저 구조·몰입·과금 분포를 한눈에 파악합니다.")
st.caption("※ 데이터 출처: Kaggle 샘플 / 통화 단위: USD($)")

# -----------------------------
# KPI
# -----------------------------
kpi = kpi_overview(filtered)

c1, c2, c3, c4 = st.columns(4)
c1.metric("유저 수", f"{kpi['total_users']:,}")
c2.metric("총 매출", f"${kpi['revenue_sum']:,.0f}")
c3.metric("과금 유저 비율", f"{kpi['payer_rate']*100:.1f}%")
c4.metric(
    "ARPPU(평균 / 중앙값)",
    f"{kpi['arppu_mean']:,.1f} USD / {kpi['arppu_median']:,.1f} USD",
)

# -----------------------------
# 핵심 차트 2개 (Above-the-fold)
# -----------------------------
left, right = st.columns(2)

with left:
    st.subheader("과금 세그먼트 분포")
    seg = (
        filtered["SpendingSegment"]
        .value_counts()
        .reindex(["Minnow", "Dolphin", "Whale"])
        .dropna()
    )
    seg.index = seg.index.map(map_spending_segment)

    fig, ax = plt.subplots(figsize=(5.2, 2.6), dpi=120)
    seg.plot(kind="bar", ax=ax, color=["#C8D6EC", "#5A8BBE", "#1F4E79"])
    ax.set_ylabel("유저 수")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=0)
    style_ax(ax)
    add_bar_labels(ax)
    st.pyplot(fig, clear_figure=True)

with right:
    st.subheader("몰입도 분포")
    pi = (
        filtered["PlayIntensity"]
        .value_counts()
        .reindex(["Low", "Mid", "High"])
        .dropna()
    )
    pi.index = pi.index.map(map_play_intensity)

    fig, ax = plt.subplots(figsize=(5.2, 2.6), dpi=120)
    pi.plot(kind="bar", ax=ax, color="#2C6BAA")
    ax.set_ylabel("유저 수")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=0)
    style_ax(ax)
    add_bar_labels(ax)
    st.pyplot(fig, clear_figure=True)

st.markdown("###  Overview 한 줄 요약")
st.write(
    "핵과금(Whale) 집중도와 고몰입(High) 비중을 먼저 확인하고, 이후 페이지에서 ‘몰입→매출 연결’ 근거를 빠르게 검증합니다."
)

# -----------------------------
# 세부 근거(접기)
# -----------------------------
with st.expander("세부 분석/근거 보기", expanded=False):

    st.subheader("과금/비과금 기본 비교")

    payer = filtered[filtered["IsPayer"] == 1]
    nonpayer = filtered[filtered["IsPayer"] == 0]

    col1, col2 = st.columns(2)

    with col1:
        st.write("**과금 유저**")
        st.write(f"- 유저 수: {payer['UserID'].nunique():,}")
        st.write(f"- 평균 세션 수: {payer['SessionCount'].mean():.2f}")
        st.write(f"- 평균 세션 길이: {payer['AverageSessionLength'].mean():.2f}")

    with col2:
        st.write("**비과금 유저**")
        st.write(f"- 유저 수: {nonpayer['UserID'].nunique():,}")
        st.write(f"- 평균 세션 수: {nonpayer['SessionCount'].mean():.2f}")
        st.write(f"- 평균 세션 길이: {nonpayer['AverageSessionLength'].mean():.2f}")
