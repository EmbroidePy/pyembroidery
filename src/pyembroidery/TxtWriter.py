from .EmbFunctions import *
from .WriteHelper import write_string_utf8


def write_mimic(pattern, f):
    emb_mod_convert = {
        STITCH: 0,
        JUMP: 1,
        TRIM: 2,
        STOP: 4,
        COLOR_CHANGE: 4,
        NEEDLE_SET: 4,
        SEQUIN_MODE: 8,
        SEQUIN_EJECT: 8,
        END: 16,
        # define NORMAL              0 /* stitch to (xx, yy) */
        # define JUMP                1 /* move to(xx, yy) */
        # define TRIM                2 /* trim + move to(xx, yy) */
        # define STOP                4 /* pause machine for thread change */
        # define SEQUIN              8 /* sequin */
        # define END                 16 /* end of program */
    }
    color = 0
    for i, stitch in enumerate(pattern.stitches):
        xx = stitch[0]
        yy = stitch[1]
        flags = stitch[2]
        if (flags & COMMAND_MASK) == COLOR_CHANGE:
            color += 1
        flags = emb_mod_convert[(flags & COMMAND_MASK)]
        txt_line = "%.1f,%.1f color:%i flags:%s\n" % (
            xx / 10.0,
            yy / 10.0,
            color,
            flags,
        )
        write_string_utf8(f, txt_line)


def write_normal(pattern, f):
    names = get_common_name_dictionary()
    color_index = 0
    color = pattern.get_thread_or_filler(color_index).color
    for i, stitch in enumerate(pattern.stitches):
        xx = stitch[0]
        yy = stitch[1]
        flags = stitch[2] & COMMAND_MASK
        if (flags & COMMAND_MASK) == COLOR_CHANGE:
            color = pattern.get_thread_or_filler(color_index).color
        named_command = names[(flags & COMMAND_MASK)]
        txt_line = "%.1f,%.1f color:%i command:%s flags:%i\n" % (
            xx,
            yy,
            color,
            named_command,
            flags,
        )
        write_string_utf8(f, txt_line)


def write(pattern, f, settings=None):
    mimic = False
    if settings is not None:
        if "mimic" in settings:
            mimic = True
        version = settings.get("version", "default")
        if version != "default":
            mimic = True
    if mimic:
        write_mimic(pattern, f)
    else:
        write_normal(pattern, f)
