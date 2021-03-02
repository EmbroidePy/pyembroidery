import os

import pyembroidery.A100Reader as A100Reader
import pyembroidery.A10oReader as A10oReader
# import pyembroidery.ArtReader as ArtReader
import pyembroidery.BroReader as BroReader
import pyembroidery.ColReader as ColReader
import pyembroidery.ColWriter as ColWriter
import pyembroidery.CsvReader as CsvReader
import pyembroidery.CsvWriter as CsvWriter
import pyembroidery.DatReader as DatReader
import pyembroidery.DsbReader as DsbReader
import pyembroidery.DstReader as DstReader
import pyembroidery.DstWriter as DstWriter
import pyembroidery.DszReader as DszReader
import pyembroidery.EdrReader as EdrReader
import pyembroidery.EdrWriter as EdrWriter
import pyembroidery.EmdReader as EmdReader
import pyembroidery.ExpReader as ExpReader
import pyembroidery.ExpWriter as ExpWriter
import pyembroidery.ExyReader as ExyReader
import pyembroidery.FxyReader as FxyReader
import pyembroidery.GcodeReader as GcodeReader
import pyembroidery.GcodeWriter as GcodeWriter
import pyembroidery.GtReader as GtReader
import pyembroidery.HusReader as HusReader
import pyembroidery.InbReader as InbReader
import pyembroidery.InfReader as InfReader
import pyembroidery.InfWriter as InfWriter
import pyembroidery.JefReader as JefReader
import pyembroidery.JefWriter as JefWriter
import pyembroidery.JpxReader as JpxReader
import pyembroidery.JsonReader as JsonReader
import pyembroidery.JsonWriter as JsonWriter
import pyembroidery.KsmReader as KsmReader
import pyembroidery.MaxReader as MaxReader
import pyembroidery.MitReader as MitReader
import pyembroidery.NewReader as NewReader
import pyembroidery.PcdReader as PcdReader
import pyembroidery.PcmReader as PcmReader
import pyembroidery.PcqReader as PcqReader
import pyembroidery.PcsReader as PcsReader
import pyembroidery.PecReader as PecReader
import pyembroidery.PecWriter as PecWriter
import pyembroidery.PesReader as PesReader
import pyembroidery.PesWriter as PesWriter
import pyembroidery.PhbReader as PhbReader
import pyembroidery.PhcReader as PhcReader
import pyembroidery.PmvReader as PmvReader
import pyembroidery.PmvWriter as PmvWriter
import pyembroidery.PngWriter as PngWriter
import pyembroidery.SewReader as SewReader
import pyembroidery.ShvReader as ShvReader
import pyembroidery.SpxReader as SpxReader
import pyembroidery.StcReader as StcReader
import pyembroidery.StxReader as StxReader
import pyembroidery.SvgWriter as SvgWriter
import pyembroidery.TapReader as TapReader
import pyembroidery.TbfReader as TbfReader
import pyembroidery.TxtWriter as TxtWriter
import pyembroidery.U01Reader as U01Reader
import pyembroidery.U01Writer as U01Writer
import pyembroidery.Vp3Reader as Vp3Reader
import pyembroidery.Vp3Writer as Vp3Writer
import pyembroidery.XxxReader as XxxReader
import pyembroidery.XxxWriter as XxxWriter
# import pyembroidery.ZhsReader as ZhsReader
import pyembroidery.ZxyReader as ZxyReader
from .EmbEncoder import Transcoder as Normalizer
from .EmbFunctions import *
from .EmbThread import EmbThread


