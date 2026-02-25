---
name: git-commit
description: Use when a feature, fix, or task has been completed and changes should be committed to git
---

# Git Commit 절차

## 커밋해야 할 타이밍
- 기능 하나가 완성됐을 때
- 버그 하나를 고쳤을 때
- 파일/폴더 구조를 변경했을 때
- 작업을 멈추고 자리를 뜰 때

## 절차
1. 변경된 파일 확인: `git status`
2. 변경 내용 확인: `git diff`
3. 스테이징: `git add .`
4. 커밋: `git commit -m "타입: 한국어 설명"`
5. 푸시: `git push`

## 커밋 메시지 형식
- `feat: 기능 추가 설명`
- `fix: 버그 수정 설명`
- `refactor: 코드 구조 변경`
- `docs: 문서 수정`
- `chore: 설정 파일 변경`

## 주의
- 커밋 전 반드시 `git status`로 의도치 않은 파일 포함 여부 확인
- `.env` 파일이 스테이징에 포함됐으면 즉시 제거: `git restore --staged .env`
- 커밋 메시지는 나중에 읽었을 때 무슨 작업인지 알 수 있게 작성
