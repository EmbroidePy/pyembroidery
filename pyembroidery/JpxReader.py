from .ReadHelper import signed8, read_int_32le


def read_jpx_stitches(f, out):
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
        if ctrl == 0x01:  # Colorchange
            out.color_change()
            if x != 0 and y != 0:
                out.move(x, y)
            continue
        if ctrl == 0x10:
            break
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    stitch_start_position = read_int_32le(f)
    f.seek(0x1C, 1)
    colors = read_int_32le(f)
    f.seek(0x18, 1)
    for i in range(0, colors):
        color_index = read_int_32le(f)
        if color_index is None:
            break
        out.add_thread({
            "color": "random",
            "name": "JPX index " + str(color_index)
        })
    f.seek(stitch_start_position, 0)
    read_jpx_stitches(f, out)
