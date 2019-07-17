from .EmbConstant import *
from .EmbThreadPec import get_thread_set
from .PecWriter import write_pec
from .WriteHelper import write_string_utf8, write_int_32le, write_int_24le, write_int_16le, write_int_8, \
    write_float_32le

SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_JUMP
FULL_JUMP = True
ROUND = True
MAX_JUMP_DISTANCE = 2047
MAX_STITCH_DISTANCE = 2047

VERSION_1 = 1.0
VERSION_6 = 6.0

PES_VERSION_1_SIGNATURE = "#PES0001"
PES_VERSION_6_SIGNATURE = "#PES0060"

EMB_ONE = "CEmbOne"
EMB_SEG = "CSewSeg"


def write(pattern, f, settings=None):
    pattern.fix_color_count()
    pattern.interpolate_stop_as_duplicate_color()
    version = VERSION_1
    truncated = False
    if settings is not None:
        version = settings.get("pes version", VERSION_1)  # deprecated, use "version".
        version = settings.get("version", version)
        truncated = settings.get("truncated", False)
        if isinstance(version, str):
            if version.endswith('t'):
                truncated = True
                version = float(version[:-1])
        version = float(version)
    if truncated:
        if version == VERSION_1:
            write_truncated_version_1(pattern, f)
        elif version == VERSION_6:
            write_truncated_version_6(pattern, f)
    else:
        if version == VERSION_1:
            write_version_1(pattern, f)
        elif version == VERSION_6:
            write_version_6(pattern, f)


