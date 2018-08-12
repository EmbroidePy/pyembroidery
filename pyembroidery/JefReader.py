from .EmbThreadJef import get_thread_set
from .ReadHelper import read_int_32le, signed8


def read_jef_stitches(f, out):
    count = 0
    while True:
        count += 1
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] != 0x80:
            x = signed8(b[0])
            y = -signed8(b[1])
            out.stitch(x, y)
            continue
        ctrl = b[1]
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        x = signed8(b[0])
        y = -signed8(b[1])
        if ctrl == 0x02:
            out.move(x, y)
            continue
        if ctrl == 0x01:
            out.color_change(0, 0)
            continue
        if ctrl == 0x10:
            break
        break  # Uncaught Control
    out.end(0, 0)


def read(f, out, settings=None):
    jef_threads = get_thread_set()
    stitch_offset = read_int_32le(f)
    f.seek(20, 1)
    count_colors = read_int_32le(f)
    f.seek(88, 1)

    for i in range(0, count_colors):
        index = abs(read_int_32le(f))
        out.add_thread(jef_threads[index % len(jef_threads)])

    f.seek(stitch_offset, 0)
    read_jef_stitches(f, out)
