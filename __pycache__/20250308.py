def calc_stats(numbers):
    half = len(numbers) // 2
    numbers.sort()

    if len(numbers) % 2 == 0:
        mdn = (numbers[half - 1] + numbers[half]) / 2
    else:
        mdn = numbers[half]

    mydict = {
        "最大値:":max(numbers),
        "最小値:":min(numbers),
        "合計:":sum(numbers),
        "平均:":round(sum(numbers)/len(numbers), 2),
        "中央値:":round(mdn, 2)
    }

    return mydict

str_input = input("数値を入力してください: ")
numbers = str_input.split()
numbers = [int(number) for number in numbers]
result = calc_stats(numbers)
print(result)