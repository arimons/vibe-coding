import streamlit as st
import pandas as pd
import io
from pathlib import Path


def download_buttons(df_target: pd.DataFrame, prefix: str = ""):
    c1, c2, _ = st.columns([1, 1, 4])
    with c1:
        csv = df_target.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("⬇️ CSV", data=csv, file_name="converted.csv",
                           mime="text/csv", use_container_width=True,
                           key=f"dl_csv_{prefix}")
    with c2:
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_target.to_excel(w, index=False, sheet_name="변환결과")
        st.download_button("⬇️ Excel", data=buf.getvalue(),
                           file_name="converted.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True, key=f"dl_xlsx_{prefix}")


def df():
    return st.session_state.df_work


st.set_page_config(page_title="임상 데이터 변환기", page_icon="🔬",
                   layout="wide", initial_sidebar_state="collapsed")

for k, v in [("df_original", None), ("df_work", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

col_title, col_reset = st.columns([9, 1])
with col_title:
    st.title("🔬 임상 데이터 변환기")
    st.caption("측정 소프트웨어 양식 → 통계 프로그램 양식 변환")
with col_reset:
    st.write("")
    st.write("")
    if st.session_state.df_work is not None:
        if st.button("🔄 초기화", use_container_width=True):
            st.session_state.df_work = st.session_state.df_original.copy()
            for k in [k for k in st.session_state if k.startswith(
                    ("rename_", "drop_cols_select", "map_col_select", "regex_"))]:
                del st.session_state[k]
            st.rerun()

with st.expander("📂 파일 열기", expanded=st.session_state.df_work is None):
    upload_tab, path_tab = st.tabs(["파일 업로드", "경로 직접 입력"])
    with upload_tab:
        uploaded = st.file_uploader("CSV 또는 Excel", type=["csv", "xlsx", "xls"],
                                    label_visibility="collapsed")
        if uploaded:
            try:
                df_load = (pd.read_csv(uploaded) if uploaded.name.endswith(".csv")
                           else pd.read_excel(uploaded))
                st.session_state.df_original = df_load.copy()
                st.session_state.df_work = df_load.copy()
                st.success(f"✅ {uploaded.name} — {df_load.shape[0]}행 × {df_load.shape[1]}열")
            except Exception as e:
                st.error(f"오류: {e}")
    with path_tab:
        app_dir = Path(__file__).parent
        st.caption(f"앱 실행 위치: `{app_dir}`")
        file_path = st.text_input("파일 경로 (상대경로 가능)", placeholder="data/sample_raw.csv")
        if st.button("불러오기") and file_path:
            try:
                p = Path(file_path) if Path(file_path).is_absolute() else app_dir / file_path
                df_load = pd.read_csv(p) if p.suffix == ".csv" else pd.read_excel(p)
                st.session_state.df_original = df_load.copy()
                st.session_state.df_work = df_load.copy()
                st.success(f"✅ {p.name} — {df_load.shape[0]}행 × {df_load.shape[1]}열")
            except Exception as e:
                st.error(f"오류: {e}")

if st.session_state.df_work is None:
    st.info("위에서 파일을 업로드하거나 경로를 입력하세요.")
    st.markdown("샘플 파일: `data/sample_raw.csv`")
    st.stop()

st.caption(f"현재 데이터: **{df().shape[0]}행 × {df().shape[1]}열** | 결측값: **{int(df().isnull().sum().sum())}개**")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 원본 보기", "📝 열 관리", "🔢 정규식 변환",
    "🔁 값 변환", "↕️ Wide → Long", "💾 최종 저장"
])

# ── TAB 1 ─────────────────────────────────────────────────────
with tab1:
    info_col, data_col = st.columns([1, 3])
    with info_col:
        st.subheader("파일 정보")
        st.metric("행", df().shape[0])
        st.metric("열", df().shape[1])
        st.metric("결측값", int(df().isnull().sum().sum()))
        st.dataframe(pd.DataFrame({
            "열": df().columns,
            "타입": df().dtypes.values.astype(str),
            "결측": df().isnull().sum().values
        }), use_container_width=True, hide_index=True)
    with data_col:
        st.subheader("현재 데이터")
        st.dataframe(df(), use_container_width=True)
        with st.expander("기술통계"):
            st.dataframe(df().describe(), use_container_width=True)

# ── TAB 2 ─────────────────────────────────────────────────────
with tab2:
    with st.expander("① 열 이름 변경", expanded=True):
        st.caption("새 이름 입력 후 Enter 또는 아래 버튼을 누르세요.")
        current_cols = list(df().columns)
        with st.form(key="rename_form"):
            rename_map = {}
            for i in range(0, len(current_cols), 3):
                cols = st.columns(3)
                for j, col in enumerate(current_cols[i:i+3]):
                    with cols[j]:
                        new_name = st.text_input(col, value=col, key=f"rename_{col}")
                        if new_name.strip() and new_name.strip() != col:
                            rename_map[col] = new_name.strip()
            if rename_map:
                st.dataframe(pd.DataFrame([{"원본": k, "→": "→", "변경 후": v}
                                           for k, v in rename_map.items()]),
                             use_container_width=True, hide_index=True)
            if st.form_submit_button("✅ 열 이름 변경 적용", use_container_width=True):
                if rename_map:
                    st.session_state.df_work = df().rename(columns=rename_map)
                    st.rerun()
                else:
                    st.warning("변경할 열 이름이 없습니다.")

    with st.expander("② 열 순서 재배치", expanded=True):
        try:
            from streamlit_sortables import sort_items
            st.caption("카드를 드래그해서 순서를 바꾸고 적용 버튼을 누르세요.")
            current_cols = list(df().columns)
            sorted_cols = sort_items(current_cols, direction="horizontal", key="col_sortable")
            if sorted_cols != current_cols:
                st.info("변경 후 순서: " + " → ".join(sorted_cols))
                if st.button("✅ 열 순서 적용", key="btn_reorder"):
                    st.session_state.df_work = df()[sorted_cols]
                    st.rerun()
        except ImportError:
            st.warning("`pip install streamlit-sortables` 후 재시작하세요.")
            order_df = pd.DataFrame({"열 이름": list(df().columns),
                                     "순서": list(range(1, len(df().columns)+1))})
            edited = st.data_editor(order_df, use_container_width=True,
                                    hide_index=True, disabled=["열 이름"], key="order_editor")
            if st.button("✅ 열 순서 적용", key="btn_reorder"):
                st.session_state.df_work = df()[edited.sort_values("순서")["열 이름"].tolist()]
                st.rerun()

    with st.expander("③ 열 삭제"):
        prev_drop = st.session_state.get("drop_cols_select", [])
        st.session_state["drop_cols_select"] = [c for c in prev_drop if c in df().columns]
        drop_cols = st.multiselect("삭제할 열 선택", options=list(df().columns),
                                   key="drop_cols_select")
        if drop_cols:
            st.warning(f"삭제 예정: {drop_cols}")
        if st.button("🗑️ 선택한 열 삭제", key="btn_drop"):
            if drop_cols:
                st.session_state.df_work = df().drop(columns=drop_cols)
                st.session_state["drop_cols_select"] = []
                st.rerun()
            else:
                st.warning("삭제할 열을 선택하세요.")

    st.divider()
    preview_tab2 = df().copy()
    live_rename = {col: str(st.session_state.get(f"rename_{col}", col)).strip()
                   for col in list(df().columns)
                   if str(st.session_state.get(f"rename_{col}", col)).strip() != col}
    if live_rename:
        preview_tab2 = preview_tab2.rename(columns=live_rename)
    live_drop = [c for c in st.session_state.get("drop_cols_select", [])
                 if c in preview_tab2.columns]
    if live_drop:
        preview_tab2 = preview_tab2.drop(columns=live_drop)
    st.markdown("**미리보기 (현재 설정 반영):**")
    st.dataframe(preview_tab2, use_container_width=True)
    download_buttons(preview_tab2, "tab2_")

# ── TAB 3 — 정규식 변환 ───────────────────────────────────────
with tab3:
    st.subheader("🔢 정규식 변환")
    st.caption("열을 선택하고 정규식 패턴으로 값을 추출하거나 변환합니다.")

    # 예시 테이블 — 기본 펼쳐짐
    with st.expander("📖 패턴 예시 — 복사해서 사용하세요", expanded=True):

        tab_ex1, tab_ex2, tab_ex3 = st.tabs(["추출 패턴", "치환 패턴", "기호 설명"])

        with tab_ex1:
            st.caption("추출(Extract): 패턴과 일치하는 부분을 새 열로 꺼냅니다. 괄호`()`안 내용이 결과가 됩니다.")
            extract_examples = pd.DataFrame([
                {"목적": "숫자만 추출",      "패턴": r"([\d.]+)",    "입력 예": "45.2 AU",          "결과": "45.2"},
                {"목적": "괄호 안 성별",    "패턴": r"\(([MF])",    "입력 예": "S001_김민지(F/28)", "결과": "F"},
                {"목적": "괄호 안 나이",    "패턴": r"/(\d+)\)",    "입력 예": "S001_김민지(F/28)", "결과": "28"},
                {"목적": "언더스코어 앞 ID","패턴": r"^([^_]+)",    "입력 예": "S001_김민지(F/28)", "결과": "S001"},
                {"목적": "이름만 추출",     "패턴": r"_([^(]+)\(",  "입력 예": "S001_김민지(F/28)", "결과": "김민지"},
                {"목적": "첫 번째 숫자 그룹","패턴": r"(\d+)",      "입력 예": "V1",                "결과": "1"},
            ])
            st.dataframe(extract_examples, use_container_width=True, hide_index=True)

        with tab_ex2:
            st.caption("치환(Replace): 패턴과 일치하는 부분을 다른 값으로 바꿉니다. '바꿀 값'을 비우면 삭제입니다.")
            replace_examples = pd.DataFrame([
                {"목적": "끝 단위 제거",    "패턴": r"\s*[A-Za-zμ²/h]+$", "바꿀 값": "",  "입력 예": "8.3 g/m²h", "결과": "8.3"},
                {"목적": "특정 단위 제거",  "패턴": r"\s*AU",             "바꿀 값": "",  "입력 예": "45.2 AU",   "결과": "45.2"},
                {"목적": "앞뒤 공백 제거",  "패턴": r"^\s+|\s+$",         "바꿀 값": "",  "입력 예": "  없음  ",  "결과": "없음"},
                {"목적": "슬래시 기준 앞만","패턴": r"/.*$",              "바꿀 값": "",  "입력 예": "F/28",      "결과": "F"},
                {"목적": "괄호 포함 제거",  "패턴": r"\(.*\)",            "바꿀 값": "",  "입력 예": "(F/28)",    "결과": ""},
            ])
            st.dataframe(replace_examples, use_container_width=True, hide_index=True)

        with tab_ex3:
            st.caption("자주 쓰는 정규식 기호 설명입니다.")
            symbol_examples = pd.DataFrame([
                {"기호": r"()",    "의미": "이 안의 내용을 추출 (캡처 그룹)",          "예": r"([\d.]+) → 숫자 부분만"},
                {"기호": r"[\d]",  "의미": "숫자 한 글자",                            "예": r"[\d]+ → 45, 28 등"},
                {"기호": r"[.]",   "의미": "점 문자 자체",                            "예": r"[\d.]+ → 45.2"},
                {"기호": r"+",     "의미": "앞 패턴 1회 이상 반복",                   "예": r"[\d.]+ → 45.2 전체"},
                {"기호": r"*",     "의미": "앞 패턴 0회 이상 반복",                   "예": r"\s* → 공백 없어도 됨"},
                {"기호": r"^",     "의미": "문자열 시작",                             "예": r"^S → S로 시작"},
                {"기호": r"$",     "의미": "문자열 끝",                               "예": r"AU$ → AU로 끝"},
                {"기호": r"\(",    "의미": "괄호 문자 ( 자체 (역슬래시로 이스케이프)", "예": r"\( → 여는 괄호"},
                {"기호": r"[^_]",  "의미": "_가 아닌 모든 문자",                      "예": r"[^_]+ → _ 전까지"},
                {"기호": r"\s",    "의미": "공백 문자 (스페이스, 탭 등)",              "예": r"\s* → 0개 이상 공백"},
            ])
            st.dataframe(symbol_examples, use_container_width=True, hide_index=True)

    # 변환 UI
    col_sel, col_regex = st.columns([1, 2])

    with col_sel:
        regex_col = st.selectbox("변환할 열 선택",
                                 options=["선택하세요"] + list(df().columns),
                                 key="regex_col_select")
        if regex_col != "선택하세요":
            st.markdown("**샘플 값:**")
            for s in df()[regex_col].dropna().astype(str).head(5).tolist():
                st.code(s)

    with col_regex:
        if regex_col != "선택하세요":
            mode = st.radio("변환 방식",
                            ["추출 (Extract) — 패턴에서 값 꺼내기",
                             "치환 (Replace) — 패턴과 일치하는 부분 바꾸기"],
                            key="regex_mode")

            is_extract = "추출" in mode
            default_pattern = r"([\d.]+)" if is_extract else r"\s*[A-Za-zμ²/h]+$"

            pattern = st.text_input(
                "정규식 패턴" + (" — 괄호`()`안 내용이 추출됩니다" if is_extract else ""),
                value=st.session_state.get("regex_pattern_val", default_pattern),
                key="regex_pattern"
            )
            st.session_state["regex_pattern_val"] = pattern

            if not is_extract:
                replacement = st.text_input("바꿀 값 (비우면 삭제)", value="", key="regex_replacement")

            to_numeric = st.checkbox("결과를 숫자형으로 변환", value=is_extract, key="regex_to_num")

            new_col_name = st.text_input(
                "결과 저장 열 이름",
                value=f"{regex_col}_추출" if is_extract else regex_col,
                key="regex_new_col"
            )

            st.markdown("**변환 미리보기:**")
            try:
                preview_series = df()[regex_col].astype(str).head(8)
                if is_extract:
                    result_series = preview_series.str.extract(pattern)[0]
                else:
                    repl = st.session_state.get("regex_replacement", "")
                    result_series = preview_series.str.replace(pattern, repl, regex=True).str.strip()

                if to_numeric:
                    result_series = pd.to_numeric(result_series, errors="coerce")

                col_name_display = new_col_name.strip() or "결과"
                st.dataframe(pd.DataFrame({
                    regex_col: preview_series.values,
                    "→": "→",
                    col_name_display: result_series.values
                }), use_container_width=True, hide_index=True)

                if st.button("✅ 변환 적용", key="btn_regex"):
                    full_series = df()[regex_col].astype(str)
                    if is_extract:
                        result_full = full_series.str.extract(pattern)[0]
                    else:
                        repl = st.session_state.get("regex_replacement", "")
                        result_full = full_series.str.replace(pattern, repl, regex=True).str.strip()
                    if to_numeric:
                        result_full = pd.to_numeric(result_full, errors="coerce")
                    col_name_save = new_col_name.strip() if new_col_name.strip() else f"{regex_col}_변환"
                    st.session_state.df_work[col_name_save] = result_full
                    st.rerun()

            except Exception as e:
                st.error(f"정규식 오류: {e}")

    st.divider()
    st.markdown("**현재 데이터 (적용 누적):**")
    st.dataframe(df(), use_container_width=True)
    download_buttons(df(), "tab3_")

# ── TAB 4 — 값 변환 ───────────────────────────────────────────
with tab4:
    st.subheader("🔁 값 변환 — 코딩 변환")
    st.caption("없음→0, 경미→1, 중등도→2 / 건성→1, 지성→2 등")

    prev_map_col = st.session_state.get("map_col_select", "선택하세요")
    if prev_map_col not in list(df().columns) + ["선택하세요"]:
        st.session_state["map_col_select"] = "선택하세요"

    map_col = st.selectbox("변환할 열 선택",
                           options=["선택하세요"] + list(df().columns),
                           key="map_col_select")

    mapping = {}
    if map_col != "선택하세요":
        unique_vals = df()[map_col].dropna().unique().tolist()
        left, right = st.columns([1, 1])
        with left:
            st.markdown(f"**`{map_col}` — 변환값 입력**")
            for val in unique_vals:
                c1, c2 = st.columns([1, 1])
                c1.text(f"  {val}")
                new_val = c2.text_input("→", key=f"map_{map_col}_{val}",
                                        label_visibility="collapsed", placeholder="변환값")
                if new_val.strip():
                    try:
                        mapping[val] = int(new_val)
                    except ValueError:
                        try:
                            mapping[val] = float(new_val)
                        except ValueError:
                            mapping[val] = new_val
        with right:
            st.markdown("**열 변환 미리보기**")
            if mapping:
                col_preview = df()[[map_col]].copy()
                col_preview["변환 후"] = col_preview[map_col].map(mapping).fillna(col_preview[map_col])
                st.dataframe(col_preview, use_container_width=True, hide_index=True)
                st.caption(f"매핑: {mapping}")
            else:
                st.info("변환값을 입력하면 미리보기가 나타납니다.")

        if st.button("✅ 값 변환 적용", key="btn_map"):
            if mapping:
                st.session_state.df_work[map_col] = (
                    df()[map_col].map(mapping).fillna(df()[map_col]))
                st.rerun()
            else:
                st.warning("변환값을 입력하세요.")

    st.divider()
    preview_tab4 = df().copy()
    if mapping and map_col != "선택하세요":
        preview_tab4[map_col] = preview_tab4[map_col].map(mapping).fillna(preview_tab4[map_col])
    st.markdown("**미리보기 (현재 설정 반영):**")
    st.dataframe(preview_tab4, use_container_width=True)
    download_buttons(preview_tab4, "tab4_")

# ── TAB 5 — Wide → Long ───────────────────────────────────────
with tab5:
    st.subheader("↕️ Wide → Long 변환")
    with st.expander("📖 언제 필요한가?"):
        st.markdown("""
**샘플 데이터는 이미 Long format이라 이 탭이 필요 없을 수 있습니다.**

| 형태 | 구조 | 예 |
|------|------|---|
| Long (현재) | 피험자 × 시점 = 각 행 | 김민지 V1 / 김민지 V2 / 김민지 V3 |
| Wide | 피험자 한 행, 시점별 열 | 김민지 \\| V1_수분 \\| V2_수분 \\| V3_수분 |

R/SPSS에서 반복측정 ANOVA, mixed model 등을 돌릴 때 Long format이 필요합니다.  
측정 소프트웨어가 Wide format으로 export했을 때 사용하세요.
""")

    left, right = st.columns([1, 1])
    with left:
        id_cols = st.multiselect("고정 열 (피험자ID, 인구통계 등)",
                                 options=list(df().columns), key="id_cols")
        value_cols = st.multiselect("펼칠 열 (반복측정값)",
                                    options=[c for c in df().columns if c not in id_cols],
                                    key="value_cols")
        c1, c2 = st.columns(2)
        var_name = c1.text_input("변수명 열 이름", value="variable", key="var_name")
        val_name = c2.text_input("값 열 이름", value="value", key="val_name")

    with right:
        if id_cols and value_cols:
            preview_head = df()[id_cols + value_cols].head(3)
            melted_preview = preview_head.melt(
                id_vars=id_cols, value_vars=value_cols,
                var_name=var_name or "variable", value_name=val_name or "value")
            st.markdown("**변환 전 (Wide, 상위 3행):**")
            st.dataframe(preview_head, use_container_width=True)
            st.markdown("**변환 후 (Long):**")
            st.dataframe(melted_preview, use_container_width=True)
            st.caption(f"행 수: {df().shape[0]} → {df().shape[0] * len(value_cols)}")
        else:
            st.info("왼쪽에서 열을 선택하면 미리보기가 나타납니다.")

    if st.button("✅ Wide → Long 변환 적용", key="btn_melt"):
        if id_cols and value_cols:
            st.session_state.df_work = df().melt(
                id_vars=id_cols, value_vars=value_cols,
                var_name=var_name or "variable", value_name=val_name or "value")
            st.rerun()
        else:
            st.warning("고정 열과 펼칠 열을 모두 선택하세요.")

    st.divider()
    if id_cols and value_cols:
        preview_tab5 = df().melt(id_vars=id_cols, value_vars=value_cols,
                                 var_name=var_name or "variable", value_name=val_name or "value")
        st.markdown("**미리보기 (변환 후 전체):**")
    else:
        preview_tab5 = df()
        st.markdown("**현재 데이터:**")
    st.dataframe(preview_tab5, use_container_width=True)
    download_buttons(preview_tab5, "tab5_")

# ── TAB 6 ─────────────────────────────────────────────────────
with tab6:
    st.subheader("💾 최종 결과 저장")
    st.info("각 탭에서 **적용** 버튼을 누른 변환들이 누적된 최종 결과입니다.")
    st.markdown(f"**{df().shape[0]}행 × {df().shape[1]}열**")
    st.dataframe(df(), use_container_width=True)
    st.divider()
    download_buttons(df(), "tab6_")
