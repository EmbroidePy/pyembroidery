from .ReadHelper import read_int_16le, read_int_8, signed16


def read(f, out, settings=None):
    f.seek(0x11E, 1)
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        dx = signed16(read_int_16le(f))
        dy = signed16(read_int_16le(f))
        c = read_int_8(f)
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if c == 0x00:
            out.stitch(dx, dy)
            continue
        if c == 0xA0:
            out.move(dx, dy)
            continue
        if c == 0xF6:
            out.move(dx, dy)
            continue
