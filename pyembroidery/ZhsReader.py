from .ReadHelper import signed8, read_int_32le


def read_zhs_stitches(f, out):
    count = 0
    while True:
        count += 1
        b = bytearray(f.read(3))
        if len(b) != 3:
            break
        ctrl = b[0]
        if ctrl == 0x10:
            pass
        x = signed8(b[1])
        y = signed8(b[2])
        if ctrl == 0x02:
            out.stitch(x, y)
            continue
        if ctrl == 0x01:
            out.move(x, y)
            continue
        if ctrl == 0x04:
            out.color_change()
            continue
        if ctrl == 0x80:
            break
    out.end()


def read(f, out, settings=None):
    f.seek(0x0F, 0)
    stitch_start_position = read_int_32le(f)
    f.seek(stitch_start_position, 0)
    read_zhs_stitches(f, out)
