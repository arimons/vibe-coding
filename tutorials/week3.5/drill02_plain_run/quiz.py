import random

questions = [
    ("Python에서 주석을 시작하는 기호는?", "#"),
    ("리스트를 만들 때 사용하는 괄호는?", "["),
    ("터미널에서 현재 위치를 확인하는 명령어는?", "pwd"),
    ("한 단계 위 폴더로 이동하는 명령어는?", "cd .."),
    ("Python 파일을 실행하는 명령어 형식은?", "python"),
]

score = 0
random.shuffle(questions)

print("=== 터미널 & Python 기초 퀴즈 ===")
print()

for i, (q, a) in enumerate(questions, 1):
    answer = input(f"Q{i}. {q}\n답: ").strip()
    if answer == a:
        print("✅ 정답!\n")
        score += 1
    else:
        print(f"❌ 오답. 정답은 '{a}' 입니다.\n")

print(f"최종 점수: {score}/{len(questions)}")
