import struct
import zlib
from math import sqrt

from .EmbConstant import *
from .EmbThread import EmbThread

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
FULL_JUMP = True

# Static characters for writing to image.
characters = {
    "0": [
        [9, 9, 4, 1, 0, 1, 5, 9, 9],
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
        [9, 9, 4, 1, 0, 1, 5, 9, 9],
    ],
    "1": [
        [9, 8, 5, 2, 0, 1, 9, 9, 9],
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
        [9, 3, 0, 0, 0, 0, 0, 0, 3],
    ],
    "2": [
        [8, 5, 2, 1, 1, 2, 6, 9, 9],
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
        [3, 0, 0, 0, 0, 0, 0, 0, 6],
    ],
    "3": [
        [9, 6, 2, 1, 1, 2, 6, 9, 9],
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
        [8, 4, 2, 0, 1, 2, 5, 9, 9],
    ],
    "4": [
        [9, 9, 9, 9, 7, 0, 0, 7, 9],
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
        [9, 9, 9, 9, 9, 4, 0, 7, 9],
    ],
    "5": [
        [7, 0, 0, 0, 0, 0, 0, 5, 9],
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
        [8, 4, 1, 0, 1, 2, 7, 9, 9],
    ],
    "6": [
        [9, 9, 7, 2, 1, 0, 3, 8, 9],
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
        [9, 9, 4, 1, 0, 1, 3, 8, 9],
    ],
    "7": [
        [2, 0, 0, 0, 0, 0, 0, 0, 5],
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
        [9, 9, 1, 0, 9, 9, 9, 9, 9],
    ],
    "8": [
        [9, 8, 3, 1, 0, 1, 4, 8, 9],
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
        [9, 8, 3, 1, 0, 1, 4, 8, 9],
    ],
    "9": [
        [9, 7, 3, 0, 0, 2, 6, 9, 9],
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
        [9, 7, 2, 0, 1, 3, 8, 9, 9],
    ],
    "-": [
        [9, 9, 9, 9, 9, 9, 9, 9, 9],
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
        [9, 9, 9, 9, 9, 9, 9, 9, 9],
    ],
    "m": [
        [9, 9, 9, 9, 9, 9, 9, 9, 9],
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
        [0, 5, 9, 6, 0, 7, 9, 4, 0],
    ],
}


def write_png(buf, width, height):
    """
    Writes PNG file to disk. Buffer must be RGBA * width * height
    """
    width_byte_4 = width * 4
    raw_data = b"".join(
        b"\x00" + buf[span : span + width_byte_4]
        for span in range(0, height * width * 4, width_byte_4)
    )

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (
            struct.pack("!I", len(data))
            + chunk_head
            + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
        )

    return b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_pack(b"IHDR", struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
            png_pack(b"IDAT", zlib.compress(raw_data, 9)),
            png_pack(b"IEND", b""),
        ]
    )


