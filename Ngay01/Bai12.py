ds = {'apple': 10, 'orange': 5, 'banana': 12}

result = sorted(ds.items(), key=lambda x:x[1], reverse=False)

print(result)