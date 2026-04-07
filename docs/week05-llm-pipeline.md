---
layout: default
title: Week 5 — LLM 문서 처리 파이프라인
nav_order: 9
---

# Week 5 — LLM 문서 처리 파이프라인

> **이번 주 목표:** PDF 논문을 AI에게 읽혀서 Markdown → 한국어 번역 → DOCX까지 자동으로 뽑아낸다.

---

## 전체 흐름 한눈에 보기

이번 주 실습은 세 개의 스크립트가 파이프라인처럼 연결됩니다.

```
[PDF 논문]
    │
    ▼  process_pdf.py
[페이지별 PNG 렌더링]  ─→  Gemini OCR  ─→  output.md
                                               │
                                               ▼  translate_md.py
                                        [용어집 추출]  (1회)
                                               │
                                        [페이지별 번역]  (페이지 수만큼)
                                               │
                                          output_ko.md
                                               │
                                               ▼  pandoc
                                          output_ko.docx
```

**핵심 설계 원칙:** 이미지 → LLM → Markdown(텍스트)으로 1차 변환하고,  
텍스트만 번역해 **이미지 토큰 비용을 절약**합니다.

> 논문 1페이지 처리 기준 이미지 입력 ~1,120 토큰 + 출력 ~1,200 토큰 → **약 3원**  
> 100페이지 처리해도 약 300원 수준입니다.

---

## ⚙️ 사전 준비 (수업 전 필수 설치)

### 1. pandoc 설치

Markdown을 DOCX로 변환하는 외부 도구입니다.

**Windows**

```
winget install pandoc
```

**macOS**

```bash
brew install pandoc
```

설치 확인:

```
pandoc -v
```

> **⚠️ Windows 주의:** Streamlit이 실행 중인 상태에서 pandoc을 설치하면 해당 터미널 세션의 PATH가 갱신되지 않아 "pandoc을 찾을 수 없음" 오류가 납니다. **pandoc 설치 후 반드시 Streamlit을 재시작**하세요.

### 2. Python 패키지 설치

```
pip install pdfplumber pymupdf pillow google-genai python-dotenv streamlit
```

> `pymupdf`는 PDF 렌더링을 담당합니다. poppler 등 별도 외부 도구 설치가 필요 없습니다.

> **⚠️ SDK 주의:** 예전 튜토리얼에서 자주 보이는 `google-generativeai`는 구형(deprecated)입니다.  
> 반드시 `google-genai`를 설치하세요. import 방식도 다릅니다:
>
> ```python
> # ❌ 구형 (deprecated)
> import google.generativeai as genai
>
> # ✅ 신형
> from google import genai
> client = genai.Client(api_key="...")
> ```

### 3. API 키 발급 및 설정

