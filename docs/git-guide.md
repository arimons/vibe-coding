---
layout: page
title: Git 초보자 가이드
nav_order: 3
---

# 초보자를 위한 Git 완전 가이드

## 🤔 Git을 왜 써야 할까요?

### 상황 1: Git 없이 코딩할 때
```
내_프로젝트_폴더/
├── main.py
├── main_백업.py
├── main_최종.py
├── main_진짜최종.py
├── main_진짜진짜최종.py
└── main_교수님께제출할파일.py
```
**문제점**: 어떤 파일이 최신인지 모르겠고, 무엇이 바뀌었는지도 모름 😵‍💫

### 상황 2: Git으로 코딩할 때
```
내_프로젝트_폴더/
├── main.py  (항상 최신 버전)
└── .git/    (모든 변경 히스토리가 숨겨진 폴더에)

Git 히스토리:
📝 v3: "버그 수정 완료" (2024-03-15)
📝 v2: "새로운 기능 추가" (2024-03-10) 
📝 v1: "프로젝트 시작" (2024-03-05)
```
**장점**: 파일은 하나뿐이지만 모든 변경 기록을 볼 수 있음! ✨

## ⚙️ Git 첫 설정 (한 번만 하면 됩니다!)

**git init 하기 전에 반드시 해야 할 설정이 있어요:**

### **사용자 정보 등록**
```bash
git config --global user.name "홍길동"
git config --global user.email "hong@example.com"
```

### **왜 필요한가요?**
- Git은 누가 언제 무엇을 바꿨는지 기록해둡니다
- 커밋할 때마다 "작성자 정보"가 함께 저장됩니다  
- 이 설정을 안 하면 첫 커밋할 때 오류가 납니다!

### **VS Code에서 설정하기**
```
1. 터미널 열기: Ctrl + `
2. 위 명령어 입력 (본인 정보로 변경)
3. 한 번만 하면 컴퓨터의 모든 프로젝트에서 사용됩니다
```

### **설정 완료 확인**
```bash
git config --list
# 또는
git config user.name    # 이름 확인
git config user.email   # 이메일 확인
```

---

## 🎯 Git을 써야 하는 이유

### 1. **타임머신 기능** ⏰
코드를 망쳤을 때 과거로 돌아갈 수 있어요
```python
# 어제 코드 (잘 작동했음)
def calculate(a, b):
    return a + b

# 오늘 코드 (망가짐)
def calculate(a, b):
    return a * b * unknown_function()  # 에러!
```
Git이 있으면: `git checkout` 명령어로 어제 코드로 즉시 복구!

### 2. **변경사항 추적** 🔍
"어디를 바꿨더라?"를 정확히 알 수 있어요
```diff
- print("Hello World")     # 삭제된 줄
+ print("안녕하세요!")      # 추가된 줄
```

### 3. **협업 필수** 👥
팀 프로젝트에서 다른 사람과 코드를 공유할 때 필수

### 4. **백업 효과** 💾
GitHub에 올려두면 컴퓨터가 고장나도 코드가 안전함

---

## 📥 Git 설치하기

### **Git 다운로드**
**공식 홈페이지**: https://git-scm.com/

Windows, macOS, Linux 모든 운영체제 지원

### **Windows 설치 시 주의사항**

#### **✅ 권장 설정 (Next만 눌러도 됨!)**
대부분의 설정은 기본값이 좋지만, 몇 가지만 확인하세요:

1. **Adjusting your PATH environment**
   - `Git from the command line and also from 3rd-party software` 선택 (기본값)
   - 이렇게 해야 VS Code에서 Git을 인식할 수 있어요

2. **Choosing HTTPS transport backend**
   - `Use the OpenSSL library` 선택 (기본값)

3. **Configuring the line ending conversions**
   - Windows: `Checkout Windows-style, commit Unix-style line endings` (기본값)
   - 다른 OS와 협업할 때 줄바꿈 문제를 자동으로 해결해줍니다

4. **Configuring the terminal emulator**
   - `Use Windows' default console window` 선택 (기본값)

#### **🚨 주의: 바꾸면 안 되는 설정**
- **기본 에디터**: 그냥 기본값 유지 (나중에 VS Code에서 사용할 거라서)
- **PATH 설정**: 반드시 기본값으로! (중요)

