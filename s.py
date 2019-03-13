import sys, math, hashlib, random, time

def writeNumber(number, fnam):
  f = open(fnam, 'wb')
  n = number
  while n > 0:
    byte = n % 256
    n = n / 256
    f.write(chr(byte))
  f.close()
 
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
 while p % 8 != 3 or p % 3 != 2:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ = 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29
  while True:
    while gcd(p,m_) != 1:
      p = p + 24 
    q = (p+1)/4/3
    if (pow(2,p-1,p) != 1):
       p = p + 24
       continue
    if (pow(3,p-1,p) != 1):
       p = p + 24
       continue
    if (pow(5,p-1,p) != 1):
       p = p + 24
       continue
    if (pow(17,p-1,p) != 1):
       p = p + 24
       continue
    break
  return p

prime = 1393796574908163946345982392040522594173643
#print "prime - 2^140 ", prime - 2**140
h_ = 1
n4 = (prime + 0)/h_
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

def genP(x,a,b):
   while (pow(x**3 + a*x + b, (prime - 1) / 2, prime) != 1):
     x = x + 1
   y = pow(x**3 + a*x + b, (prime + 1) / 4, prime)
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
  hh = h(m+str(R[0] % n4))
  s = ( inv(k,n4) * (hh + (R[0] % n4)*x) ) % n4
  return [s, R[0] % n4]

def ecdsa_v(G,m,S,Y):
  si = inv(S[0], n4)
  hh = h(m + str(S[1]))
  u1 = (si * hh) % n4
  u2 = (si * S[1]) % n4
  return addP( mulP(G, u1), mulP(Y, u2) )[0] % n4 == S[1]

#P = genP(17,a,b)
#P = mulP(P, h_)
P = [1,1]

print "Base point:\n", P
Q = mulP(P,random.randint(1,n4))
print "Second point\n",Q

f = open(sys.argv[1],'r')
message = f.read()
f.close()

x = random256(sys.argv[1])
y = mulP(P,x)

#print "The public key for Schnorr's signature \n", y
writeNumber(y[0],'y0')
writeNumber(y[1],'y1')

#sig = signSchnorr(P, message, x)
sig = ecdsa(P, message, x)
print "Verify: ", ecdsa_v(P,message,sig,y)

writeNumber(sig[0],'s0')
writeNumber(sig[1],'s1')

#print sig

print "test Schnoor ", h(str(addP(mulP(P,sig[0]),mulP(y,sig[1]))[0]) + message) == sig[1]

#h = 2**256
#for i in range(10):
#  h = nextPrime(h)
#  print "\n", h
#  h = h + 1
