def new_stitch_encoding_read(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        x = byte[0]
        y = -byte[1]
        ctrl = byte[2]

        if ctrl & 0b01000000 != 0:
            x = -x
        if ctrl & 0b00100000 != 0:
            y = -y
        ctrl &= ~0b11100000
        if ctrl == 0:
            out.stitch(x, y)
            continue
        if ctrl == 0b00010001:
            break
        if ctrl & 0b00000010 != 0:
            out.color_change()
            continue
        if ctrl & 0b00000001 != 0:
            out.move(x, y)
            continue
    out.end()


def read(f, out, settings=None):
    f.seek(2, 1)  # stitchcount.
    new_stitch_encoding_read(f, out)
