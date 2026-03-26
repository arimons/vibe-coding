import os
from utils.helper import greet, read_sample

print("=== drill03: 지도 읽기 ===")
print()

name = input("이름을 입력하세요: ")
print(greet(name))
print()

content = read_sample("data/sample.txt")
print("--- data/sample.txt 내용 ---")
print(content)
print()
print(f"[현재 실행 위치]: {os.getcwd()}")
print("✅ 올바른 위치에서 실행되었습니다.")
