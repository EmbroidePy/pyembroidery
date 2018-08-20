def read_barudan_dat(f, out):
    stitched_yet = False
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        ctrl = byte[0]
        y = -byte[1]
        x = byte[2]

        if ctrl & 0x80 == 0:
            # This bit should always be set, must be other dat type.
            return False
        if ctrl & 0x40 != 0:
            y = -y
        if ctrl & 0x20 != 0:
            x = -x
        if (ctrl & 0b11111) == 0:
            stitched_yet = True
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
            if count > 1:
                out.stop()
            continue
        if 0xE9 <= ctrl < 0xF8:
            needle = ctrl - 0xE8
            if stitched_yet:
                out.color_change()
            continue
        break  # Uncaught Control
    out.end()
    return True


def read_sunstar_dat_stitches(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        x = byte[0] & 0x7F
        y = byte[1] & 0x7F
        if byte[0] & 0x80:
            x = -x
        if byte[1] & 0x80:
            y = -y
        y = -y
        ctrl = byte[2]
        if ctrl == 0x07:
            out.stitch(x, y)
            continue
        if ctrl == 0x04:
            out.move(x, y)
            continue
        if ctrl == 0x80:
            out.trim()
            if x != 0 or y != 0:
                out.move(x, y)
            continue
        if ctrl == 0x87:
            out.color_change()
            if x != 0 or y != 0:
                out.move(x, y)
            continue
        if ctrl == 0x84:  # Initialized info.
            out.stitch(x, y)
            continue
        elif ctrl == 0:
            break
        break  # Uncaught Control
    out.end()


def read_sunstar_dat(f, out):
    # f.seek(0x02, 0)
    # stitches = read_int_16le(f)
    f.seek(0x100, 0)
    read_sunstar_dat_stitches(f, out)


def read(f, out, settings=None):
    if not read_barudan_dat(f, out):
        f.seek(0, 0)
        read_sunstar_dat(f, out)
