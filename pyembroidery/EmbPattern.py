from .EmbEncoder import Transcoder as Normalizer
from .EmbFunctions import *
from .EmbThread import EmbThread


class EmbPattern:
    def __init__(self):
        self.stitches = []  # type: list
        self.threadlist = []  # type: list
        self.extras = {}  # type: dict
        # filename, name, category, author, keywords, comments, are typical
        self._previousX = 0  # type: float
        self._previousY = 0  # type: float

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

    def extends(self):
        return self.bounds()

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
        thread_index = 0
        last_pos = 0
        for pos, stitch in enumerate(self.stitches):
            command = stitch[2] & COMMAND_MASK
            if command != COLOR_CHANGE and command != NEEDLE_SET:
                continue
            thread = self.get_thread_or_filler(thread_index)
            thread_index += 1
            yield (self.stitches[last_pos:pos], thread)
            last_pos = pos
        thread = self.get_thread_or_filler(thread_index)
        yield (self.stitches[last_pos:], thread)

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

    def add_pattern(self, pattern):
        """
        add_pattern merges the given pattern with the current pattern. It accounts for some edge conditions but
        not all of them.

        If there is an end command on the current pattern, that is removed.
        If the color ending the current pattern is equal to the color starting the next those color blocks are merged.
        Any prepended thread change command to the merging pattern is suppressed.

        :param pattern: pattern to add to current pattern
        :return:
        """
        if self.stitches[-1][2] == END:
            self.stitches = self.stitches[:-1]  # Remove END, if exists

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
        """Gets a stablized version of the pattern."""
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
