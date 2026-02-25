@echo off
chcp 65001 > nul
echo.
echo ====================================
echo  바이브 코딩 강의 환경 설치 시작
echo ====================================
echo.

REM 1. 설치 폴더 생성
echo [1/5] C:\Users\%USERNAME%\dev 폴더 생성 중...
mkdir C:\Users\%USERNAME%\dev 2>nul
echo 완료!
echo.

REM 2. Python 3.12 설치
echo [2/5] Python 3.12 설치 중...
winget install Python.Python.3.12 --silent
echo 완료!
echo.

REM 3. Git 설치
echo [3/5] Git 설치 중...
winget install Git.Git --silent
echo 완료!
echo.

REM 4. Node.js LTS 설치
echo [4/5] Node.js 설치 중...
winget install OpenJS.NodeJS.LTS --silent
echo 완료!
echo.

REM 5. 강의 자료 다운로드
echo [5/5] 강의 자료 다운로드 중...
cd C:\Users\%USERNAME%\dev
"C:\Program Files\Git\bin\git.exe" clone https://github.com/arimons/vibe-coding
echo 완료!
echo.

echo ====================================
echo  설치 완료!
echo.
echo  다음 단계:
echo  1. Antigravity 설치: https://antigravity.ai
echo  2. 설치 후 vibe-coding\antigravity-config\install.bat 실행
echo ====================================
echo.
pause
