import random, math, hashlib, sys

#p = 6668014432879854274079851790721257797144758322315908160396257811764037237817632071521432200871554290742929910593433240445888801654119365080363356052330830046095157579514014558463078285911814024728965016135886601981690748037476461291164275339
p = 2*(1416461893 + 10**500) + 1
g = 3
def gcd(a,b):
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):
 while p % 12 != 11:
   p = p + 1
 return nextPrime_s(p)

def nextPrime_s(p):
  m_ =  5 * 7 * 11 * 13 * 17 * 19 * 23 * 29 * 31
  while True:
    while gcd(p, m_) != 1 or gcd((p-1)/2, m_) != 1:
      p = p + 12
    if pow(7,p-1,p) != 1:
      p = p + 12
      continue
    if (pow(7,(p-3)/2, (p-1)/2) != 1):
      p = p + 12
      continue
    return p


#p_0 = 2**800
#print "Find prime p greater than 2^800 such that (p-1)/2 is prime"
#p = nextPrime(p_0) 
print "check p ", pow(11,p-1,p) == 1
px = (p-1)/2                    
print "check (p-1)/2 ", pow(11,px-1,px) == 1
print "\n", p                    

alice = 2134143854854758971
bob = 2994143854854754312412
Pa = pow(g,alice,p) 
Pb = pow(g,bob,p) 
print "Public key send form Alice to Bob\n", Pa 
print "Public key send form Bob to Alice\n", Pb
kab = pow(Pb,alice,p)
kba = pow(Pa,bob,p)
 
print "Are the keys equal? We check it: ", kab == kba