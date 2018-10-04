import struct
import zlib

from .EmbConstant import *
from .EmbThread import EmbThread

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
FULL_JUMP = True


def write_png(buf, width, height):
    width_byte_4 = width * 4
    raw_data = b"".join(
        b'\x00' + buf[span:span + width_byte_4] for span in range((height - 1) * width * 4, -1, - width_byte_4))

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return struct.pack("!I", len(data)) + chunk_head + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))

    return b"".join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])


class PngBuffer:
    def __init__(self, width, height):
        self.width = int(width + 3)
        self.height = int(height + 3)
        self.buf = [0] * (4 * self.width * self.height)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.alpha = 0
        self.line_width = 3

    def background(self, red, green, blue, alpha):
        for i in range(0, len(self.buf), 4):
            self.buf[i] = red
            self.buf[i + 1] = green
            self.buf[i + 2] = blue
            self.buf[i + 3] = alpha

    def plot(self, x, y):
        try:
            x += 1
            y += 1
            pos = (self.width * y) + x
            idx = pos * 4
            self.buf[idx] = self.red
            self.buf[idx + 1] = self.green
            self.buf[idx + 2] = self.blue
            self.buf[idx + 3] = self.alpha
        except IndexError:
            pass

    def draw_line(self, x0, y0, x1, y1):
        dy = y1 - y0  # BRESENHAM LINE DRAW ALGORITHM
        dx = x1 - x0
        if dy < 0:
            dy = -dy
            step_y = -1
        else:
            step_y = 1
        if dx < 0:
            dx = -dx
            step_x = -1
        else:
            step_x = 1
        if dx > dy:
            dy <<= 1  # dy is now 2*dy
            dx <<= 1
            fraction = dy - (dx >> 1)  # same as 2*dy - dx
            self.line_for_point(x0, y0, False)

            while x0 != x1:
                if fraction >= 0:
                    y0 += step_y
                    fraction -= dx  # same as fraction -= 2*dx
                x0 += step_x
                fraction += dy  # same as fraction += 2*dy
                self.line_for_point(x0, y0, False)
        else:
            dy <<= 1  # dy is now 2*dy
            dx <<= 1  # dx is now 2*dx
            fraction = dx - (dy >> 1)
            self.line_for_point(x0, y0, True)
            while y0 != y1:
                if fraction >= 0:
                    x0 += step_x
                    fraction -= dy
                y0 += step_y
                fraction += dx
                self.line_for_point(x0, y0, True)

    def line_for_point(self, x, y, dy):
        w = self.line_width
        left = w >> 1
        right = w - left
        if dy:
            for pos in range(-left, right):
                self.plot(x + pos, y)
        else:
            for pos in range(-left, right):
                self.plot(x, y + pos)


def write(pattern, f, settings=None):
    extends = pattern.bounds()
    pattern.translate(-extends[0], -extends[1])
    width = int(extends[2] - extends[0])
    height = int(extends[3] - extends[1])
    draw_buff = PngBuffer(width, height)
    if settings is not None:
        background = settings.get("background", None)
        linewidth = settings.get("linewidth", None)
        if background is not None:
            b = EmbThread()
            b.set(background)
            draw_buff.background(b.get_red(), b.get_green(), b.get_blue(), 0xFF)
        if linewidth is not None and isinstance(linewidth, int):
            draw_buff.line_width = linewidth

    for stitchblock in pattern.get_as_stitchblock():
        block = stitchblock[0]
        thread = stitchblock[1]
        draw_buff.red = thread.get_red()
        draw_buff.green = thread.get_green()
        draw_buff.blue = thread.get_blue()
        draw_buff.alpha = 255
        last_x = None
        last_y = None
        for stitch in block:
            x = int(stitch[0])
            y = -int(stitch[1])
            if last_x is not None:
                draw_buff.draw_line(last_x, last_y, x, y)
            last_x = x
            last_y = y
    f.write(write_png(bytes(bytearray(draw_buff.buf)), draw_buff.width, draw_buff.height))
