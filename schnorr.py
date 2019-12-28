'''
  Schnorr Signature 
  Secure
  Simple curve: y^2 = x^3 - x (modulo prime)
  Hash h241 
  PYthon 3
  Message in line 177
  Copyright (c) Scheerer Software 2019 - all rights reserved 
''' 
ecc_a = -1
ecc_n = 1
ecc_b = 0
ecc_prime = 0

def update241():
    global a241, i241, j241, w241, s241
    i241 = (i241 + w241) % 256
    j241 = s241[(j241 + s241[i241]) % 256]
    s241[i241], s241[j241] = s241[j241], s241[i241]

def output241():
    global a241, i241, j241, w241, s241
    update241()
    return s241[j241]

def shuffle241():
    global a241, i241, j241, w241, s241
    for v in range(256):
        update241()    
    w241 = (w241 + 2) % 256
    a241 = 0

def absorb_nibble241(x):
    global a241, i241, j241, w241, s241
    if a241 == 63:
        shuffle241()
    s241[a241], s241[240 + x] = s241[240 + x], s241[a241]
    a241 = a241 + 1

def absorb_byte241(b):
    absorb_nibble241(b % 16)
    absorb_nibble241(b >> 4)

def h(x):
  global a241, i241, j241, w241, s241
  i241 = j241 = a241 = 0
  w241 = 1
  s241 = []
  for ix in range(256):
    s241.append(ix)
  for c in x.encode():
     absorb_byte241(c) 
  shuffle241()
  shuffle241()
  shuffle241()
  out = 0 
  for bx in range(32):
    out = (out<<8) + output241()
  return out

def num2hextxt(x):
  res = ''
  h__ =  ['0','1','2','3','4','5','6','7','8','9']
  h__ += ['a','b','c','d','e','f']
  while x > 0:
    res = h__[x % 16] + res
    x >>= 4
  return res


'''
 p and (p+1) divied by 4 are primes
 There are (p+1) points on the curve.
 https://math.stackexchange.com/questions/319742/order-of-elliptic-curve-y2-x3-x-defined-over-f-p-where-p-equiv-3-m
'''
def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 12 != 7:
   p = p + 1
 return nextPrime_(p)

def nextPrime_(p):
  m =  5 * 7 * 11 * 13 * 17 * 19 * 23
  m *= 29 * 31 * 37 * 41 * 43 * 47
  while True:
    q = (p+1)//4
    while gcd(p, m) != 1 or gcd(q, m) != 1:
      p = p + 12 
      q = q + 3
    if (pow(7,p-1,p) != 1 or pow(7, q - 1, q) != 1):
      p = p + 12
      continue
    return p

'''
 The numbers prime and (prime+1) divided by 4 
 are both primes.
'''
maxx = 131 * 2**141
ecc_prime = nextPrime( h('Franz Scheerer') % maxx )
ecc_n = (ecc_prime + 1)//4
'''
 This prime is safe
''' 
print ("A prime greater than 2^141 \np = ", ecc_prime)

'''
 Add point P and Q 
 P and Q are Points 
 on the elliptic curve
'''
def addP(P,Q):
  global ecc_prime, ecc_a
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = ((3*x1*x1 + ecc_a) * pow(2*y1, ecc_prime-2, ecc_prime)) % ecc_prime
  else:  
     if x1 < x2:
        x1 = x1 + ecc_prime
     s = ((y1-y2) * pow(x1-x2, ecc_prime-2, ecc_prime)) % ecc_prime
  xr =  (s*s) - x1 - x2
  yr = s * (x1-xr) - y1 
  return [xr % ecc_prime, yr % ecc_prime]

'''
 n times the point P 
 P + P + P + P + P + P --- 
 is calculated using double and add.
'''
def mulP(P,n):
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
  global ecc_prime, ecc_n  
  # k is different if message m is different
  k = h(m + 'key value') 
  R = mulP(G,k)
  e = h(str(R[0]) + m) % ecc_n
  return [(k - x*e) % ecc_n, e]

message = '''
In cryptography, a Schnorr signature is a digital signature
produced by the Schnorr signature algorithm that was described 
by Claus Schnorr. It is a digital signature scheme known for its
simplicity,[1] among the first whose security is based on the 
intractability of certain discrete logarithm problems.[1] 

It is efficient and generates short signatures.[1]

It was covered by U.S. Patent 4,995,082 which expired in February 2008.

OUTPUT:
A prime greater than 2^141                                               
p =  248359970965070966100215621849780240684422603                       
The base point is:                                                       
[x,y]:                                                                   
 [213754921596700185067212257272351079152087106,
 184543119823406368705642531585330069262456675]                                                 
The public key is the point: 
x:  100979136531575180417606819986092376219612918
y:  183736627514541634395430962528019329021853594
                                                                         
Result of verification  True                                             
The quick brown fox jumps over the lazy dog:                             
 h =  30e0c479a075a25de6af2e52a7f2ab7120b36b68bc7643ba4c26aa6b6e54c4c    
The next prime                                                           
 515377520732011331036461129765621272702107569243                        

'''
#
# From this password the private key
# is calculated here
#
privateKey = h( 'passwordX' ) # some random number
#Generate the base point
x = 1234567
while pow(x**3 + ecc_a*x + ecc_b, (ecc_prime-1)//2, ecc_prime) != 1:
   x = x + 1 
y = pow( x**3 + ecc_a*x + ecc_b, (ecc_prime+1)//4, ecc_prime)
P = [ x , y ]
# To get a base point with prime order
P = mulP(P, 4)

print("The base point is: ")
print("x: ",P[0])
print("y: ",P[1])

publicKey = mulP(P, privateKey)

print("The public key is the point: ")
print("x: ",publicKey[0])
print("y: ",publicKey[1])
#
# The signature is calculatet as function of
#
# Base pont P
# the message to sign
# and the private Key 
# that must be kept secret 
# 
sig = signSchnorr(P, message, privateKey)
print("The signature is: ")
print("s: ",sig[0])
print("e: ",sig[1])

#Verification
R = addP(mulP(P, sig[0]), mulP(publicKey, sig[1]))
check = h(str(R[0])+message) % ((ecc_prime+1)>>2) == sig[1]
print("\nResult of verification ", check)

hash = h("The quick brown fox jumps over the lazy dog")
print ("The quick brown fox jumps over the lazy dog:\n h = ", num2hextxt(hash))

print("The next prime\n", nextPrime(3**100))
ecc_a = 0
ecc_b = 7
ecc_prime = 2**256 - 2**32 - 977
ecc_n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
#Generate the base point
x = 1234567
while pow(x**3 + ecc_a*x + ecc_b, (ecc_prime-1)//2, ecc_prime) != 1:
   x = x + 1 
y = pow( x**3 + ecc_a*x + ecc_b, (ecc_prime+1)//4, ecc_prime)
P = [ x , y ]
#print(mulP(P,ecc_n + 1))
#print(P)
sig = signSchnorr(P, message, privateKey)
#Verification
publicKey = mulP(P,privateKey)
R = addP(mulP(P, sig[0]), mulP(publicKey, sig[1]))
check = h(str(R[0])+message) % ecc_n == sig[1]
print("\nResult of verification ", check)
