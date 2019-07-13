from .ReadHelper import read_int_16be


def read_zxy_stitches(f, out):
    count = 0
    while True:
        count += 1
        b = bytearray(f.read(3))
        if len(b) != 3:
            break
        ctrl = b[0]
        x = b[1]
        y = -b[2]
        if ctrl & 0x08:
            x = -x
        if ctrl & 0x04:
            y = -y
        ctrl &= ~0x0C
        if ctrl == 0:
            out.stitch(x, y)
            continue
        if ctrl & 0x02:
            out.move(x, y)
            continue
        if ctrl & 0x20:
            if b[1] == 0xFF:
                break
            needle = b[2]
            out.needle_change(needle)
    out.end()


def read(f, out, settings=None):
    f.seek(0x01, 0)
    stitch_start_distance = read_int_16be(f)
    f.seek(stitch_start_distance, 1)
    read_zxy_stitches(f, out)
