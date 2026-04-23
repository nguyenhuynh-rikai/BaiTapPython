def permute_gen(s):
    if len(s) == 0:
        yield ""
    else:
        for i in range(len(s)):
            for p in permute_gen(s[:i] + s[i+1:]):
                yield s[i] + p


for p in permute_gen("ABC"):
    print(p)