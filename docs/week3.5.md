---
layout: page
title: "Week 3.5: 터미널 기초 실습"
nav_order: 12
---

# Week 3.5 — 터미널 기초 실습

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
Antigravity File View       터미널 (실제 실행 위치)
─────────────────────       ──────────────────────
vibe-coding/ (항상)    ≠    cd tutorials/week3.5/drill05_streamlit
  ├── docs/                  (venv) $ streamlit run app.py
  ├── tutorials/
  └── antigravity-config/
```

**File View는 참고용 지도, 터미널의 `pwd`가 내 실제 위치입니다.**

---

## 핵심 명령어 레퍼런스

```bash
pwd                     # 내가 지금 어디 있는지 확인
ls                      # 현재 폴더 내용 보기
ls -la                  # 숨김파일 포함 상세 보기
cd 폴더명               # 해당 폴더로 이동
cd ..                   # 한 단계 위 폴더로 이동
cd ../다른폴더           # 위로 갔다가 다른 폴더로
python 파일명.py         # Python 파일 실행
Tab 키                  # 명령어/파일명 자동완성
```

---

## 실습 파일 위치

```
tutorials/week3.5/
├── drill01_navigation/    ← ls, cd, pwd 탐색 훈련
├── drill02_plain_run/     ← python 파일명.py 기본 실행
├── drill03_module/        ← 실행 위치의 중요성
├── drill04_venv/          ← 가상환경 생성/활성화/비활성화
└── drill05_streamlit/     ← 실전 종합 (venv + streamlit run)
```

---

## Drill 01 — 폴더 탐색

**폴더:** `tutorials/week3.5/drill01_navigation/`

`ls`와 `cd`만으로 `secret.py` 파일을 찾아서 실행하세요. 힌트는 없습니다.

```bash
cd tutorials/week3.5/drill01_navigation
ls
# → 안이 보입니다. 어디로 가야 할까요?

python secret.py        # 찾았으면 실행
cd ../../..             # 루트로 복귀 후 pwd 확인
```

**체크포인트**
- `pwd`로 현재 위치를 확인할 수 있다
- `ls`로 폴더 내용을 볼 수 있다
- `cd ..`로 위로 올라올 수 있다
- `secret.py` 실행 시 메시지가 출력된다

---

## Drill 02 — 단순 실행

**폴더:** `tutorials/week3.5/drill02_plain_run/`

```bash
cd tutorials/week3.5/drill02_plain_run

python hello.py
python calculator.py
python quiz.py
```

`Tab` 키 자동완성을 꼭 써보세요. `python hel` 까지 치고 Tab을 누르면 자동으로 완성됩니다.

---

## Drill 03 — 지도 읽기 (실행 위치가 왜 중요한가)

**폴더:** `tutorials/week3.5/drill03_module/`

### 비유: 지도와 현재 위치

지도에 "우체국은 여기서 오른쪽 200m"라고 적혀 있어도,  
**내가 지금 어디 있는지** 모르면 그 안내는 쓸모가 없습니다.

Python의 `import`도 마찬가지입니다.

```python
# main.py 안에 이런 코드가 있다면
from utils.helper import greet
```

이 코드는 **"지금 내가 있는 폴더에서 utils 폴더를 찾아라"** 라는 뜻입니다.

### 일부러 에러를 내보기

```bash
# ❌ 잘못된 위치에서 실행 → 에러 발생
cd tutorials/week3.5/drill03_module/utils
python ../main.py
# ModuleNotFoundError: No module named 'utils'

# ✅ 올바른 위치에서 실행
cd tutorials/week3.5/drill03_module
python main.py
```

에러 메시지를 읽어보세요. Python이 "utils를 못 찾겠어요"라고 말하는 이유는 딱 하나, **실행 위치가 틀렸기 때문**입니다.

---

## Drill 04 — 가상환경 (venv)

**폴더:** `tutorials/week3.5/drill04_venv/`

### 개념: 가상환경이란?

**비유: 개인 실험실**

학교 공용 화학 실험실에는 모두가 공유하는 시약이 있습니다.  
내가 쓰고 싶은 시약이 없을 수도 있고, 다른 사람이 쓰는 시약과 섞이면 내 실험이 망가질 수도 있어요.

그래서 내 개인 실험실을 따로 만들면:
- 내가 필요한 것만 설치할 수 있고
- 다른 프로젝트와 섞이지 않고
- 실험실을 통째로 버려도 컴퓨터 본체엔 영향이 없습니다.

Python의 **가상환경(venv)** 이 바로 이 개인 실험실입니다.

### activate / deactivate

```
[시스템 Python] ←→ [내 가상환경]
   deactivate           activate
