def grade_quiz(correct_answers: list[str], student_answers: list[str]) -> tuple[int, str]:
    correct_count = 0

    for i in range(len(correct_answers)):
        if correct_answers[i] == student_answers[i]:
            correct_count += 1

    if correct_count >= 4:
        feedback = "우수"
    elif correct_count == 3:
        feedback = "보통"
    else:
        feedback = "보충 필요"

    return correct_count, feedback


def main():
    print("* 입력 규칙")
    print("1. 5 문제의 정답을 공백으로 구분하여 입력 (예: A B C D B)")
    print("2. 5 문제의 학생 답안을 공백으로 구분하여 입력 (예: A B E D C)")

    try:
        correct_input = input("정답 5 개를 입력하세요 (공백 구분): ").strip().split()

        if len(correct_input) != 5:
            print("오류: 정답은 정확히 5개 입력해야 합니다.")
            input("계속하려면 Enter 키를 누르세요...")
            return

        student_input = input("학생 답안 5개를 입력하세요 (공백 구분): ").strip().split()

        if len(student_input) != 5:
            print("오류: 학생 답안은 정확히 5개 입력해야 합니다.")
            input("계속하려면 Enter 키를 누르세요...")
            return

        score, feedback = grade_quiz(correct_input, student_input)

        print(f"결과: 총점 {score}점, 피드백: {feedback}")
        input("계속하려면 Enter 키를 누르세요...")

    except Exception as e:
        print(f"오류: {e}")
        input("계속하려면 Enter 키를 누르세요...")


if __name__ == "__main__":
    main()
