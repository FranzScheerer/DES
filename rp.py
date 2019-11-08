import random
n = 256
p = []
for i in range(n):
  p.append(i)
i = n
while i > 1:
  i = i - 1
  j = random.randint(0,i)
  p[i], p[j] = p[j], p[i]

print (p)