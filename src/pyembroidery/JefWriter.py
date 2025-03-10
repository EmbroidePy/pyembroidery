import datetime

from .EmbConstant import *
from .EmbThreadJef import get_thread_set
from .WriteHelper import write_int_8, write_int_32le, write_string_utf8

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_JUMP
FULL_JUMP = True
ROUND = True
MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127

# These are in mm, embroidery units are 1/10 mm
HOOP_110X110 = 0
HOOP_50X50 = 1
HOOP_140X200 = 2
HOOP_126X110 = 3
HOOP_200X200 = 4


def write(pattern, f, settings=None):
    trims = False
    command_count_max = 3

    date_string = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    if settings is not None:
        trims = settings.get("trims", trims)
        command_count_max = settings.get("trim_at", command_count_max)
        date_string = settings.get("date", date_string)

    pattern.fix_color_count()
    # REMOVE BUG: color_count = pattern.count_threads(). #

    # PATCH
    jef_threads = get_thread_set()
    last_index = None
    last_thread = None
    palette = []
    color_toggled = False
    color_count = 0  # Color and Stop count.
    index_in_threadlist = 0
    for stitch in pattern.stitches:
        # Iterate all stitches.
        flags = stitch[2] & COMMAND_MASK
        if flags == COLOR_CHANGE or index_in_threadlist == 0:
            # If color change *or* initial color unset.
            thread = pattern.threadlist[index_in_threadlist]
            index_in_threadlist += 1
            color_count += 1
            index_of_jefthread = thread.find_nearest_color_index(jef_threads)
            if last_index == index_of_jefthread and last_thread != thread:
                # Last thread and current thread pigeonhole to same jefcolor.
                # We set that thread to None. And get the second closest color.
                repeated_thread = jef_threads[index_of_jefthread]
                repeated_index = index_of_jefthread
                jef_threads[index_of_jefthread] = None
                index_of_jefthread = thread.find_nearest_color_index(jef_threads)
                jef_threads[repeated_index] = repeated_thread
            palette.append(index_of_jefthread)
            last_index = index_of_jefthread
            last_thread = thread
            color_toggled = False
        if flags == STOP:
            color_count += 1
            color_toggled = not color_toggled
            if color_toggled:
                palette.append(0)
            else:
                palette.append(last_index)
    # END PATCH

    offsets = 0x74 + (color_count * 8)
    write_int_32le(f, offsets)
    write_int_32le(f, 0x14)
    write_string_utf8(f, date_string)
    write_int_8(f, 0)
    write_int_8(f, 0)
    write_int_32le(f, color_count)
    point_count = 1  # 1 command for END statement
    for stitch in pattern.stitches:
        data = stitch[2] & COMMAND_MASK
        if data == STITCH:
            point_count += 1
        elif data == JUMP:
            point_count += 2
        elif data == TRIM:
            if trims:
                point_count += 2 * command_count_max
        elif data == COLOR_CHANGE or data == STOP:  # PATCH: INCLUDE STOP.
            point_count += 2
        elif data == END:
            break
    write_int_32le(f, point_count)
    extends = pattern.bounds()
    design_width = int(round(extends[2] - extends[0]))
    design_height = int(round(extends[3] - extends[1]))
    write_int_32le(f, get_jef_hoop_size(design_width, design_height))
    half_width = int(round(design_width / 2))
    half_height = int(round(design_height / 2))

    # distance from center of hoop.
    write_int_32le(f, half_width)
    write_int_32le(f, half_height)
    write_int_32le(f, half_width)
    write_int_32le(f, half_height)

    # distance from default 110 x 110 hoop
    x_hoop_edge = 550 - half_width
    y_hoop_edge = 550 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    # distance from default 50 x 50 hoop
    x_hoop_edge = 250 - half_width
    y_hoop_edge = 250 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    # distance from default 140 x 200 hoop
    x_hoop_edge = 700 - half_width
    y_hoop_edge = 1000 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    # distance from custom hoop, but this should be accepted.
    x_hoop_edge = 700 - half_width
    y_hoop_edge = 1000 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    # REMOVE (We covered this in PATCH).
    #jef_threads = get_thread_set()
    #
    #palette = build_nonrepeat_palette(jef_threads, pattern.threadlist)
    # END REMOVE

    for t in palette:
        write_int_32le(f, t)

    for i in range(0, color_count):
        write_int_32le(f, 0x0D)

    xx = 0
    yy = 0
    for stitch in pattern.stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2] & COMMAND_MASK
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if data == STITCH:
            write_int_8(f, dx)
            write_int_8(f, -dy)
            continue
        elif data == COLOR_CHANGE or data == STOP:  # PATCH INCLUDE STOP.
            f.write(b"\x80\x01")
            write_int_8(f, dx)
            write_int_8(f, -dy)
            continue
        elif data == TRIM:
            if trims:  # command trim.
                f.write(b"\x80\x02\x00\x00" * command_count_max)
            continue
        elif data == JUMP:
            f.write(b"\x80\x02")
            write_int_8(f, dx)
            write_int_8(f, -dy)
            continue
        elif data == END:
            break
    f.write(b"\x80\x10")


def get_jef_hoop_size(width, height):
    if width < 500 and height < 500:
        return HOOP_50X50
    if width < 1260 and height < 1100:
        return HOOP_126X110
    if width < 1400 and height < 2000:
        return HOOP_140X200
    if width < 2000 and height < 2000:
        return HOOP_200X200
    return HOOP_110X110


def write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge):
    if min(x_hoop_edge, y_hoop_edge) >= 0:
        write_int_32le(f, x_hoop_edge)  # left
        write_int_32le(f, y_hoop_edge)  # top
        write_int_32le(f, x_hoop_edge)  # right
        write_int_32le(f, y_hoop_edge)  # bottom
    else:
        write_int_32le(f, -1)
        write_int_32le(f, -1)
        write_int_32le(f, -1)
        write_int_32le(f, -1)
