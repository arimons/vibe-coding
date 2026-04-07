"""
PDF → Markdown / 번역 변환 도구 (Streamlit GUI)

실행:
    uv run streamlit run app.py
"""

import sys
import subprocess
from pathlib import Path

import streamlit as st

# ──────────────────────────────────────────────
# 설정
# ──────────────────────────────────────────────

WORKSPACE = Path("workspace")   # 업로드 파일 및 결과물 저장 루트
TEMPLATE_PATH = Path("template.docx")   # 고정 템플릿 저장 경로

# .venv가 있으면 venv Python 사용, 없으면(전역 설치) 현재 Python 사용
_venv_python = Path(".venv/bin/python")
PYTHON = str(_venv_python) if _venv_python.exists() else sys.executable


# ──────────────────────────────────────────────
# 헬퍼: 서브프로세스 실시간 스트리밍
# ──────────────────────────────────────────────

def run_streaming(cmd: list, log_area) -> int:
    """
    cmd를 실행하면서 stdout을 log_area(st.empty)에 실시간으로 출력.
    반환값: 종료 코드
    """
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    lines = []
    for line in iter(process.stdout.readline, ""):
        lines.append(line.rstrip())
        log_area.code("\n".join(lines[-40:]), language="")
    process.stdout.close()
    process.wait()
    return process.returncode


# ──────────────────────────────────────────────
# 헬퍼: 다운로드 버튼 표시
# ──────────────────────────────────────────────

DOWNLOAD_FILES = [
    ("output.md",      "📄 원문 Markdown",  "text/markdown"),
    ("output.docx",    "📝 원문 DOCX",      "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("output_ko.md",   "🇰🇷 번역 Markdown", "text/markdown"),
    ("output_ko.docx", "🇰🇷 번역 DOCX",     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
]

def show_downloads(work_dir: Path):
    available = [(label, fname, mime) for fname, label, mime in DOWNLOAD_FILES
                 if (work_dir / fname).exists()]
    if not available:
        return

    st.divider()
    st.subheader("다운로드")
    cols = st.columns(len(available))
    for col, (label, fname, mime) in zip(cols, available):
        file_bytes = (work_dir / fname).read_bytes()
        col.download_button(label=label, data=file_bytes,
                            file_name=fname, mime=mime)


# ──────────────────────────────────────────────
# 작업 함수
# ──────────────────────────────────────────────

def do_generate_md(pdf_path: Path, work_dir: Path):
    st.info("📄 Markdown 생성 중...")
    log = st.empty()
    code = run_streaming(
        [PYTHON, "process_pdf.py", str(pdf_path), str(work_dir)],
        log,
    )
    if code == 0:
        st.success("Markdown 생성 완료!")
    else:
        st.error("Markdown 생성 중 오류가 발생했습니다. 위 로그를 확인하세요.")
    return code == 0


def do_translate(work_dir: Path, extra_instructions: str = ""):
    md_path = work_dir / "output.md"
    if not md_path.exists():
        st.error("output.md가 없습니다. 먼저 MD 생성을 실행하세요.")
        return False

    cmd = [PYTHON, "translate_md.py", str(md_path)]
    if extra_instructions.strip():
        cmd += ["--instructions", extra_instructions.strip()]

    st.info("🇰🇷 번역 중...")
    log = st.empty()
    code = run_streaming(cmd, log)
    if code == 0:
        st.success("번역 완료!")
    else:
        st.error("번역 중 오류가 발생했습니다. 위 로그를 확인하세요.")
    return code == 0


# ──────────────────────────────────────────────
# UI
# ──────────────────────────────────────────────

st.set_page_config(page_title="PDF 변환 도구", page_icon="📑", layout="centered")
st.title("📑 PDF → Markdown / 번역 변환")
st.caption("PDF를 업로드하면 Markdown 추출 및 한국어 번역을 진행합니다.")

# ── 파일 업로드 (2열 레이아웃)
col_pdf, col_tmpl = st.columns([2, 1])

with col_pdf:
    uploaded = st.file_uploader("PDF 파일 업로드", type="pdf")

with col_tmpl:
    uploaded_template = st.file_uploader(
        "DOCX 템플릿 (선택)",
        type=["docx"],
        help="업로드하면 template.docx로 저장되어 이후 변환에 계속 적용됩니다.",
    )
    if uploaded_template:
        TEMPLATE_PATH.write_bytes(uploaded_template.getvalue())
        st.success(f"템플릿 적용됨: {uploaded_template.name}")
    elif TEMPLATE_PATH.exists():
        st.info(f"현재 템플릿: `{TEMPLATE_PATH.name}`")
        if st.button("템플릿 제거", use_container_width=True):
            TEMPLATE_PATH.unlink()
            st.rerun()

if not uploaded:
    st.stop()

# ── 작업 폴더 설정
stem = Path(uploaded.name).stem
work_dir = WORKSPACE / stem
work_dir.mkdir(parents=True, exist_ok=True)

pdf_path = work_dir / uploaded.name
pdf_path.write_bytes(uploaded.getvalue())

st.caption(f"작업 폴더: `{work_dir}/`")

# ── 번역 추가 지침
with st.expander("🗒️ 번역 추가 지침 (선택)", expanded=False):
    extra_instructions = st.text_area(
        label="추가 지침",
        placeholder=(
            "예시:\n"
            "- '경피 흡수율'은 항상 '경피흡수율(transdermal absorption rate)'로 표기\n"
            "- ISO 시험법 번호(예: ISO 10993)는 영문 그대로 유지\n"
            "- 농도 단위 ppm, ppb는 번역하지 말 것"
        ),
        height=120,
        label_visibility="collapsed",
    )

st.divider()

# ── 액션 버튼
col1, col2, col3 = st.columns(3)
run_md  = col1.button("📄 MD 생성",    use_container_width=True)
run_tr  = col2.button("🇰🇷 번역",       use_container_width=True)
run_all = col3.button("⚡ All-in-One", use_container_width=True, type="primary")

# ── 실행
if run_md:
    do_generate_md(pdf_path, work_dir)

elif run_tr:
    do_translate(work_dir, extra_instructions)

elif run_all:
    ok = do_generate_md(pdf_path, work_dir)
    if ok:
        do_translate(work_dir, extra_instructions)

# ── 다운로드 (작업 결과가 있으면 항상 표시)
show_downloads(work_dir)
