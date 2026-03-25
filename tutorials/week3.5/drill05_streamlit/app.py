import streamlit as st
import sys
import os

st.set_page_config(page_title="Week 3.5 Streamlit 실습", page_icon="🚀")

st.title("🚀 Week 3.5 — Streamlit 실습")
st.success("streamlit run app.py 실행 성공!")

st.markdown("---")

st.subheader("현재 실행 환경 정보")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Python 경로**")
    st.code(sys.executable)

with col2:
    st.markdown("**실행 위치**")
    st.code(os.getcwd())

st.markdown("---")

st.subheader("오늘 배운 것")
st.markdown("""
| 명령어 | 역할 |
|--------|------|
| `cd 폴더` | 폴더 이동 |
| `ls` | 현재 폴더 내용 보기 |
| `pwd` | 현재 위치 확인 |
| `python -m venv venv` | 가상환경 생성 |
| `source venv/bin/activate` | 가상환경 활성화 (Mac/Linux) |
| `.\\venv\\Scripts\\activate` | 가상환경 활성화 (Windows) |
| `pip install -r requirements.txt` | 패키지 설치 |
| `streamlit run app.py` | Streamlit 앱 실행 |
| `deactivate` | 가상환경 비활성화 |
""")

st.markdown("---")
st.caption("왼쪽 사이드바에서 다른 페이지도 확인해보세요 👈")
