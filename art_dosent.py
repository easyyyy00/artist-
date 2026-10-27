import pandas as pd
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 헤더
# ==========================================
st.set_page_config(
    page_title="디지털 미술관 도슨트", page_icon="🎨", layout="wide"
)

st.title("🎨 나만의 디지털 미술관 도슨트")
st.subheader(
    "당신의 미술 취향과 관람 시간에 맞춰 명화와 맞춤 해설을 추천해 드립니다."
)
st.write("---")

# ==========================================
# 2. 자체 명화 데이터베이스 (리스트 내 딕셔너리 구조)
# ==========================================
ARTWORKS = [
    {
        "id": 1,
        "title": "별이 빛나는 밤",
        "artist": "빈센트 반 고흐",
        "movement": "후기 인상주의",
        "mood": "신비로움",
        "time_req": 20,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
        "desc": "고흐가 아를의 정신병원에서 바라본 밤하늘을 격렬한 붓터치와 소용돌이치는 구도로 표현한 대표작입니다.",
        "point": "소용돌이치는 밤하늘의 강렬한 노란색과 파란색의 대비에 주목해 보세요.",
    },
    {
        "id": 2,
        "title": "인상, 일출",
        "artist": "클로드 모네",
        "movement": "인상주의",
        "mood": "차분함",
        "time_req": 15,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Monet_-_Impression%2C_Sunrise.jpg/1280px-Monet_-_Impression%2C_Sunrise.jpg",
        "desc": "'인상주의'라는 사조의 이름을 탄생시킨 모네의 역사적인 작품입니다.",
        "point": "정교한 형태보다는 순간적인 빛과 안개의 느낌을 표현한 색채를 관찰해 보세요.",
    },
    {
        "id": 3,
        "title": "아비뇽의 수녀들",
        "artist": "파블로 피카소",
        "movement": "입체주의",
        "mood": "독창적",
        "time_req": 30,
        "image": "https://upload.wikimedia.org/wikipedia/en/4/4c/Les_Demoiselles_d%27Avignon.jpg",
        "desc": "전통적인 원근법을 깨뜨리고 다각도의 시점을 한 화면에 담아낸 입체주의의 시작을 알린 작품입니다.",
        "point": "여인들의 얼굴이 기하학적 도형과 아프리카 가면 형태로 입체화된 모습을 확인해 보세요.",
    },
    {
        "id": 4,
        "title": "기억의 지속",
        "artist": "살바도르 달리",
        "movement": "초현실주의",
        "mood": "신비로움",
        "time_req": 25,
        "image": "https://upload.wikimedia.org/wikipedia/en/d/dd/The_Persistence_of_Memory.jpg",
        "desc": "녹아내리는 시계들을 통해 시간의 상대성과 무의식의 세계를 그린 초현실주의 거장의 대표작입니다.",
        "point": "사막 풍경 속 시계가 흘러내리는 기괴하고도 신비로운 꿈속 분위기를 느껴보세요.",
    },
    {
        "id": 5,
        "title": "모나리자",
        "artist": "레오나르도 다 빈치",
        "movement": "르네상스",
        "mood": "차분함",
        "time_req": 30,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg/1280px-Mona_Lisa%2C_by_Leonardo_da_Vinci%2C_from_C2RMF_retouched.jpg",
        "desc": "스푸마토 기법을 사용하여 윤곽선을 부드럽게 처리한 세계에서 가장 유명한 초상화입니다.",
        "point": "눈썹이 없는 미묘한 미소와 배경의 아득한 풍경 구도를 관찰해 보세요.",
    },
]

# ==========================================
# 3. 사용자 입력 받기 (사이드바 위젯)
# ==========================================
st.sidebar.header("🎯 관람 옵션 선택")

# 선택 옵션 목록 동적 추출
movements = ["전체"] + sorted(list(set(item["movement"] for item in ARTWORKS)))
moods = ["전체"] + sorted(list(set(item["mood"] for item in ARTWORKS)))

