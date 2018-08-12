from .ReadHelper import read_int_8, read_int_32le, read_int_24le, signed24


def read(f, out, settings=None):
    f.seek(0xD5, 0)
    stitch_count = read_int_32le(f)
    for i in range(0, stitch_count):
        x = read_int_24le(f)
        c0 = read_int_8(f)
        y = read_int_24le(f)
        c1 = read_int_8(f)
        if c1 is None:
            break
        x = signed24(x)
        y = signed24(y)
        out.stitch_abs(x, y)
    out.end()
