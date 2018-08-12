import struct


def write_int_array_8(stream, int_array):
    for value in int_array:
        v = bytes(bytearray([
            value & 0xFF,
        ]))
        stream.write(v)


def write_int_8(stream, value):
    v = bytes(bytearray([
        value & 0xFF,
    ]))
    stream.write(v)


def write_int_16le(stream, value):
    v = bytes(bytearray([
        (value >> 0) & 0xFF,
        (value >> 8) & 0xFF,
    ]))
    stream.write(v)


def write_int_16be(stream, value):
    v = bytes(bytearray([
        (value >> 8) & 0xFF,
        (value >> 0) & 0xFF,
    ]))
    stream.write(v)


def write_int_24le(stream, value):
    v = bytes(bytearray([
        (value >> 0) & 0xFF,
        (value >> 8) & 0xFF,
        (value >> 16) & 0xFF,
    ]))
    stream.write(v)


def write_int_24be(stream, value):
    v = bytes(bytearray([
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        (value >> 0) & 0xFF,
    ]))
    stream.write(v)


def write_int_32le(stream, value):
    v = bytes(bytearray([
        (value >> 0) & 0xFF,
        (value >> 8) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 24) & 0xFF
    ]))
    stream.write(v)


def write_int_32be(stream, value):
    v = bytes(bytearray([
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        (value >> 0) & 0xFF
    ]))
    stream.write(v)


def write_float_32le(stream, value):
    stream.write(struct.pack("<f", float(value)))


def write_string(stream, string, encoding='utf8'):
    # python 2,3 code
    try:
        stream.write(bytes(string).encode(encoding))
    except TypeError:
        stream.write(bytes(string, encoding))


def write_string_utf8(stream, string):
    # python 2,3 code
    try:
        stream.write(bytes(string).encode('utf8'))
    except TypeError:
        stream.write(bytes(string, 'utf8'))
