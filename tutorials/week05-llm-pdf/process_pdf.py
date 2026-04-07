"""
PDF → Markdown + DOCX 변환 스크립트

사용법:
    python process_pdf.py input.pdf
    python process_pdf.py input.pdf output_dir/
"""

import sys
import os
import re
import subprocess
from pathlib import Path
from io import BytesIO

import fitz  # pymupdf
from PIL import Image
from google import genai
from google.genai import types
from dotenv import load_dotenv

# .env 파일에서 API 키 불러오기
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("오류: .env 파일에 GEMINI_API_KEY가 설정되어 있지 않습니다.")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3.1-flash-lite-preview"

# ──────────────────────────────────────────────
# 1단계: pymupdf로 페이지별 이미지 추출
# ──────────────────────────────────────────────

def extract_images_from_page(page: fitz.Page, page_num: int, figures_dir: Path, seen_xrefs: set) -> list[str]:
    """
    한 페이지에서 이미지 객체를 추출하고 figures_dir에 저장.
    반환값: 저장된 파일 경로 리스트 (페이지 내 순서 기준)
    """
    saved_paths = []
    fig_counter = 0
    image_list = page.get_images(full=True)

    for img_info in image_list:
        xref = img_info[0]

        if xref in seen_xrefs:
            continue

        try:
            base_image = page.parent.extract_image(xref)
            img_bytes = base_image["image"]
            width = base_image["width"]
            height = base_image["height"]

            if width < 100 or height < 100:
                continue

            seen_xrefs.add(xref)
            fig_counter += 1
            filename = f"page{page_num}_fig{fig_counter}.png"
            save_path = figures_dir / filename

            img = Image.open(BytesIO(img_bytes))
            img.save(save_path, "PNG")
            saved_paths.append(str(save_path.relative_to(figures_dir.parent)))

        except Exception as e:
            print(f"  [경고] 페이지 {page_num} 이미지 추출 실패 (xref={xref}): {e}")

    return saved_paths


# ──────────────────────────────────────────────
# 2단계: pymupdf로 페이지 전체를 PNG로 렌더링
# ──────────────────────────────────────────────

def render_page_as_image(page: fitz.Page, dpi: int = 200) -> Image.Image:
    """
    fitz.Page를 지정 dpi로 렌더링해서 PIL Image로 반환.
    pdf2image + poppler 없이 fitz만으로 처리.
    """
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(BytesIO(pix.tobytes("png")))
    return img


# ──────────────────────────────────────────────
# 3단계: Gemini API로 페이지 PNG → Markdown 변환
# ──────────────────────────────────────────────

GEMINI_PROMPT = """이 이미지는 PDF 문서의 한 페이지입니다. 페이지 전체 내용을 Markdown 형식으로 변환해 주세요.

## 기본 변환 규칙

- 텍스트: 원본 내용을 그대로 Markdown 문법으로 표현 (제목, 목록 등 포함)
- 수식: LaTeX 인라인 수식 ($...$) 또는 블록 수식 ($$...$$) 형식으로 변환
- 2단 레이아웃: 왼쪽 컬럼 전체 → 오른쪽 컬럼 전체 순서로 선형화
- 추가 설명 없이 Markdown 내용만 출력 (코드블록 래퍼 없이)

## 제외할 항목 (출력하지 말 것)

페이지 상하단의 저널 메타데이터는 본문이 아니므로 출력하지 말 것:
- 상단: 저널명, 권호(Vol./No.), ISSN, DOI 헤더, 수신/수락/게재일
- 하단: 페이지 번호, 저작권 표시(© ...), 출판사명, URL

## Figure / 이미지 처리

- 그래프, 차트, 실험 사진, 다이어그램 등 실제 Figure가 있는 위치에 [FIGURE_1], [FIGURE_2] 형식의 플레이스홀더를 등장 순서대로 삽입
- 장식용 선, 배경, 로고 등은 플레이스홀더 제외
- **[중요] Figure 내부의 텍스트(축 레이블, 범례, 그래프 내 수치, 화살표 설명 등)는 별도로 추출하거나 본문에 기재하지 말 것.**
- 플레이스홀더 바로 다음 줄에 Figure 캐션(본문에 명시된 경우)만 *캐션 텍스트* 형식으로 추가

## 표(Table) 처리

- 표는 Markdown 표(| 구분자) 형식으로 변환
- **[중요] 표를 변환할 때 이미지의 세로 구분선을 직접 세어 컬럼 수를 먼저 파악하고, 모든 행에서 해당 컬럼 수를 반드시 유지할 것.**
  세로선이 없는 표는 데이터 간 공백 간격을 기준으로 컬럼을 구분하되, 우측 끝 데이터까지 빠짐없이 포함할 것.
- **[중요] 페이지 상단에서 표가 헤더 행 없이 데이터 행으로 시작하는 경우**, 이전 페이지에서 이어지는 표일 가능성이 높음.
  이 경우 표 바로 위에 다음 주석을 삽입:
  `<!-- TABLE_CONTINUES_FROM_PREVIOUS_PAGE -->`
- **[중요] 페이지 하단에서 표의 마지막 행이 잘린 것처럼 보이거나 표가 완성되지 않은 경우**, 표 바로 아래에 다음 주석을 삽입:
  `<!-- TABLE_CONTINUES_TO_NEXT_PAGE -->`
"""


