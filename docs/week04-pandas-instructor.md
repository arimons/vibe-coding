# Week 04 — pandas 데이터 분석 실전 (강사용 매뉴얼)

> **이 문서는 강사용입니다.** 수강생에게는 별도의 실습 가이드를 배포합니다.
> 각 Phase 에서 수강생이 막힐 수 있는 포인트, 프롬프트 설계 의도, 예상 결과를 포함합니다.

---

## 수업 목표

- pandas의 핵심 기능(읽기, 필터링, 변환, 집계)을 실험 데이터로 체험
- 정규식(regex)을 활용한 문자열 패턴 분리를 이해
- 여러 Excel 시트를 하나의 분석용 테이블로 취합하는 파이프라인 구축
- Streamlit으로 인터랙티브 시각화(Violin Plot) 구현

### 수업 흐름 한눈에 보기

```
[Part 1] pandas 기초 훑기 (30분)
    ↓
[Part 2] 실전: Raw Data → 분석 → 시각화 (60분)
    Phase 1: 데이터 탐색 — "내 데이터가 뭔지 먼저 보자"
    Phase 2: 패턴 발견 — "V1_S12를 분리하자"
    Phase 3: 멀티시트 취합 — "전부 하나로 모으자"
    Phase 4: 통계 처리 — "Z-score로 표준화"
    Phase 5: 시각화 — "어떤 그래프가 맞을까?"
    Phase 6: 결과 저장 — "Excel로 내보내기"
```

---

## Part 1: pandas 기초 훑기 (30분)

> **강사 노트:** 이 파트는 빠르게 넘기되, Part 2에서 쓸 함수를 미리 손에 익히는 목적입니다.
> 기존 `sample_raw.csv`를 활용하여 아래 개념을 실습합니다.

### 1-1. DataFrame이란?

```
💡 강의 포인트:
"Excel 시트 하나 = DataFrame 하나"라고 설명하면 직관적입니다.
행(row)은 관찰값, 열(column)은 변수. 이것만 기억하면 됩니다.
```

**프롬프트 예시 (수강생이 입력):**
```
sample_raw.csv 파일을 읽어서 어떤 데이터인지 보여줘.
행 수, 열 수, 컬럼 이름, 처음 5행을 확인하고 싶어.
```

**기대 결과:**
```python
import pandas as pd
df = pd.read_csv("data/sample_raw.csv")
print(df.shape)       # (24, 9)
print(df.columns)     # 컬럼 목록
print(df.head())      # 처음 5행
```

### 1-2. 기본 조작 — 선택, 필터, 정렬

**프롬프트 예시:**
```
이 데이터에서:
1. Visit이 V1인 행만 필터링
2. moisture_val 열만 선택
3. 수분값 기준 내림차순 정렬
각각 어떻게 하는지 보여줘.
```

```
💡 강의 포인트:
- df["열이름"] → 열 선택 (Series)
- df[df["열"] == "값"] → 행 필터링 (Boolean indexing)
- df.sort_values("열", ascending=False) → 정렬
이 3가지만 알면 Part 2의 80%를 해결할 수 있습니다.
```

### 1-3. 결측값 확인

```
💡 강의 포인트:
수강생들에게 "실제 실험 데이터에는 빈 칸이 반드시 있다"고 강조하세요.
S004의 V2 수분값이 비어있는 것을 sample_raw.csv에서 직접 확인시킵니다.
```

**프롬프트 예시:**
```
이 데이터에서 비어있는 값(결측값)이 있는지 확인하고,
어떤 피험자의 어떤 항목이 비었는지 알려줘.
```

**기대 결과:** `df.isnull().sum()` → moisture_val: 1, adverse_event: 1

### 1-4. 기술통계

**프롬프트 예시:**
```
Visit별로 moisture_val의 평균, 표준편차, 최소, 최대를 구해줘.
```

**기대 결과:** `df.groupby("Visit")["moisture_val"].describe()`

