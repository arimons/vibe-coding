#!/bin/zsh
# CLI의 강력함을 보여주는 배치 이미지 처리 스크립트

echo "🚀 이미지 워터마크 일괄 작업을 시작합니다..."

# 'test_image_'로 시작하고 '.jpg'로 끝나는 모든 파일에 대해 반복
for file in test_image_*.jpg
do
    # 이미 워터마크가 찍힌 파일은 건너뜀
    if [[ $file == watermarked_* ]]; then
        continue
    fi

    echo "🎨 처리 중: $file"
    ./.venv/bin/python3 apply_watermark.py "$file"
done

echo "✅ 모든 작업이 완료되었습니다!"
