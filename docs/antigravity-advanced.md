---
layout: page
title: Antigravity 심화 가이드
nav_order: 7
---

# Antigravity 심화 가이드
## 멀티 에이전트 · 브라우저 디버깅 · Artifact 피드백

> 기본 가이드를 먼저 읽고 오세요 → [Antigravity IDE 가이드](antigravity-guide)

---

## 이 문서의 대상

기본 Agent 사용에 익숙해졌고, 더 빠르고 똑똑하게 쓰고 싶은 분.  
주로 **프로젝트 단계(Week 9~12)** 에서 유용합니다.

---

## 1. 멀티 에이전트 — 동시에 여러 일 시키기

### 개념

Agent Manager에서 에이전트를 여러 개 동시에 띄울 수 있습니다.  
각 에이전트는 **독립된 Workspace**에서 작동하며, 서로 다른 Task를 병렬로 처리합니다.  
완료되면 Inbox로 알림이 옵니다. 에이전트를 감시할 필요 없이 다른 작업을 하면 됩니다.

```
기존 방식 (순차):
Task A 완료 → Task B 시작 → Task C 시작

멀티 에이전트 (병렬):
Task A ─┐
Task B ─┼─ 동시 실행 → 각각 완료 시 Inbox 알림
Task C ─┘
```

### 실제 사용 사례