```
💡 타이밍 체크:
여기까지 30분. 수강생이 "pandas로 Excel보다 편하다"는 느낌을 받았으면 성공.
"이제 진짜 실험 데이터로 해볼까요?" 하고 Part 2로 전환합니다.
```

---

## Part 2: 실전 — Raw Data → 분석 → 시각화

### 사용 데이터

| 파일 | 내용 | 시트 구조 |
|------|------|-----------|
| `Cicca B5_cholesterol_raw data.xlsx` | 콜레스테롤 측정값 | 단일 시트 (`cholesterol`) |
| `Cicca B5_fatty Acid_raw data.xlsx` | 지방산 측정값 | 6개 시트 (`C20FA` ~ `C30FA`) |

### 공통 구조 (모든 시트 동일)

```
Row 1~6: 장비 메타데이터 (Quantify Compound Summary Report, 출력일시 등)
Row 7:   컬럼 헤더
         Column C = "Sample Text" → V1_S1, V1_S2, ... V2_S33
         Column L = "ng/mg protein" → 실제 측정값
Row 8~:  데이터 (약 66행 = 33명 × 2회 방문)
```

```
⚠️ 강사 주의사항:
- Row 1~6은 skiprows=6 으로 건너뛰어야 합니다
- S4, S25, S33은 일부 시트에서 탈락 피험자 (결측 또는 제외 대상)
- Column L의 값은 이미 "ng/mL ÷ protein(mg/mL)" 으로 보정된 최종값입니다
```

---

### Phase 1: 데이터 탐색 — "내 데이터가 뭔지 먼저 보자"

> **의도:** 바이브코딩의 첫 단추 = "일단 열어보기". 데이터를 눈으로 확인하는 습관을 만듭니다.

**프롬프트 (수강생 → LLM):**
```
data 폴더에 있는 "Cicca B5_cholesterol_raw data.xlsx" 파일을 읽어서
어떤 구조인지 파악해줘.
- 시트 목록
- 각 시트의 컬럼 헤더
- 처음 10행 미리보기
```

**LLM이 생성할 코드 (예상):**
```python
import pandas as pd

# 시트 목록 확인
xls = pd.ExcelFile("data/Cicca B5_cholesterol_raw data.xlsx")
print("시트 목록:", xls.sheet_names)

# 첫 10행 미리보기 (skiprows 없이 → 메타데이터 포함 상태로 봄)
df_raw = pd.read_excel(xls, sheet_name="cholesterol", header=None)
print(df_raw.head(10))
```

```
💡 강의 포인트 — "왜 skiprows가 필요한가":
처음에 일부러 skiprows 없이 읽게 하세요.
Row 1~6이 장비 출력 메타데이터라는 걸 수강생이 직접 보고
"아, 실제 데이터는 7행부터구나" 깨닫게 합니다.

후속 프롬프트:
"위에 6줄은 장비 정보라서 필요 없어. 7행부터 읽어줘."
→ LLM이 skiprows=6 을 적용한 코드를 생성
→ "이렇게 장비마다 헤더 형식이 다를 수 있으니 항상 먼저 확인하라"고 정리
```

---

### Phase 2: 패턴 발견 — "V1_S12를 분리하자"

> **의도:** 정규식의 실용적 가치를 체감. "수동으로 V1과 S12를 분리하던 작업"이 한 줄로 끝남.

**프롬프트 (수강생 → LLM):**
```
Column C(Sample Text)에 "V1_S1", "V2_S33" 같은 값이 있어.
V 뒤의 숫자는 방문차수(1=섭취전, 2=섭취후),
S 뒤의 숫자는 피험자 번호야.

정규식으로 Visit 번호와 Subject 번호를 각각 새 컬럼으로 분리해줘.
Visit 번호는 1이면 "섭취전", 2면 "섭취후"로 변환해줘.
```

**LLM이 생성할 코드 (예상):**
```python
# 정규식으로 패턴 분리
extracted = df["Sample Text"].str.extract(r'V(\d+)_S(\d+)')
df["Visit"] = extracted[0].astype(int)
df["Subject"] = extracted[1].astype(int)

# Visit 번호 → 한글 라벨
df["Group"] = df["Visit"].map({1: "섭취전", 2: "섭취후"})
```

