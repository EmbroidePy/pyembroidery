def read_inb_stitches(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        x = byte[0]
        y = -byte[1]
        ctrl = byte[2]
        if ctrl & 0x20 != 0:
            y = -y
        if ctrl & 0x40 != 0:
            x = -x
        if (ctrl & 0b1111) == 0x00:
            out.stitch(x, y)
            continue
        if (ctrl & 0b1111) == 0x01:
            out.color_change(x, y)
            continue
        if (ctrl & 0b1111) == 0x02:
            out.move(x, y)
            continue
        if ctrl == 0x04:
            break
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    f.seek(0x2000, 0)
    read_inb_stitches(f, out)
