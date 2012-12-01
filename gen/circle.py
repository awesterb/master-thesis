from StringIO import StringIO

from common import putp
from cmath import exp, pi


DEPTH = 6
SIZE = 4

HEAD = \
"""\\begin{center}
\\begin{tikzpicture}
"""

TAIL = \
"""%\\draw (0cm,0cm) circle(1cm);

\\end{tikzpicture}
\\end{center}
"""

def main():
	buf = StringIO()
	buf.write(HEAD)
	
	idcs = [i+1 for i in xrange(DEPTH)]
	idcs.reverse()
	for i in idcs:
		#write_poly(buf, i, int(100 - 100 * (i/float(DEPTH))))
		write_poly(buf, i, 100)
	buf.write(TAIL)
	result = buf.getvalue()
	buf.close()

	putp("circle.tex", result, "gen/circle.py")

def write_poly(buf,n,color):
	buf.write("\\draw[thin,black!%s] " % (color,))
	
	# get the coordinates using the complex exponential
	coords = []
	Ncoords = 2 ** (n+1)
	gen_coord = exp(2j*pi / Ncoords)
	cur = gen_coord
	for i in xrange(Ncoords):
		coords.append(cur)
		cur *= gen_coord	

	# add gen_coord to the end to `complete the circle'
	coords.append(gen_coord)
	
	lines = "\n\t -- ".join(map(cx_to_coord, coords))

	buf.write(lines)
	buf.write(";\n\n")


def cx_to_coord(z):
	z *= SIZE
	return "({0:.20f}cm,{1:.20f}cm)".format(z.real,z.imag)




if __name__=="__main__":
	main()
