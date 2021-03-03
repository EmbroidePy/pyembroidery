from .EmbCompress import expand
from .EmbThreadHus import get_thread_set
from .ReadHelper import read_int_16le, read_int_32le, read_string_8, signed8, signed16


def read(f, out, settings=None):
    magic_code = read_int_32le(f)
    number_of_stitches = read_int_32le(f)
    number_of_colors = read_int_32le(f)

    extend_pos_x = signed16(read_int_16le(f))
    extend_pos_y = signed16(read_int_16le(f))
    extend_neg_x = signed16(read_int_16le(f))
    extend_neg_y = signed16(read_int_16le(f))

    command_offset = read_int_32le(f)
    x_offset = read_int_32le(f)
    y_offset = read_int_32le(f)

    string_value = read_string_8(f, 8)

    unknown_16_bit = read_int_16le(f)

    hus_thread_set = get_thread_set()
    for i in range(0, number_of_colors):
        index = read_int_16le(f)
        out.add_thread(hus_thread_set[index])
    f.seek(command_offset, 0)
    command_compressed = bytearray(f.read(x_offset - command_offset))
    f.seek(x_offset, 0)
    x_compressed = bytearray(f.read(y_offset - x_offset))
    f.seek(y_offset, 0)
    y_compressed = bytearray(f.read())

    command_decompressed = expand(command_compressed, number_of_stitches)
    x_decompressed = expand(x_compressed, number_of_stitches)
    y_decompressed = expand(y_compressed, number_of_stitches)

    stitch_count = min(
        len(command_decompressed), len(x_decompressed), len(y_decompressed)
    )

    for i in range(0, stitch_count):
        cmd = command_decompressed[i]
        x = signed8(x_decompressed[i])
        y = -signed8(y_decompressed[i])
        if cmd == 0x80:  # STITCH
            out.stitch(x, y)
        elif cmd == 0x81:  # JUMP
            out.move(x, y)
        elif cmd == 0x84:  # COLOR_CHANGE
            out.color_change(x, y)
        elif cmd == 0x88:  # TRIM
            if x != 0 or y != 0:
                out.move(x, y)
            out.trim()
        elif cmd == 0x90:  # END
            break
        else:  # UNMAPPED COMMAND
            break
    out.end()
