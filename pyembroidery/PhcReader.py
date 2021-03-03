from .EmbThreadPec import get_thread_set
from .PecReader import read_pec_graphics, read_pec_stitches
from .ReadHelper import read_int_8, read_int_16le, read_int_32le


def read(f, out, settings=None):
    f.seek(0x4A, 0)
    pec_graphic_icon_height = read_int_8(f)
    f.seek(1, 1)
    pec_graphic_byte_stride = read_int_8(f)
    color_count = read_int_16le(f)
    threadset = get_thread_set()
    for i in range(0, color_count):
        color_index = read_int_8(f)
        if color_index is None:
            return  # File terminated before expected end.
        out.add_thread(threadset[color_index % len(threadset)])
    byte_size = pec_graphic_byte_stride * pec_graphic_icon_height
    read_pec_graphics(
        f, out, byte_size, pec_graphic_byte_stride, color_count, out.threadlist
    )
    f.seek(0x2B, 0)
    pec_add = read_int_8(f)  # Size of pre-graphics, post copyright header.
    f.seek(4, 1)  # 0x30, graphics end size.
    pec_offset = read_int_16le(f)
    f.seek(pec_offset + pec_add, 0)
    bytes_in_section = read_int_16le(f)  # Primary bounds.
    f.seek(bytes_in_section, 1)
    bytes_in_section2 = read_int_32le(f)  # Sectional bounds.
    f.seek(bytes_in_section2 + 10, 1)
    color_count2 = read_int_8(f)
    f.seek(color_count2 + 0x1D, 1)  # 1D toto back
    read_pec_stitches(f, out)
    out.interpolate_duplicate_color_as_stop()
