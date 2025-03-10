from .WriteHelper import write_int_8, write_int_16be, write_int_32be, write_string_utf8

ENCODE = False


def patch_byte_offset(stream, offset):
    current_pos = stream.tell()
    stream.seek(offset, 0)  # Absolute position seek.
    position = current_pos - offset - 4  # 4 bytes int32
    write_int_32be(stream, position)
    stream.seek(current_pos, 0)  # Absolute position seek.


def write(pattern, f, settings=None):
    write_int_32be(f, 1)
    write_int_32be(f, 8)
    placeholder = f.tell()
    write_int_32be(f, 0)  # Placeholder.
    write_int_32be(f, len(pattern.threadlist))
    index = 0
    for thread in pattern.threadlist:
        details = thread.description
        if details is None:
            details = "Unknown"
        chart = thread.chart
        if chart is None:
            chart = "Unknown"
        write_int_16be(
            f, 11 + len(details) + len(chart)
        )  # 2 + 2 + 1 + 1 + 1 + 2 + d + 1 + c + 1 = 11 + d + c
        write_int_16be(f, index)  # record index
        index += 1
        write_int_8(f, thread.get_red())
        write_int_8(f, thread.get_green())
        write_int_8(f, thread.get_blue())
        write_int_16be(f, index)  # needle number
        write_string_utf8(f, details)
        write_int_8(f, 0)
        write_string_utf8(f, chart)
        write_int_8(f, 0)
    patch_byte_offset(f, placeholder)
