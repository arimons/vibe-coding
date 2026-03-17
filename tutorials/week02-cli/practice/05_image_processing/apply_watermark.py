import os
import sys
import platform
import argparse
from PIL import Image, ImageDraw, ImageFont


def get_font(size=50):
    """
    OS별로 사용 가능한 폰트를 찾아 반환합니다.
    없으면 기본 폰트로 폴백합니다.
    """
    system = platform.system()
    if system == "Windows":
        candidates = [
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/Arial.ttf",
            "C:/Windows/Fonts/malgun.ttf",
        ]
    elif system == "Darwin":  # macOS
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:  # Linux
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue

    return ImageFont.load_default()


def process_file(filepath, text="Confidential"):
    """
    단일 이미지 파일에 워터마크를 추가합니다.
    """
    if not os.path.exists(filepath):
        print(f"오류: 파일을 찾을 수 없습니다 - {filepath}")
        return

    try:
        with Image.open(filepath).convert("RGBA") as base:
            font = get_font(size=50)

            # 텍스트 크기 계산
            temp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
            if hasattr(temp_draw, "textbbox"):
                bbox = temp_draw.textbbox((0, 0), text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            else:
                w, h = temp_draw.textsize(text, font=font)

            # 텍스트 이미지 생성 (패딩 포함)
            pad_w, pad_h = int(w * 1.2), int(h * 1.5)
            text_img = Image.new("RGBA", (pad_w, pad_h), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text(
                ((pad_w - w) // 2, (pad_h - h) // 2),
                text,
                fill=(255, 255, 255, 60),
                font=font,
            )

            # 대각선 회전
            rotated_text = text_img.rotate(35, expand=1, resample=Image.BICUBIC)
            rw, rh = rotated_text.size

            # 3개 위치에 워터마크 합성 (좌상단, 중앙, 우하단)
            positions = [
                (base.width // 4 - rw // 2, base.height // 4 - rh // 2),
                (base.width // 2 - rw // 2, base.height // 2 - rh // 2),
                (3 * base.width // 4 - rw // 2, 3 * base.height // 4 - rh // 2),
            ]
            for pos in positions:
                base.paste(rotated_text, pos, rotated_text)

            # 저장
            dir_name = os.path.dirname(filepath)
            base_name = os.path.basename(filepath)
            output_path = os.path.join(dir_name, f"watermarked_{base_name}")
            base.convert("RGB").save(output_path, "JPEG", quality=90)
            print(f"완료: {base_name} → watermarked_{base_name}")

    except Exception as e:
        print(f"오류: {filepath} 처리 중 문제가 발생했습니다 - {e}")


def main():
    parser = argparse.ArgumentParser(
        description="이미지에 'Confidential' 워터마크를 추가합니다.",
        epilog="예시:\n"
               "  python apply_watermark.py test_image_1.jpg   # 파일 1개 처리\n"
               "  python apply_watermark.py all                 # 전체 처리",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "target",
        help='처리할 파일명 (예: test_image_1.jpg) 또는 "all" (폴더 내 전체 jpg 처리)',
    )
    parser.add_argument(
        "--text",
        default="Confidential",
        help='워터마크 텍스트 (기본값: "Confidential")',
    )
    args = parser.parse_args()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    if args.target.lower() == "all":
        files = sorted(
            f for f in os.listdir(current_dir)
            if f.lower().endswith(".jpg") and not f.startswith("watermarked_")
        )
        if not files:
            print("처리할 jpg 파일이 없습니다.")
            return
        print(f"총 {len(files)}개 파일을 처리합니다...")
        for f in files:
            process_file(os.path.join(current_dir, f), text=args.text)
        print("모든 처리가 완료됐습니다.")
    else:
        process_file(os.path.join(current_dir, args.target), text=args.text)


if __name__ == "__main__":
    main()
