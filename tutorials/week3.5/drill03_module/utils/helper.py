def greet(name: str) -> str:
    return f"안녕하세요, {name}님! utils.helper에서 인사드립니다."

def read_sample(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
