from .ReadHelper import signed8


def read_exp_stitches(f, out):
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] != 0x80:
            x = signed8(b[0])
            y = -signed8(b[1])
            out.stitch(x, y)
            continue

        control = b[1]
        b = bytearray(f.read(2))  # 07 00
        if len(b) != 2:
            break
        x = signed8(b[0])
        y = -signed8(b[1])
        if control == 0x80:  # Trim
            out.trim()
            continue
        elif control == 0x02:
            out.stitch(x, y)
            # This shouldn't exist.
            continue
        elif control == 0x04:  # Jump
            out.move(x, y)
            continue
        elif control == 0x01:  # Colorchange
            out.color_change()
            if x != 0 or y != 0:
                out.move(x, y)
            continue
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    read_exp_stitches(f, out)
