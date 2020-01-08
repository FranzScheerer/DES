'''
In cryptography the Rabin signature algorithm is a method
of digital signature originally proposed by Michael O. Rabin
in 1979. 

The Rabin signature algorithm was one of the first digital 
signature schemes proposed, and it is the only one to relate
the hardness of forgery directly to the problem of integer
factorization. 

The Rabin signature algorithm is existentially unforgeable
in the random oracle model assuming the integer factorization
problem is intractable. The Rabin signature algorithm is 
also closely related to the Rabin cryptosystem.

But, the RSA cryptosystem has a prominent role in the early
days of public key cryptography, and the Rabin signature 
algorithm is not covered in most introductory courses 
on cryptography.
'''

import sys
''' PUBLIC KEY
    This is the public key. You must fisrt insert
    the right values here before you can verfiy
    the signature.
'''    
nrabin =  28680905569579940177985684473970562124623018306535655627207222012150172760011185475402242217194092115107462027514678157485729910987072581089035116348883167252907570816551933329432686980185238562655615647501030115992095185830275722327270830812024740087182129247813994728281269758499689871263952355591093
afactor =  5
bfactor =  6

''' 
PUBLIC KEY
'''    

# *******************************************************************************
# HASH FUNCTION WITH SPRITZ
# *******************************************************************************
def updateSPZ():
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    iSPZ = (iSPZ + wSPZ) % 256
    jSPZ = sSPZ[(jSPZ + sSPZ[ iSPZ ]) % 256]
    sSPZ[ iSPZ ], sSPZ[ jSPZ ] = sSPZ[ jSPZ ], sSPZ[ iSPZ ]

def outputSPZ():
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    updateSPZ()
    return sSPZ[jSPZ]

def shuffleSPZ():
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    for v in range(256):
        updateSPZ()    
    wSPZ = (wSPZ + 2) % 256
    aSPZ = 0

def absorb_nibbleSPZ(x):
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    if aSPZ == 63:
        shuffleSPZ()
    sSPZ[aSPZ], sSPZ[240 + x] = sSPZ[240 + x], sSPZ[aSPZ]
    aSPZ = aSPZ + 1

def absorb_byteSPZ(b):
    absorb_nibbleSPZ(b % 16)
    absorb_nibbleSPZ(b >> 4)

def squeezeSPZ(out, outlen):
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    shuffleSPZ()
    shuffleSPZ()
    shuffleSPZ()
    for v in range(outlen):
        out.append( outputSPZ() )

def h(x):
  global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
  global nrabin
  jSPZ = iSPZ = aSPZ = 0
  wSPZ = 1
  sSPZ = list(range(256))
  for c in x.encode():
     absorb_byteSPZ(c) 
  res = []
  squeezeSPZ(res, 128)
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out % (nrabin)

def code2num(x):
  res = 0
  for c in x:
     if ord(c) >= 48 and ord(c) < 58:
       res = (res << 6) + ord(c) - 48
     if ord(c) >= 65 and ord(c) < 91:
       res = (res << 6) + ord(c) - 55
     if ord(c) >= 97 and ord(c) < 123:
       res = (res << 6) + ord(c) - 61
     if c == '#': 
       res = (res << 6) + 62
     if c == '/': 
       res = (res << 6) + 63
  return res

def vF(s, txt):
  a = afactor
  b = bfactor
  h0 = h(txt)
  ha = (a*h0) % nrabin
  hb = (b*h0) % nrabin
  hab = (a*b*h0) % nrabin

  sq = (s * s) % nrabin

  return (h0 == sq) or (ha == sq) or (hb == sq) or (hab == sq)
 
 
print ("\n\n RABIN SIGNATURE - copyright Scheerer Software 2019 - 2020\n\n")
print ("First parameter is V (Verify) or S (Sign) or G (Generate) \n\n")

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print ("result of verification: " + str(vF(code2num(sys.argv[3]),sys.argv[2])))

