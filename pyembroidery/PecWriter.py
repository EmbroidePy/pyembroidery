from .EmbThread import build_unique_palette
from .EmbConstant import *
from .EmbThreadPec import get_thread_set
from .PecGraphics import get_blank, draw_scaled
from .WriteHelper import write_int_8, write_int_16le, write_int_16be, \
    write_int_24le, write_string_utf8

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_JUMP
FULL_JUMP = True
ROUND = True
MAX_JUMP_DISTANCE = 2047
MAX_STITCH_DISTANCE = 2047

MASK_07_BIT = 0b01111111
JUMP_CODE = 0b00010000
TRIM_CODE = 0b00100000
FLAG_LONG = 0b10000000
PEC_ICON_WIDTH = 48
PEC_ICON_HEIGHT = 38


def write(pattern, f, settings=None):
    pattern.fix_color_count()
    pattern.interpolate_stop_as_duplicate_color()
    f.write(bytes("#PEC0001".encode('utf8')))
    write_pec(pattern, f)


def write_pec(pattern, f, threadlist=None):
    extends = pattern.bounds()
    if threadlist is None:
        pattern.fix_color_count()
        threadlist = pattern.threadlist
    color_info = write_pec_header(pattern, f, threadlist)
    write_pec_block(pattern, f, extends)
    write_pec_graphics(pattern, f, extends)
    return color_info


def write_pec_header(pattern, f, threadlist):
    name = pattern.get_metadata("name", "Untitled")
    write_string_utf8(f, "LA:%-16s\r" % name[:8])
    f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\xFF\x00')
    write_int_8(f, int(PEC_ICON_WIDTH / 8))  # PEC BYTE STRIDE
    write_int_8(f, int(PEC_ICON_HEIGHT))  # PEC ICON HEIGHT

    thread_set = get_thread_set()

    color_index_list = build_unique_palette(thread_set, pattern.threadlist)

    rgb_list = [thread.color for thread in threadlist]

    current_thread_count = len(color_index_list)
    if current_thread_count is not 0:
        f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20')
        add_value = current_thread_count - 1
        color_index_list.insert(0, add_value)
        f.write(bytes(bytearray(color_index_list)))
    else:
        f.write(b'\x20\x20\x20\x20\x64\x20\x00\x20\x00\x20\x20\x20\xFF')

    for i in range(current_thread_count, 463):
        f.write(b'\x20')  # 520
    return color_index_list, rgb_list


def write_pec_block(pattern, f, extends):
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    stitch_block_start_position = f.tell()
    f.write(b'\x00\x00')
    write_int_24le(f, 0)  # Space holder.
    f.write(b'\x31\xff\xf0')
    write_int_16le(f, int(round(width)))
    write_int_16le(f, int(round(height)))
    write_int_16le(f, 0x1E0)
    write_int_16le(f, 0x1B0)

    write_int_16be(f, 0x9000 | -int(round(extends[0])))
    write_int_16be(f, 0x9000 | -int(round(extends[1])))

    pec_encode(pattern, f)

    stitch_block_length = f.tell() - stitch_block_start_position

    current_position = f.tell()
    f.seek(stitch_block_start_position + 2, 0)
    write_int_24le(f, stitch_block_length)
    f.seek(current_position, 0)


def write_pec_graphics(pattern, f, extends):
    blank = get_blank()
    for block in pattern.get_as_stitchblock():
        stitches = block[0]
        draw_scaled(extends, stitches, blank, 6, 4)
    f.write(bytes(bytearray(blank)))

    for block in pattern.get_as_colorblocks():
        stitches = [s for s in block[0] if s[2] == STITCH]
        blank = get_blank()  # [ 0 ] * 6 * 38
        draw_scaled(extends, stitches, blank, 6)
        f.write(bytes(bytearray(blank)))


def encode_long_form(value):
    value &= 0b0000111111111111
    value |= 0b1000000000000000
    return value


def flag_jump(long_form):
    return long_form | (JUMP_CODE << 8)


def flag_trim(long_form):
    return long_form | (TRIM_CODE << 8)


def pec_encode(pattern, f):
    color_two = True
    jumping = False
    stitches = pattern.stitches
    xx = 0
    yy = 0
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2] & COMMAND_MASK
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if data == STITCH:
            if jumping and dx != 0 and dy != 0:
                f.write(b'\x00\x00')
                jumping = False
            if -64 < dx < 63 and -64 < dy < 63:
                f.write(bytes(bytearray([dx & MASK_07_BIT, dy & MASK_07_BIT])))
            else:
                dx = encode_long_form(dx)
                dy = encode_long_form(dy)
                data = [
                    (dx >> 8) & 0xFF,
                    dx & 0xFF,
                    (dy >> 8) & 0xFF,
                    dy & 0xFF]
                f.write(bytes(bytearray(data)))
            continue
        elif data == JUMP:
            jumping = True
            dx = encode_long_form(dx)
            dx = flag_trim(dx)
            dy = encode_long_form(dy)
            dy = flag_trim(dy)
            f.write(bytes(bytearray([
                (dx >> 8) & 0xFF,
                dx & 0xFF,
                (dy >> 8) & 0xFF,
                dy & 0xFF
            ])))
            continue
        elif data == COLOR_CHANGE:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xfe\xb0')
            if color_two:
                f.write(b'\x02')
            else:
                f.write(b'\x01')
            color_two = not color_two
            continue
        elif data == STOP:
            continue  # These will already be processed into duplicate colors.
        elif data == TRIM:
            continue
        elif data == END:
            f.write(b'\xff')
            break
