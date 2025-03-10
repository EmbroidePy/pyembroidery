def signed8(b):
    if b > 127:
        return -256 + b
    else:
        return b


def signed16(v):
    v &= 0xFFFF
    if v > 0x7FFF:
        return -0x10000 + v
    else:
        return v


def signed24(v):
    v &= 0xFFFFFF
    if v > 0x7FFFFF:
        return -0x1000000 + v
    else:
        return v


def read_signed(stream, n):
    byte = bytearray(stream.read(n))
    signed_bytes = []
    for b in byte:
        signed_bytes.append(signed8(b))
    return signed_bytes


def read_sint_8(stream):
    byte = bytearray(stream.read(1))
    if len(byte) == 1:
        return signed8(byte[0])
    return None


def read_int_8(stream):
    byte = bytearray(stream.read(1))
    if len(byte) == 1:
        return byte[0]
    return None


def read_int_16le(stream):
    byte = bytearray(stream.read(2))
    if len(byte) == 2:
        return (byte[0] & 0xFF) + ((byte[1] & 0xFF) << 8)
    return None


def read_int_16be(stream):
    byte = bytearray(stream.read(2))
    if len(byte) == 2:
        return (byte[1] & 0xFF) + ((byte[0] & 0xFF) << 8)
    return None


def read_int_24le(stream):
    b = bytearray(stream.read(3))
    if len(b) == 3:
        return (b[0] & 0xFF) + ((b[1] & 0xFF) << 8) + ((b[2] & 0xFF) << 16)
    return None


def read_int_24be(stream):
    b = bytearray(stream.read(3))
    if len(b) == 3:
        return (b[2] & 0xFF) + ((b[1] & 0xFF) << 8) + ((b[0] & 0xFF) << 16)
    return None


def read_int_32le(stream):
    b = bytearray(stream.read(4))
    if len(b) == 4:
        return (
            (b[0] & 0xFF)
            + ((b[1] & 0xFF) << 8)
            + ((b[2] & 0xFF) << 16)
            + ((b[3] & 0xFF) << 24)
        )
    return None


def read_int_32be(stream):
    b = bytearray(stream.read(4))
    if len(b) == 4:
        return (
            (b[3] & 0xFF)
            + ((b[2] & 0xFF) << 8)
            + ((b[1] & 0xFF) << 16)
            + ((b[0] & 0xFF) << 24)
        )
    return None


def read_string_8(stream, length):
    byte = stream.read(length)
    try:
        return byte.decode("utf8")
    except UnicodeDecodeError:
        return None  # Must be > 128 chars.


def read_string_16(stream, length):
    byte = stream.read(length)
    try:
        return byte.decode("utf16")
    except UnicodeDecodeError:
        return None
