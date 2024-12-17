age = 15

if age >= 20:
    print('成人です。')
elif age >= 18:
    print('成人ですが、お酒は飲めません。')
elif age >= 6:
    print('こどもです。')
else:
    print('乳児、幼児です。')

prefecture = "東京"

if prefecture == "東京":
    print('日本の首都です。')
else:
    ('東京ではありません。')

number = 0
if number % 2 == 0:
    print('偶数です。')
else:
    print('奇数です。')

scores = [90, 30, 49]

for x in scores:
    print(x + 1)

year = 400

if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
    print('閏年です。')
else:
    print('平年です。')

for x in range(1, 101):
    output = ''
    if x % 3 == 0:
        output += 'Fizz'
    if x % 5 == 0:
        output += 'Buzz'
    print(output or x)

# 関数定義
def print_hello():
    print('こんにちは')

# 関数呼び出し
print_hello()

def add_numbers(a, b):
    c = a + b
    return c

added = add_numbers(a = 10, b = 100)
print(added)

class User:
    def __init__(self, name, mail_address, point):
        self.name = name
        self.mail_address = mail_address
        self.point = point

    def __str__(self):
        return f'名前: {self.name}, メール: {self.mail_address}, ポイント: {self.point}'

    def add_point(self, points):
        self.point += points

user_1 = User("佐藤葵", "sato@example.com", 500)
print(user_1)
user_1.add_point(100)
print(user_1)

class Item:
    def __init__(self, id, name, price, purchase_price):
        self.id = id
        self.name = name
        self.price = price
        self.purchase_price = purchase_price
        
    def calc(self):
        return self.purchase_price / self.price

    def __str__(self):
        return f'ID: {self.id}, 名前: {self.name}, 価格: {self.price}円, 購入価格: {self.purchase_price}円'

item = Item(id = "A0001", name = "半袖クールTシャツ", price = 5000, purchase_price = 2250)
print(item.calc())