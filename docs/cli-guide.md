---
layout: page
title: CLI 기초 가이드
nav_order: 4
---

# 🖥️ 초보자를 위한 CLI 기초 가이드

## 왜 터미널을 배워야 할까요?

코딩 강의에서 "이 명령어 복사해서 붙여넣으세요"라고만 하면, 에러가 났을 때 스스로 해결할 수 없게 됩니다. 터미널은 컴퓨터와 대화하는 또 다른 방법이에요. 마우스 클릭 대신 문자로 명령을 내리는 것이죠. 처음엔 어색하지만, 익숙해지면 훨씬 빠르고 정확하게 작업할 수 있습니다.

---

## 1️⃣ 터미널의 기본 개념

### 프롬프트(Prompt) 읽기
터미널을 열면 이런 게 보입니다:
```
C:\Users\amore\Desktop>
```

이건 "지금 여기 있어요"라고 컴퓨터가 알려주는 거예요. 마치 "현재 바탕화면 폴더에 있습니다"라고 말하는 것과 같죠.

### 경로(Path)의 개념
- **절대경로**: 집 주소처럼 완전한 경로 → `C:\Users\amore\Desktop\my_project`
- **상대경로**: "여기서 두 칸 앞"처럼 현재 위치 기준 → `./my_project` 또는 `../Desktop`

`.`은 "현재 위치", `..`은 "한 단계 위 폴더"를 의미합니다.

---

## 2️⃣ 필수 네비게이션 명령어

### `pwd` - Print Working Directory
**어원**: "현재 작업 중인 디렉토리를 출력해줘"  
**상황**: "내가 지금 어디 있지?" 싶을 때

```bash
pwd
# 출력 예: C:\Users\amore\Desktop\vibe_coding
```

길을 잃었을 때 GPS로 현재 위치 확인하는 것처럼, 지금 터미널이 어느 폴더를 바라보고 있는지 알려줍니다.

---

### `ls` - List
**어원**: "리스트를 보여줘"  
**상황**: "이 폴더 안에 뭐가 있지?" 할 때

```bash
ls
# 출력: main.py  requirements.txt  data/  venv/

ls -l
# 파일 크기, 수정 날짜까지 자세히 보기

ls -a
# 숨김 파일(.env, .git 등)도 모두 보기

ls *.py
# .py로 끝나는 파일만 보기
```

탐색기에서 폴더 열어보는 것과 똑같은데, 문자로 보는 거예요. `-l`이나 `-a` 같은 게 **플래그(flag)**인데, 이건 뒤에서 자세히 설명할게요.

#### 💡 팁: 와일드카드 (Wildcard)

`*`와 `?`는 **와일드카드**라고 부르는 특수 문자입니다. 여러 파일을 한 번에 지정할 때 씁니다.

**`*` (별표)**: "아무 문자나 여러 개"를 의미
```bash
ls *.py          # .py로 끝나는 모든 파일
ls test*         # test로 시작하는 모든 파일
ls *config*      # 이름에 config가 들어간 모든 파일
rm *.txt         # 모든 txt 파일 삭제
```

**`?` (물음표)**: "아무 문자나 정확히 한 개"를 의미
```bash
ls test?.py      # test1.py, testA.py 등 (test 뒤에 문자 하나)
ls data_????.csv # data_2024.csv, data_0101.csv 등 (정확히 4글자)
```

**조합 사용**:
```bash
ls test[123].py  # test1.py, test2.py, test3.py만
ls file_2024*.txt # file_2024로 시작하는 모든 txt 파일
```

**비유**: 카드게임의 조커처럼 "무엇이든 될 수 있는" 자리 표시자입니다.

---

### `cd` - Change Directory
**어원**: "디렉토리를 바꿔줘"  
**상황**: 다른 폴더로 이동할 때

```bash
cd Desktop
# Desktop 폴더로 들어가기

cd ..
# 한 단계 위 폴더로 나가기

cd ../..
# 두 단계 위로

cd ~
# 홈 폴더로 (C:\Users\amore)

cd "Program Files"
# 공백이 있는 폴더명은 따옴표 필수!
```

