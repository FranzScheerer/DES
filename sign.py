import sys

nrabin = 1275574687529707052360270181001777089671167672089082721378211835809946265943774704298829077228926639950048281145477004890301800135170057571586644210706829514984111130118296710578328836619124873204558928730791403673479088571255223740478384830455590280922940539854528127509L

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

  
def root(m, p, q):
  x = h(m)
  a = 5
  b = 3
  if pow(x, (p-1)/2, p) > 1:
    x *= a
  if pow(x, (q-1)/2, q) > 1:
    x *= b
#  print pow(x, (q-1)/2, q)
#  print pow(x, (p-1)/2, p)
  return (pow(p,q-2,q) * p * pow(x,(q+1)/4,q) + pow(q,p-2,p) * q * pow(x,(p+1)/4,p)) % (nrabin) 

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
  p = readNumber("p")
  q = readNumber("q")

  f = open(fnam,'r')
  s = root (f.read(), p, q)
  f.close()
  return s

 
print "\n\n rabin signature - copyright Scheerer Software 2018 - all rights reserved\n\n"
print "First parameter is V (Verify) or S (Sign)\n\n"
print "\n\n verify signature (2 parameters):"
print "   > python rabin.py V <digital signature> "

print " create signature S (2 parameter):"
print "   > python rabin.py S <filename> \n\n"

print " number of parameters is " + str(len(sys.argv)-1)
print " "
print " "

if len(sys.argv) == 3 and sys.argv[1] == "S":
  print " digital signature:\n " + num2code(sF(sys.argv[2]))
     
                     