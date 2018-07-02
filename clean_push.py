from subprocess import call
import sys
v = 1.0
try:
	with open('version.txt', 'r+') as f:
		v = f.readline()
except:pass
with open('version.txt', 'w+') as f:
	f.write(str(round(float(v),1) + 0.1))

call(['rm', '-r', '__pycache__'])
call(['git', 'add', '.'])
call(['git', 'commit', '-m', "version " + str(round(float(v),1))])
call(['git', 'push'])
