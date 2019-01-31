Public key: X:  164079056091893304496598158079835370395897756838020
Public key: Y:  44713375704124239879706199940669001579995441673616
Sigature    X:  31306173963428167314426322874431146638092078847107
Sigature    y:  102583995694037449180398472600671750899682402553781

The verification of signature  True

import random, hashlib, sys

nrabin = 743285923315061462317239833498483180761958757994944213727529869984547748056373360502506707496968738956644950396991750087839098301212127406814398995599338566286313743350150054031554184465950255519795337446125090866267720843656935494147556910369163957061645307670089704099131787942606141580039094320904715577L


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

def num2hextxt(x):
  res = ''
  h__ = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  while x > 0:
    res = h__[x % 16] + res
    x /= 16
  return res

def gcd(a,b):
  if b > a:
    a,b = b,a
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 4 != 3:
   p = p + 1
 return nextPrime_3(p)
  
def nextPrime_3(p):
  m_ = 3*5*7*11*13*17*19*23*29
  while gcd(p,m_) != 1:
    p = p + 4 
  if (pow(2,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(3,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(5,p-1,p) != 1):
      return nextPrime_3(p + 4)
  if (pow(17,p-1,p) != 1):
      return nextPrime_3(p + 4)
  return p
  
def h(x):
  dx1 = hashlib.sha512(x).digest()
  dx2 = hashlib.sha512(dx1+x).digest()
  dx3 = hashlib.sha512(x+dx2).digest()
  dx4 = hashlib.sha512(x+dx3).digest()
  dx5 = hashlib.sha512(x+dx4).digest()
  res = 0
  for cx in (dx1+dx2+dx3+dx4+dx5):
    res = (res<<8) ^ ord(cx)
  return res % (nrabin)


def root(m, p, q):
  while True:
    x = h(m)
    sig =   pow(p,q-2,q) * p * pow(x,(q+1)/4,q) 
    sig = ( pow(q,p-2,p) * q * pow(x,(p+1)/4,p) + sig ) % (nrabin) 
    if (sig * sig) % nrabin == x:
      print "write extended message to file m "
      f = open('m','w')
      f.write(m)
      f.close()
      break
    m = m + ' '
  return sig

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
  n = 0
  snum = f.read()
  for i in range(len(snum)):
    n = (n << 8) ^ ord(snum[len(snum)-i-1])   
  f.close()
  return n

def random512():
  md = hashlib.sha512("RANDOM-SEED")
  md.update('large key value for generation of random number')
  md.update( str(random.random()) )
  md.update( str(random.random()) )
  result = 0
  largestr = md.digest()
  for i in range(len(largestr)):
      result = (result << 8) ^ ord(largestr[i])
  return result

def random1024():
  return random512() * random512()

def hF():
  f = open("m",'r')
  return h(f.read())

def sF(fnam):
  p = readNumber("p")
  q = readNumber("q")

  f = open(fnam,'r')
  s = root (f.read(), p, q)
  f.close()
  return s

def vF(s):
  return hF() == (s * s) % nrabin
 
print "\n\n rabin signature - copyright Scheerer Software 2018 - all rights reserved\n\n"
print "First parameter is V (Verify) or S (Sign)\n\n"
print "\n\n verify signature (2 parameters):"
print "   > python rabin.py V <digital signature> "

print " create signature S (2 parameter):"
print "   > python rabin.py S <filename> \n\n"

print " number of parameters is " + str(len(sys.argv)-1)
print " "
print " "

if  len(sys.argv) == 3 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(hextxt2num(sys.argv[2])))

if len(sys.argv) == 3 and sys.argv[1] == "S":
  print " digital signature:\n " + num2hextxt(sF(sys.argv[2]))
     
                       
