---
name: llm-model-advisor
description: >
  다음 상황에서 무조건 이 스킬을 사용해야 한다(ALWAYS trigger):
  (1) AI API 라이브러리 관련 코드 작성 — google-generativeai, openai, anthropic
  패키지 사용, Gemini/ChatGPT/Claude API 연동 코드, AI 챗봇 구현 요청;
  (2) AI 모델 선택/추천/비교 — "어떤 모델 써야 해?", "모델 추천해줘", "LLM 추천",
  "Gemini vs ChatGPT", "어떤 게 나아?", "빠르고 저렴한 모델", "비용 최소화";
  (3) 기존 코드의 모델 ID 검증 — "이 모델 맞아?", "최신 버전 아니야?",
  gemini-1.5-flash, gpt-3.5-turbo, claude-2, claude-3 같은 구버전 ID 발견 시;
  (4) AI 제공사 키워드 — Gemini, 제미나이, ChatGPT, GPT, 챗지피티, OpenAI,
  오픈AI, Claude, 클로드, Anthropic, 앤트로픽.
  Claude의 훈련 데이터에는 구버전 모델이 각인돼 있어 절대 기억에 의존해선 안 되고
  항상 WebSearch로 최신 모델을 먼저 확인해야 한다.
---

# LLM Model Advisor

## 목적

AI 훈련 데이터는 빠르게 구식이 된다. 이 스킬이 트리거되면 **반드시 WebSearch를 먼저
실행**하여 현재 사용 가능한 최신 모델을 확인한 뒤 추천한다.

> ⚠️ WebSearch 없이 기억에 의존해서 모델명을 추천하는 것은 이 스킬의 목적에 정면으로 반한다.

**지원 제공사**: Google(Gemini), OpenAI(GPT/o-시리즈), Anthropic(Claude) — 3사만

---

## 워크플로우

### 1단계: 제공사 감지

| 코드/언급 키워드 | 제공사 |
|-----------------|--------|
| Gemini, 제미나이, google-generativeai, genai | Google |
| GPT, ChatGPT, 챗지피티, openai, gpt-4, gpt-3 | OpenAI |
| Claude, 클로드, anthropic, claude-3 | Anthropic |

### 2단계: WebSearch 실행 (필수, 스킵 불가)

```
# Google
site:ai.google.dev/gemini-api/docs/models  OR  "Gemini API latest models 2026"

# OpenAI
site:platform.openai.com/docs/models  OR  "OpenAI latest models 2026"

# Anthropic
site:docs.anthropic.com/models  OR  "Anthropic Claude latest models 2026"
```

확인할 항목:
- 현재 production 사용 가능한 정확한 모델 ID 문자열
- deprecated 또는 곧 종료될 모델 목록
- 모델별 특성 (속도, 비용, context 크기)

### 3단계: 브리핑 — 최신 라인업 제시

검색 결과를 바탕으로 다음 표 형식으로 제시:

```
[제공사] 현재 사용 가능한 모델 (검색일: YYYY-MM-DD)

용도         | 모델 ID                  | 특징
-------------|--------------------------|------
범용/균형     | <exact-model-id>         | ...
빠름/저렴    | <exact-model-id>         | ...
고성능       | <exact-model-id>         | ...
추론/코딩    | <exact-model-id>         | ...
```

### 4단계: 추천 및 사용자 승인

사용자 작업 맥락에 맞는 Best Pick을 제안하고, 반드시 확인을 받는다:

> "위 모델 중 [추천 모델 ID]로 진행할까요?"

### 5단계: 코드 적용

승인된 모델의 정확한 ID를 코드에 사용. 구버전 감지 시:
1. 어느 모델이 구버전인지 명시
2. 검색 결과 기반 최신 대체 모델 제안
3. 변경된 코드 스니펫 제공

---

## 주의사항

- 모델 ID는 대소문자·하이픈까지 정확하게 (API 호출 실패 방지)
- Preview/Experimental 모델은 production 사용 비적합임을 고지
- 비용 차이가 클 경우 반드시 가격 tier 언급
- 지역 제한이나 waitlist 있는 모델은 availability 확인 후 안내
