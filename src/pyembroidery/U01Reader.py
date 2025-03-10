from .EmbConstant import *


def read_u01_stitches(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        ctrl = byte[0]
        dy = -byte[1]
        dx = byte[2]
        if (ctrl & 0x20) != 0:
            dx = -dx
        if (ctrl & 0x40) != 0:
            dy = -dy
        command = ctrl & 0b11111
        if command == 0x0:
            # Stitch
            out.stitch(dx, dy)
            continue
        if command == 0x01:
            # Jump
            out.move(dx, dy)
            continue
        if command == 0x02:
            # Fast
            out.add_stitch_relative(FAST)
            if dx != 0 or dy != 0:
                out.stitch(dx, dy)
            continue
        if command == 0x03:
            # Fast, Jump
            out.add_stitch_relative(FAST)
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x04:
            # Slow
            out.add_stitch_relative(SLOW)
            if dx != 0 or dy != 0:
                out.stitch(dx, dy)
            continue
        if command == 0x05:
            # Slow, Jump
            out.add_stitch_relative(SLOW)
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x06:
            # T1 Top Thread Trimming, TTrim.
            out.trim()
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x07:
            # T2 Bobbin Threading
            out.trim()
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if (
            command == 0x08
        ):  # ww, stop file had proper A8 rather than E8 and displacement
            # C00 Stop
            out.stop()
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if 0x09 <= command <= 0x17:
            # C01 - C14
            needle = command - 0x08
            out.needle_change(needle)
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x18:
            break
        if ctrl == 0x2B:
            break  # Rare postfix data from machine. Do not read this.
        break  # Uncaught Command
    out.end()


def read(f, out, settings=None):
    f.seek(0x80, 1)
    f.seek(0x80, 1)
    read_u01_stitches(f, out)
