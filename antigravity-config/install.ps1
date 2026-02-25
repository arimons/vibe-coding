# Antigravity 설정 설치 스크립트 (Windows PowerShell)
# 사용법: powershell -ExecutionPolicy Bypass -File install.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$GeminiDir = "$env:USERPROFILE\.gemini"
$AntigravityDir = "$GeminiDir\antigravity"

Write-Host "🚀 Antigravity 설정 설치를 시작합니다..." -ForegroundColor Cyan

# 1. 폴더 생성
New-Item -ItemType Directory -Force -Path "$AntigravityDir\skills" | Out-Null

# 2. GEMINI.md (Global Rules)
$GeminiMd = "$GeminiDir\GEMINI.md"
if (Test-Path $GeminiMd) {
    $answer = Read-Host "⚠️  GEMINI.md 가 이미 존재합니다. 덮어쓰시겠습니까? (y/n)"
    if ($answer -eq "y") {
        Copy-Item "$ScriptDir\GEMINI.md" $GeminiMd -Force
        Write-Host "✅ GEMINI.md 설치 완료" -ForegroundColor Green
    } else {
        Write-Host "⏭️  GEMINI.md 건너뜀" -ForegroundColor Yellow
    }
} else {
    Copy-Item "$ScriptDir\GEMINI.md" $GeminiMd -Force
    Write-Host "✅ GEMINI.md 설치 완료" -ForegroundColor Green
}

# 3. mcp_config.json
$McpConfig = "$AntigravityDir\mcp_config.json"
if (Test-Path $McpConfig) {
    $answer = Read-Host "⚠️  mcp_config.json 이 이미 존재합니다. 덮어쓰시겠습니까? (y/n)"
    if ($answer -eq "y") {
        Copy-Item "$ScriptDir\mcp_config.json" $McpConfig -Force
        Write-Host "✅ mcp_config.json 설치 완료" -ForegroundColor Green
    } else {
        Write-Host "⏭️  mcp_config.json 건너뜀" -ForegroundColor Yellow
    }
} else {
    Copy-Item "$ScriptDir\mcp_config.json" $McpConfig -Force
    Write-Host "✅ mcp_config.json 설치 완료" -ForegroundColor Green
}

# 4. Skills 복사
Get-ChildItem -Path "$ScriptDir\skills" -Directory | ForEach-Object {
    $skillName = $_.Name
    $target = "$AntigravityDir\skills\$skillName"
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Copy-Item "$($_.FullName)\SKILL.md" "$target\SKILL.md" -Force
    Write-Host "✅ Skills/$skillName 설치 완료" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 설치 완료! Antigravity를 재시작해주세요." -ForegroundColor Cyan
