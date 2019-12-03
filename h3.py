import random, hashlib, sys

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
  squeezeSPZ(res, 32)
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out 

def hF(fnam):
  global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
  jSPZ = iSPZ = aSPZ = 0
  wSPZ = 1
  sSPZ = []
  ix = 0
  while ix < 256:
     sSPZ.append(ix)
     ix += 1
  f = open(fnam, 'rb')
  for c in f.read():
     absorb_byteSPZ(c)
  f.close() 
  res = []
  squeezeSPZ(res, 128)
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out 

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
  h__ =  ['0','1','2','3','4','5','6','7']
  h__ += ['8','9','a','b','c','d','e','f']
  while x > 0:
    res = h__[x & 0x0F] + res
    x >>= 4
  return res

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a
 
def nextPrime(p):
 while p % 6 != 5:
   p = p + 1
 return nextPrime_e3(p)

def nextPrime_e3(p):
  m = 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29
  while gcd(p,m) != 1:
    p = p + 6 
  if (pow(5,p-1,p) != 1):
      return nextPrime_e3(p + 6)
  return p
   
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

def h256(fnam):
  f=open(fnam,'rb')
  res = 0
  for c in hashlib.sha256(f.read()).digest():
     res = (res<<8) + c
  f.close()
  return res

def hS(x):
  y = x.encode(encoding = 'UTF-8',errors = 'strict')
  return hashlib.sha256(y).hexdigest()

def rsakeys():
  global nrsa, drsa
  a = 2
  b = 2**512
  p = nextPrime(random.randint(a,b))
  q = nextPrime(random.randint(a,b))
  drsa = inv(3, (p-1)*(q-1)//gcd(p-1,q-1) )
  nrsa = p * q
  print("n = \n", p*q)
  print("e = 3, \nd = ", drsa)

def mykeys(password):
  global nrsa, drsa
  a = h(password + 'A')
  a *= h(password + 'B') 
  b = h(password + 'AA')
  b *= h(password + 'BB') 
  p = nextPrime(a)
  q = nextPrime(b)
  drsa = inv(3, (p-1)*(q-1)//gcd(p-1,q-1) )
  nrsa = p * q
  print("n = \n", p*q)
  print("e = 3, \nd = ", drsa)


print ("\n\n hash h241 - copyright Scheerer Software 2019 all rights reserved\n\n")
print ("First parameter is H\n\n")

print("Random RSA keys are generated ...\n")
mykeys('franZ63...34')

if len(sys.argv) == 3 and sys.argv[1] == "H":
  print ("hash of file centent:\n " + num2code(hF(sys.argv[2])))
     
hash = h("The quick brown fox jumps over the lazy dog")
print ("The quick brown fox jumps over the lazy dog:\n h = ", num2hextxt(hash))
print ("SHA256: ", hS("The quick brown fox jumps over the lazy dog"))