def write_truncated_version_1(pattern, f):
    write_string_utf8(f, PES_VERSION_1_SIGNATURE)
    f.write(b'\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    write_pec(pattern, f)


def write_truncated_version_6(pattern, f):
    chart = pattern.threadlist
    write_string_utf8(f, PES_VERSION_6_SIGNATURE)
    placeholder_pec_block = f.tell()
    write_int_32le(f, 0)  # Placeholder for PEC BLOCK
    write_pes_header_v6(pattern, f, chart, 0)
    f.write(bytes(bytearray([0x00] * 5)))
    write_int_16le(f, 0x0000)
    write_int_16le(f, 0x0000)
    current_position = f.tell()
    f.seek(placeholder_pec_block, 0)
    write_int_32le(f, current_position)
    f.seek(current_position, 0)
    write_pec(pattern, f)
    write_pes_addendum(f, ([0xFF], []))
    write_int_16le(f, 0x0000)  # Found in version 6 not 5,4


def write_version_1(pattern, f):
    chart = get_thread_set()
    write_string_utf8(f, PES_VERSION_1_SIGNATURE)

    extends = pattern.bounds()
    cx = (extends[2] + extends[0]) / 2.0
    cy = (extends[3] + extends[1]) / 2.0

    left = extends[0] - cx
    top = extends[1] - cy
    right = extends[2] - cx
    bottom = extends[3] - cy

    placeholder_pec_block = f.tell()
    write_int_32le(f, 0)  # Placeholder for PEC BLOCK

    if len(pattern.stitches) == 0:
        write_pes_header_v1(f, 0)
        write_int_16le(f, 0x0000)
        write_int_16le(f, 0x0000)
    else:
        write_pes_header_v1(f, 1)
        write_int_16le(f, 0xFFFF)
        write_int_16le(f, 0x0000)
        write_pes_blocks(f, pattern, chart, left, top, right, bottom, cx, cy)

    current_position = f.tell()
    f.seek(placeholder_pec_block, 0)
    write_int_32le(f, current_position)
    f.seek(current_position, 0)

    write_pec(pattern, f)


def write_version_6(pattern, f):
    pattern.fix_color_count()
    chart = pattern.threadlist
    write_string_utf8(f, PES_VERSION_6_SIGNATURE)

    extends = pattern.bounds()
    cx = (extends[2] + extends[0]) / 2.0
    cy = (extends[3] + extends[1]) / 2.0

    left = extends[0] - cx
    top = extends[1] - cy
    right = extends[2] - cx
    bottom = extends[3] - cy

    placeholder_pec_block = f.tell()
    write_int_32le(f, 0)  # Placeholder for PEC BLOCK

    if len(pattern.stitches) == 0:
        write_pes_header_v6(pattern, f, chart, 0)
        write_int_16le(f, 0x0000)
        write_int_16le(f, 0x0000)
    else:
        write_pes_header_v6(pattern, f, chart, 1)
        write_int_16le(f, 0xFFFF)
        write_int_16le(f, 0x0000)
        log = write_pes_blocks(f, pattern, chart, left, top, right, bottom, cx, cy)
        # In version 6 there is some node, tree, order thing.
        write_int_32le(f, 0)
        write_int_32le(f, 0)
        for i in range(0, len(log)):
            write_int_32le(f, i)
            write_int_32le(f, 0)

    current_position = f.tell()
    f.seek(placeholder_pec_block, 0)
    write_int_32le(f, current_position)
    f.seek(current_position, 0)
    color_info = write_pec(pattern, f)
    write_pes_addendum(f, color_info)
    write_int_16le(f, 0x0000)  # Found in version 6 not 5,4


def write_pes_header_v1(f, distinct_block_objects):
    write_int_16le(f, 0x01)  # scale to fit
    write_int_16le(f, 0x01)  # 0 = 100x100, 130x180 hoop
    write_int_16le(f, distinct_block_objects)


def write_pes_header_v6(pattern, f, chart, distinct_block_objects):
    write_int_16le(f, 0x01)  # 0 = 100x100, 130x180 hoop
    f.write(b'02')  # This is an 2-digit ascii number.
    write_pes_string_8(f, pattern.get_metadata("name", None))
    write_pes_string_8(f, pattern.get_metadata("category", None))
    write_pes_string_8(f, pattern.get_metadata("author", None))
    write_pes_string_8(f, pattern.get_metadata("keywords", None))
    write_pes_string_8(f, pattern.get_metadata("comments", None))
    write_int_16le(f, 0)  # OptimizeHoopChange = False
    write_int_16le(f, 0)  # Design Page Is Custom = False
    write_int_16le(f, 0x64)  # Hoop Width
    write_int_16le(f, 0x64)  # Hoop Height
    write_int_16le(f, 0)  # Use Existing Design Area = False
    write_int_16le(f, 0xC8)  # designWidth
    write_int_16le(f, 0xC8)  # designHeight
    write_int_16le(f, 0x64)  # designPageSectionWidth
    write_int_16le(f, 0x64)  # designPageSectionHeight
    write_int_16le(f, 0x64)  # p6 # 100
    write_int_16le(f, 0x07)  # designPageBackgroundColor
    write_int_16le(f, 0x13)  # designPageForegroundColor
    write_int_16le(f, 0x01)  # ShowGrid
    write_int_16le(f, 0x01)  # WithAxes
    write_int_16le(f, 0x00)  # SnapToGrid
    write_int_16le(f, 100)  # GridInterval
    write_int_16le(f, 0x01)  # p9 curves?
    write_int_16le(f, 0x00)  # OptimizeEntryExitPoints
    write_int_8(f, 0)  # fromImageStringLength
    #  String FromImageFilename
    write_float_32le(f, float(1))
    write_float_32le(f, float(0))
    write_float_32le(f, float(0))
    write_float_32le(f, float(1))
    write_float_32le(f, float(0))
    write_float_32le(f, float(0))
    write_int_16le(f, 0)  # numberOfProgrammableFillPatterns
    write_int_16le(f, 0)  # numberOfMotifPatterns
    write_int_16le(f, 0)  # featherPatternCount
    count_thread = len(chart)
    write_int_16le(f, count_thread)  # numberOfColors
    for thread in chart:
        write_pes_thread(f, thread)
    write_int_16le(f, distinct_block_objects)  # number ofdistinct blocks


def write_pes_addendum(f, color_info):
    color_index_list = color_info[0]
    rgb_list = color_info[1]
    count = len(color_index_list)
    f.write(bytes(bytearray(color_index_list)))
    f.write(bytes(bytearray([0x20] * (128 - count))))
    for s in range(0, len(rgb_list)):
        blank = [0x00] * 0x90
        f.write(bytes(bytearray(blank)))
    for r in rgb_list:
        write_int_24le(f, r)


def write_pes_string_8(f, string):
    if string is None:
        write_int_8(f, 0)
        return
    if len(string) > 255:
        string = string[:255]
    write_int_8(f, len(string))
    write_string_utf8(f, string)


def write_pes_string_16(f, string):
    if string is None:
        write_int_16le(f, 0)
        return
    write_int_16le(f, len(string))
    # 16 refers to the size write not the string encoding.
    write_string_utf8(f, string)


def write_pes_thread(f, thread):
    write_pes_string_8(f, thread.catalog_number)
    write_int_8(f, thread.get_red())
    write_int_8(f, thread.get_green())
    write_int_8(f, thread.get_blue())
    write_int_8(f, 0)  # unknown
    write_int_32le(f, 0xA)  # A is custom color
    write_pes_string_8(f, thread.description)
    write_pes_string_8(f, thread.brand)
    write_pes_string_8(f, thread.chart)


def write_pes_blocks(f, pattern, chart, left, top, right, bottom, cx, cy):
    if len(pattern.stitches) == 0:
        return

    write_pes_string_16(f, EMB_ONE)
    placeholder = write_pes_sewsegheader(f, left, top, right, bottom)
    write_int_16le(f, 0xFFFF)
    write_int_16le(f, 0x0000)  # FFFF0000 means more blocks exist

    write_pes_string_16(f, EMB_SEG)
    data = write_pes_embsewseg_segments(f, pattern, chart, left, bottom, cx, cy)

    sections = data[0]
    colorlog = data[1]

    current_position = f.tell()
    f.seek(placeholder, 0)
    write_int_16le(f, sections)
    f.seek(current_position, 0)  # patch final section count.

    # If there were addition embsewsegheaders or segments they would go here.

    write_int_16le(f, 0x0000)
    write_int_16le(f, 0x0000)  # 00000000 means no more blocks.

    return colorlog


def write_pes_sewsegheader(f, left, top, right, bottom):
    width = right - left
    height = bottom - top
    hoop_height = 1800
    hoop_width = 1300
    write_int_16le(f, 0)  # left
    write_int_16le(f, 0)  # top
    write_int_16le(f, 0)  # right
    write_int_16le(f, 0)  # bottom
    write_int_16le(f, 0)  # left
    write_int_16le(f, 0)  # top
    write_int_16le(f, 0)  # right
    write_int_16le(f, 0)  # bottom
    trans_x = 0
    trans_y = 0
    trans_x += float(350)
    trans_y += float(100) + height
    trans_x += hoop_width / 2
    trans_y += hoop_height / 2
    trans_x += -width / 2
    trans_y += -height / 2
    write_float_32le(f, float(1))
    write_float_32le(f, float(0))
    write_float_32le(f, float(0))
    write_float_32le(f, float(1))
    write_float_32le(f, float(trans_x))
    write_float_32le(f, float(trans_y))

    write_int_16le(f, 1)
    write_int_16le(f, 0)
    write_int_16le(f, 0)
    write_int_16le(f, int(width))
    write_int_16le(f, int(height))
    f.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')

    placeholder_needs_section_data = f.tell()
    # sections
    write_int_16le(f, 0)
    return placeholder_needs_section_data


def get_as_segments_blocks(pattern, chart, adjust_x, adjust_y):
    color_index = 0
    current_thread = pattern.get_thread_or_filler(color_index)
    color_index += 1
    color_code = current_thread.find_nearest_color_index(chart)
    stitched_x = 0
    stitched_y = 0
    for command_block in pattern.get_as_command_blocks():
        block = []
        command = command_block[0][2] & COMMAND_MASK
        if command == JUMP:
            block.append([stitched_x - adjust_x, stitched_y - adjust_y])
            last_pos = command_block[-1]
            block.append([last_pos[0] - adjust_x, last_pos[1] - adjust_y])
            flag = 1
        elif command == COLOR_CHANGE:
            current_thread = pattern.get_thread_or_filler(color_index)
            color_index += 1
            color_code = current_thread.find_nearest_color_index(chart)
            flag = 1
            continue
        elif command == STITCH:
            for stitch in command_block:
                stitched_x = stitch[0]
                stitched_y = stitch[1]
                block.append([stitched_x - adjust_x, stitched_y - adjust_y])
            flag = 0
        else:
            continue
        yield (block, color_code, flag)


def write_pes_embsewseg_segments(f, pattern, chart, left, bottom, cx, cy):
    section = 0
    colorlog = []

    previous_color_code = -1
    flag = -1
    adjust_x = left + cx
    adjust_y = bottom + cy
    for segs in get_as_segments_blocks(pattern, chart, adjust_x, adjust_y):
        if flag != -1:
            write_int_16le(f, 0x8003)  # section end.
        segments = segs[0]
        color_code = segs[1]
        flag = segs[2]

        if previous_color_code != color_code:
            colorlog.append([section, color_code])
            previous_color_code = color_code
            # This must trigger first segment.
        write_int_16le(f, flag)
        write_int_16le(f, color_code)
        write_int_16le(f, len(segments))
        for segs in segments:
            write_int_16le(f, int(segs[0]))
            write_int_16le(f, int(segs[1]))
        section += 1

    write_int_16le(f, len(colorlog))
    for log_item in colorlog:
        write_int_16le(f, log_item[0])
        write_int_16le(f, log_item[1])

    return section, colorlog  # how many sections, how color transitions.
