---
layout: page
title: Git + Syncthing 다중 PC 운용 가이드
nav_exclude: true
---


> 회사PC(Windows), 맥북, 맥미니(집) 3대에서 Syncthing으로 파일을 공유하면서
> GitHub으로 버전 관리할 때 발생하는 문제와 해결법.

---

## 왜 꼬이는가

Syncthing과 Git은 둘 다 "파일 동기화"를 하지만 방식이 다르다.

```
Syncthing: 파일 내용을 기기 간에 실시간 복사
Git:       커밋(스냅샷) 단위로 히스토리를 관리
```

`.git/` 폴더는 Syncthing이 제외하도록 설정되어 있다 (`.syncignore`에 `// Git` 섹션).
즉, **파일 내용은 동기화되지만 git 히스토리는 각 기기마다 독립적**이다.

### 충돌이 생기는 패턴

```
[맥미니] 작업 → commit → push → origin/main 업데이트
                              ↓
                      Syncthing이 파일 내용을 맥북에 복사
                              ↓
[맥북] git 입장에서는 "로컬에서 파일이 수정된 것"으로 인식
        ↓
      commit → push 시도 → origin과 히스토리가 달라서 거부 (diverged)
```

---

## 핵심 개념 정리

### git stash — 변경사항을 임시 보관

작업 중인 파일을 커밋하지 않고 잠깐 서랍에 넣어두는 기능.

```
작업 폴더 상태:  main.py (수정됨), config.py (수정됨)
                      ↓ git stash
서랍(stash):     main.py, config.py 보관됨
작업 폴더:       깨끗한 상태 (마지막 커밋 기준)
                      ↓ git stash pop
작업 폴더 상태:  main.py, config.py 복원됨
```

**언제 쓰나**: rebase, pull 등 git 작업 전에 "잠깐 치워두기"

```bash
git stash          # 서랍에 넣기
git stash list     # 서랍 목록 보기
git stash pop      # 서랍에서 꺼내기 (최근 것)
git stash drop     # 서랍 내용 버리기
```

### git rebase — 커밋을 다른 위치에 재배치

로컬에서 만든 커밋들을 origin 최신 커밋 위에 올려붙이는 작업.

```
rebase 전:
  [공통 조상] ─→ [origin: A, B, C, D ...33개]
                   └─→ [로컬: X, Y, Z ...3개]  ← 여기서 갈라짐

rebase 후:
  [공통 조상] ─→ [origin: A, B, C, D ...33개] ─→ [로컬: X, Y, Z]
```

merge와의 차이: merge는 두 히스토리를 합치는 "합류 커밋"을 만들지만,
rebase는 로컬 커밋을 origin 위에 깔끔하게 일렬로 재배치한다.

### diverged (히스토리 분기) — 꼬인 상태

```bash
# 이 메시지가 뜨면 diverged 상태
현재 브랜치와 'origin/main'이(가) 갈라졌습니다,
다른 커밋이 각각 3개와 33개 있습니다.
```

```
        ┌→ origin: 33커밋 (다른 PC에서 push한 것들)
[공통]──┤
        └→ 로컬:   3커밋  (이 PC에서 커밋한 것들)
```

원인: 다른 PC에서 push한 내용을 pull하기 전에 이 PC에서 커밋했기 때문.

---

## 오늘 발생한 상황과 해결 과정 (2025-04-09)

### 상황

- 맥미니(집)에서 5~6주차 매뉴얼 수정 후 commit + push
- 맥북은 pull을 안 한 상태에서 Syncthing이 파일만 복사해옴
- 맥북에서 commit 3개 생성 → origin과 33개 차이로 diverged

### 해결 순서

**1. 백업 브랜치 생성**
```bash
git branch backup-local-0409
```

**2. untracked 파일 문제 — git add 먼저**

rebase 전에 Syncthing이 가져온 untracked 파일들을 git이 인식하게 해야 한다.
```bash
git add .
```

**3. stash로 임시 보관**

add 후에도 "uncommitted changes" 오류가 나면 stash:
```bash
git stash
```

**4. rebase 실행**
```bash
git fetch origin
git rebase origin/main
```

**5. push**
```bash
git push origin main
```

**6. stash 정리**

pop이 필요한지 확인: 작업 폴더가 이미 깨끗하면 pop 불필요.
stash 내용이 rebase로 이미 반영된 경우 버려도 된다.
```bash
git stash list           # stash 목록 확인
git stash drop stash@{0} # 필요없으면 버리기 (목록 수만큼 반복)
```

---

## 재발 방지: 올바른 작업 순서

### 다른 PC에서 작업 후 이 PC에서 시작할 때

```bash
git pull origin main   # 반드시 먼저!
# 그 다음 작업 시작
```

Syncthing이 파일 내용을 이미 가져왔더라도 git pull은 별도로 해야 한다.
Syncthing = 파일 복사, git pull = 히스토리 동기화. 둘은 다른 작업이다.

### 작업 완료 후

```bash
git add .
git commit -m "작업 내용"
git push origin main   # 바로 push. 다른 PC에서 작업 시작 전에 pull하게
```

---

## 자주 나오는 오류 메시지

| 오류 | 원인 | 해결 |
|------|------|------|
| `rebase 할 수 없습니다: 스테이징하지 않은 변경 사항이 있습니다` | 수정된 파일 있음 | `git stash` |
| `인덱스에 커밋하지 않은 변경 사항이 있습니다` | staged 파일 있음 | `git stash` |
| `추적하지 않는 파일을 덮어씁니다` | untracked 파일이 origin 파일과 충돌 | `git add .` 후 `git stash` |
| `브랜치가 갈라졌습니다` | diverged 상태 | `git rebase origin/main` |
| `Updates were rejected` | push 거부 (diverged) | `git pull --rebase` 또는 rebase 후 push |

---

## 요약 한 줄

> Syncthing은 파일을 복사하고, Git은 히스토리를 관리한다.  
> **다른 PC 작업 후 시작할 때 항상 `git pull` 먼저.**
