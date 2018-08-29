def find_nearest_color_index(find_color, values):
    if isinstance(find_color, EmbThread):
        find_color = find_color.color
    red = (find_color >> 16) & 0xff
    green = (find_color >> 8) & 0xff
    blue = find_color & 0xff
    closest_index = -1
    current_index = -1
    current_closest_value = float("inf")
    for t in values:
        current_index += 1
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

    def __init__(self):
        self.color = 0xFF000000
        self.description = None  # type: str
        self.catalog_number = None  # type: str
        self.details = None  # type: str
        self.brand = None  # type: str
        self.chart = None  # type: str
        self.weight = None  # type: str
        # description, catalog_number, details, brand, chart, weight

    def set_color(self, r, g, b):
        self.color = 0xFF000000 | (
                (r & 255) << 16) | (
                             (g & 255) << 8) | (
                             b & 255)

    def get_opaque_color(self):
        return 0xFF000000 | self.color

    def get_red(self):
        return (self.color >> 16) & 0xFF

    def get_green(self):
        return (self.color >> 8) & 0xFF

    def get_blue(self):
        return self.color & 0xFF

    def find_nearest_color_index(self, values):
        return find_nearest_color_index(self.color, values)

    def hex_color(self):
        return "#%02x%02x%02x" % (
            self.get_red(), self.get_green(), self.get_blue())

    def set_hex_color(self, hex_string):
        h = hex_string.lstrip('#')
        size = len(h)
        if size == 6 or size == 8:
            self.color = int(h[:6], 16)
        elif size == 4 or size == 3:
            self.color = int(h[2] + h[2] + h[1] + h[1] + h[0] + h[0], 16)

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
                elif isinstance(color, str):
                    if color == "random":
                        import random
                        self.color = 0xFF000000 | random.randint(0, 0xFFFFFF)
                    if color[0:1] == "#":
                        self.set_hex_color(color[1:])
                elif isinstance(color, tuple) or isinstance(color, list):
                    self.color = (color[0] & 0xFF) << 16 | \
                                 (color[1] & 0xFF) << 8 | \
                                 (color[2] & 0xFF)
            if "hex" in thread:
                self.set_hex_color(thread["hex"])
            if "id" in thread:
                self.catalog_number = thread["id"]
            if "catalog" in thread:
                self.catalog_number = thread["catalog"]
