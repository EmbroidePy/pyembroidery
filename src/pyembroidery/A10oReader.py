def read_10o_sttiches(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        ctrl = byte[0]
        y = -byte[1]
        x = byte[2]
        if ctrl & 0x20 != 0:
            x = -x
        if ctrl & 0x40 != 0:
            y = -y

        if (ctrl & 0b11111) == 0:
            out.stitch(x, y)
            continue
        if (ctrl & 0b11111) == 0x10:
            out.move(x, y)
            continue
        if ctrl == 0x8A:
            # Start.
            continue
        if ctrl == 0x85:
            out.color_change()
            continue
        if ctrl == 0x82:
            out.stop()
            continue
        if ctrl == 0x81:
            out.trim()
            continue
        if ctrl == 0x87:
            break
        break  # Unknown Control
    out.end()


def read(f, out, settings=None):
    read_10o_sttiches(f, out)