```
💡 강의 포인트 — 정규식 비유:
정규식은 "가위"입니다. "V1_S12"라는 문자열에서
어디를 자를지 패턴으로 알려주는 것이죠.

  V(\d+)_S(\d+)
  │  │    │  │
  │  │    │  └─ 두 번째 캡처: 피험자 번호 (S 뒤 숫자들)
  │  │    └──── 구분자: 언더스코어
  │  └───────── 첫 번째 캡처: 방문차수 (V 뒤 숫자들)
  └──────────── V 문자 자체

괄호() 안에 들어간 부분만 "캡처"되어 새 컬럼으로 추출됩니다.
```

```
⚠️ 수강생 예상 질문:
Q: "\d+가 뭐예요?"
A: \d = digit(숫자 한 글자), + = 1개 이상 반복.
   즉 \d+는 "숫자가 1개 이상 연속된 부분"

Q: "왜 괄호를 쓰나요?"
A: 괄호 없으면 매칭만 하고 추출은 안 됩니다.
   괄호 = "이 부분을 꺼내줘"라는 표시.
```

**범용성 강조 포인트:**
```
기존 week04 app.py의 "정규식 변환" 탭에서 이 패턴을 직접 입력하고
미리보기로 결과를 확인할 수 있습니다.
→ 수강생 자신의 실험 데이터에서 비슷한 코딩 규칙을 찾아 적용해보게 유도
```

---

### Phase 3: 멀티시트 취합 — "전부 하나로 모으자"

> **의도:** 이 Phase가 실무에서 가장 시간을 절약해주는 단계입니다.
> 수동으로 하면 "시트 열기 → 복사 → 붙여넣기 → 시트명 기록" 반복인데,
> 코드로는 for문 한 번이면 끝납니다.

**프롬프트 (수강생 → LLM):**
```
"Cicca B5_fatty Acid_raw data.xlsx"에는 C20FA, C22FA, C24FA, C26FA, C28FA, C30FA
6개 시트가 있어. 각 시트의 구조는 동일해:
- 처음 6행은 장비 메타데이터 (건너뛰기)
- Column C = Sample Text (V1_S1 형식)
- Column L = ng/mg protein (측정값)

모든 시트에서 이 두 컬럼만 뽑아서:
1. 시트 이름을 "Component" 컬럼으로 추가
2. Sample Text에서 Visit, Subject 분리 (Phase 2와 동일)
3. 전체를 하나의 DataFrame으로 합쳐줘

콜레스테롤 데이터도 같은 구조로 합쳐서 최종적으로
Subject | Group | Component | Value 형태의 테이블을 만들어줘.
```

**LLM이 생성할 코드 (예상):**
```python
import pandas as pd

def read_raw_sheet(filepath, sheet_name):
    """원본 시트에서 필요한 컬럼만 추출"""
    df = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=6)
    df = df[["Sample Text", "ng/mg protein"]].dropna()
    
    # 정규식 분리
    extracted = df["Sample Text"].str.extract(r'V(\d+)_S(\d+)')
    df["Visit"] = extracted[0].astype(int)
    df["Subject"] = extracted[1].astype(int)
    df["Group"] = df["Visit"].map({1: "섭취전", 2: "섭취후"})
    df["Component"] = sheet_name
    df["Value"] = df["ng/mg protein"]
    
    return df[["Subject", "Group", "Component", "Value"]]

# 콜레스테롤
df_chol = read_raw_sheet("data/Cicca B5_cholesterol_raw data.xlsx", "cholesterol")
df_chol["Component"] = "Cholesterol"

# 지방산 6개 시트
fa_file = "data/Cicca B5_fatty Acid_raw data.xlsx"
fa_sheets = pd.ExcelFile(fa_file).sheet_names  # ['C20FA', 'C22FA', ...]
df_fa_list = [read_raw_sheet(fa_file, s) for s in fa_sheets]

# 전체 합치기
df_all = pd.concat([df_chol] + df_fa_list, ignore_index=True)
print(df_all.shape)
print(df_all.head())
```

