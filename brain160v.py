import math, hashlib, sys

def readNumber(fnam):
  f = open(fnam, 'rb')
  n = 0
  snum = f.read()
  for i in range(len(snum)):
    n = (n << 8) ^ ord(snum[len(snum)-i-1])   
  f.close()
  return n

def hextxt2num(x):
  res = 0
  for c in x:
    if ord(c) < 58 and ord(c) >= 48:
       res = (res<<4) + ord(c) - 48
    elif ord(c) <= ord('F') and ord(c) >= ord('A'):
       res = (res<<4) + ord(c) - 55
  return res

prime = hextxt2num("E95E4A5F737059DC60DFC7AD95B3D8139515620F") 
a = hextxt2num("340E7BE2A280EB74E2BE61BADA745D97E8F7C300")
b = hextxt2num("1E589A8595423412134FAA2DBDEC95C8D8675E58")
n = hextxt2num("E95E4A5F737059DC60DF5991D45029409E60FC09")

 
def inv(b,m):
  s = 0
  t = 1
  a = m
  while b != 1:
    q = a/b
    aa = b
    b = a % b
    a = aa
    ss = t
    t = s - q*t
    s = ss
  if t < 0:
    t = t + m
  return t

def h(x):
  dx1 = hashlib.sha256(x).digest()
  res = 0
  for cx in (dx1):
    res = (res<<8) ^ ord(cx)
  return res % n

def genP(x,a,b):
   while (pow(x**3 + a*x + b, (prime - 1)/2, prime) != 1):
     x = x + 1
   y = pow(x**3 + a*x + b, (prime + 1)/4, prime)
   return [(x) % prime, (y) % prime]

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  while x1 < x2:
     x1 = x1 + prime
  if x1 == x2:
     s = ((3*(x1**2) + a) * inv(2*y1, prime)) % prime
  else:  
     s = ((y1-y2) * inv(x1-x2, prime)) % prime
  xr = s**2 - x1 - x2
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

def ecdsa_v(G,m,S,Y):
  si = inv(S[0], n)
  hh = h(m + str(S[1]))
  u1 = (si * hh) % n
  u2 = (si * S[1]) % n
  return addP( mulP(G, u1), mulP(Y, u2) )[0] == S[1]

x = hextxt2num("BED5AF16EA3F6A4F62938C4631EB5AF7BDBCDBC3")
P = genP(x, a, b)
P = mulP(P,4)

f = open(sys.argv[1], 'r')
message = f.read()
f.close()

y = [readNumber('y0'), readNumber('y1')]
sig = [readNumber('s0'), readNumber('s1')]

print "Public key: X: ", y[0] % prime
print "Public key: Y: ", y[1] % prime
print "Sigature    X: ", sig[0]
print "Sigature    y: ", sig[1]
print ""
print "The verification of signature ", verify(P, sig[0], y, sig[1], message)
print "The verification of ecdsa signature ", ecdsa_v(P,message,sig, y)

