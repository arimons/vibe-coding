---
layout: page
title: 용어 사전
nav_order: 2
---

# 바이브 코딩 용어 사전

> 코딩하면서 자주 듣게 될 용어들을 쉽게 정리했습니다

---

## 📱 프로그램 종류

### CLI vs GUI vs Web - 프로그램의 진화

#### **CLI (Command Line Interface)**
```
명령줄 인터페이스

역사:
1970-80년대 컴퓨터는 CLI만 존재
마우스가 없었고, 모든 것을 키보드로 입력
DOS, Unix 시절의 유산

비유: 전문가용 수동 기어 자동차
- 정확한 제어 가능
- 익숙해지면 매우 빠름
- 초보자에게는 어려움

실제 모습:
C:\Users\홍길동> python script.py --input data.xlsx --output result.csv

CLI의 장점:
✅ 정확한 제어
   - flag(옵션)으로 세밀한 조정
   - --input, --output, --verbose 등
   
✅ 자동화 가능
   - 스크립트로 저장해서 반복 실행
   - 100개 파일을 한 번에 처리
   
✅ 원격 제어
   - SSH로 서버 접속해서 명령 실행
   - GUI는 화면 필요, CLI는 텍스트만
   
✅ 배치 처리
   for file in *.xlsx; do python process.py $file; done
   → 폴더 안 모든 엑셀 자동 처리

✅ 리소스 효율
   - 화면 그릴 필요 없음
   - 메모리 적게 씀

CLI의 단점:
❌ 진입장벽 높음
   - 명령어 외워야 함
   - 오타 나면 에러
   
❌ 발견 불가능
   - 어떤 기능 있는지 모름
   - help 읽어야 함

언제 쓰나요?
- 서버 관리 (GUI 없는 환경)
- 자동화 스크립트
- 개발자 도구
- 바이브 코딩 초기 단계
```

#### **GUI (Graphical User Interface)**
```
그래픽 사용자 인터페이스

역사:
1984년 Macintosh에서 대중화
"일반인도 컴퓨터를 쓸 수 있게!"
Windows 95로 폭발적 확산

비유: 자동 기어 자동차
- 누구나 쉽게 사용
- 버튼만 누르면 됨
- 세밀한 제어는 제한적

실제 모습:
[파일 열기] 버튼 클릭
→ 폴더 창 열림
→ 파일 선택
→ [확인] 클릭

GUI의 장점:
✅ 직관적
   - 보이는 대로 사용
   - 설명서 안 봐도 됨
   
✅ 발견 가능성
   - 메뉴 눌러보면 기능 발견
   - 시각적 피드백
   
✅ 진입장벽 낮음
   - 명령어 외울 필요 없음
   - 마우스 클릭만

✅ 실수 방지
   - "정말 삭제하시겠습니까?" 확인창
   - 되돌리기 버튼

GUI의 단점:
❌ 반복 작업 느림
   - 100개 파일 처리 → 100번 클릭
   - 자동화 어려움
   
❌ 원격 사용 어려움
   - 화면 전송 필요
   - 느리고 불편

❌ 리소스 많이 씀
   - 화면 렌더링
   - 메모리/CPU 사용

언제 쓰나요?
- 일반 사용자용 프로그램
- 복잡한 시각화 필요
- 한 번만 쓰는 작업
- 사진/영상 편집
```

