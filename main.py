
import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# ============================================================
# 제목
# ============================================================
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("일별 박스오피스 데이터를 이용해 영화의 관객수 변화를 살펴봅니다.")


# ============================================================
# 데이터 불러오기
# ============================================================
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 데이터 변환
    for col in ["순위", "일관객", "누적관객", "스크린수", "상영횟수"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 날짜가 없는 데이터 제거
    df = df.dropna(subset=["날짜"])

    return df


df = load_data()


# ============================================================
# 데이터 정보
# ============================================================
st.caption(
    f"총 {len(df):,}개의 기록을 불러왔습니다."
)


# ============================================================
# 그래프 1
# 영화별 날짜에 따른 일관객 변화
# ============================================================
st.header("📈 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")


# ------------------------------------------------------------
# 그래프 1
# ------------------------------------------------------------
fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                  "일관객: %{y:,}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x",
    height=500
)

st.plotly_chart(fig1, use_container_width=True)


# ------------------------------------------------------------
# 그래프 1 설명
# ------------------------------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="예: 개봉 직후 관객수가 크게 증가한 뒤 점차 감소하는 모습을 볼 수 있다.",
    height=100,
    key="graph1_explanation"
)


# ============================================================
# 그래프 2
# 일관객 합계가 가장 큰 영화 5편
# ============================================================
st.divider()

st.header("📊 그래프 2. 일관객 합계가 가장 큰 영화 5편")

st.write(
    "전체 기간의 일관객을 영화별로 합산하여, 합계가 가장 큰 5편의 날짜별 관객수 변화를 비교합니다."
)


# 영화별 일관객 합계
movie_total = (
    df.dropna(subset=["영화명", "일관객"])
    .groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
)

top5_movies = movie_total.head(5)["영화명"].tolist()


# 상위 5편 데이터
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values(["날짜", "영화명"])


# ------------------------------------------------------------
# 그래프 2
# ------------------------------------------------------------
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                  "일관객: %{y:,}명<extra>%{fullData.name}</extra>"
)

fig2.update_layout(
    hovermode="x",
    height=600,
    legend_title_text="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ------------------------------------------------------------
# 그래프 2 설명
# ------------------------------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="예: 기간 전체에서 관객수가 가장 많았던 영화 5편의 흥행 추이를 비교할 수 있다.",
    height=100,
    key="graph2_explanation"
)


# ============================================================
# 그래프 3
# 날짜별 10위권 일관객 합계
# ============================================================
st.divider()

st.header("📊 그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "각 날짜의 박스오피스 10위권 영화가 기록한 일관객을 모두 더해 날짜별 전체 관객 규모를 확인합니다."
)


# 날짜별 일관객 합계
daily_total = (
    df.dropna(subset=["날짜", "일관객"])
    .groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)


# 일관객 합계가 가장 큰 3일
top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("일관객", ascending=False)
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 그래프 3 - 영역 그래프
# ------------------------------------------------------------
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)


# 상위 3일 표시
for i, row in top3_days.iterrows():

    date_text = row["날짜"].strftime("%Y-%m-%d")

    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=f"{i + 1}위<br>{date_text}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        ax=0,
        ay=-60,
        font=dict(size=13),
        bgcolor="white",
        bordercolor="gray",
        borderwidth=1,
        borderpad=5
    )


fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>"
                  "10위권 일관객 합계: %{y:,}명<extra></extra>"
)

fig3.update_layout(
    hovermode="x",
    height=600,
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계 (명)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# 상위 3일 정보
st.write("### 🏆 일관객 합계가 가장 컸던 날")

for i, row in top3_days.iterrows():

    date_text = row["날짜"].strftime("%Y년 %m월 %d일")

    st.write(
        f"**{i + 1}위 — {date_text}** : "
        f"{row['일관객']:,.0f}명"
    )


# ------------------------------------------------------------
# 그래프 3 설명
# ------------------------------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="예: 날짜별 영화관 전체 관객 규모의 변화를 알 수 있으며, 관객이 가장 많았던 날도 확인할 수 있다.",
    height=100,
    key="graph3_explanation"
)


# ============================================================
# 그래프 4
# 영화별 일관객 합계 TOP 10
# ============================================================
st.divider()

st.header("📊 그래프 4. 영화별 일관객 합계 TOP 10")

st.write(
    "이 기간 동안 일관객의 합계가 가장 큰 영화 10편을 비교합니다."
)


# ------------------------------------------------------------
# 영화별 일관객 합계 + 10위권에 든 날수 계산
# ------------------------------------------------------------
movie_summary = (
    df.dropna(subset=["영화명", "일관객"])
    .groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        상영일수=("날짜", "nunique")
    )
    .reset_index()
)


# 일관객 합계 기준 TOP 10
top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .copy()
)


# ------------------------------------------------------------
# 가로 막대그래프
# ------------------------------------------------------------
fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    custom_data=["상영일수"],
    title="영화별 일관객 합계 TOP 10",
    labels={
        "영화명": "영화",
        "일관객합계": "일관객 합계"
    }
)


# 마우스를 올렸을 때 표시되는 정보
fig4.update_traces(
    hovertemplate=
        "<b>%{y}</b><br>"
        "일관객 합계: %{x:,}명<br>"
        "10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
)


# 관객이 많은 영화가 위에 오도록 설정
fig4.update_layout(
    height=600,
    yaxis={
        "categoryorder": "total ascending"
    },
    xaxis_title="일관객 합계 (명)",
    yaxis_title="영화"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


# ------------------------------------------------------------
# 그래프 4 설명
# ------------------------------------------------------------
st.subheader("💡 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="예: 이 기간 동안 누적해서 가장 많은 관객을 모은 영화가 무엇인지 비교할 수 있다.",
    height=100,
    key="graph4_explanation"
)
