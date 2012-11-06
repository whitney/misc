#!/usr/bin/env python

import sys
import re

def main(search_word, text_file):

	try:
		f = open(text_file)
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		sys.exit(1)

	count = 0
	distances = []
	curr_dist = 0
	found = False

	line_rgx = re.compile('\W+')
	word_rgx = re.compile(search_word, flags=re.IGNORECASE)

	for line in f:
		words = line_rgx.split(line)
		for word in words:
			if not word: continue
			if word_rgx.match(word):
				if found:
					distances.append(curr_dist)
				else:
					found = True
				count += 1
				curr_dist = 0
			else:
				curr_dist += 1
	
	avg_dist = float(sum(distances))/len(distances) if len(distances) > 0 else float('nan')

	print "Token occurences: {0}".format(count)
	print "Avg distance: {0}".format(avg_dist)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		usg =  "usage: word_count.py <word> <path_to_file>\n"
		usg += "ex. ./word_count.py peace WarAndPeace.txt"
		print usg
		sys.exit(1)

	word = sys.argv[1]
	text_file = sys.argv[2]
	main(word, text_file)