#### **Web (웹 애플리케이션)**
```
브라우저에서 실행되는 프로그램

역사:
2000년대 중반부터 본격화
Gmail(2004)이 혁명적 전환점
"설치 없이 바로 쓸 수 있다!"

비유: 공유 자동차 (쏘카)
- 내 차 아니어도 됨
- 어디서든 접근
- 최신 버전 자동 업데이트

실제 모습:
https://gmail.com 접속
→ 이메일 읽기/쓰기
→ 내 컴퓨터에 프로그램 없음

데스크톱 앱 vs Web 앱:

데스크톱 (Excel):
- 내 컴퓨터에 설치
- 인터넷 없어도 작동
- 버전 업데이트 수동
- Windows/Mac 따로 개발

Web (Google Sheets):
- 브라우저만 있으면 됨
- 인터넷 필요
- 자동 업데이트
- 모든 OS에서 동일

Web의 장점:
✅ 설치 불필요
   - URL만 알면 바로 사용
   - 저장 공간 안 씀
   
✅ 자동 업데이트
   - 새로고침하면 최신 버전
   - 사용자가 신경 안 써도 됨
   
✅ 크로스 플랫폼
   - Windows, Mac, Linux 동일
   - 스마트폰에서도 접근
   
✅ 협업 쉬움
   - URL 공유만 하면 됨
   - 실시간 동시 작업

✅ 중앙 관리
   - 데이터가 서버에
   - 내 컴퓨터 망가져도 안전

Web의 단점:
❌ 인터넷 필요
   - 오프라인 작동 제한적
   
❌ 속도 제한
   - 네트워크 왕복 필요
   - 대용량 데이터 처리 느림
   
❌ 보안 우려
   - 데이터가 서버에
   - 서비스 종료되면?

언제 쓰나요?
- 여러 명 협업
- 여러 장소에서 접근
- 설치 부담 줄이기
- Streamlit이 바로 이거!

바이브 코딩에서:
CLI로 스크립트 작성
→ Streamlit으로 Web 앱 변환
→ URL만으로 공유 가능
```

---

## 🔧 개발 도구

### IDE (통합 개발 환경)
```
Integrated Development Environment

역사:
초기에는 메모장에 코드 작성
→ 컴파일러 따로 실행
→ 에디터 + 컴파일러 + 디버거 통합
→ IDE 탄생!

비유: 주방 vs 식당 주방
- 일반 주방: 칼, 도마, 냄비 따로
- 식당 주방: 모든 도구 한곳에 체계적으로

메모장 vs IDE:

메모장으로 코딩:
1. 메모장에 코드 작성
2. 파일 저장
3. 터미널 열기
4. python script.py 실행
5. 에러 나면 1번으로
→ 불편!

IDE로 코딩:
1. 코드 작성하면서 에러 표시
2. F5 누르면 바로 실행
3. 에러 위치 자동으로 표시
→ 편함!

IDE 핵심 기능:

✅ Syntax Highlighting (문법 색깔)
   - 함수는 파란색
   - 문자열은 초록색
   - 에러는 빨간 밑줄
   → 코드 읽기 쉬움

✅ IntelliSense (자동완성)
   - pan 타이핑 → pandas 제안
   - df. 타이핑 → .head(), .tail() 등 메서드 목록
   → 함수명 외울 필요 없음

✅ 실시간 에러 검사
   - 괄호 안 닫음 → 즉시 표시
   - 변수 오타 → 빨간 밑줄
   → 실행 전에 에러 발견

✅ 통합 터미널
   - IDE 안에서 바로 실행
   - 창 전환 불필요

✅ 디버거
   - 코드 한 줄씩 실행
   - 변수 값 확인
   → 버그 찾기 쉬움

바이브 코딩에서:
Antigravity 사용
- VS Code 기반
- Gemini AI 내장
- MCP로 Context7 연결
```

### 터미널 / 명령 프롬프트 / 콘솔
```
모두 같은 말!

비유: 컴퓨터와의 직접 대화창
- GUI: 메뉴판 보고 주문
- 터미널: 주방장한테 직접 말로 주문

OS별 이름:
- Windows: 명령 프롬프트 (cmd), PowerShell
- Mac/Linux: 터미널 (Terminal)
- IDE: 통합 터미널

용도:
- 프로그램 실행
- 패키지 설치
- Git 명령어
- 폴더 이동
- 파일 생성/삭제

기본 명령어:
Windows:
  cd 폴더명        # 폴더 이동
  dir             # 목록 보기
  mkdir 폴더명    # 폴더 생성
  
Mac/Linux:
  cd 폴더명        # 폴더 이동
  ls              # 목록 보기
  mkdir 폴더명    # 폴더 생성
  
공통:
  python script.py  # Python 실행
  pip install pandas  # 패키지 설치
```