#### **설치 완료 확인**
```bash
# VS Code 터미널에서 확인
git --version
# 결과: git version 2.x.x (설치 성공!)
```

### **macOS 설치**
1. 공식 홈페이지에서 다운로드하거나
2. Homebrew 사용: `brew install git`
3. Xcode Command Line Tools: `xcode-select --install`

### **Linux 설치**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git

# CentOS/RHEL
sudo yum install git
```

---

## 🚀 Git 사용 단계별 과정

### **📋 첫 번째: 프로젝트 시작**
```
1. 새 프로젝트 폴더 생성
   ↓
2. git init (Git 저장소 초기화)
   ↓  
3. .gitignore 파일 생성 (중요!)
   ↓
4. git add .gitignore
   ↓
5. git commit -m "프로젝트 시작"
```

### **🔄 반복되는 개발 사이클**
```
1. 코드 작성/수정
   ↓
2. F5로 실행 테스트 (잘 작동하는지 확인)
   ↓
3. git add . (변경사항 스테이징)
   ↓
4. git commit -m "의미있는 메시지"
   ↓
5. 1번으로 돌아가서 다음 기능 개발...
```

### **🌐 GitHub 연동 (선택사항)**
```
로컬 작업 완료 후:
git push → GitHub 등 원격 저장소에 업로드
```

---

## 🏠 Git의 3개 공간 이해하기

Git을 이해하려면 먼저 **3개의 공간**을 알아야 해요!

### **1단계: 작업 폴더 (Working Directory)**
💡 **쉽게 말하면**: 내가 실제로 코딩하는 폴더

```
📁 내_프로젝트/
├── main.py      ← 내가 여기서 코드 수정
├── utils.py     ← 새로 만든 파일
└── README.md    ← 방금 고친 파일
```

**특징:**
- 평범한 폴더와 똑같아 보임
- 파일을 만들고, 수정하고, 삭제하는 곳
- Git이 "어? 뭔가 바뀌었네!" 하고 지켜보고 있음

### **2단계: 스테이징 영역 (Staging Area)**
💡 **쉽게 말하면**: "다음에 저장할 파일들을 모아두는 대기실"

**왜 필요할까?**
```
상황: 3개 파일을 수정했는데...
- main.py: 중요한 버그 수정 ✅ (저장하고 싶음)
- experiment.py: 실험용 코드 ❌ (아직 저장 안함)
- config.py: 완성된 새 기능 ✅ (저장하고 싶음)

해결: 스테이징으로 원하는 것만 선택!
git add main.py config.py  # 이 2개만 "저장 대기열"에 추가
```

**스테이징의 역할:**
- "다음 저장할 때 이것들만 포함시켜줘!"라고 Git에게 알려주는 것
- 마치 "장바구니"에 담는 것과 비슷함

### **3단계: Git 저장소 (Git Repository)**
💡 **쉽게 말하면**: "모든 변경 기록이 영구히 보관되는 금고"

```bash
git commit -m "버그 수정 완료"

결과: 
📚 Git 금고에 새 페이지 추가됨
├── 📄 v3: "버그 수정 완료" (2024-03-15) ← 새로 추가!
├── 📄 v2: "새 기능 추가" (2024-03-10)
└── 📄 v1: "프로젝트 시작" (2024-03-05)
```

**특징:**
- 한 번 저장되면 절대 사라지지 않음
- 언제든 과거 버전으로 돌아갈 수 있음
- "누가, 언제, 무엇을, 왜" 모든 정보가 기록됨

## 🎯 git add . 의 정확한 이해

### **`git add .` = "현재 폴더와 모든 하위 폴더의 변경사항을 스테이징"**

**중요**: Git은 **아무것도 자동으로 제외하지 않습니다!**

### **실제 예시:**
```
📁 내_프로젝트/
├── main.py               (수정됨)
├── experiment.py         (수정됨) ← 실험 파일도 포함됨!
├── new_feature.py        (새로 생성)
├── 📁 src/
│   ├── utils.py          (수정됨)
│   └── 📁 modules/
│       └── auth.py       (새로 생성)
├── 📁 venv/              (가상환경 폴더)
│   └── ...
└── 📁 __pycache__/       (Python 캐시)
    └── ...
