'''
  Schnorr Signature (Verifivation only) 
  Secure
  Simple curve: y^2 = x^3 - x (modulo prime)
  Hash h241 
  PYthon 3
  Message in line 177
  Copyright (c) Scheerer Software 2019 - all rights reserved 
''' 

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
  '''
  absorb all bytes
  of the encoded message
  '''
  for c in x.encode():
     absorb_byte241(c) 
  res = []
  squeeze241(res, 32) # 8*32 = 256 bits
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out

prime = 248359970965070966100215621849780240684422603
'''
 This prime is safe
''' 

'''
 Add point P and Q 
 P and Q are Points 
 on the elliptic curve
'''
def addP(P,Q):
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

'''
 n times the point P 
 P + P + P + P + P + P --- 
 is calculated using double and add.
'''
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

message = '''
In cryptography, a Schnorr signature is a digital signature
produced by the Schnorr signature algorithm that was described 
by Claus Schnorr. It is a digital signature scheme known for its
simplicity,[1] among the first whose security is based on the 
intractability of certain discrete logarithm problems.[1] 

It is efficient and generates short signatures.[1]

It was covered by U.S. Patent 4,995,082 which expired in February 2008.
'''

P = [233732100584156704872253479128995381436279825]
P.append(100381480487303697389898792062782541391754903)
print("The base point is: ")
print("x: ",P[0])
print("y: ",P[1])


publicKey = [1365980310789738850776807563504970164719808]
publicKey.append(8570338689453206975840082610152026678357526)
print("The public key is the point: ")
print("x: ",publicKey[0])
print("y: ",publicKey[1])
'''
  Insert the signature, s and e 
'''
sig = [45253720191432296454298011829343821337037309]
sig.append(11246055374866181080732304687990008310661320)
print("The signature is: ")
print("s: ",sig[0])
print("e: ",sig[1])

#Verification
R = addP(mulP(P, sig[0]), mulP(publicKey, sig[1]))
check = h(str(R[0])+message) % ((prime+1)>>2) == sig[1]
print("\nResult of verification ", check)


