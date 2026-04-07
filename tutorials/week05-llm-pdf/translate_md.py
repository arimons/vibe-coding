"""
Markdown 학술 논문 번역 스크립트 (영어 → 한국어)

사용법:
    python translate_md.py input.md
    python translate_md.py input.md output_ko.md

출력:
    output_ko.md   (번역된 Markdown, 기본값: input 파일과 같은 폴더)
    output_ko.docx (pandoc 변환)
"""

import sys
import os
import re
import json
import argparse
import subprocess
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("오류: .env 파일에 GEMINI_API_KEY가 설정되어 있지 않습니다.")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3.1-flash-lite-preview"

# 용어집 추출에 보낼 최대 텍스트 길이 (토큰 절약)
GLOSSARY_MAX_CHARS = 80_000


# ──────────────────────────────────────────────
# 수식 후처리 (깨진 LaTeX 패턴 교정)
# ──────────────────────────────────────────────

# 자주 깨지는 패턴 → 교정 규칙
MATH_FIX_PATTERNS = [
    # \text{μm} → \mu\text{m} 또는 μm 그대로
    (r'\$\\text\{μ\}\\text\{m\}\$', r'$\\mu$m'),
    (r'\$\\text\{μm\}\$',           r'$\\mu$m'),
    # $ 사이에 공백 없는 단위 처리: $μm$ → $\mu\text{m}$
    (r'\$μm\$',   r'$\\mu\\text{m}$'),
    (r'\$μ([A-Za-z])\$', r'$\\mu\\text{\1}$'),
    # \text{} 안에 숫자+단위 혼재: $\text{10 nm}$ → 10 nm
    (r'\$\\text\{(\d[\d\s\w]*)\}\$', r'\1'),
]

def fix_math_equations(text: str) -> str:
    for pattern, replacement in MATH_FIX_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text


# ──────────────────────────────────────────────
# 1단계: 전체 텍스트에서 용어집 추출
# ──────────────────────────────────────────────

GLOSSARY_PROMPT = """다음은 학술 논문 전체 내용입니다. 번역 일관성을 위해 아래 항목들을 JSON으로 추출하세요.

출력 형식 (JSON만, 추가 설명 없이):
{
  "keep_english": [
    "TiO2", "PEDOT:PSS", "PCE", "μm"
  ],
  "translate_with_note": {
    "power conversion efficiency": "전력변환효율(PCE)",
    "external quantum efficiency": "외부양자효율(EQE)"
  }
}

추출 기준:
- keep_english: 화학식, 물질명, 측정 단위, 고유 약어, 모델명 등 번역 없이 영문 유지할 것
- translate_with_note: 처음 등장 시 한국어(영어) 병기가 필요한 핵심 기술 용어
- 중국어·일본어 표현은 해당 의미의 영문명으로 변환해서 포함할 것

논문 내용:
"""

def extract_glossary(full_text: str) -> dict:
    """논문 전체에서 용어집을 추출해서 dict로 반환."""
    # 너무 길면 앞부분만 사용 (abstract + introduction 위주)
    truncated = full_text[:GLOSSARY_MAX_CHARS]

    print("1단계: 용어집 추출 중...")
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[GLOSSARY_PROMPT + truncated],
    )
    raw = response.text.strip()

    # 코드블록 래퍼 제거
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    try:
        glossary = json.loads(raw)
        keep = glossary.get("keep_english", [])
        translate = glossary.get("translate_with_note", {})
        print(f"  → 영문 유지 {len(keep)}개, 병기 번역 {len(translate)}개 추출")
        return glossary
    except json.JSONDecodeError:
        print("  [경고] 용어집 파싱 실패 — 빈 용어집으로 진행")
        return {"keep_english": [], "translate_with_note": {}}


# ──────────────────────────────────────────────
# 2단계: 페이지별 번역 (용어집 컨텍스트 포함)
# ──────────────────────────────────────────────

