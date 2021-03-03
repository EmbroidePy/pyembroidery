from .EmbThreadSew import get_thread_set
from .ReadHelper import read_int_16le, signed8


def read_sew_stitches(f, out):
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] != 0x80:
            out.stitch(signed8(b[0]), -signed8(b[1]))
            continue
        control = b[1]
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if control & 1:
            out.color_change()
            continue
        if control == 0x04 or control == 0x02:
            out.move(signed8(b[0]), -signed8(b[1]))
            continue
        if control == 0x10:
            out.stitch(signed8(b[0]), -signed8(b[1]))
            continue
        break
    out.end()


def read(f, out, settings=None):
    threads = get_thread_set()
    colors = read_int_16le(f)
    for c in range(0, colors):
        index = read_int_16le(f)
        index %= len(threads)
        out.add_thread(threads[index])

    f.seek(0x1D78, 0)
    read_sew_stitches(f, out)