```
💡 강의 포인트 — "함수로 만드는 이유":
같은 구조의 시트를 7번 처리해야 합니다.
복사-붙여넣기 대신 함수 하나 만들고 반복 호출.
이것이 프로그래밍의 핵심 가치 — "반복 작업의 자동화"

비유: 도장을 한 번 만들어두면 100번 찍을 수 있는 것처럼,
함수를 한 번 정의하면 시트가 60개여도 한 줄로 처리됩니다.
```

```
💡 강의 포인트 — "중간 파일이 필요 없는 이유":
원래 수작업 흐름:
  Raw Excel → (수동 복붙) → 종합정리.xlsx → (수동 복붙) → 통계분석결과.xlsx

코드 흐름:
  Raw Excel → read_raw_sheet() → pd.concat() → 끝!

중간 파일 2개가 사라집니다. 이것이 "파이프라인"의 힘입니다.
```

---

### Phase 4: 통계 처리 — "Z-score로 표준화"

> **의도:** Z-score 계산 자체보다, "왜 표준화가 필요한지"를 이해시키는 것이 목표.

**프롬프트 (수강생 → LLM):**
```
각 Component별로 Value의 Z-score를 계산해서 Z 컬럼에 추가해줘.
그리고 Component × Group별 요약 통계(평균, 표준편차, n)도 보여줘.
```

**LLM이 생성할 코드 (예상):**
```python
from scipy import stats

# Component별 Z-score 계산
df_all["Z"] = df_all.groupby("Component")["Value"].transform(
    lambda x: stats.zscore(x, nan_policy='omit')
)

# 요약 통계
summary = df_all.groupby(["Component", "Group"])["Value"].agg(
    ["count", "mean", "std"]
).round(4)
print(summary)
```

```
💡 강의 포인트 — Z-score가 왜 필요한가:
Cholesterol은 0.5~3.5 범위, C20FA는 80~400 범위입니다.
단위도 같은 ng/mg protein이지만, 값의 스케일이 전혀 다릅니다.

만약 "섭취 전후로 어떤 성분이 가장 크게 변했나?"를 비교하려면,
값 자체가 아니라 "그 성분 내에서 얼마나 벗어났는가"를 봐야 합니다.
이것이 Z-score — (값 - 평균) / 표준편차.

비유: 수학 80점과 영어 80점은 같은 점수이지만,
수학 평균이 90이고 영어 평균이 60이면 의미가 전혀 다릅니다.
Z-score는 "각 과목 내에서의 상대적 위치"를 숫자로 만든 것.
```

```
⚠️ 수강생 예상 질문:
Q: "Z-score가 2.5면 어떤 의미예요?"
A: 평균에서 표준편차 2.5배만큼 높다는 뜻.
   일반적으로 |Z| > 2는 이상치(outlier) 후보로 봅니다.
   100명 중 1~2명 정도의 극단값이라는 의미.
```

---

### Phase 5: 시각화 — "어떤 그래프가 맞을까?"

> **의도:** 차트 종류를 지정하지 않고 "상황"을 설명하는 프롬프트가 핵심입니다.
> 바이브코더는 차트 이름을 외울 필요 없이, 원하는 것을 설명하면 됩니다.

**프롬프트 1단계 — 차트 선택 (수강생 → LLM):**
```
섭취전/섭취후를 비교하는 그래프를 그리고 싶어.
- 30명 정도의 개별 데이터 포인트가 보여야 해
- 전체 분포의 모양도 보고 싶어
- 평균값과 오차도 표시되면 좋겠어
어떤 차트가 적합할까?
```

```
💡 강의 포인트 — "이름을 몰라도 설명할 수 있다":
수강생은 "Violin Plot"이란 이름을 몰라도 됩니다.
"분포도 보고 싶고 점도 보고 싶다"라고 설명하면
LLM이 Violin + Strip Plot 조합을 제안합니다.

이것이 바이브코딩의 핵심 스킬 —
"정확한 용어 대신, 원하는 결과를 묘사하는 능력"
```

