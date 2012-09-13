from __future__ import with_statement
import subprocess
import sys
import datetime
import os
import errno
from StringIO import StringIO

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

def put_git_info(buf):
	put_command_info("git", ['git','log','HEAD^..HEAD', 
		"--format=%ai (%h)"], buf)

def main():
	# Get what we think "version.tex" should be.
	buf = StringIO()
	buf.write("\\newcommand{\\version}{ ")
	put_git_info(buf)
	put_svn_info(buf)
	buf.write("{\\bf compiled} "+str(datetime.datetime.now().date()))
	buf.write('}\n')
	result = buf.getvalue()
	buf.close()

	# Get what "version.tex" actually is.
	buf = StringIO()
	if os.path.exists("version.tex"):
		with open("version.tex", "r") as f:
			while True:
				read = f.read()
				if not read:
					break
				buf.write(read)
	old = buf.getvalue()
	buf.close()

	
	if old==result:
		print "(gen-version: no changes)"
		return

	# Correct "version.tex"
	print "gen-version: version.tex has changed"
	with open("version.tex", "w") as f:
		f.write(result)

main()


	


