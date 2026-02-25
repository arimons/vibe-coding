---
name: debug-workflow
description: Use when an error or exception occurs during code execution
---

# 에러 디버깅 절차

## 순서
1. 에러 메시지 전체 읽기 (마지막 줄이 핵심)
2. 어느 파일, 몇 번째 줄인지 확인
3. 에러 종류별 1차 점검:
   - `ModuleNotFoundError` → `pip install` 누락
   - `FileNotFoundError` → 경로 확인
   - `KeyError` → 딕셔너리 키 존재 여부 확인
   - `IndentationError` → 들여쓰기 확인
   - `TypeError` → 변수 타입 확인
4. 위로 해결 안 되면 에러 메시지 그대로 검색

## 금지
- 에러 원인 파악 전 코드 임의 수정 금지
- 여러 곳 동시 수정 금지 (원인 파악이 어려워짐)

## 응답 형식
에러 분석 시 반드시 아래 형식으로 설명:
- **원인**: 왜 발생했는지
- **해결**: 어떻게 고치는지
- **예방**: 다음에 어떻게 방지하는지
