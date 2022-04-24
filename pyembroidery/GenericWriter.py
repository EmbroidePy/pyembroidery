import pyembroidery
from pyembroidery import (
    CONTINGENCY_SEQUIN_UTILIZE,
    decode_embroidery_command,
    STITCH,
    COLOR_CHANGE,
    NEEDLE_SET,
    TRIM,
    JUMP,
    SEQUIN_MODE,
    SEQUIN_EJECT,
    STOP,
    SLOW,
    FAST,
    END,
    get_common_name_dictionary,
    COMMAND_MASK,
)
from pyembroidery.WriteHelper import write_string_utf8

WRITES_SPEEDS = True
SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_UTILIZE


def write(pattern, f, settings=None):
    writer = GenericWriter(pattern, f, settings)
    writer.write()


class GenericWriter:
    """
    Generic Writer will write generic data fit to a formatted set of strings.

    Blocks are established by the first segment.
    Colors are established by the first segment or the first segment after a color change or by a needle_set.
    Documents are established by the first segment, or the first segment after an end.

    Segment is the default for any-command. Specific commands override segment.

    stitch is the default stitch.
    stitch_first overrides stitch for the first stitch in a block.
    stitch_last overrides stitch for the last stitch in a block.

    trims and jumps occurring before a color change belong to the previous color.
    trims and jumps occurring after a color change belong to the next color.

    Missing segments are treated as if they never existed. Value properties will differ if segments are excluded.
    """

    def __init__(self, pattern, f, settings):
        self.pattern = pattern
        self.f = f
        self.settings = settings
        self.metadata_entry = settings.get("metadata_entry", None)
        self.thread_entry = settings.get("thread_entry", None)
        self.pattern_start = settings.get("pattern_start", None)
        self.pattern_end = settings.get("pattern_end", None)
        self.document_start = settings.get("document_start", None)
        self.document_end = settings.get("document_end", None)
        self.color_start = settings.get("color_start", None)
        self.color_end = settings.get("color_end", None)
        self.color_join = settings.get("color_join", None)
        self.block_start = settings.get("block_start", None)
        self.block_end = settings.get("block_end", None)
        self.block_join = settings.get("block_join", None)
        self.segment_start = settings.get("segment_start", None)
        self.segment = settings.get("segment", None)
        self.segment_end = settings.get("segment_end", None)
        self.segment_join = settings.get("segment_join", None)
        self.stitch_first = settings.get("stitch_first", None)
        self.stitch_last = settings.get("stitch_last", None)
        self.stitch = settings.get("stitch", None)
        self.stop = settings.get("stop", None)
        self.jump = settings.get("jump", None)
        self.trim = settings.get("trim", None)
        self.needle_set = settings.get("needle_set", None)
        self.color_change = settings.get("color_change", None)
        self.sequin = settings.get("sequin", None)
        self.sequin_mode = settings.get("sequin_mode", None)
        self.slow = settings.get("slow", None)
        self.fast = settings.get("fast", None)
        self.end = settings.get("end", None)

        self.format_dictionary = {}
        self.pattern_established = False
        self.document_established = False
        self.color_established = False
        self.block_established = False
        self.document_index = -1
        self.thread = None
        self.thread_index = -1
        self.stitch_index = -1
        self.color_index = -1
        self.block_index = -1
        self.dx = 0
        self.dy = 0
        self.xx = 0
        self.yy = 0
        self.last_x = 0
        self.last_y = 0
        self.z = 0.0
        self.z_increment = settings.get("stitch_z_travel", 10.0)
        self.command_index = 0

        self.current_stitch = None
        self.x = None
        self.y = None
        self.command = None
        self.cmd = None
        self.thread = None
        self.needle = None
        self.order = None
        self.cmd_str = None

        self.block_closing = False
        self.color_closing = False
        self.document_closing = False

        self.block_opening = False
        self.color_opening = False
        self.document_opening = False

    def write_opens(self):
        if self.document_opening:
            self.document_opening = False
            if self.document_start is not None:
                write_string_utf8(self.f, self.document_start.format_map(self.format_dictionary))
        if self.color_opening:
            self.color_opening = False
            if self.color_join is not None and self.color_index != 0:
                write_string_utf8(self.f, self.color_join.format_map(self.format_dictionary))
            if self.color_start is not None:
                write_string_utf8(self.f, self.color_start.format_map(self.format_dictionary))
        if self.block_opening:
            self.block_opening = False
            if self.block_join is not None and self.block_index != 0:
                write_string_utf8(self.f, self.block_join.format_map(self.format_dictionary))
            if self.block_start is not None:
                write_string_utf8(self.f, self.block_start.format_map(self.format_dictionary))

    def write_closes(self):
        if self.block_closing:
            self.block_closing = False
            if self.block_end is not None:
                write_string_utf8(self.f, self.block_end.format_map(self.format_dictionary))
        if self.color_closing:
            self.color_closing = False
            if self.color_end is not None:
                write_string_utf8(self.f, self.color_end.format_map(self.format_dictionary))
        if self.document_closing:
            self.document_closing = False
            if self.document_end is not None:
                write_string_utf8(self.f, self.document_end.format_map(self.format_dictionary))

    def get_write_segment(self, cmd):
        # SEQUIN_MODE
        if cmd == SEQUIN_MODE and self.sequin_mode is not None:
            return self.sequin_mode

        # SEQUIN
        if cmd == SEQUIN_EJECT and self.sequin is not None:
            return self.sequin

        # STITCH
        if cmd == STITCH and self.stitch is not None:
            return self.stitch

        # TRIM
        if cmd == TRIM and self.trim is not None:
            return self.trim

        # JUMP
        if cmd == JUMP and self.jump is not None:
            return self.jump

        # COLOR CHANGE
        if cmd == COLOR_CHANGE and self.color_change is not None:
            return self.color_change

        # NEEDLE SET
        if cmd == NEEDLE_SET and self.needle_set is not None:
            return self.needle_set

        # STOP COMMAND
        if cmd == STOP and self.stop is not None:
            return self.stop

        # SLOW COMMAND
        if cmd == SLOW and self.slow is not None:
            return self.slow

        # FAST COMMAND
        if cmd == FAST and self.fast is not None:
            return self.fast

        # END COMMAND
        if cmd == END and self.end is not None:
            return self.end

        # GENERIC SEGMENT
        return self.segment

    def set_document_statistics(self):
        pattern = self.pattern
        self.format_dictionary.update(pattern.extras)

        bounds = pattern.bounds()  # convert to mm.
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]

        stitch_counts = {}
        for s in pattern.stitches:
            command = s[2] & COMMAND_MASK
            if command in stitch_counts:
                stitch_counts[command] += 1
            else:
                stitch_counts[command] = 1

        names = get_common_name_dictionary()
        for name in names:
            value = names[name].lower()
            self.format_dictionary[value + "_count"] = stitch_counts.get(name,0)
        self.format_dictionary.update(
            {
                "stitch_total": pattern.count_stitches(),
                "thread_total": pattern.count_threads(),
                "extents_left": bounds[0],
                "extends_top": bounds[1],
                "extends_right": bounds[2],
                "extends_bottom": bounds[3],
                "extends_width": width,
                "extends_height": height,
                "extents_left_mm": bounds[0] / 10.0,
                "extends_top_mm": bounds[1] / 10.0,
                "extends_right_mm": bounds[2] / 10.0,
                "extends_bottom_mm": bounds[3] / 10.0,
                "extends_width_mm": width / 10.0,
                "extends_height_mm": height / 10.0,
            }
        )

    def update_positions(self, x, y, cmd):
        self.dx = x - self.last_x
        self.dy = y - self.last_y
        idx = int(round(x - self.xx))
        idy = int(round(y - self.yy))
        self.xx += idx
        self.yy += idy
        self.format_dictionary.update(
            {
                "x": x,
                "y": y,
                "z": self.z,
                "_x": -x,
                "_y": -y,
                "dx": self.dx,
                "dy": self.dy,
                "idx": idx,
                "idy": idy,
                "_idx": -idx,
                "_idy": -idy,
                "ix": self.xx,
                "iy": self.yy,
                "_ix": -self.xx,
                "_iy": -self.yy,
                "last_x": self.last_x,
                "last_y": self.last_y,
                "_last_x": -self.last_x,
                "_last_y": -self.last_y,
            }
        )
        if cmd == STITCH:
            self.z += self.z_increment
        self.last_x = x
        self.last_y = y

    def update_command(self):
        try:
            self.current_stitch = self.pattern.stitches[self.command_index]

            self.x, self.y, self.command = self.current_stitch
            self.cmd, self.thread, self.needle, self.order = decode_embroidery_command(
                self.command
            )
            self.cmd_str = pyembroidery.get_common_name_dictionary()[self.cmd]
        except IndexError:
            self.current_stitch = None
            self.x = None
            self.y = None
            self.command = None
            self.cmd = None
            self.thread = None
            self.needle = None
            self.order = None
            self.cmd_str = None
        self.format_dictionary.update(
            {
                "index": self.command_index,
                "command": self.command,
                "cmd_str": self.cmd_str,
                "cmd": self.cmd,
                "cmd_thread": self.thread,
                "cmd_needle": self.needle,
                "cmd_order": self.order,
            }
        )

    def open_pattern(self):
        if not self.pattern_established:
            self.pattern_established = True
            if self.pattern_start is not None:
                write_string_utf8(
                    self.f, self.pattern_start.format_map(self.format_dictionary)
                )

    def open_document(self):
        # DOCUMENT START
        if not self.document_established:
            self.document_established = True
            self.document_index += 1
            self.document_opening = True
            self.color_index = 0

            self.format_dictionary.update(
                {
                    "document_index": self.document_index,
                    "document_index1": self.document_index + 1,
                    "color_index": self.color_index,
                    "color_index1": self.color_index + 1,
                    "block_index": self.block_index,
                    "block_index1": self.block_index + 1,
                }
            )

    def open_color(self):
        # COLOR START
        if not self.color_established:
            self.color_established = True
            self.thread_index += 1
            self.color_opening = True

            self.thread = self.pattern.get_thread_or_filler(self.thread_index)
            self.block_index = 0
            self.color_index += 1
            self.format_dictionary.update(
                {
                    "document_index": self.document_index,
                    "document_index1": self.document_index + 1,
                    "color_index": self.color_index,
                    "color_index1": self.color_index + 1,
                    "block_index": self.block_index,
                    "block_index1": self.block_index + 1,
                }
            )

    def open_block(self):
        # BLOCK START
        if not self.block_established:
            self.block_established = True
            self.block_index += 1
            self.block_opening = True
            self.format_dictionary.update(
                {
                    "document_index": self.document_index,
                    "document_index1": self.document_index + 1,
                    "color_index": self.color_index,
                    "color_index1": self.color_index + 1,
                    "block_index": self.block_index,
                    "block_index1": self.block_index + 1,
                }
            )

    def write_segment(self, segment):
        # SEGMENT
        if self.segment_start is not None:
            write_string_utf8(self.f, self.segment_start.format_map(self.format_dictionary))

        write_string_utf8(self.f, segment.format_map(self.format_dictionary))

        # SEGMENT JOIN
        if self.segment_join is not None:
            write_string_utf8(self.f, self.segment_join.format_map(self.format_dictionary))

        # SEGMENT_END
        if self.segment_end is not None:
            write_string_utf8(self.f, self.segment_end.format_map(self.format_dictionary))

    def close_pattern(self):
        if self.pattern_established:
            self.pattern_established = False
            if self.pattern_end is not None:
                write_string_utf8(
                    self.f, self.pattern_end.format_map(self.format_dictionary)
                )

    def close_document(self):
        # DOCUMENT END
        if self.document_established:
            self.document_established = False
            self.document_closing = True

    def close_color(self):
        # COLOR END
        if self.color_established:
            self.color_established = False
            self.color_closing = True

    def close_block(self):
        # BLOCK END
        if self.block_established:
            self.block_established = False
            self.block_closing = True

    def write(self):
        pattern = self.pattern
        f = self.f
        settings = self.settings

        if settings is None:
            return

        # DOCUMENT STATISTICS
        self.set_document_statistics()

        self.open_pattern()
        if self.metadata_entry is not None:
            for i, key in enumerate(pattern.extras):
                value = pattern.extras[key]
                self.format_dictionary.update({
                    "metadata_index": i,
                    "metadata_key": str(key),
                    "metadata_value": str(value),
                })
                write_string_utf8(
                    self.f, self.metadata_entry.format_map(self.format_dictionary)
                )

        if self.thread_entry is not None:
            for i, thread in enumerate(pattern.threadlist):
                self.format_dictionary.update({
                    "thread_index": i,
                    "thread_color": thread.hex_color(),
                    "thread_description": thread.description,
                    "thread_brand": thread.brand,
                    "thread_catalog_number": thread.catalog_number,
                    "thread_chart": thread.chart,
                    "thread_details": thread.details,
                    "thread_weight": thread.weight,
                    "thread_red": thread.get_red(),
                    "thread_green": thread.get_green(),
                    "thread_blue": thread.get_blue(),
                })
                write_string_utf8(
                    self.f, self.thread_entry.format_map(self.format_dictionary)
                )
        for self.command_index in range(0, len(pattern.stitches)):
            self.update_command()
            write_segment = self.get_write_segment(self.cmd)

            # MAIN CODE, there is something to write.
            if write_segment is not None:
                if isinstance(write_segment, dict):
                    key, default = write_segment[None]
                    key = key.format_map(self.format_dictionary)
                    write_segment = write_segment.get(key,default)
                self.update_positions(self.x, self.y, self.cmd)
                if self.cmd == SEQUIN_MODE:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                # SEQUIN
                if self.cmd == SEQUIN_EJECT:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                # STITCH
                if self.cmd == STITCH:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                # TRIM
                if self.cmd == TRIM:
                    self.open_document()
                    self.open_color()

                # JUMP
                if self.cmd == JUMP:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                # COLOR CHANGE
                if self.cmd == COLOR_CHANGE:
                    self.open_document()

                # NEEDLE SET
                if self.cmd == NEEDLE_SET:
                    self.open_document()
                    self.open_color()

                # STOP COMMAND
                if self.cmd == STOP:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                # SLOW COMMAND
                if self.cmd == SLOW:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                # FAST COMMAND
                if self.cmd == FAST:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                # END COMMAND
                if self.cmd == END:
                    self.open_document()
                    self.open_color()
                    self.open_block()

                self.write_opens()
                self.write_segment(write_segment)

                if self.cmd == SEQUIN_MODE:
                    pass

                # SEQUIN
                if self.cmd == SEQUIN_EJECT:
                    pass

                # STITCH
                if self.cmd == STITCH:
                    pass

                # TRIM
                if self.cmd == TRIM:
                    self.close_block()

                # JUMP
                if self.cmd == JUMP:
                    pass

                # COLOR CHANGE
                if self.cmd == COLOR_CHANGE:
                    self.close_block()
                    self.close_color()

                # NEEDLE SET
                if self.cmd == NEEDLE_SET:
                    pass

                # STOP COMMAND
                if self.cmd == STOP:
                    pass

                # SLOW COMMAND
                if self.cmd == SLOW:
                    pass

                # FAST COMMAND
                if self.cmd == FAST:
                    pass

                # END COMMAND
                if self.cmd == END:
                    self.close_block()
                    self.close_color()
                    self.close_document()
                self.write_closes()

        self.close_block()
        self.close_color()
        self.close_document()
        self.close_pattern()
