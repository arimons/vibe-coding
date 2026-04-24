---
layout: default
title: 바이브 코딩 12주 커리큘럼
nav_order: 1
---

# 바이브 코딩 12주 커리큘럼

> 연구원을 위한 실용 프로그래밍 강의

---

## 📚 학습 자료 모음

### 🔧 환경 설정

| 자료 | 설명 |
|------|------|
| [Antigravity 세팅 가이드](antigravity-setup) | Rules · Skills · MCP 설치 (수업 전 필수) |

> Git · Python · Node.js · Antigravity 설치 가이드는 별도 제공 예정

### 📖 기초 가이드

| 자료 | 설명 |
|------|------|
| [용어 사전](glossary) | 프론트엔드/백엔드/API 등 필수 개념 정리 |
| [Git 가이드](git-guide) | 버전 관리 기초 + 문제 상황 해결 |
| [CLI 기초 가이드](cli-guide) | 터미널 명령어 기초 |
| [Markdown 기초 가이드](markdown-guide) | 문서 작성 기초 |
| [프론트엔드 & 백엔드 기초개념](frontend-backend) | 웹 구조 이해 |
| [Streamlit 가이드](streamlit) | Streamlit 레퍼런스 |
| [Antigravity 가이드](antigravity-guide) | Antigravity 사용 가이드 |
| [Antigravity 심화](antigravity-advanced) | Rules · Skills 심화 설정 |

### 🗂️ 주차별 실습 자료

| 자료 | 설명 |
|------|------|
| [Week 2 실습](week02-practice) | CLI 기초 실습 파일 |
| [Week 3 실습](week03-gui) | Streamlit GUI 실습 |
| [Week 03.5 터미널 실습](week03.5) | 터미널 기초 보충 세션 |
| [Week 4 실습](week04-pandas) | 데이터 변환·분석 (pandas + 시각화) |
| [Week 5 실습](week05-llm-pipeline) | LLM 문서 처리 파이프라인 |
| [Week 6 실습](week06-structured-output) | Structured Output + 데이터 구조화 |
| [Week 7 실습](week07_web_scraping) | 웹 스크래핑 + LLM 코드 자동 생성 |

### 🚀 개인 프로젝트 (Week 9~12)

| 자료 | 설명 |
|------|------|
| [Week 9 사양설계서](week09-project-spec) | 프로젝트 시작 전 문제 정의 + 입출력 설계 템플릿 |

---

## 📋 강의 개요

### **목표**
반복 작업 자동화 도구를 직접 만들 수 있는 연구원

### **기간**
12주 (주 1회, 90분)

### **구조**
- 1주: 쇼케이스 (AI 도구로 무엇이 가능한지 체험)
- 2주: 개발 환경 + CLI 기초
- 3-7주: 데이터 실습 (Streamlit / Excel / LLM API / 웹 스크래핑)
- 8주: 프로젝트 기획 + 기술스택 이해
- 9-12주: 개인 프로젝트 개발

### **핵심 철학**
- 코드 직접 작성 ❌
- AI에게 질문하는 법 ✅
- 개념 이해 + 도구 활용 ✅

---

## 📅 주차별 커리큘럼

### **Week 1: 쇼케이스 — AI로 무엇이 가능한가**

📖 참고 자료: [Antigravity 가이드](antigravity-guide)

> 이번 주 목표: "이 수준까지 된다"는 것을 눈으로 확인한다. 실습보다 임팩트 중심.

#### 사전 준비 (수강생 숙제)
- Python 설치
- Antigravity 설치 + 로그인

#### 강의 흐름

**1. IDE 발전사 소개 (20분)**
- 메모장 → IDE → VS Code 계열의 흐름
- VS Code / Cursor / Antigravity 비교
- "AI가 코드를 대신 짜주는 시대"로 이어지는 맥락 설명

**2. Stitch로 UI 스케치 (20분)** ← 유일한 수강생 직접 체험
- 내가 만들고 싶은 앱의 입력창/버튼/출력 화면 스케치
- 결과 이미지 저장 (다음 단계에서 활용)

