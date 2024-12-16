def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")

print(parrot(1000))                                          # 1 positional argument
print(parrot(voltage=1000))                                  # 1 keyword argument
print(parrot(voltage=1000000, action='VOOOOOM'))             # 2 keyword arguments
print(parrot(action='VOOOOOM', voltage=1000000))             # 2 keyword arguments
print(parrot('a million', 'bereft of life', 'jump'))         # 3 positional arguments
print(parrot('a thousand', state='pushing up the daisies'))  # 1 positional, 1 keyword

# print(parrot())                     # required argument missing
# print(parrot(voltage=5.0, 'dead'))  # non-keyword argument after a keyword argument
# print(parrot(110, voltage=220))     # duplicate value for the same argument
# print(parrot(actor='John Cleese'))  # unknown keyword argument

def function(a):
    pass

# function(0, a=0)

def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")