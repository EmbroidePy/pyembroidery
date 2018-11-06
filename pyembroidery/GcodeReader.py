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
        if comment is not None:
            if byte == b')':
                command_map['comment'] = comment
                comment = None
            else:
                try:
                    comment += byte.decode('utf8')
                except UnicodeDecodeError:
                    pass  # skip utf8 fail
            continue
        if byte == b'(':
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
        is_end = byte == b'\n' or byte == b'\r'
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
    scale = -10.0
    for gc in parse(f):
        if 'comment' in gc:
            comment = gc['comment']
            if 'Thread' in comment:
                split = comment.split(" ")
                out.add_thread(split[1])

        if 'g' in gc and 'x' in gc and 'y' in gc:
            if gc['g'] == 0.0 or gc['g'] == 1.0:
                out.stitch_abs(gc['x'] * scale, gc['y'] * scale)
        if 'm' in gc:
            v = gc['m']
            if v == 30 or v == 2:
                out.end()
            elif v == 0 or v == 1:
                out.color_change()
