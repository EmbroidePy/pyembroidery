MIT_SIZE_CONVERSION_RATIO = 2.0 / 1.0


def read(f, out, settings=None):
    count = 0
    previous_ctrl = -1
    while True:
        count += 1
        byte = bytearray(f.read(2))
        if len(byte) != 2:
            break
        x = byte[0] & 0x1F
        y = -(byte[1] & 0x1F)
        x *= MIT_SIZE_CONVERSION_RATIO
        y *= MIT_SIZE_CONVERSION_RATIO
        if byte[0] & 0b10000000:
            x = -x
        if byte[1] & 0b10000000:
            y = -y
        ctrl = ((byte[0] & 0x60) >> 3) | ((byte[1] & 0x60) >> 5)
        if ctrl == 0b0111:
            out.stitch(x, y)
            previous_ctrl = ctrl
            continue
        elif ctrl == 0b1100:
            out.move(x, y)
        elif ctrl == 0b0100:
            out.stitch(x, y)
        elif ctrl == 0b0101:
            out.stitch(x, y)
        elif ctrl == 0b1000:
            if previous_ctrl == 0b111:
                out.color_change()
        elif ctrl == 0b0000:
            out.end()  # 0 appears at end.
        else:
            out.stitch(x, y)
        previous_ctrl = ctrl
    out.end()
