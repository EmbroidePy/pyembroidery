from .EmbThread import EmbThread
from .ReadHelper import (
    read_int_8,
    read_int_16le,
    read_int_24be,
    read_int_24le,
    signed24,
)

PC_SIZE_CONVERSION_RATIO = 5.0 / 3.0


def read_pc_file(f, out, settings=None):
    version = read_int_8(f)
    hoop_size = read_int_8(f)
    # 0 for PCD,
    # 1 for PCQ (MAXI),
    # 2 for PCS small hoop(80x80),
    # 3 for PCS with large hoop.
    color_count = read_int_16le(f)
    for i in range(0, color_count):
        thread = EmbThread()
        thread.color = read_int_24be(f)
        out.add_thread(thread)
        f.seek(1, 1)

    stitch_count = read_int_16le(f)
    while True:
        c0 = read_int_8(f)
        x = read_int_24le(f)
        c1 = read_int_8(f)
        y = read_int_24le(f)
        ctrl = read_int_8(f)
        if ctrl is None:
            break
        x = signed24(x)
        y = -signed24(y)
        x *= PC_SIZE_CONVERSION_RATIO
        y *= PC_SIZE_CONVERSION_RATIO
        if ctrl == 0x00:
            out.stitch_abs(x, y)
            continue
        if ctrl & 0x01:
            out.color_change()
            continue
        if ctrl & 0x04:
            out.move_abs(x, y)
            continue
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    read_pc_file(f, out)
