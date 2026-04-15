---
layout: default
title: Week 7 — 웹 스크래핑
nav_order: 11
---

# Week 7 — 웹 스크래핑 — LLM이 코드를 짜줍니다

> **이번 주 목표:** HTML을 외우거나 코드를 직접 짤 필요 없습니다. 다만 LLM이 정확한 코드를 만들려면 URL만으로는 부족하고, 해당 페이지의 HTML 구조를 함께 넘겨줘야 합니다. 브라우저에서 HTML을 복사하는 방법과 DevTools로 원하는 데이터 위치를 찾는 법을 익히면, LLM에게 정확한 코드를 받을 수 있습니다. 그 흐름 전체를 실습합니다.

---

## 📋 목차

1. [크롤링 vs 스크래핑](#1-크롤링-vs-스크래핑)
2. [웹 페이지는 어떻게 만들어지나요? — HTML · CSS · JS · DOM](#2-웹-페이지는-어떻게-만들어지나요--html--css--js--dom)
3. [LLM 기반 스크래핑 워크플로우 — 실습의 핵심](#3-llm-기반-스크래핑-워크플로우--실습의-핵심)
4. [DevTools — 페이지 속 들여다보기](#4-devtools--페이지-속-들여다보기)
5. [실전 사례 — Sephora 화장품 정보 수집](#5-실전-사례--sephora-화장품-정보-수집)
6. [스크래퍼 설계 전략 (3트랙)](#6-스크래퍼-설계-전략-3트랙)
7. [AI 프롬프트 예시 모음](#7-ai-프롬프트-예시-모음)
8. [스크래핑 에티켓과 주의사항](#8-스크래핑-에티켓과-주의사항)

---

## 1. 크롤링 vs 스크래핑

이 두 단어는 자주 혼용되는데, 실제로 하는 일이 다릅니다.

**크롤링(Crawling)** 은 웹 페이지를 돌아다니며 **링크를 따라가서 URL을 수집하는 과정**입니다. "어디에 뭐가 있는지" 지도를 만드는 작업입니다. 구글 검색 엔진이 매일 웹 전체를 돌아다니며 새 페이지를 발견하는 것이 대표적인 크롤링입니다.

**스크래핑(Scraping)** 은 이미 URL을 알고 있는 특정 페이지에서 **원하는 데이터를 추출하는 과정**입니다. "여기서 무엇을 뽑을지"가 핵심입니다.

> 💡 **도서관 비유**
>
> **크롤링**은 도서관 전체를 돌아다니며 "3층 과학 코너 2번 책장에 이런 책들이 있다"는 목록을 만드는 것입니다.
> **스크래핑**은 그 목록을 보고 원하는 책을 꺼내어, 필요한 쪽의 내용을 메모하는 것입니다.
>
> 이번 주는 **스크래핑**에 집중합니다 — URL을 이미 알고 있고, 거기서 데이터를 뽑는 것이 목표입니다.

### 언제 어느 쪽이 필요할까요?

| 목적 | 크롤링 필요? | 스크래핑 필요? |
|---|---|---|
| 경쟁사 특정 제품 1개 정보 수집 | ❌ URL 이미 앎 | ✅ |
| 특정 브랜드 전체 제품 목록 수집 | ✅ URL 먼저 모아야 함 | ✅ |
| 원료 공급사 가격 정기 모니터링 | ❌ URL 고정 | ✅ |
| PubMed 특정 키워드 논문 전체 수집 | ✅ | ✅ |

이번 주는 **URL을 직접 알고 있는 상황**에서 시작하므로 스크래핑만으로 충분합니다.

---

### robots.txt — 사이트가 걸어둔 교통 표지판

스크래핑을 시작하기 전에 한 가지 확인할 것이 있습니다. 어떤 웹사이트든 주소 뒤에 `/robots.txt`를 붙이면 그 사이트의 "수집 허용 규칙"을 볼 수 있습니다.

예를 들어 `https://www.sephora.com/robots.txt`에 접속하면:

```
User-agent: *
Disallow: /search          ← 검색 결과 페이지는 수집 금지
Disallow: /checkout        ← 결제 페이지는 수집 금지
Crawl-delay: 5             ← 요청 사이에 최소 5초 간격을 두세요
```

이 파일은 법적 강제사항은 아니지만, 상업 사이트에서 이를 무시하고 대량 요청을 보내면 IP가 차단되거나 법적 문제가 생길 수 있습니다. 작업 전에 항상 확인하는 것이 기본 에티켓입니다.

---

## 2. 웹 페이지는 어떻게 만들어지나요? — HTML · CSS · JS · DOM

스크래핑을 하려면 "웹 페이지가 어떤 재료로 구성되어 있는지" 최소한의 감이 있어야 합니다. 코드를 직접 짤 필요는 없고, **각 요소가 무슨 역할인지**만 알면 LLM에게 정확하게 지시할 수 있습니다.

---

### 2-1. HTML — 뼈대

**HTML(HyperText Markup Language)** 은 웹 페이지의 **구조와 내용**을 담당합니다.

사실 HTML이 생소하게 느껴질 수 있는데, 이미 6주 동안 매주 쓰고 있었습니다. 바로 **Markdown**이 HTML을 사람이 편하게 쓸 수 있도록 만든 축약 버전이기 때문입니다. 이 강의 자료도 Markdown으로 작성되어 HTML 형태로 변환되어 제공되고 있습니다.

아래 표를 보면 둘이 얼마나 비슷한지 바로 느껴집니다:

| | Markdown (우리가 쓰는 것) | HTML (브라우저가 읽는 것) |
|---|---|---|
| 큰 제목 | `# Vinoperfect Serum` | `<h1>Vinoperfect Serum</h1>` |
| 중간 제목 | `## 제품 설명` | `<h2>제품 설명</h2>` |
| 문장 | (그냥 씀) | `<p>피부 톤을 고르게 해주는 세럼</p>` |
| 링크 | `[Sephora](URL)` | `<a href="URL">Sephora</a>` |
| 굵게 | `**브랜드명**` | `<strong>브랜드명</strong>` |
| 이미지 | `![설명](경로)` | `<img src="경로" alt="설명" />` |

Markdown은 "사람이 읽고 쓰기 편하게" 만들어진 것이고, HTML은 "브라우저가 정확하게 해석하도록" 설계된 것입니다. Markdown을 쓰면 변환기가 자동으로 HTML로 바꿔서 브라우저에 전달합니다.

스크래핑 관점에서 HTML이 중요한 이유는, 모든 텍스트·이미지·가격 정보가 HTML 태그 안에 담겨 있기 때문입니다. 데이터를 뽑으려면 "어떤 태그 안에 있는지"를 찾아야 합니다.

#### 태그에 붙는 속성(Attribute)

HTML 태그에는 추가 정보인 **속성**이 붙을 수 있습니다. Markdown의 링크 문법 `[텍스트](URL)` 에서 URL에 해당하는 것이 HTML에서는 `href` 속성입니다.

```html
<a href="https://sephora.com/brand/caudalie"
   class="brand-link"
   id="main-brand"
   data-at="brand_name">
  Caudalie
</a>
```

| 속성 | 의미 | 스크래핑에서 쓰는 이유 |
|---|---|---|
| `href` | 링크가 연결될 주소 | 연결된 URL 추출할 때 |
| `class` | 스타일 그룹 이름 | 요소 식별에 쓰이지만 **불안정**함 (이유는 CSS 섹션에서) |
| `id` | 이 페이지 안에서 단 하나뿐인 고유 이름 | 가장 **안정적**인 식별자 |
| `data-at` | 개발자가 테스트 목적으로 붙인 이름 | 안정적인 식별자 |
| `src` | 이미지/파일이 있는 경로 | 이미지 URL 추출할 때 |

---

### 2-2. CSS — 스타일

**CSS(Cascading Style Sheets)** 는 HTML이 만든 구조에 **색상, 크기, 배치** 등 시각적 스타일을 입히는 언어입니다.

여기서 **Cascading(폭포처럼 흘러내림)** 이라는 단어에 주목할 필요가 있습니다. CSS의 핵심 동작 방식을 한 단어로 표현한 것입니다.

> 💡 **폭포 비유**
>
> 위에서 정의한 스타일 규칙이 아래로 흘러내리면서 적용됩니다.
>
> ```css
> /* 사이트 전체 글씨를 회색으로 */
> body { color: gray; }
>
> /* 그 중에서 제목만 검은색으로 덮어씀 */
> h1 { color: black; }
>
> /* 그 중에서도 id="main-title"인 제목만 파란색으로 덮어씀 */
> #main-title { color: blue; }
> ```
>
> 위에서 "전체는 회색"이라고 했더라도, 아래에서 더 구체적인 규칙이 내려오면 그게 우선 적용됩니다. 폭포가 위에서 아래로 흘러내리듯, 더 아래에 있는 구체적인 규칙이 이깁니다.

#### ⚠️ 스크래핑에서 class가 불안정한 이유

HTML 섹션에서 `class`가 불안정하다고 했는데, CSS를 알면 이해가 됩니다.

현대 웹사이트는 배포(업데이트)할 때 CSS를 자동으로 최적화하면서 class 이름을 짧게 압축합니다. 예를 들어 원래 `.brand-name-link`였던 class가 자동 압축 후에는 `.css-1a8e5pi`가 됩니다. 다음 배포 때는 또 `.css-3f9k2m`으로 바뀝니다.

```
오늘:    <a class="css-1a8e5pi">Caudalie</a>  ← 자동 생성된 class
내일 배포 후: <a class="css-2b9f3qr">Caudalie</a>  ← 바뀜 💀

오늘:    <a data-at="brand_name">Caudalie</a>  ← 개발자가 직접 붙인 속성
내일 배포 후: <a data-at="brand_name">Caudalie</a>  ← 그대로 ✅
```

그래서 스크래핑 코드를 만들 때는 자동생성 class 대신 `id`, `data-at` 같은 안정적인 속성을 셀렉터로 사용해야 합니다. LLM에게 코드 생성을 요청하면 이걸 알아서 판단해줍니다.

---

### 2-3. DOM — 브라우저가 만드는 완성본

**DOM(Document Object Model)** 은 브라우저가 HTML 파일을 읽은 뒤 **메모리 안에 재구성한 트리 구조**입니다.

HTML 파일과 DOM이 왜 다른 개념인지 헷갈릴 수 있는데, 레고로 비유하면 이렇습니다.

> 💡 **레고 비유**
>
> **HTML 파일** = 레고 조립 설명서(종이)
> **DOM** = 그 설명서를 보고 실제로 조립해 놓은 레고 완성품
> **JS** = 완성된 레고에서 블록을 추가하거나 교체하는 수정 작업
>
> 우리가 화면에서 보는 것은 **DOM(완성품)** 이고, `Ctrl+U`로 보는 View Source는 **HTML 파일(설명서)** 입니다. JS가 완성품을 계속 수정하기 때문에, 둘이 다를 수 있습니다.

이것이 스크래핑에서 중요한 이유가 있습니다. 어떤 사이트는 HTML 파일에 상품 가격이 없고, JS가 나중에 서버에서 가격을 받아와서 DOM에 추가합니다. 이런 경우 HTML 파일만 받아서는 가격을 뽑을 수 없습니다.

| 확인 방법 | 내용 | 스크래핑에서의 의미 |
|---|---|---|
| `Ctrl+U` View Source | 서버가 처음 보낸 HTML 파일 원문 | JS 실행 전 상태 |
| `F12` Elements 탭 | 현재 DOM 상태 (JS 실행 후) | 화면에 실제 보이는 상태 |

> 화면에 가격이 보이는데 View Source(`Ctrl+U`)에서 가격이 안 보인다면? → JS가 나중에 서버에서 불러와서 DOM에 끼워넣은 것입니다. 이 경우는 별도 전략이 필요합니다(4절 정적/동적 판단 참고).

---

### 2-4. JS — 페이지를 살아있게 만드는 것

**JS(JavaScript)** 는 HTML/CSS가 만든 정적인 페이지를 **동적으로 살아있게** 만드는 코드입니다.

> 💡 **비유로 이해하기**
>
> HTML이 건물의 **설계도**, CSS가 **인테리어 지침**이라면,
> JS는 건물에 **실제로 출근한 직원**입니다. 버튼을 누르면 반응하고, 스크롤하면 콘텐츠를 더 불러오고, 로그인 상태를 기억하는 등 모든 "동작"을 JS가 담당합니다.

JS가 스크래핑에 영향을 주는 대표적인 상황:

**상황 1: 가격이나 재고가 HTML에 없는 경우**
페이지가 열리면 JS가 서버에 "이 상품 가격 알려줘"라고 요청(API 호출)하고, 응답을 받아서 DOM에 끼워넣습니다. HTML 파일을 받는 시점에는 가격이 없고, JS가 실행된 후에야 나타납니다.

**상황 2: 무한 스크롤**
인스타그램이나 쇼핑몰 목록처럼, 스크롤을 내릴 때마다 JS가 다음 상품 목록을 불러옵니다. 한 번에 전체를 받아오는 게 아니므로, 스크롤 동작을 시뮬레이션하지 않으면 첫 화면 데이터밖에 못 뽑습니다.

**상황 3: "더보기" 버튼 뒤의 리뷰**
리뷰가 처음 6개만 보이고 "더보기"를 눌러야 나머지가 로드되는 경우, 버튼 클릭까지 시뮬레이션해야 합니다.

> 💡 **이번 주 실습 범위**
>
> JS 때문에 생기는 복잡한 상황은 Playwright 같은 도구가 필요하고, 이건 심화 내용입니다.
> 이번 주는 **HTML 파일 안에 데이터가 있는 정적 페이지** 또는 **API를 직접 호출하는 방식**에 집중합니다.

---

## 3. LLM 기반 스크래핑 워크플로우 — 실습의 핵심

이번 주 수업의 진짜 핵심은 개념보다 이 워크플로우입니다.

> **URL만 있으면 됩니다. 코드는 LLM이 짜줍니다.**

아래 6단계가 이번 주 실습의 전체 흐름입니다.

---

### Step 1 — 목표 URL 정하기

수집하고 싶은 페이지 URL을 준비합니다.

```
예시:
- 경쟁사 제품 페이지: https://www.sephora.com/product/...-P12345
- PubMed 검색 결과: https://pubmed.ncbi.nlm.nih.gov/?term=retinol+stability
- 식약처 고시: https://www.mfds.go.kr/...
- 원료사 카탈로그: https://supplier.com/catalog/...
```

자동화 전에 먼저 해당 URL을 직접 브라우저로 열어서, 수집하려는 데이터가 화면에 실제로 보이는지 확인하세요. 화면에 없는 것은 스크래핑으로도 못 뽑습니다.

---

### Step 2 — HTML 수집하기

LLM에게 "이 HTML에서 뭘 뽑아줘"라고 하려면, HTML을 먼저 LLM에 줘야 합니다.

**방법 1: View Source 복사 (가장 간단)**
```
1. 해당 URL 브라우저에서 열기
2. Ctrl+U → View Source 창 열림
3. Ctrl+A → Ctrl+C (전체 복사)
4. LLM 대화창에 붙여넣기
```

**방법 2: Python으로 파일 저장** (LLM에 먼저 이 코드를 짜달라고 요청하세요)
```python
import requests

url = "수집할 URL"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

with open("page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print("저장 완료!")
```

> 💡 **HTML이 너무 길어서 LLM에 못 넣겠다면?**
>
> 전체 HTML이 아니라 원하는 데이터 주변 부분만 잘라서 넣어도 됩니다.
> `F12` → Elements 탭 → 원하는 부분 우클릭 → **Copy > Copy outerHTML**
> 이렇게 하면 해당 영역의 HTML만 복사할 수 있습니다.

---

### Step 3 — LLM에게 코드 요청하기

HTML과 원하는 데이터를 함께 LLM에 전달합니다.

```
아래는 Sephora 상품 페이지의 HTML이야.
여기서 다음 정보를 추출하는 Python 코드를 작성해줘:
- 브랜드명
- 상품명
- 가격
- 평점 (숫자만)
- 전성분

조건:
- requests + BeautifulSoup 사용
- 결과를 pandas DataFrame으로 만들기
- Excel 파일로 저장하기 (output.xlsx)
- 한글 주석 포함

[HTML 붙여넣기]
```

---

### Step 4 — 코드 실행하기

LLM이 만들어준 코드를 Antigravity에 붙여넣고 실행합니다.

잘 실행됐다면 Step 5로, 에러가 났다면:

```
에러가 났어. 에러 메시지 알려줄게:
[에러 메시지 복사 붙여넣기]

어떻게 고치면 돼?
```

에러 메시지를 그대로 복사해서 다시 LLM에 주면 됩니다. 직접 코드를 읽고 고칠 필요 없습니다.

---

### Step 5 — 결과 확인 및 보완

수집된 데이터를 열어보고, 필요한 부분을 LLM에 추가 요청합니다.

```
잘 됐어. 그런데 전성분에 불필요한 설명이 같이 들어왔어.
"Aqua"로 시작하는 부분부터만 남겨줘.
```

---

### Step 6 — (선택) Streamlit UI 추가하기

여러 URL을 반복해서 처리할 일이 생기면, 이 코드를 Streamlit 앱으로 감싸달라고 요청합니다.

```
이 스크래핑 코드를 Streamlit 앱으로 만들어줘.
- URL 입력 텍스트 박스
- "수집 시작" 버튼
- 결과를 표로 보여주기
- Excel 다운로드 버튼
```

---

### 전체 흐름 한눈에

```
URL 준비
  ↓
HTML 수집 (View Source 또는 requests)
  ↓
LLM: "이 HTML에서 ○○ 뽑는 코드 짜줘"
  ↓
코드 실행
  ↓ (에러 나면 에러 메시지 → LLM → 수정)
결과 확인 및 보완 요청
  ↓
(선택) Streamlit UI 추가
  ↓
Excel 저장 완료 ✅
```

---

## 4. DevTools — 페이지 속 들여다보기

브라우저에 내장된 개발자 도구(DevTools, `F12`)는 스크래핑할 때 **지도** 역할을 합니다. HTML 구조 확인, 숨겨진 API 탐색, 셀렉터 테스트를 모두 여기서 할 수 있습니다.

> 💡 **비유**
>
> 식당에서 메뉴판만 보는 게 일반 브라우징이라면, DevTools는 주방 문을 살짝 열어서 "이 요리가 어떤 재료로, 어떤 순서로 만들어지는지" 들여다보는 것입니다.

---

### 탭별 역할

| 탭 | 무엇을 볼 수 있나요 | 언제 쓰나요 |
|---|---|---|
| **Elements** | 현재 DOM 구조, 각 요소의 HTML | 원하는 데이터가 어느 태그에 있는지 찾을 때 |
| **Network > Fetch/XHR** | 페이지가 호출하는 API 요청과 JSON 응답 | 가격·리뷰 등 동적으로 불러오는 데이터 찾을 때 |
| **Console** | JavaScript 명령 직접 실행 | 셀렉터가 올바른지 즉석에서 테스트할 때 |
| **Application** | 쿠키, 세션 정보 | 로그인이 필요한 페이지 다룰 때 |

---

### Elements 탭으로 셀렉터 찾기

```
1. F12 눌러 DevTools 열기
2. Elements 탭 클릭
3. 좌상단 마우스 커서 아이콘 클릭 (또는 Ctrl+Shift+C)
4. 페이지에서 원하는 데이터 위에 마우스를 올리고 클릭
   → Elements 탭이 해당 HTML 태그로 자동 이동
5. 태그에 붙은 속성 확인 (id, data-at 등)
6. 태그 우클릭 → Copy > Copy outerHTML 로 해당 HTML 복사
```

예를 들어 Sephora에서 브랜드명을 클릭하면:

```html
<a class="css-1a8e5pi"  ← ❌ 이건 바뀜
   data-at="brand_name" ← ✅ 이걸 쓰면 안정적
   href="/brand/caudalie">
  Caudalie
</a>
```

이렇게 `data-at="brand_name"` 을 발견했다면, LLM에게 "data-at이 brand_name인 요소에서 텍스트를 뽑아줘"라고 하면 됩니다.

---

### Network 탭에서 숨겨진 API 찾기

화면에는 보이는데 View Source에서 안 보이는 데이터(가격, 리뷰, 재고 등)는 JS가 API를 호출해서 가져온 것입니다. Network 탭에서 그 API를 직접 찾을 수 있습니다.

```
1. F12 → Network 탭
2. 🚫 아이콘으로 기록 초기화
3. 페이지 새로고침 (또는 원하는 동작 수행: 스크롤, 탭 클릭 등)
4. 상단에서 Fetch/XHR 필터 클릭
5. 목록에서 응답 크기가 큰 요청들을 클릭해서 확인
6. Preview 탭 → JSON 데이터 안에 원하는 데이터가 있으면 성공
```

API를 직접 찾으면 HTML 파싱 없이 **JSON으로 깔끔하게** 데이터를 받아올 수 있습니다. 복잡한 HTML 구조를 파헤칠 필요 없이, 원하는 데이터만 딱 오는 것입니다.

---

### 정적 페이지인지 동적 페이지인지 판단하기

스크래핑 전략이 달라지므로 먼저 확인해야 합니다.

```
Step 1. Ctrl+U (View Source) → Ctrl+F로 원하는 텍스트(가격, 브랜드명 등) 검색
        → 있으면: 정적 페이지 → requests + BeautifulSoup으로 해결 가능 ✅
        → 없으면: Step 2로

Step 2. F12 → Network → Fetch/XHR에서 JSON 응답 확인
        → 원하는 데이터가 JSON에 있으면: API 직접 호출 (가장 깔끔) ✅
        → 없으면: Step 3으로

Step 3. 동적 렌더링 필요 → Playwright 사용 (심화)
```

---

## 5. 실전 사례 — Sephora 화장품 정보 수집

화장품 R&D 연구원 관점에서 Sephora는 **경쟁사 성분 분석, 리뷰 수집, 가격 모니터링**에 유용한 사이트입니다. 실제로 어떤 전략으로 접근하는지 단계별로 살펴봅니다.

대상: `https://www.sephora.com/product/vinoperfect-brightening-dark-spot-serum-P94421`

---

### 5-1. 셀렉터 탐색

F12 → Elements 탭에서 브랜드명을 클릭하면:

```html
<a class="css-1a8e5pi e15t7owz0"
   data-at="brand_name"
   href="/brand/caudalie">
  Caudalie
</a>
```

CSS 섹션에서 설명한 것처럼 `class`는 배포할 때마다 바뀌지만, `data-at="brand_name"`은 안정적입니다. 이렇게 안정적인 속성을 찾아두면 몇 달 뒤에도 코드가 동작합니다.

이 방식으로 찾은 주요 셀렉터:

| 수집 데이터 | 셀렉터 | 특이사항 |
|---|---|---|
| 브랜드명 | `[data-at="brand_name"]` | — |
| 상품명 | `[data-at="product_name"]` | — |
| 별점 | `[data-comp="StarRating"]` | `aria-label` 속성에 "4.5 stars" 형태로 있음 |
| 리뷰 수 | `[data-at="number_of_reviews"]` | "4.1K" 형태 |
| 전성분 | `#ingredients` | 후처리 필요 |
| 제품 이미지 | `[data-comp="Carousel"] img` | 비디오 썸네일 혼재 → 필터링 필요 |

---

### 5-2. 전성분 추출 — 화장품만의 특이한 구조

`#ingredients` 에서 텍스트를 뽑으면 이런 구조가 나옵니다:

```
Key Ingredients:
- Viniferine: Brightening active...
- Hyaluronic Acid: Plumping...

Aqua, Glycerin, Niacinamide, Viniferine...

The ingredient list may vary slightly depending on batch.
```

앞뒤에 불필요한 설명이 붙어 있어서 전성분만 잘라내야 합니다.

```
정제 규칙:
1. "-"로 시작하는 줄 제거  (주요 성분 마케팅 설명)
2. "Aqua" 또는 "Water"로 시작하는 줄부터 자르기  (전성분 시작점)
3. "The ingredient"로 시작하는 줄부터 뒤는 제거  (면책 문구)
```

> 💡 **왜 "Aqua"가 기준점이 될까요?**
>
> 화장품 전성분 표기는 INCI 국제 규정상 **함량이 많은 순서**로 나열합니다. 대부분의 수성 제형에서 정제수(Aqua/Water)가 1위이므로, 전성분 리스트는 거의 항상 "Aqua" 또는 "Water"로 시작합니다. 이걸 앵커로 쓰면 앞에 붙은 마케팅 설명을 깔끔하게 잘라낼 수 있습니다.

---

### 5-3. JSON-LD — 이미 정리된 데이터가 숨어있다

View Source에서 `ld+json`을 검색하면 특별한 것을 발견할 수 있습니다:

```json
{
  "@type": "ProductGroup",
  "name": "Vinoperfect Brightening Dark Spot Serum...",
  "brand": { "name": "Caudalie" },
  "image": "https://www.sephora.com/productimages/sku/s2744423-main-hero.jpg",
  "hasVariant": [
    {
      "sku": "2744423",
      "offers": { "price": "82.0", "priceCurrency": "USD" }
    }
  ]
}
```

이게 뭔가요? 구글 같은 검색엔진이 상품 정보를 잘 이해할 수 있도록, 사이트가 HTML 안에 미리 구조화해서 넣어둔 데이터입니다.

검색엔진을 위해 사이트가 "이미 정리해둔" 데이터이므로, 우리가 그냥 가져다 쓸 수 있습니다. CSS 셀렉터를 하나도 몰라도 상품명·브랜드·가격·이미지를 한 번에 뽑을 수 있고, 배포가 바뀌어도 구조가 거의 유지됩니다.

---

### 5-4. 리뷰 API — 수천 건 리뷰를 깔끔하게

F12 → Network → Fetch/XHR에서 리뷰 탭을 클릭하면 이런 요청이 잡힙니다:

```
https://api.bazaarvoice.com/data/reviews.json
  ?Filter=ProductId:P94421
  &Limit=6
  &Offset=0     ← 이것만 6씩 올리면 다음 페이지
  ...
```

`Offset` 값을 0, 6, 12, 18... 로 바꿔가며 요청하면 전체 리뷰(4000건 이상)를 브라우저 없이 다 받아올 수 있습니다. 응답이 JSON이라 파싱도 간단합니다:

| 필드 | JSON 키 | R&D 활용 예시 |
|---|---|---|
| 별점 | `Rating` | 평점 분포 분석 |
| 리뷰 본문 | `ReviewText` | 성분 키워드 빈도 분석 |
| 피부타입 | `ContextDataValues.skinType.ValueLabel` | 타겟 피부타입 파악 |
| 나이대 | `ContextDataValues.ageRange.ValueLabel` | 소비자층 분석 |
| 추천 여부 | `IsRecommended` | 추천율 집계 |

---

## 6. 스크래퍼 설계 전략 (3트랙)

Sephora 하나의 상품 페이지에서도 데이터 종류에 따라 최적 방법이 다릅니다.

```
[ URL 입력 ]
    ↓
[ HTML 수집 ]  requests.get(url)
    ↓
┌──────────────┬──────────────────┬──────────────────┐
│  1트랙        │  2트랙            │  3트랙            │
│  JSON-LD     │  DOM 셀렉터       │  리뷰 API        │
│  상품명/가격  │  별점/성분/이미지  │  리뷰 대량 수집   │
│  난이도 ⭐    │  난이도 ⭐⭐       │  난이도 ⭐⭐       │
└──────────────┴──────────────────┴──────────────────┘
    ↓
[ pandas DataFrame → Excel 저장 ]
```

---

### 1트랙: JSON-LD 파싱

HTML 안에 숨어있는 구조화 데이터를 꺼냅니다. 셀렉터를 찾을 필요가 없어서 가장 안정적입니다.

```python
import requests
from bs4 import BeautifulSoup
import json

url = "https://www.sephora.com/product/...-P94421"
res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(res.text, "html.parser")

ld = soup.find("script", type="application/ld+json")
data = json.loads(ld.string)

brand = data["brand"]["name"]
name  = data["name"]
price = data["hasVariant"][0]["offers"]["price"]
```

> 이 코드를 직접 외울 필요 없습니다. LLM에게 "이 HTML에서 JSON-LD로 상품명, 브랜드, 가격 뽑는 코드 짜줘"라고 하면 됩니다.

---

### 2트랙: DOM 셀렉터 파싱

Elements 탭에서 찾은 셀렉터로 특정 요소의 텍스트를 뽑습니다.

```python
import re

# 별점: aria-label에 "4.5 stars" 형태로 들어있음
star_el = soup.select_one('[data-comp="StarRating"]')
aria    = star_el.get("aria-label", "")
rating  = re.search(r"([\d.]+)", aria).group(1)   # "4.5"

# 전성분: 후처리로 정제
ing_el   = soup.select_one("#ingredients")
raw_text = ing_el.get_text(separator="\n")
lines    = [l for l in raw_text.splitlines() if not l.startswith("-")]
ing_text = "\n".join(lines)
```

---

### 3트랙: 리뷰 API 호출

Network 탭에서 찾은 API 엔드포인트를 직접 호출합니다.

```python
import requests, time

PASSKEY = "calXm2DyQVjcCy9agq85vmTJv5ELuuBCF2sdg4BnJzJus"
PRODUCT = "P94421"
all_reviews = []
offset  = 0

while True:
    params = {
        "Filter": f"ProductId:{PRODUCT}",
        "Limit": 6, "Offset": offset,
        "passkey": PASSKEY, "apiversion": "5.4",
    }
    data = requests.get(
        "https://api.bazaarvoice.com/data/reviews.json", params=params
    ).json()

    all_reviews.extend(data["Results"])
    print(f"{len(all_reviews)} / {data['TotalResults']} 수집 완료")

    if offset + 6 >= data["TotalResults"]:
        break
    offset += 6
    time.sleep(5)   # 서버 부하 방지
```

---

### 도구 요약

| 역할 | 도구 |
|---|---|
| HTTP 요청 | `requests` |
| HTML 파싱 | `BeautifulSoup` |
| JSON 파싱 | `json` (파이썬 내장) |
| 결과 저장 | `pandas` → Excel |
| 동적 페이지 (심화) | `Playwright` |

---

### 자주 만나는 예외 상황

| 상황 | 대응 |
|---|---|
| 실행은 됐는데 결과가 비어있음 | 셀렉터가 틀렸거나 동적 페이지일 가능성 → Elements 탭에서 재확인 |
| 요청이 막힘 (403 오류) | User-Agent 헤더 추가, 혹은 요청 간격 늘리기 |
| passkey 만료 | Network 탭에서 새 요청 잡아서 passkey 갱신 |
| 전성분이 지저분하게 들어옴 | LLM에게 정제 규칙 설명하고 후처리 코드 추가 요청 |

---

## 7. AI 프롬프트 예시 모음

아래 템플릿의 `[ ]` 부분을 상황에 맞게 바꿔 사용하세요.

---

**기본 스크래핑 코드 요청**
```
아래 URL의 HTML에서 [브랜드명, 상품명, 가격, 별점, 전성분]을 추출하는
Python 코드를 작성해줘.

조건:
- requests + BeautifulSoup 사용
- pandas DataFrame으로 만들기
- output.xlsx로 저장
- 한글 주석 포함

URL: [URL 입력]
HTML: [HTML 붙여넣기]
```

---

**에러 수정 요청**
```
아래 코드 실행했는데 에러 났어.
에러 메시지: [에러 내용]
어떻게 고치면 돼?

[코드 붙여넣기]
```

---

**Streamlit UI 추가 요청**
```
아래 스크래핑 코드를 Streamlit 앱으로 바꿔줘.
- URL 입력 텍스트 박스
- "수집 시작" 버튼
- st.spinner로 진행 중 표시
- 결과를 표로 보여주기
- Excel 다운로드 버튼

[코드 붙여넣기]
```

---

**여러 URL 일괄 처리**
```
아래 코드를 수정해줘.
URL을 한 줄에 하나씩 여러 개 입력받아서
전체를 순서대로 처리하고 결과를 하나의 Excel로 합쳐 저장하도록 해줘.
URL 사이에 3초 대기 넣어줘.

[코드 붙여넣기]
```

---

**전성분 후처리 요청**
```
스크래핑한 전성분 텍스트가 아래처럼 섞여 있어.
"- Key ingredient: Vitamin C\nAqua, Glycerin...\nThe ingredient list may vary"

정제 규칙:
1. "-"로 시작하는 줄 제거
2. "Aqua" 또는 "Water"로 시작하는 부분부터만 남기기
3. "The"로 시작하는 줄 이후 모두 제거
4. 쉼표로 구분된 리스트로 변환

이 처리를 해주는 코드 추가해줘.
```

---

## 8. 스크래핑 에티켓과 주의사항

기술적으로 가능하다고 해서 뭐든 해도 되는 건 아닙니다.

**robots.txt 확인** — 작업 전에 `https://[도메인]/robots.txt` 항상 확인하세요. `Crawl-delay`가 명시되어 있으면 그 간격을 지켜야 합니다.

**요청 속도 조절** — `time.sleep(3)` 이상의 대기를 반드시 넣으세요. 대기 없이 수백 건을 한꺼번에 요청하면 IP 차단 또는 법적 문제가 생길 수 있습니다.

**이용약관 확인** — 많은 사이트가 이용약관에 "자동화된 수집 금지" 조항을 둡니다. 대규모 수집 전에는 사내 법무 검토가 필요합니다.

**개인정보 주의** — 리뷰에 포함된 닉네임, 사진 등은 GDPR 적용 대상일 수 있습니다. 사내 활용 시에도 익명화 처리를 권장합니다.

**실습에 안전한 사이트:**

| 사이트 | 접근 방식 | 활용 |
|---|---|---|
| PubMed | API 제공 (무료) | 논문 메타데이터 |
| 식약처 의약품정보 | 허용 | 성분 데이터 |
| Wikipedia | API 제공 | 성분 정의 |
| Sephora | ⚠️ 소량만 | 교육 목적 실습 |
| 쿠팡, 네이버쇼핑 | ❌ ToS 금지 | — |

---

## 📌 이번 주 핵심 정리

| 개념 | 한 줄 요약 |
|---|---|
| 크롤링 | 링크 따라 URL 목록 수집 |
| 스크래핑 | 특정 페이지에서 데이터 추출 |
| HTML | 웹 페이지의 구조와 내용 (Markdown의 원형) |
| CSS | HTML에 스타일 입힘, 폭포처럼 위 규칙이 아래로 흘러내림 |
| DOM | 브라우저가 HTML로 만든 메모리 완성품 |
| JS | 페이지를 동적으로 만드는 코드 |
| JSON-LD | 검색엔진용으로 사이트가 미리 정리해둔 구조화 데이터 |
| requests | Python으로 URL에 HTTP 요청 보내는 도구 |
| BeautifulSoup | HTML에서 원하는 요소 찾아주는 도구 |
| 핵심 워크플로우 | URL → HTML → LLM에 코드 요청 → 실행 → Excel 저장 |

---

## 📚 이후에 배울 것들

| 주제 | 설명 |
|---|---|
| Playwright | JS가 실행되어야 나타나는 동적 데이터, 클릭·스크롤 시뮬레이션 |
| Playwright Network 감지 | API passkey 만료 시 자동 재추출 |
| Web Agent | AI가 직접 브라우저를 조작하는 자동화 에이전트 |

---

## 📝 과제

정기적으로 확인하는 웹사이트 1개를 골라서:

1. View Source에서 원하는 데이터가 보이는지 확인 (정적/동적 판단)
2. 위 프롬프트 예시를 참고해서 LLM에 코드 요청
3. 코드 실행 → 결과 Excel 저장
4. (선택) Streamlit UI 추가

다음 주에 사이트, 코드, 결과 Excel 간단히 공유해 주세요.
