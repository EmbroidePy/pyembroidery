from .EmbThreadJef import get_thread_set
from .ReadHelper import read_int_32le, signed8


def read_jef_stitches(f, out, settings=None):
    clipping = True
    trims = False
    command_count_max = 3
    trim_distance = 3.0
    if settings is not None:
        command_count_max = settings.get('trim_at', command_count_max)
        trims = settings.get("trims", trims)
        trim_distance = settings.get("trim_distance", trim_distance)
        clipping = settings.get('clipping', clipping)
    if trim_distance is not None:
        trim_distance *= 10 # Pixels per mm. Native units are 1/10 mm.
    jump_count = 0
    jump_start = 0
    jump_dx = 0
    jump_dy = 0
    jumping = False
    trimmed = True
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] != 0x80:
            x = signed8(b[0])
            y = -signed8(b[1])
            out.stitch(x, y)
            trimmed = False
            jumping = False
            continue
        ctrl = b[1]
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        x = signed8(b[0])
        y = -signed8(b[1])
        if ctrl == 0x02:
            out.move(x, y)
            if not jumping:
                jump_dx = 0
                jump_dy = 0
                jump_count = 0
                jump_start = len(out.stitches) - 1
                jumping = True
            jump_count += 1
            jump_dx += x
            jump_dy += y
            if not trimmed and\
                    (
                        (
                            trims
                            and
                            jump_count == command_count_max
                        )
                        or
                        (
                            trim_distance is not None
                            and
                            (
                                abs(jump_dy) > trim_distance or abs(jump_dx) > trim_distance
                            )
                        )
                    ):
                out.trim(position=jump_start)
                jump_start += 1  # We inserted a position, start jump has moved.
                trimmed = True
            if clipping and jump_dx == 0 and jump_dy == 0:  # jump displacement is 0, clip trim command.
                out.stitches = out.stitches[:jump_start]
            continue
        if ctrl == 0x01:
            out.color_change(0, 0)
            trimmed = True
            jumping = False
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
    read_jef_stitches(f, out, settings)