### Extension (확장 프로그램)
```
IDE에 추가하는 기능

비유: 스마트폰 앱
- 기본폰: 전화, 문자만
- 앱 설치: 카카오톡, 유튜브 등 추가

VS Code/Antigravity:
- 기본: 텍스트 편집만
- Python extension: Python 문법 이해
- AI extension: 코드 자동 작성

바이브 코딩 필수 Extension:
✅ Python (Microsoft)
   - 문법 색깔
   - 자동완성
   - 에러 표시

✅ AI 도구 중 하나
   - Antigravity: Gemini 기본 내장
   - VS Code: Copilot, Claude 등 선택
```

---

## 🐍 Python 관련

### Python 인터프리터
```
Python 코드를 실행하는 프로그램

비유: 번역기
- 한국어(Python 코드)
- → 컴퓨터어(기계어)

역할:
1. .py 파일 읽기
2. 한 줄씩 번역
3. 즉시 실행

확인:
터미널에서
python --version
→ Python 3.12.1

인터프리터 vs 컴파일러:

인터프리터 (Python):
- 한 줄씩 즉시 실행
- 느리지만 개발 빠름
- 에러 나면 그 줄에서 멈춤

컴파일러 (C, Java):
- 전체 번역 후 실행
- 빠르지만 개발 느림
- 컴파일 시간 필요
```

### 패키지 / 라이브러리 / 모듈
```
거의 같은 말! (엄밀히는 차이 있지만 신경 안 써도 됨)

비유: 레고 블록 세트
- 기본 블록(Python): 직접 만들어야 함
- 레고 세트(패키지): 완성품 제공

왜 쓰나요?
직접 만들기:
  엑셀 읽기 → 1000줄 코드 필요
  
패키지 사용:
  import pandas as pd
  df = pd.read_excel("data.xlsx")
  → 2줄로 끝!

주요 패키지:

✅ pandas
   - 엑셀/CSV 처리
   - 데이터 분석

✅ requests
   - 웹페이지 가져오기
   - API 호출

✅ beautifulsoup4
   - HTML 파싱
   - 크롤링

✅ streamlit
   - 웹앱 만들기
   - 버튼, 입력창 자동 생성

✅ openai / anthropic
   - AI API 호출

설치:
pip install pandas
→ 인터넷에서 다운로드 + 설치

사용:
import pandas as pd
→ 코드에서 불러오기
```

### 프레임워크
```
라이브러리보다 큰 개념

비유:
- 라이브러리: 연장 (내가 집 짓기)
- 프레임워크: 조립식 주택 (구조 정해짐)

라이브러리 (requests):
  내가 주도권
  필요한 기능만 가져다 씀
  
프레임워크 (Streamlit):
  프레임워크가 주도권
  정해진 방식대로 코드 작성
  
  # Streamlit 방식
  import streamlit as st
  st.title("제목")  # 이렇게 써야 함
  
  → Streamlit이 알아서 웹으로 변환

프레임워크 예시:
- Django/Flask: 웹 백엔드
- Streamlit: 데이터 앱
- PyQt: 데스크톱 GUI

장점:
✅ 빠른 개발
✅ 검증된 구조
✅ 모범 사례 내장

단점:
❌ 자유도 낮음
❌ 학습 곡선
```

### venv (가상환경)
```
Virtual Environment

비유: 프로젝트별 사물함
- 공용 사물함: 충돌 발생
- 개인 사물함: 각자 독립

왜 필요?

문제 상황:
프로젝트A: pandas 1.3 필요
프로젝트B: pandas 2.0 필요
→ 하나만 설치 가능
→ 충돌!

가상환경 사용:
프로젝트A 가상환경: pandas 1.3
프로젝트B 가상환경: pandas 2.0
→ 독립적으로 관리
→ 충돌 없음!

사용법:
# 생성
python -m venv .venv

# 활성화
Windows: .venv\Scripts\activate
Mac/Linux: source .venv/bin/activate

# 패키지 설치
pip install pandas

# 비활성화
deactivate

바이브 코딩에서:
Week 10 이후에 배울 거예요
초반에는 불필요
```

---

## 🌐 웹/네트워크

