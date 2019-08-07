import sys

crabin =  '658ak9OxOEUcONnbDo9BfSREHPsSCCME'
crabin += 'Th15Mh6jrMwIAaJ6WkM4wP2#UhybruIq'
crabin += 'IoOaa6s7NrXf1bJgcHk7A#SYbhjTEoynf'
crabin += 'bDGnP48wrBxxP9J9diydrL6BfYA5FOXB'
crabin += 'i44bNJ2y5moKvJIhowkzO6GvydQ6AQBkR5goZP'

afactor = 41
bfactor = 3

def update_spr():
    global a_spr, i_spr, j_spr, w_spr, s_spr
    i_spr = i_spr + w_spr
    if i_spr > 255:
       i_spr = i_spr - 256
    j_spr = j_spr + s_spr[ i_spr ]
    if j_spr > 255:
      j_spr = s_spr[ j_spr - 256 ]
    else:
      j_spr = s_spr[ j_spr ]
    tsum = s_spr[ i_spr ] + s_spr[ j_spr ] 
    s_spr[ i_spr ] = tsum - s_spr[ i_spr ] 
    s_spr[ j_spr ] = tsum - s_spr[ j_spr ] 

def output_spr():
    global a_spr, i_spr, j_spr, w_spr, s_spr
    update_spr()
    return s_spr[ j_spr ]

def shuffle_spr():
    global a_spr, i_spr, j_spr, w_spr, s_spr
    for v in range(256):
        update_spr()    
    w_spr = w_spr + 2
    if w_spr == 255:
       w_spr = 1
    a_spr = 0

def absorb_nibble_spr(x):
    global a_spr, i_spr, j_spr, w_spr, s_spr
    if a_spr == 240:
        shuffle_spr()
    tsum = s_spr[a_spr] + s_spr[240 + x] 
    s_spr[ 240 + x ] = tsum - s_spr[ 240 + x ]
    s_spr[ a_spr ]   = tsum - s_spr[ a_spr ]
    a_spr = a_spr + 1

def absorb_byte_spr(b):
    absorb_nibble_spr(b % 16)
    absorb_nibble_spr(b / 16)

def squeeze_spr(out, outlen):
    global a_spr, i_spr, j_spr, w_spr, s_spr
    if a_spr != 0:
        shuffle_spr()
    for v in range(outlen):
        out.append(output_spr())

def h(x):
  global a_spr, i_spr, j_spr, w_spr, s_spr
  j_spr = i_spr = a_spr = 0
  w_spr = 1
  s_spr = range(256)
  for c in x:
     absorb_byte_spr(ord(c)) 

  res = []
  squeeze_spr(res, 128)

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
#
# calculate number from code value
#
nrabin = code2num(crabin)

def readNumber(fnam):
  f = open(fnam, 'rb')
  n = 0
  snum = f.read()
  for i in range(len(snum)):
    n = (n << 8) ^ ord(snum[len(snum)-i-1])   
  f.close()
  return n

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
 
print "\n\n rabin signature - copyright Scheerer Software 2019 - all rights reserved\n\n"
print "First parameter is V (Verify) or S (Sign)\n\n"

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(code2num(sys.argv[3]),sys.argv[2]))
