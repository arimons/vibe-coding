---
layout: page
title: "Week 03.5: 터미널 기초 실습"
nav_order: 12
---

# Week 03.5 — 터미널 기초 실습

> 이 주차는 정식 커리큘럼 사이에 끼어있는 **생존 훈련**입니다.  
> AI에게 맡기기 전에, 내가 지금 어디 있고 뭘 실행하는지 눈으로 확인하는 능력을 키웁니다.

---

## 왜 터미널을 알아야 하나요?

Antigravity의 AI가 코드를 대신 써줘도, **"이 파일을 실행해"** 라는 명령은 결국 어딘가에서 실행됩니다.  
그 "어딘가"를 모르면, 에러가 났을 때 왜 났는지 알 수 없어요.

터미널은 컴퓨터에게 직접 말을 거는 창구입니다.  
파일 탐색기를 마우스로 클릭하는 것과 똑같은 일을 **텍스트로** 하는 것입니다.

---

## 핵심 개념: IDE ≠ 실행 위치

Antigravity의 File View가 `vibe-coding` 전체를 보여주더라도,  
실제로 파일이 **실행되는 위치**는 터미널의 `pwd`가 가리키는 곳입니다.

```
Antigravity File View        터미널 (실제 실행 위치)
─────────────────────        ──────────────────────
vibe-coding/ (항상)     ≠    cd tutorials/week03.5/drill05_streamlit
  ├── docs/                   $ streamlit run app.py
  ├── tutorials/
  └── antigravity-config/
```

**File View는 참고용 지도, 터미널의 `pwd`가 내 실제 위치입니다.**

---

## 핵심 명령어 퀵 레퍼런스

```bash
# ── 위치 확인 / 이동 ───────────────────────────
pwd                   # 지금 내가 어디 있는지
ls                    # 현재 폴더 내용 보기
ls -la                # 숨김파일 포함 상세 보기
cd 폴더명             # 폴더 안으로 이동
cd ..                 # 한 단계 위로
cd ../다른폴더        # 위로 갔다가 옆 폴더로

# ── Python 실행 ────────────────────────────────
python 파일명.py      # Python 파일 실행
Tab 키                # 파일명/명령어 자동완성 (꼭 쓰기!)

# ── 패키지 설치 (전역) ─────────────────────────
pip install 패키지명              # 단일 패키지 설치
pip install 패키지1 패키지2       # 여러 패키지 한 번에
pip list                          # 설치된 패키지 확인

# ── Streamlit 실행 ─────────────────────────────
streamlit run app.py  # 브라우저에 웹앱 열기 (Ctrl+C로 종료)

# ── 가상환경 (개인 프로젝트부터 사용) ──────────
python -m venv .venv              # 가상환경 생성
source .venv/bin/activate         # 활성화 (Mac/Linux)
.venv\Scripts\activate            # 활성화 (Windows)
deactivate                        # 비활성화
```

---

## 실습 패키지 전역 설치

이번 실습에서 필요한 패키지를 한 번에 설치합니다.  
터미널을 열고 아래 명령어를 실행하세요.

```bash
pip install rich streamlit pandas
```

> **왜 전역(global) 설치를 하나요?**  
> 가상환경은 프로젝트마다 패키지를 **따로** 설치하는 방식이라, 설치 시 수백~수천 개 파일을 새로 생성합니다.  
> 사내 환경에서는 보안 프로그램의 파일 감시로 I/O 병목이 심해 설치에 수십 분이 걸릴 수 있어요.  
> 실습 단계에서는 충돌 위험이 낮으므로 전역 설치로 진행하고,  
> **개인 프로젝트 시작(Week 8)부터 가상환경을 구축합니다.**  
> Drill 04에서 가상환경 개념은 체험해봅니다.

---

## 실습 파일 위치

```
tutorials/week03.5/
├── drill01_navigation/    ← ls, cd, pwd 탐색 훈련
├── drill02_plain_run/     ← python 파일명.py 기본 실행
├── drill03_module/        ← 실행 위치의 중요성
├── drill04_venv/          ← 가상환경 개념 체험
└── drill05_streamlit/     ← 실전 종합 (streamlit run)
```

---

## Drill 01 — 폴더 탐색

**폴더:** `tutorials/week03.5/drill01_navigation/`

`ls`와 `cd`만으로 `secret.py` 파일을 찾아서 실행하세요. 힌트는 없습니다.

```bash
# 1. 실습 폴더로 이동
cd tutorials/week03.5/drill01_navigation

# 2. 내용 확인
ls

# 3. 탐색하며 secret.py 찾기 (힌트: 폴더 안에 폴더가 있습니다)

# 4. 찾았으면 실행
python secret.py

# 5. 루트로 복귀
cd ../../..
pwd    # vibe-coding 이어야 합니다
```

**체크포인트**

- [ ] `pwd`로 현재 위치 확인할 수 있다
- [ ] `ls`로 폴더 내용을 볼 수 있다
- [ ] `cd 폴더명` / `cd ..`으로 이동할 수 있다
- [ ] `secret.py` 실행 시 메시지가 출력된다

---

## Drill 02 — 단순 실행

**폴더:** `tutorials/week03.5/drill02_plain_run/`

패키지 설치 없이 바로 실행되는 Python 파일 3개를 실행해보세요.

```bash
cd tutorials/week03.5/drill02_plain_run

python hello.py
python calculator.py
python quiz.py
```

`Tab` 키를 꼭 활용하세요. `python hel` 까지 치고 Tab을 누르면 자동완성됩니다.

---

## Drill 03 — 지도 읽기 (실행 위치가 왜 중요한가)

**폴더:** `tutorials/week03.5/drill03_module/`

### 비유: 지도와 현재 위치

