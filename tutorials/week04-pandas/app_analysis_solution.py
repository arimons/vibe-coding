import streamlit as st
import pandas as pd
import io
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 앱 레이아웃 설정
st.set_page_config(page_title="Excel Multi-File Processor", layout="wide")

# --- 세션 상태 초기화 ---
if 'master_df' not in st.session_state:
    st.session_state.master_df = pd.DataFrame()
if 'final_workbook' not in st.session_state:
    st.session_state.final_workbook = {}

st.title("📊 Excel 데이터 통합 및 통계 분석 도구")

# --- 사이드바: 모든 공통 설정 통합 ---
st.sidebar.header("⚙️ 데이터 공통 설정")
master_filename = st.sidebar.text_input("최종 통합 파일명", value="Combined_Master_Result")
skip_rows = st.sidebar.number_input("건너뛸 행 수 (skiprows)", min_value=0, value=0, step=1)
v1_label = st.sidebar.text_input("V1 (1) 라벨", value="섭취전")
v2_label = st.sidebar.text_input("V2 (2) 라벨", value="4주 섭취 후")

st.sidebar.divider()
uploaded_files = st.sidebar.file_uploader(
    "Excel 파일들을 업로드하세요.", 
    type=["xlsx", "xls"], 
    accept_multiple_files=True
)

# 사이드바: 병합 기준 열 설정 (파일 업로드 시 자동 추출)
sub_col, val_col = None, None
if uploaded_files:
    try:
        xls_temp = pd.ExcelFile(uploaded_files[0], engine='openpyxl')
        first_sheet = xls_temp.sheet_names[0]
        df_temp = pd.read_excel(uploaded_files[0], sheet_name=first_sheet, skiprows=skip_rows, nrows=1, engine='openpyxl')
        all_cols = df_temp.columns.tolist()
        
        st.sidebar.divider()
        st.sidebar.subheader("📌 병합 기준 열 설정 (전역)")
        sub_col = st.sidebar.selectbox("피험자 정보 열 (패턴 포함)", all_cols)
        val_col = st.sidebar.selectbox("측정값 추출 열", all_cols)
    except Exception as e:
        st.sidebar.error(f"컬럼 추출 오류: {e}")

if st.sidebar.button("🗑️ 전체 데이터 초기화"):
    st.session_state.master_df = pd.DataFrame()
    st.session_state.final_workbook = {}
    st.sidebar.success("초기화 완료")

# 탭 생성
tab1, tab2, tab3, tab4 = st.tabs(["📂 데이터 하나의 테이블 중심 병합", "📊 통계 요약", "📈 개인별 변화", "📉 성분 비교"])