### API
```
Application Programming Interface

비유: 식당 메뉴판 + 주문 시스템
- 손님(내 프로그램): 메뉴판 보고 주문
- 주방(다른 프로그램/서버): 요리 제공
- 웨이터(API): 주문 전달

왜 필요?

직접 구현:
  날씨 정보 → 기상청 서버 해킹?
  번역 → 번역 엔진 개발?
  → 불가능!

API 사용:
  날씨 API: "서울 날씨 알려줘"
  번역 API: "Hello를 한국어로"
  → 간단!

실제 예시:

날씨 API:
import requests

# API 요청
response = requests.get("https://api.weather.com/seoul")

# 응답 받기
data = response.json()
print(data["temperature"])  # 15도

OpenAI API:
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
  model="gpt-4",
  messages=[{"role": "user", "content": "안녕"}]
)

print(response.choices[0].message.content)

API 종류:

✅ RESTful API (제일 흔함)
   - HTTP로 통신
   - JSON 데이터

✅ GraphQL
   - 필요한 데이터만 요청

✅ WebSocket
   - 실시간 통신
   - 채팅, 주식 등

바이브 코딩에서:
Week 7-8에서 AI API 배울 거예요
- OpenAI API
- Claude API
```

### URL / 링크 / 주소
```
모두 같은 말

구조 이해:

https://www.example.com:443/path/to/page?id=123#section

1. https:// (프로토콜)
   - 통신 방법
   - http: 일반
   - https: 암호화 (안전)

2. www.example.com (도메인)
   - 서버 주소
   - IP 주소의 별명

3. :443 (포트)
   - 보통 생략
   - 443: https 기본
   - 80: http 기본

4. /path/to/page (경로)
   - 서버 내 파일 위치

5. ?id=123 (쿼리)
   - 파라미터 전달
   - & 로 여러 개

6. #section (프래그먼트)
   - 페이지 내 위치

실제 예시:
https://github.com/arimons/vibe-coding
  → GitHub 서버
  → arimons 사용자
  → vibe-coding 저장소
```

---

## 💾 버전 관리

### Git
```
코드 버전 관리 도구

비유: 게임 세이브 포인트 + 타임머신
- 세이브: 특정 시점 저장
- 로드: 이전 시점으로 복구
- 분기: 다른 선택지 시도

왜 필요?

문제 상황:
- 코드 수정했다가 망가짐
- 어제 버전으로 돌아가고 싶음
- 어느 부분을 바꿨는지 모름
- 팀원과 코드 합치기 어려움

Git 사용:
- 모든 변경 기록
- 언제든 과거로 복구
- 누가 뭘 바꿨는지 추적
- 자동 병합

기본 개념:

Commit (저장):
  git add .
  git commit -m "엑셀 처리 기능 추가"
  → 현재 상태 저장

Branch (분기):
  git branch feature-login
  → 새로운 시도 시작
  → 원본은 안전

Merge (병합):
  git merge feature-login
  → 분기 합치기

주요 명령어:
git init         # Git 시작
git status       # 상태 확인
git add .        # 변경사항 준비
git commit -m "" # 저장
git log          # 기록 보기
git diff         # 변경 비교

바이브 코딩에서:
Week 10에 자세히 배울 거예요
```

### GitHub
```
Git 저장소를 온라인에서 관리

비유: Git = 카메라 / GitHub = 인스타그램
- Git: 사진(버전) 찍기
- GitHub: 온라인에 업로드 + 공유

차이점:
Git:
  - 내 컴퓨터에서 버전 관리
  - 오프라인 가능
  - 무료 도구

GitHub:
  - 온라인 저장소
  - 협업 기능
  - 포트폴리오
  - 무료 + 유료

주요 기능:

✅ 코드 백업
   - 컴퓨터 망가져도 안전

✅ 협업
   - 여러 명이 동시 작업
   - Pull Request로 리뷰

✅ 이슈 추적
   - 버그 리포트
   - 기능 요청

✅ 포트폴리오
   - 취업시 코드 증명

GitHub Pages:
무료 웹호스팅
- .md 파일 → 자동으로 웹사이트
- vibe-coding 교재도 여기 올림

명령어:
git push        # GitHub에 업로드
git pull        # GitHub에서 다운로드
git clone       # 저장소 복사
```

