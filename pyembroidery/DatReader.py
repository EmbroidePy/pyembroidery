from .EmbConstant import FAST, SLOW


def read_barudan_dat(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        ctrl = byte[0]
        dy = -byte[1]
        dx = byte[2]
        if ctrl & 0x80 == 0:
            # This bit should always be set, must be other dat type.
            return False
        if (ctrl & 0x20) != 0:
            dx = -dx
        if (ctrl & 0x40) != 0:
            dy = -dy
        command = ctrl & 0b11111
        if command == 0x0:
            # Stitch
            out.stitch(dx, dy)
            continue
        if command == 0x01:
            # Jump
            out.move(dx, dy)
            continue
        if command == 0x02:
            # Fast
            out.add_stitch_relative(FAST)
            if dx != 0 or dy != 0:
                out.stitch(dx, dy)
            continue
        if command == 0x03:
            # Fast, Jump
            out.add_stitch_relative(FAST)
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x04:
            # Slow
            out.add_stitch_relative(SLOW)
            if dx != 0 or dy != 0:
                out.stitch(dx, dy)
            continue
        if command == 0x05:
            # Slow, Jump
            out.add_stitch_relative(SLOW)
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x06:
            # T1 Top Thread Trimming, TTrim.
            out.trim()
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x07:
            # T2 Bobbin Threading
            out.trim()
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if (
            command == 0x08
        ):  # ww, stop file had proper A8 rather than E8 and displacement
            # C00 Stop
            out.stop()
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if 0x09 <= command <= 0x17:
            # C01 - C14
            needle = command - 0x08
            out.needle_out(needle)
            if dx != 0 or dy != 0:
                out.move(dx, dy)
            continue
        if command == 0x18:
            break
        if ctrl == 0x2B:
            break  # Rare postfix data from machine. Do not read this.
        break  # Uncaught Command
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
