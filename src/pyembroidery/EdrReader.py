from .EmbThread import EmbThread
from .ReadHelper import read_int_8


def read(f, out, settings=None):
    while True:
        red = read_int_8(f)
        green = read_int_8(f)
        blue = read_int_8(f)
        if blue is None:
            return
        f.seek(1, 1)
        thread = EmbThread()
        thread.set_color(red, green, blue)
        out.add_thread(thread)
