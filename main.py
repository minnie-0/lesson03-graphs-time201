import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# 기본 설정
# ==========================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# ==========================================
# 데이터 불러오기
# ==========================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

df = pd.read_csv(DATA_URL)

# 날짜를 실제 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(
    df["날짜"].astype(str),
    format="%Y%m%d"
)

# 숫자형 열 변환
numeric_columns = [
    "순위",
    "영화코드",
    "일관객",
    "누적관객",
    "스크린수",
    "상영횟수"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.sort_values(["날짜", "순위"])


# ==========================================
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# ==========================================

st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객"
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis=dict(tickformat="%Y-%m-%d"),
    yaxis=dict(tickformat=",")
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")

st.text_input(
    "문구를 입력하세요.",
    placeholder="예: 영화의 개봉 이후 일관객이 어떻게 변화했는지 알 수 있다.",
    key="graph1_comment"
)


# ==========================================
# 그래프 2. 일관객 합계 상위 5편 비교
# ==========================================

st.divider()

st.header("그래프 2. 일관객 합계가 가장 큰 영화 5편")

top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

top5_df = df[df["영화명"].isin(top5_movies)].copy()
top5_df = top5_df.sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="이 기간 일관객 합계 상위 5편의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra>%{fullData.name}</extra>"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis=dict(tickformat="%Y-%m-%d"),
    yaxis=dict(tickformat=","),
    legend=dict(title="영화")
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")

st.text_input(
    "문구를 입력하세요.",
    placeholder="이 그래프에서 알 수 있는 내용을 입력하세요.",
    key="graph2_comment"
)


# ==========================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ==========================================

st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("일관객", ascending=False)
)

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>10위권 일관객 합계: %{y:,}명<extra></extra>"
)

annotations = []

for _, row in top3_days.iterrows():
    annotations.append(
        dict(
            x=row["날짜"],
            y=row["일관객"],
            text=row["날짜"].strftime("%Y-%m-%d"),
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-45
        )
    )

fig3.update_layout(
    hovermode="x unified",
    xaxis=dict(tickformat="%Y-%m-%d"),
    yaxis=dict(tickformat=","),
    annotations=annotations
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")

st.text_input(
    "문구를 입력하세요.",
    placeholder="이 그래프에서 알 수 있는 내용을 입력하세요.",
    key="graph3_comment"
)


# ==========================================
# 그래프 4. 영화별 전체 기간 일관객 TOP 10
# ==========================================

st.divider()

st.header("그래프 4. 영화별 전체 기간 일관객 TOP 10")

movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        등장일수=("날짜", "nunique")
    )
    .reset_index()
)

top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .sort_values("일관객합계", ascending=True)
)

fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 전체 기간 일관객 TOP 10",
    labels={
        "일관객합계": "일관객 합계",
        "영화명": "영화"
    },
    custom_data=["등장일수"]
)

fig4.update_traces(
    hovertemplate=(
        "영화: %{y}"
        "<br>일관객 합계: %{x:,}명"
        "<br>10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis=dict(tickformat=","),
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")

st.text_input(
    "문구를 입력하세요.",
    placeholder="이 그래프에서 알 수 있는 내용을 입력하세요.",
    key="graph4_comment"
)


# ==========================================
# 그래프 5. 월 × 요일별 일관객 합계
# ==========================================

st.divider()

st.header("그래프 5. 월 × 요일별 일관객 합계")

heatmap_df = df.copy()

# 날짜에서 월과 요일 추출
heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_order = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일"
]

heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek.map(
    dict(enumerate(weekday_order))
)

# 월 × 요일별 일관객 합계
heatmap_data = (
    heatmap_df
    .groupby(["월", "요일"])["일관객"]
    .sum()
    .reset_index()
)

# 피벗
heatmap_pivot = heatmap_data.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

# 월요일 → 일요일 순서
heatmap_pivot = heatmap_pivot.reindex(
    columns=weekday_order
)

# 1월 → 12월 순서
heatmap_pivot = heatmap_pivot.reindex(
    index=range(1, 13)
)

fig5 = px.imshow(
    heatmap_pivot,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    x=weekday_order,
    y=heatmap_pivot.index,
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="Blues",
    title="월 × 요일별 일관객 합계"
)

fig5.update_traces(
    hovertemplate=(
        "%{y}월 %{x}"
        "<br>일관객 합계: %{z:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis=dict(
        categoryorder="array",
        categoryarray=weekday_order
    ),
    yaxis=dict(
        dtick=1,
        autorange="reversed"
    )
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")

st.text_input(
    "문구를 입력하세요.",
    placeholder="이 그래프에서 알 수 있는 내용을 입력하세요.",
    key="graph5_comment"
)
