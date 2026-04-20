s = "Race Car!"

def Pal_Clean(s):
    clean = "".join(ch.lower() 
    for ch in s if ch.isalnum())
    return clean == clean[::-1]

print(Pal_Clean(s))