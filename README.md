# 바이브 코딩 — 연구원을 위한 실용 프로그래밍

👉 **강의 교재 사이트**: https://arimons.github.io/vibe-coding

---

## 프로젝트 구조

```
vibe-coding/
│
├── docs/                          # GitHub Pages 교재 사이트 (Jekyll)
│   ├── _config.yml                # Jekyll 설정 (커스텀 레이아웃 적용)
│   ├── _layouts/
│   │   └── default.html           # 사이드바 + 본문 레이아웃
│   ├── assets/
│   │   └── css/
│   │       └── style.css          # Light Theme Blue 디자인 시스템
│   │
│   ├── index.md                   # 메인 (12주 커리큘럼 개요)
│   │
│   ├── [환경 설정]
│   ├── antigravity-setup.md       # Antigravity 설치 및 Rules/Skills 세팅
│   ├── antigravity-guide.md       # Antigravity 사용 가이드
│   ├── antigravity-advanced.md    # Antigravity 심화
│   │
│   ├── [기초 가이드]
│   ├── glossary.md                # 용어 사전
│   ├── git-guide.md               # Git 초보자 가이드
│   ├── cli-guide.md               # CLI 기초 가이드
│   ├── markdown-guide.md          # Markdown 기초 가이드
│   ├── frontend-backend.md        # 프론트엔드 & 백엔드 기초 개념
│   │
│   └── [주차별 실습 가이드]
│       ├── week02-practice.md     # Week 2: CLI 실습
│       ├── week03-gui.md          # Week 3: Streamlit GUI 실습
│       ├── week3.5.md             # Week 3.5: 터미널 기초 보충 세션
│       └── streamlit.md           # Streamlit 레퍼런스
│
├── tutorials/                     # 주차별 실습 파일
│   ├── week02-cli/
│   │   └── practice/              # Week 2 CLI 실습 파일
│   │
│   ├── week03-gui/
│   │   └── data/                  # Week 3 실습용 샘플 CSV 데이터
│   │
│   └── week3.5/                   # Week 3.5 터미널 기초 드릴
│       ├── drill01_navigation/    # ls, cd, pwd 탐색 훈련
│       │   └── chapter1/deeper/secret.py
│       ├── drill02_plain_run/     # python 파일명.py 직접 실행
│       │   ├── hello.py
│       │   ├── calculator.py
│       │   └── quiz.py
│       ├── drill03_module/        # 실행 위치 & import 에러 체험
│       │   ├── main.py
│       │   ├── utils/helper.py
│       │   └── data/sample.txt
│       ├── drill04_venv/          # 가상환경 생성/활성화/비활성화
│       │   ├── requirements.txt   # rich
│       │   └── app.py
│       └── drill05_streamlit/     # venv + streamlit run 종합 실전
│           ├── requirements.txt   # streamlit
│           ├── app.py
│           └── pages/
│               ├── 01_chart.py
│               └── 02_form.py
│
└── antigravity-config/            # Antigravity IDE Rules & Skills 설정
```

---

## GitHub Pages

- **URL**: https://arimons.github.io/vibe-coding
- **소스**: `main` 브랜치 `/docs` 폴더
- **설정**: Settings → Pages → Branch: `main` / `/docs` → Save
- **테마**: 커스텀 레이아웃 (Light Theme Blue) — `docs/_layouts/default.html`

push 후 1~2분이면 자동 빌드됩니다.

---

## 커리큘럼 요약

| 주차 | 주제 |
|------|------|
| Week 1 | 쇼케이스 — AI로 무엇이 가능한가 |
| Week 2 | 개발 환경 이해 + CLI 기초 |
| Week 3 | Streamlit GUI — CLI에서 브라우저로 |
| **Week 3.5** | **터미널 기초 보충 세션 (드릴 01~05)** |
| Week 4 | Excel 처리 (pandas) |
| Week 5 | PDF 처리 + LLM API 입문 |
| Week 6 | 크롤링 |
| Week 7 | LLM API 심화 |
| Week 8 | 프로젝트 기획 + 기술스택 이해 |
| Week 9–12 | 개인 프로젝트 |
