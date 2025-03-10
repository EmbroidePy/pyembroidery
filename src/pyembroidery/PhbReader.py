from .EmbThreadPec import get_thread_set
from .PecReader import read_pec_stitches
from .ReadHelper import read_int_8, read_int_16le, read_int_32le


def read(f, out, settings=None):
    # should start #PHB0003
    f.seek(0x71, 0)
    color_count = read_int_16le(f)
    threadset = get_thread_set()
    for i in range(0, color_count):
        out.add_thread(threadset[read_int_8(f) % len(threadset)])

    file_offset = 0x52

    f.seek(0x54, 0)
    file_offset += read_int_32le(f)

    f.seek(file_offset, 0)
    file_offset += read_int_32le(f) + 2

    f.seek(file_offset, 0)
    file_offset += read_int_32le(f)

    f.seek(file_offset + 14, 0)

    color_count2 = read_int_8(f)
    # 10 bytes unknown, PEC extends.
    f.seek(color_count2 + 0x15, 1)

    read_pec_stitches(f, out)
    out.interpolate_duplicate_color_as_stop()
