from .EmbThread import EmbThread
from .PecReader import read_pec
from .ReadHelper import (
    read_int_8,
    read_int_16le,
    read_int_24be,
    read_int_32le,
    read_string_8,
)


def read(f, out, settings=None):
    loaded_thread_values = []
    pes_string = read_string_8(f, 8)

    if pes_string == "#PEC0001":
        read_pec(f, out, loaded_thread_values)
        out.interpolate_duplicate_color_as_stop()
        return

    pec_block_position = read_int_32le(f)

    # Ignoring several known PES versions, just abort and read PEC block
    # All versions allow, abort and read PEC block.
    # Metadata started appearing in V4
    # Threads appeared in V5.
    # We quickly abort if there are any complex items in the header.
    if pes_string == "#PES0100":
        out.metadata("version", 10)
        read_pes_header_version_10(f, out, loaded_thread_values)
    elif pes_string == "#PES0090":
        out.metadata("version", 9)
        read_pes_header_version_9(f, out, loaded_thread_values)
    elif pes_string == "#PES0080":
        out.metadata("version", 8)
        read_pes_header_version_8(f, out, loaded_thread_values)
    elif pes_string == "#PES0070":
        out.metadata("version", 7)
        read_pes_header_version_7(f, out, loaded_thread_values)
    elif pes_string == "#PES0060":
        out.metadata("version", 6)
        read_pes_header_version_6(f, out, loaded_thread_values)
    elif pes_string == "#PES0050":
        out.metadata("version", 5)
        read_pes_header_version_5(f, out, loaded_thread_values)
    elif pes_string == "#PES0055":
        out.metadata("version", 5.5)
        read_pes_header_version_5(f, out, loaded_thread_values)
    elif pes_string == "#PES0056":
        out.metadata("version", 5.6)
        read_pes_header_version_5(f, out, loaded_thread_values)
    elif pes_string == "#PES0040":
        out.metadata("version", 4)
        read_pes_header_version_4(f, out)
    elif pes_string == "#PES0030":
        out.metadata("version", 3)
    elif pes_string == "#PES0022":
        out.metadata("version", 2.2)
    elif pes_string == "#PES0020":
        out.metadata("version", 2)
    elif pes_string == "#PES0001":
        out.metadata("version", 1)
        read_pes_header_version_1(f, out)
    else:
        pass  # Header is unrecognised.
    f.seek(pec_block_position, 0)
    read_pec(f, out, loaded_thread_values)
    out.interpolate_duplicate_color_as_stop()


def read_pes_string(f):
    length = read_int_8(f)
    if length == 0:
        return None
    return read_string_8(f, length)


def read_pes_metadata(f, out):
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("name", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("category", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("author", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("keywords", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("comments", v)


def read_pes_thread(f, threadlist):
    thread = EmbThread()
    thread.catalog_number = read_pes_string(f)
    thread.color = 0xFF000000 | read_int_24be(f)
    f.seek(5, 1)
    thread.description = read_pes_string(f)
    thread.brand = read_pes_string(f)
    thread.chart = read_pes_string(f)
    threadlist.append(thread)


def read_pes_header_version_1(f, out):
    # Nothing I care about.
    pass


def read_pes_header_version_4(f, out):
    f.seek(4, 1)
    read_pes_metadata(f, out)


def read_pes_header_version_5(f, out, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, out)
    f.seek(24, 1)  # this is 36 in version 6 and 24 in version 5
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("image", v)
    f.seek(24, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)


def read_pes_header_version_6(f, out, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, out)
    f.seek(36, 1)  # this is 36 in version 6 and 24 in version 5
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("image_file", v)
    f.seek(24, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)


def read_pes_header_version_7(f, out, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, out)
    f.seek(36, 1)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("image_file", v)
    f.seek(24, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)


def read_pes_header_version_8(f, out, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, out)
    f.seek(38, 1)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("image_file", v)
    f.seek(26, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)


def read_pes_header_version_9(f, out, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, out)
    f.seek(14, 1)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("hoop_name", v)
    f.seek(30, 1)  # this is 36 in version 6 and 24 in version 5
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("image_file", v)
    f.seek(34, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)


def read_pes_header_version_10(f, out, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, out)
    f.seek(14, 1)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("hoop_name", v)
    f.seek(38, 1)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        out.metadata("image_file", v)
    f.seek(34, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)
