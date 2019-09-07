import sys, hashlib
# ******************************************************************************
# PUBLIC KEY
#
#crabin = 'YRIHHp5r2jMo0lGlz9eZH2HouQ6OcKmO#4dDQpDpoSqQELliuS1zbhRFxhPs7zFGG2nOl7dWwc2xInW5lNfY9as0nGLhKe16BoC3wDMKx5OHChOR3RLdHE1W9QfJG/FgldeZz07Y6mzfF5wqQpuN06/uib0gLP6QPXqpIWn'
#afactor =  6
#bfactor =  3

#crabin =  '4zmx8OD7vbXz#YssGea#JF/sdw4RyixR2KokAvbSeCPk6/M74A3ymvRr8GfKcAHxAOeW'
#crabin += 'BnvA10kQyOM1BfTckS8ZxU#QoddVlzKKeJWIOUDYuJIpGJ#N4djuLGdhSM9RQfnU6A/i'
#crabin += 'pmn/#LvH/C#ezSrvGGTBlVsXaY8vJ#L'

#afactor =  3
#bfactor =  7

#crabin = '3peYeoomxFJ2i4tDMficQRJN1n6Tfv5Lj4gFvrwZw2pe3Y6eVgiD7sDRWKNGWDFkDg#Ujpmg7MH5MbuicpKA35rlqsh#KIpJ/EijdjXLU/cwENt1hJCGYrxJ4s6YN5aqQlkoGoJ7Ex6IMhZAYu7L7Vq#ASseGIUD5HVg8c9'
#afactor =  11
#bfactor =  33

crabin = 'FyQkptYMNODa9fz/zwTi0vIumF0xYl5JBIY2dvARGrFlPXkUk#wGBF4MjEX/r1cuI1eh3BZxb1ZQzF#URpK6Yqjwpiyqg3RXDrw5nE05sq6Rzg72Q5RE0pZf8ib7p3Z2Fdx4Nd90X5LX/iro57N3/nwtYADmZQb49h22ks1'
afactor =  5
bfactor =  3
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
    if aSPZ == 240:
        shuffleSPZ()
    sSPZ[aSPZ], sSPZ[240 + x] = sSPZ[240 + x], sSPZ[aSPZ]
    aSPZ = aSPZ + 1

def absorb_byteSPZ(b):
    absorb_nibbleSPZ(b % 16)
    absorb_nibbleSPZ(b / 16)

def squeezeSPZ(out, outlen):
    global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
    if aSPZ != 0:
        shuffleSPZ()
    for v in range(outlen):
        out.append( outputSPZ() )

def hg(x):
  global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
  jSPZ = iSPZ = aSPZ = 0
  wSPZ = 1
  sSPZ = range(256)
  for c in x:
     absorb_byteSPZ(ord(c)) 
  res = []
  squeezeSPZ(res, 128)
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out % (2**1000)

#def h( arg ):
#  cstr_ =  hashlib.sha256(arg).digest()
#  out = 0 
#  for c in cstr_:
#    out = (out<<8) + ord(c)

#  return (out << 750) % (nrabin)

def h(x):
  global aSPZ, iSPZ, jSPZ, wSPZ, sSPZ
  jSPZ = iSPZ = aSPZ = 0
  wSPZ = 1
  sSPZ = range(256)
  for c in x:
     absorb_byteSPZ(ord(c)) 
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

nrabin = code2num(crabin)


def hF(fnam):
  f = open(fnam,'r')
  return h(f.read())

def vF(s, fnam):
  a = afactor
  b = bfactor
  h0 = hF(fnam)
  ha = (a*h0) % nrabin
  hb = (b*h0) % nrabin
  hab = (a*b*h0) % nrabin

  sq = (s * s) % nrabin

  return (h0 == sq) or (ha == sq) or (hb == sq) or (hab == sq)
 
print "\n\n RABIN SIGNATURE - copyright Scheerer Software 2019 - all rights reserved\n\n"
print "First parameter is V (Verify)  \n\n"

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(code2num(sys.argv[3]),sys.argv[2]))