class EmbPattern:
    def __init__(self, *args, **kwargs):
        self.stitches = []  # type: list
        self.threadlist = []  # type: list
        self.extras = {}  # type: dict
        # filename, name, category, author, keywords, comments, are typical
        self._previousX = 0  # type: float
        self._previousY = 0  # type: float
        len_args = len(args)
        if len_args >= 1:
            arg0 = args[0]
            if isinstance(arg0, EmbPattern):
                self.stitches = arg0.stitches[:]
                self.threadlist = arg0.threadlist[:]
                self.extras.update(arg0.extras)
                self._previousX = arg0._previousX
                self._previousY = arg0._previousY
                return
            if len(args) >= 2:
                settings = args[1]
            elif 'settings' in kwargs:
                settings = kwargs['settings']
            else:
                settings = kwargs
            if isinstance(arg0, str):
                EmbPattern.static_read(arg0, settings=settings, pattern=self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, EmbPattern):
            return False
        if self.stitches != other.stitches:
            return False
        if self.threadlist != other.threadlist:
            return False
        if self.extras != other.extras:
            return False
        return True

    def __str__(self):
        if "name" in self.extras:
            return "EmbPattern %s (commands: %3d, threads: %3d)" % \
                   (self.extras["name"], len(self.stitches), len(self.threadlist))
        return "EmbPattern (commands: %3d, threads: %3d)" % (len(self.stitches), len(self.threadlist))

    def __len__(self):
        return len(self.stitches)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.extras[item]
        return self.stitches[item]

    def __setitem__(self, key, value):
        if isinstance(key, str):
            self.extras[key] = value
        else:
            self.stitches[key] = value

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self):
        return self.copy()

    def __iadd__(self, other):
        if isinstance(other, EmbPattern):
            self.add_pattern(other)
        elif isinstance(other, EmbThread) or isinstance(other, str):
            self.add_thread(other)
            for i in range(0, len(self.stitches)):
                data = self.stitches[i][2] & COMMAND_MASK
                if data == STITCH or data == SEW_TO or data == NEEDLE_AT:
                    self.color_change()
                    break  # Only add color change if stitching exists.
        elif isinstance(other, int):
            self.add_command(other)
        elif isinstance(other, list) or isinstance(other, tuple):  # tuple or list
            if len(other) == 0:
                return
            v = other[0]
            if isinstance(v, list) or isinstance(v, tuple):  # tuple or list of tuple or lists
                for v in other:
                    x = v[0]
                    y = v[1]
                    try:
                        cmd = v[2]
                    except IndexError:
                        cmd = STITCH
                    self.add_stitch_absolute(cmd, x, y)
            elif isinstance(v, complex):  # tuple or list of complex
                for v in other:
                    x = v.real
                    y = v.imag
                    self.add_stitch_absolute(STITCH, x, y)
            elif isinstance(v, int) or isinstance(v, float):  # tuple or list of numbers.
                i = 0
                ie = len(other)
                while i < ie:
                    self.add_stitch_absolute(STITCH, other[i], other[i + 1])
                    i += 2
            elif isinstance(v, str):
                self.extras[v] = other[1]
        else:
            raise ValueError()
        return self

    def __add__(self, other):
        p = self.copy()
        p.add_pattern(other)
        return p

    def __radd__(self, other):
        p = other.copy()
        p.add_pattern(self)
        return p

    def copy(self):
        emb_pattern = EmbPattern()
        emb_pattern.stitches = self.stitches[:]
        emb_pattern.threadlist = self.threadlist[:]
        emb_pattern.extras.update(self.extras)
        emb_pattern._previousX = self._previousX
        emb_pattern._previousY = self._previousY
        return emb_pattern

    def clear(self):
        self.stitches = []
        self.threadlist = []
        self.extras = {}
        self._previousX = 0
        self._previousY = 0

    def read(self, filename, **settings):
        EmbPattern.static_read(filename, settings=settings, pattern=self)

    def write(self, filename, **settings):
        EmbPattern.static_write(self, filename, settings=settings)

    def move(self, dx=0, dy=0, position=None):
        """Move dx, dy"""
        if position is None:
            self.add_stitch_relative(JUMP, dx, dy)
        else:
            self.insert_stitch_relative(position, JUMP, dx, dy)

    def move_abs(self, x, y, position=None):
        """Move absolute x, y"""
        if position is None:
            self.add_stitch_absolute(JUMP, x, y)
        else:
            self.insert(position, JUMP, x, y)

    def stitch(self, dx=0, dy=0, position=None):
        """Stitch dx, dy"""
        if position is None:
            self.add_stitch_relative(STITCH, dx, dy)
        else:
            self.insert_stitch_relative(position, STITCH, dx, dy)

    def stitch_abs(self, x, y, position=None):
        """Stitch absolute x, y"""
        if position is None:
            self.add_stitch_absolute(STITCH, x, y)
        else:
            self.insert(position, STITCH, x, y)

    def stop(self, dx=0, dy=0, position=None):
        """Stop dx, dy"""
        if position is None:
            self.add_stitch_relative(STOP, dx, dy)
        else:
            self.insert_stitch_relative(position, STOP, dx, dy)

    def trim(self, dx=0, dy=0, position=None):
        """Trim dx, dy"""
        if position is None:
            self.add_stitch_relative(TRIM, dx, dy)
        else:
            self.insert_stitch_relative(position, TRIM, dx, dy)

    def color_change(self, dx=0, dy=0, position=None):
        """Color Change dx, dy"""
        if position is None:
            self.add_stitch_relative(COLOR_CHANGE, dx, dy)
        else:
            self.insert_stitch_relative(position, COLOR_CHANGE, dx, dy)

    def needle_change(self, needle=0, dx=0, dy=0, position=None):
        """Needle change, needle, dx, dy"""
        cmd = encode_thread_change(NEEDLE_SET, None, needle)
        if position is None:
            self.add_stitch_relative(cmd, dx, dy)
        else:
            self.insert_stitch_relative(position, cmd, dx, dy)

    def sequin_eject(self, dx=0, dy=0, position=None):
        """Eject Sequin dx, dy"""
        if position is None:
            self.add_stitch_relative(SEQUIN_EJECT, dx, dy)
        else:
            self.insert_stitch_relative(position, SEQUIN_EJECT, dx, dy)

    def sequin_mode(self, dx=0, dy=0, position=None):
        """Eject Sequin dx, dy"""
        if position is None:
            self.add_stitch_relative(SEQUIN_MODE, dx, dy)
        else:
            self.insert_stitch_relative(position, SEQUIN_MODE, dx, dy)

    def end(self, dx=0, dy=0, position=None):
        """End Design dx, dy"""
        if position is None:
            self.add_stitch_relative(END, dx, dy)
        else:
            self.insert_stitch_relative(position, END, dx, dy)

    def add_thread(self, thread):
        """Adds thread to design.
        Note: this has no effect on stitching and can be done at any point."""
        if isinstance(thread, EmbThread):
            self.threadlist.append(thread)
        else:
            thread_object = EmbThread()
            thread_object.set(thread)
            self.threadlist.append(thread_object)

    def metadata(self, name, data):
        """Adds select metadata to design.
        Note: this has no effect on stitching and can be done at any point."""
        self.extras[name] = data

    def get_metadata(self, name, default=None):
        return self.extras.get(name, default)

    def bounds(self):
        """Returns the bounds of the stitch data:
        min_x, min_y, max_x, max_y"""
        min_x = float('inf')
        min_y = float('inf')
        max_x = -float('inf')
        max_y = -float('inf')

        for stitch in self.stitches:
            if stitch[0] > max_x:
                max_x = stitch[0]
            if stitch[0] < min_x:
                min_x = stitch[0]
            if stitch[1] > max_y:
                max_y = stitch[1]
            if stitch[1] < min_y:
                min_y = stitch[1]
        return min_x, min_y, max_x, max_y

    extends = bounds
    extents = bounds

    def count_stitch_commands(self, command):
        count = 0
        for stitch in self.stitches:
            flags = stitch[2] & COMMAND_MASK
            if flags == command:
                count += 1
        return count

    def count_color_changes(self):
        return self.count_stitch_commands(COLOR_CHANGE)

    def count_needle_sets(self):
        return self.count_stitch_commands(NEEDLE_SET)

    def count_stitches(self):
        return len(self.stitches)

    def count_threads(self):
        return len(self.threadlist)

    @staticmethod
    def get_random_thread():
        thread = EmbThread()
        thread.set("random")
        thread.description = "Random"
        return thread

    def get_thread_or_filler(self, index):
        if len(self.threadlist) <= index:
            return self.get_random_thread()
        else:
            return self.threadlist[index]

    def get_thread(self, index):
        return self.threadlist[index]

    def get_match_commands(self, command):
        for stitch in self.stitches:
            flags = stitch[2] & COMMAND_MASK
            if flags == command:
                yield stitch

    def get_as_stitchblock(self):
        stitchblock = []
        thread = self.get_thread_or_filler(0)
        thread_index = 1
        for stitch in self.stitches:
            flags = stitch[2] & COMMAND_MASK
            if flags == STITCH:
                stitchblock.append(stitch)
            else:
                if len(stitchblock) > 0:
                    yield (stitchblock, thread)
                    stitchblock = []
                if flags == COLOR_CHANGE:
                    thread = self.get_thread_or_filler(thread_index)
                    thread_index += 1
        if len(stitchblock) > 0:
            yield (stitchblock, thread)

    def get_as_command_blocks(self):
        last_pos = 0
        last_command = NO_COMMAND
        for pos, stitch in enumerate(self.stitches):
            command = stitch[2] & COMMAND_MASK
            if command == last_command or last_command == NO_COMMAND:
                last_command = command
                continue
            last_command = command
            yield self.stitches[last_pos:pos]
            last_pos = pos
        yield self.stitches[last_pos:]

    def get_as_colorblocks(self):
        """
        Returns a generator for colorblocks. Color blocks defined with color_breaks will have
        the command omitted whereas color blocks delimited with color_change will end with the
        color_change command, and if delimited with needle_set, the blocks will begin the new
        color block with the needle_set.
        """
        thread_index = 0
        colorblock_start = 0

        for pos, stitch in enumerate(self.stitches):
            command = stitch[2] & COMMAND_MASK
            if command == COLOR_BREAK:
                if colorblock_start != pos:
                    thread = self.get_thread_or_filler(thread_index)
                    thread_index += 1
                    yield self.stitches[colorblock_start:pos], thread
                colorblock_start = pos + 1
                continue
            if command == COLOR_CHANGE:
                thread = self.get_thread_or_filler(thread_index)
                thread_index += 1
                yield self.stitches[colorblock_start:pos + 1], thread
                colorblock_start = pos + 1
                continue
            if command == NEEDLE_SET and colorblock_start != pos:
                thread = self.get_thread_or_filler(thread_index)
                thread_index += 1
                yield self.stitches[colorblock_start:pos], thread
                colorblock_start = pos
                continue

        if colorblock_start != len(self.stitches):
            thread = self.get_thread_or_filler(thread_index)
            yield self.stitches[colorblock_start:], thread

    def get_as_stitches(self):
        """pos, x, y, command, v1, v2, v3"""
        for pos, stitch in enumerate(self.stitches):
            decode = decode_embroidery_command(stitch[2])
            command = decode[0]
            thread = decode[1]
            needle = decode[2]
            order = decode[3]
            yield pos, stitch[0], stitch[1], command, thread, needle, order

    def get_unique_threadlist(self):
        return set(self.threadlist)

    def get_singleton_threadlist(self):
        singleton = []
        last_thread = None
        for thread in self.threadlist:
            if thread != last_thread:
                singleton.append(thread)
            last_thread = thread
        return singleton

    def move_center_to_origin(self):
        extends = self.bounds()
        cx = round((extends[2] - extends[0]) / 2.0)
        cy = round((extends[3] - extends[1]) / 2.0)
        self.translate(-cx, -cy)

    def translate(self, dx, dy):
        for stitch in self.stitches:
            stitch[0] += dx
            stitch[1] += dy

    def transform(self, matrix):
        for stitch in self.stitches:
            matrix.apply(stitch)

    def fix_color_count(self):
        """Ensure that there are threads for all color blocks."""
        thread_index = 0
        init_color = True
        for stitch in self.stitches:
            data = stitch[2] & COMMAND_MASK
            if data == STITCH or data == SEW_TO or data == NEEDLE_AT:
                if init_color:
                    thread_index += 1
                    init_color = False
            elif data == COLOR_CHANGE or data == COLOR_BREAK or data == NEEDLE_SET:
                init_color = True
        while len(self.threadlist) < thread_index:
            self.add_thread(self.get_thread_or_filler(len(self.threadlist)))

    def add_stitch_absolute(self, cmd, x=0, y=0):
        """Add a command at the absolute location: x, y"""
        self.stitches.append([x, y, cmd])
        self._previousX = x
        self._previousY = y

    def add_stitch_relative(self, cmd, dx=0, dy=0):
        """Add a command relative to the previous location"""
        x = self._previousX + dx
        y = self._previousY + dy
        self.add_stitch_absolute(cmd, x, y)

    def insert_stitch_relative(self, position, cmd, dx=0, dy=0):
        """Insert a relative stitch into the pattern. The stitch is relative to the stitch before it.
        If inserting at position 0, it's relative to 0,0. If appending, add is called, updating the positioning.
        """
        if position < 0:
            position += len(self.stitches)  # I need positive positions.
        if position == 0:
            self.stitches.insert(0, [dx, dy, TRIM])  # started (0,0)
        elif position == len(self.stitches) or position is None:  # This is properly just an add.
            self.add_stitch_relative(cmd, dx, dy)
        elif 0 < position < len(self.stitches):
            p = self.stitches[position - 1]
            x = p[0] + dx
            y = p[1] + dy
            self.stitches.insert(position, [x, y, TRIM])

    def insert(self, position, cmd, x=0, y=0):
        """Insert a stitch or command"""
        self.stitches.insert(position, [x, y, cmd])

    def prepend_command(self, cmd, x=0, y=0):
        """Prepend a command, without treating parameters as locations"""
        self.stitches.insert(0, [x, y, cmd])

    def add_command(self, cmd, x=0, y=0):
        """Add a command, without treating parameters as locations
         that require an update"""
        self.stitches.append([x, y, cmd])

    def add_block(self, block, thread=None):
        if thread is not None:
            self.add_thread(thread)
        if block is None:
            return

        if isinstance(block, list) or isinstance(block, tuple):
            if len(block) == 0:
                return
            v = block[0]
            if isinstance(v, list) or isinstance(v, tuple):
                for v in block:
                    x = v[0]
                    y = v[1]
                    try:
                        cmd = v[2]
                    except IndexError:
                        cmd = STITCH
                    self.add_stitch_absolute(cmd, x, y)
            elif isinstance(v, complex):
                for v in block:
                    x = v.real
                    y = v.imag
                    self.add_stitch_absolute(STITCH, x, y)
            elif isinstance(v, int) or isinstance(v, float):
                i = 0
                ie = len(block)
                while i < ie:
                    self.add_stitch_absolute(STITCH, block[i], block[i + 1])
                    i += 2
        self.add_command(COLOR_BREAK)

    def add_stitchblock(self, stitchblock):
        threadlist = self.threadlist
        block = stitchblock[0]
        thread = stitchblock[1]
        if len(threadlist) == 0 or thread is not threadlist[-1]:
            threadlist.append(thread)
            self.add_stitch_relative(COLOR_BREAK)
        else:
            self.add_stitch_relative(SEQUENCE_BREAK)

        for stitch in block:
            try:
                self.add_stitch_absolute(stitch.command, stitch.x, stitch.y)
            except AttributeError:
                self.add_stitch_absolute(stitch[2], stitch[0], stitch[1])

    def add_pattern(self, pattern, dx=None, dy=None, sx=None, sy=None, rotate=None):
        """
        add_pattern merges the given pattern with the current pattern. It accounts for some edge conditions but
        not all of them.

        If there is an end command on the current pattern, that is removed.
        If the color ending the current pattern is equal to the color starting the next those color blocks are merged.
        Any prepended thread change command to the merging pattern is suppressed.

        :param pattern: pattern to add to current pattern
        :param dx: position change of the added pattern x
        :param dy: position change of the added pattern y
        :param sx: scale of the added pattern x
        :param sy: scale fo the added pattern y
        :param rotate: rotation of the added pattern
        :return:
        """
        if isinstance(pattern, str):
            pattern = EmbPattern(pattern)
        if self.stitches[-1][2] == END:
            self.stitches = self.stitches[:-1]  # Remove END, if exists
        if dx is not None or dy is not None:
            if dx is None:
                dx = 0
            if dy is None:
                dy = 0
            self.add_command(MATRIX_TRANSLATE, dx, dy)
        if sx is not None or sx is not None:
            if sx is None:
                sx = sy
            if sy is None:
                sy = sx
            self.add_command(MATRIX_SCALE, sx, sy)
        if rotate is not None:
            self.add_command(MATRIX_ROTATE, rotate)
        # Add the new thread only if it's different from the last one
        self.fix_color_count()

        if len(pattern.threadlist) > 0:
            if pattern.threadlist[0] == self.threadlist[-1]:
                self.threadlist.extend(pattern.threadlist[1:])
            else:
                self.threadlist.extend(pattern.threadlist)
                self.color_change()
        join_position = len(self.stitches)
        self.stitches.extend(pattern.stitches)

        for i in range(join_position, len(self.stitches)):
            data = self.stitches[i][2] & COMMAND_MASK
            if data == STITCH or data == SEW_TO or data == NEEDLE_AT:
                break
            elif data == COLOR_CHANGE or data == COLOR_BREAK or data == NEEDLE_SET:
                self.stitches[i][2] = NO_COMMAND
        self.extras.update(pattern.extras)

    def interpolate_duplicate_color_as_stop(self):
        """Processes a pattern replacing any duplicate colors in the threadlist as a stop."""
        thread_index = 0
        init_color = True
        last_change = None
        for position, stitch in enumerate(self.stitches):
            data = stitch[2] & COMMAND_MASK
            if data == STITCH or data == SEW_TO or data == NEEDLE_AT:
                if init_color:
                    try:
                        if last_change is not None and thread_index != 0 and \
                                self.threadlist[thread_index - 1] == self.threadlist[thread_index]:
                            del self.threadlist[thread_index]
                            self.stitches[last_change][2] = STOP
                        else:
                            thread_index += 1
                    except IndexError:  # Non-existant threads cannot double
                        return
                    init_color = False
            elif data == COLOR_CHANGE or data == COLOR_BREAK or data == NEEDLE_SET:
                init_color = True
                last_change = position

    def interpolate_stop_as_duplicate_color(self, thread_change_command=COLOR_CHANGE):
        """Processes a pattern replacing any stop as a duplicate color, and color_change
         or another specified thread_change_command"""
        thread_index = 0
        for position, stitch in enumerate(self.stitches):
            data = stitch[2] & COMMAND_MASK
            if data == STITCH or data == SEW_TO or data == NEEDLE_AT:
                continue
            elif data == COLOR_CHANGE or data == COLOR_BREAK or data == NEEDLE_SET:
                thread_index += 1
            elif data == STOP:
                try:
                    self.threadlist.insert(thread_index, self.threadlist[thread_index])
                    self.stitches[position][2] = thread_change_command
                    thread_index += 1
                except IndexError:  # There are no colors to duplicate
                    return

    def interpolate_frame_eject(self):
        """Processes a pattern replacing jump-stop-jump/jump-stop-end sequences with FRAME_EJECT."""
        mode = 0
        stop_x = None
        stop_y = None
        sequence_start_position = None
        position = 0
        ie = len(self.stitches)
        while position < ie:
            stitch = self.stitches[position]
            data = stitch[2] & COMMAND_MASK
            if data == STITCH or data == SEW_TO or data == NEEDLE_AT or \
                    data == COLOR_CHANGE or data == COLOR_BREAK or data == NEEDLE_SET:
                if mode == 3:
                    del self.stitches[sequence_start_position:position]
                    position = sequence_start_position
                    self.stitches.insert(position, [stop_x, stop_y, FRAME_EJECT])
                    ie = len(self.stitches)
                mode = 0
            elif data == JUMP:
                if mode == 2:
                    mode = 3
                if mode == 0:
                    sequence_start_position = position
                    mode = 1
            elif data == STOP:
                if mode == 1:
                    mode = 2
                    stop_x = stitch[0]
                    stop_y = stitch[1]
            position += 1
        if mode >= 2:  # Frame_eject at end.
            del self.stitches[sequence_start_position:position]
            position = sequence_start_position
            self.stitches.insert(position, [stop_x, stop_y, FRAME_EJECT])

    def interpolate_trims(self, jumps_to_require_trim=None, distance_to_require_trim=None, clipping=True):
        """Processes a pattern adding trims according to the given criteria."""
        i = -1
        ie = len(self.stitches) - 1

        x = 0
        y = 0
        jump_count = 0
        jump_start = 0
        jump_dx = 0
        jump_dy = 0
        jumping = False
        trimmed = True
        while i < ie:
            i += 1
            stitch = self.stitches[i]
            dx = stitch[0] - x
            dy = stitch[1] - y
            x = stitch[0]
            y = stitch[1]
            command = stitch[2] & COMMAND_MASK
            if command == STITCH or command == SEQUIN_EJECT:
                trimmed = False
                jumping = False
            elif command == COLOR_CHANGE or command == NEEDLE_SET or command == TRIM:
                trimmed = True
                jumping = False
            if command == JUMP:
                if not jumping:
                    jump_dx = 0
                    jump_dy = 0
                    jump_count = 0
                    jump_start = i
                    jumping = True
                jump_count += 1
                jump_dx += dx
                jump_dy += dy
                if not trimmed:
                    if jump_count == jumps_to_require_trim or \
                            distance_to_require_trim is not None and \
                            (
                                    abs(jump_dy) > distance_to_require_trim or \
                                    abs(jump_dx) > distance_to_require_trim
                            ):
                        self.trim(position=jump_start)
                        jump_start += 1  # We inserted a position, start jump has moved.
                        i += 1
                        ie += 1
                        trimmed = True
                if clipping and jump_dx == 0 and jump_dy == 0:  # jump displacement is 0, clip trim command.
                    del self.stitches[jump_start:i + 1]
                    i = jump_start - 1
                    ie = len(self.stitches) - 1

    def get_pattern_interpolate_trim(self, jumps_to_require_trim):
        """Gets a processed pattern with untrimmed jumps merged
        and trims added if merged jumps are beyond the given value.
        The expectation is that it has core commands and not
        middle-level commands"""
        new_pattern = EmbPattern()
        i = -1
        ie = len(self.stitches) - 1
        count = 0
        trimmed = True
        while i < ie:
            i += 1
            stitch = self.stitches[i]
            command = stitch[2] & COMMAND_MASK
            if command == STITCH or command == SEQUIN_EJECT:
                trimmed = False
            elif command == COLOR_CHANGE or command == NEEDLE_SET or command == TRIM:
                trimmed = True
            if trimmed or stitch[2] != JUMP:
                new_pattern.add_stitch_absolute(stitch[2],
                                                stitch[0],
                                                stitch[1])
                continue
            while i < ie and command == JUMP:
                i += 1
                stitch = self.stitches[i]
                command = stitch[2]
                count += 1
            if command != JUMP:
                i -= 1
            stitch = self.stitches[i]
            if count >= jumps_to_require_trim:
                new_pattern.trim()
            count = 0
            new_pattern.add_stitch_absolute(stitch[2],
                                            stitch[0],
                                            stitch[1])
        new_pattern.threadlist.extend(self.threadlist)
        new_pattern.extras.update(self.extras)
        return new_pattern

    def get_pattern_merge_jumps(self):
        """Returns a pattern with all multiple jumps merged."""
        new_pattern = EmbPattern()
        i = -1
        ie = len(self.stitches) - 1
        stitch_break = False
        while i < ie:
            i += 1
            stitch = self.stitches[i]
            command = stitch[2] & COMMAND_MASK
            if command == JUMP:
                if stitch_break:
                    continue
                new_pattern.add_command(STITCH_BREAK)
                stitch_break = True
                continue
            new_pattern.add_stitch_absolute(stitch[2],
                                            stitch[0],
                                            stitch[1])
        new_pattern.threadlist.extend(self.threadlist)
        new_pattern.extras.update(self.extras)
        return new_pattern

    def get_stable_pattern(self):
        """Gets a stabilized version of the pattern."""
        stable_pattern = EmbPattern()
        for stitchblock in self.get_as_stitchblock():
            stable_pattern.add_stitchblock(stitchblock)
        stable_pattern.extras.update(self.extras)
        return stable_pattern

    def get_normalized_pattern(self, encode_settings=None):
        """Encodes pattern typically for saving."""
        normal_pattern = EmbPattern()
        transcoder = Normalizer(encode_settings)
        transcoder.transcode(self, normal_pattern)
        return normal_pattern

    def append_translation(self, x, y):
        """Appends translation to the pattern.
        All commands will be translated by the given amount,
        including absolute location commands."""
        self.add_stitch_relative(MATRIX_TRANSLATE, x, y)

    @staticmethod
    def supported_formats():
        """Generates dictionary entries for supported formats. Each entry will
        always have description, extension, mimetype, and category. Reader
        will provide the reader, if one exists, writer will provide the writer,
        if one exists.

        Metadata gives a list of metadata read and/or written by that type.

        Options provides accepted options by the format and their accepted values.
        """
        # yield ({
        #     "description": "Art Embroidery Format",
        #     "extension": "art",
        #     "extensions": ("art",),
        #     "mimetype": "application/x-art",
        #     "category": "embroidery",
        #     "reader": ArtReader,
        #     "metadata": ("name")
        # })
        yield ({
            "description": "Brother Embroidery Format",
            "extension": "pec",
            "extensions": ("pec",),
            "mimetype": "application/x-pec",
            "category": "embroidery",
            "reader": PecReader,
            "writer": PecWriter,
            "metadata": ("name")
        })
        yield ({
            "description": "Brother Embroidery Format",
            "extension": "pes",
            "extensions": ("pes",),
            "mimetype": "application/x-pes",
            "category": "embroidery",
            "reader": PesReader,
            "writer": PesWriter,
            "versions": ("1", "6", "1t", "6t"),
            "metadata": ("name", "author", "category", "keywords", "comments")
        })
        yield ({
            "description": "Melco Embroidery Format",
            "extension": "exp",
            "extensions": ("exp",),
            "mimetype": "application/x-exp",
            "category": "embroidery",
            "reader": ExpReader,
            "writer": ExpWriter,
        })
        yield ({
            "description": "Tajima Embroidery Format",
            "extension": "dst",
            "extensions": ("dst",),
            "mimetype": "application/x-dst",
            "category": "embroidery",
            "reader": DstReader,
            "writer": DstWriter,
            "read_options": {
                "trim_distance": (None, 3.0, 50.0),
                "trim_at": (2, 3, 4, 5, 6, 7, 8),
                "clipping": (True, False)
            },
            "write_options": {
                "trim_at": (2, 3, 4, 5, 6, 7, 8)
            },
            "versions": ("default", "extended"),
            "metadata": ("name", "author", "copyright")
        })
        yield ({
            "description": "Janome Embroidery Format",
            "extension": "jef",
            "extensions": ("jef",),
            "mimetype": "application/x-jef",
            "category": "embroidery",
            "reader": JefReader,
            "writer": JefWriter,
            "read_options": {
                "trim_distance": (None, 3.0, 50.0),
                "trims": (True, False),
                "trim_at": (2, 3, 4, 5, 6, 7, 8),
                "clipping": (True, False)
            },
            "write_options": {
                "trims": (True, False),
                "trim_at": (2, 3, 4, 5, 6, 7, 8),
            },
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "vp3",
            "extensions": ("vp3",),
            "mimetype": "application/x-vp3",
            "category": "embroidery",
            "reader": Vp3Reader,
            "writer": Vp3Writer,
        })
        yield ({
            "description": "Scalable Vector Graphics",
            "extension": "svg",
            "extensions": ("svg", "svgz"),
            "mimetype": "image/svg+xml",
            "category": "vector",
            "writer": SvgWriter,
        })
        yield ({
            "description": "Comma-separated values",
            "extension": "csv",
            "extensions": ("csv",),
            "mimetype": "text/csv",
            "category": "debug",
            "reader": CsvReader,
            "writer": CsvWriter,
            "versions": ("default", "delta", "full")
        })
        yield ({
            "description": "Singer Embroidery Format",
            "extension": "xxx",
            "extensions": ("xxx",),
            "mimetype": "application/x-xxx",
            "category": "embroidery",
            "reader": XxxReader,
            "writer": XxxWriter
        })
        yield ({
            "description": "Janome Embroidery Format",
            "extension": "sew",
            "extensions": ("sew",),
            "mimetype": "application/x-sew",
            "category": "embroidery",
            "reader": SewReader
        })
        yield ({
            "description": "Barudan Embroidery Format",
            "extension": "u01",
            "extensions": ("u00", "u01", "u02"),
            "mimetype": "application/x-u01",
            "category": "embroidery",
            "reader": U01Reader,
            "writer": U01Writer
        })
        yield ({
            "description": "Husqvarna Viking Embroidery Format",
            "extension": "shv",
            "extensions": ("shv",),
            "mimetype": "application/x-shv",
            "category": "embroidery",
            "reader": ShvReader
        })
        yield ({
            "description": "Toyota Embroidery Format",
            "extension": "10o",
            "extensions": ("10o",),
            "mimetype": "application/x-10o",
            "category": "embroidery",
            "reader": A10oReader
        })
        yield ({
            "description": "Toyota Embroidery Format",
            "extension": "100",
            "extensions": ("100",),
            "mimetype": "application/x-100",
            "category": "embroidery",
            "reader": A100Reader
        })
        yield ({
            "description": "Bits & Volts Embroidery Format",
            "extension": "bro",
            "extensions": ("bro",),
            "mimetype": "application/x-Bro",
            "category": "embroidery",
            "reader": BroReader
        })
        yield ({
            "description": "Sunstar or Barudan Embroidery Format",
            "extension": "dat",
            "extensions": ("dat",),
            "mimetype": "application/x-dat",
            "category": "embroidery",
            "reader": DatReader
        })
        yield ({
            "description": "Tajima(Barudan) Embroidery Format",
            "extension": "dsb",
            "extensions": ("dsb",),
            "mimetype": "application/x-dsb",
            "category": "embroidery",
            "reader": DsbReader
        })
        yield ({
            "description": "ZSK USA Embroidery Format",
            "extension": "dsz",
            "extensions": ("dsz",),
            "mimetype": "application/x-dsz",
            "category": "embroidery",
            "reader": DszReader
        })
        yield ({
            "description": "Elna Embroidery Format",
            "extension": "emd",
            "extensions": ("emd",),
            "mimetype": "application/x-emd",
            "category": "embroidery",
            "reader": EmdReader
        })
        yield ({
            "description": "Eltac Embroidery Format",
            "extension": "exy",  # e??, e01
            "extensions": ("e00", "e01", "e02"),
            "mimetype": "application/x-exy",
            "category": "embroidery",
            "reader": ExyReader
        })
        yield ({
            "description": "Fortron Embroidery Format",
            "extension": "fxy",  # f??, f01
            "extensions": ("f00", "f01", "f02"),
            "mimetype": "application/x-fxy",
            "category": "embroidery",
            "reader": FxyReader
        })
        yield ({
            "description": "Gold Thread Embroidery Format",
            "extension": "gt",
            "extensions": ("gt",),
            "mimetype": "application/x-exy",
            "category": "embroidery",
            "reader": GtReader
        })
        yield ({
            "description": "Inbro Embroidery Format",
            "extension": "inb",
            "extensions": ("inb",),
            "mimetype": "application/x-inb",
            "category": "embroidery",
            "reader": InbReader
        })
        yield ({
            "description": "Tajima Embroidery Format",
            "extension": "tbf",
            "extensions": ("tbf",),
            "mimetype": "application/x-tbf",
            "category": "embroidery",
            "reader": TbfReader
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "ksm",
            "extensions": ("ksm",),
            "mimetype": "application/x-ksm",
            "category": "embroidery",
            "reader": KsmReader
        })
        yield ({
            "description": "Happy Embroidery Format",
            "extension": "tap",
            "extensions": ("tap",),
            "mimetype": "application/x-tap",
            "category": "embroidery",
            "reader": TapReader
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "spx",
            "extensions": ("spx"),
            "mimetype": "application/x-spx",
            "category": "embroidery",
            "reader": SpxReader
        })
        yield ({
            "description": "Data Stitch Embroidery Format",
            "extension": "stx",
            "extensions": ("stx",),
            "mimetype": "application/x-stx",
            "category": "embroidery",
            "reader": StxReader
        })
        yield ({
            "description": "Brother Embroidery Format",
            "extension": "phb",
            "extensions": ("phb",),
            "mimetype": "application/x-phb",
            "category": "embroidery",
            "reader": PhbReader
        })
        yield ({
            "description": "Brother Embroidery Format",
            "extension": "phc",
            "extensions": ("phc",),
            "mimetype": "application/x-phc",
            "category": "embroidery",
            "reader": PhcReader
        })
        yield ({
            "description": "Ameco Embroidery Format",
            "extension": "new",
            "extensions": ("new",),
            "mimetype": "application/x-new",
            "category": "embroidery",
            "reader": NewReader
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "max",
            "extensions": ("max",),
            "mimetype": "application/x-max",
            "category": "embroidery",
            "reader": MaxReader
        })
        yield ({
            "description": "Mitsubishi Embroidery Format",
            "extension": "mit",
            "extensions": ("mit",),
            "mimetype": "application/x-mit",
            "category": "embroidery",
            "reader": MitReader
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "pcd",
            "extensions": ("pcd",),
            "mimetype": "application/x-pcd",
            "category": "embroidery",
            "reader": PcdReader
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "pcq",
            "extensions": ("pcq",),
            "mimetype": "application/x-pcq",
            "category": "embroidery",
            "reader": PcqReader
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "pcm",
            "extensions": ("pcm",),
            "mimetype": "application/x-pcm",
            "category": "embroidery",
            "reader": PcmReader
        })
        yield ({
            "description": "Pfaff Embroidery Format",
            "extension": "pcs",
            "extensions": ("pcs",),
            "mimetype": "application/x-pcs",
            "category": "embroidery",
            "reader": PcsReader
        })
        yield ({
            "description": "Janome Embroidery Format",
            "extension": "jpx",
            "extensions": ("jpx",),
            "mimetype": "application/x-jpx",
            "category": "embroidery",
            "reader": JpxReader
        })
        yield ({
            "description": "Gunold Embroidery Format",
            "extension": "stc",
            "extensions": ("stc",),
            "mimetype": "application/x-stc",
            "category": "embroidery",
            "reader": StcReader
        })
        # yield ({
        #     "description": "Zeng Hsing Embroidery Format",
        #     "extension": "zhs",
        #     "mimetype": "application/x-zhs",
        #     "category": "embroidery",
        #     "reader": ZhsReader
        # })
        yield ({
            "description": "ZSK TC Embroidery Format",
            "extension": "zxy",
            "extensions": ("z00", "z01", "z02"),
            "mimetype": "application/x-zxy",
            "category": "embroidery",
            "reader": ZxyReader
        })
        yield ({
            "description": "Brother Stitch Format",
            "extension": "pmv",
            "extensions": ("pmv",),
            "mimetype": "application/x-pmv",
            "category": "stitch",
            "reader": PmvReader,
            "writer": PmvWriter
        })
        yield ({
            "description": "PNG Format, Portable Network Graphics",
            "extension": "png",
            "extensions": ("png",),
            "mimetype": "image/png",
            "category": "image",
            "writer": PngWriter,
            "write_options": {
                "background": (0x000000, 0xFFFFFF),
                "linewidth": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
            },
        })
        yield ({
            "description": "txt Format, Text File",
            "extension": "txt",
            "extensions": ("txt",),
            "mimetype": "text/plain",
            "category": "debug",
            "writer": TxtWriter,
            "versions": ("default", "embroidermodder")
        })
        yield ({
            "description": "gcode Format, Text File",
            "extension": "gcode",
            "extensions": ("gcode", "g-code", "ngc", "nc", ".g"),
            "mimetype": "text/plain",
            "category": "embroidery",
            "reader": GcodeReader,
            "writer": GcodeWriter,
            "write_options": {
                "stitch_z_travel": (5.0, 10.0),
            },
        })
        yield ({
            "description": "Husqvarna Embroidery Format",
            "extension": "hus",
            "extensions": ("hus",),
            "mimetype": "application/x-hus",
            "category": "embroidery",
            "reader": HusReader
        })
        yield ({
            "description": "Edr Color Format",
            "extension": "edr",
            "extensions": ("edr",),
            "mimetype": "application/x-edr",
            "category": "color",
            "reader": EdrReader,
            "writer": EdrWriter
        })
        yield ({
            "description": "Col Color Format",
            "extension": "col",
            "extensions": ("col",),
            "mimetype": "application/x-col",
            "category": "color",
            "reader": ColReader,
            "writer": ColWriter
        })
        yield ({
            "description": "Inf Color Format",
            "extension": "inf",
            "extensions": ("inf",),
            "mimetype": "application/x-inf",
            "category": "color",
            "reader": InfReader,
            "writer": InfWriter
        })
        yield ({
            "description": "Json Export",
            "extension": "json",
            "extensions": ("json",),
            "mimetype": "application/json",
            "category": "debug",
            "reader": JsonReader,
            "writer": JsonWriter
        })

    @staticmethod
    def convert(filename_from, filename_to, settings=None):
        pattern = EmbPattern.static_read(filename_from, settings)
        if pattern is None:
            return
        EmbPattern.static_write(pattern, filename_to, settings)

    @staticmethod
    def get_extension_by_filename(filename):
        """extracts the extension from a filename"""
        return os.path.splitext(filename)[1][1:]

    @staticmethod
    def read_embroidery(reader, f, settings=None, pattern=None):
        """Reads fileobject or filename with reader."""
        if reader is None:
            return None
        if pattern is None:
            pattern = EmbPattern()

        if EmbPattern.is_str(f):
            text_mode = False
            try:
                text_mode = reader.READ_FILE_IN_TEXT_MODE
            except AttributeError:
                pass
            if text_mode:
                try:
                    with open(f, "r") as stream:
                        reader.read(stream, pattern, settings)
                        stream.close()
                except IOError:
                    pass
            else:
                try:
                    with open(f, "rb") as stream:
                        reader.read(stream, pattern, settings)
                        stream.close()
                except IOError:
                    pass
        else:
            reader.read(f, pattern, settings)
        return pattern

    @staticmethod
    def read_dst(f, settings=None, pattern=None):
        """Reads fileobject as DST file"""
        return EmbPattern.read_embroidery(DstReader, f, settings, pattern)

    @staticmethod
    def read_pec(f, settings=None, pattern=None):
        """Reads fileobject as PEC file"""
        return EmbPattern.read_embroidery(PecReader, f, settings, pattern)

    @staticmethod
    def read_pes(f, settings=None, pattern=None):
        """Reads fileobject as PES file"""
        return EmbPattern.read_embroidery(PesReader, f, settings, pattern)

    @staticmethod
    def read_exp(f, settings=None, pattern=None):
        """Reads fileobject as EXP file"""
        return EmbPattern.read_embroidery(ExpReader, f, settings, pattern)

    @staticmethod
    def read_vp3(f, settings=None, pattern=None):
        """Reads fileobject as VP3 file"""
        return EmbPattern.read_embroidery(Vp3Reader, f, settings, pattern)

    @staticmethod
    def read_jef(f, settings=None, pattern=None):
        """Reads fileobject as JEF file"""
        return EmbPattern.read_embroidery(JefReader, f, settings, pattern)

    @staticmethod
    def read_u01(f, settings=None, pattern=None):
        """Reads fileobject as U01 file"""
        return EmbPattern.read_embroidery(U01Reader, f, settings, pattern)

    @staticmethod
    def read_csv(f, settings=None, pattern=None):
        """Reads fileobject as CSV file"""
        return EmbPattern.read_embroidery(CsvReader, f, settings, pattern)

    @staticmethod
    def read_gcode(f, settings=None, pattern=None):
        """Reads fileobject as GCode file"""
        return EmbPattern.read_embroidery(GcodeReader, f, settings, pattern)

    @staticmethod
    def read_xxx(f, settings=None, pattern=None):
        """Reads fileobject as XXX file"""
        return EmbPattern.read_embroidery(XxxReader, f, settings, pattern)

    @staticmethod
    def static_read(filename, settings=None, pattern=None):
        """Reads file, assuming type by extension"""
        extension = EmbPattern.get_extension_by_filename(filename)
        extension = extension.lower()
        for file_type in EmbPattern.supported_formats():
            if file_type['extension'] != extension:
                continue
            reader = file_type.get("reader", None)
            return EmbPattern.read_embroidery(reader, filename, settings, pattern)
        return None

    @staticmethod
    def write_embroidery(writer, pattern, stream, settings=None):
        if pattern is None:
            return
        if settings is None:
            settings = {}
        else:
            settings = settings.copy()
        try:
            encode = writer.ENCODE
        except AttributeError:
            encode = True

        if settings.get("encode", encode):
            if not ("max_jump" in settings):
                try:
                    settings["max_jump"] = writer.MAX_JUMP_DISTANCE
                except AttributeError:
                    pass
            if not ("max_stitch" in settings):
                try:
                    settings["max_stitch"] = writer.MAX_STITCH_DISTANCE
                except AttributeError:
                    pass
            if not ("full_jump" in settings):
                try:
                    settings["full_jump"] = writer.FULL_JUMP
                except AttributeError:
                    pass
            if not ("round" in settings):
                try:
                    settings["round"] = writer.ROUND
                except AttributeError:
                    pass
            if not ("writes_speeds" in settings):
                try:
                    settings["writes_speeds"] = writer.WRITES_SPEEDS
                except AttributeError:
                    pass
            if not ("sequin_contingency" in settings):
                try:
                    settings["sequin_contingency"] = writer.SEQUIN_CONTINGENCY
                except AttributeError:
                    pass
            if not ("thread_change_command" in settings):
                try:
                    settings["thread_change_command"] = writer.THREAD_CHANGE_COMMAND
                except AttributeError:
                    pass
            if not ("translate" in settings):
                try:
                    settings["translate"] = writer.TRANSLATE
                except AttributeError:
                    pass
            if not ("scale" in settings):
                try:
                    settings["scale"] = writer.SCALE
                except AttributeError:
                    pass
            if not ("rotate" in settings):
                try:
                    settings["rotate"] = writer.ROTATE
                except AttributeError:
                    pass
            pattern = pattern.get_normalized_pattern(settings)

        if EmbPattern.is_str(stream):
            text_mode = False
            try:
                text_mode = writer.WRITE_FILE_IN_TEXT_MODE
            except AttributeError:
                pass
            if text_mode:
                try:
                    with open(stream, "w") as stream:
                        writer.write(pattern, stream, settings)
                except IOError:
                    pass
            else:
                try:
                    with open(stream, "wb") as stream:
                        writer.write(pattern, stream, settings)
                except IOError:
                    pass
        else:
            writer.write(pattern, stream, settings)

    @staticmethod
    def write_dst(pattern, stream, settings=None):
        """Writes fileobject as DST file"""
        EmbPattern.write_embroidery(DstWriter, pattern, stream, settings)

    @staticmethod
    def write_pec(pattern, stream, settings=None):
        """Writes fileobject as PEC file"""
        EmbPattern.write_embroidery(PecWriter, pattern, stream, settings)

    @staticmethod
    def write_pes(pattern, stream, settings=None):
        """Writes fileobject as PES file"""
        EmbPattern.write_embroidery(PesWriter, pattern, stream, settings)

    @staticmethod
    def write_exp(pattern, stream, settings=None):
        """Writes fileobject as EXP file"""
        EmbPattern.write_embroidery(ExpWriter, pattern, stream, settings)

    @staticmethod
    def write_vp3(pattern, stream, settings=None):
        """Writes fileobject as Vp3 file"""
        EmbPattern.write_embroidery(Vp3Writer, pattern, stream, settings)

    @staticmethod
    def write_jef(pattern, stream, settings=None):
        """Writes fileobject as JEF file"""
        EmbPattern.write_embroidery(JefWriter, pattern, stream, settings)

    @staticmethod
    def write_u01(pattern, stream, settings=None):
        """Writes fileobject as U01 file"""
        EmbPattern.write_embroidery(U01Writer, pattern, stream, settings)

    @staticmethod
    def write_csv(pattern, stream, settings=None):
        """Writes fileobject as CSV file"""
        EmbPattern.write_embroidery(CsvWriter, pattern, stream, settings)

    @staticmethod
    def write_txt(pattern, stream, settings=None):
        """Writes fileobject as CSV file"""
        EmbPattern.write_embroidery(TxtWriter, pattern, stream, settings)

    @staticmethod
    def write_gcode(pattern, stream, settings=None):
        """Writes fileobject as Gcode file"""
        EmbPattern.write_embroidery(GcodeWriter, pattern, stream, settings)

    @staticmethod
    def write_xxx(pattern, stream, settings=None):
        """Writes fileobject as XXX file"""
        EmbPattern.write_embroidery(XxxWriter, pattern, stream, settings)

    @staticmethod
    def write_svg(pattern, stream, settings=None):
        """Writes fileobject as DST file"""
        EmbPattern.write_embroidery(SvgWriter, pattern, stream, settings)

    @staticmethod
    def write_png(pattern, stream, settings=None):
        """Writes fileobject as PNG file"""
        EmbPattern.write_embroidery(PngWriter, pattern, stream, settings)

    @staticmethod
    def static_write(pattern, filename, settings=None):
        """Writes file, assuming type by extension"""
        extension = EmbPattern.get_extension_by_filename(filename)
        extension = extension.lower()

        for file_type in EmbPattern.supported_formats():
            if file_type['extension'] != extension:
                continue
            writer = file_type.get("writer", None)
            if writer is None:
                continue
            EmbPattern.write_embroidery(writer, pattern, filename, settings)

    @staticmethod
    def is_str(obj):
        try:
            return isinstance(obj, basestring)
        except NameError:
            return isinstance(obj, str)
