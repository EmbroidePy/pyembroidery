from .ReadHelper import read_int_32le, signed8


def read_zhs_stitches(f, out):
    count = 0

    while True:
        count += 1
        b = bytearray(f.read(3))
        if len(b) != 3:
            break
        ctrl = b[0]
        if ctrl == 0x10:
            continue
        i = (b[1] << 8) + b[2]
        x = 0
        x |= (i & 0b00000001_00000000) >> 8
        x |= (i & 0b00000000_00000010) >> 0
        x |= (i & 0b00000100_00000000) >> 8
        x |= (i & 0b00000000_00001000) >> 0
        x |= (i & 0b00010000_00000000) >> 8
        x |= (i & 0b00000000_00100000) >> 0
        x |= (i & 0b01000000_00000000) >> 8
        x |= (i & 0b00000000_10000000) >> 0
        if x >= 127:
            x = -256 + x
        if x >= 63:
            x += 1
        if x <= -63:
            x -= 1
        y = 0
        y |= (i & 0b00000000_00000001) >> 0
        y |= (i & 0b00000010_00000000) >> 8
        y |= (i & 0b00000000_00000100) >> 0
        y |= (i & 0b00001000_00000000) >> 8
        y |= (i & 0b00000000_00010000) >> 0
        y |= (i & 0b00100000_00000000) >> 8
        y |= (i & 0b00000000_01000000) >> 0
        y |= (i & 0b10000000_00000000) >> 8

        if y >= 127:
            y = -256 + y
        if y >= 63:
            y += 1
        if y <= -63:
            y -= 1
        if ctrl == 0x02:
            out.stitch(x, -y)
            continue
        if ctrl == 0x01:
            out.move(x,-y)
            continue
        if ctrl == 0x04:
            out.color_change()
            continue
        if ctrl == 0x80:
            break
    out.end()


def read(f, out, settings=None):
    f.seek(0x0F, 0)
    stitch_start_position = read_int_32le(f)
    f.seek(stitch_start_position, 0)
    read_zhs_stitches(f, out)
