s = 'First line.\nSecond line.'
print(s)

print('C:\some\name')
print(r'C:\some\name')

print("""\
Usage: thingy [OPTIONS]
      -h                    Display this usage message
      -H hostname           Hostname to connect to
""")

print('Py''thon')
print('Put several strings within parenthese '
      'to have them joined together.')

prefix = 'Py'
# print(prefix'thon')

# print(('un' * 3) 'ium')

print(prefix + 'thon')

word = 'Python'
print(word[0])
print(word[5])

print(word[-1])
print(word[-2])
print(word[-6])

print(word[0:2])
print(word[2:6])
print(word[0:-1])

print(word[:2])
print(word[4:])
print(word[-2:])

print(word[:2] + word[2:])
print(word[:4] + word[4:])

# print(word[6])

print(word[4:43])
print(word[6:])

# word[0] = 'J'
# word[2:] = 'py'

print('J' + word[1:])
print(word[:2] + 'py')

s = 'supercalifragilisticexpialidocious'
print(len(s))

squeres = [1, 4, 9, 16, 25]
print(squeres)

print(squeres[0])
print(squeres[-1])
print(squeres[-3:])

print(squeres + [36, 49, 64, 81, 100])

cubes = [1, 8, 27, 65, 125]
print(4 ** 3)
cubes[3] = 4 ** 3
print(cubes)

cubes.append(216)
cubes.append(7 ** 3)
print(cubes)