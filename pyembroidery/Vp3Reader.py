from .EmbThread import EmbThread
from .ReadHelper import read_int_16be, read_int_8, read_int_32be, read_int_24be, read_signed, read_string_8, \
    read_string_16


def read_vp3_string_16(stream):
    # Reads the header strings which are 16le numbers of size followed by
    # utf-16 text
    string_length = read_int_16be(stream)
    return read_string_16(stream, string_length)


def read_vp3_string_8(stream):
    # Reads the body strings which are 16be numbers followed by utf-8 text
    string_length = read_int_16be(stream)
    return read_string_8(stream, string_length)


def skip_vp3_string(stream):
    string_length = read_int_16be(stream)
    stream.seek(string_length, 1)


def signed32(b):
    b &= 0xFFFFFFFF
    if b > 0x7FFFFFFF:
        return - 0x100000000 + b
    else:
        return b


def signed16(b0, b1):
    b0 &= 0xFF
    b1 &= 0xFF
    b = (b0 << 8) | b1
    if b > 0x7FFF:
        return - 0x10000 + b
    else:
        return b


def read(f, out, settings=None):
    b = f.read(6)
    # magic code: %vsm%\0
    skip_vp3_string(f)  # "Produced by     Software Ltd"
    f.seek(7, 1)
    skip_vp3_string(f)  # "" comments and note string.
    f.seek(32, 1)
    center_x = (signed32(read_int_32be(f)) / 100)
    center_y = -(signed32(read_int_32be(f)) / 100)
    f.seek(27, 1)
    skip_vp3_string(f)  # ""
    f.seek(24, 1)
    skip_vp3_string(f)  # "Produced by     Software Ltd"
    count_colors = read_int_16be(f)
    for i in range(0, count_colors):
        vp3_read_colorblock(f, out, center_x, center_y)
        if (i + 1) < count_colors:  # Don't add the color change on the final read.
            out.color_change()
    out.end()


def vp3_read_colorblock(f, out, center_x, center_y):
    bytescheck = f.read(3)  # \x00\x05\x00
    distance_to_next_block_050 = read_int_32be(f)
    block_end_position = distance_to_next_block_050 + f.tell()

    start_position_x = (signed32(read_int_32be(f)) / 100)
    start_position_y = -(signed32(read_int_32be(f)) / 100)
    abs_x = start_position_x + center_x
    abs_y = start_position_y + center_y
    if abs_x != 0 and abs_y != 0:
        out.move_abs(abs_x, abs_y)
    thread = vp3_read_thread(f)
    out.add_thread(thread)
    f.seek(15, 1)
    bytescheck = f.read(3)  # \x0A\xF6\x00
    stitch_byte_length = block_end_position - f.tell()
    stitch_bytes = read_signed(f, stitch_byte_length)
    i = 0
    while i < len(stitch_bytes) - 1:
        x = stitch_bytes[i]
        y = stitch_bytes[i + 1]
        i += 2
        if (x & 0xFF) != 0x80:
            out.stitch(x, y)
            continue
        if y == 0x01:
            x = signed16(stitch_bytes[i], stitch_bytes[i + 1])
            i += 2
            y = signed16(stitch_bytes[i], stitch_bytes[i + 1])
            i += 2
            out.stitch(x, y)
            i += 2
            # Final element is typically 0x80 0x02, this is skipped regardless of its value.
        elif y == 0x02:
            # This is only seen after 80 01 and should have been skipped. Has no known effect.
            pass
        elif y == 0x03:
            out.trim()


def vp3_read_thread(f):
    thread = EmbThread()
    colors = read_int_8(f)
    transition = read_int_8(f)
    for m in range(0, colors):
        thread.color = read_int_24be(f)
        parts = read_int_8(f)
        color_length = read_int_16be(f)
    thread_type = read_int_8(f)
    weight = read_int_8(f)
    thread.catalog_number = read_vp3_string_8(f)
    thread.description = read_vp3_string_8(f)
    thread.brand = read_vp3_string_8(f)
    return thread
