'''
E: Set of points with
   y^2 = (x^3 - x) mod p 
plus neutral element at infinity defines a smooth elliptic curve.
p := (2^160 * 5 * 23) + 86427
is a prime number.

The number
n4 := (p + 1) / 4
is also a prime. 
G is specially chosen point on the curve E, 
such that n4 is the order of the subgroup of that point G.
'''
import sys, math, hashlib, random, time

def writeNumber(number, fnam):
  f = open(fnam, 'wb')
  n = number
  while n > 0:
    byte = n % 256
    n = n / 256
    f.write(chr(byte))
  f.close()

# must be of the form 4k + 3 = 4(k+1) - 1
# prime from NIST
prime = 2**256 - 2**224 + 2**192 + 2**96 - 1
 
def bin2num(x):
  res = 0
  for c in x:
    res = (res<<8) ^ ord(c)
  return res

def num2bin(x):
  res = ''
  while x > 0:
    res = chr(x % 256) + res
    x /= 256
  return res

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 3 != 2 or p % 2 != 1:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ = 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29
  while True:
    while gcd(p,m_) != 1:
      p = p + 6 
    q = (p+1)/4
    if (pow(2,p-1,p) != 1 or pow(2,q-1,q) != 1):
       p = p + 6
       continue
    if (pow(3,p-1,p) != 1 or pow(3,q-1,q) != 1):
       p = p + 6
       continue
    if (pow(5,p-1,p) != 1 or pow(5,q-1,q) != 1):
       p = p + 6
       continue
    if (pow(17,p-1,p) != 1 or pow(17,q-1,q) != 1):
       p = p + 6
       continue
    break
  return p

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

def E(m, key, prime):
  return pow(m, key, prime)

def D(c, key, prime):
  key = inv(key, prime - 1)
  return pow(c, key, prime)

def hextxt2num(x):
  res = 0
  for c in x:
    if ord(c) < 58 and ord(c) >= 48:
       res = (res<<4) + ord(c) - 48
    elif ord(c) <= ord('f') and ord(c) >= ord('a'):
       res = (res<<4) + ord(c) - 87
  return res

#bhex = "5ac635d8 aa3a93e7 b3ebbd55 769886bc 651d06b0 cc53b0f6 3bce3c3e 27d2604b" 
#b = hextxt2num(bhex)
#prime = nextPrime(2**170)
prime = 1496577676626844588240573268701473812127674924030189L
b = 7
a = 0
def code2num(x):
  res = 0
  for c in x:
     if ord(c) >= 48 and ord(c) < 58:
       res = (res << 6) + ord(c) - 48
     if ord(c) >= 65 and ord(c) < 91:
       res = (res << 6) + ord(c) - 55
     if ord(c) >= 97 and ord(c) < 123:
       res = (res << 6) + ord(c) - 61
     if c == '#': 
       res = (res << 6) + 62
     if c == '/': 
       res = (res << 6) + 63
  return res

def num2code(x):
  res = ''
  while x > 0:
    y = x % 64
    if y < 10:
       res = chr( y + 48 ) + res
    elif y < 36:
       res = chr( y + 55 ) + res
    elif y < 62:
       res = chr( y + 61 ) + res 
    elif y == 62:
       res = '#' + res 
    elif y == 63:
       res = '/' + res 
    x /= 64
  return res


def h(x):
  dx1 = hashlib.sha256(x).digest()
  res = 0
  for cx in (dx1):
    res = (res<<8) ^ ord(cx)
  return res % n4

def random256(m):
  md = hashlib.sha256("***RANDOM-SEED_X***")
  md.update('large key value for generation of random number')
  md.update( m )
  result = 0
  largestr = md.digest()
  for i in range(len(largestr)):
      result = (result << 8) ^ ord(largestr[i])
  return result

def randomX(m):
  md = hashlib.sha256("***RANDOM-SEED_X***")
  md.update('large key value for generation of random number')
  md.update( m )
#  md.update( str(random.randint(0, 999999999999)) )
  md.update( str(time.gmtime().tm_year + time.gmtime().tm_mday))
  result = 0
  largestr = md.digest()
  for i in range(len(largestr)):
      result = (result << 8) ^ ord(largestr[i])
  return result

def genP(y,b):
   yy = (y * y - b) % (prime)
   x = pow(yy, inv(3, prime-1), prime)
   return [(x) % prime, (y) % prime]

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

def signSchnorr(G,m,x):
  k = randomX(m)
  R = mulP(G,k)
  e = h(str(R[0]) + m)
  return [(k - x*e) % n4, e]

def ecdsa(G,m,x):
  k = randomX(m)
  R = mulP(G,k)
  hh = h(m+str(R[0]))
  s = ( inv(k,n4) * (hh + R[0]*x) ) % n4
  return [s, R[0]]

