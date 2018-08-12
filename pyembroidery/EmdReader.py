from .ReadHelper import signed8


def read_emd_stitches(f, out):
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
        control = b[1]
        if control == 0x80:
            b = bytearray(f.read(2))
            if len(b) != 2:
                break
            x = signed8(b[0])
            y = -signed8(b[1])
            out.move(x, y)
            continue
        if control == 0x2A:
            out.color_change()
            continue
        if control == 0x7D:
            continue  # Dunno, occurs at position 0.
        if control == 0xAD:
            out.trim()
            continue
        if control == 0x90:
            out.trim()  # Final command before returning to start.
            continue
        elif control == 0xFD:
            break
        break  # Uncaught Control
    out.end()


def read(f, out, settings=None):
    f.seek(0x30, 0)
    read_emd_stitches(f, out)
