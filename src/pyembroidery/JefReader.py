from .EmbThreadJef import get_thread_set
from .ReadHelper import read_int_32le, signed8


def read_jef_stitches(f, out, settings=None):
    color_index = 1
    while True:
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
            # PATCH: None means stop since it was color #0
            if out.threadlist[color_index] is None:
                out.stop(0, 0)
                del out.threadlist[color_index]
            else:
                out.color_change(0, 0)
                color_index += 1
            continue
        if ctrl == 0x10:
            break
        break  # Uncaught Control
    out.end(0, 0)

    clipping = True
    trims = False
    count_max = None
    trim_distance = 3.0
    if settings is not None:
        count_max = settings.get("trim_at", count_max)
        trims = settings.get("trims", trims)
        trim_distance = settings.get("trim_distance", trim_distance)
        clipping = settings.get("clipping", clipping)
    if trims and count_max is None:
        count_max = 3
    if trim_distance is not None:
        trim_distance *= 10  # Pixels per mm. Native units are 1/10 mm.
    out.interpolate_trims(count_max, trim_distance, clipping)


def read(f, out, settings=None):
    jef_threads = get_thread_set()
    stitch_offset = read_int_32le(f)
    f.seek(20, 1)
    count_colors = read_int_32le(f)
    f.seek(88, 1)

    for i in range(0, count_colors):
        index = abs(read_int_32le(f))
        if index == 0:
            # Patch: If we have color 0. Go ahead and set that to None.
            out.threadlist.append(None)
        else:
            out.add_thread(jef_threads[index % len(jef_threads)])

    f.seek(stitch_offset, 0)
    read_jef_stitches(f, out, settings)
