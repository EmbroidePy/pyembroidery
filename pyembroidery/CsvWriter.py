import math

from .EmbFunctions import *
from .PecGraphics import get_graphic_as_string
from .WriteHelper import write_string_utf8

ENCODE = False
WRITES_SPEEDS = True
SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_UTILIZE


def csv(f, values):
    string = ""
    for v in values:
        if len(string) > 0:
            string += ","
        string += '"%s"' % v
    write_string_utf8(f, string + "\n")


def distance(dx, dy):
    dx *= dx
    dy *= dy
    return math.sqrt(dx + dy)


def angle(dx, dy):
    tau = math.pi * 2
    angle = math.atan2(dy, dx)
    angle += tau / float(2)
    angle /= tau
    return angle


def write_data(pattern, f):
    names = get_common_name_dictionary()
    extends = pattern.bounds()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    csv(f, ("#", "[VAR_NAME]", "[VAR_VALUE]"))
    count_stitches = pattern.count_stitches()
    csv(f, (">", "STITCH_COUNT:", str(count_stitches)))
    count_threads = pattern.count_color_changes()
    csv(f, (">", "THREAD_COUNT:", str(count_threads)))
    count_set_needles = pattern.count_needle_sets()
    csv(f, (">", "NEEDLE_COUNT:", str(count_set_needles)))
    csv(f, (">", "EXTENTS_LEFT:", str(extends[0])))
    csv(f, (">", "EXTENTS_TOP:", str(extends[1])))
    csv(f, (">", "EXTENTS_RIGHT:", str(extends[2])))
    csv(f, (">", "EXTENTS_BOTTOM:", str(extends[3])))
    csv(f, (">", "EXTENTS_WIDTH:", str(width)))
    csv(f, (">", "EXTENTS_HEIGHT:", str(height)))

    stitch_counts = {}
    for s in pattern.stitches:
        command = s[2] & COMMAND_MASK
        if command in stitch_counts:
            stitch_counts[command] += 1
        else:
            stitch_counts[command] = 1

    if len(stitch_counts) != 0:
        for the_key, the_value in stitch_counts.items():
            try:
                the_key &= COMMAND_MASK
                name = "COMMAND_" + names[the_key]
            except (IndexError, KeyError):
                name = "COMMAND_UNKNOWN_" + str(the_key)
            csv(f, (">", name, str(the_value)))

    write_string_utf8(f, "\n")


def write_metadata(pattern, f):
    if len(pattern.extras) > 0:
        csv(f, ("#", "[METADATA_NAME]", "[METADATA]"))
        for the_key, the_value in pattern.extras.items():
            if isinstance(the_value, tuple):
                the_value = "\n" + get_graphic_as_string(the_value)
            csv(f, ("@", str(the_key), str(the_value)))
        write_string_utf8(f, "\n")


def write_threads(pattern, f):
    if len(pattern.threadlist) > 0:
        csv(
            f,
            (
                "#",
                "[THREAD_NUMBER]",
                "[HEX_COLOR]",
                "[DESCRIPTION]",
                "[BRAND]",
                "[CATALOG_NUMBER]",
                "[DETAILS]",
                "[WEIGHT]",
            ),
        )
        for i, thread in enumerate(pattern.threadlist):
            csv(
                f,
                (
                    "$",
                    str(i),
                    thread.hex_color(),
                    thread.description,
                    thread.brand,
                    thread.catalog_number,
                    thread.details,
                    thread.weight,
                ),
            )
        write_string_utf8(f, "\n")


def decoded_name(names, data):
    command = decode_embroidery_command(data)
    try:
        name = names[command[0]]
        if command[1] is not None:
            name = name + " t" + str(command[1])
        if command[2] is not None:
            name = name + " n" + str(command[2])
        if command[3] is not None:
            name = name + " o" + str(command[3])
    except (IndexError, KeyError):
        name = "UNKNOWN " + str(data)
    return name


def write_stitches_displacement(pattern, f):
    names = get_common_name_dictionary()
    csv(
        f,
        (
            "#",
            "[STITCH_INDEX]",
            "[STITCH_TYPE]",
            "[X]",
            "[Y]",
            "[DX]",
            "[DY]",
            "[R]",
            "[ANGLE]",
        ),
    )

    current_x = 0
    current_y = 0
    for i, stitch in enumerate(pattern.stitches):
        name = decoded_name(names, stitch[2])
        dx = stitch[0] - current_x
        dy = stitch[1] - current_y
        csv(
            f,
            (
                "*",
                str(i),
                name,
                str(stitch[0]),
                str(stitch[1]),
                str(dx),
                str(dy),
                str(distance(dx, dy)),
                str(angle(dx, dy)),
            ),
        )
        current_x = stitch[0]
        current_y = stitch[1]


def write_stitches_deltas(pattern, f):
    names = get_common_name_dictionary()
    csv(f, ("#", "[STITCH_INDEX]", "[STITCH_TYPE]", "[X]", "[Y]", "[DX]", "[DY]"))
    current_x = 0
    current_y = 0
    for i, stitch in enumerate(pattern.stitches):
        name = decoded_name(names, stitch[2])
        dx = stitch[0] - current_x
        dy = stitch[1] - current_y
        csv(f, ("*", str(i), name, str(stitch[0]), str(stitch[1]), str(dx), str(dy)))
        current_x = stitch[0]
        current_y = stitch[1]


def write_stitches(pattern, f):
    names = get_common_name_dictionary()
    csv(f, ("#", "[STITCH_INDEX]", "[STITCH_TYPE]", "[X]", "[Y]"))
    for i, stitch in enumerate(pattern.stitches):
        name = decoded_name(names, stitch[2])
        csv(
            f,
            (
                "*",
                str(i),
                name,
                str(stitch[0]),
                str(stitch[1]),
            ),
        )


def write(pattern, f, settings=None):
    version = "default"
    if settings is not None:
        if "deltas" in settings:
            version = "delta"
        elif "displacement" in settings:
            version = "full"
        version = settings.get("version", version)
    write_data(pattern, f)
    write_metadata(pattern, f)
    write_threads(pattern, f)

    if len(pattern.stitches) > 0:
        if version == "full":
            write_stitches_displacement(pattern, f)
        elif version == "delta":
            write_stitches_deltas(pattern, f)
        else:
            write_stitches(pattern, f)
