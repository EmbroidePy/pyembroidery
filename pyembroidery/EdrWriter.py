from .WriteHelper import write_int_8

ENCODE = False


def write(pattern, f, settings=None):
    if len(pattern.threadlist) > 0:
        for thread in pattern.threadlist:
            write_int_8(f, thread.get_red())
            write_int_8(f, thread.get_green())
            write_int_8(f, thread.get_blue())
            write_int_8(f, 0)
