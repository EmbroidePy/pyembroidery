from .ReadHelper import signed8


def stc_stitch_encoding_read(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        x = signed8(byte[0])
        y = -signed8(byte[1])
        ctrl = byte[2]

        if ctrl == 0x01:
            out.stitch(x, y)
            continue
        if ctrl == 0x00:
            out.move(x, y)
            continue
        if ctrl == 25:
            break
        else:
            needle = ctrl - 2
            out.needle_change(needle)
    out.end()


def read(f, out, settings=None):
    f.seek(0x28, 1)  # DESIGN: xxxxxx STITCHES: xxxx.
    stc_stitch_encoding_read(f, out)
