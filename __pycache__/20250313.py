while True:
    try:
        str_input = input("整数を入力してください:")
        array = str_input.split()
        array = [int(number) for number in array]
        for i in range(len(array)):
            if array[i] > 0:
                print("正の数")
            else:
                print("負の数")
        break
    except(ValueError, IndexError):
        print("整数を入力してください")