**사례 1 — 블로그 핫픽스 (Zeabur 개발팀)**  
메인 작업을 하면서 사이드 태스크(드롭다운 z-index 수정, CSS 버그 등)가 생길 때마다  
별도 에이전트에 던져두고 메인 작업에 집중.  
"이전에는 메모장에 나중에 할 일 목록을 적어뒀는데, 이제는 에이전트가 알아서 처리해주고 완료 알림을 준다."  
→ 출처: [Zeabur 블로그](https://zeabur.com/blogs/google-antigravity-agentic-ide-features)

**사례 2 — MVP 하루 만에 완성**  
한 개발자가 Secure File Sharing 앱 MVP를 멀티 에이전트로 몇 시간 만에 완성.  
혼자 개발했다면 며칠 걸렸을 작업.  
→ 출처: [ni18 블로그](https://blog.ni18.in/google-antigravity-ide-features-developer-should-know/)

**사례 3 — 라이브러리 전체 리팩토링 (DEV Community)**  
복잡한 리팩토링 시 에이전트가 먼저 단계별 계획을 세우고,  
여러 에이전트가 각 모듈을 병렬로 처리.  
"대규모 리팩토링을 훨씬 적은 수작업으로 끝낼 수 있었다."  
→ 출처: [DEV Community 후기](https://dev.to/this-is-learning/my-experience-with-google-antigravity-how-i-refactored-easy-kit-utils-with-ai-agents-2e54)

### 언제 쓰면 좋을까?

| 상황 | 활용법 |
|------|--------|
| 기능 개발 중 버그 발견 | 버그 수정을 별도 에이전트에 맡기고 개발 계속 |
| 서로 독립적인 기능 2~3개 동시 개발 | 각 기능을 다른 에이전트에 할당 |
| 반복적인 정리 작업 | 코드 정리 / 주석 번역 등을 백그라운드 에이전트에 위임 |

> ⚠️ **주의**: 같은 파일을 두 에이전트가 동시에 수정하면 충돌 가능. 독립적인 Task에만 사용하세요.

---

## 2. 내장 브라우저 — 눈으로 보면서 버그 수정

### 개념

Chrome 익스텐션을 설치하면 에이전트가 브라우저를 직접 조작합니다.  
코드 수정 → 실행 → 확인 → 버그 발견 → 재수정을 **에이전트가 혼자** 합니다.

```
브라우저 없을 때:
에이전트가 코드 작성 → 사용자가 직접 실행 → 버그 발견 → 에이전트에게 설명 → 수정

브라우저 있을 때:
에이전트가 코드 작성 → 직접 브라우저 실행 → 버그 발견 → 혼자 수정 → 스크린샷 첨부
```

### 에이전트가 브라우저로 할 수 있는 것

- 버튼 클릭, 폼 입력, 페이지 이동
- 스크린샷 자동 저장 (Artifact로 남김)
- 브라우저 세션 녹화 (영상으로 저장)
- 콘솔 오류 읽기
- DOM 구조 파악

### 실제 사용 사례

**사례 1 — 드롭다운 스타일 버그 (whatplugin.ai 리뷰어)**  
텍스트로 설명해도 에이전트가 못 고쳤던 스타일 버그를  
"브라우저 써서 직접 봐" 한 마디로 즉시 해결.  
"AI에게 시각적 피드백을 주는 게 텍스트 설명보다 훨씬 빠르고 정확했다."  
→ 출처: [whatplugin.ai 리뷰](https://newsletter.whatplugin.ai/p/i-tested-antigravity-googles-agentic-ide)

**사례 2 — 다크모드 토글 확인 (DataCamp 튜토리얼)**  
"설정 페이지에 다크모드 토글 추가해줘"  
→ 에이전트가 코드 작성 → localhost 실행 → 설정 페이지 이동 → 토글 클릭 → 스크린샷으로 확인까지 자동 완료.  
→ 출처: [DataCamp 튜토리얼](https://www.datacamp.com/tutorial/google-antigravity-tutorial)

**사례 3 — 라이브러리 문서 검증 (DEV Community)**  
코드 리팩토링 후 테스트 페이지를 에이전트가 직접 실행하고,  
유틸리티 함수들이 제대로 동작하는지 브라우저에서 확인.  
사람이 생각하지 못한 엣지 케이스도 발견.  
→ 출처: [DEV Community 후기](https://dev.to/this-is-learning/my-experience-with-google-antigravity-how-i-refactored-easy-kit-utils-with-ai-agents-2e54)

### 설치 방법

1. Antigravity에서 브라우저 기능 첫 실행 시 자동으로 안내
2. Chrome 웹 스토어에서 Antigravity 익스텐션 설치
3. 권한 허용 후 바로 사용 가능

> 📌 Streamlit 앱도 localhost에서 실행되므로 브라우저 연동으로 자동 테스트 가능합니다.

---

## 3. Artifact 피드백 — Google Docs처럼 코멘트

### 개념

에이전트가 만든 결과물(구현 계획, 스크린샷, Task 목록)에  
**특정 부분을 드래그해서 코멘트**를 달 수 있습니다.  
에이전트는 실행을 멈추지 않고, 다음 작업 시 코멘트를 반영합니다.

```
기존 방식:
에이전트 실행 중단 → 전체 다시 설명 → 처음부터 재시작

Artifact 피드백:
실행 중에 코멘트 → 에이전트가 다음 pass에서 반영 → 흐름 유지
```

### 실제 사용 사례

**구현 계획 수정**  
에이전트가 Yup으로 검증 로직을 짜려는 것을 발견 →  
구현 계획의 해당 부분을 드래그 → `"Yup 대신 Zod 써줘"` 코멘트  
→ 에이전트가 실행 중 반영, 재시작 없이 계속 진행.  
→ 출처: [index.dev 블로그](https://www.index.dev/blog/google-antigravity-agentic-ide)

**스크린샷에 코멘트**  
에이전트가 찍은 스크린샷의 특정 UI 영역을 드래그 →  
`"이 버튼 색깔이 디자인 스펙이랑 달라"` 코멘트  
→ 에이전트가 CSS 수정 후 재스크린샷.

### 활용 팁

- 전체를 다시 설명하기보다 **문제 있는 부분만** 드래그해서 짧게 코멘트
- 여러 곳에 동시에 코멘트 가능 → 에이전트가 한 번에 반영
- 코멘트 이력이 Artifact에 남아서 나중에 참고 가능

---

## 4. 멀티모달 — 이미지로 설명하기

### 개념

Gemini 3의 멀티모달 능력으로 **이미지를 그대로 붙여넣어** 요청할 수 있습니다.

### 활용법

```
텍스트로 설명하기 어려운 경우:
- Figma 디자인 스크린샷 → "이렇게 만들어줘"
- 에러 스크린샷 → "이 오류 고쳐줘"
- 참고 UI 사진 → "이 스타일로 바꿔줘"
```

**사례 — Figma 디자인 구현 (DEV Community)**  
디자인 목업 스크린샷을 붙여넣고 "이렇게 만들어줘"  
→ 에이전트가 이미지와 의도를 동시에 파악해서 CSS/JS 생성.  
→ 출처: [DEV Community 후기](https://dev.to/this-is-learning/my-experience-with-google-antigravity-how-i-refactored-easy-kit-utils-with-ai-agents-2e54)

---

## 📚 더 읽어볼 자료

| 자료 | 내용 |
|------|------|
| [Google 공식 블로그](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/) | 공식 기능 소개 |
| [Google Codelabs — 시작하기](https://codelabs.developers.google.com/getting-started-google-antigravity) | 실습형 튜토리얼 |
| [Google Codelabs — Skills 만들기](https://codelabs.developers.google.com/getting-started-with-antigravity-skills) | 커스텀 Skills 제작 |
| [DataCamp 튜토리얼](https://www.datacamp.com/tutorial/google-antigravity-tutorial) | 실제 프로젝트 빌드 과정 |
| [whatplugin.ai 리뷰](https://newsletter.whatplugin.ai/p/i-tested-antigravity-googles-agentic-ide) | 비개발자 관점 실사용 후기 |

---

**대상:** 바이브 코딩 수강생 (프로젝트 단계)
