from .DstReader import dst_read_stitches


def read(f, out, settings=None):
    f.seek(0x100)
    dst_read_stitches(f, out, settings)
