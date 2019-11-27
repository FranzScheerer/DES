'''
  Schnorr Signature 
  Secure
  Simple curve: y^2 = x^3 - x (modulo prime)
  Hash h241 
  PYthon 3
  Verification only 
  Copyright (c) Scheerer Software 2019 - all rights reserved 

''' 
import sys, hashlib

prime =  155290274003083342322476192189053102662851

P = [83121615494937603289470348650512900644084]
P.append(128331514779326507229042701794577809691621)

publicKey = [51832892944004914084463600943575298192624]
publicKey.append(69084455079363677946579759623969965834606)

sig = [11526257842179973443649750622549910694762]
sig.append(31709713789100773424391354079811061729721)

f = open(sys.argv[1],"rb")
message = hashlib.sha256(f.read()).hexdigest()

def update241():
    global a241, i241, j241, w241, s241
    i241 = (i241 + w241) % 256
    j241 = s241[(j241 + s241[i241]) % 256]
    s241[i241], s241[j241] = s241[j241], s241[i241]

def output241():
    global a241, i241, j241, w241, s241
    update241()
    return s241[j241]

def shuffle241():
    global a241, i241, j241, w241, s241
    for v in range(256):
        update241()    
    w241 = (w241 + 2) % 256
    a241 = 0

def absorb_nibble241(x):
    global a241, i241, j241, w241, s241
    if a241 == 241:
        shuffle241()
    s241[a241], s241[240 + x] = s241[240 + x], s241[a241]
    a241 = a241 + 1

def absorb_byte241(b):
    absorb_nibble241(b % 16)
    absorb_nibble241(b >> 4)

def squeeze241(out, outlen):
    global a241, i241, j241, w241, s241
    shuffle241()
    for v in range(outlen):
        out.append(output241())

def h(x):
  global a241, i241, j241, w241, s241
  i241 = j241 = a241 = 0
  w241 = 1
  s241 = []
  for ix in range(256):
    s241.append(ix)
  #
  # absorb all bytes
  #
  for c in x:
     absorb_byte241(ord(c)) 
  res = []
  squeeze241(res, 32) # 8*32 = 256 bits
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out

#
# Add point P and Q on the curve
#
def addP(P,Q):
  global prime
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = ((3*x1*x1 - 1) * pow(2*y1, prime-2, prime)) % prime
  else:  
     if x1 < x2:
        x1 = x1 + prime
     s = ((y1-y2) * pow(x1-x2, prime-2, prime)) % prime
  xr =  (s*s) - x1 - x2
  yr = s * (x1-xr) - y1 
  return [xr % prime, yr % prime]

#
# P + P + P + P + P + P --- n times
# 
def mulP(P,n):
  global prime
  resP = 'ZERO'
  PP = P
  while n != 0:
     if (n % 2 != 0):   
         if resP == 'ZERO':
            resP = PP
         else:
            resP = addP(resP,PP)
     PP = addP(PP, PP) 
     n >>= 1 
  return resP


#Verification
R = addP(mulP(P, sig[0]), mulP(publicKey, sig[1]))
check = h(str(R[0])+message) % ((prime+1)>>2) == sig[1]
print("\nResult of verification ", check)

def num2hextxt(x):
  res = ''
  h__ = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
  while x > 0:
    res = h__[x % 16] + res
    x >>= 4
  return res

hash = h("The quick brown fox jumps over the lazy dog")
print ("The quick brown fox jumps over the lazy dog:\n h = ", num2hextxt(hash))