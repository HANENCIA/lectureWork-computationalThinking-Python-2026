def check_book_loan_eligibility(member_level: str, current_loans: int, has_overdue: bool) -> str:
    max_loans_by_level = {'학부생': 5, '대학원생': 10, '교직원': 15}

    if has_overdue:
        return "대출 불가"

    max_loans = max_loans_by_level.get(member_level, 0)

    if current_loans >= max_loans:
        return "대출 불가"
    else:
        return "대출 가능"

def main():
    try:
        member_level = input("회원 등급을 입력하세요 (학부생/대학원생/교직원): ").strip()

        if member_level not in ['학부생', '대학원생', '교직원']:
            print("오류: 회원 등급은 '학부생', '대학원생', '교직원' 중 하나여야 합니다.")
            input("계속하려면 Enter 키를 누르세요...")
            return

        current_loans = int(input("현재 대출 권수를 입력하세요: "))

        if current_loans < 0:
            print("오류: 대출 권수는 0 이상의 숫자여야 합니다.")
            input("계속하려면 Enter 키를 누르세요...")
            return

        overdue_input = input("반납기한이 지난 책이 있나요? (y/n): ").strip().lower()

        if overdue_input == 'y':
            has_overdue = True
        elif overdue_input == 'n':
            has_overdue = False
        else:
            print("오류: 반납기한이 지난 책 여부는 'y' 또는 'n'으로 입력하세요.")
            input("계속하려면 Enter 키를 누르세요...")
            return

        result = check_book_loan_eligibility(member_level, current_loans, has_overdue)

        print(f"결과: {result}")
        input("계속하려면 Enter 키를 누르세요...")

    except ValueError:
        print("오류: 숫자를 올바르게 입력해주세요.")
        input("계속하려면 Enter 키를 누르세요...")
    except Exception as e:
        print(f"오류: {e}")
        input("계속하려면 Enter 키를 누르세요...")

if __name__ == "__main__":
    main()