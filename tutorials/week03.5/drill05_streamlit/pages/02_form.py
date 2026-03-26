import streamlit as st

st.title("📝 페이지 2 — 폼")
st.info("이 파일은 pages/02_form.py 입니다.")

st.markdown("---")

with st.form("intro_form"):
    name = st.text_input("이름")
    week = st.selectbox("현재 수강 주차", ["1주차", "2주차", "3주차", "3.5주차", "4주차"])
    feeling = st.slider("터미널 친숙도 (1=생소함, 10=익숙함)", 1, 10, 5)
    submitted = st.form_submit_button("제출")

if submitted:
    st.success(f"안녕하세요, {name}님!")
    st.write(f"현재 {week} 수강 중이시군요.")
    if feeling >= 7:
        st.balloons()
        st.write("터미널이 많이 익숙해지셨네요! 🎉")
    else:
        st.write("조금만 더 연습하면 금방 익숙해집니다. 💪")
