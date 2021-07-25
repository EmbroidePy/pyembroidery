from .ReadHelper import read_int_32le, signed8


def read_zhs_stitches(f, out):
    count = 0

    xx = 0
    yy = 0
    while True:
        count += 1
        b = bytearray(f.read(3))
        if len(b) != 3:
            break
        ctrl = b[0]
        if ctrl == 0x10:
            # Checksum
            continue
        # x
        x = 0
        x += b[1] & 0b00000001
        x += b[2] & 0b00000010
        x += b[1] & 0b00000100
        x += b[2] & 0b00001000
        x += b[1] & 0b00010000
        x += b[2] & 0b00100000
        x += b[1] & 0b01000000
        x += b[2] & 0b10000000
        if x >= 127:
            x = -256 + x
        if x >= 63:
            x += 1
        if x <= -63:
            x -= 1

        # y
        y = 0
        y += b[2] & 0b00000001
        y += b[1] & 0b00000010
        y += b[2] & 0b00000100
        y += b[1] & 0b00001000
        y += b[2] & 0b00010000
        y += b[1] & 0b00100000
        y += b[2] & 0b01000000
        y += b[1] & 0b10000000

        if y >= 127:
            y = -256 + y
        if y >= 63:
            y += 1
        if y <= -63:
            y -= 1

        xx += x
        yy += y
        if ctrl == 0x41:
            # Still unmapped.
            pass
        elif ctrl == 0x02:
            out.stitch(xx, -yy)
            xx = 0
            yy = 0
            continue
        elif ctrl == 0x01:
            out.move(xx, -yy)
            xx = 0
            yy = 0
            continue
        elif ctrl == 0x04:
            xx = 0
            yy = 0
            out.color_change()
            continue
        elif ctrl == 0x80:
            break
    out.end()


def read(f, out, settings=None):
    f.seek(0x0F, 0)
    stitch_start_position = read_int_32le(f)
    f.seek(stitch_start_position, 0)
    read_zhs_stitches(f, out)
