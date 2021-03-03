def getbit(b, pos):
    return (b >> pos) & 1


def decode_dx(b0, b1, b2):
    x = 0
    x += getbit(b2, 2) * (+81)
    x += getbit(b2, 3) * (-81)
    x += getbit(b1, 2) * (+27)
    x += getbit(b1, 3) * (-27)
    x += getbit(b0, 2) * (+9)
    x += getbit(b0, 3) * (-9)
    x += getbit(b1, 0) * (+3)
    x += getbit(b1, 1) * (-3)
    x += getbit(b0, 0) * (+1)
    x += getbit(b0, 1) * (-1)
    return x


def decode_dy(b0, b1, b2):
    y = 0
    y += getbit(b2, 5) * (+81)
    y += getbit(b2, 4) * (-81)
    y += getbit(b1, 5) * (+27)
    y += getbit(b1, 4) * (-27)
    y += getbit(b0, 5) * (+9)
    y += getbit(b0, 4) * (-9)
    y += getbit(b1, 7) * (+3)
    y += getbit(b1, 6) * (-3)
    y += getbit(b0, 7) * (+1)
    y += getbit(b0, 6) * (-1)
    return -y


def process_header_info(out, prefix, value):
    if prefix == "LA":
        out.metadata("name", value)
    elif prefix == "AU":
        out.metadata("author", value)
    elif prefix == "CP":
        out.metadata("copyright", value)
    elif prefix == "TC":
        values = [x.strip() for x in value.split(",")]
        out.add_thread({"hex": values[0], "description": value[1], "catalog": value[2]})
    else:
        out.metadata(prefix, value)


def dst_read_header(f, out):
    header = f.read(512)
    start = 0
    for i, element in enumerate(header):
        if (
            element == 13 or element == 10 or element == "\n" or element == "\r"
        ):  # 13 =='\r', 10 = '\n'
            end = i
            data = header[start:end]
            start = end
            try:
                line = data.decode("utf8").strip()
                if len(line) > 3:
                    process_header_info(out, line[0:2].strip(), line[3:].strip())
            except UnicodeDecodeError:  # Non-utf8 information. See #83
                continue


def dst_read_stitches(f, out, settings=None):
    sequin_mode = False
    while True:
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        dx = decode_dx(byte[0], byte[1], byte[2])
        dy = decode_dy(byte[0], byte[1], byte[2])
        if byte[2] & 0b11110011 == 0b11110011:
            break
        elif byte[2] & 0b11000011 == 0b11000011:
            out.color_change(dx, dy)
        elif byte[2] & 0b01000011 == 0b01000011:
            out.sequin_mode(dx, dy)
            sequin_mode = not sequin_mode
        elif byte[2] & 0b10000011 == 0b10000011:
            if sequin_mode:
                out.sequin_eject(dx, dy)
            else:
                out.move(dx, dy)
        else:
            out.stitch(dx, dy)
    out.end()

    count_max = 3
    clipping = True
    trim_distance = None
    if settings is not None:
        count_max = settings.get("trim_at", count_max)
        trim_distance = settings.get("trim_distance", trim_distance)
        clipping = settings.get("clipping", clipping)
    if trim_distance is not None:
        trim_distance *= 10  # Pixels per mm. Native units are 1/10 mm.
    out.interpolate_trims(count_max, trim_distance, clipping)


def read(f, out, settings=None):
    dst_read_header(f, out)
    dst_read_stitches(f, out, settings)
