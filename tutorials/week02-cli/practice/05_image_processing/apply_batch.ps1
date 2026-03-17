# 이미지 워터마크 일괄 처리 스크립트 (Windows PowerShell)
# 사용법: .\apply_batch.ps1

# 가상환경 활성화 확인
$venvPython = ".\.venv\Scripts\python.exe"
if (-Not (Test-Path $venvPython)) {
    Write-Host "❌ 가상환경이 없습니다. 먼저 아래 명령어를 실행하세요:" -ForegroundColor Red
    Write-Host "   python -m venv .venv" -ForegroundColor Yellow
    Write-Host "   .venv\Scripts\activate" -ForegroundColor Yellow
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "🚀 이미지 워터마크 일괄 작업을 시작합니다..." -ForegroundColor Cyan

$files = Get-ChildItem -Filter "test_image_*.jpg"
$count = 0

foreach ($file in $files) {
    if ($file.Name -like "watermarked_*") { continue }

    Write-Host "🎨 처리 중: $($file.Name)" -ForegroundColor Gray
    & $venvPython apply_watermark.py $file.Name
    $count++
}

Write-Host ""
Write-Host "✅ 완료! 총 $count 개 파일을 처리했습니다." -ForegroundColor Green
