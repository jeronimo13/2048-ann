from pprint import pprint

import numpy

np = numpy



a = numpy.array([1, 2, 3])
b = numpy.array([5, 6,3])
c =numpy.stack([a,b])
concatenate = numpy.concatenate([a, b])

pprint(concatenate)
