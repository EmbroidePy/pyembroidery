from .DstReader import dst_read_header


def z_stitch_encoding_read(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        y = -byte[0]
        x = byte[1]
        ctrl = byte[2]

        if ctrl & 0x40 != 0:
            x = -x
        if ctrl & 0x20 != 0:
            y = -y

        if (ctrl & 0b11111) == 0:
            out.stitch(x, y)
            continue
        if (ctrl & 0b11111) == 1:
            out.move(x, y)
            continue
        if ctrl == 0x82:
            out.stop()
            continue
        if ctrl == 0x9B:
            out.trim()
            continue
        if 0x83 <= ctrl <= 0x9A:
            needle = (ctrl - 0x83) >> 1
            out.needle_change(needle)
            continue
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    dst_read_header(f, out)
    z_stitch_encoding_read(f, out)
