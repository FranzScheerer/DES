import random, math, hashlib, sys

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
    elif ord(c) <= ord('f') and ord(c) >= ord('a'):
       res = (res<<4) + ord(c) - 87
    elif ord(c) <= ord('F') and ord(c) >= ord('A'):
       res = (res<<4) + ord(c) - 55
  return res

#prime = (2**160 * 5 * 23) + 86427
prime = hextxt2num("04 8E1D43F2 93469E33 194C4318 6B3ABC0B")
a = hextxt2num("04 1CB121CE 2B31F608 A76FC8F2 3D73CB66")
b = hextxt2num("02 F74F717E 8DEC9099 1E5EA9B2 FF03DA58") 
n4 = hextxt2num("04 8E1D43F2 93469E31 7F7ED728 F6B8E6F1")
xx = hextxt2num("03 DF84A96B 5688EF57 4FA91A32 E197198A")
yy = hextxt2num("01 47211619 17A44FB7 B4626F36 F0942E71")

  
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
  return res % n4

def genP(x,a,b):
   while pow(x**3 + a*x + b, (prime - 1)/2, prime) != 1:
     x = x + 1
   y = pow(x**3 + a*x + b, (prime + 1)/4, prime)
   return [x % prime, y % prime]

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
  si = inv(S[0], n4)
  hh = h(m + str(S[1]))
  u1 = (si * hh) % n4
  u2 = (si * S[1]) % n4
  return addP( mulP(G, u1), mulP(Y, u2) )[0] == S[1]


P = [xx,yy]


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

def writeNumber(number, fnam):
  f = open(fnam, 'wb')
  n = number
  while n > 0:
    byte = n % 256
    n = n / 256
    f.write(chr(byte))
  f.close()

def signSchnorr(G,m,x):
  k = h(m + 'kk1')
  R = mulP(G,k)
  e = h(str(R[0]) + m)
  return [(k - x*e) % n4, e]

hxx = h('kk1_' + str(777*random.random()))
sig = signSchnorr(P, message, hxx)
y = mulP(P, hxx)
writeNumber(sig[0],'s0')
writeNumber(sig[1],'s1')
writeNumber(y[0],'y0')
writeNumber(y[1],'y1')
#print "Test n ", pow(7,n4-1,n4) == 1
#print b

  
