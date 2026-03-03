---
name: python-project
description: Use when creating a Python project, installing packages, adding dependencies, running Python code, or encountering import/module errors
---

# Python 프로젝트 환경 관리 규칙

## 1. 프로젝트 시작 시

### 순서
1. **가상환경 생성 (3.12 버전 명시)**
   - Windows: `py -3.12 -m venv .venv`
   - macOS/Linux: `python3.12 -m venv .venv`
2. **가상환경 활성화 확인** — 아래 활성화 확인 절차 반드시 수행
3. **기본 파일 생성**: `.gitignore`, `requirements.txt`, `.env.example`, `README.md`

### 기본 폴더 구조
```
project/
├── .venv/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

---

## 2. 가상환경 활성화 확인 (매번 필수)

패키지 설치 또는 코드 실행 전 **반드시** 아래 순서로 확인:

```bash
# Step 1: 활성화
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Step 2: 활성화 여부 확인 (프롬프트에 (.venv) 표시 확인)
# Windows
where python        # → .venv 경로가 나와야 함
# macOS/Linux
which python        # → .venv 경로가 나와야 함

# Step 3: 확인 안 되면 활성화 재시도
```

> 활성화 없이 패키지를 설치하면 전역 환경에 설치됨 → 절대 금지

---

## 3. 패키지 설치 시 (매번 필수)

패키지를 설치할 때마다 아래 두 단계를 반드시 함께 실행:

```bash
# Step 1: 설치
pip install 패키지명

# Step 2: requirements.txt 즉시 갱신 (설치 후 반드시)
pip freeze > requirements.txt
```

> pip install 후 requirements.txt 갱신을 빠뜨리면
> 다른 환경에서 실행 시 ModuleNotFoundError 발생

---

## 4. 코드 실행 전 체크리스트

실행 전 아래 순서로 확인:

```
□ 가상환경 활성화 여부 확인 (which python / where python)
□ requirements.txt 기준 패키지 설치 여부 확인
  → pip install -r requirements.txt
□ .env 파일 존재 여부 확인
□ 필요한 API 키가 .env에 있는지 확인
```

---

## 5. import 에러 / ModuleNotFoundError 발생 시

추측으로 코드 수정하지 말고 아래 순서대로 진단:

```bash
# 1. 가상환경 활성화 여부 먼저 확인
which python  # .venv 경로인지 확인

# 2. 패키지 설치 여부 확인
pip show 패키지명

# 3. 미설치 확인 시
pip install 패키지명
pip freeze > requirements.txt  # 갱신 필수
```

---

## 주의사항
- `.env`는 절대 git에 올리지 않음 (`.gitignore`에 반드시 포함)
- `.venv` 폴더는 프로젝트 루트에 생성
- 패키지 설치는 항상 가상환경 활성화 후 진행
