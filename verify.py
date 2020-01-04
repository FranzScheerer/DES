'''
  Verify Schnorr Signature 
 
  Curve: y^2 = x^3 - x (modulo prime), (prime+1)//4 is prime
  Hash Md5
  Random Generator SPTITZ (secure variant, not included here)
  PYthon 3
  Message in line 120

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
#
# Note: The Schnorr Signature uses a NONCE together
# with the hash. It means, only 128 bits are
# required.
#
import hashlib
def h(x):
  b = hashlib.md5(x.encode()).digest()
  out = 0
  for bb in b:
      out = (out << 8) + bb
  return out     

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
ecc_prime = nextPrime( (h('''
password for gneration of  prime''')<<100) % maxx )
assert(ecc_prime > 2**141)
#
# The so called order of the subgroup,
# that is the period of the sequence of points.
# P, P + P, P + P + P, ...
#
ecc_n = (ecc_prime + 1)//4

print ("A prime greater than 2^141 \np = %x " % ecc_prime)

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
p = 34eda566700a887ba50ee4674bb239fb                                                
The base point is:                                                                  
x: 705b755147f6ea461f5c35bc40be810                                                  
y: 199a76a759da464ad7ffb6c4ba7f775d                                                 
The public key is the point:                                                        
x: 1f21c268859c2c2f743b1e28f319f0e0                                                 
y: 15e8348eeffe80e2bf71253e8170f450                                                 
The signature is:                                                                   
e: cfcfc0338626ee11c4ef1c102618e4                                                   
s: a43a6d25455815c31c5e22db12af664                                                  
The quick brown fox jumps over the lazy dog  
9e107d9d372bb6826bd81d3542a419d6       
                                                                                    
'''
#
# From this password the private key
# is calculated here
# PLEASE CHANGE - PLEASE CHANGE - PLEASE CHANGE
#

#Generate the base 

P = [0x2942b8228093955f3857f765d8dfbf60dc977,                            
     0x2aa80e88f527472d337610600679fc7d5802f] 

print("The base point is: ")
print("x: 0x%x" % P[0])
print("y: 0x%x" % P[1])
#publicKey = mulP(P, privateKey)
publicKey = [0x433459cdcae741392178e432418b66bf8351a,                               
             0x815330495bbb82730f40e07737976708637b3]                               
                                    
sig = {'e':0xff6bae22cc327c0d110502f39b996556,                            
's': 0xfc2c44ec1d591d14585226cdd8a152260d30} 

print("The public key is the point: ")
print("x: 0x%x" % publicKey[0])
print("y: 0x%x" % publicKey[1])

print("The signature is: ")
print("sig['e'] = 0x%x" % sig['e'])
print("sig['s'] = 0x%x" % sig['s'])

#Verification
P1 = mulP(P, sig['s'])
P2 = mulP(publicKey, sig['e'])
R = addP(P1, P2)
comp_e = h(str(R[0]) + message) % ecc_n
print("Result of verification: ", (comp_e == sig['e']))

