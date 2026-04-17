inp = 'Race Car!'

def palindrome_clean(inp):
    s = ''
    for x in inp:
        if x >= 'a' and x <= 'z' or x >= 'A' and x <= 'Z':
            s += x.lower()
    return s == s[::-1]

print(palindrome_clean(inp))

