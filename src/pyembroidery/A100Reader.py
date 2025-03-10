def read_100_stitches(f, out):
    count = 0
    while True:
        count += 1
        b = bytearray(f.read(4))
        if len(b) != 4:
            break
        x = b[2]
        y = b[3]
        if x > 0x80:
            x -= 0x80
            x = -x
        if y > 0x80:  # because 2s complement is for chumps?
            y -= 0x80
            y = -y
        if b[0] == 0x61:
            out.stitch(x, -y)
            continue
        elif (b[0] & 0x01) != 0:
            out.move(x, -y)
            continue
        else:  # too broad of catch
            out.color_change()
            continue
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    read_100_stitches(f, out)
