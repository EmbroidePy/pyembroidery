from __future__ import print_function

import sys
from pyembroidery import *

if len(sys.argv) <= 1:
    print("No command arguments")
    exit(1)
input_file = sys.argv[1]
pattern = read(input_file)

write(pattern, input_file + ".dst")
write(pattern, input_file + ".exp")
write(pattern, input_file + ".vp3")
write(pattern, input_file + ".pes")
write(pattern, input_file + ".jef")
write(pattern, input_file + ".u01")