**실전 예시**: 프로젝트 폴더가 `Desktop/my_project`에 있다면
```bash
cd Desktop
cd my_project
# 또는 한 번에: cd Desktop/my_project
```

#### 💡 팁: Tab 키로 자동완성

타이핑 중간에 `Tab`을 누르면 자동으로 완성됩니다. **초보자에게 가장 중요한 기능!**

```bash
cd Desk[Tab 누르기]
# → cd Desktop/

cd my_pro[Tab]
# → cd my_project/

python mai[Tab]
# → python main.py
```

**장점**:
- 타이핑 시간 절약
- 오타 방지
- 긴 파일명도 쉽게 입력
- 존재하지 않는 파일/폴더는 완성 안 됨 (철자 확인 가능)

**여러 개가 일치할 때**: Tab을 두 번 누르면 후보 목록이 나옵니다.
```bash
cd D[Tab][Tab]
# Desktop/  Documents/  Downloads/
```

---

## 3️⃣ 파일과 폴더 다루기

### `mkdir` - Make Directory
**어원**: "디렉토리를 만들어줘"  
**상황**: 새 프로젝트 폴더를 만들 때

```bash
mkdir weather_app
# weather_app 폴더 생성

mkdir -p parent/child/grandchild
# 중첩된 폴더를 한 번에 만들기
# -p 플래그: 부모 폴더가 없어도 알아서 만들어줌
```

마우스 우클릭 → "새 폴더"와 같은 기능이에요.

---

### `rm` - Remove
**어원**: "제거해줘"  
**상황**: 파일이나 폴더 삭제할 때

```bash
rm test.py
# test.py 파일 삭제

rm -r old_project
# 폴더와 그 안의 모든 내용 삭제
# -r (recursive): 재귀적으로, 즉 안에 있는 것까지 전부

rm -rf backup
# -f (force): 강제로, 확인 안 받고 바로 삭제
```

⚠️ **주의**: 휴지통으로 안 가고 바로 삭제됩니다! 복구 불가능하니 조심하세요.

---

### `cp` - Copy
**어원**: "복사해줘"  
**상황**: 파일 백업할 때

```bash
cp main.py main_backup.py
# main.py를 복사해서 main_backup.py로 저장

cp -r project1 project2
# 폴더 전체 복사 (-r 필수)
```

---

### `mv` - Move
**어원**: "옮겨줘"  
**상황**: 파일 이동하거나 이름 바꿀 때

```bash
mv old_name.py new_name.py
# 파일 이름 변경

mv test.py ../
# 파일을 상위 폴더로 이동

mv *.txt backup/
# 모든 txt 파일을 backup 폴더로 이동
```

---

### `cat` - Concatenate
**어원**: "연결해서 보여줘" (원래는 파일 여러 개를 이어붙이는 기능)  
**상황**: 파일 내용을 빠르게 확인할 때

```bash
cat requirements.txt
# 파일 내용을 터미널에 바로 출력

cat main.py config.py
# 여러 파일을 이어서 보기
```

메모장으로 파일 열어보는 것보다 훨씬 빠르죠. 특히 간단한 설정 파일이나 로그 확인할 때 유용합니다.

---

## 4️⃣ 환경변수(Environment Variables)란?

### 환경변수의 개념

프로그램이 실행될 때 필요한 **설정값을 미리 저장해두는 공간**입니다.

**비유**: 집에 메모를 붙여놓는 것과 비슷해요.
- "택배는 현관 앞에 놔주세요" ← `DELIVERY_LOCATION=front_door`
- "비밀번호는 1234" ← `PASSWORD=1234`

프로그램은 이 메모를 보고 필요한 정보를 가져다 씁니다.

### 왜 환경변수를 쓸까요?

1. **보안**: API 키 같은 민감한 정보를 코드에 직접 쓰면 GitHub에 올렸을 때 노출됨
2. **유연성**: 개발/운영 환경별로 다른 설정을 쉽게 적용

### API 키(API Key)란?

