from .ReadHelper import read_int_16be, read_int_8


def read_cnd_stitches(f, out):
    while True:
        control = read_int_8(f)
        if control is None:
            break
        x = read_int_16be(f)
        y = -read_int_16be(f)
        if control & 0x20:
            y = -y
        if control & 0x40:
            x = -x
        if y is None:
            break
        if control & 0xF == 0x07:  # Jump
            out.trim()
            continue
        if control & 0xF == 0x01:
            out.stitch_abs(x, y)
            continue
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    read_cnd_stitches(f, out)
