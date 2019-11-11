import random, math, getpass, sys

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
    if a_spritz == 241:
        shuffle_spritz()
    s_spritz[a_spritz], s_spritz[240 + x] = s_spritz[240 + x], s_spritz[a_spritz]
    a_spritz = a_spritz + 1

def absorb_byte_spritz(b):
    absorb_nibble_spritz(b % 16)
    absorb_nibble_spritz(b // 16)

def squeeze_spritz(out, outlen):
    global a_spritz, i_spritz, j_spritz, w_spritz, s_spritz
    shuffle_spritz()
    for v in range(outlen):
        out.append(output_spritz())

def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

#
# p and (p+1)//12 are primes
#
def nextPrime(p):
 while p % 12 != 11:
   p = p + 1
 return nextPrime_odd(p)

def nextPrime_odd(p):
  m_ =  5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31 * 37 * 41 * 43 * 47
  while True:
    while gcd(p, m_) != 1 or gcd((p+1)//12, m_) != 1:
      p = p + 12 
    if (pow(7,p-1,p) != 1 or pow(7, (p+1)//12 - 1, (p+1)//12) != 1):
      p = p + 12
      continue
    return p

#
# (prime+1) divided by 12 ts prime
#
prime = nextPrime(12 * 2**131)

print ("A prime greater than 12 times 2^131 \np = ", prime)

def inv(b,a):
  m = a
  s = 0
  t = 1
  while b != 1:
    q = a//b
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
  s_spritz = []
  for ix in range(256):
    s_spritz.append(ix)
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
  return out % (prime+1)//12

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = (3*(x1**2) * inv(2*y1, prime)) % prime
  else:  
     if x1 < x2:
        x1 = x1 + prime
     s = ((y1-y2) * inv(x1-x2, prime)) % prime
  xr = s**2 - x1 - x2
  yr = s * (x1-xr) - y1 
  return [xr % prime, yr % prime]

def mulP(P,n):
  isFirst = True
  resP = 'NONE'
  PP = P
  while n > 0:
     if (n % 2 != 0):   
         if isFirst:
            resP = PP
            isFirst = False
         else:
            resP = addP(resP,PP)
     PP = addP(PP, PP) 
     n = n // 2
  return resP

def signSchnorr(G, m, x):
  # k is different if m is different
  k = h(m + 'key value') 
  R = mulP(G,k)
  e = h(str(R[0]) + m)
  return [(k - x*e) % ((prime+1)//12), e]

#Generate the base point
x = 1234567
while pow(x**3 + 1, (prime-1)//2, prime) != 1:
   x = x + 1
y = pow(x**3 + 1, (prime+1)//4, prime)
P = [x % prime, y % prime]


P = mulP(P, 12)

fo = open('vFS.py','r')
print("\n\n Read message to sign from file: ", fo.name)
message = fo.read()
fo.close()

privateKey = h('mypassword')

sig = signSchnorr(P, message, privateKey)
print("The signature is: ",sig)
publicKey = mulP(P, privateKey)

#Verification
#sig = [217386284724654099298610386906895450235, 1593176211314688851384299242063611055952]
R = addP(mulP(P, sig[0]), mulP(publicKey, sig[1]))
check = h(str(R[0])+message) == sig[1]
print("\nResult of verification ", check)
print()

 
