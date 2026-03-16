---
name: context7-usage
description: Use when writing code that involves any external library, API integration, LLM model selection, or version-sensitive implementation
---
# Context7 사용 규칙
## 반드시 조회 (Context7 필수)
### LLM / AI API 관련 — 최우선 적용
- Gemini, OpenAI, Claude, Anthropic 등 LLM API 코드 작성 시
- 모델명을 코드에 명시할 때 (예: `model="..."`)
- LLM 클라이언트 초기화 시 (예: `genai.GenerativeModel`, `openai.Client`)
- 임베딩, 멀티모달, 파일 업로드 등 API 기능 사용 시
- → **모델명·클래스명·메서드명은 학습 데이터 기준으로 틀릴 수 있음. 반드시 최신 문서 확인**

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
