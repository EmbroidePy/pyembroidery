from .ReadHelper import read_int_32le, read_int_16le, read_int_8, read_int_24be, signed8


def read_zhs_stitches(f, out):
    count = 0

    xx = 0
    yy = 0
    while True:
        count += 1
        b = bytearray(f.read(3))
        if len(b) != 3:
            break
        ctrl = b[0]
        if ctrl == 0x10:
            # Checksum
            continue
        # x
        x = 0
        x += b[1] & 0b00000001
        x += b[2] & 0b00000010
        x += b[1] & 0b00000100
        x += b[2] & 0b00001000
        x += b[1] & 0b00010000
        x += b[2] & 0b00100000
        x += b[1] & 0b01000000
        x += b[2] & 0b10000000
        x = signed8(x)
        if x >= 63:
            x += 1
        if x <= -63:
            x -= 1

        # y
        y = 0
        y += b[2] & 0b00000001
        y += b[1] & 0b00000010
        y += b[2] & 0b00000100
        y += b[1] & 0b00001000
        y += b[2] & 0b00010000
        y += b[1] & 0b00100000
        y += b[2] & 0b01000000
        y += b[1] & 0b10000000

        y = signed8(y)
        if y >= 63:
            y += 1
        if y <= -63:
            y -= 1

        xx += x
        yy += y
        if ctrl == 0x41:
            # Still unmapped.
            pass
        elif ctrl == 0x02:
            out.stitch(xx, -yy)
            xx = 0
            yy = 0
            continue
        elif ctrl == 0x01:
            out.move(xx, -yy)
            xx = 0
            yy = 0
            continue
        elif ctrl == 0x04:
            xx = 0
            yy = 0
            out.color_change()
            continue
        elif ctrl == 0x80:
            break
    out.end()


def read_zhs_header(f, out):
    color_count = read_int_8(f)
    for i in range(color_count):
        out.add_thread(read_int_24be(f))
    length = read_int_16le(f)
    b = bytearray(f.read(length))
    thread_data = b.decode('utf8')
    threads = thread_data.split("&$")
    try:
        for i, data in enumerate(threads[1:]):
            thread = out.threadlist[i]
            parts = data.split("&#")
            try:
                if len(parts[0]):
                    thread.chart = parts[0]
                if len(parts[1]):
                    thread.description = parts[1]
                if len(parts[2]) > 3:
                    thread.catalog_number = parts[2][:-2]
            except IndexError:
                pass
    except IndexError:
        pass


def read(f, out, settings=None):
    f.seek(0x0F, 0)
    stitch_start_position = read_int_32le(f)
    header_start_position = read_int_32le(f)
    f.seek(header_start_position, 0)
    read_zhs_header(f, out)
    f.seek(stitch_start_position, 0)
    read_zhs_stitches(f, out)
