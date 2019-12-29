'''
  Secure Schnorr Signature 
 
  Curve: y^2 = x^3 - x (modulo prime), (prime+1)//4 is prime
  Hash Spritz (a secure variant)
  PYthon 3
  Message in line 172

  Copyright (c) Scheerer Software 2019 - all rights reserved 
''' 
#
# The domain parameters of the elliptic curve
#
# To use ECC, all parties must agree on all the elements 
# defining the elliptic curve, that is, the domain parameters
# of the scheme.
#
ecc_a = -1
ecc_n = "no value assigned yet"
ecc_b = 0
ecc_prime = "no value assigned yet"

def update_h():
    global a_h, i_h, j_h, w_h, s_h
    i_h = (i_h + w_h) % 256
    j_h = s_h[(j_h + s_h[i_h]) % 256]
    s_h[i_h], s_h[j_h] = s_h[j_h], s_h[i_h]

def output_h():
    global a_h, i_h, j_h, w_h, s_h
    update_h()
    return s_h[j_h]

def shuffle_h():
    global a_h, i_h, j_h, w_h, s_h
    for v in range(256):
        update_h()    
    w_h = (w_h + 2) % 256
    a_h = 0

def absorb_nibble_h(x):
    global a_h, i_h, j_h, w_h, s_h
    if a_h == 63:
        shuffle_h()
    s_h[a_h], s_h[240 + x] = s_h[240 + x], s_h[a_h]
    a_h = a_h + 1

def absorb_byte_h(b):
    absorb_nibble_h(b % 16)
    absorb_nibble_h(b >> 4)

def h(x):
  global a_h, i_h, j_h, w_h, s_h
  i_h = j_h = a_h = 0
  w_h = 1
  s_h = list(range(256))
  for c in x.encode():
     absorb_byte_h(c) 
#
# shuffle three times      
# really very save
#
  shuffle_h()
  shuffle_h()
  shuffle_h()
  out = 0 
  size = 32 # 256 output bits
  cnt = 0
  while cnt < size: 
    out = ( out << 8 ) + output_h()
    cnt = cnt + 1 
    
  return out

def num2hextxt(x):
  res = ''
  hex =  list('0123456789abcdef')
  while x > 0:
    res = hex[x % 16] + res
    x >>= 4
  return res

'''
 p and (p+1) divied by 4 are primes
 There are (p+1) points on the curve.
 https://math.stackexchange.com/questions/319742/
 order-of-elliptic-curve-y2-x3-x-defined-over-
 f-p-where-p-equiv-3-m
'''
def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 12 != 7:
   p = p + 1
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
#
# The so called order of the subgroup,
# that is the period of the sequence of points.
# P, P + P, P + P + P, ...
#
ecc_n = (ecc_prime + 1)//4

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
  return {'s': (k - x*e) % ecc_n, 'e': e}

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
p =  8382083088130818198057506480161002632392363
The base point is: 
x:  2400903933844834017113403539491540283138712
y:  3281438224871239470173532295957803652647917
The public key is the point: 
x:  1383784377075446170610817616465588368645567
y:  1328568639004457085982642885570687641791144
The signature is: 
s:  896103487225214507160629533521853058887545
e:  306904037606407358103986197421651853250429

Result of verification  True
The quick brown fox jumps over the lazy dog:
 h =  ec88926b1a9daab6e56ef4be30f9ff5b480fdb80c3a7048405880364e3e134f5
The next prime greater than 2^300 is
 515377520732011331036461129765621272702107569243

Result of verification (secp256k1)  True

'''
#
# From this password the private key
# is calculated here
# PLEASE CHANGE - PLEASE CHANGE - PLEASE CHANGE
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
# message:
# the message to sign
# private key: 
# that must be kept secret 
# 
sig = signSchnorr(P, message, privateKey)
print("The signature is: ")
print(sig)

#Verification
R = addP(mulP(P, sig['s']), mulP(publicKey, sig['e']))
check = h(str(R[0])+message) % ((ecc_prime+1)>>2) == sig['e']
print("\nResult of verification ", check)

hash = h("The quick brown fox jumps over the lazy dog")
print ("The quick brown fox jumps over the lazy dog:\n h = ", num2hextxt(hash))

print("The next prime greater than 3^100 is\n", nextPrime(3**100))
'''
  secp256k1 - just to check it!
'''  
ecc_a = 0
ecc_b = 7
ecc_prime = 2**256 - 2**32 - 977
ecc_n = ecc_prime - 432420386565659656852420866390673177326
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
R = addP(mulP(P, sig['s']), mulP(publicKey, sig['e']))
check = h(str(R[0])+message) % ecc_n == sig['e']
print("\nResult of verification (secp256k1) ", check)

print("It is the difference ", ecc_prime-ecc_n)


