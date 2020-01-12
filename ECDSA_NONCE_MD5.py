#
# Note: The Schnorr Signature uses a NONCE together
# with the hash. It means, only 128 bits are
# required.
# We can use a NONCE together with ECDSA too!
#

'''
 Doch - MD5 also 128 Bits, das reicht aus! 
  
 Der Hacker oder Codeknacker kann mit Kollisionen, 
 die er eventuell finden könnte, nichts anfangen. Die
 Signatur wird nicht aus einer dem Knacker bekannten 
 oder vom ihm erwartbaren Nachricht berechnet.
 
 Den rechtmäßigen Unterzeichner brauchen wir nicht 
 betrachten. Er kann ohnehin jede Nachricht, auch 
 gefälschte, unterzeichnen. Dies lässt sich mit dem
 Signaturverfahren nicht verhindern.
''' 
import hashlib
def h(x):
  z = 0 
  for b in hashlib.md5(x.encode()).digest():
      z = 256*z + b
  return z     

def gcd(a,b):      # greatest common divisor
  while b > 0:
    a,b = b,a % b
  return a

def nextPrime(p):     # find the smallest prime 
 while p % 12 != 7:   # greater or equal p 
   p = p + 1          # with some other properties.
 m =  5 * 7 * 11 * 13 * 17 * 19 * 23
 m *= 29 * 31 * 37 * 41 * 43 * 47
 while True:
    q = (p+1)//4
    while gcd(p, m) != 1 or gcd(q, m) != 1:
      p = p + 12 
      q = q + 3
    if (pow(7, p - 1, p) != 1
       or pow(7, q - 1, q) != 1):
      p = p + 12
      continue
    return p

maxx = 131 * 2**141
ecc_prime = nextPrime( h('generate prime Abc')<<20 % maxx )
''' 
    Yes, the prime is large enough.

    Niemals wurde der diskrete Logarithmus bei elliptischen
    Kurven bei Primzahlen größer 2^120 geknackt. Es sind
    Preise im fünfstelligen Bereich ausgesetzt für nur 
    131 Bits und diese wurden in über 10 Jahren nicht 
    eingelöst.
'''
assert(ecc_prime > 2**141)

ecc_n = (ecc_prime + 1)//4
print ("ecc_prime = ", ecc_prime)
print ("ecc_n = ", ecc_n)

def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = ((3*x1*x1 - 1) * pow(2*y1, ecc_prime-2,
     ecc_prime)) % ecc_prime
  else:  
     if x1 < x2:
        x1 = x1 + ecc_prime
     s = ((y1-y2) * pow(x1-x2, ecc_prime-2, 
     ecc_prime)) % ecc_prime
  xr =  (s*s) - x1 - x2
  yr = s * (x1-xr) - y1 
  return [xr % ecc_prime, yr % ecc_prime]

def mulP(P,n):
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
  
ecc_n = (ecc_prime + 1) // 4

def ECDSA_N(G, m, x):
  # k is different if message m is different,
  # almost sure for a random message.
  k = h('password X' + m + 'key value') 
  r = mulP(G,k)[0] % ecc_n     # the NONCE
  kinv = pow(k, ecc_n-2, ecc_n) # more than 140 bits
  z = h(m + str(r)) % ecc_n
  return {'s': (kinv*(z + x*r)) % ecc_n, 'r': r}

message = '''
Supernova = Gravistionsline

Stehen zwei Sterne und der Beobachter exakt auf einer 
Geraden, wird das Licht des vermeintlich verdeckten Sterns
tatsächlich verstärkt, denn die Querschnittsfläche wird 
zu einem Kreis aufgeweitet (siehe Gravitationsline). 

Dies ist die wahre Ursache für Supernovae und 
ferne Galaxien. Es handelt sich um nichts anderes als 
Sternenbedeckungen.
 
'''
#Generate the private key from a password
privateKey = h( 'this is passwordX' ) 

#Generate the base point from another password
x = h("password 1234567 ABC_")
ecc_a = ecc_prime - 1
ecc_b = 0
if pow(x**3 + ecc_a*x + ecc_b, (ecc_prime-1)//2, 
   ecc_prime) != 1:
   x = ecc_prime - x 
y = pow( x**3 + ecc_a*x + ecc_b, (ecc_prime+1)//4,
    ecc_prime)
P = [ x , y ]
# To get a base point with prime order
P = mulP(P, 4)

print("P = ", P)

publicKey = mulP(P, privateKey)

print("publicKey = ", publicKey)

sig = ECDSA_N(P, message, privateKey)
print("sig = ", sig)
'''
This is a modified extended public key and signature
for a modified message.
----------------------------------------------------------
ecc_prime =  152074719225497009012760430396303867304218603             
ecc_n     =  38018679806374252253190107599075966826054651                  
P =  [30747039278785896093374005797275912866203796,
      132132253200420609789780790216880705438538587]                                            
publicKey =  [129317480793006411510305718835033420956774725,
              24011586631153721894836941764948420309273951]                                    
sig =  {'r': 637395933887908073180323526266340010316366, 
        's': 35757153672042405466245383980422896515488576}                                   
-----------------------------------------------------------
'''
ecc_prime =  67005694743602434949129979245186326089241891              
ecc_n =  16751423685900608737282494811296581522310473                  
P =  [10242082634297248831485179437573283115860652, 
13121388037010927625773940114350218727612211]                                             
publicKey =  [9813922895496718147309957513638910633475046,
 3430694419994462808857825510572041846001964]                                       
sig =  {'s': 14723242786326851345623878297667502893672654,
 'r': 308557476658922364520627271084261314659046}                                   
  
#Verification of ECDSA_N
z = h(message + str(sig['r'])) 
sinv = pow(sig['s'], ecc_n-2, ecc_n)
P1 = mulP(P, sinv * z)
P2 = mulP(publicKey, sinv * sig['r'])
r = addP(P1, P2)[0]
assert(r % ecc_n == sig['r'])

