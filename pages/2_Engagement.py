# 2_engagement.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    load_data,
    apply_page_style,
    filter_block,
    style_ax,
    map_play_intensity,
    map_spending_segment,
)

st.set_page_config(page_title="Engagement | Game BI", layout="wide")
apply_page_style()

df = load_data()
filtered = filter_block(df)

st.title("플레이 패턴 비교")
st.caption("몰입도(PlayIntensity) 구조를 중심으로 플레이 지표를 비교합니다.")

# -----------------------------
# Above-the-fold: 표 1개 + 차트 1개
# -----------------------------
st.subheader("① 몰입도별 플레이 지표 요약")

summary = (
    filtered.groupby("PlayIntensity")
    .agg(
        유저수=("UserID", "count"),
        세션수_평균=("SessionCount", "mean"),
        # 세션수_중앙값=("SessionCount", "median"),
        세션길이_평균=("AverageSessionLength", "mean"),
        # 세션길이_중앙값=("AverageSessionLength", "median"),
    )
    .reindex(["Low", "Mid", "High"])
)

# 인덱스 한글화
summary.index = summary.index.map(map_play_intensity)

st.dataframe(
    summary.style.format(
        {
            "유저수": "{:,.0f}",
            "세션수_평균": "{:.2f}",
            # "세션수_중앙값": "{:.0f}",
            "세션길이_평균": "{:.2f}",
            # "세션길이_중앙값": "{:.2f}",
        }
    ),
    use_container_width=True,
)

st.subheader("② 첫 결제까지 걸린 일수 분포")
fp = filtered["FirstPurchaseDaysAfterInstall"].dropna()
if len(fp) == 0:
    st.info("표시할 데이터가 없습니다(결측).")
else:
    fig, ax = plt.subplots(figsize=(10.8, 2.6), dpi=120)
    ax.hist(fp, bins=10)
    ax.set_xlabel("일")
    ax.set_ylabel("유저 수")
    ax.set_xlim(0, 30)
    ax.axvline(fp.mean(), linestyle="--", linewidth=1)
    ax.axvline(fp.median(), linestyle=":", linewidth=1)
    style_ax(ax)
    st.pyplot(fig, clear_figure=True)
    st.caption(f"평균 {fp.mean():.1f}일 / 중앙값 {fp.median():.0f}일")

st.markdown("###  Engagement 한 줄 요약")
st.write(
    "세션 길이는 몰입 구간 간 큰 차이를 보이지 않으며, 몰입 증가에 따라 세션 빈도가 뚜렷하게 증가하는 구조이며, 결제는 초기 구간부터 발생하되 후반으로 갈수록 소폭 증가하는 경향을 보입니다."
)

# -----------------------------
# 세부 근거(접기)
# -----------------------------
with st.expander("세부 분석/근거 보기", expanded=False):
    st.subheader("③ 디바이스 × 몰입도 비율")
    ct_device = pd.crosstab(
        filtered["Device"], filtered["PlayIntensity"], normalize="index"
    ).reindex(columns=["Low", "Mid", "High"])
    ct_device.columns = [map_play_intensity[c] for c in ct_device.columns]
    st.dataframe((ct_device * 100).round(1).astype(str) + "%", use_container_width=True)

    st.subheader("④ 연령대 × 몰입도 비율")
    ct_age = pd.crosstab(
        filtered["AgeGroup"], filtered["PlayIntensity"], normalize="index"
    ).reindex(columns=["Low", "Mid", "High"])
    age_order = ["10s", "20s", "30s", "40s", "50+"]
    ct_age = ct_age.reindex([a for a in age_order if a in ct_age.index])
    ct_age.columns = [map_play_intensity[c] for c in ct_age.columns]
    st.dataframe((ct_age * 100).round(1).astype(str) + "%", use_container_width=True)
