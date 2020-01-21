class ECHASH:
  def update(H):
    H.i = (H.i + H.w) % 256
    H.j = H.s[(H.j + H.s[H.i]) % 256]
    H.s[H.i], H.s[H.j] = H.s[H.j], H.s[H.i]

  def shuffle(H):
    for v in range(256):
        ECHASH.update(H)    
    H.w = (H.w + 2) % 256
    H.a = 0

  def absorb_nibble(H,x):
    if H.a == 63:
        ECHASH.shuffle(H)
    H.s[H.a], H.s[240 + x] = H.s[240 + x], H.s[H.a]
    H.a = H.a + 1

  def absorb_byte(H,b):
    ECHASH.absorb_nibble(H, b % 16)
    ECHASH.absorb_nibble(H, b >> 4)

  def h(H, msg, outlen):
    H.s = list(range(256))   
    H.a = H.i = H.j = 0
    H.w = 1
    for c in msg.encode():
       ECHASH.absorb_byte(H,c)
    ECHASH.shuffle(H)
    ECHASH.shuffle(H)
    ECHASH.shuffle(H)
    out = 0
    for v in range(outlen):
        ECHASH.update(H)
        out = (out << 8) + H.s[H.j]
    return out   

  def gcd(a,b):
    while b > 0:
      a,b = b,a % b
    return a

  def nextPrime(p):
    while p % 12 != 7:
      p = p + 1
    m =  5 * 7 * 11 * 13 * 17 * 19 * 23
    m *= 29 * 31 * 37 * 41 * 43 * 47
    while True:
      q = (p+1)//4
      x1 = ECHASH.gcd(p, m)
      x2 = ECHASH.gcd(q, m)
      while x1 != 1 or x2 != 1:
        p = p + 12 
        q = q + 3
        x1 = ECHASH.gcd(p, m)
        x2 = ECHASH.gcd(q, m)
      x1 = pow(7, p-1, p)    
      x2 = pow(7, q-1, q)    
      if (x1 != 1 or x2 != 1):
        p = p + 12
        continue
      return p
    
# 20 Bytes output like in SHA-1
def h(x):
  ha = ECHASH()
  return ECHASH.h(ha,x,20)     

maxx = 131 * 2**141
h0 = h('generate prime X')
ecc_prime = ECHASH.nextPrime( h0 % maxx )
''' Yes, the prime is large enough'''
print ("A prime greater than 2^141") 
print ("p = ", ecc_prime)
assert(ecc_prime > 2**141)

