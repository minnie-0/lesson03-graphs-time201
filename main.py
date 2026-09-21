# ==========================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ==========================================

st.divider()
st.header("그래프 3. 날짜별 10위권 일관객 합계")

# 날짜별 10위권 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 합계가 가장 큰 날 3일
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

# 마우스를 올렸을 때 날짜와 합계 표시
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>10위권 일관객 합계: %{y:,}명<extra></extra>"
)

# 상위 3일을 그래프 위에 표시
annotations = []

for _, row in top3_days.iterrows():
    annotations.append(
        dict(
            x=row["날짜"],
            y=row["일관객"],
            text=f"{row['날짜'].strftime('%Y-%m-%d')}<br>{row['일관객']:,}명",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-45
        )
    )

fig3.update_layout(
    hovermode="x unified",
    xaxis=dict(
        tickformat="%Y-%m-%d"
    ),
    yaxis=dict(
        tickformat=","
    ),
    annotations=annotations
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")

st.text_input(
    "문구를 입력하세요.",
    placeholder="이 그래프에서 알 수 있는 내용을 입력하세요.",
    key="graph3_comment"
)
