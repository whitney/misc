#!/usr/bin/env python

import sys
import re
from sympy.solvers import solve
from sympy import Symbol
from sympy import Lambda

"""
This program uses polynomial interpolation (http://en.wikipedia.org/wiki/Polynomial_interpolation) 
to determine the polynomial p which best 'fits' the provided sequence. 

Given any sequence of numbers [a0, a1, a2, ..., an], we use polynomial interpolation to find 
an n-1 degree polynomial p such that p(i) = ai.

To find this polynomial we have to solve a matrix multiplication equation which gives us a 
system of n+1 equations, which we solve with the sympy solvers module.

Once we determine the polynomial 'fitting' our sequence we simply plugin n+1, ..., n+10 to find 
the next ten elements in the sequence.
"""

def main(int_seq):
	seq_rgx = re.compile('\W+')
	ints = seq_rgx.split(int_seq)
	degree = len(ints)-1 # degree of the polynomial we're looking for

	coeffs,image,vandermonde_matrix = gen_matrices(ints, degree)

	eqns = gen_equations(vandermonde_matrix, coeffs, image, degree)

	# solve system to determine interpolation polynomial
	soln = solve(eqns, coeffs)
	poly = gen_poly(soln, coeffs, degree)

	f = Lambda(Symbol('x'), poly)
	
	# compute the next 10 elems in the seq using the interpolation poly
	for n in range(degree+1, degree+11):
		print("{0}th elem: {1}".format(n+1, f(n)))

def gen_poly(soln, coeffs, degree):
	x = Symbol('x')
	poly = soln[coeffs[0]]*x**degree
	for i in range(1,degree+1):
		poly += soln[coeffs[i]]*x**(degree-i)
	return poly

def gen_equations(vandermonde_matrix, coeffs, image, degree):
	eqns = [] # system of equations
	for idx, row in enumerate(vandermonde_matrix):
		eqn = row[0] * coeffs[0]
		for col in range(1,degree+1):
			eqn += row[col] * coeffs[col]

		eqn -= image[idx]
		eqns.append(eqn)
	return eqns

def gen_matrices(seq, degree):
	coeffs = []
	image = [] # this is the 'range' of the polynomial we're looking for
	vandermonde_matrix = []

	for idx, num in enumerate(seq):
		num = int(num)
		assert(idx == 0 or int(seq[idx-1]) <= num) # ensure increasing

		image.append(num)
		coeffs.append(Symbol('a'+str(degree-idx)))

		vdm_row = []
		for i in range(degree): 
			vdm_row.append(idx**(degree-i))
		vdm_row.append(1)
		vandermonde_matrix.append(vdm_row)

	return coeffs,image,vandermonde_matrix

if __name__ == "__main__":
	if len(sys.argv) != 2:
		usg =  "usage: int_seq.py <comma_seperated_increasing_int_seq>\n"
		usg += "ex. ./int_seq.py '1,9,25,49'"
		print usg
		sys.exit(1)

	int_seq = sys.argv[1]
	main(int_seq)