# ==========================================
# Tab 1: 데이터 병합
# ==========================================
with tab1:
    st.header("📂 여러 파일의 데이터를 하나의 통합 데이터로 병합")
    st.info("파일의 시트를 시트별 분석하는 것이 아니라 **모든 파일과 모든 시트를 하나로 가로 병합 (Horizontal Merge)** 합니다.")
    
    if not uploaded_files:
        st.info("💡 왼쪽 사이드바에서 Excel 파일들을 먼저 업로드해 주세요.")
    else:
        for f_idx, file in enumerate(uploaded_files):
            with st.expander(f"📁 파일: {file.name}", expanded=True):
                try:
                    xls = pd.ExcelFile(file, engine='openpyxl')
                    s_names = xls.sheet_names
                    
                    st.write(f"시트 수: {len(s_names)} / 첫 시트 미리보기:")
                    df_p = pd.read_excel(file, sheet_name=s_names[0], skiprows=skip_rows, nrows=5, engine='openpyxl')
                    st.dataframe(df_p, use_container_width=True)

                    c_name, c_tot, c_btn = st.columns([2, 2, 1])
                    with c_name:
                        default_res_sheet = os.path.splitext(file.name)[0]
                        res_sheet_name = st.text_input("📂 파일 저장 시트 이름", value=default_res_sheet[:31], key=f"res_s_{f_idx}")
                    with c_tot:
                        # 합계 열 이름 지정 (파일 단위)
                        default_total = "FA_total" if "fatty" in file.name.lower() else ("Chol_total" if "chol" in file.name.lower() else "Total")
                        total_col_name = st.text_input(f"➕ 수치 합계(Total) 변수명", value=default_total, key=f"tot_n_{f_idx}")
                    with c_btn:
                        st.write(" ")
                        if st.button(f"🚀 병합 추가", key=f"btn_{f_idx}", use_container_width=True):
                            if not sub_col or not val_col:
                                st.error("사이드바에서 기준 열들을 먼저 선택해 주세요.")
                            else:
                                file_sheet_dfs = []
                                pr_s_names = []
                                for s_name in s_names:
                                    df = pd.read_excel(file, sheet_name=s_name, skiprows=skip_rows, engine='openpyxl')
                                    if sub_col in df.columns and val_col in df.columns:
                                        ext = df[sub_col].astype(str).str.extract(r'V(\d+)_S(\d+)')
                                        if ext.isna().all().all(): continue
                                        ext.columns = ["방문코드", "피험자번호"]
                                        ext["적용시점"] = ext["방문코드"].map({"1": v1_label, "2": v2_label}).fillna(ext["방문코드"])
                                        ext["피험자번호"] = pd.to_numeric(ext["피험자번호"], errors='coerce')
                                        res_t = pd.concat([ext[["적용시점", "피험자번호"]], df[[val_col]]], axis=1)
                                        # 컬럼명을 원본 시트 이름으로 변경
                                        res_t = res_t.rename(columns={val_col: s_name}).drop_duplicates(subset=["적용시점", "피험자번호"])
                                        file_sheet_dfs.append(res_t)
                                        pr_s_names.append(s_name)
                                        
                                if file_sheet_dfs:
                                    # 해당 파일 내부 시트들 병합
                                    merged_f = file_sheet_dfs[0]
                                    for next_f in file_sheet_dfs[1:]:
                                        merged_f = pd.merge(merged_f, next_f, on=["적용시점", "피험자번호"], how="outer")
                                    
                                    cats = [v1_label, v2_label]
                                    merged_f["적용시점"] = pd.Categorical(merged_f["적용시점"], categories=cats, ordered=True)
                                    merged_f = merged_f.sort_values(by=["적용시점", "피험자번호"]).reset_index(drop=True)
                                    
                                    # 콤마 제거 및 숫자 변환
                                    for pcol in pr_s_names:
                                        if merged_f[pcol].dtype == object or merged_f[pcol].dtype == str:
                                            merged_f[pcol] = merged_f[pcol].astype(str).str.replace(',', '', regex=False)
                                        merged_f[pcol] = pd.to_numeric(merged_f[pcol], errors='coerce')
                                        
                                    # 설정한 이름으로 파일 전체 (또는 단일 컬럼) 합계 계산
                                    merged_f[total_col_name] = merged_f[pr_s_names].sum(axis=1, skipna=True)
                                    
                                    # 1. 개별 단위: 이 파일의 결과만을 final_workbook에 개별 시트로 저장
                                    st.session_state.final_workbook[res_sheet_name] = merged_f.copy()
                                    
                                    # 2. 통합 단위: 마스터 데이터프레임과 병합 (시각화/다중 비교용)
                                    if st.session_state.master_df.empty:
                                        st.session_state.master_df = merged_f
                                    else:
                                        st.session_state.master_df = pd.merge(
                                            st.session_state.master_df, 
                                            merged_f, 
                                            on=["적용시점", "피험자번호"], 
                                            how="outer"
                                        )
                                        st.session_state.master_df["적용시점"] = pd.Categorical(st.session_state.master_df["적용시점"], categories=cats, ordered=True)
                                        st.session_state.master_df = st.session_state.master_df.sort_values(by=["적용시점", "피험자번호"]).reset_index(drop=True)

                                    st.success(f"✅ '{res_sheet_name}' 시트 추가 및 Master 병합 완료! (추가된 열: {len(pr_s_names)}개 + '{total_col_name}')")
                except Exception as e:
                    st.error(f"에러: {e}")

    if not st.session_state.master_df.empty:
        st.divider()
        st.header("📦 구축된 마스터 데이터 미리보기 및 다운로드")
        st.dataframe(st.session_state.master_df, use_container_width=True)
        
        out_buf = io.BytesIO()
        with pd.ExcelWriter(out_buf, engine="openpyxl") as writer:
            # 통합된 전체 데이터 (Master 시트)
            st.session_state.master_df.to_excel(writer, sheet_name="Master", index=False)
            
            # 각 파일별 개별 결과 시트들 추가
            for s_name, d_frame in st.session_state.final_workbook.items():
                safe_name = str(s_name)[:31] # 엑셀 시트 이름 길이 제한
                # 만약 Master와 이름이 우연히 겹치는 것을 대비 (보통은 안겹침)
                if safe_name.lower() == "master": safe_name += "_1"
                d_frame.to_excel(writer, sheet_name=safe_name, index=False)
        st.download_button(
            label=f"📥 {master_filename}.xlsx 다운로드", 
            data=out_buf.getvalue(), 
            file_name=f"{master_filename}.xlsx", 
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
            use_container_width=True
        )