### Repository (저장소)
```
프로젝트 폴더

비유: 프로젝트 전용 USB
- 코드, 문서, 설정 등 모두 포함
- Git으로 관리됨

구조:
my-project/         # 저장소 루트
├── .git/           # Git 데이터 (숨김)
├── src/            # 소스 코드
├── README.md       # 프로젝트 설명
├── requirements.txt # 필요 패키지
└── .gitignore      # Git 무시 파일

종류:
- 로컬 저장소: 내 컴퓨터
- 원격 저장소: GitHub

용어:
- Clone: 원격 → 로컬 복사
- Fork: 다른 사람 저장소 복사
- Star: 북마크 (좋아요)
```

---

## ⚙️ 실행 관련

### 실행 / Run / 런타임
```
프로그램을 돌리는 것

실행 방법:

1. CLI:
   python script.py

2. IDE:
   F5 또는 Run 버튼

3. 자동 실행:
   - 부팅시
   - 스케줄 (매일 9시)

런타임 (Runtime):
  프로그램이 실행 중인 상태
  
  런타임 에러:
  - 실행 중에 발생하는 에러
  - 문법 에러와 다름
  
  예시:
  # 문법 에러
  print("hello"  # 괄호 안 닫음
  → 실행 전에 발견
  
  # 런타임 에러
  x = 10 / 0  # 0으로 나누기
  → 실행해야 발견
```

### 에러 / 버그
```
에러 (Error): 프로그램이 멈춤
버그 (Bug): 잘못된 동작

비유:
- 에러: 차 시동 안 걸림 (치명적)
- 버그: 방향지시등 반대로 (동작하지만 잘못됨)

흔한 Python 에러:

SyntaxError (문법 에러):
  print("hello"  # 괄호 안 닫음
  → 실행 전에 발견

NameError (이름 에러):
  print(x)  # x 정의 안 함
  → 변수 없음

TypeError (타입 에러):
  "hello" + 5  # 문자+숫자
  → 타입 안 맞음

ModuleNotFoundError:
  import pandas  # pandas 안 깔림
  → pip install pandas

IndentationError:
  def hello():
  print("hi")  # 들여쓰기 안 함
  → Python은 들여쓰기 필수

IndexError:
  lst = [1, 2, 3]
  print(lst[10])  # 인덱스 없음
  → 범위 초과

에러 읽는 법:
Traceback (most recent call last):
  File "script.py", line 5, in <module>
    result = 10 / 0
ZeroDivisionError: division by zero

해석:
- script.py 파일
- 5번째 줄
- 0으로 나누기 에러
```

### 디버깅
```
Debugging = 벌레(Bug) 제거

역사:
1947년 Harvard Mark II 컴퓨터
실제 나방이 회로에 끼어서 오작동
→ "버그" 용어 탄생

디버깅 방법:

1. 에러 메시지 읽기
   - 어느 줄?
   - 무슨 에러?
   
2. print() 디버깅
   print("여기까지 왔나?")
   print(f"x 값: {x}")
   → 어디서 잘못됐는지 추적

3. AI한테 물어보기 (바이브 코딩 방식!)
   에러 메시지 복사
   → AI한테 붙여넣기
   → "이 에러 뭐야? 어떻게 고쳐?"

4. 구글링
   에러 메시지 검색
   → Stack Overflow

5. IDE 디버거
   - 중단점 설정
   - 한 줄씩 실행
   - 변수 값 확인

바이브 코딩 디버깅:
1. 에러 메시지 복사
2. AI한테 물어보기
3. 제안된 코드 적용
4. 해결!
```

---

## 📝 코드 기본

### 변수
```
값을 담는 상자

비유: 이름표 붙인 박스
- 상자 안에 물건(값) 넣기
- 이름표로 찾기

예시:
name = "홍길동"     # 문자열
age = 30            # 숫자
is_student = True   # 참/거짓

변수명 규칙:
✅ 가능:
   my_name
   user_age
   total2

❌ 불가능:
   2total  # 숫자로 시작
   my-name  # 하이픈
   for  # 예약어

변수의 장점:

반복 사용:
name = "홍길동"
print(f"안녕하세요 {name}님")
print(f"{name}님의 포인트")

한 번에 수정:
name을 "김철수"로 바꾸면
모든 곳에 적용
```