**3. MVP 시연 (40분)** ← 강사 시연
- 미리 준비한 boilerplate 불러오기
- Stitch 이미지 + boilerplate → Antigravity로 MVP 구현 과정 시연
- Antigravity Rules/Skills 설정 간단 안내
- "여기까지 오늘 보여드린 겁니다" 마무리

#### 과제
용어 사전 읽고 모르는 단어 별표 표시 (다음 주 Q&A)

---

### **Week 2: 개발 환경 이해 + CLI 기초**

📖 참고 자료: [용어 사전](glossary) · [Git 초보자 가이드](git-guide) · [CLI 기초 가이드](cli-guide) · [Week 2 실습](week02-practice)

#### 주제
- 용어 사전 Q&A: Week 1 숙제 리뷰 (모르는 단어 함께 정리)
- Git은 왜 쓰는가: 저장 + 되돌리기 + 협업 (개념만)
- CLI가 필요한 이유: 프로그램을 직접 실행하려면
- 필수 명령어: `pwd`, `cd`, `ls`, `mkdir`, `cp`, `mv`
- 와일드카드와 Tab 자동완성
- 가상환경 개념 (설명만, 실습은 Week 3 이후)

#### 시연 (30분)
1. Week 1 MVP — 실제로 어떻게 실행되는가 (터미널 기준)
2. 터미널로 폴더 이동 → 파일 확인 → 스크립트 실행 흐름
3. AI가 만든 스크립트 실행 시연

#### 실습 (50분)
- 실습 파일로 퀴즈 미션 수행 (backup 폴더 만들기, 파일 복사/이름 변경)
- AI에게 파일 정리 스크립트 요청 → 터미널에서 실행
- 에러 발생 시 AI에게 재질문하는 흐름 연습

#### 과제
본인 폴더에서 파일 정리 스크립트 1개 만들어보기

---

### **Week 3: Streamlit GUI — CLI에서 브라우저로**

📖 참고 자료: [Antigravity 환경 세팅 가이드](antigravity-setup) · [Week 3 실습](week03-gui)

> 핵심 철학: Streamlit 문법을 배우는 게 아니라, AI한테 시켜서 앱을 뚝딱 만드는 경험

#### 주제
- CLI vs GUI: 같은 작업, 다른 경험 — 언제 어느 쪽이 유리한가
- 가상환경 실습: 생성 → 활성화 → 패키지 설치 (`streamlit`, `pandas`, `plotly`, `pillow`)
- Streamlit 실행 한 줄: `streamlit run app.py`
- AI 프롬프트 패턴: 도구 탐색 → 기본 구현 → 기능 추가 반복

#### 시연 (20분)
1. Week 2 워터마크 스크립트 — CLI 1줄 vs Streamlit 브라우저 앱 비교
2. "어떤 패키지를 써야 하나요?" AI에게 물어보는 흐름 시연
3. 기본 앱 → 기능 추가 요청 → 재실행 루프 시연

#### 실습 (60분)
- **Phase 1**: 워터마크 GUI — 이미지 업로드 → 워터마크 → 다운로드 (CLI 경험 연결)
- **Phase 2**: 실험 데이터 뷰어 — CSV 업로드 → 이상값 자동 감지 → plotly 시각화
- **Phase 3**: LLM 연동 맛보기 — Gemini API로 데이터 분석 + 보고 초안 생성

#### 과제
본인 업무 데이터(CSV, 이미지 등) 1개로 간단한 Streamlit 앱 만들어보기

---

### **Week 03.5: 터미널 기초 실습** ← 보충 세션

📖 참고 자료: [터미널 기초 실습](week03.5)

> 3주차 실습 중 터미널/가상환경 개념이 필요해 별도로 편성된 보충 세션입니다.

