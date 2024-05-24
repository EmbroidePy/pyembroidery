import re

from .EmbFunctions import *

PU_COMMAND = re.compile(r"PU\s*([0-9]+)\s*,\s*([0-9]+)")
PD_COMMAND = re.compile(r"PD\s*([0-9]+)\s*,\s*([0-9]+)")
SP_COMMAND = re.compile(r"SP\s*([0-9]+)\s*")


def read(f, out, settings=None):
    data = f.read()
    data = str(data, "utf8")
    lines = data.split(";")
    for line in lines:
        line = line.strip()
        match = PU_COMMAND.match(line)
        if match:
            x = int(match.group(1)) / 4.0
            y = int(match.group(2)) / 4.0
            out.move_abs(x, y)
            out.stitch_abs(x, y)

        match = PD_COMMAND.match(line)
        if match:
            x = int(match.group(1)) / 4.0
            y = int(match.group(2)) / 4.0
            out.stitch_abs(x, y)

        match = SP_COMMAND.match(line)
        if match:
            pen = int(match.group(1))
            out.needle_change(pen)

        if line == "EN":
            print("Done")
            break