```

| 상태 | 터미널 프롬프트 | 의미 |
|------|--------------|------|
| 비활성화 | `$` | 시스템 Python 사용 중 |
| 활성화 | `(venv) $` | 내 가상환경 사용 중 |

`(venv)` 가 앞에 붙어 있으면 "나는 지금 내 실험실 안에 있다"는 신호입니다.

### 전체 흐름 실습

```bash
cd tutorials/week3.5/drill04_venv

# 1. 가상환경 생성 (처음 한 번만)
python -m venv venv
ls    # venv/ 폴더가 생겼는지 확인

# 2. 활성화
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 프롬프트가 (venv) $ 로 바뀌었는지 확인!

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 실행
python app.py

# 5. 비활성화
deactivate
```

### 먼저 에러부터 내보기

activate **없이** 실행하면 어떻게 되는지 먼저 확인하세요.  
에러를 먼저 봐야 activate의 의미를 체감할 수 있습니다.

```bash
python app.py
# → ModuleNotFoundError: No module named 'rich'

source venv/bin/activate
python app.py
# → 정상 작동
```

### venv 폴더는 git에 올리지 않는다

`venv/` 안에는 수천 개의 파일이 있습니다.  
대신 `requirements.txt` 하나만 올리면, 다른 사람이 `pip install -r requirements.txt`로 똑같이 재현할 수 있습니다.  
그래서 `.gitignore`에 `venv/`를 추가해두는 것이 관례입니다.

---

## Drill 05 — Streamlit 실전 (종합)

**폴더:** `tutorials/week3.5/drill05_streamlit/`

Drill 04에서 배운 가상환경 흐름을 그대로 적용해서 Streamlit 앱을 실행합니다.

```bash
cd tutorials/week3.5/drill05_streamlit

# 가상환경 생성 + 활성화
python -m venv venv
source venv/bin/activate      # (venv) 확인

# 패키지 설치 (시간이 좀 걸립니다)
pip install -r requirements.txt

# 실행 (python이 아니라 streamlit run!)
streamlit run app.py
# 브라우저가 자동으로 열립니다: http://localhost:8501
# 종료: Ctrl+C
```

### `python app.py` vs `streamlit run app.py`

| 명령어 | 결과 |
|--------|------|
| `python app.py` | 에러 또는 아무것도 안 보임 |
| `streamlit run app.py` | 브라우저에 웹앱 열림 |

Streamlit 앱은 Python 파일을 직접 실행하는 게 아니라,  
`streamlit` 엔진이 그 파일을 해석해서 웹으로 보여주는 방식입니다.  
`streamlit` 명령어 자체도 pip으로 설치된 프로그램이라, **activate 없이는 명령어 자체를 못 찾습니다.**

### pages/ 폴더의 역할

```
drill05_streamlit/
├── app.py           ← 메인 페이지
└── pages/
    ├── 01_chart.py  ← 사이드바에 자동으로 메뉴 생성됨
    └── 02_form.py
```

Streamlit은 `pages/` 폴더를 자동으로 인식해서 사이드바 메뉴로 만들어 줍니다.  
파일 이름 앞의 숫자(`01_`, `02_`)가 메뉴 순서를 결정합니다.

---

## 전체 체크리스트

| Drill | 핵심 목표 | 의도적 함정 |
|-------|---------|------------|
| 01 | ls, cd, pwd 탐색 | 파일 위치를 알려주지 않음 |
| 02 | python 파일명.py 실행 | 없음 (Tab 자동완성 연습) |
| 03 | 실행 위치의 중요성 | 잘못된 위치에서 실행 → 에러 |
| 04 | venv 전체 흐름 | activate 없이 실행 → 에러 |
| 05 | streamlit run + venv 종합 | python으로 실행 → 에러 |
