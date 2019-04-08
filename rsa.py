import random, hashlib, sys

nrsa =  19118832000105763637938157152850467974273167818828649375827825148849964309807866314390379881226224652434132598287639675152101593061907171227851105919168683025350974887841508141070136389244359833771900938550228403669389043766459235557858070265875058027244065551

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


def num2hextxt(x):
  res = ''
  h__ = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  while x > 0:
    res = h__[x % 16] + res
    x /= 16
  return res

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def issmooth(n,m):
  g = gcd(n,m)
  while True:
    n = n / g
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
  print "nrsa = ", p*q
  
def pubkey(k1,k2):
  p = nextPrime(bin2num(k1) * 2**400)
  q = nextPrime(bin2num(k2) * 2**400)
  print "nrsa = ", p*q
  d =  inv(rsa129,(p-1)*(q-1))
  print "e = ", d
  writeNumber(inv(rsa129,(p-1)*(q-1)),'gxxx')
   
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
  for cx in largestr:
      result = (result << 8) ^ ord(cx)
  return result

def random1024():
  return random512() * random512()

def h(x):
  dx1 = hashlib.sha512(x).digest()
  dx2 = hashlib.sha512(dx1+x).digest()
  dx3 = hashlib.sha512(x+dx2).digest()
  dx4 = hashlib.sha512(x+dx3).digest()
  dx5 = hashlib.sha512(x+dx4).digest()
  res = 0
  for cx in (dx1+dx2+dx3+dx4+dx5):
    res = (res<<8) ^ ord(cx)
  return res % (nrsa)

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

# My public key
#>>> readNumber('n')
n = 132158664968768490782960847799015406036650767779277459921379897867566679587724524521987896737725523269165395751923267303738641975289767617733673183719848122664620561025225091299282924584871878765772994798839194882625865916048662867255808940326382392925259371837094024054492616735167070129273991602554868281260403078931758978042320828712406521136768937860224472073584018384229887268232999555522044285586888065207215194190028245326972822338830044710482833241494104291299248101801097861695990218731328867880865825220780717582330616093628187888772860304794060649785037872959663106341572544892592180043533578078543073813L
#>>> readNumber('e')
e = 3705065645512927316321462305254520982876035314505654008283722719433928258945868606816193707934157371759177881042853386436215164383893639793003538863209251L
#>>> 
rsa129 = 114381625757888867669235779976146612010218296721242362562561842935706935245733897830597123563958705058989075147599290026879543541
p1 = 3490529510847650949147849619903898133417764638493387843990820577
p2 = 32769132993266709549961988190834461413177642967992942539798288533


print "\n\n rsacrypt - copyright Scheerer Software 2017 - all rights reserved\n\n"
print "First parameter is V,S,E or D\n\n"
print "\n\n verify signature (3 parameters):"
print "   > python rsacrypt.py V <filename> <digital signature> "

print " create signature S (2 parameter):"
print "   > python rsacrypt.py S <filename> \n\n"
print " encrypt E (2 parameter):"
print "   > python rsacrypt.py E <text> \n\n"
print " decrypt D (2 parameter):"
print "   > python rsacrypt.py D <bigInteger> \n\n"

print " number of parameters is " + str(len(sys.argv)-1)
print " "
print " "

if len(sys.argv) == 3 and sys.argv[1] == "E":
  print "encrypted text: \n" + str (pow(bin2num(sys.argv[2]), readNumber('gxxx'), nrsa))

if len(sys.argv) == 3 and sys.argv[1] == "D":
  print " decrypt text:\n " + num2bin(pow (digital2num(sys.argv[2]),rsa129,nrsa)) 

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(sys.argv[2], code2num(sys.argv[3])))

if len(sys.argv) == 3 and sys.argv[1] == "S":
  print " digital signature:\n " + num2code(sF(sys.argv[2]))
     
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
#d = inv(e,(p1-1)*(p2-1)) 
#writeNumber(d,'gxxx')
#writeNumber(n,'nrsa')
#pubkey('1Franz','3Scheerer')   