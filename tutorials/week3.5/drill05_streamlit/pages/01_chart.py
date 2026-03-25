import streamlit as st
import random

st.title("📊 페이지 1 — 차트")
st.info("이 파일은 pages/01_chart.py 입니다.")
st.markdown("Streamlit은 `pages/` 폴더를 자동으로 인식해서 사이드바 메뉴로 만들어 줍니다.")

st.markdown("---")

import pandas as pd

data = {
    "월": ["1월", "2월", "3월", "4월", "5월"],
    "값": [random.randint(10, 100) for _ in range(5)]
}

df = pd.DataFrame(data)
st.bar_chart(df.set_index("월"))
st.caption("새로고침하면 값이 바뀝니다 (random 사용)")
