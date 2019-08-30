import random, hashlib, sys

nrsa = 29746358878928083861237817222954677677152481785351811006421449568488007506618838431501380761939331839202115522100484371951305362698541726995193181514480854479235870344802990899716815205765298780141729114308584093033967074038423933744823970683410211257431791252652117523816679871100597902024086062137064382361

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
  return out % (nrsa)


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
 
def hF(fnam):
  f = open(fnam,'r')
  return h(f.read())

def vF(fnam,s):
  f = open(fnam,'r')
  return  h(f.read()) == pow (s, e, nrsa)
 
e = 2**127 - 1

print "\n\n rsacrypt - copyright Scheerer Software 2017 - 2019 all rights reserved\n\n"
print "First parameter is V (Verify) \n\n"

#
# Parameter V <file> <signature>
#
if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(sys.argv[2], code2num(sys.argv[3])))

     
