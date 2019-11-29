import random, hashlib, sys

nrsa = 29746358878928083861237817222954677677152481785351811006421449568488007506618838431501380761939331839202115522100484371951305362698541726995193181514480854479235870344802990899716815205765298780141729114308584093033967074038423933744823970683410211257431791252652117523816679871100597902024086062137064382361

def updateSPZ():
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    iSPZ = (iSPZ + wSPZ) % 256
    jSPZ = sSPZ[(jSPZ + sSPZ[ iSPZ ]) % 256]
    sSPZ[ iSPZ ], sSPZ[ jSPZ ] = sSPZ[ jSPZ ], sSPZ[ iSPZ ]

def outputSPZ():
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    updateSPZ()
    return sSPZ[jSPZ]

def shuffleSPZ():
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    for v in range(256):
        updateSPZ()    
    wSPZ = (wSPZ + 2) % 256
    aSPZ = 0

def absorb_nibbleSPZ(x):
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    if aSPZ == 241:
        shuffleSPZ()
    sSPZ[aSPZ], sSPZ[240 + x] = sSPZ[240 + x], sSPZ[aSPZ]
    aSPZ = aSPZ + 1

def absorb_byteSPZ(b):
    absorb_nibbleSPZ(b % 16)
    absorb_nibbleSPZ(b >> 4)

def squeezeSPZ(out, outlen):
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    shuffleSPZ()
    for v in range(outlen):
        out.append( outputSPZ() )

def h(x):
  global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
  jSPZ = iSPZ = aSPZ = 0
  wSPZ = 1
  sSPZ = []
  ix = 0
  while ix < 256:
     sSPZ.append(ix)
     ix += 1
  for c in x:
     absorb_byteSPZ(ord(c)) 
  res = []
  squeezeSPZ(res, 128)
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out % (nrsa)

def bin2num(x):
  res = 0
  for c in x:
    res = (res<<8) ^ ord(c)
  return res

def num2bin(x):
  res = ''
  while x > 0:
    res = (x & 0xFF) + res
    x >>= 8
  return res

def digital2num(x):
  res = 0
  for c in x:
    if ord(c) >= 48 and ord(c) <= 57:
      res = (res*10) + ord(c) - 48
  return res

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
    x >>= 6
  return res


def num2hextxt(x):
  res = ''
  h__ = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  while x > 0:
    res = h__[x % 16] + res
    x >>= 4
  return res

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def issmooth(n,m):
  g = gcd(n,m)
  while True:
    n = n // g
    g = gcd(n,m)
    if g == 1:
      break
  return n == 1

def pp(x):
 i = ii = 1
 while i < x:
   i = i + 1
   if gcd(ii,i) == 1:
     ii = i * ii
 return ii
 
def nextPrime(p):
 if p % 2 == 0:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ = 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29
  while gcd(p,m_) != 1:
    p = p + 2 
  if (pow(2,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  if (pow(3,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  if (pow(5,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  if (pow(17,p-1,p) != 1):
      return nextPrime_odd(p + 2)
  return p

def nextP(r,limit):
  while r < limit: 
     r = r * 7
  return nextPrime(r)

def wgxxx():
  p = nextP(1689398, 2**400)
  q = nextP(49611, 2**401)
  writeNumber(inv(rsa129,(p-1)*(q-1)),'gxxx')
  print ("nrsa = ", p*q)
  
def pubkey(k1,k2):
  p = nextPrime(bin2num(k1) * 2**400)
  q = nextPrime(bin2num(k2) * 2**400)
  print ("nrsa = ", p*q)
  d =  inv(rsa129,(p-1)*(q-1))
  print ("e = ", d)
  writeNumber(inv(rsa129,(p-1)*(q-1)),'gxxx')
   
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


def random512():
  md = hashlib.sha512("RANDOM-SEED")
  md.update('large key value for generation of random number')
  md.update( str(random.random()) )
  md.update( str(random.random()) )
  result = 0
  largestr = md.digest()
  for cx in largestr:
      result = (result << 8) ^ ord(cx)
  return result

def random1024():
  return random512() * random512()

def hF(fnam):
  f = open(fnam,'r')
  return h(f.read())

def sF(fnam):
  f = open(fnam,'r')
  s = pow (h(f.read()), readNumber('gxxx'), nrsa)
  f.close()
  return s

def vF(fnam,s):
  f = open(fnam,'r')
  return  h(f.read()) == pow (s, rsa129, nrsa)
 
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

rsa129 = 2**7 - 1

print ("\n\n rsacrypt - copyright Scheerer Software 2017 - 2019 all rights reserved\n\n")
print ("First parameter is V,S,E or D\n\n")
print ("\n\n verify signature (3 parameters):")
print ("   > python rsacrypt.py V <filename> <digital signature> ")

print (" create signature S (2 parameter):")
print ("   > python rsacrypt.py S <filename> \n\n")
print (" encrypt E (2 parameter):")
print ("   > python rsacrypt.py E <text> \n\n")
print (" decrypt D (2 parameter):")
print ("   > python rsacrypt.py D <bigInteger> \n\n")

print (" number of parameters is " + str(len(sys.argv)-1))
print (" ")
print (" ")

nrsa = readNumber('n')
if len(sys.argv) == 3 and sys.argv[1] == "E":
  print ("encrypted text: \n" + str (pow(bin2num(sys.argv[2]), readNumber('gxxx'), nrsa)))

if len(sys.argv) == 3 and sys.argv[1] == "D":
  print (" decrypt text:\n " + num2bin(pow (digital2num(sys.argv[2]),rsa129,nrsa))) 

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print ("result of verification: " + str(vF(sys.argv[2], code2num(sys.argv[3]))))

if len(sys.argv) == 3 and sys.argv[1] == "S":
  print (" digital signature:\n " + num2code(sF(sys.argv[2])))
     
#m = pp(25000)
#x = 2**50
#for i in range(25):
#  cnt = 0
#  x = x * 2
#  for j in range(600000):
#    if issmooth(x+j,m):
#      cnt = cnt + 1
#  print x, " - ", cnt


#print np(random512())
 
#p1 = nextPrime(random512())
#p2 = nextPrime(random512())
#n = p1*p2
#e = rsa129
#d = inv(e,( (p1-1)*(p2-1) )/gcd(p1-1,p2-1)) 
#writeNumber(d,'gxxx')
#writeNumber(n,'nrsa')
#print "n = ", n
