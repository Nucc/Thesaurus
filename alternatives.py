#!/usr/bin/env python
try:
	import sys
	import enchant
	d = enchant.Dict("en_US")
	print("alternatives = " + str(d.suggest(sys.argv[1])))
except Exception as err:
	print("alternatives = ['error', '%s']" % err)