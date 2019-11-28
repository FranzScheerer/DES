import sys

crabin =   '24O49OhPkEt6wGslwOgkwNylcjeagSyqFp8cFSazODDI9s4/I#TYR9OYfvTY49'
crabin +=  'lXCOugd88UBaLOX6u3ryeLfjGbpHe7ib18rYC2M160hp04dwRIeDH9L9mvwXOUTdt'
crabin +=  'GyaufZNRRCTX4#tXfEaWCtL2HJIa9XDv7gq7pg9X'
afactor =  3
bfactor =  6

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
    absorb_nibble_h(b >> 4)

def squeeze_h(out, outlen):
    global a_h,i_h,j_h,w_h,s_h
    shuffle_h()
    for v in range(outlen):
        out.append(output_h())

def h(x):
  global a_h,i_h,j_h,w_h,s_h
  j_h = i_h = a_h = 0
  w_h = 1
  s_h = []
  for ix in range(256):
    s_h.append(ix)

  for c in x:
     absorb_byte_h(ord(c)) 
  res = []
  squeeze_h(res, 128)
  out = 0 
  for bx in res:
    out = (out<<8) + bx
  return out % (nrabin)


def hb(x):
  global a_h,i_h,j_h,w_h,s_h
  j_h = i_h = a_h = 0
  w_h = 1
  s_h = []
  for ix in range(256):
    s_h.append(ix)

  for c in x:
     absorb_byte_h(c) 
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
  
def writeNumber(n, fnam):
  f = open(fnam, 'wb')
  while n > 0:
    b = n & 0xFF
    n >>= 8
    f.write(bytes([b]))
  f.close()

def readNumber(fnam):
  f = open(fnam, 'rb')
  n = 0
  for c in reversed(f.read()):
    n = (n << 8) ^ c   
  f.close()
  return n

def hF(fnam):
  f = open(fnam,'rb')
  return hb(f.read())

def vF(s, fnam):
  a = afactor
  b = bfactor
  h0 = hF(fnam)
  ha = (a*h0) % nrabin
  hb = (b*h0) % nrabin
  hab = (a*b*h0) % nrabin

  sq = (s * s) % nrabin

  return (h0 == sq) or (ha == sq) or (hb == sq) or (hab == sq)
 
print ("\n rabin signature - copyright Scheerer Software 2019 - all rights reserved\n\n")
print ("First parameter is V (Verify)\n\n")


if  len(sys.argv) == 4 and sys.argv[1] == "V":
  print ("result of verification: " + str(vF(code2num(sys.argv[3]),sys.argv[2])))

