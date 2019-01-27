import math, hashlib, sys

def readNumber(fnam):
  f = open(fnam, 'rb')
  n = 0
  snum = f.read()
  for i in range(len(snum)):
    n = (n << 8) ^ ord(snum[len(snum)-i-1])   
  f.close()
  return n

prime = (2**160 * 5 * 23) + 86427
n_ = prime + 1
a = prime - 31
c = 17
b = 0

def h(x):
  txt = hashlib.md5(x).digest()
  res = 0
  for cx in txt:
    res = (res<<8) ^ ord(cx)
  return res

def genP(x,a,b):
   if (4*a*a*a + 27*b*b) % prime == 0:
      b = b + 1
   while pow(c*x**3 + a*x + b, (prime - 1)/2, prime) != 1:
     x = x + 1
   y = pow(c*x**3 + a*x + b, (prime + 1)/4, prime)
   return [x % prime, (y) % prime]

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  while x1 < x2:
     x1 = x1 + prime
  if x1 == x2:
     s = ((3*c*(x1**2) + a) * pow(2*y1, prime - 2, prime)) % prime
  else:  
     s = ((y1-y2) * pow(x1-x2, prime-2, prime)) % prime
  xr = cinv*s**2 - x1 - x2
  yr = s * (x1-xr) - y1 
  return [xr % prime, yr % prime]

def mulP(P,n):
  isFirst = True
  resP = P
  if n < 0:
    resP[1] = prime - resP[1]
    n = (-1)*n 
  PP = resP
  while n > 0:
     if (n % 2 != 0):   
         if isFirst:
            resP = PP
            isFirst = False
         else:
            resP = addP(resP,PP)
     PP = addP(PP, PP) 
     n = n / 2
  return resP


def verify(G,s,Y,e,m):
  return e == h(str(addP(mulP(G,s),mulP(Y,e))[0]) + m)

P = genP(a+17, a, b)
cinv = pow(c, prime-2, prime)

f = open(sys.argv[1], 'r')
message = f.read()
f.close()

y = [readNumber('y0'), readNumber('y1')]
sig = [readNumber('s0'), readNumber('s1')]
print "The verification of signature ", verify(P, sig[0], y, sig[1], message)

