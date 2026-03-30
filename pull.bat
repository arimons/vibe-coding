@echo off
chcp 65001 > nul

echo.
echo ====================================
echo  강의 자료 업데이트
echo ====================================
echo.

REM 현재 위치를 vibe-coding 폴더로 이동
cd /d C:\Developer\vibe-coding

REM hook 파일이 없으면 설치 (최초 1회 자동 설치)
if not exist ".git\hooks\post-merge" (
    echo [자동 설치] Git hook 설치 중...
    copy "post-merge" ".git\hooks\post-merge" >nul
    echo 완료!
    echo.
)

REM git pull 실행 (성공하면 post-merge hook이 자동으로 tutorials/ 초기화)
echo 최신 강의 자료를 다운로드합니다...
git pull

echo.
echo ====================================
echo  업데이트 완료!
echo  tutorials 폴더가 최신 버전으로 갱신됐습니다.
echo ====================================
echo.
pause
