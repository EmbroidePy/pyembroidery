from .ExpReader import read_exp_stitches
from .ReadHelper import read_int_32le


def read(f, out, settings=None):
    # File starts with STX
    f.seek(0x0C, 1)
    color_start_position = read_int_32le(f)
    dunno_block_start_position = read_int_32le(f)
    stitch_start_position = read_int_32le(f)
    f.seek(stitch_start_position, 0)
    read_exp_stitches(f, out)