### 함수
```
특정 작업을 수행하는 코드 묶음

비유: 레고 블록
- 한 번 만들면 계속 재사용
- 조립해서 큰 프로그램 만들기

함수 없이:
print("=" * 50)
print("환영합니다!")
print("=" * 50)

print("=" * 50)
print("감사합니다!")
print("=" * 50)
→ 반복!

함수 사용:
def print_box(message):
    print("=" * 50)
    print(message)
    print("=" * 50)

print_box("환영합니다!")
print_box("감사합니다!")
→ 깔끔!

함수의 장점:
✅ 재사용
✅ 코드 정리
✅ 유지보수 쉬움

예시:
def calculate_tax(price):
    return price * 0.1

tax1 = calculate_tax(10000)  # 1000
tax2 = calculate_tax(50000)  # 5000
```

### 주석
```
코드 설명 (실행 안 됨)

비유: 요리책의 팁
- "이 단계가 중요해요!"
- "소금 대신 간장도 가능"

Python 주석:
# 한 줄 주석
x = 10  # 변수 선언

"""
여러 줄
주석
"""

좋은 주석:
# 할인율 적용
price = price * 0.9

나쁜 주석:
# x에 10을 넣음
x = 10
→ 코드만 봐도 알 수 있음

주석 원칙:
- "왜" 를 설명 (무엇이 아니라)
- 나중의 나를 위해
- 복잡한 부분만

바이브 코딩에서:
AI가 주석도 자동 작성
"# 엑셀 파일 읽기" 같은 주석 자동 생성
```

---

## 🤖 AI 관련

### 프롬프트
```
AI에게 주는 명령/질문

비유: 식당 주문
- 나쁜 주문: "뭐 좀"
- 좋은 주문: "된장찌개, 덜 짜게, 밥 곱빼기"

나쁜 프롬프트:
"엑셀 처리"
→ 뭘 어떻게?

좋은 프롬프트:
"pandas를 사용해서
data.xlsx 파일을 읽고,
'날짜' 컬럼으로 내림차순 정렬한 후,
sorted.xlsx로 저장하는
Python 코드를 작성해줘"
→ 구체적!

프롬프트 작성 팁:

✅ 구체적으로
   ❌ "웹 크롤링"
   ✅ "네이버 뉴스 제목 100개 크롤링"

✅ 단계별로
   1. 파일 읽기
   2. 중복 제거
   3. 정렬
   4. 저장

✅ 제약 조건 명시
   - pandas 사용
   - 에러 처리 포함
   - 진행률 표시

✅ 예시 제공
   입력: data.xlsx (이름, 나이)
   출력: sorted.csv (나이순)

바이브 코딩 = 좋은 프롬프트 작성법 배우기
```

### LLM
```
Large Language Model
거대 언어 모델

비유: 초대형 도서관 + 사서
- 엄청난 양의 책(학습 데이터)
- 질문하면 답변 생성

예시:
- GPT (OpenAI)
- Claude (Anthropic)
- Gemini (Google)

어떻게 작동?

학습:
인터넷의 수십억 페이지 읽음
→ 패턴 학습
→ 다음 단어 예측

사용:
"Python에서 엑셀 읽는 법"
→ 학습한 패턴으로 답변 생성

특징:
✅ 방대한 지식
✅ 자연어 이해
✅ 코드 생성 가능

⚠️ 한계:
❌ 환각(Hallucination)
   - 그럴싸한 거짓말
   - 없는 함수 만들어냄
   
❌ 최신 정보 부족
   - 학습 데이터 기준
   - → MCP Context7로 해결!

❌ 수학 약함
   - 계산보다 패턴

바이브 코딩에서:
LLM = 코딩 조수
명령만 잘하면 코드 자동 작성
```

---

## 🔌 AI 도구 연동

