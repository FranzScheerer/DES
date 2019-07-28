import sys

nrabin = 1275574687529707052360270181001777089671167672089082721378211835809946265943774704298829077228926639950048281145477004890301800135170057571586644210706829514984111130118296710578328836619124873204558928730791403673479088571255223740478384830455590280922940539854528127509L

def update_spritz():
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    i_spritz = (i_spritz + w_spritz) % 256
    j_spritz = s_spritz[(j_spritz + s_spritz[i_spritz]) % 256]
    s_spritz[i_spritz], s_spritz[j_spritz] = s_spritz[j_spritz], s_spritz[i_spritz]

def output_spritz():
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    update_spritz()
    return s_spritz[j_spritz]

def shuffle_spritz():
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    for v in range(256):
        update_spritz()    
    w_spritz = (w_spritz + 2) % 256
    a_spritz = 0

def absorb_nibble_spritz(x):
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    if a_spritz == 240:
        shuffle_spritz()
    s_spritz[a_spritz], s_spritz[240 + x] = s_spritz[240 + x], s_spritz[a_spritz]
    a_spritz = a_spritz + 1

def absorb_byte_spritz(b):
    absorb_nibble_spritz(b % 16)
    absorb_nibble_spritz(b / 16)

def squeeze_spritz(out, outlen):
    global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
    if a_spritz != 0:
        shuffle_spritz()
    for v in range(outlen):
        out.append(output_spritz())

def h(x):
  global a_spritz,i_spritz,j_spritz,w_spritz,s_spritz
  j_spritz = i_spritz = a_spritz = 0
  w_spritz = 1
  s_spritz = range(256)
  for c in x:
     absorb_byte_spritz(ord(c)) 
  res = []
  squeeze_spritz(res, 128)
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

def num2code(x):
  res = ''
  while x > 0:
    y = x % 64
    if y < 10:
       res = chr( y + 48 ) + res
    elif y < 36:
       res = chr( y + 55 ) + res
    elif y < 62:
       res = chr( y + 61 ) + res 
    elif y == 62:
       res = '#' + res 
    elif y == 63:
       res = '/' + res 
    x /= 64
  return res

def hF(fnam):
  f = open(fnam,'r')
  return h(f.read())

def sF(fnam):
  p = readNumber("p")
  q = readNumber("q")

  f = open(fnam,'r')
  s = root (f.read(), p, q)
  f.close()
  return s

def vF(s, fnam):
  a = 5
  b = 3
  h0 = hF(fnam)
  ha = (a*h0) % nrabin
  hb = (b*h0) % nrabin
  hab = (a*b*h0) % nrabin

  sq = (s * s) % nrabin
  return (h0 == sq) or (ha == sq) or (hb == sq) or (hab == sq)
 
print "\n\n rabin signature - copyright Scheerer Software 2019 - all rights reserved\n\n"

if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(code2num(sys.argv[3]),sys.argv[2]))

     
                     