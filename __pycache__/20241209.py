rgb = ["Red", "Green", "Blue"]
rgba = rgb
print(id(rgb) == id(rgba))
rgba.append("Alph")
print(rgb)

correct_rgba = rgba[:]
correct_rgba[-1] = "Alpha"
print(correct_rgba)
print(rgba)

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
print(letters)
# replace some value
letters[2:5] = ['C', 'D', 'E']
print(letters)
# now remove them
letters[2:5] = []
print(letters)
# clear the list by replacing all the elements with an empty list
letters[:] = []
print(letters)

letters = ['a', 'b', 'c', 'd']
print(len(letters))

a = ['a', 'b', 'c']
n = ['1', '2', '3']
x = [a, n]
print(x)
print(x[0])
print(x[0][1])

# Fibonacci series:
# the sum of two elements defines the next
a, b = 0, 1
while a < 100:
    print(a)
    a, b = b, a + b
# while文の終わりには空行を入れる。

i = 256*256
print('The value of i is', i)

a, b = 0, 1
while a < 10000:
    print(a, end=',')
    a, b = b, a+b

