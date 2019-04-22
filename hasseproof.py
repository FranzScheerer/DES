import math

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

for prime in primes:
 print "prime ", prime
 min = (prime + 0) - 2 * math.sqrt(prime)
 max = (prime + 0) + 2 * math.sqrt(prime)

 for a in range(prime):
  for b in range(prime):
    cnt = 1                   # point at infinity
#   print "prime ", prime, "\n cnt = ", cnt, " b = ", b
    for x in range(prime):
      yy = x*x*x +(a)*x + b
      if yy % prime == 0:
         cnt = cnt + 1
      else:
         if pow(yy, (prime-1)/2, prime) == 1:
           cnt = cnt + 2 
    if cnt > max or cnt < min:
      print "prime ", prime, " a = ", a, " b = ", b, " cnt = ", cnt

