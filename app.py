import streamlit as st

st.set_page_config(page_title="Game BI Dashboard", layout="wide")

st.title("게임 유저 & 매출 분석 대시보드")

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
**1️) 전체 유저·매출 개요**  
→ 전체 유저 구조 및 핵심 KPI 요약  

**2️) 플레이 패턴 분석**  
→ 몰입(세션 빈도) 구조 및 세그먼트 비교  

**3️) 과금 구조 분석**  
→ 과금 구조 분석 및 매출 기여도  

**4️) 핵심 인사이트**  
→ 핵심 인사이트 및 실행 전략 제안
"""
)
