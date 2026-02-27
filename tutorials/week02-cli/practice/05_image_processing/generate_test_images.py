import os
import random
from PIL import Image, ImageDraw, ImageFont

def create_images(output_dir, count=10):
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(1, count + 1):
        # 640x480, random background
        bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        img = Image.new('RGB', (640, 480), color=bg_color)
        
        draw = ImageDraw.Draw(img)
        text = f"Photo #{i}"
        
        # Try to load a font, fallback to default if not found
        try:
            # macOS default font path
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (center)
        if hasattr(draw, 'textbbox'):
            bbox = draw.textbbox((0, 0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        else:
            w, h = draw.textsize(text, font=font)
            
        x = (640 - w) / 2
        y = (480 - h) / 2
        
        draw.text((x, y), text, fill="white", font=font)
        
        filename = f"test_image_{i}.jpg"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath, "JPEG")
        print(f"Created {filename}")

if __name__ == "__main__":
    output = "/Users/changhyunpark/Developer/vibe-coding/tutorials/week02-cli/practice/05_image_processing"
    create_images(output)
