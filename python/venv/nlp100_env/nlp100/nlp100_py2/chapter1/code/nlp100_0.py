def reverse1(data):
    result = ""
    for letter in list(data):
        result = letter + result
    return result

def reverse2(data):
    return "".join(reversed(list(data)))

def reverse3(data):
    return "".join([data[i] for i in range(len(data)-1, -1, -1)])

def reverse4(data):
    return "".join([data[i*-1] for i in range(1, len(data)+1)])

def reverse5(data):
    return data[::-1]

print(reverse1("stressed"))
print(reverse2("stressed"))
print(reverse3("stressed"))
print(reverse4("stressed"))
print(reverse5("stressed"))
