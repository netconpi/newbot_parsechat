
g = []

a = 31
b = 1

z = []
if b == 0: 
    for i in range(6):
        z.append("")
else:
    for i in range(1, b):
        z.append('')

g.append(z.copy())
z = []

for i in range(1, a+1):
    if len(g[-1]) < 7:
        g[-1].append(i)
    else:
        g.append([i])

print(g)