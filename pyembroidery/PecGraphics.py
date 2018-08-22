from math import floor

blank = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0xF0, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x10,
    0x04, 0x00, 0x00, 0x00, 0x00, 0x20,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x04, 0x00, 0x00, 0x00, 0x00, 0x20,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x10,
    0xF0, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]


def get_blank():
    return [m for m in blank]


def create(width, height):
    width /= 8
    return [0x00] * width * height


def draw(points, graphic, stride=6):
    for point in points:
        try:
            try:
                graphic_mark_bit(graphic,
                                 int(point.x),
                                 int(point.y),
                                 stride)
            except AttributeError:
                graphic_mark_bit(graphic,
                                 int(point[0]),
                                 int(point[1]),
                                 stride)
        except IndexError:
            pass


def draw_scaled(extends, points, graphic, stride, buffer=5):
    if extends is None:
        draw(points, graphic, stride)
        return
    try:
        left = extends.left
        top = extends.top
        right = extends.right
        bottom = extends.bottom
    except AttributeError:
        left = extends[0]
        top = extends[1]
        right = extends[2]
        bottom = extends[3]

    diagram_width = right - left
    diagram_height = bottom - top

    graphic_width = stride * 8
    graphic_height = len(graphic) / stride

    if diagram_width == 0:
        diagram_width = 1
    if diagram_height == 0:
        diagram_height = 1

    scale_x = (graphic_width - buffer) / float(diagram_width)
    scale_y = (graphic_height - buffer) / float(diagram_height)

    scale = min(scale_x, scale_y)

    cx = (right + left) / 2
    cy = (bottom + top) / 2

    translate_x = -cx
    translate_y = -cy

    translate_x *= scale
    translate_y *= scale

    translate_x += graphic_width / 2
    translate_y += graphic_height / 2

    for point in points:
        try:
            try:
                graphic_mark_bit(graphic,
                                 int(floor((point.x * scale) + translate_x)),
                                 int(floor((point.y * scale) + translate_y)),
                                 stride)
            except AttributeError:
                graphic_mark_bit(graphic,
                                 int(floor((point[0] * scale) + translate_x)),
                                 int(floor((point[1] * scale) + translate_y)),
                                 stride)
        except IndexError:
            pass


def clear(graphic):
    for b in graphic:
        b = 0


def graphic_mark_bit(graphic, x, y, stride=6):
    """expressly sets the bit in the give graphic object"""
    graphic[(y * stride) + int(x / 8)] |= 1 << (x % 8)


def graphic_unmark_bit(graphic, x, y, stride=6):
    """expressly unsets the bit in the give graphic object"""
    graphic[(y * stride) + int(x / 8)] &= ~(1 << (x % 8))


def get_graphic_as_string(graphic, one="#", zero=" "):
    """Prints graphic object in text."""
    stride = 6
    if isinstance(graphic, tuple):
        stride = graphic[1]
        graphic = graphic[0]

    if isinstance(graphic, str):
        graphic = bytearray(graphic)

    list_string = [
        one if (byte >> i) & 1 else zero
        for byte in graphic
        for i in range(0, 8)
    ]
    bit_stride = 8 * stride
    bit_length = 8 * len(graphic)
    return '\n'.join(
        ''.join(list_string[m:m + bit_stride])
        for m in range(0, bit_length, bit_stride))
