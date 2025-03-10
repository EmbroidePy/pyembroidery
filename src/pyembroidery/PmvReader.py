from .ReadHelper import read_int_8, read_int_16le


def find_extends(stitches):
    min_x = float("inf")
    min_y = float("inf")
    max_x = -float("inf")
    max_y = -float("inf")

    for stitch in stitches:
        if stitch[0] > max_x:
            max_x = stitch[0]
        if stitch[0] < min_x:
            min_x = stitch[0]
        if stitch[1] > max_y:
            max_y = stitch[1]
        if stitch[1] < min_y:
            min_y = stitch[1]
    return min_x, min_y, max_x, max_y


def read_pmv_stitches(f, out, settings=None):
    """PMV files are stitch files, not embroidery."""
    px = 0
    # stitches = []
    while True:
        stitch_count = read_int_16le(f)
        block_length = read_int_16le(f)
        if block_length is None:
            return
        if block_length >= 256:
            break
        if stitch_count == 0:
            continue
        for i in range(0, stitch_count):
            x = read_int_8(f)
            y = read_int_8(f)
            if y > 16:
                y = -(32 - y)  # This is 5 bit signed number.
            if x > 32:
                x = -(64 - x)  # This is a 6 bit signed number.
            x *= 2.5
            y *= -2.5
            dx = x
            out.stitch_abs(px + x, y)  # This is a hybrid relative, absolute value.
            px += dx
    # f.seek(20,1)
    # length_table_index = read_int_8(f)
    # length_table_size = read_int_8(f)
    # length_table = []
    # for j in range(length_table_size):
    #     v1 = read_int_16le(f)
    #     v2 = read_int_16le(f)
    #     length_table.append((v1, v2))
    # print("Length Index is: %d -- %s" % (length_table_index, str(length_table[length_table_index])))
    # print(length_table)
    # width_table_index = read_int_8(f)
    # width_table_size = read_int_8(f)
    # width_table = []
    # for j in range(width_table_size):
    #     v1 = read_int_16le(f)
    #     v2 = read_int_16le(f)
    #     width_table.append((v1, v2))
    # print("Width Index is: %d -- %s" % (width_table_index, str(width_table[width_table_index])))
    # print(width_table)
    out.end()


def read(f, out, settings=None):
    f.seek(0x64, 0)
    read_pmv_stitches(f, out)
