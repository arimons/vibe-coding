#!/bin/bash
# 이미지 워터마크 일괄 처리 스크립트 (Mac / Linux)
# 사용법: bash apply_batch.sh

VENV_PYTHON="./.venv/bin/python3"

# 가상환경 활성화 확인
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ 가상환경이 없습니다. 먼저 아래 명령어를 실행하세요:"
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

echo "🚀 이미지 워터마크 일괄 작업을 시작합니다..."

count=0
for file in test_image_*.jpg; do
    [ -f "$file" ] || continue
    echo "🎨 처리 중: $file"
    "$VENV_PYTHON" apply_watermark.py "$file"
    count=$((count + 1))
done

echo ""
echo "✅ 완료! 총 ${count}개 파일을 처리했습니다."
