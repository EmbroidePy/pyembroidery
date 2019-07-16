from .DstReader import dst_read_stitches


def read(f, out, settings=None):
    dst_read_stitches(f, out, settings)