**프롬프트 2단계 — Streamlit 구현 (수강생 → LLM):**
```
Streamlit 앱으로 만들어줘.
1. Component를 선택하는 드롭다운
2. 선택한 성분의 Violin Plot
3. 섭취전/섭취후 비교가 잘 보이도록 색상 구분
4. 아래에 요약 통계 테이블도 보여줘
```

**LLM이 생성할 코드 (예상):**
```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🔬 Lipid Analysis — 섭취전 vs 섭취후")

# 데이터 로드 (Phase 3~4에서 만든 df_all)
# ... (데이터 준비 코드)

component = st.selectbox("성분 선택", df_all["Component"].unique())
df_plot = df_all[df_all["Component"] == component]

fig = px.violin(
    df_plot, x="Group", y="Value", color="Group",
    box=True,         # 박스플롯 포함
    points="all",     # 개별 점 표시
    title=f"{component} — 섭취전 vs 섭취후",
    color_discrete_map={"섭취전": "#636EFA", "섭취후": "#EF553B"}
)
fig.update_layout(
    yaxis_title="ng/mg protein",
    xaxis_title="",
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# 요약 통계
summary = df_plot.groupby("Group")["Value"].agg(
    ["count", "mean", "std", "min", "max"]
).round(4)
st.dataframe(summary)
```

```
💡 강의 포인트 — 차트 종류별 적합 상황:
| 상황 | 추천 차트 |
|------|-----------|
| 두 그룹 비교 + 분포 + 개별점 | Violin Plot (지금 사례) |
| 시간 흐름에 따른 변화 | Line Chart |
| 여러 성분의 크기 비교 | Bar Chart |
| 두 변수의 관계 | Scatter Plot |
| 분포 확인 (단순) | Histogram / Box Plot |

이 표를 수강생에게 보여주면
"내 데이터에는 어떤 차트가 맞을까?"를 스스로 판단할 수 있습니다.
```

---

### Phase 6: 결과 저장

**프롬프트 (수강생 → LLM):**
```
최종 분석 결과를 Excel로 저장해줘.
- 시트 1: 전체 tidy data (Subject, Group, Component, Value, Z)
- 시트 2: Component × Group별 요약 통계
파일명은 "분석결과.xlsx"로.
```

```python
with pd.ExcelWriter("data/분석결과.xlsx", engine="openpyxl") as writer:
    df_all.to_excel(writer, sheet_name="전체데이터", index=False)
    summary.to_excel(writer, sheet_name="요약통계")
```

---

## 수업 진행 팁

### 시간 배분 가이드

| Phase | 소요시간 | 핵심 활동 |
|-------|----------|-----------|
| Part 1: 기초 | 25~30분 | sample_raw.csv로 pandas 기본 체험 |
| Phase 1: 탐색 | 10분 | Raw 파일 열어보기, skiprows 발견 |
| Phase 2: 정규식 | 15분 | V1_S12 분리, 정규식 패턴 이해 |
| Phase 3: 취합 | 15분 | 멀티시트 → 하나의 DataFrame |
| Phase 4: 통계 | 10분 | Z-score 계산 (개념만 짧게) |
| Phase 5: 시각화 | 15분 | Violin Plot + Streamlit |
| Phase 6: 저장 | 5분 | Excel 내보내기 |

### 수강생이 자주 겪는 문제

1. **`skiprows`를 모름** → Phase 1에서 일부러 안 쓰고 읽게 한 뒤 발견하게 유도
2. **정규식 공포증** → "가위" 비유 + 기존 app.py의 미리보기 탭 활용
3. **`pd.concat` 결과가 이상함** → `ignore_index=True` 빠뜨림. 인덱스가 중복되어 보임
4. **Plotly 설치 안 됨** → `pip install plotly` (requirements.txt에 추가)
5. **한글 깨짐** → Excel 저장 시 `encoding` 문제보다는 `engine="openpyxl"` 확인

### 프롬프트 설계 원칙 (수업 중 강조)