# ==========================================
# 공통 데이터 로드 함수 (Tab 2 & Tab 3용)
# ==========================================
def get_analysis_source(tab_key):
    st.markdown("### 🗂️ 데이터 분석 소스 설정")
    source_type_tab = st.radio("분석할 데이터 형태", ["통합된 마스터 데이터 사용", "새로운 엑셀 파일 업로드"], horizontal=True, key=f"src_type_{tab_key}")
    
    if source_type_tab == "통합된 마스터 데이터 사용":
        if st.session_state.master_df.empty:
            st.warning("먼저 '데이터 병합' 탭에서 데이터를 추가해 주세요.")
            return None
        return st.session_state.master_df
    else:
        new_f_tab = st.file_uploader("분석용 엑셀 파일 업로드", type=["xlsx", "xls"], key=f"up_{tab_key}")
        if new_f_tab:
            xls_an_tab = pd.ExcelFile(new_f_tab, engine='openpyxl')
            an_s_tab = st.selectbox("분석할 시트 선택", xls_an_tab.sheet_names, key=f"an_s_{tab_key}")
            return pd.read_excel(new_f_tab, sheet_name=an_s_tab, engine='openpyxl')
        return None

# ==========================================
# Tab 2: 📊 통계 요약
# ==========================================
with tab2:
    st.header("📊 데이터 통계 분석 및 요약")
    analysis_source = get_analysis_source("tab2")
    
    if analysis_source is not None:
        st.divider()
        df_an = analysis_source.copy()
        all_cols_an = df_an.columns.tolist()
        
        c1, c2 = st.columns(2)
        with c1: v_col_an = st.selectbox("방문 구분 (Visit)", all_cols_an, index=0 if '적용시점' in all_cols_an else 0, key="stat_v")
        with c2: s_col_an = st.selectbox("피험자 식별 (Sample #)", all_cols_an, index=all_cols_an.index('피험자번호') if '피험자번호' in all_cols_an else 1, key="stat_s")
        
        num_cols = df_an.select_dtypes(include=[np.number]).columns.tolist()
        m_cols = [c for c in num_cols if c not in [v_col_an, s_col_an]]
        
        target_cols = st.multiselect("분석할 항목 모두 선택 (Total 포함)", m_cols, default=m_cols, key="stat_target")
        
        if target_cols:
            st.subheader("📋 시점별 기초 통계 요약")
            st.dataframe(df_an.groupby(v_col_an)[target_cols].agg(['mean', 'median', 'std']).T, use_container_width=True)

            st.subheader("🔄 피험자별 변화량 및 변화율 분석")
            vs_list = df_an[v_col_an].unique().tolist()
            if len(vs_list) >= 2:
                v_b, v_a = (v1_label if v1_label in vs_list else vs_list[0]), (v2_label if v2_label in vs_list else vs_list[1])
                res_delta = []
                for col in target_cols:
                    pivot = df_an[[s_col_an, v_col_an, col]].pivot(index=s_col_an, columns=v_col_an, values=col)
                    if v_b in pivot.columns and v_a in pivot.columns:
                        pivot['Delta'] = pivot[v_a] - pivot[v_b]
                        pivot['Rate(%)'] = (pivot[v_a] - pivot[v_b]) / pivot[v_b] * 100
                        res_delta.append({"측정항목": col, "변화량(평균)": pivot['Delta'].mean(), "변화량(중앙값)": pivot['Delta'].median(), "변화량(표준편차)": pivot['Delta'].std(), "변화율(평균 %)": pivot['Rate(%)'].mean()})
                st.dataframe(pd.DataFrame(res_delta).set_index("측정항목"), use_container_width=True)