**비유**: API 키는 건물의 **출입증**과 같습니다.
- OpenAI, Google Maps 같은 서비스를 사용하려면 "당신이 허가받은 사용자"임을 증명해야 함
- API 키 = "제 이름은 amore이고, 저는 이 서비스를 쓸 권한이 있습니다"라는 증명서
- 남에게 보여주면 그 사람이 당신 이름으로 서비스를 쓸 수 있음 (비용 청구!)
- 그래서 `.env` 파일(숨김)에 넣고, Git에는 절대 올리면 안 됨

**예시**:
```
일반 코드에 직접: ❌ "출입증 번호를 옷에 써서 돌아다니기"
.env 파일 사용: ✅ "출입증을 지갑 안쪽에 숨겨서 다니기"
```

### 환경변수 설정하기 (임시)

**현재 터미널 세션에만** 적용되는 방법:

```bash
# PowerShell
$env:API_KEY = "your_secret_key_here"

# 확인
echo $env:API_KEY
```

터미널을 닫으면 사라집니다. 그래서 보통 파일로 저장해서 씁니다.

---

### `.env` 파일이란?

환경변수를 **파일로 저장**해두는 방식입니다. 

**점(`.`)으로 시작하는 이유**: Unix/Linux 시스템에서 `.`으로 시작하는 파일은 **숨김 파일**입니다. `ls` 명령어로는 안 보이고, `ls -a`로만 보입니다. 설정 파일에는 민감한 정보(비밀번호, API 키 등)가 들어가는 경우가 많아서, 실수로 공유되거나 노출되지 않도록 숨김 처리하려고 점을 붙이는 관례가 생겼습니다.

```bash
# .env 파일 내용
API_KEY=sk-abcd1234efgh5678
DB_HOST=localhost
DB_PORT=5432
DEBUG=True
```

Python에서는 `python-dotenv` 라이브러리로 이 파일을 읽어서 환경변수로 만듭니다:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일 읽기
api_key = os.getenv('API_KEY')  # 환경변수 가져오기
```

⚠️ `.env` 파일은 **절대 Git에 올리면 안 됩니다**! `.gitignore`에 꼭 추가하세요.

---

## 5️⃣ 리다이렉션과 파이프

### `>` - 리다이렉션 (Redirection)

**의미**: "출력을 파일로 보내줘" (덮어쓰기)

```bash
echo "Hello World" > test.txt
# "Hello World"를 test.txt에 저장 (파일이 없으면 생성)

ls > file_list.txt
# 현재 폴더의 파일 목록을 file_list.txt에 저장
```

**주의**: 기존 파일이 있으면 **내용이 완전히 사라지고** 새 내용으로 대체됩니다.

---

### `>>` - Append (추가)

**의미**: "출력을 파일 끝에 추가해줘"

```bash
echo "First line" > log.txt
echo "Second line" >> log.txt
echo "Third line" >> log.txt

cat log.txt
# 출력:
# First line
# Second line
# Third line
```

기존 내용을 지우지 않고 밑에 계속 추가됩니다. 로그 파일 만들 때 유용해요.

---

### `|` - 파이프 (Pipe)

**의미**: "왼쪽 명령의 출력을 오른쪽 명령의 입력으로 보내줘"

```bash
ls | grep ".py"
# ls의 결과에서 ".py"가 포함된 줄만 필터링

cat log.txt | wc -l
# log.txt의 줄 수를 세기
```

**비유**: 공장 컨베이어 벨트처럼 데이터를 다음 단계로 전달하는 겁니다.

---

### `<<` - Here Document (EOF)

**의미**: "여러 줄을 입력으로 넘겨줘"

Claude Code에서 자주 보셨을 `EOF`가 이겁니다:

```bash
cat << EOF > config.yaml
database:
  host: localhost
  port: 5432
user:
  name: admin
