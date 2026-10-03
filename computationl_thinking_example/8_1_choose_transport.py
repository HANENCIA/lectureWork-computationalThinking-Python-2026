def choose_transport(current_hour: int) -> str:
    if current_hour < 7:
        return "지하철"
    else:
        return "버스"


def main():
    try:
        current_hour = int(input("현재 시간을 입력하세요 (예: 6, 7, 14, 23): "))

        if not 0 <= current_hour <= 23:
            print("오류: 시간은 0 에서 23 사이의 숫자여야 합니다.")
            input("계속하려면 Enter 키를 누르세요...")
            return

        transport = choose_transport(current_hour)
        print(f"결과: 현재 시간 {current_hour:02d}시, 선택할 교통수단: {transport}")
        input("계속하려면 Enter 키를 누르세요...")

    except ValueError:
        print("오류: 숫자를 올바르게 입력해주세요.")
        input("계속하려면 Enter 키를 누르세요...")
    except Exception as e:
        print(f"오류: {e}")
        input("계속하려면 Enter 키를 누르세요...")


if __name__ == "__main__":
    main()
