"""
🔬 실험 데이터 분석기 — Raw Data → 취합 → 통계 → 시각화
Week 04 실전 실습용 Streamlit 앱

사용법:
  streamlit run app_analysis.py

필요 패키지:
  pip install streamlit pandas openpyxl plotly scipy
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import io
import re
from pathlib import Path

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="실험 데이터 분석기",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 세션 상태 초기화 ─────────────────────────────────────────
DEFAULTS = {
    "raw_sheets": {},          # {시트명: DataFrame} — 원본 시트들
    "df_tidy": None,           # 취합된 tidy DataFrame
    "file_info": None,         # 로드된 파일 정보
    "selected_sheets": [],     # 선택된 시트 목록
    "regex_pattern": r"V(\d+)_S(\d+)",
    "col_sample": None,        # 정규식 적용 컬럼
    "col_value": None,         # 측정값 컬럼
    "skip_rows": 0,            # 건너뛸 행 수
    "group_labels": {},        # Visit → 라벨 매핑 (예: {1: "섭취전", 2: "섭취후"})
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def df_tidy():
    """취합된 tidy DataFrame 반환 (함수로 접근하여 stale 방지)"""
    return st.session_state.df_tidy


# ── 유틸리티 함수 ────────────────────────────────────────────
def download_buttons(df_target: pd.DataFrame, prefix: str = ""):
    """CSV / Excel 다운로드 버튼"""
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        csv = df_target.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            "⬇️ CSV", data=csv, file_name="export.csv",
            mime="text/csv", use_container_width=True,
            key=f"dl_csv_{prefix}",
        )
    with c2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_target.to_excel(w, index=False, sheet_name="데이터")
        st.download_button(
            "⬇️ Excel", data=buf.getvalue(), file_name="export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True, key=f"dl_xlsx_{prefix}",
        )


def download_multi_sheet(sheets_dict: dict, filename: str, prefix: str = ""):
    """여러 시트를 포함한 Excel 다운로드"""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        for name, df_sheet in sheets_dict.items():
            safe_name = name[:31]  # Excel 시트명 31자 제한
            df_sheet.to_excel(w, index=False, sheet_name=safe_name)
    st.download_button(
        f"⬇️ {filename}",
        data=buf.getvalue(),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        key=f"dl_multi_{prefix}",
    )


# ── 헤더 ─────────────────────────────────────────────────────
col_title, col_reset = st.columns([9, 1])
with col_title:
    st.title("🔬 실험 데이터 분석기")
    st.caption("Raw Data → 취합 → 통계 처리 → 시각화")
with col_reset:
    st.write("")
    st.write("")
    if st.session_state.df_tidy is not None:
        if st.button("🔄 초기화", use_container_width=True):
            for k, v in DEFAULTS.items():
                st.session_state[k] = v
            st.rerun()


# ── 탭 구성 ──────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 데이터 로드",
    "🔧 데이터 취합",
    "📊 통계 처리",
    "📈 데이터 시각화",
    "💾 결과 저장",
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: 데이터 로드
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.subheader("📂 Excel 파일 로드")
    st.caption("분석할 Excel 파일을 업로드하세요. 여러 시트가 있으면 자동으로 인식합니다.")

    upload_tab, path_tab = st.tabs(["파일 업로드", "경로 직접 입력"])

    with upload_tab:
        uploaded = st.file_uploader(
            "Excel 파일", type=["xlsx", "xls"],
            label_visibility="collapsed",
        )
        if uploaded and st.button("📖 파일 읽기", key="btn_upload_read"):
            try:
                xls = pd.ExcelFile(uploaded)
                sheets = {}
                for name in xls.sheet_names:
                    sheets[name] = pd.read_excel(xls, sheet_name=name, header=None)
                st.session_state.raw_sheets = sheets
                st.session_state.file_info = uploaded.name
                st.success(f"✅ {uploaded.name} — {len(sheets)}개 시트 로드")
                st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")

    with path_tab:
        app_dir = Path(__file__).parent
        st.caption(f"앱 실행 위치: `{app_dir}`")
        file_path = st.text_input(
            "파일 경로 (상대경로 가능)",
            placeholder="data/Cicca B5_cholesterol_raw data.xlsx",
        )
        if st.button("📖 불러오기", key="btn_path_read") and file_path:
            try:
                p = Path(file_path) if Path(file_path).is_absolute() else app_dir / file_path
                xls = pd.ExcelFile(p)
                sheets = {}
                for name in xls.sheet_names:
                    sheets[name] = pd.read_excel(xls, sheet_name=name, header=None)
                st.session_state.raw_sheets = sheets
                st.session_state.file_info = p.name
                st.success(f"✅ {p.name} — {len(sheets)}개 시트 로드")
                st.rerun()
            except Exception as e:
                st.error(f"오류: {e}")

    # 추가 파일 로드 (여러 파일 합치기)
    if st.session_state.raw_sheets:
        st.divider()
        st.markdown(f"**현재 로드: `{st.session_state.file_info}`** — "
                     f"{len(st.session_state.raw_sheets)}개 시트")

        with st.expander("➕ 추가 파일 합치기 (시트 추가)", expanded=False):
            st.caption("다른 파일의 시트를 현재 데이터에 추가합니다.")
            extra_file = st.file_uploader(
                "추가 Excel 파일", type=["xlsx", "xls"],
                label_visibility="collapsed", key="extra_upload",
            )
            if extra_file and st.button("➕ 시트 추가", key="btn_add_sheets"):
                try:
                    xls2 = pd.ExcelFile(extra_file)
                    added = 0
                    for name in xls2.sheet_names:
                        # 시트명 충돌 시 파일명 접두어 추가
                        key = name if name not in st.session_state.raw_sheets else f"{extra_file.name}_{name}"
                        st.session_state.raw_sheets[key] = pd.read_excel(
                            xls2, sheet_name=name, header=None
                        )
                        added += 1
                    st.session_state.file_info += f" + {extra_file.name}"
                    st.success(f"✅ {added}개 시트 추가됨 (총 {len(st.session_state.raw_sheets)}개)")
                    st.rerun()
                except Exception as e:
                    st.error(f"오류: {e}")

        # 시트 목록 & 미리보기
        st.markdown("**시트 목록:**")
        sheet_names = list(st.session_state.raw_sheets.keys())
        cols = st.columns(min(len(sheet_names), 6))
        for i, name in enumerate(sheet_names):
            shape = st.session_state.raw_sheets[name].shape
            cols[i % len(cols)].code(f"{name}\n{shape[0]}행 × {shape[1]}열")

        preview_sheet = st.selectbox("미리보기 시트", sheet_names, key="preview_sheet")
        if preview_sheet:
            st.dataframe(
                st.session_state.raw_sheets[preview_sheet].head(15),
                use_container_width=True,
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: 데이터 취합
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.subheader("🔧 데이터 취합 — Raw → Tidy")

    if not st.session_state.raw_sheets:
        st.info("먼저 **📂 데이터 로드** 탭에서 파일을 로드하세요.")
        st.stop()

    sheet_names = list(st.session_state.raw_sheets.keys())

    # ── Step 1: 건너뛸 행 설정 ──
    with st.expander("① 건너뛸 행 수 (skiprows)", expanded=True):
        st.caption("장비 출력 파일은 상단에 메타데이터(장비명, 출력일시 등)가 있을 수 있습니다. "
                   "실제 데이터가 시작되는 행 위의 행 수를 입력하세요.")

        sample_sheet = st.selectbox("확인할 시트", sheet_names, key="skip_sample")
        if sample_sheet:
            st.markdown("**상단 10행 미리보기** — 데이터가 몇 행부터 시작하는지 확인:")
            st.dataframe(
                st.session_state.raw_sheets[sample_sheet].head(10),
                use_container_width=True,
            )

        skip = st.number_input(
            "건너뛸 행 수", min_value=0, max_value=50, value=st.session_state.skip_rows,
            help="예: 장비 메타데이터가 6행이면 6 입력",
        )
        st.session_state.skip_rows = skip

        if skip > 0:
            st.markdown(f"**skiprows={skip} 적용 후 미리보기:**")
            df_preview = st.session_state.raw_sheets[sample_sheet].iloc[skip:].reset_index(drop=True)
            df_preview.columns = df_preview.iloc[0]
            df_preview = df_preview[1:]
            st.dataframe(df_preview.head(10), use_container_width=True)

    # ── Step 2: 컬럼 선택 ──
    with st.expander("② 컬럼 선택", expanded=True):
        st.caption("정규식을 적용할 컬럼(피험자 정보)과 측정값 컬럼을 선택하세요.")

        # 첫 시트에서 헤더 추출
        first_sheet = st.session_state.raw_sheets[sheet_names[0]]
        if skip > 0 and skip < len(first_sheet):
            header_row = first_sheet.iloc[skip].tolist()
        else:
            header_row = first_sheet.iloc[0].tolist()

        col_options = [str(h) for h in header_row if pd.notna(h)]

        c1, c2 = st.columns(2)
        with c1:
            col_sample = st.selectbox(
                "피험자 정보 컬럼 (정규식 적용 대상)",
                options=col_options,
                index=col_options.index("Sample Text") if "Sample Text" in col_options else 0,
                key="sel_col_sample",
            )
        with c2:
            col_value = st.selectbox(
                "측정값 컬럼",
                options=col_options,
                index=col_options.index("ng/mg protein") if "ng/mg protein" in col_options else min(len(col_options)-1, 5),
                key="sel_col_value",
            )
        st.session_state.col_sample = col_sample
        st.session_state.col_value = col_value

        # 선택한 컬럼의 샘플값
        if col_sample and col_value:
            df_temp = first_sheet.iloc[skip:].reset_index(drop=True)
            df_temp.columns = df_temp.iloc[0]
            df_temp = df_temp[1:]
            if col_sample in df_temp.columns and col_value in df_temp.columns:
                st.markdown("**선택한 컬럼 샘플값:**")
                st.dataframe(
                    df_temp[[col_sample, col_value]].head(5),
                    use_container_width=True,
                )

    # ── Step 3: 정규식 패턴 ──
    with st.expander("③ 정규식 패턴 — 피험자 정보 분리", expanded=True):
        st.caption("피험자 정보 컬럼에서 그룹과 피험자 번호를 추출하는 정규식을 입력하세요.")

        with st.popover("📖 정규식 패턴 예시"):
            st.markdown("""