class PngBuffer:
    def __init__(self, width, height):
        self.width = int(width + 3)
        self.height = int(height + 3)
        self.buf = bytearray(4 * self.width * self.height)
        self.line_width = 3
        self.fancy = True
        self._red = 0
        self._green = 0
        self._blue = 0
        self._alpha = 0
        self._distance_from_black = 0
        self._gradient_shade_ends = 0.65
        self._gradient_shade_edge = 1.1
        self._gradient_shade_center = 1.55
        self._gradient_color_position1 = 0.40
        self._gradient_color_position2 = 0.50
        self._gradient_color_position3 = 0.70

    def modify_gradient(
        self,
        gradient_shade_ends=0.65,
        gradient_shade_edge=1.1,
        gradient_shade_center=1.55,
        gradient_color_position1=0.40,
        gradient_color_position2=0.50,
        gradient_color_position3=0.70,
    ):
        self._gradient_shade_ends = gradient_shade_ends
        self._gradient_shade_edge = gradient_shade_edge
        self._gradient_shade_center = gradient_shade_center
        self._gradient_color_position1 = gradient_color_position1
        self._gradient_color_position2 = gradient_color_position2
        self._gradient_color_position3 = gradient_color_position3

    def set_color(self, r, g, b, a=255):
        self._red = r
        self._green = g
        self._blue = b
        self._alpha = a
        rmean = int(r / 2)
        self._distance_from_black = sqrt(
            (((512 + rmean) * r * r) >> 8) + 4 * g * g + (((767 - rmean) * b * b) >> 8)
        )

    def gradient(self, position_in_line):
        """
        This function gives different value scales between 0 and 1 which are used to multiply
        all the components of the color to create a darker value. This generally works save for
        black which is already (0,0,0) and can't increase value.
        """
        if (
            position_in_line <= self._gradient_color_position1
        ):  # start_of_grdient -> Position 1
            from_shade = self._gradient_shade_ends
            to_shade = self._gradient_shade_edge
            range = self._gradient_color_position1 - 0  # Range of transition
            amount = (position_in_line - 0) * (1 / range)

        # light to extra_light
        elif (
            position_in_line <= self._gradient_color_position2
        ):  # Position 1 -> Position 2.
            from_shade = self._gradient_shade_edge
            to_shade = self._gradient_shade_center
            range = self._gradient_color_position2 - self._gradient_color_position1
            amount = (position_in_line - self._gradient_color_position1) * (1 / range)

        # center of gradient

        # extra_light to light
        elif (
            position_in_line <= self._gradient_color_position3
        ):  # Position 2 -> Position 3
            from_shade = self._gradient_shade_center
            to_shade = self._gradient_shade_edge
            range = self._gradient_color_position3 - self._gradient_color_position2
            amount = (position_in_line - self._gradient_color_position2) * (1 / range)

        # light to dark
        elif position_in_line <= 1:  # Position 3 -> end_of_gradient
            from_shade = self._gradient_shade_edge
            to_shade = self._gradient_shade_ends
            range = 1 - self._gradient_color_position3
            amount = (position_in_line - self._gradient_color_position3) * (1 / range)
        else:
            raise ValueError("Did not occur within line.")
        v = amount * (to_shade - from_shade) + from_shade
        return max(min(v, 1.0), 0.0)

    def background(self, red, green, blue, alpha):
        for i in range(0, len(self.buf), 4):
            self.buf[i] = red
            self.buf[i + 1] = green
            self.buf[i + 2] = blue
            self.buf[i + 3] = alpha

    def plot(self, x, y, v=None, a=None):
        """
        Plot a particular point in the canvas.
        :param x: x position to plot
        :param y: y position to plot
        :param v: value scale of particular color (0-1)
        :param a: alpha to set for this particular plot if not self.alpha
        :return:
        """
        a = int(a) if a is not None else self._alpha
        if v is None:
            v = 1.0
        try:
            x += 1
            y += 1
            pos = (self.width * y) + x
            idx = pos * 4
            background_a = self.buf[idx + 3]

            # get rgb and check if close to black and make off dark gray
            # this makes black have highlights
            if self._distance_from_black < 15:
                r = 35
                g = 35
                b = 35
                r = r * v
                g = g * v
                b = b * v
                # end of check and make gray
            else:
                r = self._red * v
                g = self._green * v
                b = self._blue * v
            if 0 > r:
                r = 0
            if 0 > g:
                g = 0
            if 0 > b:
                b = 0
            if r > 255:
                r = 255
            if g > 255:
                g = 255
            if b > 255:
                b = 255
            if background_a != 0 and a != 255:
                s_alpha = a / 255.0
                s_background_a = background_a / 255.0
                one_minus_salpha = 1 - s_alpha

                background_r = self.buf[idx]
                background_g = self.buf[idx + 1]
                background_b = self.buf[idx + 2]
                r = r * s_alpha + one_minus_salpha * background_r
                g = g * s_alpha + one_minus_salpha * background_g
                b = b * s_alpha + one_minus_salpha * background_b
                a = (s_alpha + one_minus_salpha * s_background_a) * 255
            self.buf[idx] = int(r)
            self.buf[idx + 1] = int(g)
            self.buf[idx + 2] = int(b)
            self.buf[idx + 3] = (
                int(a) - 4
            )  # remove just a little opacity for background color tint show thru
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
        odx = abs(dx)
        ody = abs(dy)
        if dx < 0:
            dx = -dx
            step_x = -1
        else:
            step_x = 1
        i = 0
        if dx > dy:
            dy <<= 1  # dy is now 2*dy
            dx <<= 1
            fraction = dy - (dx >> 1)  # same as 2*dy - dx
            self.line_for_point(x0, y0, False, odx, i)
            i += 1

            while x0 != x1:
                if fraction >= 0:
                    y0 += step_y
                    fraction -= dx  # same as fraction -= 2*dx
                x0 += step_x
                fraction += dy  # same as fraction += 2*dy
                self.line_for_point(x0, y0, False, odx, i)
                i += 1
        else:
            dy <<= 1  # dy is now 2*dy
            dx <<= 1  # dx is now 2*dx
            fraction = dx - (dy >> 1)
            self.line_for_point(x0, y0, True, ody, i)
            i += 1
            while y0 != y1:
                if fraction >= 0:
                    x0 += step_x
                    fraction -= dy
                y0 += step_y
                fraction += dx
                self.line_for_point(x0, y0, True, ody, i)

    def line_for_point(self, x, y, dy, max_pos, index):
        w = self.line_width
        left = w >> 1
        right = w - left
        if self.fancy and max_pos > 0:
            v = self.gradient(index / max_pos)
        else:
            v = 1.0
        if dy:
            for pos in range(-left, right):
                self.plot(x + pos, y, v)
        else:
            for pos in range(-left, right):
                self.plot(x, y + pos, v)

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


