from .ReadHelper import read_int_8, read_int_16be, signed8, signed16


def read(f, out, settings=None):
    f.seek(0x11E, 1)
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        dy = -signed16(read_int_16be(f))
        dx = signed16(read_int_16be(f))
        c = signed8(read_int_8(f))
        dy -= c
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        out.stitch(dx, dy)