```

### **`git add .` 실행 결과:**
```bash
🎭 스테이징:
✅ main.py
✅ experiment.py        ← 실험 파일도 스테이징됨!
✅ new_feature.py
✅ src/utils.py         ← 하위 폴더도 재귀적으로 포함
✅ src/modules/auth.py  ← 하위 폴더도 재귀적으로 포함
✅ venv/ (전체 폴더)   ← 가상환경도 포함됨! 😱
✅ __pycache__/        ← 캐시도 포함됨! 😱
```

## 🚨 .gitignore의 중요성

### **문제: 원하지 않는 파일들까지 포함됨**

**해결: .gitignore 파일 생성**
```bash
# .gitignore 내용
venv/
__pycache__/
*.pyc
.env
experiment.py    ← 실험 파일도 제외
temp/
*.log
```

### **이제 `git add .` 실행하면:**
```bash
🎭 스테이징:
✅ main.py
✅ new_feature.py
✅ src/utils.py
✅ src/modules/auth.py
❌ experiment.py     (ignored)
❌ venv/            (ignored)
❌ __pycache__/     (ignored)
```

## 🎯 올바른 워크플로우

### **프로젝트 시작 시 (필수!):**
```bash
git init
# .gitignore 파일 먼저 만들기! (GitHub 템플릿 사용 권장)
git add .gitignore
git commit -m "프로젝트 초기 설정: .gitignore 추가"
```

### **일반적인 개발 사이클:**
```bash
# 1. 코딩 작업
# 2. F5로 실행/테스트 (잘 작동하는지 확인)
# 3. 잘 작동하면 커밋
git add .                    # .gitignore로 자동 필터링됨
git commit -m "새 기능 추가"
```

## 💡 VS Code에서 Git 사용하기 - GUI로 보면 이렇게 생겼어요!

위에서 배운 Git 개념들이 VS Code에서는 어떻게 보이는지 알아봅시다!

### **Git 패널 열기**
```
왼쪽 사이드바 → Git 아이콘 (분기 모양) 클릭
또는 Ctrl + Shift + G
```

### **SOURCE CONTROL 패널 구성**
```
┌─ SOURCE CONTROL ──────────┐
│ ⚙️ CHANGES                │  ← git status와 동일
│   📄 main.py         M    │  ← Modified (수정됨)
│   📄 new_file.py     U    │  ← Untracked (새 파일)
│   📄 deleted.py      D    │  ← Deleted (삭제됨)
│                           │
│ 💬 Message (Ctrl+Enter...) │  ← 커밋 메시지 입력
│ ┌───────────────────────┐ │
│ │ 새 기능 추가           │ │
│ └───────────────────────┘ │
│                           │
│    ✅ Commit              │  ← git commit 실행
└───────────────────────────┘
```

### **VS Code GUI ↔ Git 명령어 연결**

#### **1. 파일 상태 확인**
```
VS Code 화면                   Git 명령어
─────────────                 ─────────────
📄 main.py    M               git status
📄 utils.py   U               (자동으로 실행됨)
📄 old.py     D               
```

#### **2. 스테이징 (무대에 올리기)**
```
VS Code 동작                   Git 명령어
─────────────                 ─────────────
Changes 옆 [+] 클릭      →     git add .
개별 파일 [+] 클릭       →     git add main.py
[-] 클릭 (스테이징 취소)  →     git reset main.py
```

#### **3. 커밋 (사진 촬영해서 앨범에 보관)**
```
VS Code 동작                   Git 명령어
─────────────                 ─────────────
메시지 입력 + Ctrl+Enter →     git commit -m "메시지"
[Commit] 버튼 클릭       →     git commit -m "메시지"
```

### **실제 워크플로우**
```
1. 코딩 작업 완료
   ↓
2. Git 패널에서 Changes 확인
   ↓  
3. [+] 버튼으로 스테이징
   ↓
4. 커밋 메시지 입력
   ↓
5. Ctrl+Enter 또는 [Commit] 클릭
   ↓
