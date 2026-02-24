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
st.subheader("몰입도별 플레이 지표 요약")

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

st.subheader("첫 결제까지 걸린 일수 분포 (구간 요약, 0~30일)")

fp = filtered["FirstPurchaseDaysAfterInstall"].dropna()

if len(fp) == 0:
    st.info("표시할 데이터가 없습니다(결측).")
else:
    # 정수 일 단위 + 0~30일 제한
    fp_days = fp.astype(int).clip(lower=0, upper=30)

    # ---- 1) 균등 3구간 ----
    bins = [-1, 10, 20, 30]
    labels = ["0~10일", "11~20일", "21~30일"]

    fp_bucket = pd.cut(fp_days, bins=bins, labels=labels)

    bucket_counts = fp_bucket.value_counts().reindex(labels, fill_value=0)
    bucket_ratio = (bucket_counts / bucket_counts.sum() * 100).round(1)

    # ---- 2) 시각화 ----
    fig, ax = plt.subplots(figsize=(8, 3), dpi=120)

    ax.bar(bucket_counts.index, bucket_counts.values, width=0.4, color="#4C72B0")

    ax.set_xlabel("설치 후 첫 결제까지 걸린 기간")
    ax.set_ylabel("첫 결제 유저 수")

    ax.set_ylim(0, bucket_counts.max() * 1.15)

    style_ax(ax)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    max_val = max(bucket_counts.values)
    ax.set_ylim(0, max_val * 1.12)
    y_offset = max_val * 0.02
    # 막대 위 라벨
    for i, (cnt, pct) in enumerate(zip(bucket_counts.values, bucket_ratio.values)):
        ax.text(
            i,
            cnt + y_offset,
            f"{cnt:,}명 ({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9,
            color="#333333",
        )

    st.pyplot(fig, clear_figure=True)

    st.caption("0~30일을 균등하게 3구간으로 나눈 첫 결제 분포입니다.")

st.markdown("###  Engagement 한 줄 요약")
st.write(
    "세션 길이는 몰입 구간 간 큰 차이를 보이지 않으며, 몰입 증가에 따라 세션 빈도가 뚜렷하게 증가하는 구조이며, 첫 결제는 특정 시점에 집중되지 않고, 0~30일 전 구간에 고르게 분포하는 구조입니다."
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
