import sys

crabin = '4BHc94p6cZohh5KfZfvWfF1Pr8nRK77kpzdGhihgG/I2mmqlGWapPh2KvMxa825MFSiUrv2lShyKt4uadqEcDPimmRha2/8xqSi8Icp1k/T38sV109xGsoOPZEf2b5zJEkjpUtkgmOuRXRJvukbLNDdyLCkaJLV2DzmZhKT'
afactor =  5
bfactor =  3

def update_h():
    global a_h,i_h,j_h,w_h,s_h
    i_h = i_h + w_h 
    if i_h > 255:
       i_h = i_h - 256
    j_h = j_h + s_h[ i_h ]
    if j_h > 255:
      j_h = s_h[ j_h - 256 ]
    else:
      j_h = s_h[ j_h ]
    t = s_h[i_h] + s_h[j_h] 
    s_h[ j_h ] = t - s_h[ j_h ]
    s_h[ i_h ] = t - s_h[ i_h ]

def output_h():
    global a_h,i_h,j_h,w_h,s_h
    update_h()
    return s_h[j_h]

def shuffle_h():
    global a_h,i_h,j_h,w_h,s_h
    for v in range(256):
        update_h()    
    w_h = (w_h + 2) % 256
    a_h = 0

def absorb_nibble_h(x):
    global a_h,i_h,j_h,w_h,s_h
    if a_h == 241:
        shuffle_h()
    s_h[a_h], s_h[240 + x] = s_h[240 + x], s_h[a_h]
    a_h = a_h + 1

def absorb_byte_h(b):
    absorb_nibble_h(b % 16)
    absorb_nibble_h(b / 16)

def squeeze_h(out, outlen):
    global a_h,i_h,j_h,w_h,s_h
    if a_h != 0:
        shuffle_h()
    for v in range(outlen):
        out.append(output_h())

def h(x):
  global a_h,i_h,j_h,w_h,s_h
  j_h = i_h = a_h = 0
  w_h = 1
  s_h = range(256)
  for c in x:
     absorb_byte_h(ord(c)) 
  res = []
  squeeze_h(res, 128)
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
  
def root(m, p, q):
  x = h(m)
  a = afactor
  b = bfactor
  if pow(x, (p-1)/2, p) > 1:
    x *= a
  if pow(x, (q-1)/2, q) > 1:
    x *= b
#  print pow(x, (q-1)/2, q)
#  print pow(x, (p-1)/2, p)
  return (pow(p,q-2,q) * p * pow(x,(q+1)/4,q) + pow(q,p-2,p) * q * pow(x,(p+1)/4,p)) % (nrabin) 


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
 
print "\n rabin signature - copyright Scheerer Software 2019 - all rights reserved\n\n"
print "First parameter is V (Verify)\n\n"


if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print "result of verification: " + str(vF(code2num(sys.argv[3]),sys.argv[2]))

