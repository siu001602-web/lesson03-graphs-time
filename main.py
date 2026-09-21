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
st.info("💡 **이 그래프로 알 수 있는 것:** 기간 내 가장 많은 관객을 모은 흥행 TOP 5 영화들의 흥행 피크 시점과 상영 기간별 관객수 유지력을 한눈에 비교할 수 있습니다. (우측 범례 항목을 클릭해 특정 영화 선을 켜거나 끌 수 있습니다.)")

st.markdown("---")

# 6. 구역 3: 날짜별 10위권 전체 일관객 합계 영역 그래프
st.header("📌 Section 3. 날짜별 박스오피스 TOP 10 전체 관객수 합계")

# 날짜별 10위권 일관객 합계 계산
daily_total_df = df.groupby("날짜")["일관객"].sum().reset_index().sort_values("날짜")

# 일관객 합계가 가장 컸던 날 Top 3 추출
top3_days = daily_total_df.nlargest(3, "일관객")

# Plotly 영역 그래프(Area Chart) 생성
fig3 = px.area(
    daily_total_df,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 총합 추이",
    labels={"날짜": "날짜", "일관객": "10위권 일관객 총합(명)"},
)

# 마우스 호버 설정
fig3.update_traces(
    hovertemplate="<b>날짜</b>: %{x|%Y-%m-%d}<br><b>전체 일관객수</b>: %{y:,}명<extra></extra>",
    line_color="#2b5c8f",
)

# 관객수 Top 3 날짜를 그래프 상에 주석(Annotation)으로 표시
for i, row in enumerate(top3_days.itertuples(), start=1):
    date_str = row.날짜.strftime("%Y-%m-%d")
    audience_cnt = row.일관객

    fig3.add_annotation(
        x=row.날짜,
        y=audience_cnt,
        text=f"<b>{i}위: {date_str}</b><br>({audience_cnt:,}명)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        ax=0,
        ay=-40,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="red",
        borderwidth=1,
        borderpad=4,
    )

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# 그래프 해석 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 극장가 전체의 성수기/비수기 패턴과 연중 가장 많은 관객이 몰렸던 역대급 흥행 일자 Top 3를 한눈에 파악할 수 있습니다.")

st.markdown("---")

# 7. 구역 4: 기간 내 총 관객수 TOP 10 영화 가로 막대그래프
st.header("📌 Section 4. 기간 내 총 관객수 TOP 10 영화")

# 영화별 총 관객수 및 10위권 진입 일수(차트인 일수) 집계
top10_stats = (
    df.groupby("영화명")
    .agg(
        총관객수=("일관객", "sum"),
        차트인일수=("날짜", "nunique")
    )
    .reset_index()
    .nlargest(10, "총관객수")
)

# 관객수가 많은 영화가 위쪽에 나오도록 오름차순 정렬 (Plotly y축 표시 특성 반영)
top10_stats = top10_stats.sort_values("총관객수", ascending=True)

# Plotly 가로 막대그래프 생성
fig4 = px.bar(
    top10_stats,
    x="총관객수",
    y="영화명",
    orientation="h",
    title="기간 내 총 관객수 TOP 10 영화 순위",
    labels={"총관객수": "총 관객수(명)", "영화명": "영화 제목", "차트인일수": "10위권 진입 일수"},
    custom_data=["차트인일수"],
    text_auto=".2s",
)

# 마우스 호버 커스텀
fig4.update_traces(
    hovertemplate="<b>영화명</b>: %{y}<br><b>총 관객수</b>: %{x:,}명<br><b>10위권 진입 일수</b>: %{customdata[0]}일<extra></extra>",
    marker_color="#4C78A8",
)

# 그래프 출력
st.plotly_chart(fig4, use_container_width=True)

# 그래프 해석 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 기간 내 최상위 흥행을 기록한 10개 작품의 총 관객 규모와 흥행 기간(10위권 유지 일수)의 상관관계를 비교할 수 있습니다.")

st.markdown("---")

# 8. 구역 5: 월×요일별 일관객 합계 히트맵
st.header("📌 Section 5. 월×요일별 관객수 분포 히트맵")

# 날짜에서 월과 요일 추출
df_heatmap = df.copy()
df_heatmap["월"] = df_heatmap["날짜"].dt.month.astype(str) + "월"

# 요일 한글 변환 및 순서 고정 (월요일 ~ 일요일)
days_order = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
day_map = {
    "Monday": "월요일",
    "Tuesday": "화요일",
    "Wednesday": "수요일",
    "Thursday": "목요일",
    "Friday": "금요일",
    "Saturday": "토요일",
    "Sunday": "일요일",
}
df_heatmap["요일"] = df_heatmap["날짜"].dt.day_name().map(day_map)

# 월(1월~12월) 순서 정렬용
months_order = [f"{m}월" for m in range(1, 13)]

# 월×요일별 일관객 합계 집계
heatmap_pivot = (
    df_heatmap.groupby(["월", "요일"])["일관객"]
    .sum()
    .reset_index()
)

# 피벗 테이블 형태로 변환 (행: 요일, 열: 월)
pivot_table = heatmap_pivot.pivot(index="요일", columns="월", values="일관객")

# 순서 재정렬 (월~일, 1월~12월)
pivot_table = pivot_table.reindex(index=days_order, columns=[m for m in months_order if m in pivot_table.columns])

# Plotly 히트맵 생성 (관객이 많을수록 진한 색상)
fig5 = px.imshow(
    pivot_table,
    labels=dict(x="월", y="요일", color="일관객 합계(명)"),
    x=pivot_table.columns,
    y=pivot_table.index,
    color_continuous_scale="Blues",  # 값이 클수록 진한 푸른색
    title="월 및 요일별 일관객 합계 히트맵",
    text_auto=",d",  # 수치 콤마 표시
)

# 마우스 호버 커스텀
fig5.update_traces(
    hovertemplate="<b>%{x} %{y}</b><br><b>일관객 합계</b>: %{z:,}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig5, use_container_width=True)

# 그래프 해석 문구 자리
st.info("💡 **이 그래프로 알 수 있는 것:** 월별 성수기/비수기와 요일별(주말 vs 평일) 관객 집중 현상을 종합적으로 분석하여 극장 방문이 가장 활발한 시기를 한눈에 파악할 수 있습니다.")

st.markdown("---")

# 9. 구역 6: 추후 그래프 추가용 구역
st.header("📌 Section 6. 추가 그래프 구역")
st.write("앞으로 시간 축 기반의 새로운 그래프가 이곳에 추가될 예정입니다.")

st.info("💡 **이 그래프로 알 수 있는 것:** (새로운 그래프에 대한 분석 설명이 들어갈 자리입니다.)")
