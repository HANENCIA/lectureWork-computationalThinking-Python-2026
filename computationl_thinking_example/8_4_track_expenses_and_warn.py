def track_expenses_and_warn(budgets: dict[str, float], expenses: list[tuple[str, float]]) -> None:
    totals = {category: 0.0 for category in budgets}

    for category, amount in expenses:
        if category in totals:
            totals[category] += amount

    has_warning = False

    print("카테고리별 총 지출")
    for category, total in totals.items():
        print(f"- {category}: {total:,.0f}원 (예산: {budgets[category]:,.0f}원)")

        if total > budgets[category]:
            print(f"* 경고: {category} 예산 초과")
            has_warning = True

    if has_warning:
        print("* 경고: 일부 카테고리 예산 초과")
    else:
        print("* 안전: 모든 카테고리 예산 이내 지출")


def main():
    print("* 입력 규칙")
    print("1. 카테고리는 '식비', '교통비', '문화비', '기타'만 입력 가능")
    print("2. 지출 입력은 '카테고리 금액' 형식 (예: 식비 25000)")
    print("3. 지출 입력을 끝내려면 '끝'이라고 입력하세요\n")
    print("* 참고: 기본 예산")
    print("식비: 200,000원, 교통비: 50,000원, 문화비: 100,000원, 기타: 50,000\n")

    try:
        budgets = {'식비': 200000, '교통비': 50000, '문화비': 100000, '기타': 50000}

        expenses = []

        while True:
            line = input("지출 내역을 입력하세요 (예: 식비 10000 또는 끝): ").strip()

            if line == '끝':
                break

            parts = line.split()

            if len(parts) != 2:
                print("오류: '카테고리 금액' 형식으로 입력하세요 (예: 식비 25000)")
                continue

            category, amount_str = parts

            if category not in budgets:
                print(f"오류: '{category}'는 유효하지 않은 카테고리입니다.")
                print(f"사용 가능한 카테고리: {', '.join(budgets.keys())}")
                continue

            try:
                amount = int(amount_str)
                if amount < 0:
                    print("오류: 금액은 0 이상의 숫자여야 합니다.")
                    continue
                expenses.append((category, amount))
            except ValueError:
                print("오류: 금액은 숫자로 입력하세요.")
                input("계속하려면 Enter 키를 누르세요...")

        if len(expenses) == 0:
            print("* 안전: 지출 내역이 없습니다.")
            input("계속하려면 Enter 키를 누르세요...")
            return

        track_expenses_and_warn(budgets, expenses)
        input("계속하려면 Enter 키를 누르세요...")


    except Exception as e:
        print(f"오류: {e}")
        input("계속하려면 Enter 키를 누르세요...")


if __name__ == "__main__":
    main()