def draw_guides(draw_buff, extends):
    width = int(extends[2] - extends[0])
    height = int(extends[3] - extends[1])
    draw_buff.set_color(0, 0, 0, 255)
    draw_buff.line_width = 1
    min_x = int(extends[0])
    min_y = int(extends[1])
    points = 50
    draw_buff.draw_text(0, 0, "mm")
    for x in range(points - (min_x % points), width - 30, points):
        if x < 30:
            continue
        draw_buff.draw_text(x, 0, str(int((x + min_x) / 10)), rotate=True)
        draw_buff.draw_line(x, 0, x, 30)
    for y in range(points - (min_y % points), height - 30, points):
        if y < 30:
            continue
        draw_buff.draw_text(0, y, str(int((y + min_y) / 10)))
        draw_buff.draw_line(0, y, 30, y)


def write(pattern, f, settings=None):
    guides = settings.get("guides", False)
    extends = pattern.bounds()
    pattern.translate(-extends[0], -extends[1])
    width = int(extends[2] - extends[0])
    height = int(extends[3] - extends[1])
    draw_buff = PngBuffer(width, height)
    draw_buff.fancy = settings.get("fancy", False)
    if settings is not None:
        background = settings.get("background")
        if background is not None:
            b = EmbThread()
            b.set(background)
            draw_buff.background(b.get_red(), b.get_green(), b.get_blue(), 0xFF)
        linewidth = settings.get("linewidth")
        if linewidth is not None and isinstance(linewidth, int):
            draw_buff.line_width = linewidth

    for stitchblock in pattern.get_as_stitchblock():
        block = stitchblock[0]
        thread = stitchblock[1]
        draw_buff.set_color(
            thread.get_red(), thread.get_green(), thread.get_blue(), 255
        )
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
        draw_guides(draw_buff, extends)

    f.write(write_png(draw_buff.buf, draw_buff.width, draw_buff.height))
