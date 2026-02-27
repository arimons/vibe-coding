import os
import sys
from PIL import Image, ImageDraw, ImageFont

def process_file(filepath, text="Confidential"):
    """
    단일 이미지 파일에 워터마크를 추가합니다.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found - {filepath}")
        return

    try:
        with Image.open(filepath).convert("RGBA") as base:
            # 폰트 설정
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
            except:
                font = ImageFont.load_default()
            
            # 텍스트 레이어 생성을 위한 더미 draw
            temp_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
            
            # 텍스트 크기 계산 (패딩 추가로 잘림 방지)
            if hasattr(temp_draw, 'textbbox'):
                bbox = temp_draw.textbbox((0, 0), text, font=font)
                w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            else:
                w, h = temp_draw.textsize(text, font=font)
            
            # 텍스트 이미지를 위한 여유 공간 (패딩 20% 추가)
            pad_w, pad_h = int(w * 1.2), int(h * 1.5)
            text_img = Image.new("RGBA", (pad_w, pad_h), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            
            # 더 낮은 투명도 (60) 적용 및 중앙 정렬하여 그리기
            text_draw.text(((pad_w - w) // 2, (pad_h - h) // 2), text, fill=(255, 255, 255, 60), font=font)
            
            # 대각선 회전
            rotated_text = text_img.rotate(35, expand=1, resample=Image.BICUBIC)
            rw, rh = rotated_text.size
            
            # 3개의 워터마크 위치 설정 (좌상단, 중앙, 우하단)
            positions = [
                (base.width // 4 - rw // 2, base.height // 4 - rh // 2),
                (base.width // 2 - rw // 2, base.height // 2 - rh // 2),
                (3 * base.width // 4 - rw // 2, 3 * base.height // 4 - rh // 2)
            ]
            
            # 각 위치에 워터마크 합성
            for pos in positions:
                base.paste(rotated_text, pos, rotated_text)
            
            # 결과 저장
            dir_name = os.path.dirname(filepath)
            base_name = os.path.basename(filepath)
            output_path = os.path.join(dir_name, f"watermarked_{base_name}")
            
            base.convert("RGB").save(output_path, "JPEG", quality=90)
            print(f"Success: Upgraded watermark added to {base_name}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python apply_watermark.py <filename_or_all>")
        sys.exit(1)

    target = sys.argv[1]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if target.lower() == "all":
        # 폴더 내의 모든 jpg 파일 처리 (이미 워터마크가 찍힌 파일 제외)
        files = [f for f in os.listdir(current_dir) if f.lower().endswith(".jpg") and not f.startswith("watermarked_")]
        for f in files:
            process_file(os.path.join(current_dir, f))
    else:
        # 특정 파일 하나만 처리
        process_file(os.path.join(current_dir, target))
