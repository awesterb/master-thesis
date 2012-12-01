from __future__ import with_statement
import os

from StringIO import StringIO

#
#  Write `value` to file at `path`,
#  but only if this changes the content of the file.
#  Returns whether writing `value` to the file at `path` was necessary.
#
def put(path, value):
	# read the current content of the file
	buf = StringIO()
	if os.path.exists(path):
		with open(path, "r") as f:
			while True:
				read = f.read()
				if not read:
					break
				buf.write(read)
	current = buf.getvalue()
	buf.close()

	if current==value:
		return False
	
	with open(path, "w") as f:
		f.write(value)
	
	return True


def putp(path, value, commandn):
	if put(path, value):
		print "%s: %s has changed" % (commandn, path)
	else:
		print "(%s: no changes to %s)" % (commandn, path)
