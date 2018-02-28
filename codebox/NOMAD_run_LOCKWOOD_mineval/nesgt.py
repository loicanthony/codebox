#!/usr/bin/env python
import sys
import subprocess

args_to_bb = ' '.join(sys.argv[1:])
process = subprocess.Popen(['./bb.exe ' + args_to_bb], shell=True, stdout=subprocess.PIPE)
process.wait()

sys.stdout.write('-'+process.communicate()[0])