EOF
```

**설명**:
- `<< EOF`: "EOF를 만날 때까지의 모든 줄을 입력으로 받아"
- `> config.yaml`: "그걸 config.yaml 파일로 저장해"
- `EOF`: "여기까지!" (End Of File의 약자)

여러 줄짜리 파일을 터미널에서 바로 만들 때 편리합니다. `EOF` 대신 다른 단어(`END`, `STOP` 등)를 써도 되는데, 관례적으로 `EOF`를 많이 씁니다.

---

## 6️⃣ 플래그(Flag)와 옵션

### 플래그란?

명령어에 붙이는 **추가 옵션**입니다. 요리할 때 "소금 조금, 설탕 많이" 같은 지시사항이라고 생각하면 돼요.

### `-` vs `--` 차이

```bash
ls -a        # 짧은 형식 (short flag)
ls --all     # 긴 형식 (long flag), 같은 기능

rm -rf folder     # 짧은 플래그 여러 개 결합
rm -r -f folder   # 위와 동일
```

- **단일 대시 `-`**: 한 글자 약어 (`-a`, `-l`, `-r`)
- **이중 대시 `--`**: 전체 단어 (`--all`, `--help`, `--verbose`)

여러 개를 붙여 쓸 수 있어요: `-rf` = `-r -f`

---

### 자주 쓰는 플래그들

#### `-h` 또는 `--help` - 도움말
```bash
ls --help
# ls 명령어의 모든 옵션 설명이 나옴

python --help
pip install --help
```

**언제 쓰나요?**: 명령어를 어떻게 쓰는지 모를 때. 구글 검색보다 빠를 때도 많아요!

---

#### `-v` 또는 `--verbose` - 자세히 보기
```bash
pip install requests -v
# 패키지 설치 과정을 자세히 보여줌

rm -v test.txt
# 삭제하면서 "test.txt를 삭제했습니다" 메시지 출력
```

**언제 쓰나요?**: 뭔가 잘 안 될 때. 에러가 어디서 나는지 파악하기 좋습니다.

---

#### `-r` 또는 `--recursive` - 재귀적으로
```bash
cp -r folder1 folder2
# 폴더 안의 모든 내용까지 복사

rm -r old_project
# 폴더와 그 안의 모든 것 삭제

grep -r "TODO" .
# 현재 폴더 아래 모든 파일에서 "TODO" 검색
```

**의미**: "안에 있는 것까지 전부" 처리하라는 뜻

---

#### `-f` 또는 `--force` - 강제로
```bash
rm -f locked_file.txt
# 쓰기 보호되어도 강제 삭제

pip install --upgrade --force-reinstall requests
# 강제로 재설치
```

⚠️ 확인 절차 없이 바로 실행되니 조심하세요!

---

#### `-a` 또는 `--all` - 모두
```bash
ls -a
# 숨김 파일(.으로 시작하는 파일)까지 모두 보기

git add -A
# 모든 변경사항을 스테이징
```

---

#### `-i` 또는 `--interactive` - 대화형
```bash
rm -i *.txt
# 각 파일마다 "정말 삭제할까요?" 물어봄

cp -i file.txt backup.txt
# 덮어쓸 때 확인
```

**언제 쓰나요?**: 실수 방지용. 초보자에게 추천!

---

### 플래그 조합 예시

```bash
ls -lah
# -l (자세히) + -a (숨김파일 포함) + -h (파일크기 사람이 읽기 쉽게)

rm -rif old_project
# -r (재귀) + -i (확인) + -f (강제)
# 근데 -i랑 -f는 모순이라 -i가 우선됨

