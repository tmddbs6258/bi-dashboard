# 4_insights.py
import streamlit as st
import pandas as pd
import numpy as np

from utils import load_data, apply_page_style, map_play_intensity

st.set_page_config(page_title="Insights | Game BI", layout="wide")
apply_page_style()

df = load_data()

st.title("인사이트")
st.caption("EDA 결과를 운영 의사결정 언어로 변환해 핵심 액션 포인트를 제안합니다.")

# -----------------------------
# Quick numbers
# -----------------------------
total_users = df["UserID"].nunique()
payer_rate = df["IsPayer"].mean()
whale_rate = (df["SpendingSegment"] == "Whale").mean()

fp = df["FirstPurchaseDaysAfterInstall"].dropna()
fp_mean = fp.mean() if len(fp) else np.nan
fp_median = fp.median() if len(fp) else np.nan

pi_mean_pay = (
    df.groupby("PlayIntensity")["InAppPurchaseAmount"]
    .mean()
    .reindex(["Low", "Mid", "High"])
)
pi_mean_pay.index = pi_mean_pay.index.map(map_play_intensity)

pi_whale_share = pd.crosstab(
    df["PlayIntensity"], df["SpendingSegment"], normalize="index"
).reindex(index=["Low", "Mid", "High"], columns=["Whale"])
pi_whale_share.index = pi_whale_share.index.map(map_play_intensity)

dev_mean_pay = df.groupby("Device")["InAppPurchaseAmount"].mean()

# -----------------------------
# Executive Summary
# -----------------------------
st.markdown("## 한 줄 결론")
st.info(
    "이 게임은 세션을 자주 할수록 과금이 늘어나며, 매출은 많이 쓰는 소수 유저와 인원이 많은 중간 몰입 유저가 함께 만들어내는 구조입니다."
)

# c1, c2, c3, c4 = st.columns(4)
# c1.metric("유저 수", f"{total_users:,}")
# c2.metric("과금 유저 비율", f"{payer_rate*100:.1f}%")
# c3.metric("핵과금(Whale) 비율", f"{whale_rate*100:.1f}%")
# if not np.isnan(fp_mean):
#     c4.metric("첫 결제 시점(평균/중앙)", f"{fp_mean:.1f} / {fp_median:.0f}일")
# else:
#     c4.metric("첫 결제 시점", "N/A")

# -----------------------------
# Insight Cards (압축 버전)
# -----------------------------
st.markdown("## 핵심 인사이트 4가지")

colL, colR = st.columns(2)

with colL:
    st.markdown("### 1) 몰입(세션 빈도)은 매출과 직결")
    low = pi_mean_pay.get("낮음", np.nan)
    mid = pi_mean_pay.get("중간", np.nan)
    high = pi_mean_pay.get("높음", np.nan)
    st.write(f"- 세션 수가 늘어날수록 평균 과금이 뚜렷하게 증가")
    high_whale = (
        pi_whale_share.loc["높음", "Whale"] * 100
        if "높음" in pi_whale_share.index
        else np.nan
    )
    st.write(f"- High 그룹에서 Whale 비율이 가장 높음")
    st.success(
        "운영: **중간 유저의 플레이 빈도 상승** → **High 전환 유도**(일일보상, 출석 이벤트, 미션 강화, 반복 플레이 보상)"
    )

with colR:
    st.markdown("### 2) 결제는 즉시형 + 후반 증가형 혼합")
    if not np.isnan(fp_mean):
        st.write(f"- 첫 결제는 0일부터 발생")
        st.write(f"- 2주 전후 구간에서 소폭 증가")
    st.success("운영: **초반 유입** 패키지 + **2주 전후** 프로모션 강화")

colL2, colR2 = st.columns(2)

with colL2:
    st.markdown("### 3) 연령 차이보다 행동 차이가 더 중요")
    st.write("- 연령대별 몰입 분포는 큰 차이 없음")
    st.write("- 몰입·과금 세그먼트 기준이 더 설명력 높음")
    st.success("운영: 인구통계 기반보다 **몰입도 기반 세그먼트 중심 운영**")

with colR2:
    st.markdown("### 4) 플랫폼 몰입은 유사, 지출 수준은 차이")
    ios_val = dev_mean_pay.get("iOS", np.nan)
    and_val = dev_mean_pay.get("Android", np.nan)
    st.write(f"- iOS 평균 과금이 더 높게 나타남")
    st.write(f"- 몰입 구조 자체는 플랫폼 간 큰 차이 없음")
    st.success(
        "운영: **iOS**는 **프리미엄 상품** 테스트 + **Android**는 **많은 사람 대상으로 할인/이벤트**"
    )

st.divider()

with st.expander("운영 KPI", expanded=False):
    st.markdown("## 운영 KPI")
    st.markdown(
        """
    - **High 몰입 유저 비율 (주간 변화)**  
    → 자주 플레이하는 유저가 늘고 있는가?

    - **중간 → High 전환율**  
    → 중간 유저를 High 플레이 유저로 끌어올리고 있는가?

    - **Whale 비율 변화**  
    → 과금을 많이 하는 유저가 늘고 있는가?

    - **플랫폼별 ARPPU (iOS vs Android)**  
    → 아이폰 유저가 실제로 더 많이 쓰고 있는가?

    - **첫 결제 발생률 (0~7일)**  
    → 초반 과금 유도가 잘 되고 있는가?
    """
    )