# 입력 위젯 구성
selected_movement = st.sidebar.selectbox("선호 미술 사조를 선택하세요", movements)
selected_mood = st.sidebar.radio("원하는 분위기를 선택하세요", moods)
max_time = st.sidebar.slider(
    "총 관람 가능 시간 (분)", min_value=15, max_value=120, value=60, step=5
)

# ==========================================
# 4. 조건 필터링 알고리즘 및 예외 처리
# ==========================================
filtered_artworks = []
is_default = False

# 사용자가 선택한 조건(사조, 분위기, 소요시간) 만족 여부 다중 조건 검색
for art in ARTWORKS:
    match_movement = (selected_movement == "전체") or (
        art["movement"] == selected_movement
    )
    match_mood = (selected_mood == "전체") or (art["mood"] == selected_mood)
    match_time = art["time_req"] <= max_time

    if match_movement and match_mood and match_time:
        filtered_artworks.append(art)

# [예외 처리] 검색 결과가 없을 경우 예외 메시지 출력 후 기본 대표 명화 선별
if not filtered_artworks:
    st.warning(
        "⚠️ 일치하는 작품이 없습니다. 선택하신 조건에 맞는 작품을 찾지 못하여 기본 대표 명화를 자동으로 추천해 드립니다."
    )
    # 입력된 시간 내에 감상 가능한 기본 대표 명화 추출
    filtered_artworks = [
        art for art in ARTWORKS if art["time_req"] <= max_time
    ]
    if not filtered_artworks:  # 입력 시간이 너무 짧은 경우 전체 중 1개 기본 출력
        filtered_artworks = [ARTWORKS[0]]
    is_default = True

# ==========================================
# 5. 결과 화면 출력 (카드 형태 시각화)
# ==========================================
if is_default:
    st.markdown("### 🏛️ 기본 대표 명화 컬렉션")
else:
    st.markdown(
        f"### 🏛️ 맞춤 추천 작품 (총 {len(filtered_artworks)}개 작품)"
    )

# container 및 columns 위젯을 사용한 카드형 레이아웃 구성
for art in filtered_artworks:
    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(
                art["image"],
                caption=f"<{art['title']}>",
                use_container_width=True,
            )

        with col2:
            st.subheader(f"{art['title']} — {art['artist']}")
            st.write(
                f"**미술 사조:** {art['movement']} | **분위기:** {art['mood']} | **권장 감상시간:** {art['time_req']}분"
            )
            st.markdown(f"**📖 요약 해설:**\n{art['desc']}")
            st.info(f"💡 **핵심 감상 포인트:** {art['point']}")

        st.divider()

# ==========================================
# 6. 갤러리 도록 요약 및 CSV 저장 기능
# ==========================================
st.subheader("📋 나만의 갤러리 도록 요약")

# 결과 목록을 데이터프레임으로 정리
df_summary = pd.DataFrame(filtered_artworks)[
    ["title", "artist", "movement", "mood", "time_req"]
]
df_summary.columns = [
    "작품명",
    "작가명",
    "미술 사조",
    "분위기",
    "소요 시간(분)",
]

# 요약 데이터프레임 표 출력
st.dataframe(df_summary, use_container_width=True)

# CSV 파일 다운로드 버튼 생성 (한글 깨짐 방지 utf-8-sig 인코딩 적용)
csv_data = df_summary.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="📥 갤러리 도록 다운로드 (CSV)",
    data=csv_data,
    file_name="gallery_catalog.csv",
    mime="text/csv",
)
```<FollowUp>
<SuggestedQuestions>
1. 보고서에 첨부할 '프로젝트 구현 및 실행 화면 설명' 파트도 추가로 정리해 드릴까요?
2. 이 코드를 터미널에서 실행하는 방법이나 필요한 라이브러리 설치 안내가 필요하신가요?
</SuggestedQuestions>
</FollowUp>