tar -xzvf archive.tar.gz
# -x (압축풀기) + -z (gzip) + -v (자세히) + -f (파일명 지정)
```

---

## 7️⃣ Python 실전 워크플로우

### 가상환경(Virtual Environment)이란?

**핵심 개념**: 프로젝트마다 독립된 Python 환경을 만드는 것입니다.

**비유로 이해하기**: 
목수가 일할 때 프로젝트마다 별도의 공구함을 쓰는 것과 같아요. 
- 가구 만들기 프로젝트 → 톱, 망치, 못
- 배관 작업 프로젝트 → 렌치, 파이프 커터

Python도 마찬가지입니다:
- 웹 프로젝트 → Django 3.2, requests 2.28
- 데이터 분석 프로젝트 → pandas 1.5, numpy 1.23

**왜 필요한가요?**

1. **버전 충돌 방지**
   ```
   프로젝트 A: requests 2.20 필요
   프로젝트 B: requests 2.31 필요
   → 가상환경 없으면 하나만 설치 가능!
   ```

2. **깔끔한 관리**
   - 프로젝트 삭제 = 가상환경 폴더만 지우면 끝
   - 다른 프로젝트에 영향 없음

3. **배포 용이성**
   - `requirements.txt`로 정확히 같은 환경 재현 가능

---

### 가상환경 만들기

```bash
# 가상환경 생성 (둘 중 선택)
python -m venv venv      # venv 폴더
python -m venv .venv     # .venv 폴더 (숨김)
```

💡 **어느 쪽을 써도 괜찮지만, `.venv`가 요즘 트렌드입니다.**  
IDE가 자동 인식하고, 프로젝트 파일과 시각적으로 분리되기 때문이죠.

**설명**:
- `python -m venv`: "Python 모듈 중 venv를 실행해"
- `.venv`: 생성할 폴더 이름

이 명령을 실행하면 해당 폴더 안에 독립된 Python 환경이 만들어집니다.

```
.venv/
├── Scripts/          # Windows (activate.bat, python.exe 등)
├── Lib/             # 설치된 패키지들
└── pyvenv.cfg       # 설정 파일
```

---

### 가상환경 활성화 (Activate)

**activate의 의미**: "이 가상환경을 활성화해서 사용하겠다"는 선언입니다.

```bash
# Windows PowerShell
.\.venv\Scripts\activate

# Windows CMD
.venv\Scripts\activate.bat

# Mac/Linux
source .venv/bin/activate
```

**활성화되면 무슨 일이 일어나나요?**

1. **프롬프트가 바뀝니다**:
   ```bash
   # 활성화 전
   C:\Users\amore\weather_app>
   
   # 활성화 후
   (.venv) C:\Users\amore\weather_app>
   ```
   앞에 `(.venv)` 표시가 붙으면 성공!

2. **python 명령이 가상환경 것을 가리킵니다**:
   ```bash
   # 확인해보기
   where python
   # 출력: C:\Users\amore\weather_app\.venv\Scripts\python.exe
   ```

3. **pip install하면 가상환경 안에만 설치됩니다**:
   ```bash
   pip install requests
   # .venv/Lib/site-packages/ 안에만 설치됨
   ```

**비유**: 공구함을 "열었다"는 뜻입니다. 이제 이 공구함의 도구들을 쓸 수 있어요.

---

### 가상환경 비활성화

```bash
deactivate
# 프롬프트에서 (.venv) 표시가 사라짐
```

다시 전역 Python 환경으로 돌아갑니다. 프로젝트 작업이 끝났을 때 사용하세요.

---

### 패키지 설치와 관리

**가상환경이 활성화된 상태에서만** 설치하세요!

```bash
# 하나씩 설치
pip install requests
pip install python-dotenv

# 여러 개 한 번에
pip install requests python-dotenv openai

# requirements.txt로 일괄 설치
pip install -r requirements.txt

# 설치된 것 확인
pip list

# 현재 환경의 패키지 목록 저장
pip freeze > requirements.txt
```

**requirements.txt 예시**:
```
requests==2.31.0
python-dotenv==1.0.0
openai==1.3.5
```

버전까지 정확히 기록되므로, 다른 컴퓨터에서도 똑같은 환경을 만들 수 있습니다!

---

### 실전 예시: 새 프로젝트 시작하기

OpenAI API를 사용하는 프로젝트를 처음부터 만들어봅시다.

```bash
# 1. 프로젝트 폴더 생성 및 이동
mkdir weather_chatbot
cd weather_chatbot

# 2. 가상환경 생성
python -m venv .venv
# → .venv 폴더 생김

# 3. 가상환경 활성화
.\.venv\Scripts\activate
# → (.venv) 표시 확인!