1. [Google AI Studio](https://aistudio.google.com) 접속
2. 우측 상단 **Get API key** 클릭 → 키 복사
3. 프로젝트 폴더에 `.env` 파일 생성:

```
GEMINI_API_KEY=여기에_키_붙여넣기
```

> `.env` 파일은 절대 GitHub에 올리지 마세요. `.gitignore`에 추가되어 있는지 확인하세요.

---

## 실습 Step 1 — PDF → Markdown (`process_pdf.py`)

### 스크립트 역할

| 단계 | 동작 |
|---|---|
| PDF 열기 | `pymupdf(fitz)`로 PDF를 불러옴 |
| 이미지 추출 | 페이지 내 embedded 이미지를 `figures/` 폴더에 저장 |
| 페이지 렌더링 | 페이지 전체를 PNG(200 dpi)로 렌더링 |
| OCR | Gemini에 페이지 PNG를 전달 → Markdown 텍스트 반환 |
| 플레이스홀더 치환 | `[FIGURE_1]` → `![](figures/page1_fig1.png)` |
| DOCX 변환 | `pandoc`으로 output.docx 생성 |

### Gemini OCR 프롬프트

Gemini에게 "이렇게 Markdown으로 변환해"라고 알려주는 지시문입니다. 실제 코드에서 사용하는 프롬프트:

```
이 이미지는 PDF 문서의 한 페이지입니다. 페이지 전체 내용을 Markdown 형식으로 변환해 주세요.

## 기본 변환 규칙
- 텍스트: 원본 내용을 그대로 Markdown 문법으로 표현 (제목, 목록 등 포함)
- 수식: LaTeX 인라인 수식 ($...$) 또는 블록 수식 ($$...$$) 형식으로 변환
- 2단 레이아웃: 왼쪽 컬럼 전체 → 오른쪽 컬럼 전체 순서로 선형화
- 추가 설명 없이 Markdown 내용만 출력 (코드블록 래퍼 없이)

## 제외할 항목 (출력하지 말 것)
페이지 상하단의 저널 메타데이터는 본문이 아니므로 출력하지 말 것:
- 상단: 저널명, 권호(Vol./No.), ISSN, DOI 헤더, 수신/수락/게재일
- 하단: 페이지 번호, 저작권 표시(© ...), 출판사명, URL

## Figure / 이미지 처리
- 그래프, 차트, 실험 사진, 다이어그램 등 실제 Figure가 있는 위치에
  [FIGURE_1], [FIGURE_2] 형식의 플레이스홀더를 등장 순서대로 삽입
- 장식용 선, 배경, 로고 등은 플레이스홀더 제외
- Figure 내부 텍스트(축 레이블, 범례 등)는 별도 추출하지 말 것
- 플레이스홀더 바로 다음 줄에 Figure 캐션만 *캐션 텍스트* 형식으로 추가

## 표(Table) 처리
- 표는 Markdown 표(| 구분자) 형식으로 변환
- 페이지 상단에서 헤더 없이 데이터 행으로 시작 → 이전 페이지 연속 표 의심:
  <!-- TABLE_CONTINUES_FROM_PREVIOUS_PAGE --> 주석 삽입
- 페이지 하단에서 표가 잘린 것처럼 보임 →
  <!-- TABLE_CONTINUES_TO_NEXT_PAGE --> 주석 삽입
```

> **프롬프트가 길어 보이지만** 각 규칙이 하는 일이 다릅니다.  
> "2단 레이아웃 선형화", "헤더·푸터 제외", "Figure 플레이스홀더" — 이 세 가지가 핵심입니다.  
> 이 규칙들을 빼면 Gemini가 페이지를 왼쪽→오른쪽이 아닌 행 순서로 섞어 읽고,  
> 저널명·페이지번호까지 본문에 포함시킵니다.

### 핵심 코드 이해

**PDF → PNG 렌더링 (pymupdf만으로)**

```python
import fitz  # pymupdf
from io import BytesIO
from PIL import Image

def render_page_as_image(page: fitz.Page, dpi: int = 200) -> Image.Image:
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    return Image.open(BytesIO(pix.tobytes("png")))
```

> **왜 pymupdf 하나만?**  
> 처음에는 `pdf2image` 라이브러리를 같이 썼는데, 이 라이브러리가 내부적으로 `poppler`라는
> 외부 프로그램을 필요로 합니다. Windows에서 poppler를 수동으로 설치하고 PATH를 잡는 과정이
> 진입장벽이 되어서, pymupdf가 자체적으로 제공하는 렌더링 기능으로 완전히 대체했습니다.
> `pip install pymupdf` 한 줄이면 끝입니다.

**Gemini API 호출**

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def page_image_to_markdown(page_image: Image.Image) -> str:
    buf = BytesIO()
    page_image.save(buf, format="PNG")

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=[
            GEMINI_PROMPT,                                          # 텍스트 프롬프트
            types.Part.from_bytes(                                  # 이미지
                data=buf.getvalue(), mime_type="image/png"
            ),
        ]
    )
    return response.text.strip()
```

### CLI 실행

```bash
python process_pdf.py paper.pdf
```

출력 폴더 구조:

```
paper/
├── output.md          ← 전체 Markdown
├── output.docx        ← pandoc 변환 DOCX
└── figures/
    ├── page1_fig1.png
    ├── page2_fig1.png
    └── ...