지도에 "우체국은 여기서 오른쪽 200m"라고 적혀 있어도,  
**내가 지금 어디 있는지** 모르면 그 안내는 쓸모가 없습니다.

Python의 `import`도 마찬가지입니다.

```python
# main.py 안에 이런 코드가 있다면
from utils.helper import greet
```

이 코드는 **"지금 내가 있는 폴더에서 utils 폴더를 찾아라"** 라는 뜻입니다.

### 일부러 에러 내보기 → 원인 파악

```bash
# ❌ 잘못된 위치에서 실행
cd tutorials/week03.5/drill03_module/utils
python ../main.py
# ModuleNotFoundError: No module named 'utils'

# ✅ 올바른 위치에서 실행
cd tutorials/week03.5/drill03_module
python main.py
```

에러 원인은 딱 하나, **실행 위치가 틀렸기 때문**입니다.

**체크포인트**

- [ ] 잘못된 위치에서 실행 → `ModuleNotFoundError` 확인
- [ ] 올바른 위치로 이동 후 실행 → 정상 출력 확인
- [ ] 에러 원인을 말로 설명할 수 있다

---

## Drill 04 — 가상환경 개념 체험

**폴더:** `tutorials/week03.5/drill04_venv/`

### 가상환경이란?

**비유: 개인 실험실**

학교 공용 실험실에는 모두가 공유하는 시약이 있습니다.  
내가 원하는 버전의 시약이 없거나, 다른 사람 실험과 섞일 수 있어요.

**개인 실험실(가상환경)** 을 만들면:
- 이 프로젝트에 필요한 패키지만 격리해서 설치
- 다른 프로젝트와 버전 충돌 없음
- 실험실을 통째로 지워도 컴퓨터 본체에 영향 없음

### activate / deactivate 구조

```
[시스템 Python]  ──activate──▶  [.venv 가상환경]
                 ◀─deactivate──
```

| 상태 | 프롬프트 | 의미 |
|------|---------|------|
| 비활성화 | `$` | 시스템 Python 사용 중 |
| 활성화 | `(.venv) $` | 가상환경 사용 중 |

`(.venv)` 가 앞에 붙으면 "내 실험실 안에 있다"는 신호입니다.

### 전체 흐름 체험

```bash
cd tutorials/week03.5/drill04_venv

# 1. 가상환경 생성
python -m venv .venv
ls    # .venv/ 폴더 생성 확인

# 2. 활성화
source .venv/bin/activate        # Mac/Linux
# .venv\Scripts\activate         # Windows
# → 프롬프트 앞에 (.venv) 가 붙었는지 확인!

# 3. 이 환경에 rich 설치
pip install rich

# 4. 실행
python app.py

# 5. 비활성화
deactivate
# → (.venv) 가 사라졌는지 확인!
```

> **지금 실습에서는 전역 설치를 사용합니다.**  
> 가상환경은 개념 체험용으로 만들어보는 것입니다.  
> Week 8 개인 프로젝트 시작 전에 가상환경을 다시 구축해서 사용합니다.

### .venv 폴더는 git에 올리지 않는다

`.venv/` 안에는 수천 개의 파일이 있습니다.  
대신 `requirements.txt` 하나만 올리면, 누구든 `pip install -r requirements.txt`로 재현 가능합니다.  
`.gitignore`에 `.venv/`를 추가하는 것이 관례입니다.

**체크포인트**

- [ ] `python -m venv .venv` 실행 후 `.venv/` 폴더 생성 확인
- [ ] activate 전후 프롬프트 변화 확인
- [ ] `deactivate` 후 프롬프트 복구 확인

---

## Drill 05 — Streamlit 실전 (종합)

**폴더:** `tutorials/week03.5/drill05_streamlit/`

앞에서 설치한 패키지(`streamlit`, `pandas`)를 사용해 앱을 실행합니다.

```bash
cd tutorials/week03.5/drill05_streamlit

# streamlit run 으로 실행 (python이 아닙니다!)
streamlit run app.py
# → 브라우저가 자동으로 열립니다: http://localhost:8501
# 종료: Ctrl+C
```

### `python app.py` vs `streamlit run app.py`

| 명령어 | 결과 |
|--------|------|
| `python app.py` | 에러 또는 아무것도 안 보임 |
| `streamlit run app.py` | 브라우저에 웹앱 열림 |

Streamlit은 `streamlit` 엔진이 파일을 해석해서 웹으로 보여주는 방식입니다.  
`streamlit` 명령어 자체가 pip으로 설치된 프로그램이므로, 설치가 안 된 환경에서는 명령어 자체를 찾지 못합니다.

### pages/ 폴더 구조

```
drill05_streamlit/
├── app.py            ← 메인 페이지
└── pages/
    ├── 01_chart.py   ← 사이드바에 자동으로 메뉴 생성
    └── 02_form.py
```

파일 이름 앞의 숫자(`01_`, `02_`)가 사이드바 메뉴 순서를 결정합니다.

**체크포인트**

- [ ] `streamlit run app.py` → 브라우저 확인
- [ ] 사이드바에서 01_chart, 02_form 메뉴 클릭
- [ ] `Ctrl+C`로 서버 종료

---

## 전체 체크리스트

| Drill | 핵심 목표 | 의도적 함정 |
|-------|---------|------------|
| 01 | `ls`, `cd`, `pwd` 탐색 | 파일 위치를 알려주지 않음 |
| 02 | `python 파일명.py` 실행 | 없음 (Tab 자동완성 연습) |
| 03 | 실행 위치의 중요성 | 잘못된 위치 → `ModuleNotFoundError` |
| 04 | 가상환경 개념 체험 | activate 전후 프롬프트 비교 |
| 05 | `streamlit run` 실전 | `python`으로 실행 → 동작 안 함 |
