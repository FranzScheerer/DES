'''
  Schnorr Signature 
  Secure
  Simple curve: y^2 = x^3 - x (modulo prime)
  Hash h241 
  PYthon 3
  Message in line 177
  Copyright (c) Scheerer Software 2019 - all rights reserved 
''' 

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
    if a241 == 241:
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
  m_ =  5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43 * 47
  while True:
    while gcd(p, m_) != 1 or gcd((p+1)>>2, m_) != 1:
      p = p + 12 
    if (pow(7,p-1,p) != 1 or pow(7, ((p+1)>>2) - 1, (p+1)>>2) != 1):
      p = p + 12
      continue
    return p

'''
 The numbers prime and (prime+1) divided by 4 
 are both primes.
'''
maxx = 131 * 2**141
prime = nextPrime( h('Franz Scheerer') % maxx )
'''
 This prime is safe
''' 
print ("A prime greater than 2^141 \np = ", prime)

'''
 Add point P and Q 
 P and Q are Points 
 on the elliptic curve
'''
def addP(P,Q):
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

'''
 n times the point P 
 P + P + P + P + P + P --- 
 is calculated using double and add.
'''
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
y = pow( x**3 - x, (prime+1)>>2, prime)
P = [ x % prime, y % prime ]
# To get a base point with prime order
P = mulP(P, 4)

message = '''
Elliptische Kurven über dem Körper der reellen Zahlen können als die Menge 
aller (affinen) Punkte 

{\displaystyle (x,y)\in \mathbb {R} ^{2}} (x,y)\in {\mathbb  {R}}^{2} angesehen werden, 
die die Gleichung

{\displaystyle y^{2}=x^{3}+ax+b} y^{2}=x^{3}+ax+b

erfüllen, zusammen mit einem sogenannten Punkt im Unendlichen 
(notiert als {\displaystyle \infty } \infty  oder {\displaystyle {\mathcal {O}}} {\mathcal  O}).
Die (reellen) Koeffizienten {\displaystyle a} a und {\displaystyle b} b müssen 
dabei die Bedingung erfüllen, dass für die Diskriminante des kubischen Polynoms 
in {\displaystyle x} x auf der rechten Seite 
{\displaystyle -4a^{3}-27b^{2}\neq 0} {\displaystyle -4a^{3}-27b^{2}\neq 0} gilt,
 um Singularitäten auszuschließen 
(die Wurzeln des Polynoms sind dann paarweise verschieden, 
die Kurve hat keine Doppelpunkte oder andere Singularitäten).
'''

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

hash = h("The quick brown fox jumps over the lazy dog")
print ("The quick brown fox jumps over the lazy dog:\n h = ", num2hextxt(hash))

print("The next prime\n", nextPrime(3**100))

