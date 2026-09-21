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

# 날짜 열을 실제 날짜 형식으로 변환
df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

# 숫자형 열 변환
numeric_columns = ["순위", "영화코드", "일관객", "누적관객", "스크린수", "상영횟수"]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 날짜순으로 정렬
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

fig = px.line(
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

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickformat="%Y-%m-%d"
    ),
    yaxis=dict(
        tickformat=","
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.text_input(
    "문구를 입력하세요.",
    placeholder="예: 영화의 개봉 이후 일관객이 어떻게 변화했는지 알 수 있다.",
    key="graph1_comment"
)


# ==========================================
# 앞으로 추가할 그래프
# ==========================================

st.divider()
st.header("그래프 2")
st.info("앞으로 추가할 그래프 영역입니다.")

st.markdown("**이 그래프로 알 수 있는 것:**")
st.text_input(
    "문구를 입력하세요.",
    placeholder="이 그래프에서 알 수 있는 내용을 입력하세요.",
    key="graph2_comment"
)


st.divider()
st.header("그래프 3")
st.info("앞으로 추가할 그래프 영역입니다.")

st.markdown("**이 그래프로 알 수 있는 것:**")
st.text_input(
    "문구를 입력하세요.",
    placeholder="이 그래프에서 알 수 있는 내용을 입력하세요.",
    key="graph3_comment"
)
