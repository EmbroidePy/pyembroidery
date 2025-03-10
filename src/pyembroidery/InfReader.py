from .EmbThread import EmbThread
from .ReadHelper import read_int_16be, read_int_32be


def read(f, out, settings=None):
    u0 = read_int_32be(f)
    u1 = read_int_32be(f)
    u2 = read_int_32be(f)
    number_of_colors = read_int_32be(f)
    for j in range(0, number_of_colors):
        length = read_int_16be(f) - 2  # 2 bytes of the length.
        byte_data = bytearray(f.read(length))
        if len(byte_data) != length:
            break
        red = byte_data[2]
        green = byte_data[3]
        blue = byte_data[4]
        thread = EmbThread()
        thread.set_color(red, green, blue)
        byte_data = byte_data[7:]
        for j in range(0, len(byte_data)):
            b = byte_data[j]
            if b == 0:
                thread.description = byte_data[:j].decode("utf8")
                byte_data = byte_data[j + 1 :]
                break
        for j in range(0, len(byte_data)):
            b = byte_data[j]
            if b == 0:
                thread.chart = byte_data[:j].decode("utf8")
                break
        out.add_thread(thread)