# 4. 가상환경이 제대로 활성화됐는지 확인
where python
# C:\Users\amore\weather_chatbot\.venv\Scripts\python.exe
# ↑ .venv 경로가 나오면 성공!

# 5. 필요한 라이브러리 설치
pip install openai python-dotenv requests

# 6. 설치된 패키지 확인
pip list
# openai         1.3.5
# python-dotenv  1.0.0
# requests       2.31.0
# ...

# 7. .env 파일 생성 (환경변수)
cat << EOF > .env
OPENAI_API_KEY=sk-your-api-key-here
WEATHER_API_KEY=your-weather-api-key
EOF

# 8. .gitignore 생성 (민감 정보 제외)
cat << EOF > .gitignore
.env
.venv/
__pycache__/
*.pyc
EOF

# 9. 메인 스크립트 작성
cat << EOF > main.py
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 환경변수 가져오기
api_key = os.getenv('OPENAI_API_KEY')
print(f"API Key 로드 완료: {api_key[:10]}...")

if __name__ == "__main__":
    print("Weather Chatbot 시작!")
EOF

# 10. 실행해보기
python main.py
# 출력: API Key 로드 완료: sk-proj-ab...
#       Weather Chatbot 시작!

# 11. 패키지 목록 파일로 저장 (다른 사람과 공유용)
pip freeze > requirements.txt

# 12. VS Code로 프로젝트 열기
code .
```

---

### 외부에서 받은 프로젝트 시작하기

동료나 인터넷에서 Python 프로젝트를 받으면 보통 이런 파일들이 있습니다:

```
프로젝트 폴더/
├── main.py              # 소스 코드
├── utils.py
├── requirements.txt     # 필요한 패키지 목록
└── README.md           # 사용 설명서
```

**핵심**: `.venv` 폴더나 설치된 패키지는 공유되지 않습니다. 각자 만들어야 해요!

```bash
# 1. 받은 프로젝트 폴더로 이동
cd weather_chatbot

# 2. 가상환경 새로 생성
python -m venv .venv

# 3. 활성화
.\.venv\Scripts\activate

# 4. requirements.txt로 똑같은 환경 만들기
pip install -r requirements.txt
# → 프로젝트에 필요한 모든 패키지가 자동으로 설치됨!

# 5. .env 파일은 보안상 공유 안 되므로 직접 만들기
# (API 키는 각자 발급받아야 함)
echo OPENAI_API_KEY=당신의키 > .env
```

**왜 이렇게 하나요?**
- **requirements.txt**: "이 프로젝트는 requests 2.31.0이 필요해요" 같은 정보 저장
- **pip install -r**: 목록의 모든 패키지를 한 번에 설치
- **결과**: 원작자와 똑같은 환경에서 코드 실행 가능!

---

### 자주 하는 실수

#### 실수 1: 가상환경 활성화 안 하고 설치
```bash
❌ pip install requests
# 전역 환경에 설치됨!

✅ .\.venv\Scripts\activate
   pip install requests
# 가상환경 안에 설치됨
```

#### 실수 2: 가상환경이 활성화됐는지 확인 안 함
```bash
# 프롬프트 확인
(.venv) C:\...\>  # ✅ 활성화됨
C:\...\>          # ❌ 활성화 안 됨

# 또는 직접 확인
where python
# .venv 경로가 나와야 함
```

#### 실수 3: .venv 폴더를 Git에 올림
```bash
# .gitignore에 꼭 추가!
.venv/
venv/
```

가상환경 폴더는 용량이 크고, 각자 만들어야 하는 것이므로 Git에 올리면 안 됩니다.

---

## 8️⃣ 유용한 단축키와 팁

### 현재 폴더를 탐색기/에디터로 열기

```bash
explorer .
# Windows 탐색기로 현재 폴더 열기

code .
# VS Code로 현재 폴더 열기

code main.py
# VS Code로 main.py 파일 열기
```

`.`은 "현재 위치"를 의미합니다.

---

### 화면 정리

```bash
clear
# 터미널 화면 깨끗하게 지우기

