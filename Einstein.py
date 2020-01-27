'''
  Diese Klasse ist total genial, deshalb heißt sie 

  EINSTEIN
  
  Copyright (c) 2020 Scheerer Software 
  All rights reserved - alle Rechte vorbehalten 
'''

class EINSTEIN:

  def update(H):
    H.i = (H.i + H.w) % 256
    H.j = H.s[(H.j + H.s[H.i]) % 256]
    H.s[H.i], H.s[H.j] = H.s[H.j], H.s[H.i]

  def shuffle(H):
    for v in range(256):
        EINSTEIN.update(H)    
    H.w = (H.w + 2) % 256
    H.a = 0

  def absorb_nibble(H,x):
    if H.a == 63:
        EINSTEIN.shuffle(H)
    H.s[H.a], H.s[240 + x] = H.s[240 + x], H.s[H.a]
    H.a = H.a + 1

  def absorb_byte(H,b):
    EINSTEIN.absorb_nibble(H, b % 16)
    EINSTEIN.absorb_nibble(H, b >> 4)

  def h(H, msg, outlen):
    H.s = list(range(256))   
    H.a = H.i = H.j = 0
    H.w = 1
    for c in msg.encode():
       EINSTEIN.absorb_byte(H,c)
    EINSTEIN.shuffle(H)
    EINSTEIN.shuffle(H)
    EINSTEIN.shuffle(H)
    out = 0
    for v in range(outlen):
        EINSTEIN.update(H)
        out = (out << 8) + H.s[H.j]
    return out   

  def gcd(a,b):
    while b > 0:
      a,b = b,a % b
    return a

  def PP(n):
    pX = n * [True]
    res = 1
    k = 2
    while k <= n:
      if pX[k-2]:
        res *= k
        kk = 2*k
        while kk <= n:
          pX[kk-2] = False
          kk += k
      k += 1
    return res  

  def smooth(n,m):
    g = EINSTEIN.gcd(n,m)
    while g > 1:
       n //= g
       g = EINSTEIN.gcd(n,m)
    return n == 1

  def test(n,m,a):
    cnt = 0
    c = 0
    while c < a:
       x = n + c
       c += 1 
       if EINSTEIN.smooth(x,m):
          cnt += 1
          print(x, " is smooth number ",cnt, "\nof ", c, " numbers tested ")

  def nextPrime(p):
    while p % 12 != 7:
      p = p + 1
    m =  5 * 7 * 11 * 13 * 17 * 19 * 23
    m *= 29 * 31 * 37 * 41 * 43 * 47
    while True:
      q = (p+1)//4
      x1 = EINSTEIN.gcd(p, m)
      x2 = EINSTEIN.gcd(q, m)
      while x1 != 1 or x2 != 1:
        p = p + 12 
        q = q + 3
        x1 = EINSTEIN.gcd(p, m)
        x2 = EINSTEIN.gcd(q, m)
      x1 = pow(7, p-1, p)    
      x2 = pow(7, q-1, q)    
      if (x1 != 1 or x2 != 1):
        p = p + 12
        continue
      return p
      
  def addP(P,Q):
    global ecc_prime     
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
    global ecc_prime     
    resP = 'ZERO'
    PP = P
    while n != 0:
       if (n % 2 != 0):   
         if resP == 'ZERO':
            resP = PP
         else:
            resP = EINSTEIN.addP(resP,PP)
       PP = EINSTEIN.addP(PP, PP) 
       n >>= 1 
    return resP

  def signSchnorr(G, m, x):
    global ecc_n     
    k = h('password X' + m + 'key value') 
    R = EINSTEIN.mulP(G,k) 
    e = h(str(R[0]) + m) % ecc_n
    return {'s': (k - x*e) % ecc_n, 'e': e}

  def ECDSA_N(G, m, x):
    global ecc_n     
    k = h('password X' + m + 'key value') 
    r = EINSTEIN.mulP(G,k)[0] % ecc_n     # the NONCE
    kinv = pow(k, ecc_n-2, ecc_n)
    z = h(m + str(r)) % ecc_n
    return {'s': (kinv*(z + x*r)) % ecc_n, 'r': r}

def h(x):         # output 20 bytes is enough with nonce 
  ha = EINSTEIN()
  return EINSTEIN.h(ha, x, 20)     

maxx = 131 * 2**141
h0 = h('generate prime X')
ecc_prime = EINSTEIN.nextPrime( h0 % maxx )
''' Yes, the prime is large enough'''
print ("A prime greater than 2^141") 
print ("p = ", ecc_prime)
assert(ecc_prime > 2**141)

ecc_n = (ecc_prime + 1)//4

