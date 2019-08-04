import sys

crabin =  '658ak9OxOEUcONnbDo9BfSREHPsSCCMETh15Mh6jrMwIAaJ6WkM4wP2#UhybruIq'
crabin += 'IoOaa6s7NrXf1bJgcHk7A#SYbhjTEoynfbDGnP48wrBxxP9J9diydrL6BfYA5FOXB'
crabin += 'i44bNJ2y5moKvJIhowkzO6GvydQ6AQBkR5goZP'

afactor = 41
bfactor = 3

def update_spritz():
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    i_spritz = (i_spritz + w_spritz) % 256
    j_spritz = s_spritz[(j_spritz + s_spritz[i_spritz]) % 256]
    s_spritz[i_spritz], s_spritz[j_spritz] = s_spritz[j_spritz], s_spritz[i_spritz]

def output_spritz():
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    update_spritz()
    return s_spritz[j_spritz]

def shuffle_spritz():
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    for v in range(256):
        update_spritz()    
    w_spritz = (w_spritz + 2) % 256
    a_spritz = 0

def absorb_nibble_spritz(x):
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    if a_spritz == 240:
        shuffle_spritz()
    s_spritz[a_spritz], s_spritz[240 + x] = s_spritz[240 + x], s_spritz[a_spritz]
    a_spritz = a_spritz + 1

def absorb_byte_spritz(b):
    absorb_nibble_spritz(b % 16)
    absorb_nibble_spritz(b / 16)

def squeeze_spritz(out, outlen):
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    if a_spritz != 0:
        shuffle_spritz()
    for v in range(outlen):
        out.append(output_spritz())

def h(x):
  global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
  j_spritz = i_spritz = a_spritz = 0
  w_spritz = 1
  s_spritz = range(256)
  for c in x:
     absorb_byte_spritz(ord(c)) 
  res = []
  squeeze_spritz(res, 128)
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out % (nrabin)

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

nrabin = code2num(crabin)

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

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 4 != 3:
   p = p + 1
 return nextPrime_(p)
  
def nextPrime_(p):
  m_ = 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29
  while gcd(p,m_) != 1:
    p = p + 4 
  if (pow(2,p-1,p) != 1):
      return nextPrime_(p + 4)
  if (pow(3,p-1,p) != 1):
      return nextPrime_(p + 4)
  if (pow(5,p-1,p) != 1):
      return nextPrime_(p + 4)
  if (pow(17,p-1,p) != 1):
      return nextPrime_(p + 4)
  return p
  

def root(m, p, q):
  x = h(m)
  a = afactor
  b = bfactor
  if pow(x, (p-1)/2, p) > 1:
    x *= a
  if pow(x, (q-1)/2, q) > 1:
    x *= b
#  print pow(x, (q-1)/2, q)
#  print pow(x, (p-1)/2, p)
  return (pow(p,q-2,q) * p * pow(x,(q+1)/4,q) + pow(q,p-2,p) * q * pow(x,(p+1)/4,p)) % (nrabin) 


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

def hF(fnam):
  f = open(fnam,'r')
  return h(f.read())

def sF(fnam):
  p = readNumber("p_")
  q = readNumber("q_")

  f = open(fnam,'r')
  s = root (f.read(), p, q)
  f.close()
  return s

# find factors a and b from primes p,q
def f_ab(p,q):
  res = [3,3]
  while pow(res[0], (p-1)/2, p) == 1 or pow(res[0], (q-1)/2, q) != 1:
    res[0] = res[0] + 1
  while pow(res[1], (p-1)/2, p) != 1 or pow(res[1], (q-1)/2, q) == 1:
    res[1] = res[1] + 1
  return res

def vF(s, fnam):
  a = afactor
  b = bfactor
  h0 = hF(fnam)
  ha = (a*h0) % nrabin
  hb = (b*h0) % nrabin
  hab = (a*b*h0) % nrabin

  sq = (s * s) % nrabin

  return (h0 == sq) or (ha == sq) or (hb == sq) or (hab == sq)
 
print "\n\n rabin signature - copyright Scheerer Software 2018 - all rights reserved\n\n"
print "First parameter is V (Verify) or S (Sign)\n\n"
print "\n\n verify signature (2 parameters):"
print "   > python rabin.py V <digital signature> "

print " create signature S (2 parameter):"
print "   > python rabin.py S <filename> \n\n"

print " number of parameters is " + str(len(sys.argv)-1)
print " "
print " "

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(code2num(sys.argv[3]),sys.argv[2]))

if len(sys.argv) == 3 and sys.argv[1] == "S":
  print " digital signature:\n " + num2code(sF(sys.argv[2]))

if len(sys.argv) == 3 and sys.argv[1] == "G":
  print " generate primes ... "
  p = nextPrime( h(sys.argv[2]) % (2**501 + 1) )  
  q = nextPrime( h(sys.argv[2] + '0') % (2**501 + 1) )  
  writeNumber(p, 'p_')                     
  writeNumber(q, 'q_')     
  print "nrabin = ", (p * q) 
  print "\ncrabin = \n", num2code(p * q) 
  print "afactor = ", f_ab(p,q)[0]             
  print "bfactor = ", f_ab(p,q)[1]             

print ""
print "nrabin as code \n",num2code(nrabin)