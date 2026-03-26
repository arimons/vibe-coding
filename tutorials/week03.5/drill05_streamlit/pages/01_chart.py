import streamlit as st
import random
import pandas as pd

st.title("📊 페이지 1 — 차트")
st.info("이 파일은 pages/01_chart.py 입니다.")
st.markdown("`pages/` 폴더 안의 파일은 사이드바 메뉴로 자동 등록됩니다.")

st.markdown("---")

data = {"월": ["1월", "2월", "3월", "4월", "5월"],
        "값": [random.randint(10, 100) for _ in range(5)]}
df = pd.DataFrame(data)
st.bar_chart(df.set_index("월"))
st.caption("새로고침하면 값이 바뀝니다 (random)")
