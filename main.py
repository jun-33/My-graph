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

    # 날짜: YYYYMMDD 형식의 숫자를 실제 날짜로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 데이터 변환
    df["순위"] = pd.to_numeric(df["순위"], errors="coerce")
    df["일관객"] = pd.to_numeric(df["일관객"], errors="coerce")
    df["누적관객"] = pd.to_numeric(df["누적관객"], errors="coerce")
    df["스크린수"] = pd.to_numeric(df["스크린수"], errors="coerce")
    df["상영횟수"] = pd.to_numeric(df["상영횟수"], errors="coerce")

    # 날짜가 잘못된 행 제거
    df = df.dropna(subset=["날짜"])

    return df


df = load_data()


# ============================================================
# 데이터 확인
# ============================================================
st.caption(
    f"총 {len(df):,}개의 기록을 불러왔습니다. "
    f"기간: {df['날짜'].min().date()} ~ {df['날짜'].max().date()}"
)


# ============================================================
# 그래프 1
# 영화별 날짜에 따른 일관객 변화
# ============================================================
st.header("📈 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 선택하면 해당 영화가 날짜별로 하루에 몇 명의 관객을 모았는지 볼 수 있습니다."
)

# 영화 목록
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")


# ============================================================
# 선 그래프
# ============================================================
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)


# ============================================================
# 그래프에서 알 수 있는 것
# ============================================================
st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "주말마다 일관객 수가 평일보다 훨씬 많다."
)


# ============================================================
# 앞으로 추가할 그래프 구역
# ============================================================
st.divider()

st.header("📊 그래프 2")
st.info("여기에 다음 그래프를 추가할 예정입니다.")


st.divider()

st.header("📊 그래프 3")
st.info("여기에 다음 그래프를 추가할 예정입니다.")


st.divider()

st.header("📊 그래프 4")
st.info("여기에 다음 그래프를 추가할 예정입니다.")
