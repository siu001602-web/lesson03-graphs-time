import pandas as pd
import plotly.express as px
import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")

# 2. 데이터 불러오기 및 전처리
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    # 데이터 로드
    df = pd.read_csv(DATA_URL)

    # 날짜 열(YYYYMMDD 형태의 숫자/문자열)을 진짜 datetime 객체로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d", errors="coerce")

    return df


df = load_data()

# 3. 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("1년치 일별 박스오피스 데이터를 바탕으로 시계열 흐름을 분석합니다.")

st.markdown("---")

# 4. 구역 1: 개별 영화의 일별 관객수 변화
st.header("📌 Section 1. 영화별 일관객수 추이")

# 영화 목록 추출 (영화명 기준)
movie_list = df["영화명"].dropna().unique().tolist()
movie_list.sort()

# 드롭다운 선택 상자
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

if selected_movie:
    # 선택된 영화 데이터 필터링
    filtered_df = df[df["영화명"] == selected_movie].sort_values("날짜")

    # Plotly 선 그래프 생성
    fig1 = px.line(
        filtered_df,
        x="날짜",
        y="일관객",
        title=f"'{selected_movie}' 날짜별 일관객수 변화",
        labels={"날짜": "날짜", "일관객": "일일 관객수(명)"},
        markers=True,
    )

    # 마우스 호버 시 날짜와 관객수 표시 설정
    fig1.update_traces(
        hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>일관객수</b>: %{y:,}명<extra></extra>"
    )

    # 그래프 출력
    st.plotly_chart(fig1, use_container_width=True)

    # 그래프 해석 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** 선택한 영화의 상영 기간별 관객수 증감 추이와 주말/평일 간의 관객수 격차 변화를 확인할 수 있습니다.")

st.markdown("---")

# 5. 구역 2: 기간 내 관객수 상위 5개 영화 비교
st.header("📌 Section 2. 누적 일관객수 TOP 5 영화 비교")

# 데이터 내 전체 기간 동안의 일관객수 합계가 가장 높은 상위 5개 영화 추출
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index
    .tolist()
)

# TOP 5 영화 데이터 필터링
top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

# Plotly 다중 선 그래프 생성 (color='영화명'으로 구분)
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="기간 내 일관객수 합계 TOP 5 영화 추이 비교",
    labels={"날짜": "날짜", "일관객": "일일 관객수(명)", "영화명": "영화 제목"},
    markers=False,
)

# Hover format 및 범례 설정
fig2.update_traces(
    hovertemplate="<b>영화명</b>: %{fullData.name}<br><b>날짜</b>: %{x|%Y-%m-%d}<br><b>일관객수</b>: %{y:,}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 기간 내 가장 많은 관객을 모은 흥행 TOP 5 영화들의 흥행```python
import plotly.express as px

# 1. 영화별 누적 관객수 계산 및 상위 10개 영화 추출
top10_movies = (
    df.groupby('movieNm')['audiCnt']
    .sum()
    .nlargest(10)
    .reset_index()
)

# 2. 각 영화별 10위권 이내 진입 일수 계산
# (데이터프레임에 rank 칼럼이 없더라도 TOP 10 데이터셋 내 일수를 집계)
top10_days = (
    df[df['movieNm'].isin(top10_movies['movieNm'])]
    .groupby('movieNm')['targetDt']
    .nunique()
    .reset_index(name='top10_days')
)

# 3. 데이터 합치기
top10_df = top10_movies.merge(top10_days, on='movieNm')

# 4. 관객 수가 많은 영화가 위에 오도록 정렬 (Plotly y축 역순 정렬 대응)
top10_df = top10_df.sort_values(by='audiCnt', ascending=True)

# 5. 가로 막대그래프 생성
fig4 = px.bar(
    top10_df,
    x='audiCnt',
    y='movieNm',
    orientation='h',
    title='기간 내 누적 관객수 TOP 10 영화',
    labels={
        'audiCnt': '총 관객수(명)',
        'movieNm': '영화 제목',
        'top10_days': '10
