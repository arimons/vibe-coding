---
name: python-project
description: Use when starting a new Python project or setting up a new workspace for the first time
---

# Python 프로젝트 시작 절차

## 순서
1. **프로젝트 폴더 구조 생성**
2. **가상환경 생성 (3.12 버전 명시)**
   - **Windows:** `py -3.12 -m venv .venv`
   - **macOS/Linux:** `python3.12 -m venv .venv`
3. **가상환경 활성화**
   - **Windows:** `.\.venv\Scripts\activate`
   - **macOS/Linux:** `source .venv/bin/activate`
4. **`.gitignore` 생성** (`.venv/`, `__pycache__/`, `.env`, `.DS_Store` 포함)
5. **`requirements.txt` 생성** (빈 파일로 시작하거나 기본 의존성 추가)
6. **`.env.example` 생성** (API 키 구조만 작성, 실제 값은 제외)
7. **`README.md` 생성** (프로젝트 목적, 파이썬 버전 3.12 명시, 실행 방법)
## 기본 폴더 구조
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

## 주의
- `.env`는 절대 git에 올리지 않음 (.gitignore에 반드시 포함)
- 패키지 설치 후 반드시 `pip freeze > requirements.txt` 실행
- `.venv` 폴더는 프로젝트 루트에 생성
