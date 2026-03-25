from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

console.print(Panel.fit(
    "[bold green]가상환경 실습 성공![/bold green]\n"
    "rich 패키지가 정상적으로 설치되었습니다.",
    title="drill04"
))

table = Table(title="가상환경 명령어 정리")
table.add_column("명령어", style="cyan")
table.add_column("의미", style="white")

table.add_row("python -m venv venv", "가상환경 생성")
table.add_row("source venv/bin/activate", "가상환경 활성화 (Mac/Linux)")
table.add_row("venv\\Scripts\\activate", "가상환경 활성화 (Windows)")
table.add_row("pip install -r requirements.txt", "패키지 일괄 설치")
table.add_row("deactivate", "가상환경 비활성화")

console.print(table)

import sys
console.print(f"\n현재 사용 중인 Python: [yellow]{sys.executable}[/yellow]")
console.print("경로에 'venv'가 포함되어 있으면 가상환경이 활성화된 것입니다. ✅")
