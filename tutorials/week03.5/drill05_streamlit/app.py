import streamlit as st
import sys
import os

st.set_page_config(page_title="Week 03.5 Streamlit 실습", page_icon="🚀")

st.title("🚀 Week 03.5 — Streamlit 실습")
st.success("streamlit run app.py 실행 성공!")

st.markdown("---")
st.subheader("현재 실행 환경")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Python 경로**")
    st.code(sys.executable)
with col2:
    st.markdown("**실행 위치**")
    st.code(os.getcwd())

st.markdown("---")
st.subheader("Week 03.5 핵심 명령어")
st.markdown("""
| 명령어 | 역할 |
|--------|------|
| `pwd` | 현재 위치 확인 |
| `ls` | 폴더 내용 보기 |
| `cd 폴더` | 폴더 이동 |
| `python 파일.py` | Python 파일 실행 |
| `pip install 패키지` | 패키지 전역 설치 |
| `streamlit run app.py` | Streamlit 앱 실행 |
""")

st.info("왼쪽 사이드바에서 다른 페이지도 확인해보세요 👈")
