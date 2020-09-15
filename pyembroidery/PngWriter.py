import struct
import zlib

from .EmbConstant import *
from .EmbThread import EmbThread

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
FULL_JUMP = True

characters = {
    '0': [[9, 9, 4, 1, 0, 1, 5, 9, 9],
          [9, 3, 0, 0, 0, 0, 0, 5, 9],
          [7, 0, 1, 7, 9, 6, 0, 0, 9],
          [4, 0, 5, 9, 9, 9, 4, 0, 6],
          [3, 0, 8, 9, 9, 9, 6, 0, 4],
          [2, 0, 9, 5, 0, 6, 8, 0, 3],
          [2, 0, 9, 4, 0, 6, 8, 0, 3],
          [2, 0, 9, 9, 9, 9, 8, 0, 3],
          [3, 0, 8, 9, 9, 9, 6, 0, 4],
          [4, 0, 5, 9, 9, 9, 4, 0, 6],
          [7, 0, 1, 7, 9, 6, 0, 0, 8],
          [9, 3, 0, 0, 0, 0, 0, 5, 9],
          [9, 9, 4, 1, 0, 1, 5, 9, 9]],

    '1': [[9, 8, 5, 2, 0, 1, 9, 9, 9],
          [9, 1, 0, 0, 0, 1, 9, 9, 9],
          [9, 2, 4, 7, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 9, 9, 9, 1, 1, 9, 9, 9],
          [9, 3, 0, 0, 0, 0, 0, 0, 3],
          [9, 3, 0, 0, 0, 0, 0, 0, 3]],

    '2': [[8, 5, 2, 1, 1, 2, 6, 9, 9],
          [4, 0, 0, 0, 0, 0, 0, 4, 9],
          [5, 4, 7, 8, 8, 5, 0, 0, 8],
          [9, 9, 9, 9, 9, 9, 3, 0, 7],
          [9, 9, 9, 9, 9, 9, 3, 0, 9],
          [9, 9, 9, 9, 9, 8, 0, 4, 9],
          [9, 9, 9, 9, 8, 1, 2, 9, 9],
          [9, 9, 9, 8, 2, 2, 9, 9, 9],
          [9, 9, 8, 1, 2, 9, 9, 9, 9],
          [9, 8, 1, 2, 9, 9, 9, 9, 9],
          [7, 1, 2, 9, 9, 9, 9, 9, 9],
          [3, 0, 0, 0, 0, 0, 0, 0, 6],
          [3, 0, 0, 0, 0, 0, 0, 0, 6]],

    '3': [[9, 6, 2, 1, 1, 2, 6, 9, 9],
          [5, 0, 0, 0, 0, 0, 0, 4, 9],
          [6, 3, 7, 8, 9, 6, 1, 0, 8],
          [9, 9, 9, 9, 9, 9, 3, 0, 8],
          [9, 9, 9, 9, 8, 6, 1, 1, 9],
          [9, 9, 4, 0, 0, 0, 2, 8, 9],
          [9, 9, 4, 0, 0, 0, 2, 8, 9],
          [9, 9, 9, 9, 8, 6, 1, 1, 8],
          [9, 9, 9, 9, 9, 9, 5, 0, 6],
          [9, 9, 9, 9, 9, 9, 5, 0, 5],
          [3, 5, 7, 9, 8, 6, 1, 0, 7],
          [2, 0, 0, 0, 0, 0, 0, 3, 9],
          [8, 4, 2, 0, 1, 2, 5, 9, 9]],

    '4': [[9, 9, 9, 9, 7, 0, 0, 7, 9],
          [9, 9, 9, 9, 2, 1, 0, 7, 9],
          [9, 9, 9, 5, 2, 4, 0, 7, 9],
          [9, 9, 8, 1, 7, 4, 0, 7, 9],
          [9, 9, 3, 4, 9, 4, 0, 7, 9],
          [9, 6, 1, 9, 9, 4, 0, 7, 9],
          [8, 1, 6, 9, 9, 4, 0, 7, 9],
          [4, 3, 9, 9, 9, 4, 0, 7, 9],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [9, 9, 9, 9, 9, 4, 0, 7, 9],
          [9, 9, 9, 9, 9, 4, 0, 7, 9],
          [9, 9, 9, 9, 9, 4, 0, 7, 9]],

    '5': [[7, 0, 0, 0, 0, 0, 0, 5, 9],
          [7, 0, 0, 0, 0, 0, 0, 5, 9],
          [7, 0, 5, 9, 9, 9, 9, 9, 9],
          [7, 0, 5, 9, 9, 9, 9, 9, 9],
          [7, 0, 1, 1, 0, 2, 6, 9, 9],
          [7, 0, 0, 0, 0, 0, 0, 5, 9],
          [7, 4, 7, 9, 8, 4, 0, 0, 9],
          [9, 9, 9, 9, 9, 9, 3, 0, 6],
          [9, 9, 9, 9, 9, 9, 5, 0, 6],
          [9, 9, 9, 9, 9, 9, 3, 0, 6],
          [3, 5, 8, 9, 8, 5, 0, 0, 9],
          [2, 0, 0, 0, 0, 0, 0, 6, 9],
          [8, 4, 1, 0, 1, 2, 7, 9, 9]],

    '6': [[9, 9, 7, 2, 1, 0, 3, 8, 9],
          [9, 6, 0, 0, 0, 0, 0, 3, 9],
          [8, 0, 0, 4, 8, 9, 6, 4, 9],
          [5, 0, 4, 9, 9, 9, 9, 9, 9],
          [3, 0, 8, 9, 9, 9, 9, 9, 9],
          [2, 1, 8, 3, 0, 1, 3, 8, 9],
          [2, 2, 2, 0, 0, 0, 0, 1, 8],
          [2, 0, 2, 7, 9, 8, 2, 0, 5],
          [3, 0, 7, 9, 9, 9, 7, 0, 3],
          [4, 0, 7, 9, 9, 9, 7, 0, 3],
          [7, 0, 2, 7, 9, 8, 2, 0, 5],
          [9, 3, 0, 0, 0, 0, 0, 1, 8],
          [9, 9, 4, 1, 0, 1, 3, 8, 9]],

    '7': [[2, 0, 0, 0, 0, 0, 0, 0, 5],
          [2, 0, 0, 0, 0, 0, 0, 0, 7],
          [9, 9, 9, 9, 9, 9, 3, 2, 9],
          [9, 9, 9, 9, 9, 8, 0, 5, 9],
          [9, 9, 9, 9, 9, 4, 0, 8, 9],
          [9, 9, 9, 9, 9, 1, 3, 9, 9],
          [9, 9, 9, 9, 6, 0, 6, 9, 9],
          [9, 9, 9, 9, 2, 1, 9, 9, 9],
          [9, 9, 9, 7, 0, 4, 9, 9, 9],
          [9, 9, 9, 3, 0, 8, 9, 9, 9],
          [9, 9, 8, 0, 2, 9, 9, 9, 9],
          [9, 9, 5, 0, 6, 9, 9, 9, 9],
          [9, 9, 1, 0, 9, 9, 9, 9, 9]],

    '8': [[9, 8, 3, 1, 0, 1, 4, 8, 9],
          [8, 1, 0, 0, 0, 0, 0, 1, 9],
          [5, 0, 3, 8, 9, 7, 2, 0, 6],
          [5, 0, 7, 9, 9, 9, 5, 0, 6],
          [7, 0, 3, 8, 9, 7, 2, 1, 8],
          [9, 7, 2, 0, 0, 0, 2, 7, 9],
          [9, 5, 1, 0, 0, 0, 1, 6, 9],
          [6, 0, 3, 8, 9, 7, 2, 0, 7],
          [2, 0, 9, 9, 9, 9, 7, 0, 4],
          [2, 0, 9, 9, 9, 9, 7, 0, 3],
          [3, 0, 3, 8, 9, 7, 2, 0, 4],
          [7, 0, 0, 0, 0, 0, 0, 1, 8],
          [9, 8, 3, 1, 0, 1, 4, 8, 9]],

    '9': [[9, 7, 3, 0, 0, 2, 6, 9, 9],
          [7, 0, 0, 0, 0, 0, 0, 5, 9],
          [3, 0, 4, 8, 9, 7, 1, 0, 9],
          [1, 0, 9, 9, 9, 9, 5, 0, 6],
          [1, 1, 9, 9, 9, 9, 5, 0, 5],
          [3, 0, 4, 8, 9, 7, 1, 0, 4],
          [7, 0, 0, 0, 0, 0, 3, 0, 4],
          [9, 7, 2, 0, 1, 4, 7, 0, 4],
          [9, 9, 9, 9, 9, 9, 5, 0, 5],
          [9, 9, 9, 9, 9, 9, 2, 0, 7],
          [9, 3, 7, 9, 8, 3, 0, 2, 9],
          [9, 1, 0, 0, 0, 0, 0, 7, 9],
          [9, 7, 2, 0, 1, 3, 8, 9, 9]],

    '-': [[9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 1, 0, 0, 0, 3, 9, 9],
          [9, 9, 1, 0, 0, 0, 3, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9]],

    'm': [[9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [9, 9, 9, 9, 9, 9, 9, 9, 9],
          [0, 5, 2, 1, 7, 6, 1, 2, 8],
          [0, 1, 0, 0, 1, 1, 0, 0, 3],
          [0, 2, 9, 4, 0, 4, 8, 2, 1],
          [0, 5, 9, 6, 0, 7, 9, 4, 1],
          [0, 5, 9, 6, 0, 7, 9, 4, 0],
          [0, 5, 9, 6, 0, 7, 9, 4, 0],
          [0, 5, 9, 6, 0, 7, 9, 4, 0],
          [0, 5, 9, 6, 0, 7, 9, 4, 0],
          [0, 5, 9, 6, 0, 7, 9, 4, 0],
          [0, 5, 9, 6, 0, 7, 9, 4, 0]]
}


def write_png(buf, width, height):
    width_byte_4 = width * 4
    raw_data = b"".join(
        b'\x00' + buf[span:span + width_byte_4] for span in range(0, height * width * 4, width_byte_4))

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

    def draw_text(self, x, y, string, rotate=False):
        for c in string:
            m = characters[c]
            for cx in range(len(m[0])):
                for cy in range(len(m)):
                    v = m[cy][cx]
                    if v == 9:
                        continue
                    if rotate:
                        gx = x + (len(m) - cy) + 1
                        gy = y + cx + 2
                    else:
                        gx = x + cx + 2
                        gy = y + cy + 2
                    pos = (self.width * gy) + gx
                    idx = pos * 4
                    a2 = (9.0 - v) / 9.0
                    r = (1.0 - a2) * self.buf[idx]
                    g = (1.0 - a2) * self.buf[idx + 1]
                    b = (1.0 - a2) * self.buf[idx + 2]
                    a1 = self.buf[idx + 3] / 255.0
                    a = a2 + a1 * (1.0 - a2)
                    try:
                        self.buf[idx] = int(r)
                        self.buf[idx + 1] = int(g)
                        self.buf[idx + 2] = int(b)
                        self.buf[idx + 3] = int(a * 255)
                    except IndexError:
                        pass
            if rotate:
                y += 11
            else:
                x += 11


def write(pattern, f, settings=None):
    guides = settings.get("guides", False)
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
            y = int(stitch[1])
            if last_x is not None:
                draw_buff.draw_line(last_x, last_y, x, y)
            last_x = x
            last_y = y

    if guides:
        draw_buff.red = 0
        draw_buff.green = 0
        draw_buff.blue = 0
        draw_buff.alpha = 255
        draw_buff.line_width = 1
        min_x = extends[0]
        min_y = extends[1]
        points = 50
        draw_buff.draw_text(0, 0, 'mm')
        for x in range(points-(min_x % points), width - 30, points):
            if x < 30:
                continue
            draw_buff.draw_text(x, 0, str(int((x + min_x) / 10)), rotate=True)
            draw_buff.draw_line(x, 0, x, 30)
        for y in range(points-(min_y % points), height - 30, points):
            if y < 30:
                continue
            draw_buff.draw_text(0, y, str(int((y + min_y) / 10)))
            draw_buff.draw_line(0, y, 30, y)

    f.write(write_png(bytes(bytearray(draw_buff.buf)), draw_buff.width, draw_buff.height))
