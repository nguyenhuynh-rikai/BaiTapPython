def combine_gen(s, k):
    if k == 0:
        yield ""
        return
    
    for i in range(len(s)):
        for c in combine_gen(s[i+1:], k-1):
            yield s[i] + c


for c in combine_gen("ABC", 2):
    print(c)