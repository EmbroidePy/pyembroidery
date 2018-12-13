def parse(f):
    comment = None
    code = ""
    value = ""
    command_map = {}
    ord_a = ord('a')
    ord_A = ord('A')
    ord_z = ord('z')
    ord_Z = ord('Z')
    while True:
        byte = f.read(1)
        if byte is None:
            break
        if len(byte) == 0:
            break
        is_end = byte == b'\n' or byte == b'\r'
        if comment is not None:
            if byte == b')' or is_end:
                command_map['comment'] = comment
                comment = None
                if not is_end:
                    continue
            else:
                try:
                    comment += byte.decode('utf8')
                except UnicodeDecodeError:
                    pass  # skip utf8 fail
                continue
        if byte == b'(':
            comment = ""
            continue
        elif byte == b';':
            comment = ""
            continue
        elif byte == b'\t':
            continue
        elif byte == b' ':
            continue
        elif byte == b'/' and len(code) == 0:
            continue
        b = ord(byte)
        if ord('0') <= b <= ord('9') \
                or byte == b'+' \
                or byte == b'-' \
                or byte == b'.':
            value += byte.decode('utf8')
            continue

        if ord_A <= b <= ord_Z:
            b = b - ord_A + ord_a
            byte = chr(b)
        is_letter = ord_a <= b <= ord_z
        if (is_letter or is_end) and len(code) != 0:
            command_map[code] = float(value)
            code = ""
            value = ""
        if is_letter:
            code += str(byte)
            continue
        elif is_end:
            if len(command_map) == 0:
                continue
            yield command_map
            command_map = {}
            code = ""
            value = ""
            continue


def read(f, out, settings=None):
    absolute_mode = True
    flip_x = -1  # Assumes the GCode is flip_x, -1 is flip, 1 is normal
    flip_y = -1  # Assumes the Gcode is flip_y,  -1 is flip, 1 is normal
    scale = 10.0  # Initially assume mm mode G20.
    for gc in parse(f):
        if 'comment' in gc:
            comment = gc['comment']
            if 'Thread' in comment:
                split = comment.split(" ")
                out.add_thread(split[1])

        if 'g' in gc:
            if 'x' in gc and 'y' in gc and gc['g'] == 0.0 or gc['g'] == 1.0:
                if absolute_mode:
                    out.stitch_abs(gc['x'] * scale * flip_x, gc['y'] * scale * flip_y)
                else:
                    out.stitch(gc['x'] * scale * flip_x, gc['y'] * scale * flip_y)
                continue
            if gc['g'] == 21.0 or gc['g'] == 71.0:
                scale = 10.0  # g20 is mm mode. 10 1/10th mm in a mm.
            elif gc['g'] == 20.0 or gc['g'] == 70.0:
                scale = 254  # g20 is inch mode. 254 1/10th mm in an inch.
            elif gc['g'] == 90.0:
                absolute_mode = True
            elif gc['g'] == 91.0:
                absolute_mode = False
        if 'm' in gc:
            v = gc['m']
            if v == 30 or v == 2:
                out.end()
            elif v == 0 or v == 1:
                out.color_change()