#### 주제
- IDE(File View)와 터미널 실행 위치는 별개라는 개념 체득
- `ls`, `cd`, `pwd`로 폴더 구조 자유롭게 탐색
- `python 파일명.py` 직접 실행
- 실행 위치에 따라 import 에러가 나는 경험 (지도 읽기)
- 가상환경 생성 → 활성화 → 패키지 설치 → 비활성화 전체 흐름
- `streamlit run app.py`와 일반 `python` 실행의 차이

#### 실습 드릴
- **Drill 01**: `ls`, `cd`, `pwd`로 숨겨진 파일 찾기
- **Drill 02**: 패키지 없는 Python 파일 3개 직접 실행
- **Drill 03**: 잘못된 위치에서 실행 → 에러 → 올바른 위치 파악
- **Drill 04**: venv 생성/activate/deactivate + `rich` 패키지 설치
- **Drill 05**: venv + `streamlit run` 종합 실전

---

### **Week 4: 데이터 변환·분석 — pandas + Streamlit**

📖 참고 자료: [Week 4 실습](week04-pandas)

> 두 가지 앱으로 실습합니다.
> **Part 1** — 측정 소프트웨어 양식 → R/SPSS 입력 양식 변환기 (`app.py`)
> **Part 2** — 장비 Raw Data → 취합 → 통계 → 시각화 분석 파이프라인 (`app_analysis.py`)

#### 주제
- pandas 핵심 기능 체험 (읽기 / 정제 / 변환 / 집계 / 포맷 변환)
- 정규식(regex)으로 피험자 정보 분리
- 멀티시트 Excel 취합 → Tidy Data 변환
- Z-score 표준화 + Violin Plot 시각화
- Streamlit GUI로 변환·분석 규칙을 직접 조작하면서 결과 확인

#### 시연 (20분)
1. sample_raw.csv 열어서 문제점 파악 → app.py로 변환 시연
2. 장비 Raw Data(cholesterol, fatty acid) → app_analysis.py로 취합·시각화 시연

#### 실습 (60분)
- **Part 1 — 변환기** (`streamlit run app.py`)
  - Phase 1: 파일 업로드 → 구조 파악 (열 타입, 결측값 확인)
  - Phase 2: 열 이름 변경 + 순서 재배치
  - Phase 3: 정규식으로 단위 제거, 피험자 정보 분리
  - Phase 4: 코딩 변환 매핑 (텍스트 → 숫자)
  - Phase 5: Wide → Long 포맷 변환
  - Phase 6: CSV / Excel 다운로드
- **Part 2 — 분석 파이프라인** (`streamlit run app_analysis.py`)
  - Step 1: Raw Data 로드 + 여러 파일 합치기
  - Step 2: skiprows 설정, 정규식 분리, 멀티시트 취합
  - Step 3: Z-score 계산 + 이상치 확인
  - Step 4: Violin Plot / Box Plot / Paired Plot 시각화
  - Step 5: 멀티시트 Excel 저장

#### 과제
본인이 실제로 쓰는 Excel 파일을 업로드해서 AI에게 변환 기능 추가 요청해보기

---

### **Week 5: LLM 문서 처리 파이프라인**

📖 참고 자료: [Week 5 실습](week05-llm-pipeline)

> 이번 주 목표: "텍스트든 이미지든 문서를 LLM에 던지면 원하는 형태로 뽑아낼 수 있다"는 것을 체감한다.

> **사전 준비 (수강생 숙제):** poppler, pandoc 설치 — 매뉴얼 참고

#### Example 5 — 공개 논문 PDF → Markdown → 번역 → DOCX

##### 주제
- LLM API 기초: Gemini API 키 발급, 요청 구조, 비용 개념
- PDF/DOCX 텍스트 추출 (pdfplumber)
- Negative word 검출 시스템 (금지 성분·표현 자동 플래그)
- 논문/시험법 이미지 OCR → Markdown 변환
- Markdown → DOCX 변환 (pandoc)
- Streamlit UI로 전체 파이프라인 묶기