# 또는 Ctrl + L (더 빠름)
```

---

### 명령어 히스토리

```bash
history
# 지금까지 입력한 모든 명령어 보기

↑ ↓ 화살표
# 이전/다음 명령어 불러오기

Ctrl + R
# 명령어 검색 (PowerShell)
# 예: "python" 검색하면 python 관련 명령어들 나옴
```

---

### Python 어디 있는지 확인

```bash
where python
# Windows에서 python.exe 위치 찾기

python --version
# Python 버전 확인

which python
# Mac/Linux
```

**언제 쓰나요?**: 가상환경이 제대로 활성화됐는지 확인할 때

```bash
# 가상환경 활성화 전
where python
# C:\Python311\python.exe

# 가상환경 활성화 후
where python
# C:\Users\amore\weather_app\.venv\Scripts\python.exe
```

경로가 `.venv` 안이면 제대로 된 거예요!

---

## 9️⃣ 자주 하는 실수와 해결법

### 실수 1: 공백 처리 안 함
```bash
❌ cd Program Files
# 에러: 'Program'이라는 폴더를 찾을 수 없음

✅ cd "Program Files"
# 또는
✅ cd Program\ Files    # 백슬래시로 이스케이프
```

---

### 실수 2: 폴더인지 파일인지 모르고 명령어 사용
```bash
❌ cat my_folder
# 폴더는 cat으로 못 봄

✅ ls my_folder
# 폴더 안 보기

✅ cat my_file.txt
# 파일 내용 보기
```

---

### 실수 3: 경로 헷갈림
```bash
# 현재 위치: C:\Users\ChangHyun\Desktop

cd project     # ✅ Desktop 안의 project로 이동
cd /project    # ❌ C:\project를 찾음 (루트 기준)
cd ./project   # ✅ 명시적으로 현재 폴더 기준
```

---

### 실수 4: 가상환경 활성화 안 됨 (Windows)
```bash
❌ .\.venv\Scripts\activate
# 보안 정책 에러

✅ 해결법:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# 그 다음 다시 활성화 시도
```

---

## 🎯 정리: 꼭 기억할 핵심 명령어

| 명령어 | 의미 | 언제 쓰나 |
|--------|------|-----------|
| `pwd` | 현재 위치 확인 | 길 잃었을 때 |
| `ls` | 파일 목록 보기 | 뭐가 있나 확인할 때 |
| `ls -a` | 숨김 파일까지 보기 | .env 같은 설정 파일 찾을 때 |
| `cd` | 폴더 이동 | 다른 곳으로 갈 때 |
| `cd ..` | 상위 폴더로 | 한 단계 나갈 때 |
| `mkdir` | 폴더 만들기 | 새 프로젝트 시작할 때 |
| `rm -r` | 폴더 삭제 | 프로젝트 지울 때 |
| `cat` | 파일 내용 보기 | 빠르게 확인할 때 |
| `>` | 출력을 파일로 | 결과 저장할 때 |
| `>>` | 파일에 추가 | 로그 쌓을 때 |
| `--help` | 도움말 | 모르는 명령어 있을 때 |
| `Tab` | 자동완성 | 타이핑 귀찮을 때 (항상!) |
| `python -m venv .venv` | 가상환경 생성 | 프로젝트 시작할 때 |
| `activate` | 가상환경 활성화 | 개발 시작 전 |
| `pip install` | 패키지 설치 | 라이브러리 필요할 때 |

---

이제 터미널이 조금 덜 무섭죠? 처음엔 타이핑이 느려도 괜찮아요. 몇 번만 하다 보면 마우스보다 훨씬 빠르다는 걸 느끼실 거예요! 💪

**기억하세요**: 
- 막히면 `--help` 사용
- Tab으로 자동완성
- 가상환경은 항상 활성화
- 중요한 작업 전엔 `pwd`로 위치 확인!

---

## ✏️ 실습하러 가기

개념을 읽었다면 이제 직접 해볼 차례예요.

👉 **[Week 2 실습 퀴즈 & 미션](../week02-practice)**