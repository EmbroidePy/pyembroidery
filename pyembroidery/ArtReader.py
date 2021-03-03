# from .ReadHelper import read_int_8
# from io import BytesIO
#
# import compoundfiles
# import zlib
#
#
# def swizzle(b):
#     b ^= 0xD2
#     b <<= 1
#     b |= b >> 8
#     return b & 0xFF
#
#
# def parse_art_file(file):
#     with open(file, 'rb') as f:
#         contents = compoundfiles.CompoundFileReader(f).open('Contents')
#         contents.seek(4)  # file size
#         return zlib.decompress(bytes([swizzle(b) for b in contents.read()]))
#
#
# def read(f, out, settings=None):
#     contents = compoundfiles.CompoundFileReader(f).open('Contents')
#     contents.seek(4)  # file size
#     art = BytesIO(zlib.decompress(bytes([swizzle(b) for b in contents.read()])))
#     with open('file.bin', 'bw') as f:
#         while True:
#             b = read_int_8(art)
#             if b is None or b == -1:
#                 break
#             f.write(bytearray(chr(b), 'utf-8'))
#             print('%02X' % b)