### MCP (Model Context Protocol)
```
AI가 외부 도구와 소통하는 표준

비유: USB 포트
- 컴퓨터에 USB 포트
- 키보드, 마우스, 프린터 연결
- AI에 MCP 포트
- 파일, 데이터베이스, 최신 문서 연결

왜 필요?

문제:
AI: "pandas로 엑셀 읽어"
→ pandas 1.0 문법으로 코드 생성
→ 실제 설치된 버전: pandas 2.0
→ 에러!

LLM 학습 데이터:
- 2025년 1월까지
- pandas 2.0 출시: 2025년 2월
- → 최신 문법 모름

해결책: MCP Context7
- 실시간으로 pandas 2.0 문서 검색
- 최신 문법 제공
- AI가 최신 코드 작성

MCP 서버 종류:

Context7 (필수!):
- 라이브러리 최신 문서
- pandas, requests, streamlit 등
- 구버전 코드 방지

Filesystem:
- 파일/폴더 접근
- 코드베이스 읽기

Database:
- MySQL, PostgreSQL 연결
- 쿼리 실행

Serena (고급):
- LSP 기반 코드 분석
- 함수 참조 찾기
- 대규모 프로젝트용
- 바이브 코딩에는 과함

설정 방법 (Antigravity):
1. 우상단 "..." 클릭
2. "MCP Servers" 선택
3. MCP Store 열기
4. "Context7" 검색
5. Install 클릭
6. 완료!

사용 예시:

Context7 없이:
"pandas로 엑셀 읽기"
→ pd.read_excel() # 옛날 방식

Context7 사용:
"pandas로 엑셀 읽기"
→ AI가 Context7에서 최신 문서 확인
→ pd.read_excel(engine='openpyxl') # 최신 방식

바이브 코딩에서:
✅ Context7만 설치하면 됨
❌ 다른 MCP는 불필요
```

---

## 📦 파일 관련

### 경로 (Path)
```
파일의 위치

비유: 집 주소
- 절대 주소: 서울시 강남구 테헤란로 123
- 상대 주소: 옆집, 2층

절대 경로 (Absolute Path):
Windows:
  C:\Users\홍길동\Documents\project\data.xlsx

Mac/Linux:
  /Users/honggildong/Documents/project/data.xlsx

상대 경로 (Relative Path):
현재 위치: C:\Users\홍길동\Documents\project

./data.xlsx            # 같은 폴더
../images/photo.jpg    # 상위 폴더의 images
subfolder/file.txt     # 하위 폴더

특수 기호:
.   현재 폴더
..  상위 폴더
~   홈 폴더 (Mac/Linux)

OS별 차이:
Windows: 역슬래시 \
Mac/Linux: 슬래시 /

Python에서는:
import os
path = os.path.join("folder", "file.txt")
→ OS 상관없이 작동
```

### 확장자
```
파일 형식 구분

구조:
파일명.확장자
script.py
document.docx

주요 확장자:

코드:
- .py: Python
- .js: JavaScript
- .java: Java
- .c: C언어

데이터:
- .xlsx: 엑셀
- .csv: 쉼표로 구분
- .json: JavaScript Object
- .xml: 구조화된 데이터
- .txt: 텍스트

문서:
- .md: Markdown
- .docx: Word
- .pdf: PDF

실행 파일:
- .exe (Windows)
- .app (Mac)
- .sh (Linux 스크립트)

이미지:
- .jpg / .png / .gif

왜 중요?

Python에서:
파일 읽을 때 확장자 확인

if file.endswith('.xlsx'):
    df = pd.read_excel(file)
elif file.endswith('.csv'):
    df = pd.read_csv(file)
```

---

## 💡 기타 유용한 용어

### 오픈소스
```
Open Source

소스 코드가 공개된 프로그램

비유: 공개 레시피
- 일반 레시피: 비공개 (코카콜라)
- 공개 레시피: 누구나 보고 수정 가능

특징:
✅ 무료
✅ 수정 가능
✅ 재배포 가능
✅ 커뮤니티 개발

대표 예시:
- Python (언어)
- Linux (OS)
- VS Code (IDE)
- pandas (라이브러리)

vs 상용 소프트웨어:
- Windows (유료, 비공개)
- Adobe Photoshop (유료, 비공개)

왜 무료?
1. 취미 프로젝트
2. 회사 홍보
3. 커뮤니티 기여

오픈소스 라이선스:
- MIT: 제일 자유로움
- GPL: 수정본도 공개 필수
- Apache: 특허 보호
```

