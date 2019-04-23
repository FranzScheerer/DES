import random, math, hashlib, sys

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 24 != 19:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ =  5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43 * 47
  while True:
    while gcd(p, m_) != 1 or gcd((p+1)/4, m_) != 1:
      p = p + 24 
    if (pow(7,p-1,p) != 1 or pow(7, (p+1)/4 - 1, (p+1)/4) != 1):
      p = p + 24
      continue
    return p


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
prime = 6277101735386680763835789423207666416083908700390324961279
a = prime - 3
b = hextxt2num("64210519 e59c80e7 0fa7e9ab 72243049 feb8deec c146b9b1")
n4 = 6277101735386680763835789423176059013767194773182842284081 
hsize = 2**100 + 7
 
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
  return res % hsize

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  while x1 < x2:
     x1 = x1 + prime
  if x1 == x2:
     s = ((3*(x1**2) + a + prime) * inv(2*y1, prime)) % prime
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

x = 1
while pow(x**3 + a*x + b, (prime - 1)/2, prime) != 1:
   x = x + 1
y = pow(x**3 + a*x + b, (prime + 1)/4, prime)
P = [x % prime, y % prime]
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
#print "The verification of ecdsa signature ", ecdsa_v(P,message,sig, y)

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

def ecdsa(G,m,x):
  k = h(m + 'ecdsa')
  R = mulP(G,k)
  hh = h(m+str(R[0]))
  s = ( inv(k,n4) * (hh + R[0]*x) ) % n4
  return [s, R[0]]

hxx = h('kk1_' + str(777*random.random()))
sig = signSchnorr(P, message, hxx)
y = mulP(P, hxx)
dsa = ecdsa(P,message,hxx)
print "The verification of ecdsa signature  ", ecdsa_v(P,message,dsa,y)

writeNumber(sig[0],'s0')
writeNumber(sig[1],'s1')
writeNumber(y[0],'y0')
writeNumber(y[1],'y1')
len = 0
while 2**len < n4:
  len = len + 1
print "\nMore security checks "
print "bitlength ", len
print "\ncheck prime       ", pow(7,prime-1,prime) == 1 
print "prime order       ", pow(7,n4-1,n4) == 1 
print "period            ", P == mulP(P,n4+1) 

