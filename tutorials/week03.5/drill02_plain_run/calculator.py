print("간단한 계산기입니다. (연산자: + - * /)")
print()

a = float(input("첫 번째 숫자: "))
op = input("연산자: ")
b = float(input("두 번째 숫자: "))

if op == "+":
    print(f"결과: {a + b}")
elif op == "-":
    print(f"결과: {a - b}")
elif op == "*":
    print(f"결과: {a * b}")
elif op == "/":
    if b == 0:
        print("0으로 나눌 수 없습니다.")
    else:
        print(f"결과: {a / b}")
else:
    print("알 수 없는 연산자입니다.")
