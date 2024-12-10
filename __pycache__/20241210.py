# x = int(input("Pleas enter an integer: "))
# if x < 0:
#     x = 0
#     print('Negative changed to zero')
# elif x == 0:
#     print('Zero')
# elif x == 1:
#     print('Single')
# else:
#     print('More')

# 文字列計算:
words = ['cat', 'window', 'defenestrate']
for w in words:
    print(w, len(w))

# コレクション作成
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# 方針:　コピーを反復
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]
        print(users)

# 方針:　新コレクション作成
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status
        print(active_users)
