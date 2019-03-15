import sys, math, hashlib, random, time

def writeNumber(number, fnam):
  f = open(fnam, 'wb')
  n = number
  while n > 0:
    byte = n % 256
    n = n / 256
    f.write(chr(byte))
  f.close()
 
def readNumber(fnam):
  f = open(fnam, 'rb')
  txt = f.read()
  f.close()
  number = 0 
  for c in reversed(txt):
    number = (number << 8) + ord(c)
  return number
 
# VERIFY SCHNORR
prime = 40094690950920881030683735292761468389214899724061
#
# A prime factor of RSA100
#
h = 1
n = prime
b = 0
a = 0

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

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x2 > x1:
    x2 = x2 - prime
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
     if (n & 1) != 0:   
         if isFirst:
            resP = PP
            isFirst = False
         else:
            resP = addP(resP,PP)
     PP = addP(PP, PP)
     n = n >> 1 
  return resP

P = [1,1]

f = open(sys.argv[1],'r')
message = f.read()
f.close()


sig = [readNumber('s0'), readNumber('s1')]
y = [readNumber('y0'), readNumber('y1')]

print "test Schnoor ", h(str(addP(mulP(P,sig[0]),mulP(y,sig[1]))[0]) + message) == sig[1]

print "s ", sig
print "y ", y