import streamlit as st
import pandas as pd
import io

# 페이지 설정
st.set_page_config(
    page_title="Pandas 데이터 변환기",
    page_icon="🧪",
    layout="wide"
)

# 제목
st.title("🧪 Pandas 데이터 변환기 (수정본)")
st.markdown("---")

# 사이드바에서 파일 업로드
st.sidebar.header("📂 파일 업로드")
uploaded_file = st.sidebar.file_uploader(
    "CSV 또는 Excel 파일을 선택하세요", 
    type=["csv", "xlsx", "xls"]
)

# 파일이 업로드되지 않았을 때 안내 메시지
if uploaded_file is None:
    st.info("👋 왼쪽 사이드바에서 분석할 파일을 업로드해주세요.")
    st.markdown("""
    ### 현재 제공되는 변환 기능:
    1. **피험자 정보 분리**: `Subject_Info` 열을 ID, 성명, 성별, 나이로 분리
    2. **단위 제거**: 측정값에서 숫자만 추출 (수분량, TEWL, 피지량 등)
    3. **값 매핑**: 텍스트(피부타입, 이상반응 등)를 숫자 코드로 변환
    4. **형식 변환**: 방문차수 숫자 추출, 날짜 형식 통일 등
    
    ### 테스트용 샘플 파일:
    - `data/sample_raw.csv` 파일을 사용해보세요.
    """)
