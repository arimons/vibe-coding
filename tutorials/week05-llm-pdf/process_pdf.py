"""
PDF → Markdown + DOCX 변환 스크립트

사용법:
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

        # 중복 이미지 제거
        if xref in seen_xrefs:
            continue

        try:
            base_image = page.parent.extract_image(xref)
            img_bytes = base_image["image"]
            width = base_image["width"]
            height = base_image["height"]

            # 너무 작은 이미지(로고, 아이콘 등) 제외
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
- **[중요] Figure 내부의 텍스트(축 레이블, 범례, 그래프 내 수치, 화살표 설명 등)는 별도로 추출하거나 본문에 기재하지 말 것.** 이미지 자체가 별도 파일로 저장되므로 내부 텍스트 재현은 불필요함.
- 플레이스홀더 바로 다음 줄에 Figure 캐션(본문에 명시된 경우)만 *캐션 텍스트* 형식으로 추가

## 표(Table) 처리

- 표는 Markdown 표(| 구분자) 형식으로 변환
- **[중요] 페이지 상단에서 표가 헤더 행 없이 데이터 행으로 시작하는 경우**, 이전 페이지에서 이어지는 표일 가능성이 높음. 이 경우 표 바로 위에 다음 주석을 삽입:
  `<!-- TABLE_CONTINUES_FROM_PREVIOUS_PAGE -->`
- **[중요] 페이지 하단에서 표의 마지막 행이 잘린 것처럼 보이거나 표가 완성되지 않은 경우**, 표 바로 아래에 다음 주석을 삽입:
  `<!-- TABLE_CONTINUES_TO_NEXT_PAGE -->`
"""


def page_image_to_markdown(page_image: Image.Image) -> str:
    """페이지 이미지를 Gemini API에 전달해서 Markdown 텍스트 반환."""
    buf = BytesIO()
    page_image.save(buf, format="PNG")
    image_bytes = buf.getvalue()

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            GEMINI_PROMPT,
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
        idx = int(match.group(1)) - 1  # 0-indexed
        if idx < len(image_paths):
            rel_path = image_paths[idx]
            return f"![]({rel_path})"
        else:
            return match.group(0)  # 플레이스홀더 그대로

    return re.sub(r'\[FIGURE_(\d+)\]', replacer, markdown_text)


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

            # ── Gemini API로 Markdown 변환
            markdown_raw = page_image_to_markdown(page_img)

            # ── 플레이스홀더 치환
            markdown_replaced = replace_placeholders(markdown_raw, image_paths)

            all_markdown_pages.append(markdown_replaced)

        except Exception as e:
            print(f"  [오류] 페이지 {page_num} 처리 실패, 건너뜀: {e}")
            all_markdown_pages.append(f"_[페이지 {page_num} 처리 오류: {e}]_")

    pdf_doc.close()

    # ── 전체 Markdown 합치기 (페이지 구분선 포함)
    full_markdown = "\n\n---\n\n".join(all_markdown_pages)
    md_output = out_path / "output.md"
    md_output.write_text(full_markdown, encoding="utf-8")
    print(f"\nMarkdown 저장 완료: {md_output}")

    # ── pandoc으로 DOCX 변환
    docx_output = out_path / "output.docx"
    print("DOCX 변환 중 (pandoc)...")
    try:
        cmd = ["pandoc", "output.md", "-o", "output.docx"]
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