```

> 폴더명은 PDF 파일 이름에서 자동 생성됩니다. `paper.pdf` → `paper/`

---

## 실습 Step 2 — Markdown 번역 (`translate_md.py`)

### 왜 이미지 재처리를 안 할까?

Step 1에서 이미 이미지를 다 읽었으니, 번역은 **텍스트(output.md)만** 처리합니다.  
이미지를 다시 Gemini에 넘기면 토큰 비용이 2배가 됩니다.

### 2단계 번역 전략

단순히 전체를 한 번에 번역하면 용어 불일치가 생깁니다.  
앞에서는 "전력변환효율", 뒤에서는 "power conversion efficiency"가 섞이는 식으로요.  
이를 해결하기 위해 **용어집 추출 → 번역** 2단계로 나눕니다.

```
output.md 전체
    │
    ▼  1단계: 용어집 추출 (1회 API 호출)
[영문 유지 목록] + [한영 병기 목록]  →  용어집 JSON
    │
    ▼  2단계: 페이지별 번역 (페이지 수만큼 API 호출)
용어집을 컨텍스트로 주입 → 각 페이지 번역
    │
    ▼
output_ko.md  +  output_ko.docx
```

### 1단계 프롬프트 — 용어집 추출

```
다음은 학술 논문 전체 내용입니다. 번역 일관성을 위해 아래 항목들을 JSON으로 추출하세요.

출력 형식 (JSON만, 추가 설명 없이):
{
  "keep_english": ["TiO2", "PEDOT:PSS", "PCE", "μm"],
  "translate_with_note": {
    "power conversion efficiency": "전력변환효율(PCE)",
    "external quantum efficiency": "외부양자효율(EQE)"
  }
}

추출 기준:
- keep_english: 화학식, 물질명, 측정 단위, 고유 약어, 모델명 등 번역 없이 영문 유지
- translate_with_note: 처음 등장 시 한국어(영어) 병기가 필요한 핵심 기술 용어
- 중국어·일본어 표현은 해당 의미의 영문명으로 변환해서 포함할 것
```

> **JSON 출력을 요청하는 이유:** "추가 설명 없이 JSON만"이라고 명시해야  
> "네, 추출했습니다. 용어집은 다음과 같습니다..." 같은 전문(preamble)을 붙이지 않습니다.  
> 코드에서 `json.loads(response.text)` 바로 파싱하기 위해서입니다.

### 2단계 프롬프트 — 번역 규칙

용어집을 컨텍스트로 넣어 페이지별로 반복 호출합니다:

```
당신은 학술 논문 번역 전문가입니다. 아래 규칙을 반드시 따라 영어 Markdown을 한국어로 번역하세요.

## 이 논문 확정 용어집
영문 유지 (번역 금지): TiO2, PEDOT:PSS, PCE, μm, ...
한국어(영어) 병기: power conversion efficiency → 전력변환효율(PCE), ...

## 번역 규칙
1. 영문 유지: 화학식·물질명·측정 단위·약어·Figure/Table 참조
2. 병기: 처음 등장 시 "한국어(English)" 형식, 이후 한국어만
3. 문장 번역: 학술 논문체 한국어 (합니다/됩니다 체)
4. 중국어·일본어: 한국어 또는 영문 통용명으로 번역 (원문 그대로 남기지 말 것)
5. 수식 보존: $...$ 및 $$...$$ LaTeX 수식은 절대 수정하지 말 것
6. Markdown 보존: #, |, -, *, ![](), --- 등 구조 그대로 유지

추가 설명 없이 번역된 Markdown만 출력할 것.
```

> **"중국어·일본어는 번역할 것"이라는 규칙이 왜 있을까?**  
> 논문에 중국어(羟基辛酸 등)나 일본어(ヒアルロン酸 등) 출처 표기가 섞인 경우,  
> 처음에는 "원문 보존 컬럼은 그대로 두어라"처럼 복잡한 예외 규칙을 뒀는데  
> 오히려 모델이 중국어를 그대로 남기는 역효과가 났습니다.  
> "중국어·일본어는 한국어 또는 영문 통용명으로 번역"이라고 단순화하니 해결됐습니다.  
> **프롬프트 규칙은 많을수록 좋은 게 아닙니다.**

### CLI 실행

```bash
# 기본 실행
python translate_md.py paper/output.md

