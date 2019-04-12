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

ps = readNumber('ps') 

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
 while p % 6 != 5:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ =  5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43 * 47
  while True:
    while gcd(p, m_) != 1 or gcd(2*p+1, m_) != 1:
      p = p + 6 
    if (pow(7,p-1,p) != 1 or pow(7, 2*p, 2*p+1) != 1):
      p = p + 6
      continue
    return 2*p + 1

prime = 2**127 - 1

h = 1
n = ps - 1
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
  md.update( str(time.gmtime().tm_year + 0*time.gmtime().tm_mday))
  result = 0
  largestr = md.digest()
  for i in range(len(largestr)):
      result = (result << 8) ^ ord(largestr[i])
  return result

def addP(P,Q):
  return (P*Q) % ps 

def mulP(P,n):
  isFirst = True
  resP = P
  if n < 0:
    resP = inv(resP, ps-2)
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
  e = h(str(R) + m)
  return [(k - x*e) % n, e]

P = 17 * 17

print "Base point:\n", P
Q = mulP(P,random.randint(1,n))
print "Second point\n",Q

f = open(sys.argv[1],'r')
message = f.read()
f.close()

x = random256(sys.argv[1])
y = mulP(P,x)

#print "The public key for Schnorr's signature \n", y
writeNumber(y,'y')
#writeNumber(y[1],'y1')

sig = signSchnorr(P, message, x)

writeNumber(sig[0],'s0')
writeNumber(sig[1],'s1')

print "test Schnoor ", h(str(addP(mulP(P,sig[0]),mulP(y,sig[1]))) + message) == sig[1]

print "s ", sig
print "y ", y

#ps = nextPrime(2**800+17)
#writeNumber(ps,'ps')
print nextPrime(2**800) 