##### 시연 (60분)
1. Gemini API 키 발급 흐름 + 비용 계산 (페이지당 ~3원) — 8분
2. pdfplumber로 PDF 텍스트 추출 시연 — 10분
3. 추출 텍스트 → LLM → Negative word 검출 결과 시연 — 10분
4. 논문 PNG 이미지 → LLM OCR → Markdown 출력 시연 — 12분
5. Markdown → pandoc → DOCX 다운로드 시연 — 8분
6. Streamlit으로 전체 UI 통합 완성본 시연 — 12분

##### 실습 (30분)
- 본인 PDF 또는 논문 이미지 업로드 → 텍스트 추출 확인
- Negative word 목록 수정해서 재검출
- Markdown → DOCX 변환 결과 확인

##### 과제
본인 업무 문서(논문, 시험법 등) 대상으로 OCR → DOCX 파이프라인 1회 완성

---

### **Week 6: Structured Output — 문서에서 데이터 뽑기**

📖 참고 자료: [Week 6 실습](week06-structured-output)

> 이번 주 목표: LLM에게 "양식을 채워달라"고 시키는 법을 익힌다.
> 정규식이나 파싱 코드 없이, 원하는 구조의 데이터를 바로 얻어내는 경험.

#### 주제
- Structured Output 개념: 자유 텍스트 출력 vs 양식 출력
- JSON Schema 정의법 (모델명, 타입, 필수 필드)
- 원료 규격서 구조화 추출 실습
- 임상·안정성 시험 보고서 구조화 추출 실습
- 추출 결과 → pandas DataFrame → Excel 저장 (Week 4 연결)

#### 시연 (50분)
1. 개념 설명: 자유 출력 vs 구조화 출력 비교 시연 — 15분
2. JSON Schema 정의하는 법 — 10분
3. 원료 규격서 PDF → 구조화 추출 → DataFrame 시연 — 15분
4. 결과 Excel 저장 + 멀티 문서 배치 처리 시연 — 10분

#### 실습 (30분)
- 원료 규격서 또는 시험 보고서 1종 골라서 Schema 직접 정의
- LLM에게 추출 요청 → DataFrame 확인
- 필드 추가/수정하면서 출력 품질 개선

#### 과제
본인 업무에서 "정형화하고 싶은 문서" 1종 선정 → Schema 설계해보기

---

### **Week 7: 웹 스크래핑 — LLM으로 코드 자동 생성**

📖 참고 자료: [Week 7 실습](week07_web_scraping)

> 이번 주 목표: HTML selector를 몰라도 된다. URL만 주면 LLM이 스크래핑 코드를 짜준다.

#### 주제
- 웹 스크래핑 vs 크롤링 개념 구분
- HTML 최소 개념 (태그, class, id — F12 없이도 이해할 수 있는 수준)
- requests + BeautifulSoup 기초
- LLM 기반 스크래핑 코드 자동 생성 흐름
  - URL 입력 → HTML 수집 → LLM에 던지기 → 코드 초안 생성 → 실행 확인
- 수집 결과 → DataFrame → Excel 저장
- Streamlit UI로 감싸기

#### 시연 (60분)
1. 웹 스크래핑 vs 크롤링 개념 + HTML 구조 간단 설명 — 10분
2. 특허청(또는 PubMed) URL → HTML 수집 → LLM에 전달 시연 — 15분
3. LLM이 생성한 스크래핑 코드 실행 → 결과 확인 — 10분
4. 코드 안 될 때 LLM에 재질문하는 흐름 시연 — 10분
5. 결과 → DataFrame → Excel 저장 — 8분
6. Streamlit UI 통합 완성본 시연 — 7분

#### 실습 (30분)
- 본인이 정기적으로 확인하는 사이트 1개 선정
- URL 입력 → LLM 스크래핑 코드 생성 → 실행
- 결과 Excel 다운로드 확인

#### 과제
정기적으로 확인하는 사이트 1개 스크래퍼 + Streamlit 연결 완성

---

### **Week 8: 프로젝트 기획 + 기술스택 이해**

📖 참고 자료: [프론트엔드 & 백엔드 기초개념](frontend-backend)

