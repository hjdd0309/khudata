import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_excel('result.xlsx')

df = load_data()
# 입력값 받기
degree_map = {"고졸 이하":1, "전문대":2, "대학교":3, "대학원 이상":5}
intern_map = {"없음":2, "있음":1}
major_map = {"불만족":1, "보통":2, "만족":2}
degree = st.selectbox("학위 수준", list(degree_map.keys()))
intern = st.radio("인턴 경험 여부", list(intern_map.keys()))
job_try = st.slider("일자리 지원 횟수", 0, 10)
major_satisfaction = st.radio("전공 만족도", list(major_map.keys()))
life_satisfaction = st.slider("삶의 만족도", 1, 10)

# 입력값 코드화
input_degree = degree_map[degree]
input_intern = intern_map[intern]
input_major = major_map[major_satisfaction]
input_life = life_satisfaction

# 유사 데이터 필터링
filtered = df[
    (df['학위'] == input_degree) &
    (df['인턴경험'] == input_intern) &
    (df['전공 만족 여부'] == input_major) &
    (df['삶의 만족도'] == input_life)
]

# 유사 집단 비교 정보
if not filtered.empty:
    avg_job_try = filtered['일자리 지원 회수'].mean()
    st.write(f"유사 집단의 평균 일자리 지원 횟수: {avg_job_try:.1f}회")
else:
    st.write("유사한 데이터가 부족합니다. 기본 규칙으로 유형을 분류합니다.")

# 기존 유형 분류 함수
def classify(degree, intern, job_try, major_satisfaction, life_satisfaction):
    if job_try == 0 and major_satisfaction == "불만족":
        return "🌱 무방향형"
    elif intern == "있음" and job_try > 3 and major_satisfaction == "만족":
        return "🔧 스펙형"
    elif job_try > 3 and intern == "없음":
        return "🔥 열정형"
    elif job_try > 0 and life_satisfaction <= 3:
        return "🧊 좌절형"
    else:
        return "🌀 혼란형"

def get_policy(neet_type):
    policy_map = {
        "🌱 무방향형": ("청년 진로상담소", "https://youth.seoul.go.kr/site/main/content/youthcenter"),
        "🔧 스펙형": ("지역 일경험 프로그램", "https://www.work.go.kr/youth/"),
        "🔥 열정형": ("K-Digital Training", "https://kdt.go.kr/"),
        "🧊 좌절형": ("청년 마음건강 지원", "https://www.bokjiro.go.kr/"),
        "🌀 혼란형": ("커리어 설계 멘토링", "https://www.hrd.go.kr/")
    }
    return policy_map.get(neet_type)

# 최종 유형 및 정책 출력
neet_type = classify(degree, intern, job_try, major_satisfaction, life_satisfaction)
policy_name, policy_link = get_policy(neet_type)
st.subheader(f"당신의 유형: {neet_type}")
st.markdown(f"**추천 정책:** [{policy_name}]({policy_link})")

# ✅ 여기에 부족한 항목 분석 기능 추가
# 추가 변수 정규화 기반 부족 탐색
features = ['학위', '인턴경험', '전공 만족 여부', '삶의 만족도',
            '일자리 지원 회수', '외국어회화', '토익토플', 'IT교육']
df_clean = df[features].dropna()

scaler = MinMaxScaler()
scaled = scaler.fit_transform(df_clean)
feature_means = pd.Series(scaled.mean(axis=0), index=features)

# 사용자 입력에 없는 항목도 더 받기
lang_map = {"없음":1, "보통":2, "유창":3}
binary_map = {"없음":0, "있음":1}
lang = st.radio("외국어 회화 수준", list(lang_map.keys()))
toeic = st.radio("토익/토플 경험", list(binary_map.keys()))
it = st.radio("IT 교육 이수 여부", list(binary_map.keys()))

user_row = pd.DataFrame([{
    '학위': input_degree,
    '인턴경험': input_intern,
    '전공 만족 여부': input_major,
    '삶의 만족도': input_life,
    '일자리 지원 회수': job_try,
    '외국어회화': lang_map[lang],
    '토익토플': binary_map[toeic],
    'IT교육': binary_map[it]
}])
user_scaled = scaler.transform(user_row)[0]
user_series = pd.Series(user_scaled, index=features)

# 평균보다 15% 이상 낮은 항목 찾기
threshold = 0.15
weaks = [col for col in features if user_series[col] < feature_means[col] - threshold]

# 부족 항목별 정책 추천
policy_map = {
    '학위': ("학력 향상 프로그램", "https://www.nile.or.kr/"),
    '인턴경험': ("청년 인턴십 매칭 플랫폼", "https://www.work.go.kr/youth/"),
    '전공 만족 여부': ("진로 설계 멘토링", "https://www.hrd.go.kr/"),
    '삶의 만족도': ("청년 마음건강 지원", "https://www.bokjiro.go.kr/"),
    '일자리 지원 회수': ("1:1 진로코칭", "https://youth.seoul.go.kr/"),
    '외국어회화': ("국비 외국어 교육", "https://www.kosaf.go.kr/"),
    '토익토플': ("스펙 향상 온라인 과정", "https://kdt.go.kr/"),
    'IT교육': ("K-Digital Training", "https://kdt.go.kr/")
}

if weaks:
    st.markdown("---")
    st.subheader("📉 당신에게 부족한 항목 & 맞춤 정책")
    for w in weaks:
        name, link = policy_map[w]
        st.markdown(f"- **{w}** → [{name}]({link})")
else:
    st.success("👏 유사 청년들에 비해 당신은 모든 영역에서 평균 이상입니다.")
