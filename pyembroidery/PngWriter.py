import struct
import zlib
from math import sin, sqrt

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
        self.show_fabric = False
        self.render_3d = False
        self.needle_holes = False
        self._highlight_alpha = 30
        self._shadow_alpha = 68

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
        return max(v, 0.0)

    def background(self, red, green, blue, alpha):
        for i in range(0, len(self.buf), 4):
            self.buf[i] = red
            self.buf[i + 1] = green
            self.buf[i + 2] = blue
            self.buf[i + 3] = alpha

        if self.show_fabric:
            self.apply_fabric_texture(red, green, blue, alpha)

    def apply_fabric_texture(self, red, green, blue, alpha):
        weave = 7
        for y in range(self.height):
            for x in range(self.width):
                idx = ((self.width * y) + x) * 4
                warp = ((x % weave) == 0)
                weft = ((y % weave) == 0)
                micro = sin((x + y) * 0.35) * 2.5
                tone = micro
                if warp:
                    tone -= 11
                if weft:
                    tone += 7
                if warp and weft:
                    tone -= 3
                r = max(0, min(255, red + int(tone)))
                g = max(0, min(255, green + int(tone)))
                b = max(0, min(255, blue + int(tone / 2)))
                self.buf[idx] = r
                self.buf[idx + 1] = g
                self.buf[idx + 2] = b
                self.buf[idx + 3] = alpha

    def width_profile(self, pos, left, right):
        span = max((left + right) - 1, 1)
        center = span / 2.0
        distance = abs((pos + left) - center) / max(center, 1.0)
        return 0.84 + ((1.0 - distance) * 0.22)

    def needle_hole(self, x, y):
        if not self.render_3d or not self.needle_holes:
            return
        radius = max(1, self.line_width // 3)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if (dx * dx) + (dy * dy) > (radius * radius) + 1:
                    continue
                distance = sqrt((dx * dx) + (dy * dy))
                falloff = distance / float(radius + 1)
                self.plot(x + dx, y + dy, 0.45 + (falloff * 0.16), 82)

    def should_draw_needle_hole(self, prev_point, point, next_point):
        if not self.render_3d or not self.needle_holes:
            return False
        if prev_point is None or next_point is None:
            return True
        ax = point[0] - prev_point[0]
        ay = point[1] - prev_point[1]
        bx = next_point[0] - point[0]
        by = next_point[1] - point[1]
        len_a = abs(ax) + abs(ay)
        len_b = abs(bx) + abs(by)
        if len_a == 0 or len_b == 0:
            return False
        cross = abs((ax * by) - (ay * bx))
        dot = (ax * bx) + (ay * by)
        if dot < 0:
            return True
        return cross > max(8, (len_a + len_b) // 3)

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

    def draw_line(self, x0, y0, x1, y1, stitch_mode=False):
        start_x = x0
        start_y = y0
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
            self.line_for_point(x0, y0, False, odx, i, stitch_mode)
            i += 1

            while x0 != x1:
                if fraction >= 0:
                    y0 += step_y
                    fraction -= dx  # same as fraction -= 2*dx
                x0 += step_x
                fraction += dy  # same as fraction += 2*dy
                self.line_for_point(x0, y0, False, odx, i, stitch_mode)
                i += 1
        else:
            dy <<= 1  # dy is now 2*dy
            dx <<= 1  # dx is now 2*dx
            fraction = dx - (dy >> 1)
            self.line_for_point(x0, y0, True, ody, i, stitch_mode)
            i += 1
            while y0 != y1:
                if fraction >= 0:
                    x0 += step_x
                    fraction -= dy
                y0 += step_y
                fraction += dx
                self.line_for_point(x0, y0, True, ody, i, stitch_mode)
                i += 1

    def line_for_point(self, x, y, dy, max_pos, index, stitch_mode=False):
        w = self.line_width
        left = w >> 1
        right = w - left
        along = (index / float(max_pos)) if max_pos > 0 else 0.5
        if stitch_mode and self.render_3d:
            v = 1.0
        elif self.fancy and max_pos > 0:
            v = self.gradient(along)
        else:
            v = 1.0
        ridge = 1.0
        if stitch_mode and self.render_3d:
            ridge = 0.88 + (0.18 * (1.0 - abs(0.5 - along) * 2.0))
        if dy:
            for pos in range(-left, right):
                point_v = v * ridge
                if stitch_mode and self.render_3d:
                    point_v *= self.width_profile(pos, left, right)
                    self.plot(x + pos + 1, y + 1, point_v * 0.62, self._shadow_alpha)
                    self.plot(x + pos - 1, y - 1, point_v * 1.08, self._highlight_alpha)
                self.plot(x + pos, y, point_v)
        else:
            for pos in range(-left, right):
                point_v = v * ridge
                if stitch_mode and self.render_3d:
                    point_v *= self.width_profile(pos, left, right)
                    self.plot(x + 1, y + pos + 1, point_v * 0.62, self._shadow_alpha)
                    self.plot(x - 1, y + pos - 1, point_v * 1.08, self._highlight_alpha)
                self.plot(x, y + pos, point_v)

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
    settings = settings or {}
    guides = settings.get("guides", False)
    extends = pattern.bounds()
    pattern.translate(-extends[0], -extends[1])
    width = int(extends[2] - extends[0])
    height = int(extends[3] - extends[1])
    draw_buff = PngBuffer(width, height)
    draw_buff.render_3d = settings.get("3d", settings.get("depth", False))
    draw_buff.show_fabric = settings.get("fabric", draw_buff.render_3d)
    draw_buff.needle_holes = settings.get("needle_holes", draw_buff.render_3d)
    draw_buff.fancy = settings.get("fancy", draw_buff.render_3d)

    highlight_alpha = settings.get("highlight_alpha")
    if isinstance(highlight_alpha, int):
        draw_buff._highlight_alpha = max(0, min(255, highlight_alpha))

    shadow_alpha = settings.get("shadow_alpha")
    if isinstance(shadow_alpha, int):
        draw_buff._shadow_alpha = max(0, min(255, shadow_alpha))

    default_gradient = {
        "gradient_shade_ends": 0.48
        if draw_buff.render_3d
        else draw_buff._gradient_shade_ends,
        "gradient_shade_edge": 1.08
        if draw_buff.render_3d
        else draw_buff._gradient_shade_edge,
        "gradient_shade_center": 1.42
        if draw_buff.render_3d
        else draw_buff._gradient_shade_center,
        "gradient_color_position1": 0.22
        if draw_buff.render_3d
        else draw_buff._gradient_color_position1,
        "gradient_color_position2": 0.50
        if draw_buff.render_3d
        else draw_buff._gradient_color_position2,
        "gradient_color_position3": 0.78
        if draw_buff.render_3d
        else draw_buff._gradient_color_position3,
    }
    draw_buff.modify_gradient(
        gradient_shade_ends=settings.get(
            "gradient_shade_ends", default_gradient["gradient_shade_ends"]
        ),
        gradient_shade_edge=settings.get(
            "gradient_shade_edge", default_gradient["gradient_shade_edge"]
        ),
        gradient_shade_center=settings.get(
            "gradient_shade_center", default_gradient["gradient_shade_center"]
        ),
        gradient_color_position1=settings.get(
            "gradient_color_position1", default_gradient["gradient_color_position1"]
        ),
        gradient_color_position2=settings.get(
            "gradient_color_position2", default_gradient["gradient_color_position2"]
        ),
        gradient_color_position3=settings.get(
            "gradient_color_position3", default_gradient["gradient_color_position3"]
        ),
    )

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
        points = [(int(stitch[0]), int(stitch[1])) for stitch in block]
        for i, (x, y) in enumerate(points):
            if i > 0:
                last_x, last_y = points[i - 1]
                draw_buff.draw_line(last_x, last_y, x, y, stitch_mode=True)
            prev_point = points[i - 1] if i > 0 else None
            next_point = points[i + 1] if i + 1 < len(points) else None
            if draw_buff.should_draw_needle_hole(prev_point, (x, y), next_point):
                draw_buff.needle_hole(x, y)

    if guides:
        draw_guides(draw_buff, extends)

    f.write(write_png(draw_buff.buf, draw_buff.width, draw_buff.height))