| 데이터 형식 | 패턴 | 결과 |
|------------|------|------|
| `V1_S12` | `V(\\d+)_S(\\d+)` | 그룹1, 캡처2 |
| `Pre_001` | `(Pre\|Post)_(\\d+)` | 그룹, 번호 |
| `BL-S03` | `(BL\|W4)\\-S(\\d+)` | 시점, 번호 |
| `Group1_ID005` | `Group(\\d+)_ID(\\d+)` | 그룹, ID |

**규칙:** 괄호 `()` 안에 들어간 부분이 추출됩니다.
- 첫 번째 `()` = 그룹/방문 정보
- 두 번째 `()` = 피험자 번호
            """)

        regex_pattern = st.text_input(
            "정규식 패턴",
            value=st.session_state.regex_pattern,
            help="첫 번째 캡처그룹 = 그룹/방문, 두 번째 캡처그룹 = 피험자 번호",
        )
        st.session_state.regex_pattern = regex_pattern

        # 미리보기
        if col_sample and regex_pattern:
            df_temp = first_sheet.iloc[skip:].reset_index(drop=True)
            df_temp.columns = df_temp.iloc[0]
            df_temp = df_temp[1:]
            if col_sample in df_temp.columns:
                sample_vals = df_temp[col_sample].dropna().astype(str).head(8)
                try:
                    extracted = sample_vals.str.extract(regex_pattern)
                    preview_df = pd.DataFrame({"원본": sample_vals.values})
                    for i in range(extracted.shape[1]):
                        preview_df[f"캡처{i+1}"] = extracted[i].values
                    st.markdown("**정규식 추출 미리보기:**")
                    st.dataframe(preview_df, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"정규식 오류: {e}")

    # ── Step 4: 그룹 라벨 매핑 ──
    with st.expander("④ 그룹 라벨 (선택사항)", expanded=True):
        st.caption("캡처그룹1의 값을 읽기 좋은 라벨로 변환합니다. 비워두면 원본 값을 사용합니다.")

        c1, c2 = st.columns(2)
        with c1:
            label_1 = st.text_input("캡처그룹1 값 '1' →", value="섭취전", key="lbl_1")
        with c2:
            label_2 = st.text_input("캡처그룹1 값 '2' →", value="섭취후", key="lbl_2")

        if label_1.strip() and label_2.strip():
            st.session_state.group_labels = {1: label_1.strip(), 2: label_2.strip()}
        else:
            st.session_state.group_labels = {}

    # ── Step 5: 시트 선택 & 취합 실행 ──
    with st.expander("⑤ 시트 선택 & 취합 실행", expanded=True):
        st.caption("취합할 시트를 선택하세요. 시트 이름이 성분(Component)으로 기록됩니다.")

        selected = st.multiselect(
            "취합할 시트",
            options=sheet_names,
            default=sheet_names,
            key="sel_sheets",
        )

        # 시트별 Component 이름 커스터마이징
        if selected:
            st.markdown("**시트별 성분 이름 (수정 가능):**")
            component_names = {}
            cols_grid = st.columns(min(len(selected), 4))
            for i, name in enumerate(selected):
                with cols_grid[i % len(cols_grid)]:
                    comp = st.text_input(name, value=name, key=f"comp_{name}")
                    component_names[name] = comp.strip() or name

        if st.button("🔄 취합 실행", key="btn_merge", type="primary", use_container_width=True):
            if not selected:
                st.warning("시트를 하나 이상 선택하세요.")
            else:
                try:
                    all_dfs = []
                    skip_n = st.session_state.skip_rows
                    pattern = st.session_state.regex_pattern
                    c_sample = st.session_state.col_sample
                    c_value = st.session_state.col_value
                    labels = st.session_state.group_labels

                    for sheet_name in selected:
                        raw = st.session_state.raw_sheets[sheet_name]

                        # skiprows + 헤더 설정
                        df_s = raw.iloc[skip_n:].reset_index(drop=True)
                        df_s.columns = df_s.iloc[0]
                        df_s = df_s[1:].reset_index(drop=True)

                        # 필요한 컬럼만
                        if c_sample not in df_s.columns or c_value not in df_s.columns:
                            st.warning(f"시트 '{sheet_name}'에 '{c_sample}' 또는 '{c_value}' 컬럼이 없습니다. 건너뜁니다.")
                            continue

                        df_s = df_s[[c_sample, c_value]].copy()
                        df_s = df_s.dropna(subset=[c_sample])

                        # 정규식 추출
                        extracted = df_s[c_sample].astype(str).str.extract(pattern)
                        if extracted.shape[1] >= 2:
                            df_s["_group_raw"] = pd.to_numeric(extracted[0], errors="coerce")
                            df_s["Subject"] = pd.to_numeric(extracted[1], errors="coerce")
                        elif extracted.shape[1] == 1:
                            df_s["_group_raw"] = pd.to_numeric(extracted[0], errors="coerce")
                            df_s["Subject"] = range(1, len(df_s) + 1)

                        # 그룹 라벨 매핑
                        if labels:
                            df_s["Group"] = df_s["_group_raw"].map(labels).fillna(
                                df_s["_group_raw"].astype(str)
                            )
                        else:
                            df_s["Group"] = df_s["_group_raw"].astype(str)

                        df_s["Component"] = component_names.get(sheet_name, sheet_name)
                        df_s["Value"] = pd.to_numeric(df_s[c_value], errors="coerce")
                        df_s = df_s[["Subject", "Group", "Component", "Value"]].dropna(subset=["Value"])

                        all_dfs.append(df_s)

                    if all_dfs:
                        df_merged = pd.concat(all_dfs, ignore_index=True)
                        st.session_state.df_tidy = df_merged
                        st.success(
                            f"✅ 취합 완료: {df_merged.shape[0]}행 × {df_merged.shape[1]}열 "
                            f"({df_merged['Component'].nunique()}개 성분, "
                            f"{int(df_merged['Subject'].nunique())}명 피험자)"
                        )
                        st.rerun()
                    else:
                        st.error("취합된 데이터가 없습니다. 설정을 확인하세요.")

                except Exception as e:
                    st.error(f"취합 오류: {e}")
                    import traceback
                    st.code(traceback.format_exc())

    # 취합 결과 미리보기
    if df_tidy() is not None:
        st.divider()
        st.markdown(f"**취합 결과:** {df_tidy().shape[0]}행 × {df_tidy().shape[1]}열")
        st.dataframe(df_tidy(), use_container_width=True)
        download_buttons(df_tidy(), "tab2_")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: 통계 처리
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.subheader("📊 통계 처리")

    if df_tidy() is None:
        st.info("먼저 **🔧 데이터 취합** 탭에서 데이터를 취합하세요.")
        st.stop()

    # ── Z-score 계산 ──
    with st.expander("Z-score 계산", expanded=True):
        st.caption(
            "Z-score = (값 − 평균) / 표준편차. "
            "성분별로 계산하여 서로 다른 스케일의 값을 비교할 수 있게 합니다."
        )

        zscore_scope = st.radio(
            "Z-score 계산 범위",
            ["Component별 (성분 내 표준화)", "Component × Group별 (그룹 내 표준화)"],
            key="zscore_scope",
        )

        if st.button("📐 Z-score 계산", key="btn_zscore", use_container_width=True):
            df = df_tidy().copy()
            if "Component별" in zscore_scope:
                df["Z"] = df.groupby("Component")["Value"].transform(
                    lambda x: stats.zscore(x, nan_policy="omit")
                )
            else:
                df["Z"] = df.groupby(["Component", "Group"])["Value"].transform(
                    lambda x: stats.zscore(x, nan_policy="omit")
                )
            st.session_state.df_tidy = df
            st.success("✅ Z-score 계산 완료")
            st.rerun()

    # ── 이상치 확인 ──
    if "Z" in df_tidy().columns:
        with st.expander("이상치 확인 (|Z| ≥ 2)", expanded=False):
            threshold = st.slider("Z-score 임계값", 1.5, 3.5, 2.0, 0.5, key="z_thresh")
            outliers = df_tidy()[df_tidy()["Z"].abs() >= threshold]
            if len(outliers) > 0:
                st.warning(f"⚠️ |Z| ≥ {threshold} 인 데이터: {len(outliers)}건")
                st.dataframe(outliers.sort_values("Z", ascending=False), use_container_width=True)
            else:
                st.success(f"✅ |Z| ≥ {threshold} 인 이상치가 없습니다.")

    # ── 요약 통계 ──
    with st.expander("요약 통계", expanded=True):
        summary = df_tidy().groupby(["Component", "Group"])["Value"].agg(
            n="count",
            평균="mean",
            표준편차="std",
            최소="min",
            중앙값="median",
            최대="max",
        ).round(4)
        st.dataframe(summary, use_container_width=True)

        # 변화율 (섭취전 → 섭취후)
        groups = df_tidy()["Group"].unique()
        if len(groups) == 2:
            st.markdown("**그룹 간 변화:**")
            means = df_tidy().groupby(["Component", "Group"])["Value"].mean().unstack("Group")
            g1, g2 = groups[0], groups[1]
            if g1 in means.columns and g2 in means.columns:
                change = pd.DataFrame({
                    g1: means[g1],
                    g2: means[g2],
                    "차이": means[g2] - means[g1],
                    "변화율(%)": ((means[g2] - means[g1]) / means[g1] * 100),
                }).round(4)
                st.dataframe(change, use_container_width=True)

    st.divider()
    st.markdown("**현재 데이터:**")
    st.dataframe(df_tidy(), use_container_width=True)
    download_buttons(df_tidy(), "tab3_")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4: 데이터 시각화
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.subheader("📈 데이터 시각화")

    if df_tidy() is None:
        st.info("먼저 **🔧 데이터 취합** 탭에서 데이터를 취합하세요.")
        st.stop()

    # ── 차트 설정 사이드바 ──
    with st.container():
        cfg_col, chart_col = st.columns([1, 3])

        with cfg_col:
            st.markdown("### 설정")

            # 차트 종류 선택 — 설명 포함
            chart_type = st.selectbox(
                "차트 종류",
                [
                    "Violin Plot — 분포 + 개별점",
                    "Box Plot — 사분위수 요약",
                    "Strip Plot — 개별 데이터 점",
                    "Bar Chart — 그룹 평균 비교",
                    "Histogram — 분포 빈도",
                    "Paired Plot — 전후 개인별 변화",
                ],
                key="chart_type",
            )

            # 성분 선택
            components = sorted(df_tidy()["Component"].unique())
            selected_components = st.multiselect(
                "성분 선택",
                options=components,
                default=components[:1] if components else [],
                key="viz_components",
            )

            # 색상 맵
            color_palette = st.selectbox(
                "색상",
                ["기본", "파랑-빨강", "초록-주황", "보라-노랑"],
                key="color_pal",
            )
            color_maps = {
                "기본": None,
                "파랑-빨강": {df_tidy()["Group"].unique()[0]: "#636EFA",
                           df_tidy()["Group"].unique()[-1]: "#EF553B"}
                           if len(df_tidy()["Group"].unique()) >= 2 else None,
                "초록-주황": {df_tidy()["Group"].unique()[0]: "#00CC96",
                           df_tidy()["Group"].unique()[-1]: "#FFA15A"}
                           if len(df_tidy()["Group"].unique()) >= 2 else None,
                "보라-노랑": {df_tidy()["Group"].unique()[0]: "#AB63FA",
                           df_tidy()["Group"].unique()[-1]: "#FECB52"}
                           if len(df_tidy()["Group"].unique()) >= 2 else None,
            }
            cmap = color_maps.get(color_palette)

            # 추가 옵션
            show_points = st.checkbox("개별 데이터 점 표시", value=True, key="show_pts")
            show_box = st.checkbox("박스플롯 포함", value=False, key="show_box")
            use_zscore = st.checkbox(
                "Z-score로 표시 (Y축)",
                value=False,
                disabled="Z" not in df_tidy().columns,
                key="use_z",
            )

        with chart_col:
            if not selected_components:
                st.info("왼쪽에서 성분을 하나 이상 선택하세요.")
            else:
                y_col = "Z" if use_zscore and "Z" in df_tidy().columns else "Value"
                y_label = "Z-score" if use_zscore else "ng/mg protein"
                chart_name = chart_type.split("—")[0].strip()

                for comp in selected_components:
                    df_plot = df_tidy()[df_tidy()["Component"] == comp].copy()

                    if chart_name == "Violin Plot":
                        fig = px.violin(
                            df_plot, x="Group", y=y_col, color="Group",
                            box=show_box,
                            points="all" if show_points else False,
                            title=comp,
                            color_discrete_map=cmap,
                        )
                        fig.update_layout(
                            yaxis_title=y_label, xaxis_title="",
                            showlegend=False,
                        )

                    elif chart_name == "Box Plot":
                        fig = px.box(
                            df_plot, x="Group", y=y_col, color="Group",
                            points="all" if show_points else False,
                            title=comp,
                            color_discrete_map=cmap,
                        )
                        fig.update_layout(
                            yaxis_title=y_label, xaxis_title="",
                            showlegend=False,
                        )

                    elif chart_name == "Strip Plot":
                        fig = px.strip(
                            df_plot, x="Group", y=y_col, color="Group",
                            title=comp,
                            color_discrete_map=cmap,
                        )
                        fig.update_layout(
                            yaxis_title=y_label, xaxis_title="",
                            showlegend=False,
                        )

                    elif chart_name == "Bar Chart":
                        df_bar = df_plot.groupby("Group")[y_col].agg(
                            ["mean", "std"]
                        ).reset_index()
                        fig = px.bar(
                            df_bar, x="Group", y="mean", color="Group",
                            error_y="std",
                            title=comp,
                            color_discrete_map=cmap,
                        )
                        fig.update_layout(
                            yaxis_title=f"{y_label} (평균 ± SD)", xaxis_title="",
                            showlegend=False,
                        )

                    elif chart_name == "Histogram":
                        fig = px.histogram(
                            df_plot, x=y_col, color="Group",
                            barmode="overlay", opacity=0.7,
                            title=comp,
                            color_discrete_map=cmap,
                        )
                        fig.update_layout(
                            xaxis_title=y_label, yaxis_title="빈도",
                        )

                    elif chart_name == "Paired Plot":
                        # 전후 비교 — 같은 Subject를 선으로 연결
                        groups = df_plot["Group"].unique()
                        if len(groups) != 2:
                            st.warning(f"{comp}: Paired Plot은 정확히 2개 그룹이 필요합니다.")
                            continue

                        df_wide = df_plot.pivot(
                            index="Subject", columns="Group", values=y_col
                        ).dropna()

                        fig = go.Figure()
                        g1, g2 = groups[0], groups[1]

                        # 개별 선
                        for subj in df_wide.index:
                            color = "#EF553B" if df_wide.loc[subj, g2] > df_wide.loc[subj, g1] else "#636EFA"
                            fig.add_trace(go.Scatter(
                                x=[g1, g2],
                                y=[df_wide.loc[subj, g1], df_wide.loc[subj, g2]],
                                mode="lines+markers",
                                line=dict(color=color, width=1),
                                marker=dict(size=6),
                                showlegend=False,
                                hovertext=f"Subject {int(subj)}",
                            ))

                        # 평균선
                        fig.add_trace(go.Scatter(
                            x=[g1, g2],
                            y=[df_wide[g1].mean(), df_wide[g2].mean()],
                            mode="lines+markers",
                            line=dict(color="black", width=3),
                            marker=dict(size=10, symbol="diamond"),
                            name="평균",
                        ))

                        fig.update_layout(
                            title=comp,
                            yaxis_title=y_label,
                            xaxis_title="",
                        )

                    st.plotly_chart(fig, use_container_width=True, key=f"chart_{comp}_{chart_name}")

                    # 간단 요약 테이블
                    with st.expander(f"{comp} — 요약 통계", expanded=False):
                        comp_summary = df_plot.groupby("Group")[y_col].agg(
                            ["count", "mean", "std", "min", "max"]
                        ).round(4)
                        st.dataframe(comp_summary, use_container_width=True)

    # ── 멀티 성분 비교 차트 ──
    st.divider()
    with st.expander("🔀 전체 성분 비교 (Z-score 기준)", expanded=False):
        if "Z" not in df_tidy().columns:
            st.info("📊 통계 처리 탭에서 Z-score를 먼저 계산하세요.")
        else:
            fig_all = px.box(
                df_tidy(), x="Component", y="Z", color="Group",
                title="전체 성분 Z-score 비교",
                color_discrete_map=cmap,
            )
            fig_all.update_layout(
                xaxis_title="", yaxis_title="Z-score",
                xaxis_tickangle=-45,
            )
            st.plotly_chart(fig_all, use_container_width=True)

            # 변화율 바 차트
            st.markdown("**성분별 평균 변화율:**")
            groups = df_tidy()["Group"].unique()
            if len(groups) == 2:
                means = df_tidy().groupby(["Component", "Group"])["Value"].mean().unstack("Group")
                g1, g2 = groups[0], groups[1]
                if g1 in means.columns and g2 in means.columns:
                    change_pct = ((means[g2] - means[g1]) / means[g1] * 100).reset_index()
                    change_pct.columns = ["Component", "변화율(%)"]
                    change_pct["색상"] = change_pct["변화율(%)"].apply(
                        lambda x: "증가" if x > 0 else "감소"
                    )
                    fig_change = px.bar(
                        change_pct, x="Component", y="변화율(%)", color="색상",
                        color_discrete_map={"증가": "#EF553B", "감소": "#636EFA"},
                        title=f"성분별 평균 변화율 ({g1} → {g2})",
                    )
                    fig_change.update_layout(xaxis_tickangle=-45, showlegend=False)
                    st.plotly_chart(fig_change, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 5: 결과 저장
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab5:
    st.subheader("💾 결과 저장")

    if df_tidy() is None:
        st.info("먼저 **🔧 데이터 취합** 탭에서 데이터를 취합하세요.")
        st.stop()

    st.markdown(f"**최종 데이터:** {df_tidy().shape[0]}행 × {df_tidy().shape[1]}열")
    st.dataframe(df_tidy(), use_container_width=True)

    st.divider()

    # ── 단일 시트 다운로드 ──
    st.markdown("**단일 시트:**")
    download_buttons(df_tidy(), "tab5_single_")

    # ── 멀티 시트 다운로드 ──
    st.markdown("**멀티 시트 (전체 데이터 + 요약 통계):**")

    sheets_to_export = {"전체데이터": df_tidy()}

    # 요약 통계 시트
    summary_export = df_tidy().groupby(["Component", "Group"])["Value"].agg(
        n="count", 평균="mean", 표준편차="std", 최소="min", 중앙값="median", 최대="max",
    ).reset_index().round(4)
    sheets_to_export["요약통계"] = summary_export

    # 변화율 시트
    groups = df_tidy()["Group"].unique()
    if len(groups) == 2:
        means = df_tidy().groupby(["Component", "Group"])["Value"].mean().unstack("Group")
        g1, g2 = groups[0], groups[1]
        if g1 in means.columns and g2 in means.columns:
            change_export = pd.DataFrame({
                "Component": means.index,
                g1: means[g1].values,
                g2: means[g2].values,
                "차이": (means[g2] - means[g1]).values,
                "변화율(%)": ((means[g2] - means[g1]) / means[g1] * 100).values,
            }).round(4)
            sheets_to_export["변화율"] = change_export

    # 성분별 개별 시트
    st.markdown("**성분별 개별 시트 포함:**")
    include_per_component = st.checkbox("성분별 시트도 추가", value=True, key="per_comp")
    if include_per_component:
        for comp in df_tidy()["Component"].unique():
            df_comp = df_tidy()[df_tidy()["Component"] == comp].copy()
            sheets_to_export[comp] = df_comp

    download_multi_sheet(sheets_to_export, "분석결과.xlsx", "tab5_multi_")

    st.caption(f"포함 시트: {', '.join(sheets_to_export.keys())}")