def ecdsa_v(G,m,S,Y):
  si = inv(S[0], n4)
  hh = h(m + str(S[1]))
  u1 = (si * hh) % n4
  u2 = (si * S[1]) % n4
  return addP( mulP(G, u1), mulP(Y, u2) )[0] == S[1]



# The starting point which is added many times to itself 
#cinv = inv(c, prime)
P = genP(17, b)
n4 = (prime+1) / 90
P = mulP(P,90)

print mulP(P, prime+2)
print P
print "Primzahl ", prime


#Q = P = [2,2]
#for xx in range(10):
#  if mulP(P,xx+2) == P: 
#    print "ERROR ", xx

# mulP(P,n_) to test mulP(P,b_) is infty :)

f = open(sys.argv[1],'r')
message = f.read()
f.close()

x = 2*random256(sys.argv[1]) + 1
y = mulP(P,x)

#print "The public key for Schnorr's signature \n", y
writeNumber(y[0],'y0')
writeNumber(y[1],'y1')

#sig = signSchnorr(P, message, x)
sig = ecdsa(P, message, x)
print "Verify: ", ecdsa_v(P,message,sig,y)

writeNumber(sig[0],'s0')
writeNumber(sig[1],'s1')


print "test Schnoor ", h(str(addP(mulP(P,sig[0]),mulP(y,sig[1]))[0]) + message) == sig[1]


#print "Schnorr's signature: ", sig
#sig = [-1292541924106963660360868782867113836640471570935670569480312947333642626935647627L, 104703152638071622131923639130501753836895585613487714321614770491877799248030L]
#y=[27762649179563285105647484721445015479861271674141761119854131955025690103024L, 20688193634345669388836031406765716102383163783280129571842259728849528226163L]

# The public keys
#privAlice = 85743857348573489891704994859049170499485904
#privBob = 455457456346534563457893499994859049170499485904*1111
# We calulate the public keys
#pubkAlice = mulP(P, privAlice)
#print "Public Key from Alice \n", pubkAlice  
#pubkBob = mulP(P, privBob)
#print "Public Key from Bob \n", pubkBob  

#shareBob   = mulP(pubkAlice, privBob)
#shareAlice = mulP(pubkBob, privAlice)

#print "\n\nThe shared key as calculated from Alice\n", shareAlice 

#print "\n\n"
#print "Verification: Are the shared keys equal? ", shareAlice == shareBob

#key = 12344567
#ikey = inv( key, prime + 1 )
#Pm = mulP(pubkAlice, h('Karo Ass'))
#print "encrypt/decrypt test: ", mulP(mulP(Pm, key),ikey) == Pm
# test Schnorr Identifikacation
#G = Pm
#x=12312878789789
#y = mulP(G,x)
#e = 8878578945748989578
#k = 5849547584657846777
#r = mulP(G,k)

#s = (k + e*x) % n_
#print " Schnorr-Identifikation: test ... ", mulP(G, s) == addP(r,mulP(y,e))
#
# Die Primzahl von Hans Riesel ;)
#
#p = 2**3217 - 1
#k = 1785968598548549*2**80 + 1
#k_inv = inv(k, prime + 1)
#kk = 1777777777777*2**99 + 1
#kk_inv = inv(kk, prime + 1)

#print "The secret ... ", k,kk
#m = "Secret message from Bob to Alice"
#print "Message: ", m

#number = bin2num(m)
#print "Message converted to a number: \n", number
#x = number
#if pow (c*x**3 + a*x, (prime-1)/2, prime) != 1:
#  x = prime - x
#P_ = [x, pow (c*x**3 + a*x, (prime+1)/4, prime)]
#e_ = mulP(P_,k)
#print "\n encrypted point is sent to Alice\n", e_
#ee_ = mulP(e_,kk)
#print "\n Point sent to Bob, encrypted twice\n", ee_
#d1 = mulP(ee_,k_inv)
#print "\n Single encrypted point is send to Alice: \n", d1
#mm = mulP(d1, kk_inv)[0]
#if mm > (prime+1)/2:
#  mm = prime - mm
#mm = num2bin(mm)
#print "\n Encrypred by Alice: ", mm

#print "Does it work, is mm = m? ", mm == m

#print prime - (2**160) * 115
#a=7
#b=7
#import math
#for px in range(3500):
#  prime = 4*(px+1) + 3
#  if pow(7, prime-1, prime) == 1:
#    x=0
#    sq = math.sqrt(prime)
#    while pow(x**3 + a*x + b,(prime-1)/2,prime) != 1:
#      x = x + 1
#    y = pow(x**3 + a*x + b,(prime+1)/4,prime)
#    Q = P = [x,y]
#    Q = addP(Q,P)
#    n = 3
#    while Q[0] != P[0]:
#      n = n + 1
#      Q = addP(Q,P)
#    if n - prime - 1 > sq:
#      print prime, " ", n - prime - 1


  
