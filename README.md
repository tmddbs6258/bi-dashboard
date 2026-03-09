# Game User Behavior & Revenue BI Dashboard

데이터 기반 게임 운영 의사결정을 위한  
**게임 유저 행동 · 몰입 구조 · 과금 구조 분석 BI 프로젝트**

모바일 게임 유저 데이터를 분석하여  
**플레이 몰입도와 매출 구조 간 관계를 파악하고 실제 운영 인사이트를 도출**하는 것을 목표로 한 프로젝트입니다.

단순 데이터 시각화가 아닌  
**게임 서비스 운영 관점(Game BI)에서 분석을 진행**했습니다.

---

# Project Goal

게임 서비스 운영에서 중요한 질문

- 어떤 유저가 매출을 만드는가?
- 플레이 몰입도는 매출과 어떤 관계가 있는가?
- 어떤 유저를 집중적으로 운영해야 하는가?

이 프로젝트는 위 질문에 대해  
**데이터 기반으로 답을 찾는 것을 목표로 합니다.**

---

# Dashboard Overview

분석은 3가지 관점으로 진행했습니다.

1. **유저 구조 분석**  
2. **플레이 행동 패턴 분석**  
3. **매출 구조 분석**

이를 통해

- 유저 행동
- 몰입도
- 과금 구조

간의 관계를 확인할 수 있습니다.

---

# Dashboard Structure

## 1. Overview

전체 유저 구조와 핵심 KPI 요약

주요 지표

- Total Users
- Total Revenue
- Paying User Ratio
- ARPPU
- Monetization Segment Distribution
- Play Intensity Distribution

목적

→ **게임 서비스의 전체 유저 구조를 빠르게 파악**

---

## 2. Play Pattern Analysis

유저 플레이 행동 패턴 분석

몰입도(PlayIntensity) 기준 플레이 패턴 비교

분석 지표

- 평균 세션 수
- 평균 세션 길이
- 디바이스별 몰입도 분포
- 연령대별 몰입도 분포
- 첫 결제까지 걸린 기간

목적

→ **유저 플레이 행동과 몰입 구조 이해**

---

## 3. Revenue Structure Analysis

몰입도와 과금 관계 분석

분석 지표

- 몰입도별 평균 결제 금액
- 몰입도별 중앙값 결제 금액
- 과금 세그먼트 구성
- 몰입도별 매출 기여도

목적

→ **어떤 행동 패턴이 매출로 이어지는지 분석**

---

## 4. Insights

EDA 결과를 기반으로

- 핵심 인사이트 정리
- 게임 운영 전략 제안

---

# Key Metrics

| Metric | Value |
|------|------|
| Total Users | 3,024 |
| Total Revenue | $296,259 |
| Paying Users | 95.5% |
| ARPPU (Mean) | $102.6 |
| ARPPU (Median) | $12.0 |

---

# Key Findings

## 1. 몰입(세션 빈도)은 매출과 강하게 연결

세션 수가 증가할수록 평균 결제 금액 증가

High 몰입 그룹에서  
**Whale 유저 비율이 가장 높게 나타남**

운영 전략

- 중간 몰입 유저 → High 몰입 유저 전환
- 반복 플레이 유도 시스템 강화

예시

- 출석 이벤트
- 일일 미션 강화
- 반복 플레이 보상

---

## 2. 결제는 특정 시점 집중형이 아닌 분산 구조

첫 결제 발생 분포

| 기간 | 비율 |
|----|----|
| 0~10일 | 34.1% |
| 11~20일 | 31.8% |
| 21~30일 | 34.0% |

결제는 특정 시점이 아닌  
**서비스 초기 30일 동안 지속적으로 발생**

운영 전략

→ **30일 동안 지속되는 온보딩 이벤트 설계**

---

## 3. 연령보다 행동 기반 세그먼트가 더 중요

연령대별 몰입 차이는 크지 않음

하지만

몰입도 기준 세그먼트에서는  
플레이 행동 차이가 명확하게 나타남

운영 전략

→ **연령 기반 마케팅보다 행동 기반 운영 전략이 효과적**

---

## 4. 플랫폼 몰입 구조는 유사하지만 지출 수준은 차이

iOS 유저

- 평균 결제 금액 높음

Android 유저

- 유저 수 많음
- 지출 규모 상대적으로 낮음

운영 전략

- iOS → 프리미엄 상품 테스트
- Android → 할인 이벤트 및 프로모션

---

# Operational KPI

게임 운영 관점에서 지속적으로 추적해야 할 KPI

- High 몰입 유저 비율 (주간 변화)
- 중간 → High 몰입 전환율
- Whale 유저 비율 변화
- 플랫폼별 ARPPU (iOS vs Android)
- 세션 기반 첫 결제 전환율

---

# Project Structure
```
project
│
├─ data
│ └─ game_dataset.csv
│
├─ pages
│ ├─ 1_Overview.py
│ ├─ 2_Play_Patterns.py
│ ├─ 3_Revenue.py
│ └─ 4_Insights.py
│
├─ app.py
└─ README.md
```
---

# Tech Stack

- Python
- Pandas
- Matplotlib
- Streamlit

---

# Dataset

Kaggle Mobile Game Dataset

분석 데이터

- User behavior data
- Session activity
- Purchase behavior
- Demographic information

---

## Dashboard

Streamlit App

👉 https://bgnf9yjrhdtt8hzydapmdt.streamlit.app/

## Documentation

👉 https://www.notion.so/BI-302d9ef92ba280ac851dd118588862eb
---

# What I Learned

이 프로젝트를 통해

- 게임 서비스 데이터 분석 구조 이해
- 유저 행동 기반 세그먼트 분석
- 매출 구조 분석
- 데이터 기반 운영 인사이트 도출

을 경험했습니다.

단순 분석을 넘어  
**게임 운영 의사결정에 활용 가능한 BI 대시보드 구축**을 목표로 진행했습니다.
