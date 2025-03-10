from .ReadHelper import read_int_8, read_int_16be, read_int_24be, signed24

PC_SIZE_CONVERSION_RATIO = 5.0 / 3.0


def read_pc_file(f, out, settings=None):
    pcm_threads = [
        {"color": 0x000000, "description": "PCM Color 1"},
        {"color": 0x000080, "description": "PCM Color 2"},
        {"color": 0x0000FF, "description": "PCM Color 3"},
        {"color": 0x008080, "description": "PCM Color 4"},
        {"color": 0x00FFFF, "description": "PCM Color 5"},
        {"color": 0x800080, "description": "PCM Color 6"},
        {"color": 0xFF00FF, "description": "PCM Color 7"},
        {"color": 0x800000, "description": "PCM Color 8"},
        {"color": 0xFF0000, "description": "PCM Color 9"},
        {"color": 0x008000, "description": "PCM Color 10"},
        {"color": 0x00FF00, "description": "PCM Color 11"},
        {"color": 0x808000, "description": "PCM Color 12"},
        {"color": 0xFFFF00, "description": "PCM Color 13"},
        {"color": 0x808080, "description": "PCM Color 14"},
        {"color": 0xC0C0C0, "description": "PCM Color 15"},
        {"color": 0xFFFFFF, "description": "PCM Color 16"},
    ]

    f.seek(2, 0)

    colors = read_int_16be(f)
    if colors is None:
        return  # File is blank.
    for i in range(0, colors):
        color_index = read_int_16be(f)
        thread = pcm_threads[color_index]
        out.add_thread(thread)

    stitch_count = read_int_16be(f)
    while True:
        x = read_int_24be(f)
        c0 = read_int_8(f)
        y = read_int_24be(f)
        c1 = read_int_8(f)
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