def extract_table_header(markdown_text: str) -> str | None:
    """
    Markdown 텍스트에서 마지막 표의 헤더 행+구분선을 추출해서 반환.
    TABLE_CONTINUES_TO_NEXT_PAGE 주석이 있을 때 다음 페이지 OCR에 전달하기 위해 사용.

    반환 예시:
        | α-羟基酸组分 | 检出限 (μg) | 定量下限 (μg) | 检出浓度 (μg/g) | 最低定量浓度 (μg/g) |
        |:---|:---|:---|:---|:---|
    """
    lines = markdown_text.split("\n")
    header_row = None
    separator_row = None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            # 헤더 다음 줄이 구분선 행(|---|)인지 확인
            if next_line.startswith("|") and re.match(r'\|[-:\s|]+\|', next_line):
                header_row = stripped
                separator_row = next_line

    if header_row and separator_row:
        return f"{header_row}\n{separator_row}"
    return None


def page_image_to_markdown(page_image: Image.Image, table_header: str | None = None) -> str:
    """
    페이지 이미지를 Gemini API에 전달해서 Markdown 텍스트 반환.
    table_header: 이전 페이지에서 이어지는 표의 헤더 (있으면 프롬프트에 주입)
    """
    buf = BytesIO()
    page_image.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    # 이전 페이지에서 이어지는 표가 있으면 헤더 정보를 프롬프트에 추가
    prompt = GEMINI_PROMPT
    if table_header:
        col_count = table_header.count("|") // 2
        prompt += f"""

## 이전 페이지에서 이어지는 표 (최우선 적용)

이 페이지 상단의 표는 이전 페이지에서 이어지는 표입니다.
아래는 이전 페이지에서 확인된 이 표의 헤더와 컬럼 구조입니다:

{table_header}

- 위 헤더 기준으로 컬럼 수({col_count}개)를 반드시 유지할 것
- 세로 구분선이 없더라도 데이터 간 공백을 기준으로 컬럼을 구분하고 모든 셀을 포함할 것
- 이 페이지의 데이터 행에도 헤더와 동일한 수의 셀이 있어야 함
- 이 표의 데이터 행 위에 <!-- TABLE_CONTINUES_FROM_PREVIOUS_PAGE --> 주석을 삽입할 것
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        ],
    )
    return response.text.strip()


# ──────────────────────────────────────────────
# 4단계: 플레이스홀더 → 실제 이미지 경로 치환
# ──────────────────────────────────────────────

def replace_placeholders(markdown_text: str, image_paths: list[str]) -> str:
    """
    [FIGURE_1], [FIGURE_2], ... 를 실제 이미지 경로로 치환.
    페이지별 독립 카운터 사용 (1-indexed).
    추출된 이미지보다 플레이스홀더가 많으면 그대로 남김.
    """
    def replacer(match):
        idx = int(match.group(1)) - 1
        if idx < len(image_paths):
            return f"![]({image_paths[idx]})"
        return match.group(0)

    return re.sub(r'\[FIGURE_(\d+)\]', replacer, markdown_text)


# ──────────────────────────────────────────────
# 5단계: 페이지를 넘어 분리된 표 합치기 (후처리)
# ──────────────────────────────────────────────

def merge_continued_tables(markdown_text: str) -> str:
    """
    TABLE_CONTINUES 주석 쌍을 기준으로 페이지를 넘어 분리된 표를 하나로 병합.
    연속 3페이지 이상도 while 루프에서 i를 유지해 처리.
    """
    pages = markdown_text.split("\n\n---\n\n")

    i = 0
    merged_count = 0
    while i < len(pages) - 1:
        current = pages[i]
        next_page = pages[i + 1]

        if ("<!-- TABLE_CONTINUES_TO_NEXT_PAGE -->" in current and
                "<!-- TABLE_CONTINUES_FROM_PREVIOUS_PAGE -->" in next_page):

            current_clean = current.replace(
                "\n<!-- TABLE_CONTINUES_TO_NEXT_PAGE -->", ""
            ).rstrip()

            next_clean = next_page.replace(
                "<!-- TABLE_CONTINUES_FROM_PREVIOUS_PAGE -->\n", ""
            ).lstrip()

            # 표 행(| 로 시작)과 나머지 본문 분리
            next_lines = next_clean.split("\n")
            table_lines = []
            non_table_lines = []
            in_table = True
            for line in next_lines:
                if in_table and line.strip().startswith("|"):
                    table_lines.append(line)
                else:
                    in_table = False
                    non_table_lines.append(line)

            merged = current_clean + "\n" + "\n".join(table_lines)
            remaining = "\n".join(non_table_lines).strip()
            if remaining:
                merged += "\n\n" + remaining

            pages[i] = merged
            pages.pop(i + 1)
            merged_count += 1
            # i 유지: 합쳐진 페이지가 또 TABLE_CONTINUES_TO_NEXT_PAGE를 가질 수 있음
        else:
            i += 1

    if merged_count > 0:
        print(f"  [후처리] 페이지 연속 표 {merged_count}건 병합 완료")

    return "\n\n---\n\n".join(pages)


# ──────────────────────────────────────────────
# 메인 파이프라인
# ──────────────────────────────────────────────

def process_pdf(input_pdf: str, output_dir: str):
    input_path = Path(input_pdf)
    out_path = Path(output_dir)
    figures_dir = out_path / "figures"

    # 출력 디렉토리 생성
    out_path.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # PDF 열기
    pdf_doc = fitz.open(str(input_path))
    total_pages = len(pdf_doc)
    print(f"총 {total_pages}페이지 처리 시작: {input_path.name}")

    all_markdown_pages = []
    seen_xrefs: set = set()
    pending_table_header: str | None = None  # 이전 페이지에서 이어지는 표 헤더

    for page_num in range(1, total_pages + 1):
        print(f"페이지 {page_num}/{total_pages} 처리 중...")

        try:
            page = pdf_doc[page_num - 1]

            # ── 이미지 추출 (pymupdf)
            image_paths = extract_images_from_page(page, page_num, figures_dir, seen_xrefs)

            # ── 스캔본 감지
            text_content = page.get_text().strip()
            if len(image_paths) == 0 and len(text_content) < 50:
                print(f"  [경고] 페이지 {page_num}: 스캔본으로 의심됩니다 (추출 이미지 0개, 텍스트 {len(text_content)}자)")

            # ── 페이지 전체 렌더링 (fitz, dpi=200)
            page_img = render_page_as_image(page, dpi=200)

            # ── Gemini API로 Markdown 변환 (이전 페이지 표 헤더 있으면 주입)
            markdown_raw = page_image_to_markdown(page_img, pending_table_header)
            if pending_table_header:
                print(f"  [표 연속] 이전 헤더 주입 → 컬럼 수 고정")

            # ── 다음 페이지를 위해 표 헤더 추출 또는 초기화
            if "<!-- TABLE_CONTINUES_TO_NEXT_PAGE -->" in markdown_raw:
                pending_table_header = extract_table_header(markdown_raw)
                print(f"  [표 연속] 다음 페이지로 헤더 전달 예정")
            else:
                pending_table_header = None

            # ── 플레이스홀더 치환
            markdown_replaced = replace_placeholders(markdown_raw, image_paths)
            all_markdown_pages.append(markdown_replaced)

        except Exception as e:
            print(f"  [오류] 페이지 {page_num} 처리 실패, 건너뜀: {e}")
            all_markdown_pages.append(f"_[페이지 {page_num} 처리 오류: {e}]_")
            pending_table_header = None  # 오류 시 헤더 초기화

    pdf_doc.close()

    # ── 전체 Markdown 합치기 (페이지 구분선 포함)
    full_markdown = "\n\n---\n\n".join(all_markdown_pages)

    # ── 페이지를 넘어 분리된 표 병합 후처리
    full_markdown = merge_continued_tables(full_markdown)

    md_output = out_path / "output.md"
    md_output.write_text(full_markdown, encoding="utf-8")
    print(f"\nMarkdown 저장 완료: {md_output}")

    # ── pandoc으로 DOCX 변환
    docx_output = out_path / "output.docx"
    print("DOCX 변환 중 (pandoc)...")
    try:
        cmd = ["pandoc", "output.md", "-o", "output.docx"]
        template = Path("Template.docx")
        if not template.exists():
            template = Path("template.docx")
        if template.exists():
            cmd += [f"--reference-doc={template.resolve()}"]
            print(f"  템플릿 적용: {template}")
        subprocess.run(
            cmd,
            cwd=str(out_path),
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"DOCX 저장 완료: {docx_output}")
    except FileNotFoundError:
        print("  [오류] pandoc이 설치되어 있지 않습니다. pandoc을 설치하세요.")
    except subprocess.CalledProcessError as e:
        print(f"  [오류] pandoc 변환 실패: {e.stderr}")

    print("\n완료!")
    print(f"  figures : {figures_dir}/")
    print(f"  markdown: {md_output}")
    print(f"  docx    : {docx_output}")


# ──────────────────────────────────────────────
# CLI 진입점
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("사용법: python process_pdf.py input.pdf [output_dir/]")
        print("  output_dir 생략 시 PDF 파일명 기반 폴더 자동 생성")
        sys.exit(1)

    input_pdf = sys.argv[1]

    if not Path(input_pdf).exists():
        print(f"오류: 파일을 찾을 수 없습니다: {input_pdf}")
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) == 3 else Path(input_pdf).stem

    process_pdf(input_pdf, output_dir)
