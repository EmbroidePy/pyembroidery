def read_ksm_stitches(f, out):
    trimmed = False
    stitched_yet = False
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        y = -byte[0]
        x = byte[1]
        ctrl = byte[2]

        if ctrl & 0x40 != 0:
            x = -x
        if ctrl & 0x20 != 0:
            y = -y

        ctrl &= 0b11111
        if x != 0 or y != 0:
            if trimmed:  # any x, y gets executed regardless.
                out.move(x, y)
            else:
                out.stitch(x, y)
                stitched_yet = True

        if ctrl == 0x00:
            continue
        # print(str(f), " ", str(count), " ", str("{0:b}").format(ctrl), " 0x%0.2X " % ctrl, x, " ", y)

        if ctrl == 0x07 or ctrl == 0x13 or ctrl == 0x1D:
            if stitched_yet:
                out.trim()
            trimmed = True
            continue
        if 0x17 <= ctrl <= 0x19:  # start sewing again.
            trimmed = False
            continue
        if 0x0B <= ctrl <= 0x12:
            needle = ctrl - 0x0A
            out.needle_change(needle)
            trimmed = True
            continue
        if ctrl == 0x05:
            out.stop()
            continue
        if ctrl == 0x1B:  # Called before end command
            trimmed = False
            continue
        if ctrl == 0x08:  # End command #88 zero direction.
            break
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    f.seek(0x200, 0)
    read_ksm_stitches(f, out)
