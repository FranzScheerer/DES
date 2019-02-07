import random

def shuffle(ary):
    a=len(ary)
    b=a-1
    for d in range(b,0,-1):
      e=random.randint(0,d)
      if e == d:
            continue
      ary[d],ary[e]=ary[e],ary[d]
    return ary

x = range(64)
x = shuffle(x)
xs = ''
for i in range(64):
  if i<63: 
     xs += str(x[i]+1) + ', '
  else:
     xs += str(x[i]+1)
  if i % 10 == 9:  
    xs = xs + "\n"

print "const int InitialPermutation[64] = { "
print xs
print "};"

y = range(64)
for i in range(64):
  y[ x[i] ] = i

xs = ''
for i in range(64):
  if i<63: 
     xs += str(y[i]+1) + ', '
  else:
     xs += str(y[i]+1)
  if i % 10 == 9:  
    xs = xs + "\n"

print "const int FinalPermutation[64] = { "
print xs
print "};"

  