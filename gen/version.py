from __future__ import with_statement
import subprocess
import sys
import datetime
import os
import errno
from StringIO import StringIO

from common import putp

# call a command with arguments specified in args
# and returns the stdout.
# That is, if the command exists and no text is written to stderr.
# Otherwise it returns False.
def call(args):
	try:
		p = subprocess.Popen(args, 
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
	except OSError as e:
		# errno.ENOENT ~ "No such file or directory"
		if e.errno == errno.ENOENT:
			return False
		raise e
	info = p.stdout.read()
	err = p.stderr.read()
	if err:
		# there was an error!
		return False
	return info

def put_command_info(label, args, buf):
	info = call(args)
	if not info:
		return
	buf.write("{\\bf %s} %s --- " % (label,info))

def put_svn_info(buf):
	put_command_info("svn", ['./svn-revision.sh'], buf)

GIT_COMMAND = ['git','log','HEAD^..HEAD', "--format=%ad (%h)", 
		"--date=short"]

def put_git_info(buf):
	put_command_info("git", GIT_COMMAND, buf)

def main():
	# Get what we think "version.tex" should be.
	buf = StringIO()

	buf.write("\\newcommand{\\version}{ ")
	put_git_info(buf)
	put_svn_info(buf)
	buf.write("{\\bf compiled} "+str(datetime.datetime.now().date()))
	buf.write('}\n')

	buf.write("\\newcommand{\\shortversion}{ ")
	buf.write(call(GIT_COMMAND).strip())
	buf.write("}\n")

	result = buf.getvalue()
	buf.close()

	putp("version.tex", result, "gen/version.py")



main()


	


