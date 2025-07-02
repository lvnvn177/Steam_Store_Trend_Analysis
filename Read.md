---

## 🎯 프로젝트 주제 

> “Steam API를 활용한 2020~2025 게임 트렌드 분석 및 인디 게임 성공 요소 탐색”
> 

---

## 🧭 전체 단계 요약

1. **목표 및 분석 질문 정의**
2. **Steam API 이해 및 데이터 수집**
3. **데이터 저장 및 가공**
4. **EDA 및 시각화**
5. **트렌드 분석 및 인사이트 도출**
6. **보고서 및 대시보드 제작**
7. **확장/응용 방향 (게임 기획 또는 유튜브 콘텐츠와 연결)**

---

## 🔍 1. 목표 및 분석 질문 정의

### 🎯 목적

- 최근 5년간 **어떤 장르/태그가 트렌디한지**
- **유저 리뷰 수와 평점의 관계**
- **인디 게임의 성공 요인 분석**
- **무료/유료 게임 비율 변화**
- **한글화 지원이 유저 반응에 어떤 영향을 주는지**

### 📌 예시 질문

- 2020~2025년 가장 많이 출시된 장르는?
- 'Deckbuilding', 'Souls-like' 같은 태그는 얼마나 성장했는가?
- 평균 리뷰 수가 많은 게임의 가격대는?
- 한글 지원 여부가 있는 게임이 더 많은 유저 평가를 받는가?

---

## 🔌 2. Steam API 이해 및 데이터 수집

### 📘 주요 API 목록

| API | 설명 |
| --- | --- |
| `GetAppList` | 전체 게임(AppID) 목록 가져오기 |
| `GetAppDetails` (비공식) | 게임별 상세 정보 (장르, 태그, 가격 등) |
| `SteamSpy` API | 더 정제된 게임 통계 정보 (유저 수, 평가 등) |
| → https://steamspy.com/api.php |  |
| `store.steampowered.com/api/appdetails?appids=XXXX` | 공식 App Detail API (title, genre, 가격, 스크린샷 등 제공) |

---

### 🔧 예시 수집 코드 (Python)

```python
import requests

# 예: Steam 앱 리스트 가져오기
url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
response = requests.get(url)
apps = response.json()['applist']['apps']

# 특정 AppID의 정보 가져오기
app_id = 1091500  # 예: Cyberpunk 2077
details_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
res = requests.get(details_url).json()

game_info = res[str(app_id)]['data']
print(game_info['name'], game_info['genres'], game_info['release_date'])

```

---

## 🧹 3. 데이터 저장 및 가공

### ✅ 방법

- 크롤링한 데이터를 **CSV나 SQLite**로 저장
- 수집 필드 예시:
    - AppID
    - Name
    - Release Date
    - Genres
    - Tags
    - Price (USD)
    - is_free
    - Positive/Negative Reviews (SteamSpy API 기준)
    - Supported Languages

### ⚠️ 팁

- API 호출이 많으니 `time.sleep()` 넣고 **rate limit** 주의
- `pandas`로 바로 `DataFrame` 구성해서 `to_csv()`로 저장 추천

---

## 📊 4. EDA 및 시각화 (Exploratory Data Analysis)

### 시각화 예시

- 연도별 출시 게임 수 (막대그래프)
- 태그/장르별 출현 빈도 변화 (꺾은선/누적막대)
- 무료/유료 게임 비율 변화
- 리뷰 수 vs 가격 산점도
- 긍정 리뷰율 상위 게임 리스트 (Top N)

### 라이브러리 추천

- `matplotlib`, `seaborn`, `plotly`, `wordcloud`
- 인터랙티브: `plotly.express` or `Looker Studio`

---

## 🧠 5. 트렌드 분석 및 인사이트 도출

### 인사이트 예시

- 인디 게임의 평균 가격은 감소 추세지만 리뷰 수는 오히려 증가
- ‘roguelike’, ‘deckbuilder’ 태그는 2022~2025년 급증
- 한글 지원 게임은 평균 리뷰 수가 1.4배 많음 → 현지화 중요
- 출시 후 첫 6개월 내 리뷰 수가 전체의 80% 차지 → 초기 마케팅 중요

---

## 🧾 6. 보고서, 발표자료 또는 대시보드 제작

### 추천 형식

- **Jupyter Notebook 포트폴리오**
- **PDF 또는 PPT 형식 리포트**
- **Streamlit 앱으로 웹 대시보드 제작**
- **Looker Studio 시각화 페이지로 공유**

---

## 🧩 7. 확장 방향: 내 게임 또는 유튜브에 연결

### 🎮 게임 기획으로 확장

- 내가 만들고 있는 게임 장르의 시장성 분석
- 유저들이 선호하는 가격대, 태그 조합 참고
- 출시 시점(계절, 경쟁작 등) 판단

### 📹 유튜브 콘텐츠로 확장

- "2025년 스팀에서 가장 많이 팔린 인디 게임 TOP 10 분석"
- "Roguelike 장르가 이렇게 많아진 이유는?"
- 실제 데이터 기반으로 **해설형 영상** 제작 가능

---

## ✨ 결론: 이렇게 하면 강력한 포트폴리오가 됩니다

- **실제 API 기반 수집 + 분석**
- **현업 마케팅/기획/리서치 관점 인사이트**
- **당신의 개발/유튜브 콘텐츠와 연동되는 주제**

---

## 📁 원하시면 도와드릴 수 있는 것

- SteamSpy/Steam API 데이터 수집 스크립트
- 분석 템플릿 (Jupyter Notebook)
- 발표자료용 요약 리포트 구조
- 유튜브 콘텐츠 기획서

원하시는 부분이 있으면 말씀해주세요. 바로 도와드릴게요!