def build_translation_prompt(glossary: dict, extra_instructions: str = "") -> str:
    keep = ", ".join(glossary.get("keep_english", [])[:60])  # 너무 길지 않게
    translate_pairs = "\n".join(
        f"  - {k} → {v}"
        for k, v in list(glossary.get("translate_with_note", {}).items())[:40]
    )
    extra_section = (
        f"\n## 추가 번역 지침 (우선 적용)\n{extra_instructions.strip()}\n"
        if extra_instructions.strip() else ""
    )
    return f"""당신은 학술 논문 번역 전문가입니다. 아래 규칙을 반드시 따라 영어 Markdown을 한국어로 번역하세요.

## 이 논문 확정 용어집

**영문 유지 (번역 금지):**
{keep}

**한국어(영어) 병기:**
{translate_pairs}

## 번역 규칙

1. **영문 유지**: 화학식·물질명·측정 단위(μm, nm, eV, GPa, wt% 등)·약어·Figure/Table/Eq. 참조
2. **병기**: 위 목록의 핵심 용어는 처음 등장 시 "한국어(English)" 형식, 이후에는 한국어만
3. **문장 번역**: 나머지 모든 문장은 학술 논문체 한국어 (합니다/됩니다 체)
4. **중국어·일본어**: 중국어(한자)나 일본어가 나오면 해당 의미에 맞는 한국어 또는 영문 통용명으로 번역할 것 (원문 그대로 남기지 말 것)
5. **수식 보존**: $...$ 및 $$...$$ LaTeX 수식은 내용·공백 포함 절대 수정하지 말 것
6. **Markdown 보존**: #, |, -, *, ![](…), --- 등 Markdown 구조 그대로 유지
7. **페이지 구분선**: --- 단독 줄은 그대로 유지
{extra_section}
추가 설명 없이 번역된 Markdown만 출력할 것.

번역할 내용:
"""

def translate_page(page_text: str, prompt_prefix: str) -> str:
    """단일 페이지 텍스트를 번역."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt_prefix + page_text],
    )
    return response.text.strip()


# ──────────────────────────────────────────────
# 메인 파이프라인
# ──────────────────────────────────────────────

def translate_md(input_md: str, output_md: str, extra_instructions: str = ""):
    input_path = Path(input_md)
    output_path = Path(output_md)

    full_text = input_path.read_text(encoding="utf-8")

    # 페이지 구분선으로 분리
    pages = re.split(r'\n\n---\n\n', full_text)
    total = len(pages)
    print(f"총 {total}페이지 번역 시작: {input_path.name}")
    if extra_instructions.strip():
        print(f"추가 지침 적용: {extra_instructions[:80]}{'...' if len(extra_instructions) > 80 else ''}")

    # ── 1단계: 용어집 추출
    glossary = extract_glossary(full_text)
    translation_prompt = build_translation_prompt(glossary, extra_instructions)

    # ── 2단계: 페이지별 번역
    translated_pages = []
    for i, page in enumerate(pages, 1):
        print(f"페이지 {i}/{total} 번역 중...")

        if not page.strip():
            translated_pages.append(page)
            continue

        try:
            translated = translate_page(page, translation_prompt)
            # 수식 후처리
            translated = fix_math_equations(translated)
            translated_pages.append(translated)
        except Exception as e:
            print(f"  [오류] 페이지 {i} 번역 실패, 원문 유지: {e}")
            translated_pages.append(page)

    # ── Markdown 저장
    full_translated = "\n\n---\n\n".join(translated_pages)
    output_path.write_text(full_translated, encoding="utf-8")
    print(f"\nMarkdown 저장 완료: {output_path}")

    # ── pandoc으로 DOCX 변환
    docx_path = output_path.with_suffix(".docx")
    print("DOCX 변환 중 (pandoc)...")
    try:
        cmd = ["pandoc", output_path.name, "-o", docx_path.name]
        # template.docx가 프로젝트 루트에 있으면 자동 적용
        template = Path("template.docx")
        if template.exists():
            cmd += [f"--reference-doc={template.resolve()}"]
            print(f"  템플릿 적용: {template}")
        subprocess.run(
            cmd,
            cwd=str(output_path.parent),   # md 파일 위치에서 실행 → 상대경로 이미지 정상 인식
            check=True, capture_output=True, text=True,
        )
        print(f"DOCX 저장 완료: {docx_path}")
    except FileNotFoundError:
        print("  [오류] pandoc 미설치. `brew install pandoc` 으로 설치하세요.")
    except subprocess.CalledProcessError as e:
        print(f"  [오류] pandoc 변환 실패: {e.stderr}")

    print("\n완료!")
    print(f"  번역 MD : {output_path}")
    print(f"  번역 DOCX: {docx_path}")


# ──────────────────────────────────────────────
# CLI 진입점
# ──────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Markdown 학술 논문 번역 (영어 → 한국어)"
    )
    parser.add_argument("input_md", help="번역할 Markdown 파일 경로")
    parser.add_argument("output_md", nargs="?", help="출력 파일 경로 (기본: input_ko.md)")
    parser.add_argument(
        "--instructions", default="",
        help="추가 번역 지침 (프롬프트에 우선 적용)"
    )
    args = parser.parse_args()

    if not Path(args.input_md).exists():
        print(f"오류: 파일을 찾을 수 없습니다: {args.input_md}")
        sys.exit(1)

    if args.output_md:
        output_md = args.output_md
    else:
        p = Path(args.input_md)
        output_md = str(p.parent / (p.stem + "_ko.md"))

    translate_md(args.input_md, output_md, extra_instructions=args.instructions)