```
좋은 프롬프트의 3요소:
1. 데이터 구조 설명 — "Column C에 V1_S12 형식의 값이 있어"
2. 원하는 결과 — "Visit과 Subject를 분리하고 싶어"
3. 제약 조건 — "첫 6행은 메타데이터라 건너뛰어야 해"

나쁜 프롬프트: "데이터 분석해줘"
좋은 프롬프트: "Column C의 V1_S12 패턴에서
                V 뒤 숫자(방문차수)와 S 뒤 숫자(피험자번호)를
                정규식으로 분리해서 새 컬럼으로 만들어줘"
```

---

## 부록: 전체 파이프라인 통합 코드

> 수업 후 수강생에게 참고용으로 제공할 수 있는 전체 흐름 코드입니다.
> 실제 수업에서는 Phase별로 나눠서 진행하세요.

```python
import pandas as pd
from scipy import stats
import plotly.express as px
import streamlit as st

# ─── 설정 ───────────────────────────────────────────
CHOL_FILE = "data/Cicca B5_cholesterol_raw data.xlsx"
FA_FILE = "data/Cicca B5_fatty Acid_raw data.xlsx"
SKIP_ROWS = 6
COL_SAMPLE = "Sample Text"     # Column C
COL_VALUE = "ng/mg protein"    # Column L
VISIT_MAP = {1: "섭취전", 2: "섭취후"}

# ─── Phase 1~3: 읽기 + 분리 + 취합 ──────────────────
def read_raw_sheet(filepath, sheet_name, component_name=None):
    """원본 시트에서 tidy format으로 변환"""
    df = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=SKIP_ROWS)
    df = df[[COL_SAMPLE, COL_VALUE]].dropna()
    
    extracted = df[COL_SAMPLE].str.extract(r'V(\d+)_S(\d+)')
    df["Subject"] = extracted[1].astype(int)
    df["Group"] = extracted[0].astype(int).map(VISIT_MAP)
    df["Component"] = component_name or sheet_name
    df["Value"] = df[COL_VALUE]
    
    return df[["Subject", "Group", "Component", "Value"]]

# 콜레스테롤
df_chol = read_raw_sheet(CHOL_FILE, "cholesterol", "Cholesterol")

# 지방산 (멀티시트)
fa_sheets = pd.ExcelFile(FA_FILE).sheet_names
df_fa = pd.concat(
    [read_raw_sheet(FA_FILE, s) for s in fa_sheets],
    ignore_index=True
)

# 전체 합치기
df_all = pd.concat([df_chol, df_fa], ignore_index=True)

# ─── Phase 4: Z-score ────────────────────────────────
df_all["Z"] = df_all.groupby("Component")["Value"].transform(
    lambda x: stats.zscore(x, nan_policy='omit')
)

# ─── Phase 5: Streamlit 시각화 ────────────────────────
st.title("🔬 Lipid Analysis — 섭취전 vs 섭취후")

component = st.selectbox("성분 선택", sorted(df_all["Component"].unique()))
df_plot = df_all[df_all["Component"] == component]

fig = px.violin(
    df_plot, x="Group", y="Value", color="Group",
    box=True, points="all",
    title=f"{component}",
    color_discrete_map={"섭취전": "#636EFA", "섭취후": "#EF553B"}
)
fig.update_layout(yaxis_title="ng/mg protein", xaxis_title="", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# 요약 통계
summary = df_plot.groupby("Group")["Value"].agg(["count", "mean", "std"]).round(4)
st.dataframe(summary, use_container_width=True)

# ─── Phase 6: 다운로드 ───────────────────────────────
import io
buf = io.BytesIO()
with pd.ExcelWriter(buf, engine="openpyxl") as writer:
    df_all.to_excel(writer, sheet_name="전체데이터", index=False)
    df_all.groupby(["Component", "Group"])["Value"].agg(
        ["count", "mean", "std"]).to_excel(writer, sheet_name="요약통계")

st.download_button(
    "⬇️ 분석결과 다운로드 (Excel)",
    data=buf.getvalue(),
    file_name="분석결과.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
```
