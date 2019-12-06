'''
  Schnorr Signature 
  Secure
  Simple curve: y^2 = x^3 - x (modulo prime)
  Hash SHA-256 
  PYthon 3

  Copyright (c) Scheerer Software 2019 - all rights reserved 
''' 

import sys, hashlib

def h(x):
  y = x.encode(encoding = 'UTF-8',errors = 'strict')
  out = 0 
  for bx in hashlib.sha256(y).digest():
    out = (out<<8) + bx
  return out

def hF(x):
  f = open(x, "rb")
  out = 0
  for bx in f.read():
    out = (out<<8) + bx
  f.close()
  return num2hextxt(out)

#
# p and (p+1) divied by 4 are primes
# There are (p+1) points on the curve.
# https://math.stackexchange.com/questions/319742/order-of-elliptic-curve-y2-x3-x-defined-over-f-p-where-p-equiv-3-m
#
def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 12 != 7:
   p = p + 1
 return nextPrime_(p)

def nextPrime_(p):
  m_ =  5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43 * 47
  while True:
    while gcd(p, m_) != 1 or gcd((p+1)>>2, m_) != 1:
      p = p + 12 
    if (pow(7,p-1,p) != 1 or pow(7, ((p+1)>>2) - 1, (p+1)>>2) != 1):
      p = p + 12
      continue
    return p

#
# (prime+1) divided by 4 ts prime
#
maxx = 131 * 2**131
prime = nextPrime( h('Franz Scheerer') % maxx )
print ("A prime greater than 2^131 \np = ", prime)

#
# Add point P and Q on the curve
#
def addP(P,Q):
  global prime
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = ((3*x1*x1 - 1) * pow(2*y1, prime-2, prime)) % prime
  else:  
     if x1 < x2:
        x1 = x1 + prime
     s = ((y1-y2) * pow(x1-x2, prime-2, prime)) % prime
  xr =  (s*s) - x1 - x2
  yr = s * (x1-xr) - y1 
  return [xr % prime, yr % prime]

#
# P + P + P + P + P + P --- n times
# 
def mulP(P,n):
  global prime
  resP = 'ZERO'
  PP = P
  while n != 0:
     if (n % 2 != 0):   
         if resP == 'ZERO':
            resP = PP
         else:
            resP = addP(resP,PP)
     PP = addP(PP, PP) 
     n >>= 1 
  return resP

def signSchnorr(G, m, x):
  global prime
  # k is different if message m is different
  k = h(m + 'key value') 
  R = mulP(G,k)
  e = h(str(R[0]) + m) % ((prime+1)>>2)
  return [(k - x*e) % ((prime+1)>>2), e]

#Generate the base point
x = 1234567
if pow(x**3 - x, (prime-1)>>1, prime) != 1:
   x = prime - x 
y = pow( x**3 - x, (prime+1)//4, prime)
P = [ x % prime, y % prime ]
#
# Choose P is in a subgrooup of order (p+1)//4
#
P = mulP(P, 4)

f = open(sys.argv[1],"rb")
message = hashlib.sha256(f.read()).hexdigest()
f.close()

privateKey = h( 'passwordX' ) # some random number
print("The base point is: ")
print("x: ",P[0])
print("y: ",P[1])

publicKey = mulP(P, privateKey)

print("The public key is the point: ")
print("x: ",publicKey[0])
print("y: ",publicKey[1])

sig = signSchnorr(P, message, privateKey)
print("The signature is: ")
print("s: ",sig[0])
print("e: ",sig[1])

#Verification
R = addP(mulP(P, sig[0]), mulP(publicKey, sig[1]))
check = h(str(R[0])+message) % ((prime+1)>>2) == sig[1]
print("\nResult of verification ", check)

