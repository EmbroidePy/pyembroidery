from __future__ import print_function

from pyembroidery import *


def value_input(prompt):
    try:
        return str(raw_input(prompt))
    except NameError:
        return str(input(prompt))


pattern = EmbPattern()
while True:
    triple = False
    prompt = value_input("(T)riple/(S)ingle/(Q)uit?")
    if "t" in prompt or "T" in prompt:
        triple = True
    if "s" in prompt or "S" in prompt:
        triple = False
    if "q" in prompt or "Q" in prompt:
        break
    while True:
        needle_position = value_input(" - :")
        try:
            int_needle = int(needle_position)
        except ValueError:
            break
        fabric_position = value_input(" | : ")
        try:
            int_fabric = int(fabric_position)
        except ValueError:
            break
        int_needle -= 7
        int_needle *= 2
        pattern.stitch_abs(int_fabric * 2.5, int_needle * 2.5)
        if triple:
            try:
                previous = pattern.stitches[-2]
                pattern.stitch_abs(previous[0], previous[1])
                pattern.stitch_abs(int_fabric * 2.5, int_needle * 2.5)
            except IndexError:
                pass

filename = value_input("Filename? ")
if filename is None:
    filename = "stitch.pmv"
if filename[:3] != 'pmv':
    filename += '.pmv'
write(pattern, filename)