ecc_n = (ecc_prime + 1)//4
ecc_a = -1 
ecc_b = 0 
def addP(P,Q):
  x1 = P[0]
  x2 = Q[0]
  y1 = P[1] 
  y2 = Q[1] 
  if x1 == x2:
     s = ((3*x1*x1 + ecc_a) * pow(2*y1, ecc_prime-2, 
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

def signSchnorr(G, m, x):
  k = h('password X' + m + 'key value') 
  R = mulP(G,k) 
  e = h(str(R[0]) + m) % ecc_n
  return {'s': (k - x*e) % ecc_n, 'e': e}

def ECDSA_N(G, m, x):
  k = h('password X' + m + 'key value') 
  r = mulP(G,k)[0] % ecc_n     # the NONCE
  kinv = pow(k, ecc_n-2, ecc_n)
  z = h(m + str(r)) % ecc_n
  return {'s': (kinv*(z + x*r)) % ecc_n, 'r': r}

message = '''
          DIE LICHTABLENKUNG DURCH SCHWERKRAFT
------------------------------------------------------
I. Die klassische Berechnung

Die Sonne, eine Punktmasse befinde sich im Ursrung
unseres Koordinatensystems.

Das Lichtteilchen bewege sich in großer Entfernung x0
zur Sonne in x Richtung auf die Sonne zu. Mit der Licht-
geschwingkeit c.

Der Abstand zur y-Achse Y0 = R sei der Sonnenrandius
und in guter Nährerung konstanr.

Wir berechnen die Winkeländerung (Bogenmaß) entlang
einer kurzen Wegstrecke dx. Das Licht legt die Strecke dx 
in der Zeit dt zurück.

dt = dx/c 

Dazu berechnen wir die jetzt Kraft nach Newtons Lraftgesetz
auf das Lichtteilchens senkrecht zu Strahlrichtung 
(y-Richtung). Durch Division durch die Masse 
des Lichtteilchens könnten wir die Masse aus der 
Energie E des Lichtteilchens berechnen.

m = E/c^2

Wir brauchen die Masse m tatsächlich gar nicht
kennen, weil sie sich bei der Berechnung der 
Geschschwingitkeitsänderung, der Beschleunigung
herauskürzt. Aus den Beschleunigung können die 
Geschwingkeitsänderung dv denkrecht zur x-Axhse 
berechnen und daraus schließlich die Winkeländerung 

d(phi) = (1/c) ((GM)/r^2) (y/r) (dx/c)

       = ((GM)/c^2) y/r^3 dx

Dabei ist r der Abstand des Lichtteilchens zur 
Sonne.
  
               r = sqrt ( x*x + y*y )
               
G ist die Gravitationskonstante und M die Masse 
der Sonne. Die Abkürzung sqrt steht für square 
root also die Quadratwurzel.

Den Wert von y können wir in sehr guter Näherung 
als konstant ansehen, da sich das Teilchen senkrecht 
dazu bewegt und die Winkeländerung nur minimal ist.

Um den Wert der Ablenkung aus großer Entfernung zur 
Sonne bis wieder in großer Entfernung zur Sonne zu 
berechnen, müssen wir die Winkeländerungen addieren.

Mathematisch läuft dies auf die Integration von 
minus unendlich (-infty) bis plus unendlich (+infty)
hinaus. Das Ergbnis finden wir mit Wolfram Alpha:

https://www.wolframalpha.com

Ergebnis der klassischen Berechnung:

Winkelabweichung im Bogenmaß  
(1 rad = 1° mal pi/180 

1'' = Bogensekunde = pi / (180 * (60*60))
pi = 3.1415.... die berühmte Kreiszahl

Die gesamte Winkeländerung nach Integration:

Delata phi  = 2 * (GM/c^2) / R

Mit R dem Abstand in dem das Teilchen die Sonne 
passiert. R ist größer oder gleich dem Sonnenradius,
versteht sich.


Einstein sagt:
Die Winkelabweicung ist genau:

Delata phi  = 4 * (GM/c^2) / R

... und wer kann mir das jetzt einmal erklären,
woher kommt der zusätzliche Faktor zwei ?????????


'''
#Generate the private key from a password
privateKey = h( 'passwordX' ) 

#Generate the base point from another password
x = h("password 1234567")
if pow(x**3 + ecc_a*x + ecc_b, (ecc_prime-1)//2, 
   ecc_prime) != 1:
   x = ecc_prime - x 
y = pow( x**3 + ecc_a*x + ecc_b, (ecc_prime+1)//4,
    ecc_prime)
P = [ x , y ]
# To get a base point with prime order
P = mulP(P, 4)

print("The base point is: \n P = ", P)

publicKey = mulP(P, privateKey)

print("The public key is the point: ")
print ("publicKey = ", publicKey)
sig = signSchnorr(P, message, privateKey)
print("The signature is: ")
print("sig = ", sig)
#Verification
P1 = mulP(P, sig['s'])
P2 = mulP(publicKey, sig['e'])
r = addP(P1, P2)[0]
assert(h(str(r)+message) % ecc_n == sig['e'])
'''
   ECDSA_N with sig['r'] used as NONCE

   This algorithm is equivalent to Schnorr's signature.
   We can apply the same public and private key and 
   the same message.
   
   In cryptography, a nonce is an arbitrary number 
   that can be used just once in a cryptographic 
   communication. It is similar in spirit to a nonce word,
   hence the name. It is often a random or pseudo-random
   number issued in an authentication protocol to ensure
   that old communications cannot be reused in replay attacks.
   They can also be useful as initialization vectors and in
   cryptographic hash functions.
'''
sig = ECDSA_N(P, message, privateKey)
print("The signature is: ")
print("sig = ",  sig)

#Verification
z = h(message + str(sig['r'])) 
sinv = pow(sig['s'], ecc_n-2, ecc_n)
P1 = mulP(P, sinv * z)
P2 = mulP(publicKey, sinv * sig['r'])
r = addP(P1, P2)[0]
assert( r % ecc_n == sig['r'] )