else:
    try:
        # 파일 읽어서 세션 스테이트에 원본 저장
        if "df_original" not in st.session_state or st.session_state.get("file_name") != uploaded_file.name:
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file, encoding="utf-8-sig")
            else:
                df_raw = pd.read_excel(uploaded_file)
            st.session_state.df_original = df_raw
            st.session_state.file_name = uploaded_file.name
        
        df_original = st.session_state.df_original
        df_modified = df_original.copy()

        # --- 변환 옵션 섹션 ---
        st.subheader("🛠 데이터 변환 설정")
        
        # 4개의 컬럼으로 체크박스 배치
        trans_col1, trans_col2, trans_col3, trans_col4 = st.columns(4)
        
        with trans_col1:
            do_split = st.checkbox("1. 피험자 정보 분리", value=False)
            if do_split:
                st.caption("Subject_Info → 4개 열 분리")
                split_name1 = st.text_input("ID 열 이름", value="피험자번호")
                split_name2 = st.text_input("성명 열 이름", value="피험자명")
                split_name3 = st.text_input("성별 열 이름", value="성별")
                split_name4 = st.text_input("나이 열 이름", value="나이")

        with trans_col2:
            do_unit = st.checkbox("2. 측정값 단위 제거", value=False)
            if do_unit:
                st.caption("숫자만 추출 및 열 이름 변경")
                st.write("- 수분량_AU, TEWL_gm2h, 피지량_ugcm2")

        with trans_col3:
            do_mapping = st.checkbox("3. 값 매핑 (코드화)", value=False)
            if do_mapping:
                st.caption("피부타입(1～4), 이상반응(0～3)")

        with trans_col4:
            do_other = st.checkbox("4. 기타 형식 변환", value=False)
            if do_other:
                st.caption("방문차수(숫자), 날짜(YYYY-MM-DD), 연구원 명칭 변경")

        # --- 변환 로직 실행 (컬럼 순서 보존) ---
        # 1. Subject_Info 분리
        if do_split and "Subject_Info" in df_modified.columns:
            split_df = df_modified["Subject_Info"].str.extract(r'^([^_]+)_([^(]+)\(([MF])/(\d+)\)')
            split_df.columns = [split_name1, split_name2, split_name3, split_name4]
            split_df[split_name4] = pd.to_numeric(split_df[split_name4], errors="coerce")
            
            idx = df_modified.columns.get_loc("Subject_Info")
            df_modified = df_modified.drop(columns=["Subject_Info"])
            for i, col in enumerate(split_df.columns):
                df_modified.insert(idx + i, col, split_df[col])

        # 2. 단위 제거 (제자리 변환)
        if do_unit:
            unit_cols = {"moisture_val": "수분량_AU", "TEWL_val": "TEWL_gm2h", "sebum_val": "피지량_ugcm2"}
            for old_col, new_col in unit_cols.items():
                if old_col in df_modified.columns:
                    val = df_modified[old_col].str.extract(r'([\d.]+)').astype(float)
                    idx = df_modified.columns.get_loc(old_col)
                    df_modified = df_modified.drop(columns=[old_col])
                    df_modified.insert(idx, new_col, val)

        # 3. 값 매핑 (제자리 변환)
        if do_mapping:
            if "skin_type" in df_modified.columns:
                skin_map = {"건성": 1, "중성": 2, "지성": 3, "복합성": 4}
                idx = df_modified.columns.get_loc("skin_type")
                val = df_modified["skin_type"].map(skin_map)
                df_modified = df_modified.drop(columns=["skin_type"])
                df_modified.insert(idx, "피부타입", val)
            
            if "adverse_event" in df_modified.columns:
                event_map = {"없음": 0, "경미": 1, "중등도": 2, "중증": 3}
                idx = df_modified.columns.get_loc("adverse_event")
                val = df_modified["adverse_event"].map(event_map).fillna(0).astype(int)
                df_modified = df_modified.drop(columns=["adverse_event"])
                df_modified.insert(idx, "이상반응", val)

        # 4. 기타 변환
        if do_other:
            if "Visit" in df_modified.columns:
                idx = df_modified.columns.get_loc("Visit")
                val = df_modified["Visit"].str.extract(r'(\d+)').astype(int)
                df_modified = df_modified.drop(columns=["Visit"])
                df_modified.insert(idx, "방문차수", val)
            
            if "측정일" in df_modified.columns:
                df_modified["측정일"] = pd.to_datetime(df_modified["측정일"], format='mixed').dt.strftime('%Y-%m-%d')
            
            if "담당연구원" in df_modified.columns:
                df_modified = df_modified.rename(columns={"담당연구원": "연구원"})

        st.markdown("---")

        # --- 사이드바: 정보 및 다운로드 ---
        with st.sidebar:
            st.markdown("---")
            st.subheader("🔍 변환 후 데이터 정보")
            m1, m2 = st.columns(2)
            m1.metric("행 수", df_modified.shape[0])
            m2.metric("열 수", df_modified.shape[1])
            
            st.write("**최종 컬럼 목록:**")
            st.code(", ".join(df_modified.columns.tolist()))
            
            st.write("**열별 결측값:**")
            st.dataframe(df_modified.isnull().sum().reset_index().rename(columns={0: "결측치"}), 
                         use_container_width=True, hide_index=True)
            
            st.subheader("💾 수정본 저장")
            # 원본 파일명 기반으로 저장명 설정
            base_name = uploaded_file.name.rsplit('.', 1)[0]
            # 접미사 입력 받기
            suffix = st.text_input("파일명 접미사", value="수정본")
            save_name = f"{base_name}_{suffix}"
            
            st.caption(f"최종파일명: **{save_name}**")
            
            # Excel 익스포트
            output_excel = io.BytesIO()
            with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                df_modified.to_excel(writer, index=False, sheet_name='Sheet1')
            
            st.download_button(
                label="📥 Excel로 다운로드 (.xlsx)",
                data=output_excel.getvalue(),
                file_name=f"{save_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            # CSV 익스포트
            output_csv = df_modified.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="📥 CSV로 다운로드 (.csv)",
                data=output_csv,
                file_name=f"{save_name}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # --- 메인 영역: 미리보기 (나란히 보기) ---
        col_orig, col_mod = st.columns(2)
        
        with col_orig:
            st.subheader("📄 원본 데이터")
            st.dataframe(df_original, use_container_width=True)
            
        with col_mod:
            st.subheader("📝 변환 후 데이터")
            st.dataframe(df_modified, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 처리 중 오류 발생: {e}")
        st.exception(e)

# 푸터
st.markdown("---")
st.caption("Pandas Tutorial - Data Transformer App")
