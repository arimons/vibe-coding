---
name: streamlit-app
description: Use when creating or modifying a Streamlit web application
---

# Streamlit 앱 구조 규칙

## 기본 구조
```python
import streamlit as st

# 페이지 설정 (반드시 첫 번째 st 명령)
st.set_page_config(page_title="앱 이름", layout="wide")

# 사이드바: 설정/옵션
with st.sidebar:
    st.header("설정")
    ...

# 메인: 결과 표시
st.title("제목")
```

## 체크리스트
- [ ] `st.set_page_config`는 항상 첫 번째
- [ ] 파일 업로드는 `st.file_uploader` 사용
- [ ] 긴 작업은 `st.spinner`로 감싸기
- [ ] 에러는 `st.error()`, 성공은 `st.success()`
- [ ] 결과 다운로드는 `st.download_button` 제공

## 금지
- 전역 변수로 데이터 저장 금지 → `st.session_state` 사용
- `st.rerun()` 남발 금지
- `st.set_page_config` 중복 호출 금지