message = '''
          DIE LICHTABLENKUNG DURCH SCHWERKRAFT
------------------------------------------------------
I. Die klassische Berechnung

Die Sonne, eine Punktmasse befinde sich im Ursrung
unseres Koordinatensystems.

Das Lichtteilchen bewege sich in großer Entfernung x0
zur Sonne in x Richtung auf die Sonne zu. Mit der Licht-
geschwingkeit c.

Der Abstand zur y-Achse 

y = Y0 = R 

sei der Sonnenrandius und in guter Nährerung konstant.

Wir berechnen die Winkeländerung (Bogenmaß) entlang
einer kurzen Wegstrecke dx. Das Licht legt die Strecke dx 
in der Zeit dt zurück.

dt = dx/c 

Dazu berechnen wir die jetzt die Kraft nach Newtons 
Kraftgesetz auf das Teilchens senkrecht zur Strahlrichtung 
Durch Division durch die Masse  des Teilchens könnten wir 
die Masse aus der Energie E des Lichtteilchens berechnen.

Die Masse des Photons:

                      m = E/c^2

Wir brauchen die Masse m tatsächlich gar nicht
kennen, weil sie sich bei der Berechnung der 
Geschschwingitkeitsänderung, der Beschleunigung
herauskürzt. Aus den Beschleunigung können wir die 
Geschwingkeitsänderung dv denkrecht zur x-Axhse 
berechnen und daraus schließlich die Winkeländerung 

d(phi) = dv/c = (1/c) ((GM)/r^2) (R/r) (dx/c)

       = ((GM)/c^2) R/r^3 dx

Dabei ist r der Abstand des Teilchens zur Sonne.
  
               r = sqrt ( x*x + R*R )
               
G ist die Gravitationskonstante und M die Masse 
der Sonne. Die Abkürzung sqrt steht für square 
root also die Quadratwurzel.

Den Wert von y = R können wir in sehr guter Näherung 
als konstant ansehen, da sich das Teilchen senkrecht 
dazu bewegt und die Winkeländerung nur minimal ist.

Um den Wert der Ablenkung aus großer Entfernung zur 
Sonne bis wieder in großer Entfernung zur Sonne zu 
berechnen, müssen wir die Winkeländerungen addieren.

Mathematisch läuft dies auf die Integration von 
minus unendlich (-infty) bis plus unendlich (+infty)
hinaus. Das Ergbnis finden wir zum Beispiel mit 
Wolfram Alpha:

https://www.wolframalpha.com

Ergebnis der klassischen Berechnung:
----------------------------------------------------

Winkelabweichung im Bogenmaß  
Einheit des Winkels: 1 rad = 1° mal pi/180) 

1'' = Bogensekunde = pi / (180 * (60*60))
pi = 3.1415.... die berühmte Kreiszahl

Die gesamte Winkeländerung nach Integration:

Delta phi  = 2 * (GM/c^2) / R

Mit R dem Abstand in dem das Teilchen die Sonne 
passiert. R ist größer oder gleich dem Sonnenradius,
versteht sich.


Einstein sagt:
Die Winkelabweicung ist genau:

Delta phi  = 4 * (GM/c^2) / R

... und wer kann mir das jetzt einmal erklären,
woher kommt der zusätzliche Faktor zwei ?????????

-----------------END OF MESSAGE------------------
'''

#Generate the private key from a password
privateKey = h( 'passwordX' ) 

#Generate the base point from another password
x = h("password 1234567")
if pow(x**3 - x, (ecc_prime-1)//2, ecc_prime) != 1:
   x = ecc_prime - x 
y = pow( x**3 -x, (ecc_prime+1)//4, ecc_prime)
P = [ x , y ]
# To get a base point with prime order
P = EINSTEIN.mulP(P, 4)

print("The base point is: \n P = ", P)

publicKey = EINSTEIN.mulP(P, privateKey)

print("The public key is the point: ")
print ("publicKey = ", publicKey)
sig = EINSTEIN.signSchnorr(P, message, privateKey)
print("The signature is: ")
print("sig = ", sig)
#Verification
P1 = EINSTEIN.mulP(P, sig['s'])
P2 = EINSTEIN.mulP(publicKey, sig['e'])
r  = EINSTEIN.addP(P1, P2)[0]

# Verify the Schnorr Signature
assert(h(str(r)+message) % ecc_n == sig['e'])

'''
   ECDSA_N with sig['r'] used as NONCE

   This algorithm is equivalent to Schnorr's signature.
   We can apply the same public and private key and 
   also the same message.
   
   In cryptography, a nonce is an arbitrary number 
   that can be used just once in a cryptographic 
   communication. It is similar in spirit to a nonce word,
   hence the name. It is often a random or pseudo-random
   number issued in an authentication protocol to ensure
   that old communications cannot be reused in replay attacks.
   They can also be useful as initialization vectors and in
   cryptographic hash functions.
'''

sig = EINSTEIN.ECDSA_N(P, message, privateKey)
print("The ECDSA_N signature is: ")
print("sig = ",  sig)

#Verification
z = h(message + str(sig['r'])) 
sinv = pow(sig['s'], ecc_n-2, ecc_n)
P1 = EINSTEIN.mulP(P, sinv * z)
P2 = EINSTEIN.mulP(publicKey, sinv * sig['r'])
r = EINSTEIN.addP(P1, P2)[0]
assert( r % ecc_n == sig['r'] )

print("Test security of RSA and Rabin Signature")
print(5000)
import random
print("******************************************** 70 *********************")
for x in range(20): 
   EINSTEIN.test(random.randint(1,2**70), EINSTEIN.PP(50000), 10000)
   print("x = ",x)
print("******************************************** 80 *********************")
for x in range(20): 
   EINSTEIN.test(random.randint(1,2**80), EINSTEIN.PP(50000), 10000)
   print("x = ",x)
print("******************************************** 100 *********************")
for x in range(20): 
   EINSTEIN.test(random.randint(1,2**100), EINSTEIN.PP(200000), 10000)
   print("x = ",x)

