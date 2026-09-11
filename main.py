# ============================================================
# 그래프 5
# 월 × 요일별 일관객 합계 히트맵
# ============================================================
st.divider()

st.header("📊 그래프 5. 월 × 요일별 일관객 합계")

st.write(
    "날짜에서 월과 요일을 추출하여, "
    "각 월·요일에 기록된 10위권 영화의 일관객 합계를 히트맵으로 보여 줍니다."
)


# ------------------------------------------------------------
# 월과 요일 추출
# ------------------------------------------------------------
heatmap_df = df.dropna(subset=["날짜", "일관객"]).copy()

heatmap_df["월"] = heatmap_df["날짜"].dt.month

# 요일 번호: 월요일=0 ~ 일요일=6
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


# ------------------------------------------------------------
# 월 × 요일별 일관객 합계 계산
# ------------------------------------------------------------
monthly_weekday_total = (
    heatmap_df
    .groupby(["월", "요일"], as_index=False)["일관객"]
    .sum()
)


# ------------------------------------------------------------
# 히트맵용 표 만들기
# ------------------------------------------------------------
heatmap_table = monthly_weekday_total.pivot(
    index="월",
    columns="요일",
    values="일관객"
)

# 월요일 → 일요일 순서로 정렬
heatmap_table = heatmap_table.reindex(
    columns=weekday_order
)

# 1월 → 12월 순서로 정렬
heatmap_table = heatmap_table.reindex(
    range(1, 13)
)


# ------------------------------------------------------------
# 히트맵
# ------------------------------------------------------------
fig5 = px.imshow(
    heatmap_table,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    x=weekday_order,
    y=[f"{month}월" for month in range(1, 13)],
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="Blues",
    title="월 × 요일별 10위권 일관객 합계"
)


# ------------------------------------------------------------
# 그래프 설정
# ------------------------------------------------------------
fig5.update_layout(
    height=650,
    xaxis_title="요일",
    yaxis_title="월"
)

fig5.update_traces(
    hovertemplate=
        "%{y} %{x}<br>"
        "일관객 합계: %{z:,}명"
        "<extra></extra>"
)


st.plotly_chart(
    fig5,
    use_container_width=True
)


# ------------------------------------------------------------
# 그래프 5 설명
# ------------------------------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="예: 어느 월의 어떤 요일에 영화 관객이 많았는지 한눈에 비교할 수 있다.",
    height=100,
    key="graph5_explanation"
)
