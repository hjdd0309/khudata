# khudata(니트족 구제를 위한 데이터 분석 및 해결방안)
NEET족 구제하기 - KHU'DATA 3조
본 프로젝트는 청년 NEET(Not in Education, Employment, or Training) 족 문제 해결을 위한 데이터 분석 및 정책 제안 서비스입니다. NEET 상태의 청년들을 판별하고, 그들에게 맞춤형 정책을 제안하는 것을 목표로 합니다.

📌 프로젝트 개요
프로젝트명: NEET족 구제하기

주최: KHUDA 7기

팀원: 조민우, 성민지, 정시찬, 김현정, 유민아, 박태호

❓ 주제 선정 이유
NEET족은 교육도, 직업 훈련도, 취업도 하지 않는 청년층으로 사회적 위험군으로 분류됨

이들의 비율 증가는 경제 성장 저해, 인구 구조 악화, 삶의 질 저하 등 사회적 문제를 유발

데이터를 기반으로 한 진단 및 정책 추천으로 실질적인 도움을 줄 수 있는 시스템 개발 필요

📂 사용 데이터
청년패널조사(YP): 설문 기반의 청년 개인 데이터

정부 청년정책 API: 현재 시행 중인 다양한 정책 정보

⚙ 데이터 전처리
NEET 여부 판단 가능한 변수 15개 선별

결측치 제거 및 중요 피처 추출

변수 매핑 및 재정의

상관관계 분석 수행

🤖 모델링
모델: Logistic Regression

성능 지표:

R² Score: 0.5951

MAE(Mean Absolute Error): 0.144

📊 결과 및 의의
NEET 여부를 데이터 기반으로 예측하는 모델 개발

개인별 NEET 지수 제공 가능

정부 정책과 연결되는 추천 시스템 가능성 제시

NEET 특성에 맞는 정책 매칭으로 현실적 청년 지원 가능

⚠️ 한계점 및 향후 방향
극단값에 대한 예측 성능 미흡

신규 사용자에 대한 일반화 부족

메뉴 및 검색 기능 강화 필요

웹 서비스 범위 확장 필요