6. 완료! 🎉
```

**결론**: VS Code GUI는 결국 같은 Git 명령어를 더 편리하게 실행하는 것입니다!

## 💡 핵심 정리

### **Git의 철학:**
"개발자가 명시적으로 제외하라고 말하지 않으면 모든 파일을 추적한다"

### **올바른 접근:**
1. **.gitignore 먼저 설정** (venv, 캐시, 실험 파일 등 제외)
2. **git add . 사용** (자동으로 필터링됨)
3. **의미있는 단위로 커밋** (기능별, 버그 수정별)

### **실무 팁:**
- 📁 **샘플 데이터**: 프로젝트 외부 폴더에 저장 권장
- 🔧 **VS Code**: Git 패널 활용으로 시각적 관리
- 📋 **.gitignore**: GitHub 템플릿 또는 gitignore.io 활용

**핵심**: .gitignore로 원하지 않는 파일을 제외하고, git add .로 편리하게 관리하세요!

---

## 💡 실제 작업 흐름 예시

### 첫 번째 프로젝트 시작
```bash
# 1. 프로젝트 폴더에서 Git 시작
git init
# 메시지: "빈 Git repository 생성됨"

# 2. 첫 코드 작성 후
echo "print('Hello World')" > main.py

# 3. Git에 추가
git add main.py

# 4. 첫 번째 저장
git commit -m "프로젝트 시작: Hello World 출력"
```

### 기능 추가 작업
```bash
# 1. 코드 수정
echo "print('안녕하세요!')" > main.py

# 2. 변경사항 확인
git status  # "main.py가 수정됨"이라고 표시

# 3. 스테이징
git add main.py

# 4. 저장
git commit -m "인사말을 한국어로 변경"
```

### 히스토리 확인
```bash
git log --oneline

# 결과:
# a1b2c3d 인사말을 한국어로 변경
# e4f5g6h 프로젝트 시작: Hello World 출력
```

---

## 🏠 Local vs Remote (로컬 vs 원격)

### **Local Repository (로컬 저장소)**
```
내 컴퓨터 📱
├── 내_프로젝트/
│   ├── main.py
│   └── .git/  ← 여기에 모든 히스토리 저장
```
- 내 컴퓨터에만 있는 Git 저장소
- `git commit`까지는 여기에만 저장됨

### **Remote Repository (원격 저장소)**
```
GitHub 서버 ☁️
└── my-project/
    ├── main.py
    └── 모든 Git 히스토리
```
- 인터넷상의 Git 저장소 (GitHub, GitLab 등)
- `git push`로 로컬 내용을 원격에 업로드

### **동기화 과정**
```bash
# 로컬 → 원격 (업로드)
git push origin main

# 원격 → 로컬 (다운로드)
git pull origin main
```

---

## 🎯 VS Code에서 Git 사용하기

### **Git 상태 확인**
VS Code에서 파일 옆에 표시되는 아이콘들:
- `M` (Modified): 수정됨
- `U` (Untracked): 새로 만든 파일
- `A` (Added): 스테이징됨

### **VS Code Git 패널**
1. 왼쪽 사이드바에서 Git 아이콘 클릭
2. 변경된 파일들 목록 표시
3. `+` 버튼으로 `git add`
4. 메시지 작성 후 `Ctrl+Enter`로 `git commit`

### **내장 터미널 사용**
```bash
# VS Code 내장 터미널에서 Git 명령어 사용 가능
Ctrl + ` (백틱)으로 터미널 열기
```

---

## 🔧 초보자 필수 Git 명령어

### **기본 설정 (맨 처음 한 번만)**
```bash
git config --global user.name "내이름"
git config --global user.email "내이메일@gmail.com"
```

### **자주 사용하는 명령어**
```bash
git init          # Git 시작
git status        # 현재 상태 확인
git add .         # 모든 변경사항 스테이징
git commit -m "메시지"  # 저장
git log           # 히스토리 보기
git push          # 원격 저장소에 업로드
git pull          # 원격 저장소에서 다운로드
```

---

## 🎉 요약: Git을 써야 하는 이유

1. **파일 관리가 깔끔해짐** - 백업파일 지옥 탈출
2. **실수해도 안전함** - 언제든 과거로 돌아갈 수 있음
3. **변경사항 추적** - 무엇을 언제 바꿨는지 정확히 알 수 있음
4. **협업 필수** - 팀 프로젝트에서 반드시 필요
5. **포트폴리오 구축** - GitHub에 내 코드를 멋지게 전시

**초보자 권장 학습 순서:**
1. `git init`, `git add`, `git commit` 익히기
2. VS Code Git 패널 사용해보기
3. GitHub 연동해보기 (`git push`)
4. 협업 기능은 나중에 (브랜치, 머지 등)

Git은 처음엔 복잡해 보이지만, 한 번 익히면 코딩할 때 없어서는 안 될 도구가 됩니다!