# ==========================================
# Tab 3: 📈 개인별 변화
# ==========================================
with tab3:
    st.header("📈 피험자별 변화 추이 시각화")
    st.info("""
    **💡 그래프 이해하기 (2D 공간에 3개 변수 표현)**
    - **가로축(X)**: 실험 단계 (**방문 시점**)를 나타냅니다.
    - **세로축(Y)**: 선택하신 **측정 항목의 수치**를 나타냅니다.
    - **연결선(Line)**: 동일한 **피험자(번호)**의 전/후 데이터를 선으로 연결하여 개별 변화를 보여줍니다.
    """)
    st.divider()
    
    analysis_source = get_analysis_source("tab3")
    
    if analysis_source is not None:
        st.divider()
        df_viz = analysis_source.copy()
        all_cols_viz = df_viz.columns.tolist()
        
        st.subheader("🛠️ 시각화 설정")
        cv1, cv2, cv3 = st.columns(3)
        with cv1:
            v_col_v = st.selectbox("1️⃣ 방문 시점 열 (X축)", all_cols_viz, index=0 if '적용시점' in all_cols_viz else 0)
        with cv2:
            s_col_v = st.selectbox("2️⃣ 피험자 식별 열", all_cols_viz, index=all_cols_viz.index('피험자번호') if '피험자번호' in all_cols_viz else 1)
        with cv3:
            target_viz = st.selectbox("3️⃣ 시각화할 여러 항목 중 선택 (Y축)", [c for c in all_cols_viz if c not in [v_col_v, s_col_v]])

        if target_viz:
            df_viz[target_viz] = pd.to_numeric(df_viz[target_viz], errors='coerce')
            df_viz = df_viz.dropna(subset=[target_viz])
            
            v_min, v_max = df_viz[target_viz].min(), df_viz[target_viz].max()
            v_mean = df_viz[target_viz].mean()
            st.caption(f"📈 데이터 범위: 최소 {v_min:,.1f} ~ 최대 {v_max:,.1f} (평균 {v_mean:,.1f})")

            cats_v = [v1_label, v2_label]
            valid_cats = [c for c in cats_v if c in df_viz[v_col_v].unique()]
            if not valid_cats:
                valid_cats = df_viz[v_col_v].unique().tolist()
                
            df_viz[v_col_v] = pd.Categorical(df_viz[v_col_v], categories=valid_cats, ordered=True)
            df_viz = df_viz.sort_values([v_col_v, s_col_v])

            fig = go.Figure()

            for s_id in df_viz[s_col_v].unique():
                sub = df_viz[df_viz[s_col_v] == s_id]
                if len(sub) >= 2:
                    fig.add_trace(go.Scatter(x=sub[v_col_v], y=sub[target_viz], mode='lines+markers', line=dict(color='rgba(150, 150, 150, 0.4)', width=1.5), marker=dict(color='gray', size=6, opacity=0.5), name=f"피험자 {s_id}", showlegend=False, hoverinfo='skip'))
                else:
                    fig.add_trace(go.Scatter(x=sub[v_col_v], y=sub[target_viz], mode='markers', marker=dict(color='lightgray', size=6), name=f"피험자 {s_id} (단일)", showlegend=False, hoverinfo='skip'))

            mean_df = df_viz.groupby(v_col_v, observed=True)[target_viz].mean().reset_index()
            fig.add_trace(go.Scatter(
                x=mean_df[v_col_v], y=mean_df[target_viz], mode='lines+markers+text',
                text=[f"{v:,.1f}" for v in mean_df[target_viz]], textposition="top center",
                line=dict(color='royalblue', width=5), marker=dict(color='royalblue', size=14, symbol='diamond'),
                name='전체 평균 (Mean)', hovertemplate="전체 평균<br>시점: %{x}<br>평균값: %{y:,.2f}<extra></extra>"
            ))

            fig.update_layout(
                title=dict(text=f"<b>[{target_viz}]</b> 개인별 전/후 변화 추이", x=0.5, xanchor='center'),
                xaxis_title="방문 시점 (Visit Stage)",
                yaxis=dict(title=f"수치값", autorange=True, gridcolor='lightgray'),
                template="plotly_white", height=700, hovermode="x unified", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.7)")
            )
            
            st.plotly_chart(fig, use_container_width=True, key=f"plot_v_{target_viz}_{v_mean}")

