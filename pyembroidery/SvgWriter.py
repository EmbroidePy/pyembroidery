from xml.etree.cElementTree import Element, ElementTree, SubElement

from .EmbConstant import CONTINGENCY_SEQUIN_STITCH

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
# technically I could use svg to draw a sequin as a 2 element circle path.
FULL_JUMP = False  # just drops all jumps anyway.
MAX_JUMP_DISTANCE = float('inf')
MAX_STITCH_DISTANCE = float('inf')

NAME_SVG = "svg"
ATTR_VERSION = "version"
VALUE_SVG_VERSION = "1.1"
ATTR_XMLNS = "xmlns"
VALUE_XMLNS = "http://www.w3.org/2000/svg"
ATTR_XMLNS_LINK = "xmlns:xlink"
VALUE_XLINK = "http://www.w3.org/1999/xlink"
ATTR_XMLNS_EV = "xmlns:ev"
VALUE_XMLNS_EV = "http://www.w3.org/2001/xml-events"
ATTR_WIDTH = "width"
ATTR_HEIGHT = "height"
ATTR_VIEWBOX = "viewBox"
NAME_PATH = "path"
ATTR_DATA = "d"
ATTR_FILL = "fill"
ATTR_STROKE = "stroke"
ATTR_STROKE_WIDTH = "stroke-width"
VALUE_NONE = "none"


def create_svg_dom(pattern):
    root = Element(NAME_SVG)
    root.set(ATTR_VERSION, VALUE_SVG_VERSION)
    root.set(ATTR_XMLNS, VALUE_XMLNS)
    root.set(ATTR_XMLNS_LINK, VALUE_XLINK)
    root.set(ATTR_XMLNS_EV, VALUE_XMLNS_EV)
    extends = pattern.bounds()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]
    root.set(ATTR_WIDTH, str(width))
    root.set(ATTR_HEIGHT, str(height))
    viewbox = \
        str(extends[0]) + " " + \
        str(extends[1]) + " " + \
        str(width) + " " + \
        str(height)
    root.set(ATTR_VIEWBOX, viewbox)

    for stitchblock in pattern.get_as_stitchblock():
        block = stitchblock[0]
        thread = stitchblock[1]
        path = SubElement(root, NAME_PATH)
        data = "M"
        for stitch in block:
            x = stitch[0]
            y = stitch[1]
            data += " " + str(x) + "," + str(y)
        path.set(ATTR_DATA, data)
        path.set(ATTR_FILL, VALUE_NONE)
        path.set(ATTR_STROKE, thread.hex_color())
        path.set(ATTR_STROKE_WIDTH, "3")
    return ElementTree(root)


def write(pattern, f, settings=None):
    """Writes an svg file of the stitchblocks."""
    tree = create_svg_dom(pattern)
    tree.write(f)
