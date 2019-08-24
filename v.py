import sys, hashlib
#crabin = 'PMmPC1Ghzisi6UVQAidfKfw9qrEQAzgx#uYAuxHJyJZ9cO#EfKjrb3r1YKUw/3mSr/Nxc/BvYJBSf2dHC3HEnvxTLbIITwzC8Q9YhCeG2hswUPF9YmGvR4Fqt9N1kiz10XYDGBYo6f#gGXRi51VneO4kFwlF9fGogatU14L'
#afactor =  3
#bfactor =  7

#crabin = 'e5ROvXYsiG5cazuQD5iZjFnMnD#xhsD2yo/0NS2Hj0sLGVJwX2DYl3gLqMgyzyqolx3oU47Q5TqXE4xVF6lfmB1NWAPRqljSyxrce2vWjb6Jl9suKT281gA/RAs0sutXhF0SB5vK1Aq#7bF3Zh2ORrc6XiWicZtN28MSf41'
#afactor =  5
#bfactor =  3
crabin = '4zmx8OD7vbXz#YssGea#JF/sdw4RyixR2KokAvbSeCPk6/M74A3ymvRr8GfKcAHxAOeWBnvA10kQyOM1BfTckS8ZxU#QoddVlzKKeJWIOUDYuJIpGJ#N4djuLGdhSM9RQfnU6A/ipmn/#LvH/C#ezSrvGGTBlVsXaY8vJ#L'
afactor =  3
bfactor =  7

#crabin = 'g7YB1743P2dblx2oqa7FGNj2LsvhK9ei04NrvNgEt30OE/#XJ1cgRvcnUHy4bW/7wax/8NsmInEYi7X2mDKu3yUI9sd/#7cx/G7He3b6vb87/ouYoOJGE3ZJCTyM1MHE7YuAcTIPjILgAX4FLQvvXxjzn/r6MOL8XTS4M2v'
#afactor =  14
#bfactor =  7

def swap_h(x,y):
    global a_h,i_h,j_h,w_h,s_h
    s_h[x],s_h[y] = s_h[y],s_h[x]

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
    swap_h(i_h, j_h)

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
    if a_h == 240:
        shuffle_h()
    swap_h(a_h, 240 + x)
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

#def h( arg ):
#  cstr_ =  hashlib.sha256(arg).digest()
#  out = 0 
#  for c in cstr_:
#    out = (out<<8) + ord(c)

#  return (out << 750) % (nrabin)


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
  if pow(x, (q-1)/2, q) != 1 or pow(x, (p-1)/2, p) != 1:
    print "Errrrrrrrrrrrrrrrrrrror"
    return -1
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

