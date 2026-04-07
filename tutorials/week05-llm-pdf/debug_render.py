"""
PDF 페이지를 PNG로 렌더링해서 workspace 에 저장하는 디버그 스크립트

사용법:
    python debug_render.py input.pdf
    python debug_render.py input.pdf --dpi 300
    python debug_render.py input.pdf --pages 2 3    # 특정 페이지만
"""

import sys
import argparse
from pathlib import Path
from io import BytesIO

import fitz  # pymupdf
from PIL import Image


def render_pages(input_pdf: str, dpi: int = 200, pages: list[int] | None = None):
    input_path = Path(input_pdf)
    out_dir = Path("workspace") / f"_debug_{input_path.stem}_dpi{dpi}"
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_doc = fitz.open(str(input_path))
    total_pages = len(pdf_doc)

    target_pages = pages if pages else list(range(1, total_pages + 1))
    print(f"렌더링 대상: {input_path.name}  총 {total_pages}페이지 중 {len(target_pages)}페이지")
    print(f"DPI: {dpi}  →  저장 위치: {out_dir}/")

    for page_num in target_pages:
        if page_num < 1 or page_num > total_pages:
            print(f"  [건너뜀] 페이지 {page_num}: 범위 초과 (총 {total_pages}페이지)")
            continue

        page = pdf_doc[page_num - 1]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(BytesIO(pix.tobytes("png")))

        out_path = out_dir / f"page_{page_num:03d}.png"
        img.save(out_path, "PNG")

        w, h = img.size
        print(f"  페이지 {page_num:3d}  →  {out_path.name}  ({w}x{h}px)")

    pdf_doc.close()
    print(f"\n완료: {out_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF 페이지 PNG 렌더링 디버그 도구")
    parser.add_argument("input_pdf", help="PDF 파일 경로")
    parser.add_argument("--dpi", type=int, default=200, help="렌더링 해상도 (기본: 200)")
    parser.add_argument("--pages", type=int, nargs="+", help="렌더링할 페이지 번호 (기본: 전체)")
    args = parser.parse_args()

    if not Path(args.input_pdf).exists():
        print(f"오류: 파일을 찾을 수 없습니다: {args.input_pdf}")
        sys.exit(1)

    render_pages(args.input_pdf, dpi=args.dpi, pages=args.pages)
