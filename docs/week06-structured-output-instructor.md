---
layout: page
title: Week 6 — Structured Output
nav_order: 10
---

# Week 6 — Structured Output — 문서에서 데이터 뽑기

> **이번 주 목표:** LLM에게 "양식을 채워달라"고 시키는 법을 익힌다.  
> 정규식이나 파싱 코드 없이, 원하는 구조의 데이터를 바로 얻어내는 경험.

---

## 💡 핵심 개념: 자유 출력 vs 구조화 출력

LLM은 기본적으로 **자유 텍스트**로 답합니다.

```
질문: 이 원료 규격서에서 원료명과 순도를 알려줘
답변: 이 규격서에 따르면 원료명은 Cetyl Alcohol이며, 순도는 98.5% 이상으로
      명시되어 있습니다. 보관 조건은 ...
```

이 텍스트에서 다시 원료명, 순도를 추출하려면 파싱 코드가 필요합니다.

Structured Output은 LLM에게 **미리 정의한 양식(Schema)** 으로 답하도록 강제합니다.

```json
{
  "원료명": "Cetyl Alcohol",
  "CAS번호": "36653-82-4",
  "순도": "98.5%",
  "보관조건": "15-25°C, 차광"
}
```

비유하자면 — 연구원이 **빈 칸짜리 양식지를 주고 거기에 채워넣으라고 시키는 것**입니다.  
빈 답안지에 자유롭게 쓰는 것과, 항목별 칸에 채워 넣는 것의 차이입니다.

---

## 1. JSON Schema 정의하기

Schema는 "어떤 필드를, 어떤 타입으로, 반드시 포함해야 하는가"를 정의합니다.

### 원료 규격서 Schema 예시

```python
ingredient_schema = {
    "type": "object",
    "properties": {
        "원료명_한글": {"type": "string"},
        "원료명_영문": {"type": "string"},
        "CAS번호": {"type": "string"},
        "순도": {"type": "string"},
        "외관": {"type": "string"},
        "보관조건": {"type": "string"},
        "사용제한": {"type": "string"}
    },
    "required": ["원료명_한글", "원료명_영문", "CAS번호", "순도"]
}
```

`required`에 없는 필드는 문서에 정보가 없으면 LLM이 비워둡니다.

### 안정성 시험 보고서 Schema 예시

```python
stability_schema = {
    "type": "object",
    "properties": {
        "제품명": {"type": "string"},
        "시험기간": {"type": "string"},
        "시험조건": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "온도": {"type": "string"},
                    "습도": {"type": "string"},
                    "기간": {"type": "string"}
                }
            }
        },
        "평가항목": {"type": "array", "items": {"type": "string"}},
        "최종판정": {"type": "string", "enum": ["적합", "부적합", "보류"]}
    },
    "required": ["제품명", "시험기간", "최종판정"]
}
```

`enum`을 사용하면 정해진 값 중에서만 선택하도록 강제할 수 있습니다.

---

## 2. Gemini로 Structured Output 요청

```python
from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_structured(text: str, schema: dict) -> dict:
    prompt = f"""
다음 문서에서 정보를 추출해 주세요.
반드시 아래 JSON 형식으로만 답하세요. 다른 설명은 절대 포함하지 마세요.

추출 항목:
{json.dumps(schema, ensure_ascii=False, indent=2)}

문서 내용:
{text}
"""
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=prompt
    )

    # JSON 파싱
    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())
```

---

## 3. 결과 → pandas DataFrame → Excel

```python
import pandas as pd

# 여러 문서 처리
results = []

for pdf_path in pdf_files:
    text = extract_text(pdf_path)          # Week 5 pdfplumber
    data = extract_structured(text, ingredient_schema)
    data["파일명"] = pdf_path
    results.append(data)

# DataFrame 변환
df = pd.DataFrame(results)

# Excel 저장
df.to_excel("원료_정보_취합.xlsx", index=False)
print(f"{len(results)}개 문서 처리 완료")
```

