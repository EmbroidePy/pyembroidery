from .DstReader import dst_read_header


def b_stitch_encoding_read(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        ctrl = byte[0]
        y = -byte[1]
        x = byte[2]

        if ctrl & 0x40 != 0:
            y = -y
        if ctrl & 0x20 != 0:
            x = -x

        if (ctrl & 0b11111) == 0:
            out.stitch(x, y)
            continue
        if (ctrl & 0b11111) == 1:
            out.move(x, y)
            continue
        if ctrl == 0xF8:
            break
        if ctrl == 0xE7:
            out.trim()
            continue
        if ctrl == 0xE8:
            out.stop()
            continue
        if 0xE9 <= ctrl < 0xF8:
            needle = ctrl - 0xE8
            out.needle_change(needle)
            continue
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    dst_read_header(f, out)
    b_stitch_encoding_read(f, out)
