#!/bin/bash
# Antigravity 설정 설치 스크립트
# 사용법: bash install.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GEMINI_DIR="$HOME/.gemini"
ANTIGRAVITY_DIR="$GEMINI_DIR/antigravity"

echo "🚀 Antigravity 설정 설치를 시작합니다..."

# 1. 폴더 생성
mkdir -p "$ANTIGRAVITY_DIR/skills"

# 2. GEMINI.md (Global Rules)
if [ -f "$GEMINI_DIR/GEMINI.md" ]; then
  echo "⚠️  GEMINI.md 가 이미 존재합니다. 덮어쓰시겠습니까? (y/n)"
  read -r answer
  if [ "$answer" = "y" ]; then
    cp "$SCRIPT_DIR/GEMINI.md" "$GEMINI_DIR/GEMINI.md"
    echo "✅ GEMINI.md 설치 완료"
  else
    echo "⏭️  GEMINI.md 건너뜀"
  fi
else
  cp "$SCRIPT_DIR/GEMINI.md" "$GEMINI_DIR/GEMINI.md"
  echo "✅ GEMINI.md 설치 완료"
fi

# 3. mcp_config.json
if [ -f "$ANTIGRAVITY_DIR/mcp_config.json" ]; then
  echo "⚠️  mcp_config.json 이 이미 존재합니다. 덮어쓰시겠습니까? (y/n)"
  read -r answer
  if [ "$answer" = "y" ]; then
    cp "$SCRIPT_DIR/mcp_config.json" "$ANTIGRAVITY_DIR/mcp_config.json"
    echo "✅ mcp_config.json 설치 완료"
  else
    echo "⏭️  mcp_config.json 건너뜀"
  fi
else
  cp "$SCRIPT_DIR/mcp_config.json" "$ANTIGRAVITY_DIR/mcp_config.json"
  echo "✅ mcp_config.json 설치 완료"
fi

# 4. Skills 복사
for skill_dir in "$SCRIPT_DIR/skills"/*/; do
  skill_name=$(basename "$skill_dir")
  target="$ANTIGRAVITY_DIR/skills/$skill_name"
  mkdir -p "$target"
  cp -r "$skill_dir/." "$target/"
  echo "✅ Skills/$skill_name 설치 완료"
done

echo ""
echo "🎉 설치 완료! Antigravity를 재시작해주세요."