---

## 4. 배치 처리 — 여러 문서 한 번에

```python
import streamlit as st
import pandas as pd

st.title("📋 문서 구조화 추출기")

schema_type = st.selectbox(
    "문서 유형 선택",
    ["원료 규격서", "안정성 시험 보고서", "임상 시험 결과"]
)

uploaded_files = st.file_uploader(
    "PDF 파일 업로드 (여러 개 가능)",
    type="pdf",
    accept_multiple_files=True
)

if uploaded_files and st.button("추출 시작"):
    results = []
    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):
        # 텍스트 추출 + 구조화 처리
        # results.append(...)
        progress.progress((i + 1) / len(uploaded_files))

    df = pd.DataFrame(results)
    st.dataframe(df)

    # Excel 다운로드
    excel_data = df.to_excel(index=False)
    st.download_button("Excel 다운로드", excel_data, "추출결과.xlsx")
```

---

## 5. Schema 설계 팁

| 상황 | 권장 방식 |
|---|---|
| 값이 정해진 항목 (합격/불합격) | `"enum": ["적합", "부적합"]` |
| 여러 개가 나올 수 있는 항목 | `"type": "array"` |
| 없을 수도 있는 항목 | `required` 목록에서 제외 |
| 숫자로 계산할 값 | `"type": "number"` (문자열 아님) |
| 날짜 | `"type": "string"` + 프롬프트에 형식 명시 (`YYYY-MM-DD`) |

### 프롬프트 품질 개선 포인트

LLM이 엉뚱한 값을 넣는다면:

```python
# 프롬프트에 예시를 추가
prompt = f"""
...
출력 예시:
{{
  "원료명_한글": "세틸알코올",
  "CAS번호": "36653-82-4",
  "순도": "98.5% 이상"
}}

문서 내용:
{text}
"""
```

예시를 하나만 보여줘도 품질이 크게 올라갑니다.

---

## 📦 이번 주 사용 패키지 정리

| 패키지 | 역할 |
|---|---|
| `google-genai` | Gemini LLM API (Week 5 동일) |
| `pdfplumber` | PDF 텍스트 추출 (Week 5 동일) |
| `pandas` | 결과 → DataFrame (Week 4 연결) |
| `openpyxl` | Excel 저장 |

신규 설치 없음 — Week 5 환경 그대로 사용합니다.

---

## ✅ 이번 주 체크리스트

- [ ] Structured Output 개념 이해 (자유 출력 vs 양식 출력)
- [ ] 원료 규격서용 Schema 1개 직접 정의
- [ ] LLM 추출 결과 → DataFrame 변환 성공
- [ ] 여러 파일 배치 처리 → Excel 저장 성공
- [ ] Streamlit 배치 처리 앱 실행 확인

---

## 💬 자주 나오는 질문

**Q. LLM이 JSON 말고 다른 형식으로 답하면?**  
프롬프트 마지막에 `"JSON 외 어떤 텍스트도 포함하지 마세요."` 를 추가하거나,  
코드의 JSON 파싱 부분에서 ```json ... ``` 블록을 제거하는 처리를 추가하세요.

**Q. 문서에 해당 항목 정보가 없으면?**  
Schema에서 `required` 목록에서 빼두면 LLM이 `null` 또는 빈 문자열로 반환합니다.  
DataFrame에서 빈 칸으로 표시됩니다.

**Q. 영문 원료명이 섞인 문서도 되나요?**  
됩니다. LLM이 언어 구분 없이 읽어냅니다. Schema의 필드명을 한글로 해도 무방합니다.

---

## 🔗 다음 주 예고

Week 7에서는 **웹 스크래핑**을 다룹니다.  
URL만 주면 LLM이 스크래핑 코드를 자동으로 생성해주는 흐름을 배웁니다.  
HTML selector를 직접 찾지 않아도 됩니다.