#### 주제
- 개인 프로젝트 아이디어 발굴 + 워크시트 (입력 / 처리 / 출력)
- 기술스택 선택: Streamlit으로 충분한지 체크리스트
- 다음 단계 안내: React + FastAPI 구조 개념

#### 시연 (20분)
예시 프로젝트 기획 전 과정 시연 + Streamlit vs Frontend 비교

#### 실습 (60분)
- 본인 프로젝트 구체화 + 1:1 피드백
- 기술스택 선택 근거 작성

#### 과제
프로젝트 기획서 완성 + 개발 시작

---

### **Week 9~12: 개인 프로젝트**

📖 참고 자료: [Week 9 사양설계서](week09-project-spec)

> 이번 주 목표: PDF / Excel / 웹 스크래핑 중 1개 이상을 활용한 실무 자동화 도구를 완성한다.

| 주차 | 핵심 활동 | 산출물 |
|------|-----------|--------|
| Week 9 | 사양설계서 작성 + 실습 데이터 준비 + 강사 피드백 | 완성된 사양설계서 |
| Week 10 | MVP 구현 (핵심 기능 1개 작동) | 실행 가능한 MVP |
| Week 11 | 기능 고도화 + 엣지케이스 처리 + 동료 리뷰 | 완성본 |
| Week 12 | 최종 발표 (문제 → 해결 → 시연 → 회고) | 발표 자료 + GitHub |

---

## ⏱️ 주간 시간 배분

| 구간 | 시연 | 실습 | 비고 |
|------|------|------|------|
| Week 1 | 60분 | 20분 | 쇼케이스 중심 |
| Week 2 | 30분 | 50분 | 실습 드릴 중심 |
| Week 3 | 20분 | 60분 | 앱 제작 경험 중심 |
| Week 4 | 20분 | 60분 | pandas 실습 |
| Week 5 | 60분 | 30분 | 강사 데모 위주, 사전 설치 필수 |
| Week 6 | 50분 | 30분 | 개념 설명 ↔ 시연 교차 |
| Week 7 | 60분 | 30분 | LLM 코드 생성 데모 위주 |
| Week 8 | 20분 | 60분 | 1:1 피드백 중심 |
| Week 9~12 | — | 80분 | 멘토링 + 공유 10분 |

---

## 🎯 단계별 학습 목표

| 구간 | 목표 |
|------|------|
| Week 1 | AI 도구로 가능한 수준 체감 (쇼케이스) |
| Week 2 | 개발 환경 이해, 용어 정리, 터미널 기초 익히기 |
| Week 3 | CLI → GUI 전환 경험, Streamlit 앱 제작 |
| Week 4 | pandas/Excel 처리, 실용 변환·분석 도구 완성 |
| Week 5 | LLM API 첫 경험, 문서 처리 파이프라인 구축 |
| Week 6 | Structured Output으로 문서 → 데이터 구조화 |
| Week 7 | LLM 기반 웹 스크래핑 코드 자동 생성 |
| Week 8 | 프로젝트 기획 능력, 기술스택 선택 판단 |
| Week 9~12 | 실제 사용 가능한 도구 완성, 독립적 문제 해결 |

---

## 🎓 최종 결과물

1. **실제 사용 가능한 도구 1개** (Streamlit 웹앱 또는 CLI 스크립트)
2. **GitHub 저장소** (코드 + README + 실행 방법)
3. **발표 자료** (문제 정의 → 해결 방법 → 시연 → 배운 점)

---

## 💡 강의 원칙

**하지 않을 것:** 코드 문법 강의 ❌ · 알고리즘 풀이 ❌ · CS 이론 ❌

**할 것:** 개념 이해 ✅ · AI 질문법 ✅ · 에러 대응 ✅ · 실용 도구 만들기 ✅

---

## 🔄 후속 학습 경로

```
Level 1 (현재): Streamlit 기반 도구  →  연구원 대부분 여기서 충분
Level 2 (심화): React + FastAPI      →  더 전문적인 웹 서비스
Level 3 (전문): AI/ML · 데이터 사이언스 · DevOps
```

---

**문의 및 피드백: [연락처]**
