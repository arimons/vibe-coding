---
name: context7-usage
description: Use when the user mentions LLM, AI API, Gemini, OpenAI, Claude API, 모델 연동, AI 연동, API 연동, or any external library integration. Triggers on keywords like: LLM, Gemini, OpenAI, Claude, AI 분석, AI 버튼, 모델명, API 키, google-generativeai, openai, anthropic, streamlit+AI, 최신 모델
---
# Context7 사용 규칙
## 반드시 조회 (Context7 필수)
### LLM / AI API 관련 — 최우선 적용
- Gemini, OpenAI, Claude, Anthropic 등 LLM API 코드 작성 시
- 모델명을 코드에 명시할 때 (예: `model="..."`)
- LLM 클라이언트 초기화 시 (예: `genai.GenerativeModel`, `openai.Client`)
- 임베딩, 멀티모달, 파일 업로드 등 API 기능 사용 시
- → **모델명·클래스명·메서드명은 학습 데이터 기준으로 틀릴 수 있음. 반드시 최신 문서 확인**

### ❗ LLM 모델명 기준 (Context7 조회 전 참고용 — 반드시 조회로 최종 확인)
> AI 모델은 수시로 업데이트됩니다. 아래는 이 Skill 작성 시점 기준이며,
> **실제 코드 작성 전 반드시 Context7로 최신 모델명을 재확인하세요.**
> 아래 모델명이 조회 결과와 다르면 조회 결과를 우선합니다.

| 제공사 | 권장 모델 (현재 기준) | 피해야 할 구버전 예시 |
|--------|----------------------|----------------------|
| Google Gemini | `gemini-3.1-pro-preview` | `gemini-1.5-flash`, `gemini-2.0-*`, `gemini-3-pro-preview` |
| OpenAI | Context7로 확인 | `gpt-3.5-*`, 오래된 preview 버전 |
| Anthropic | Context7로 확인 | 구버전 claude-2, claude-instant |

- 모델명을 **기억에 의존해 임의로 작성하지 말 것** — 반드시 Context7 문서 기반으로 작성
- `-latest` 같은 alias는 언제든 가리키는 모델이 바뀔 수 있으므로 명시적 모델명 사용 권장

### ❗ 검색(Query) 작성 원칙 (매우 중요)
1. **선입견 배제**: Context7에 `query`를 던질 때, 당신의 과거 학습 데이터에 있는 특정 버전이나 모델명(예: "Gemini 2.0")을 검색어에 미리 포함하지 마세요.
2. **최신 정보 탐색**: "What is the latest model and how to use it?" 처럼 중립적이고 범용적인 질문을 던져서, Context7이 문서 기반으로 실제 최신 모델과 버전을 알려주도록 유도하세요.

### 외부 라이브러리 일반
- 이 프로젝트에서 해당 라이브러리를 처음 사용할 때
- 라이브러리 버전이 바뀐 후 첫 작업 시
- 에러가 "deprecated" 또는 버전 관련일 때
- 공식 문서 URL이 없는 상태에서 API 스펙을 추측해야 할 때

## 조회 불필요 (Context7 생략)
- 이미 이 세션에서 검증된 패턴 반복 시
- 기본 Python / JS 문법 (조건문, 반복문, 함수 등)
- 이미 작동 중인 코드 패턴 재사용 시
- 표준 라이브러리 (os, json, datetime 등)

## 절차
1. Context7에서 해당 라이브러리 최신 문서 조회
2. 현재 설치 버전 확인 (`pip show 패키지명` 또는 `npm list 패키지명`)
3. 문서 기준 최신 모델명·클래스명·메서드명으로 코드 작성
4. 사용한 버전 및 모델명을 주석으로 명시

## 판단 기준
코드에 외부 서비스의 **고유 명사(모델명, 클래스명, 엔드포인트)** 가 들어간다면
→ Context7 조회 후 작성
