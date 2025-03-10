from .DszReader import z_stitch_encoding_read


def read(f, out, settings=None):
    f.seek(0x100)
    z_stitch_encoding_read(f, out)