# 추가 지침 주입
python translate_md.py paper/output.md --instructions "경피 흡수율은 항상 경피흡수율(transdermal absorption rate)로 표기"
```

출력:

```
paper/
├── output.md          ← (기존) 원문 Markdown
├── output.docx        ← (기존) 원문 DOCX
├── output_ko.md       ← 번역 Markdown  ← NEW
└── output_ko.docx     ← 번역 DOCX      ← NEW
```

---

## 실습 Step 3 — GUI로 통합 실행 (`app.py`)

CLI가 익숙해지면 GUI로 묶어서 사용합니다.

### 실행

```bash
streamlit run app.py
```

### 화면 구성

```
┌──────────────────────────────────────────────────────┐
│  📑 PDF → Markdown / 번역 변환                        │
├───────────────────────┬──────────────────────────────┤
│  PDF 파일 업로드      │  DOCX 템플릿 (선택)           │
│  [파일 선택]          │  [파일 선택]                  │
│                       │  현재 템플릿: Template.docx  │
├───────────────────────┴──────────────────────────────┤
│  🗒️ 번역 추가 지침 (선택)  ▼                          │
│  ┌────────────────────────────────────────────────┐  │
│  │  예시:                                          │  │
│  │  - 'ISO 10993'은 영문 그대로 유지               │  │
│  └────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│  [📄 MD 생성]   [🇰🇷 번역]   [⚡ All-in-One]         │
│                                                      │
│  > 처리 로그가 실시간으로 표시됩니다                  │
│                                                      │
│  ─────────────────────────────────────────────────  │
│  다운로드                                            │
│  [📄 원문 MD]  [📝 원문 DOCX]  [🇰🇷 번역 MD]  [🇰🇷 번역 DOCX] │
└──────────────────────────────────────────────────────┘
```

**버튼 설명:**

| 버튼 | 동작 |
|---|---|
| 📄 MD 생성 | `process_pdf.py` 실행 → output.md 생성 |
| 🇰🇷 번역 | `translate_md.py` 실행 → output_ko.md 생성 |
| ⚡ All-in-One | MD 생성 → 번역을 순서대로 자동 실행 |

**DOCX 템플릿 업로드:**  
회사 Word 템플릿을 올려두면 이후 모든 변환에 폰트·스타일이 자동 적용됩니다.  
프로젝트 폴더의 `template.docx`를 교체하는 방식입니다.

---

## pandoc과 template.docx

pandoc은 Markdown을 DOCX로 변환할 때 `--reference-doc` 옵션으로 템플릿을 참조합니다.

```bash
# 수동 실행 예시
pandoc output_ko.md -o output_ko.docx --reference-doc=template.docx
```

> `template.docx`는 내용이 아닌 **스타일만** 참조합니다. Word에서 "스타일 편집"으로  
> 제목/본문/표 스타일을 회사 양식에 맞게 설정해두면, 변환 결과물이 그 스타일을 따릅니다.

---

## 📦 이번 주 사용 패키지 정리

| 패키지 | 역할 | 설치 방법 |
|---|---|---|
| `pymupdf` | PDF 렌더링 + 이미지 추출 | pip (`import fitz`) |
| `pillow` | 이미지 처리 | pip |
| `google-genai` | Gemini LLM API | pip |
| `python-dotenv` | API 키 환경변수 관리 | pip |
| `streamlit` | GUI | pip |
| `pandoc` | Markdown → DOCX | winget / brew (별도 설치) |

---

## ✅ 이번 주 체크리스트

- [ ] pandoc 설치 확인 (`pandoc -v`)
- [ ] Python 패키지 설치 완료 (`google-genai` 설치 확인)
- [ ] Gemini API 키 발급 + `.env` 저장
- [ ] `python process_pdf.py sample.pdf` 실행 → output.md 생성 확인
- [ ] output.md 내용 직접 열어서 Markdown 변환 품질 확인
- [ ] `python translate_md.py sample/output.md` 실행 → output_ko.md 생성 확인
- [ ] `streamlit run app.py` 실행 → GUI 동작 확인
- [ ] All-in-One 버튼으로 PDF → 번역 DOCX 전 과정 완주

---

## 🔗 다음 주 예고

Week 6에서는 LLM에게 **"자유 텍스트 대신 정해진 양식으로 답해달라"** 고 요청하는 방법을 배웁니다.  
원료 규격서, 시험 보고서에서 원하는 항목만 뽑아서 Excel로 바로 저장하는 파이프라인입니다.
