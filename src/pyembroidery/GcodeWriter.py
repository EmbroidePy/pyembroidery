from .EmbFunctions import *
from .WriteHelper import write_string_utf8

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
SCALE = (-1, -1)  # This performs a default X,Y flip.


def write_data(pattern, f):
    bounds = [float(e) / 10.0 for e in pattern.bounds()]  # convert to mm.
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    count_stitches = pattern.count_stitches()
    count_threads = pattern.count_color_changes()

    write_string_utf8(f, "(STITCH_COUNT: %d)\n" % count_stitches)
    write_string_utf8(f, "(THREAD_COUNT: %d)\n" % count_threads)
    write_string_utf8(f, "(EXTENTS_LEFT: %.3f)\n" % bounds[0])
    write_string_utf8(f, "(EXTENTS_TOP: %.3f)\n" % bounds[1])
    write_string_utf8(f, "(EXTENTS_RIGHT: %.3f)\n" % bounds[2])
    write_string_utf8(f, "(EXTENTS_BOTTOM: %.3f)\n" % bounds[3])
    write_string_utf8(f, "(EXTENTS_WIDTH: %.3f)\n" % width)
    write_string_utf8(f, "(EXTENTS_HEIGHT: %.3f)\n" % height)

    stitch_counts = {}
    for s in pattern.stitches:
        command = s[2] & COMMAND_MASK
        if command in stitch_counts:
            stitch_counts[command] += 1
        else:
            stitch_counts[command] = 1

    names = get_common_name_dictionary()
    if len(stitch_counts) != 0:
        for the_key, the_value in stitch_counts.items():
            try:
                the_key &= COMMAND_MASK
                name = "COMMAND_" + names[the_key]
            except (IndexError, KeyError):
                name = "COMMAND_UNKNOWN_" + str(the_key)
            write_string_utf8(f, "(%s: %d)\n" % (name, the_value))


def write_metadata(pattern, f):
    if len(pattern.extras) > 0:
        for the_key, the_value in pattern.extras.items():
            try:
                if isinstance(the_value, basestring):
                    write_string_utf8(f, "(%s: %s)\n" % (the_key, the_value))
            except NameError:
                if isinstance(the_value, str):
                    write_string_utf8(f, "(%s: %s)\n" % (the_key, the_value))


def write_threads(pattern, f):
    if len(pattern.threadlist) > 0:
        for i, thread in enumerate(pattern.threadlist):
            write_string_utf8(
                f,
                "(Thread%d: %s %s %s %s)\n"
                % (
                    i,
                    thread.hex_color(),
                    thread.description,
                    thread.brand,
                    thread.catalog_number,
                ),
            )


def write(pattern, f, settings=None):
    if settings is None:
        settings = {}
    increment_value = settings.get("stitch_z_travel", 10.0)
    write_data(pattern, f)
    write_metadata(pattern, f)
    write_threads(pattern, f)

    z = 0.0
    for i, stitch in enumerate(pattern.stitches):
        x = float(stitch[0]) / 10.0
        y = float(stitch[1]) / 10.0
        cmd = decode_embroidery_command(stitch[2])
        command = cmd[0]
        if command == STITCH:
            write_string_utf8(f, "G00 X%.3f Y%.3f\nG00 Z%.1f\n" % (x, y, z))
            z += increment_value
            continue
        elif command == JUMP:
            continue
        elif command == TRIM:
            continue
        elif command == COLOR_CHANGE:
            write_string_utf8(f, "M00\n")
            continue
        elif command == STOP:
            write_string_utf8(f, "M00\n")
            continue
        elif command == END:
            write_string_utf8(f, "M30\n")
            continue
        break  # Code shouldn't reach this point.
