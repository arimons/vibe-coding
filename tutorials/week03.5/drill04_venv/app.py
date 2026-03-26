# drill04_venv/app.py
# 실행 전 가상환경을 활성화하세요:
#
#   python -m venv .venv
#   source .venv/bin/activate      # Mac/Linux
#   .venv\Scripts\activate         # Windows
#   pip install rich
#   python app.py

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import sys

console = Console()

console.print(Panel.fit(
    "[bold green]가상환경 실습 성공![/bold green]\n"
    "rich 패키지가 정상적으로 설치되었습니다.",
    title="drill04"
))

table = Table(title="가상환경 핵심 명령어")
table.add_column("명령어", style="cyan")
table.add_column("의미", style="white")

table.add_row("python -m venv .venv",          "가상환경 생성 (.venv 폴더)")
table.add_row("source .venv/bin/activate",     "활성화 (Mac/Linux)")
table.add_row(".venv\\Scripts\\activate",       "활성화 (Windows)")
table.add_row("pip install -r requirements.txt","패키지 일괄 설치")
table.add_row("deactivate",                    "비활성화")

console.print(table)

console.print(f"\n현재 Python 경로: [yellow]{sys.executable}[/yellow]")

if ".venv" in sys.executable or "venv" in sys.executable.lower():
    console.print("✅ 가상환경 안에서 실행 중입니다.")
else:
    console.print("[yellow]⚠️  전역(global) Python으로 실행 중입니다.[/yellow]")

console.print("""
[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 강의 안내
원래 프로젝트는 항상 가상환경(.venv)에서 작업합니다.
하지만 사내 환경 특성상 IO 속도 문제로,
실습 기간 중에는 전역(global) 설치로 진행합니다.
개인 프로젝트 시작 전(Week 8)에 다시 .venv로 전환합니다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/dim]
""")
