# 3_revenue.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import (
    load_data,
    apply_page_style,
    filter_block,
    style_ax,
    add_bar_labels,
    map_play_intensity,
    map_spending_segment,
)

st.set_page_config(page_title="Revenue | Game BI", layout="wide")
apply_page_style()

df = load_data()
filtered = filter_block(df)

st.title("과금 구조 분석")
st.caption(
    "몰입도(PlayIntensity) 관점에서 과금 수준과 Whale 영향(평균 vs 중앙값)을 비교합니다."
)
# st.caption("※ 데이터 출처: Kaggle 샘플 / 통화 단위: USD($)")

# amt = filtered["InAppPurchaseAmount"]
# payer = filtered[filtered["IsPayer"] == 1]

# total_rev = float(amt.sum())
# arppu_mean = float(payer["InAppPurchaseAmount"].mean()) if len(payer) else np.nan
# arppu_median = float(payer["InAppPurchaseAmount"].median()) if len(payer) else np.nan
# whale_rate = float((filtered["SpendingSegment"] == "Whale").mean())
# payer_rate = float(filtered["IsPayer"].mean())

# c1, c2, c3, c4 = st.columns(4)
# c1.metric("총 매출", f"${total_rev:,.0f}")
# c2.metric("과금 유저 비율", f"{payer_rate*100:.1f}%")
# c3.metric("ARPPU(평균/중앙)", f"${arppu_mean:,.1f} / ${arppu_median:,.1f}")
# c4.metric("핵과금(Whale) 비율", f"{whale_rate*100:.1f}%")

# -----------------------------
# Above-the-fold: 평균 vs 중앙값 2차트
# -----------------------------
st.subheader("① 몰입도 × 과금 수준 (평균 vs 중앙값)")

pi_pay = (
    filtered.groupby("PlayIntensity")["InAppPurchaseAmount"]
    .agg(과금자수=("count"), 평균=("mean"), 중앙값=("median"), 매출합=("sum"))
    .reindex(["Low", "Mid", "High"])
)

# 인덱스 한글화
pi_pay.index = pi_pay.index.map(map_play_intensity)

left, right = st.columns(2)

with left:
    fig, ax = plt.subplots(figsize=(5.2, 2.6), dpi=120)
    pi_pay["평균"].plot(kind="bar", ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("평균 결제금액($)")
    ax.tick_params(axis="x", rotation=0)
    style_ax(ax)
    st.pyplot(fig, clear_figure=True)
    st.caption("평균은 Whale의 영향이 크게 반영됩니다.")

with right:
    fig, ax = plt.subplots(figsize=(5.2, 2.6), dpi=120)
    pi_pay["중앙값"].plot(kind="bar", ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("중앙값 결제금액($)")
    ax.tick_params(axis="x", rotation=0)
    style_ax(ax)
    st.pyplot(fig, clear_figure=True)
    st.caption("중앙값은 일반 유저의 결제 수준을 더 안정적으로 보여줍니다.")

st.markdown("### Revenue 한 줄 요약")
st.write(
    "평균 과금은 증가하지만 중앙값은 거의 변하지 않아, 매출 상승은 소수 고과금 유저에 의해 발생하는 구조입니다."
)

# -----------------------------
# 세부 근거(접기)
# -----------------------------
with st.expander("세부 분석/근거 보기", expanded=False):
    st.subheader("② 몰입도별 과금 요약표")
    st.dataframe(
        pi_pay.style.format(
            {
                "과금자수": "{:,.0f}",
                "평균": "{:,.2f}",
                "중앙값": "{:,.2f}",
                "매출합": "${:,.0f}",
            }
        ),
        use_container_width=True,
    )

    st.subheader("③ 몰입도 × 과금 세그먼트 구성 비율")
    ct_pi_seg = pd.crosstab(
        filtered["PlayIntensity"], filtered["SpendingSegment"], normalize="index"
    ).reindex(index=["Low", "Mid", "High"], columns=["Minnow", "Dolphin", "Whale"])
    ct_pi_seg.index = ct_pi_seg.index.map(map_play_intensity)
    ct_pi_seg.columns = [map_spending_segment[c] for c in ct_pi_seg.columns]
    st.dataframe((ct_pi_seg * 100).round(1).astype(str) + "%", use_container_width=True)

    st.subheader("④ 몰입도별 매출 기여도(합)")
    pi_rev = (
        filtered.groupby("PlayIntensity")["InAppPurchaseAmount"]
        .sum()
        .reindex(["Low", "Mid", "High"])
    )
    pi_rev.index = pi_rev.index.map(map_play_intensity)

    fig, ax = plt.subplots(figsize=(10.8, 2.6), dpi=120)
    pi_rev.plot(kind="bar", ax=ax)
    ax.set_xlabel("")
    ax.set_ylabel("매출 합계($)")
    ax.tick_params(axis="x", rotation=0)
    style_ax(ax)
    add_bar_labels(ax)
    st.pyplot(fig, clear_figure=True)
