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

prime = nextPrime(2019 * (2**130))
a = prime - 5
b = 0
c = 17
while pow(c, (prime-1)/3, prime) == 1:
  c = c + 1
print "factor c = ", c
cinv = pow(c, prime-2, prime)
 
r = (prime + 1)/4
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
     s = ((3*c*(x1**2) - 5 + prime) * inv(2*y1, prime)) % prime
  else:  
     s = ((y1-y2) * inv(x1-x2, prime)) % prime
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

def ecdsa_v(G,m,S,Y):
  si = inv(S[0], r)
  hh = h(m + str(S[1]))
  u1 = (si * hh) % r
  u2 = (si * S[1]) % r
  return addP( mulP(G, u1), mulP(Y, u2) )[0] == S[1]

x = 1
if pow(c*x**3 - 5*x + prime, (prime - 1)/2, prime) != 1:
   x = prime - x
y = pow(c*x**3 - 5*x + prime, (prime + 1)/4, prime)
P = [x % prime, y % prime]
P = mulP(P, 4)

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
  return [(k - x*e) % r, e]

hxx = h('kk1_' + str(777*random.random()))
sig = signSchnorr(P, message, hxx)
y = mulP(P, hxx)
writeNumber(sig[0],'s0')
writeNumber(sig[1],'s1')
writeNumber(y[0],'y0')
writeNumber(y[1],'y1')

 
lb = r
cx = 0
while lb > 0:
  lb = lb/2
  cx = cx + 1
print "Bitlength ", cx
print "\nChallenege: a = p-5, b = 0, \n p = ", prime, "\n check prime   ", pow(7,prime-1,prime) == 1

print " check prime r ", pow(7,r-1,r) == 1
print " check period  ", mulP(P,r+1) == P
print "\n\nPx ", P[0]
print "Py ", P[1]

Q = mulP(P, random.randint(2,prime-2) )

print "Challenge: Find d, Q = d P "
print "\n\nQx ", Q[0]
print "Qy ", Q[1]


