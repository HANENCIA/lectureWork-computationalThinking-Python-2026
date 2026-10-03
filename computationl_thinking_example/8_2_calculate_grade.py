def calculate_grade(scores: list[int]) -> tuple[float, str]:
    total = sum(scores)
    average = total / len(scores)

    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "F"

    return average, grade


def main():
    try:
        scores = []
        print("10 개 과목 점수를 입력하세요:")

        for i in range(1, 11):
            while True:
                score = int(input(f"과목 {i} 점수: "))
                if 0 <= score <= 100:
                    scores.append(score)
                    break
                else:
                    print("오류: 점수는 0에서 100 사이여야 합니다. 다시 입력하세요.")

        average, grade = calculate_grade(scores)

        print(f"결과: 평균 {average:.1f}점, 등급 {grade}")
        input("계속하려면 Enter 키를 누르세요...")

    except ValueError:
        print("오류: 숫자를 올바르게 입력해주세요.")
        input("계속하려면 Enter 키를 누르세요...")
    except Exception as e:
        print(f"오류: {e}")
        input("계속하려면 Enter 키를 누르세요...")


if __name__ == "__main__":
    main()
