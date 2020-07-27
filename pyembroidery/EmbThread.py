
def build_unique_palette(thread_palette, threadlist):
    """Turns a threadlist into a unique index list with the thread palette"""
    chart = [None] * len(thread_palette)  # Create a lookup chart.
    for thread in set(threadlist):  # for each unique color, move closest remaining thread to lookup chart.
        index = thread.find_nearest_color_index(thread_palette)
        if index is None:
            break  # No more threads remain in palette
        thread_palette[index] = None  # entries may not be reused.
        chart[index] = thread  # assign the given index to the lookup.

    palette = []
    for thread in threadlist:  # for each thread, return the index.
        palette.append(thread.find_nearest_color_index(chart))
    return palette


def build_palette(thread_palette, threadlist):
    palette = []
    for thread in threadlist:  # for each thread, return the index.
        palette.append(thread.find_nearest_color_index(thread_palette))
    return palette


def build_nonrepeat_palette(thread_palette, threadlist):
    last_index = None
    last_thread = None
    palette = []
    for thread in threadlist:  # for each thread, return the index.
        index = thread.find_nearest_color_index(thread_palette)
        if last_index == index and last_thread != thread:
            repeated_thread = thread_palette[index]
            repeated_index = index
            thread_palette[index] = None
            index = thread.find_nearest_color_index(thread_palette)
            # index will no longer be repeated.
            thread_palette[repeated_index] = repeated_thread
        palette.append(index)
        last_index = index
        last_thread = thread

    return palette


def find_nearest_color_index(find_color, values):
    if isinstance(find_color, EmbThread):
        find_color = find_color.color
    red = (find_color >> 16) & 0xff
    green = (find_color >> 8) & 0xff
    blue = find_color & 0xff
    closest_index = None
    current_closest_value = float("inf")
    for current_index, t in enumerate(values):
        if t is None:
            continue
        dist = color_distance_red_mean(
            red,
            green,
            blue,
            t.get_red(),
            t.get_green(),
            t.get_blue())
        if dist <= current_closest_value:  # <= choose second if they tie.
            current_closest_value = dist
            closest_index = current_index
    return closest_index


def color_rgb(r, g, b):
    return int(((r & 255) << 16) |
               ((g & 255) << 8) |
               (b & 255))


def color_hex(hex_string):
    h = hex_string.lstrip('#')
    size = len(h)
    if size == 6 or size == 8:
        return int(h[:6], 16)
    elif size == 4 or size == 3:
        return int(h[0] + h[0] + h[1] + h[1] + h[2] + h[2], 16)


def color_distance_red_mean(
        r1, g1, b1,
        r2, g2, b2):
    red_mean = int(round((r1 + r2) / 2))
    r = int(r1 - r2)
    g = int(g1 - g2)
    b = int(b1 - b2)
    return (((512 + red_mean) * r * r) >> 8) + 4 * g * g + \
           (((767 - red_mean) * b * b) >> 8)
    # See the very good color distance paper:
    # https://www.compuphase.com/cmetric.htm


