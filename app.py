import streamlit as st

st.set_page_config(page_title="Game BI Dashboard", layout="wide")

st.title("Game User & Revenue BI Dashboard")

st.markdown(
    """
데이터 기반 게임 운영 의사결정을 위한  
**유저 행동 · 몰입 구조 · 과금 구조 분석 대시보드**
"""
)

st.divider()

st.subheader("페이지 구성")

st.markdown(
    """
**1️) Overview**  
→ 전체 유저 구조 및 핵심 KPI 요약  

**2️) Engagement**  
→ 몰입(세션 빈도) 구조 및 세그먼트 비교  

**3️) Revenue**  
→ 과금 구조 분석 및 매출 기여도  

**4️) Insights**  
→ 핵심 인사이트 및 실행 전략 제안
"""
)
