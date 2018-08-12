from .ReadHelper import read_int_8, read_int_16le


def find_extends(stitches):
    min_x = float('inf')
    min_y = float('inf')
    max_x = -float('inf')
    max_y = -float('inf')

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
            y *= 2.5
            dx = x
            out.stitch_abs(px + x, y)  # This is a hybrid relative, absolute value.
            px += dx
            # stitches.append((x, y))
    out.end()
    # f.seek(0x10, 1)  # 16 bytes
    # block_end = read_int_16le(f)
    # if block_end != 256:
    #     return
    # steps = []
    # dunno0 = read_int_8(f)
    # dunno1 = read_int_8(f)
    # length_steps = read_int_8(f)
    # steps_size = read_int_8(f)
    # for i in range(0, steps_size):
    #     x = read_int_16le(f)
    #     y = read_int_16le(f)
    #     if x is None or y is None:
    #         break
    #     steps.append((x, y))
    # width_units = read_int_8(f)
    # steps2_size = read_int_8(f)
    # steps2 = []
    # for i in range(0, steps2_size):
    #     x = read_int_16le(f)
    #     y = read_int_16le(f)
    #     if x is None or y is None:
    #         break
    #     steps2.append((x, y))
    # dunno4 = read_int_16le(f)  # seems to be 0x12.
    # f.seek(0x10, 1)  # 16 bytes
    # # EOF - This should be End of File.
    # none_bytes = read_int_8(f)
    # if none_bytes is None:
    #     pass
    #
    # extends = find_extends(stitches)
    # print(f)
    # print("Stitches: Total ", len(stitches), " : ", stitches)
    # print("Unknown0:", dunno0)
    # print("Unknown1:", dunno1)
    # print("Length Position:", length_steps)
    # print("Length Lookup: ", len(steps), " : ", steps)
    # print("Length value:", steps[length_steps])
    # length_max = extends[2] - extends[0]
    # width_max = extends[3] - extends[1]
    # print("Max Length:", length_max)
    # print("Max dx+:", extends[2])
    # print("Max dx-:", extends[0])
    # print("Width Position:", width_units)
    # print("Width Lookup:", len(steps2), " : ", steps2)
    # print("Width value:", steps2[width_units])
    # print("Max Width:", width_max)
    #
    # print("Unknown4:", dunno4)

    out.end()


def read(f, out, settings=None):
    f.seek(0x64, 0)
    read_pmv_stitches(f, out)