class EmbThread:

    def __init__(self, thread=None, description=None, catalog_number=None, details=None, brand=None, chart=None, weight=None):
        self.color = 0x000000
        self.description = description  # type: str
        self.catalog_number = catalog_number  # type: str
        self.details = details  # type: str
        self.brand = brand  # type: str
        self.chart = chart  # type: str
        self.weight = weight  # type: str
        # description, catalog_number, details, brand, chart, weight
        if thread is not None:
            self.set(thread)

    def __repr__(self):
        parts = list()
        parts.append("thread='%s'" % self.hex_color())
        if self.description is not None:
            parts.append("description='%s'" % self.description)
        if self.catalog_number is not None:
            parts.append("catalog_number='%s'" % self.catalog_number)
        if self.details is not None:
            parts.append("details='%s'" % self.details)
        if self.brand is not None:
            parts.append("brand='%s'" % self.brand)
        if self.chart is not None:
            parts.append("chart='%s'" % self.chart)
        if self.weight is not None:
            parts.append("weight='%s'" % self.weight)
        return "EmbThread(%s)" % ", ".join(parts)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, int):
            return self.color & 0xFFFFFF == other & 0xFFFFFF
        try:
            if isinstance(other, basestring):
                return self.color & 0xFFFFFF == EmbThread.parse_string_color(other) & 0xFFFFFF
        except NameError:
            if isinstance(other, str):
                return self.color & 0xFFFFFF == EmbThread.parse_string_color(other) & 0xFFFFFF
        if not isinstance(other, EmbThread):
            return False
        if self.color & 0xFFFFFF != other.color & 0xFFFFFF:
            return False
        if self.description != other.description:
            return False
        if self.catalog_number != other.catalog_number:
            return False
        if self.details != other.details:
            return False
        if self.brand != other.brand:
            return False
        if self.chart != other.chart:
            return False
        if self.weight != other.weight:
            return False
        return True

    def __hash__(self):
        return self.color & 0xFFFFFF

    def __str__(self):
        if self.description is None:
            return "EmbThread %s" % self.hex_color()
        else:
            return "EmbThread %s %s" % (self.description, self.hex_color())

    def set_color(self, r, g, b):
        self.color = color_rgb(r, g, b)

    def get_opaque_color(self):
        return 0xFF000000 | self.color

    def get_red(self):
        red = self.color >> 16
        return red & 0xFF

    def get_green(self):
        green = self.color >> 8
        return green & 0xFF

    def get_blue(self):
        blue = self.color
        return blue & 0xFF

    def find_nearest_color_index(self, values):
        return find_nearest_color_index(int(self.color), values)

    def hex_color(self):
        return "#%02x%02x%02x" % (
            self.get_red(), self.get_green(), self.get_blue()
        )

    def set_hex_color(self, hex_string):
        self.color = color_hex(hex_string)

    def set(self, thread):
        if isinstance(thread, EmbThread):
            self.color = thread.color
            self.description = thread.description
            self.catalog_number = thread.catalog_number
            self.details = thread.details
            self.brand = thread.brand
            self.chart = thread.chart
            self.weight = thread.weight
        elif isinstance(thread, int):
            self.color = thread
        elif isinstance(thread, dict):
            if "name" in thread:
                self.description = thread["name"]
            if "description" in thread:
                self.description = thread["description"]
            if "desc" in thread:
                self.description = thread["desc"]
            if "brand" in thread:
                self.brand = thread["brand"]
            if "manufacturer" in thread:
                self.brand = thread["manufacturer"]
            if "color" in thread or "rgb" in thread:
                try:
                    color = thread["color"]
                except KeyError:
                    color = thread["rgb"]
                if isinstance(color, int):
                    self.color = color
                elif isinstance(color, tuple) or isinstance(color, list):
                    self.color = (color[0] & 0xFF) << 16 | \
                                 (color[1] & 0xFF) << 8 | \
                                 (color[2] & 0xFF)
                else:
                    try:
                        if isinstance(color, basestring):
                            self.color = self.parse_string_color(color)
                    except NameError:
                        if isinstance(color, str):
                            self.color = self.parse_string_color(color)
            if "hex" in thread:
                self.set_hex_color(thread["hex"])
            if "id" in thread:
                self.catalog_number = thread["id"]
            if "catalog" in thread:
                self.catalog_number = thread["catalog"]
        else:
            try:
                if isinstance(thread, basestring):
                    self.color = self.parse_string_color(thread)
            except NameError:
                if isinstance(thread, str):
                    self.color = self.parse_string_color(thread)
            try:  # We might be using python 3.
                if isinstance(thread, long):
                    self.color = int(thread)
            except NameError:
                pass

    @staticmethod
    def parse_string_color(color):
        if color == "random":
            import random
            return random.randint(0, 0xFFFFFF)
        if color[0:1] == "#":
            return color_hex(color[1:])
        color_dict = {
            "aliceblue": color_rgb(240, 248, 255),
            "antiquewhite": color_rgb(250, 235, 215),
            "aqua": color_rgb(0, 255, 255),
            "aquamarine": color_rgb(127, 255, 212),
            "azure": color_rgb(240, 255, 255),
            "beige": color_rgb(245, 245, 220),
            "bisque": color_rgb(255, 228, 196),
            "black": color_rgb(0, 0, 0),
            "blanchedalmond": color_rgb(255, 235, 205),
            "blue": color_rgb(0, 0, 255),
            "blueviolet": color_rgb(138, 43, 226),
            "brown": color_rgb(165, 42, 42),
            "burlywood": color_rgb(222, 184, 135),
            "cadetblue": color_rgb(95, 158, 160),
            "chartreuse": color_rgb(127, 255, 0),
            "chocolate": color_rgb(210, 105, 30),
            "coral": color_rgb(255, 127, 80),
            "cornflowerblue": color_rgb(100, 149, 237),
            "cornsilk": color_rgb(255, 248, 220),
            "crimson": color_rgb(220, 20, 60),
            "cyan": color_rgb(0, 255, 255),
            "darkblue": color_rgb(0, 0, 139),
            "darkcyan": color_rgb(0, 139, 139),
            "darkgoldenrod": color_rgb(184, 134, 11),
            "darkgray": color_rgb(169, 169, 169),
            "darkgreen": color_rgb(0, 100, 0),
            "darkgrey": color_rgb(169, 169, 169),
            "darkkhaki": color_rgb(189, 183, 107),
            "darkmagenta": color_rgb(139, 0, 139),
            "darkolivegreen": color_rgb(85, 107, 47),
            "darkorange": color_rgb(255, 140, 0),
            "darkorchid": color_rgb(153, 50, 204),
            "darkred": color_rgb(139, 0, 0),
            "darksalmon": color_rgb(233, 150, 122),
            "darkseagreen": color_rgb(143, 188, 143),
            "darkslateblue": color_rgb(72, 61, 139),
            "darkslategray": color_rgb(47, 79, 79),
            "darkslategrey": color_rgb(47, 79, 79),
            "darkturquoise": color_rgb(0, 206, 209),
            "darkviolet": color_rgb(148, 0, 211),
            "deeppink": color_rgb(255, 20, 147),
            "deepskyblue": color_rgb(0, 191, 255),
            "dimgray": color_rgb(105, 105, 105),
            "dimgrey": color_rgb(105, 105, 105),
            "dodgerblue": color_rgb(30, 144, 255),
            "firebrick": color_rgb(178, 34, 34),
            "floralwhite": color_rgb(255, 250, 240),
            "forestgreen": color_rgb(34, 139, 34),
            "fuchsia": color_rgb(255, 0, 255),
            "gainsboro": color_rgb(220, 220, 220),
            "ghostwhite": color_rgb(248, 248, 255),
            "gold": color_rgb(255, 215, 0),
            "goldenrod": color_rgb(218, 165, 32),
            "gray": color_rgb(128, 128, 128),
            "grey": color_rgb(128, 128, 128),
            "green": color_rgb(0, 128, 0),
            "greenyellow": color_rgb(173, 255, 47),
            "honeydew": color_rgb(240, 255, 240),
            "hotpink": color_rgb(255, 105, 180),
            "indianred": color_rgb(205, 92, 92),
            "indigo": color_rgb(75, 0, 130),
            "ivory": color_rgb(255, 255, 240),
            "khaki": color_rgb(240, 230, 140),
            "lavender": color_rgb(230, 230, 250),
            "lavenderblush": color_rgb(255, 240, 245),
            "lawngreen": color_rgb(124, 252, 0),
            "lemonchiffon": color_rgb(255, 250, 205),
            "lightblue": color_rgb(173, 216, 230),
            "lightcoral": color_rgb(240, 128, 128),
            "lightcyan": color_rgb(224, 255, 255),
            "lightgoldenrodyellow": color_rgb(250, 250, 210),
            "lightgray": color_rgb(211, 211, 211),
            "lightgreen": color_rgb(144, 238, 144),
            "lightgrey": color_rgb(211, 211, 211),
            "lightpink": color_rgb(255, 182, 193),
            "lightsalmon": color_rgb(255, 160, 122),
            "lightseagreen": color_rgb(32, 178, 170),
            "lightskyblue": color_rgb(135, 206, 250),
            "lightslategray": color_rgb(119, 136, 153),
            "lightslategrey": color_rgb(119, 136, 153),
            "lightsteelblue": color_rgb(176, 196, 222),
            "lightyellow": color_rgb(255, 255, 224),
            "lime": color_rgb(0, 255, 0),
            "limegreen": color_rgb(50, 205, 50),
            "linen": color_rgb(250, 240, 230),
            "magenta": color_rgb(255, 0, 255),
            "maroon": color_rgb(128, 0, 0),
            "mediumaquamarine": color_rgb(102, 205, 170),
            "mediumblue": color_rgb(0, 0, 205),
            "mediumorchid": color_rgb(186, 85, 211),
            "mediumpurple": color_rgb(147, 112, 219),
            "mediumseagreen": color_rgb(60, 179, 113),
            "mediumslateblue": color_rgb(123, 104, 238),
            "mediumspringgreen": color_rgb(0, 250, 154),
            "mediumturquoise": color_rgb(72, 209, 204),
            "mediumvioletred": color_rgb(199, 21, 133),
            "midnightblue": color_rgb(25, 25, 112),
            "mintcream": color_rgb(245, 255, 250),
            "mistyrose": color_rgb(255, 228, 225),
            "moccasin": color_rgb(255, 228, 181),
            "navajowhite": color_rgb(255, 222, 173),
            "navy": color_rgb(0, 0, 128),
            "oldlace": color_rgb(253, 245, 230),
            "olive": color_rgb(128, 128, 0),
            "olivedrab": color_rgb(107, 142, 35),
            "orange": color_rgb(255, 165, 0),
            "orangered": color_rgb(255, 69, 0),
            "orchid": color_rgb(218, 112, 214),
            "palegoldenrod": color_rgb(238, 232, 170),
            "palegreen": color_rgb(152, 251, 152),
            "paleturquoise": color_rgb(175, 238, 238),
            "palevioletred": color_rgb(219, 112, 147),
            "papayawhip": color_rgb(255, 239, 213),
            "peachpuff": color_rgb(255, 218, 185),
            "peru": color_rgb(205, 133, 63),
            "pink": color_rgb(255, 192, 203),
            "plum": color_rgb(221, 160, 221),
            "powderblue": color_rgb(176, 224, 230),
            "purple": color_rgb(128, 0, 128),
            "red": color_rgb(255, 0, 0),
            "rosybrown": color_rgb(188, 143, 143),
            "royalblue": color_rgb(65, 105, 225),
            "saddlebrown": color_rgb(139, 69, 19),
            "salmon": color_rgb(250, 128, 114),
            "sandybrown": color_rgb(244, 164, 96),
            "seagreen": color_rgb(46, 139, 87),
            "seashell": color_rgb(255, 245, 238),
            "sienna": color_rgb(160, 82, 45),
            "silver": color_rgb(192, 192, 192),
            "skyblue": color_rgb(135, 206, 235),
            "slateblue": color_rgb(106, 90, 205),
            "slategray": color_rgb(112, 128, 144),
            "slategrey": color_rgb(112, 128, 144),
            "snow": color_rgb(255, 250, 250),
            "springgreen": color_rgb(0, 255, 127),
            "steelblue": color_rgb(70, 130, 180),
            "tan": color_rgb(210, 180, 140),
            "teal": color_rgb(0, 128, 128),
            "thistle": color_rgb(216, 191, 216),
            "tomato": color_rgb(255, 99, 71),
            "turquoise": color_rgb(64, 224, 208),
            "violet": color_rgb(238, 130, 238),
            "wheat": color_rgb(245, 222, 179),
            "white": color_rgb(255, 255, 255),
            "whitesmoke": color_rgb(245, 245, 245),
            "yellow": color_rgb(255, 255, 0),
            "yellowgreen": color_rgb(154, 205, 50)
        }
        return color_dict.get(color.lower(), 0x000000)
        # return color or black.