### 크로스 플랫폼
```
여러 운영체제에서 작동

비유: 멀티 어댑터
- 한국, 미국, 유럽 어디서나 사용

예시:

크로스 플랫폼:
- Python (Windows/Mac/Linux)
- VS Code
- Chrome
- Node.js

플랫폼 종속:
- .exe (Windows만)
- .dmg (Mac만)
- Safari (Mac/iPhone만)

장점:
✅ 개발 한 번
✅ 모든 OS 지원
✅ 사용자 넓음

어떻게 가능?

방법 1: 인터프리터 언어
  Python 코드는 똑같음
  Python 인터프리터가 OS별로 다름

방법 2: 가상 머신
  Java → JVM 위에서 실행

방법 3: 웹
  브라우저만 있으면 됨
```

### 의존성
```
Dependency

다른 패키지가 필요함

비유: 자동차 부품
- 엔진: 배터리 필요
- 배터리: 충전기 필요
→ 의존성 체인

예시:

Streamlit 설치:
pip install streamlit

자동으로 함께 설치:
- pandas
- numpy
- pillow
- ...

왜? Streamlit이 이것들 사용하니까

의존성 지옥 (Dependency Hell):

문제:
- 패키지A: numpy 1.20 필요
- 패키지B: numpy 1.24 필요
→ 충돌!

해결:
- venv로 분리
- 버전 명시
- requirements.txt 관리

requirements.txt:
pandas==2.0.0
requests>=2.28.0
streamlit==1.28.0

사용:
pip install -r requirements.txt
→ 명시된 버전 설치
```

### 배포 / 디플로이
```
Deploy

프로그램을 실제로 사용 가능하게

비유: 요리
- 개발: 요리 연습
- 배포: 손님에게 제공

배포 종류:

1. 웹 배포:
   - Streamlit Cloud
   - Heroku
   - AWS
   → URL로 접근

2. 앱스토어:
   - Google Play
   - App Store
   → 다운로드 설치

3. 서버 배포:
   - 회사 서버에 설치
   - 내부에서만 사용

4. 실행 파일:
   - .exe 만들기
   - 배포용 패키징

바이브 코딩 배포:

개발:
python app.py
→ 내 컴퓨터에서만

배포:
streamlit deploy
→ https://my-app.streamlit.app
→ 전세계 누구나 접근

배포시 고려사항:
- 보안 (API 키 숨기기)
- 성능 (동시 접속)
- 비용 (서버 요금)
```

---

## 🎯 바이브 코딩 핵심 용어 Top 10

```
1. CLI: 명령어로 실행 (자동화 핵심)
2. Web: 브라우저에서 실행 (Streamlit)
3. IDE: 코드 에디터 (Antigravity)
4. 터미널: 명령어 입력 화면
5. 패키지: 남이 만든 코드 (pandas)
6. API: 프로그램끼리 소통 (OpenAI)
7. 에러: 프로그램 멈춤 (디버깅 대상)
8. 함수: 코드 묶음 (재사용)
9. 프롬프트: AI한테 주는 명령 (핵심 스킬)
10. MCP: AI에게 최신 문서 제공 (Context7)
```

---

## 💬 모르는 용어 나오면?

```
1. 이 문서 검색 (Ctrl+F)
   - 5000단어 이상 수록
   - 비유와 예시 포함

2. AI한테 물어보기
   "Python에서 [용어]가 뭐야?"
   "비유로 설명해줘"

3. 강의 중 질문하기
   - 바보 같은 질문은 없습니다
   - 모르는 게 당연합니다

기억하세요:
"개발자도 구글/AI 보면서 일합니다!"
```

---

**작성일:** 2025년 2월 11일  
**버전:** 3.0 (비유와 맥락 강화)  
**대상:** 바이브 코딩 Week 1 수강생  
**분량:** 약 8,000 단어
