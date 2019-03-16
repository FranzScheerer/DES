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
prime = 2**127 - 1
n = prime
b = 0
a = 0

def h(x):
  dx = hashlib.sha256(x).digest()
  res = 0
  for cx in dx:
    res = (res<<8) ^ ord(cx)
  return res % prime

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = ((3*(x1**2) + a) * pow(2*y1, prime-2, prime)) % prime
  else:
     s = ((y1-y2) * pow(x1-x2, prime-2, prime)) % prime
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

print "Signature ", sig[0]
print "signature ", sig[1]
print "Public Key ", y[0]
print "Public Key ", y[1]
