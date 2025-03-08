while True:
    try:
        num = int(input("数値を入力: "))
        if num == 0:
            print("ゼロ")
        result = "偶数" if num % 2 == 0 else "奇数"
        prefix = "負の" if num < 0 else ""
        print(f"{prefix}{result}")
        break
    except ValueError:
        print("整数を入力してください。")