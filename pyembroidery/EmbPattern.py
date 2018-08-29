import random

from .EmbThread import EmbThread
from .EmbEncoder import Transcoder as Normalizer
from .EmbConstant import *


class EmbPattern:
    def __init__(self):
        self.stitches = []  # type: list
        self.threadlist = []  # type: list
        self.extras = {}
        # filename, name, category, author, keywords, comments, are typical
        self._previousX = 0  # type: float
        self._previousY = 0  # type: float

    def move(self, dx=0, dy=0):
        """Move dx, dy"""
        self.add_stitch_relative(JUMP, dx, dy)

    def move_abs(self, x, y):
        """Move absolute x, y"""
        self.add_stitch_absolute(JUMP, x, y)

    def stitch(self, dx=0, dy=0):
        """Stitch dx, dy"""
        self.add_stitch_relative(STITCH, dx, dy)

    def stitch_abs(self, x, y):
        """Stitch absolute x, y"""
        self.add_stitch_absolute(STITCH, x, y)

    def stop(self, dx=0, dy=0):
        """Stop dx, dy"""
        self.add_stitch_relative(STOP, dx, dy)

    def trim(self, dx=0, dy=0):
        """Trim dx, dy"""
        self.add_stitch_relative(TRIM, dx, dy)

    def color_change(self, dx=0, dy=0):
        """Color Change dx, dy"""
        self.add_stitch_relative(COLOR_CHANGE, dx, dy)

    def sequin_eject(self, dx=0, dy=0):
        """Eject Sequin dx, dy"""
        self.add_stitch_relative(SEQUIN_EJECT, dx, dy)

    def sequin_mode(self, dx=0, dy=0):
        """Eject Sequin dx, dy"""
        self.add_stitch_relative(SEQUIN_MODE, dx, dy)

    def end(self, dx=0, dy=0):
        """End Design dx, dy"""
        self.add_stitch_relative(END, dx, dy)

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

    def extends(self):
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

    def count_stitch_commands(self, command):
        count = 0
        for stitch in self.stitches:
            flags = stitch[2]
            if flags == command:
                count += 1
        return count

    def count_color_changes(self):
        return self.count_stitch_commands(COLOR_CHANGE)

    def count_stitches(self):
        return len(self.stitches)

    def count_threads(self):
        return len(self.threadlist)

    @staticmethod
    def get_random_thread():
        thread = EmbThread()
        thread.color = 0xFF000000 | random.randint(0, 0xFFFFFF)
        thread.description = "Random"
        return thread

    def get_thread_or_filler(self, index):
        if len(self.threadlist) <= index:
            return self.get_random_thread()
        else:
            return self.threadlist[index]

    def get_as_stitchblock(self):
        stitchblock = []
        thread = self.get_thread_or_filler(0)
        thread_index = 1
        for stitch in self.stitches:
            flags = stitch[2]
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
            command = stitch[2]
            if command == last_command or last_command == NO_COMMAND:
                last_command = command
                continue
            last_command = command
            yield self.stitches[last_pos:pos]
            last_pos = pos
        yield self.stitches[last_pos:]

    def get_as_colorblocks(self):
        thread_index = 0
        last_pos = 0
        for pos, stitch in enumerate(self.stitches):
            if stitch[2] != COLOR_CHANGE:
                continue
            thread = self.get_thread_or_filler(thread_index)
            thread_index += 1
            yield (self.stitches[last_pos:pos], thread)
            last_pos = pos
        thread = self.get_thread_or_filler(thread_index)
        yield (self.stitches[last_pos:], thread)

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
        extends = self.extends()
        cx = round((extends[2] - extends[0]) / 2.0)
        cy = round((extends[3] - extends[1]) / 2.0)
        self.translate(-cx, -cy)

    def translate(self, dx, dy):
        for stitch in self.stitches:
            stitch[0] += dx
            stitch[1] += dy

    def fix_color_count(self):
        """Ensure the there are threads for all color blocks."""
        thread_index = 0
        init_color = True
        for stitch in self.stitches:
            data = stitch[2] & COMMAND_MASK
            if data == STITCH or data == SEW_TO or data == NEEDLE_AT:
                if init_color:
                    thread_index += 1
                    init_color = False
            elif data == COLOR_CHANGE or data == COLOR_BREAK:
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

    def add_command(self, cmd, x=0, y=0):
        """Add a command, without treating parameters as locations
         that require an update"""
        self.stitches.append([x, y, cmd])

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
            command = stitch[2]
            if command == STITCH or command == SEQUIN_EJECT:
                trimmed = False
            elif command == COLOR_CHANGE or command == TRIM:
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
            if stitch[2] == JUMP:
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
        """Gets a stablized version of the pattern."""
        stable_pattern = EmbPattern()
        for stitchblock in self.get_as_stitchblock():
            stable_pattern.add_stitchblock(stitchblock)
        stable_pattern.extras.update(self.extras)
        return stable_pattern

    def get_normalized_pattern(self, encode_settings=None):
        """Encodes"""
        normal_pattern = EmbPattern()
        transcoder = Normalizer(encode_settings)
        transcoder.transcode(self, normal_pattern)
        return normal_pattern

    def append_translation(self, x, y):
        """Appends translation to the pattern.
        All commands will be translated by the given amount,
        including absolute location commands."""
        self.add_stitch_relative(MATRIX_TRANSLATE, x, y, )

    def append_enable_tie_on(self, x=0, y=0):
        """Appends enable tie on.
        All starts of new stitching will be tied on"""
        self.add_stitch_relative(OPTION_ENABLE_TIE_ON, x, y)

    def append_enable_tie_off(self, x=0, y=0):
        """Appends enable tie off.
        All ends of stitching will be tied off"""
        self.add_stitch_relative(OPTION_ENABLE_TIE_OFF, x, y)

    def append_disable_tie_on(self, x=0, y=0):
        """Appends disable tie on.
        New stitching will no longer be tied on"""
        self.add_stitch_relative(OPTION_DISABLE_TIE_ON, x, y)

    def append_disable_tie_off(self, x=0, y=0):
        """Appends enable tie off.
        Ends of stitching will no longer be tied off"""
        self.add_stitch_relative(OPTION_DISABLE_TIE_OFF, x, y)
