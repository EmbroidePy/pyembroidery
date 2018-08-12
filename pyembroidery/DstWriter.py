from .EmbConstant import *
from .WriteHelper import write_string_utf8

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_UTILIZE
FULL_JUMP = False
MAX_JUMP_DISTANCE = 121
MAX_STITCH_DISTANCE = 121
PPMM = 10
DSTHEADERSIZE = 512


def bit(b):
    return 1 << b


def encode_record(x, y, flags):
    y = -y  # flips the coordinate y space.
    b0 = 0
    b1 = 0
    b2 = 0
    if flags == JUMP or flags == SEQUIN_EJECT:
        b2 += bit(7)  # jumpstitch 10xxxx11
    if flags == STITCH or flags == JUMP or flags == SEQUIN_EJECT:
        b2 += bit(0)
        b2 += bit(1)
        if x > 40:
            b2 += bit(2)
            x -= 81
        if x < -40:
            b2 += bit(3)
            x += 81
        if x > 13:
            b1 += bit(2)
            x -= 27
        if x < -13:
            b1 += bit(3)
            x += 27
        if x > 4:
            b0 += bit(2)
            x -= 9
        if x < -4:
            b0 += bit(3)
            x += 9
        if x > 1:
            b1 += bit(0)
            x -= 3
        if x < -1:
            b1 += bit(1)
            x += 3
        if x > 0:
            b0 += bit(0)
            x -= 1
        if x < 0:
            b0 += bit(1)
            x += 1
        if x != 0:
            raise ValueError("The dx value given to the writer exceeds maximum allowed.")
        if y > 40:
            b2 += bit(5)
            y -= 81
        if y < -40:
            b2 += bit(4)
            y += 81
        if y > 13:
            b1 += bit(5)
            y -= 27
        if y < -13:
            b1 += bit(4)
            y += 27
        if y > 4:
            b0 += bit(5)
            y -= 9
        if y < -4:
            b0 += bit(4)
            y += 9
        if y > 1:
            b1 += bit(7)
            y -= 3
        if y < -1:
            b1 += bit(6)
            y += 3
        if y > 0:
            b0 += bit(7)
            y -= 1
        if y < 0:
            b0 += bit(6)
            y += 1
        if y != 0:
            raise ValueError("The dy value given to the writer exceeds maximum allowed.")
    elif flags is COLOR_CHANGE:
        b2 = 0b11000011
    elif flags is STOP:
        b2 = 0b11000011
    elif flags is END:
        b2 = 0b11110011
    elif flags is SEQUIN_MODE:
        b2 = 0b01000011
    return bytes(bytearray([b0, b1, b2]))


def write(pattern, f, settings=None):
    extended_header = False
    if settings is not None:
        extended_header = settings.get("extended header", extended_header)

    extends = pattern.extends()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    name = pattern.get_metadata("name", "Untitled")

    write_string_utf8(f, "LA:%-16s\r" % name)
    write_string_utf8(f, "ST:%7d\r" % pattern.count_stitches())
    write_string_utf8(f, "CO:%3d\r" % pattern.count_color_changes())
    x_extend = int(round(PPMM * width / 2))
    y_extend = int(round(PPMM * height / 2))
    write_string_utf8(f, "+X:%5d\r" % x_extend)
    write_string_utf8(f, "-X:%5d\r" % x_extend)
    write_string_utf8(f, "+Y:%5d\r" % y_extend)
    write_string_utf8(f, "-Y:%5d\r" % y_extend)
    write_string_utf8(f, "AX:+%5d\r" % 0)
    write_string_utf8(f, "AY:+%5d\r" % 0)
    write_string_utf8(f, "MX:+%5d\r" % 0)
    write_string_utf8(f, "AY:+%5d\r" % 0)
    write_string_utf8(f, "PD:%6s\r" % "******")
    if extended_header:
        author = pattern.get_metadata("author")
        if author is not None:
            write_string_utf8(f, "AU:%s\r" % author)
        meta_copyright = pattern.get_metadata("copyright")
        if meta_copyright is not None:
            write_string_utf8(f, "CP:%s\r" % meta_copyright)
        if len(pattern.threadlist) > 0:
            for thread in pattern.threadlist:
                write_string_utf8(f, "TC:%s,%s,%s\r" %
                                  (thread.hex_color(),
                                   thread.description,
                                   thread.catalog_number))
    f.write(b'\x1a')
    for i in range(f.tell(), DSTHEADERSIZE):
        f.write(b'\x20')  # space

    stitches = pattern.stitches
    xx = 0
    yy = 0
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if data == TRIM:
            f.write(encode_record(2, 2, JUMP))
            f.write(encode_record(-4, -4, JUMP))
            f.write(encode_record(2, 2, JUMP))
        else:
            f.write(encode_record(dx, dy, data))