# ==========================================
# Tab 4: 📉 성분 비교
# ==========================================
with tab4:
    st.header("📉 성분별 평균 변화율 비교")
    st.info("각 측정 성분의 **섭취 전 대비 섭취 후의 평균 변화율(%)**을 막대 그래프로 비교합니다.")
    st.divider()
    
    analysis_source = get_analysis_source("tab4")
    
    if analysis_source is not None:
        st.divider()
        df_comp = analysis_source.copy()
        all_cols_comp = df_comp.columns.tolist()
        
        st.subheader("🛠️ 시각화 설정")
        c1, c2 = st.columns(2)
        with c1:
            v_col_c = st.selectbox("1️⃣ 방문 시점 열 (분석 기준)", all_cols_comp, index=0 if '적용시점' in all_cols_comp else 0, key="v_col_c")
        with c2:
            s_col_c = st.selectbox("2️⃣ 피험자 식별 열", all_cols_comp, index=all_cols_comp.index('피험자번호') if '피험자번호' in all_cols_comp else 1, key="s_col_c")
            
        # 수치형 열 찾기 (단, 임의의 'total' 들어간 열은 기본적으로 제외 대상)
        num_cols = df_comp.select_dtypes(include=[np.number]).columns.tolist()
        candidate_cols = [c for c in num_cols if c not in [v_col_c, s_col_c] and 'total' not in str(c).lower()]
        
        target_cols = st.multiselect("📊 비교할 성분 항목 선택 (Total 제외됨)", num_cols, default=candidate_cols, key="target_comp")

        if target_cols:
            vs_list = df_comp[v_col_c].dropna().unique().tolist()
            if len(vs_list) >= 2:
                # 라벨을 기반으로 우선순위 결정, 없으면 고유값 중 첫 2개 사용
                v_b = v1_label if v1_label in vs_list else vs_list[0]
                v_a = v2_label if v2_label in vs_list else vs_list[1]
                
                mean_change_rates = []
                for t_col in target_cols:
                    df_comp[t_col] = pd.to_numeric(df_comp[t_col], errors='coerce')
                    mean_b = df_comp[df_comp[v_col_c] == v_b][t_col].mean()
                    mean_a = df_comp[df_comp[v_col_c] == v_a][t_col].mean()
                    
                    if pd.notna(mean_b) and mean_b != 0:
                        change_rate = (mean_a - mean_b) / mean_b * 100
                        mean_change_rates.append({
                            "성분명": str(t_col),
                            "변화율(%)": change_rate
                        })
                
                if mean_change_rates:
                    df_res = pd.DataFrame(mean_change_rates)
                    
                    # 변화율에 따른 색상 구분
                    df_res['Color'] = np.where(df_res['변화율(%)'] > 0, '#4169E1', '#CD5C5C') # 양수: RoyalBlue, 음수: IndianRed
                    
                    fig = px.bar(
                        df_res, 
                        x="성분명", 
                        y="변화율(%)", 
                        color="Color",
                        color_discrete_map="identity",
                        text="변화율(%)"
                    )
                    
                    fig.update_traces(
                        texttemplate='%{text:+.1f}%', # 양수에는 + 기호 표시
                        textposition='outside'
                    )
                    
                    fig.update_layout(
                        title=dict(text="<b>성분별 평균 변화율 (%)</b>", x=0.5, xanchor='center'),
                        xaxis_title="측정 성분",
                        yaxis_title="평균 변화율 (%)",
                        template="plotly_white",
                        height=600 if len(df_res) > 3 else 500, # 항목이 적을 때는 높이 조정
                        showlegend=False
                    )
                    
                    # 수평선(기준선 0) 추가
                    fig.add_hline(y=0, line_width=1, line_color="black")
                    
                    st.plotly_chart(fig, use_container_width=True, key="bar_chart_comp")
                else:
                    st.warning("선택하신 항목 중 유효한 변화율을 계산할 수 있는 데이터가 없습니다.")
            else:
                st.warning("비교할 방문 시점이 2개 이상 존재해야 합니다.")
