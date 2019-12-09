import random, math, hashlib, sys

def writeNumber(n, fnam):
  f = open(fnam, 'wb')
  while n > 0:
    b = n & 0xFF
    n >>= 8
    f.write(bytes([b]))
  f.close()

def readNumber(fnam):
  f = open(fnam, 'rb')
  n = 0
  for c in reversed(f.read()):
    n = (n << 8) ^ c   
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
#
# The curve eccp131 from the famous ecc challenge
# The cost to crack the DLP is at least 20000$
#  
prime = hextxt2num("05 177B8A2A 0FD6A4FF 55CDA06B 0924E125 F86CAD9B")
a = hextxt2num("04 3182D283 FCE38807 30C9A2FD D3F60165 29A166AF")
b = hextxt2num("02 0C61E945 9E53D887 1BCAADC2 DFC8AD52 25228035") 
n4 = hextxt2num("05 177B8A2A 0FD6A4FF 55CCA7B8 A1E21C88 BD53B2C1")
  
def inv(b,m):
  s = 0
  t = 1
  a = m
  while b != 1:
    q = a//b
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
  dx1 = hashlib.sha256(x.encode(encoding = 'UTF-8',errors = 'strict')).hexdigest()
  res = 0
  for cx in (dx1):
    res = (res<<8) ^ ord(cx)
  return res % n4

def genP(x,a,b):
   while pow(x**3 + a*x + b, (prime - 1)//2, prime) != 1:
     x = x + 1
   y = pow(x**3 + a*x + b, (prime + 1)//4, prime)
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
     n = n // 2
  return resP

def verify(G,s,Y,e,m):
  return e == h(str(addP(mulP(G,s),mulP(Y,e))[0]) + m)

def ecdsa_v(G,m,S,Y):
  si = inv(S[0], n4)
  hh = h(m + str(S[1]))
  u1 = (si * hh) % n4
  u2 = (si * S[1]) % n4
  return addP( mulP(G, u1), mulP(Y, u2) )[0] == S[1]

xx = 1
while pow(xx**3 + a*xx + b, (prime - 1)//2, prime) != 1:
  xx = xx + 1
yy = pow(xx**3 + a*xx + b, (prime + 1)//4, prime)

P = [xx,yy]

f = open(sys.argv[1], 'r')
message = f.read()
f.close()

y = [readNumber('y0'), readNumber('y1')]
sig = [readNumber('s0'), readNumber('s1')]

print( "Public key: X: ", y[0] % prime)
print( "Public key: Y: ", y[1] % prime)
print( "Sigature    X: ", sig[0])
print( "Sigature    y: ", sig[1])
print( "" )
print( "The verification of signature ", verify(P, sig[0], y, sig[1], message))
x = random.randint(2,n4-1)
ydsa = mulP(P,x)

def ecdsa(G,m,x):
  k = h(m + 'ecdsa')
  R = mulP(G,k)
  hh = h(m + str(R[0]))
  s = ( inv(k,n4) * (hh + R[0]*x) ) % n4
  return [s, R[0]]

sig = ecdsa(P, message, x)

print( "The verification of ecdsa signature ", ecdsa_v(P,message,sig, ydsa))


def signSchnorr(G,m,x):
  # pseudo random k, allways different for different messages m
  k = h(m + 'kk2') 
  R = mulP(G,k)
  e = h(str(R[0]) + m)
  return [(k - x*e) % n4, e]

onetime_private_key = h('kk1_' + str(random.randint(2,n4-1)))
sig = signSchnorr(P, message, onetime_private_key)
y = mulP(P, onetime_private_key) # The public key required to verify signature
writeNumber(sig[0],'s0')
writeNumber(sig[1],'s1')
writeNumber(y[0],'y0')
writeNumber(y[1],'y1')
#
# base point P or P' - it doesn't matter,
# since
# a P = Q
# b P'= Q => aP = bP'
# P' = cP => b = a/c
#
len = 0
while 2**len < n4:
  len = len + 1
print ("\nMore security checks ")
print ("bitlength ", len)
print ("\ncheck prime       ", pow(7,prime-1,prime) == 1) 
print ("prime order       ", pow(7,n4-1,n4) == 1) 
print ("period            ", P == mulP(P,n4+1)) 
  