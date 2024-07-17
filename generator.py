#sage -python *.py

from sage.all import *
from random import randrange
from math import gcd
from sympy import isprime,nextprime

print('Python initialized')
print()

# nxn matrix over a finite field 
n=4
b=16
p=nextprime(randrange(2**(b-1)))
print(f'p={p}')
R=GF(p)

# This must be done once for all signers
def factors(nm):
	f=list(factor(nm))
	return [f[i][0] for i in range(len(f))]

# We choose p^(n-1) instead of p^n to find a generator
q=p**(n-1)
fct=factors(q-1)
print(f'Prime factors of {q-1} are {fct}')
print()

# Return random matrix with coefficients in GF(p)
# with last two rows equal
def rand_matrix():
	M=matrix(R,[[randrange(p) for i in range(n)] for j in range(n)])
	for i in range(n):
		M[n-1,i]=sum([M[j,i] for j in range(n-1)])%p
	return M

#Look for a generator with order p^(n-1)-1
def gen_matrix():

	while True:
		A=rand_matrix()
		V=A**q
		if A==V:
			j=0
			while j<len(fct):
				if V**((q-1)//fct[j]+1)==V:
					break
				j+=1
			if j!=len(fct):
				continue
			else:
				break
	return A

# A costly check that the generator is of maximal order
if False:
	V=A
	for j in range(1,q-2):
		V=V*A
		if V==A:
			print('subset',j)
			quit()

A,G=gen_matrix(),gen_matrix()

print('Generators:')
print(A)
print(G)
print()
if A!=A**q:
	print('Generator check failed')

# Define order and check that the hash has no common
# divisors with the order
o=q-1
k,c,h=[randrange(o) for _ in range(3)]
while gcd(h,o)!=1:
	h=(h+1)%o
	
print('Private keys and number to sign:')
print(f'k={k}, c={c}, h={h}')
print()

# Compute a working q for the hash h
# k+qh=c q=(c-k)/h
#q=((c-k)*pow(h,-1,o))%o
q=(c*pow(h,-1,o)-k)%o

print('Exponent for the signature of h:')
print(f'q={q}')
print()
print('Signature of h:')
print(G*A**q)
print()

# Correctness of the signature verification
LF=G*A**(k*h)*A**(q*h)
RG=G*A**c

if LF==RG:
	print('(A^kh A^q)^h=A^c=')
	print(LF)
	print()
	print(f'Signature verified (p={p})')
else:
	print('Something wrong happened')


