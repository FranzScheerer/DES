import random, math, hashlib, sys

PublickeyX =  392937783511856504522659672430734557979
PublickeyY =  4034124688196261675086793643422882347425

def update_spritz():
    global a_spritz, i_spritz, j_spritz, w_spritz, s_spritz
    i_spritz = (i_spritz + w_spritz) % 256
    j_spritz = s_spritz[(j_spritz + s_spritz[i_spritz]) % 256]
    s_spritz[i_spritz], s_spritz[j_spritz] = s_spritz[j_spritz], s_spritz[i_spritz]

def output_spritz():
    global a_spritz, i_spritz, j_spritz, w_spritz, s_spritz
    update_spritz()
    return s_spritz[j_spritz]

def shuffle_spritz():
    global a_spritz, i_spritz, j_spritz, w_spritz, s_spritz
    for v in range(256):
        update_spritz()    
    w_spritz = (w_spritz + 2) % 256
    a_spritz = 0

def absorb_nibble_spritz(x):
    global a_spritz, i_spritz, j_spritz, w_spritz, s_spritz
    if a_spritz == 240:
        shuffle_spritz()
    s_spritz[a_spritz], s_spritz[240 + x] = s_spritz[240 + x], s_spritz[a_spritz]
    a_spritz = a_spritz + 1

def absorb_byte_spritz(b):
    absorb_nibble_spritz(b % 16)
    absorb_nibble_spritz(b / 16)

def squeeze_spritz(out, outlen):
    global a_spritz, i_spritz, j_spritz, w_spritz, s_spritz
    if a_spritz != 0:
        shuffle_spritz()
    for v in range(outlen):
        out.append(output_spritz())

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def readNumber(fnam):
  f = open(fnam, 'rb')
  n = 0
  snum = f.read()
  for i in range(len(snum)):
    n = (n << 8) ^ ord(snum[len(snum)-i-1])   
  f.close()
  return n


prime = 32667107224410092492483962313449748403011

print "A prime greater than 12 times 2^131 \np = ", prime

a = 0
b = prime - 3 # b = -3 modulo prime
 
r = (prime + 1) / 12
hsize = r
 
def inv(b,a):
  m = a
  s = 0
  t = 1
  while b != 1:
    q = a/b
    a_tmp = b
    b = a % b
    a = a_tmp
    s_tmp = t
    t = s - q*t
    s = s_tmp
  if t < 0:
    t = t + m
  return t

def h(x):
  global a_spritz, i_spritz, j_spritz, w_spritz, s_spritz
  i_spritz = j_spritz = a_spritz = 0
  w_spritz = 1
  s_spritz = range(256)
  #
  # absorb all bytes
  #
  for c in x:
     absorb_byte_spritz(ord(c)) 

  res = []
  squeeze_spritz(res, 32) # 8*32 = 256 bits
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out % (hsize)

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = ((3*(x1**2) + a) * inv(2*y1, prime)) % prime
  else:  
     if x1 < x2:
        x1 = x1 + prime
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
     if (n % 2 != 0):   
         if isFirst:
            resP = PP
            isFirst = False
         else:
            resP = addP(resP,PP)
     PP = addP(PP, PP) 
     n = n / 2
  return resP

def verify(G,s,Y,e,m):
  return e == h(str(addP(mulP(G,s),mulP(Y,e))[0]) + m)


x = 1234567
while pow(x**3 + a*x + b, (prime - 1)/2, prime) != 1:
   x = x + 1
y = pow(x**3 + a*x + b, (prime + 1)/4, prime)
P = [x % prime, y % prime]
P = mulP(P, 12)

#
# read message from file 
#
f = open(sys.argv[1], 'r')
message = f.read()
f.close()

y = [PublickeyX, PublickeyY]
sig = [readNumber('s0'), readNumber('s1')]

print "Public key: X: ", y[0] % prime
print "Public key: Y: ", y[1] % prime
print "Sigature    X: ", sig[0]
print "Sigature    y: ", sig[1]
print ""
print "The verification of signature ", verify(P, sig[0], y, sig[1], message)
#print "The verification of ecdsa signature ", ecdsa_v(P,message,sig, y)

