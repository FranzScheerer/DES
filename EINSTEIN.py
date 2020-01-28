'''
  Diese Klasse ist total genial, deshalb heißt sie 

  EINSTEIN KLASSE ;)
  
  Copyright (c) 2020 Scheerer Software 
  All rights reserved - alle Rechte vorbehalten 
'''
import random

class EINSTEIN:

  def trueRandom(H):
    H.a = random.randint(0,255)
    H.i = random.randint(0,255)
    H.j = random.randint(0,255)
    H.w = 2*random.randint(0,127) + 1
    H.s = list(range(256))
    for i in range(1000):
       H.s[H.i], H.s[H.j] = H.s[H.j], H.s[H.i]
       H.i = random.randint(0,255)
       H.j = random.randint(0,255)

  def init(H):
    H.i = H.j = H.a = 0
    H.w = 13
    H.s = [186, 133, 249, 206, 35, 127, 235, 58, 172, 156, 148, 137, 113,
           147, 136, 204, 159, 45, 196, 243, 139, 229, 57, 149, 180, 247, 
           185, 150, 162, 87, 23, 222, 146, 192, 173, 237, 119, 120, 43, 
           32, 201, 8, 182, 248, 27, 6, 4, 233, 171, 36, 128, 106, 26, 152,
           174, 68, 60, 116, 141, 67, 84, 129, 161, 199, 216, 143, 52, 244,
           124, 51, 66, 215, 101, 25, 30, 135, 10, 220, 193, 33, 112, 231,
           197, 98, 20, 93, 179, 175, 203, 208, 107, 75, 76, 221, 122, 21, 214, 
           212, 11, 42, 130, 230, 251, 188, 111, 151, 86, 167, 24, 218, 31, 74, 
           94, 163, 81, 183, 145, 255, 47, 9, 44, 88, 236, 252, 38, 28, 213, 104,
           105, 228, 18, 15, 41, 92, 109, 110, 238, 241, 126, 83, 62, 176, 79,
           253, 157, 195, 14, 232, 217, 138, 134, 39, 170, 227, 72, 40, 64,
           12, 29, 131, 164, 114, 55, 224, 178, 100, 187, 48, 108, 99, 53, 19,
           211, 226, 191, 54, 207, 91, 245, 117, 190, 169, 61, 96, 200, 59, 77,
           65, 144, 210, 46, 198, 71, 202, 168, 240, 160, 2, 0, 123, 37, 194, 158,
           22, 140, 166, 95, 7, 17, 50, 121, 97, 103, 70, 69, 13, 3, 242, 85, 118,
           80, 89, 142, 219, 165, 223, 246, 73, 82, 90, 177, 125, 102, 5, 250, 49,
           132, 16, 1, 155, 225, 181, 56, 239, 205, 63, 34, 189, 154, 209, 184, 78,
           115, 254, 234, 153]
       
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
    H = EINSTEIN()
    EINSTEIN.init(H)
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

#    
# The hash has 20 Bytes, 160 Bits output like 
# the most famous hash function of the world 
# SHA-1
#
def h(x):
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
Jetzt mit wirklich geheimen privateKey:
knoppix@Microknoppix:~$ python3 Einstein.py
A prime greater than 2^141
p =  256720937847416416719320263092896073801153427
The base point is: 
 P =  [92078480886683387215913498910810247905170284, 40947367689051583059937238585334772307041483]
The public key is the point: 
publicKey =  [160864477288199191601687665837873216269146054, 118839288427090957263623062207631219027743850]
The signature is: 
sig =  {'s': 40044821288411386228336633515934671164199071, 'e': 7017085782106084387282504533057023059850811}
The signature is: 
sig =  {'s': 29894892226540636659019679439320177039516900, 'r': 57165726512791895295253814044235168822619777}

          DIE LICHTABLENKUNG DURCH SCHWERKRAFT
------------------------------------------------------
I. Die klassische Berechnung

Die Sonne, eine Punktmasse befinde sich im Ursrung
unseres Koordinatensystems.

Das Lichtteilchen bewege sich in großer Entfernung x0
zur Sonne in x Richtung auf die Sonne zu. Mit der Licht-
geschwingkeit c.

Der Abstand zur y-Achse Y0 = R sei der Sonnenradius
und in guter Nährerung konstant.

Wir berechnen die Winkeländerung im Bogenmaß entlang 
einer kurzen Wegstrecke dx. Der Winkel wird also angegeben
durch die Bogenlänge im Einheitskreis wie in der 
Mathematik üblich.

Das Licht lege die Strecke dx in der Zeit 

dt = dx/c 

zurück.

Zur Winkelbestimmung berechnen wir zunächst die Kraft nach
Newtons Kraftgesetz. Wir benötigen nur die Komponente der
Kraft senkrecht zu Strahlrichtung (y-Richtung). 

Aus der Energie E des Lichtteilchens können wir die Masse M
des Lichtteilchens berechnen.

M = E/c^2

Wir brauchen die Masse M tatsächlich gar nicht
kennen, weil sie sich bei der Berechnung der 
Geschschwingitkeitsänderung, der Beschleunigung
herauskürzt. Aus den Beschleunigung können die 
Geschwingkeitsänderung dv denkrecht zur x-Achse 
berechnen und daraus schließlich die Winkeländerung 

d(phi) = dv/c = (1/c) ((GM)/r^2) (y/r) (dx/c)

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
hinaus. Das Ergbnis finden wir zum Beispiel mit 
Wolfram Alpha:

https://www.wolframalpha.com

Ergebnis der klassischen Berechnung:

Winkelabweichung im Bogenmaß  (1 rad = 1° mal (pi/180) 
Eine Bogensekunde (1'') = pi / (180 * (60*60))
pi = 3.1415.... die berühmte Kreiszahl

Die gesamte Winkeländerung nach Integration:

         Delta phi  = 2 * (GM/c^2) / R

R muss nicht der Sonnenradius sein, allgemein kann R
als der Abstand in dem das Teilchen die Sonne 
passiert betrachtet werden. Aber R ist immer größer 
oder gleich dem Radius der Sonne, versteht sich.

Einstein sagte 1915 (Allgemeine Relativitätstheorie):
Die Winkelabweichung ist genau:

         Delta phi = 4 * (GM/c^2) / R

... und wer kann mir das jetzt einmal erklären,
woher kommt der zusätzliche Faktor zwei ?????????
'''
#Generate the private key from a secret password
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
sig = EINSTEIN.ECDSA_N(P, message, privateKey)
print("The signature is: ")
print("sig = ",  sig)

#Verification
z = h(message + str(sig['r'])) 
sinv = pow(sig['s'], ecc_n-2, ecc_n)
P1 = EINSTEIN.mulP(P, sinv * z)
P2 = EINSTEIN.mulP(publicKey, sinv * sig['r'])
r = EINSTEIN.addP(P1, P2)[0]
assert( r % ecc_n == sig['r'] )
