import math

from .EmbFunctions import *
from .EmbMatrix import EmbMatrix


class Transcoder:
    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        self.max_stitch = settings.get("max_stitch", float('inf'))
        self.max_jump = settings.get("max_jump", float('inf'))
        self.full_jump = settings.get("full_jump", False)
        self.round = settings.get("round", False)
        self.needle_count = settings.get("needle_count", 5)
        self.thread_change_command = settings.get("thread_change_command", COLOR_CHANGE)
        if self.needle_count <= 1 and self.thread_change_command == NEEDLE_SET:
            self.thread_change_command = STOP
        strip_sequins = settings.get("strip_sequins", True)
        # deprecated, use sequin_contingency.
        if strip_sequins:
            self.sequin_contingency = CONTINGENCY_SEQUIN_JUMP
        else:
            self.sequin_contingency = CONTINGENCY_SEQUIN_UTILIZE
        self.sequin_contingency = settings.get("sequin_contingency", self.sequin_contingency)

        self.writes_speeds = settings.get("writes_speeds", True)
        self.explicit_trim = settings.get("explicit_trim", False)

        self.tie_on_contingency = settings.get("tie_on", CONTINGENCY_TIE_ON_NONE)
        if self.tie_on_contingency is True:
            self.tie_on_contingency = CONTINGENCY_TIE_ON_THREE_SMALL
        if self.tie_on_contingency is False:
            self.tie_on_contingency = CONTINGENCY_TIE_ON_NONE

        self.tie_off_contingency = settings.get("tie_off", CONTINGENCY_TIE_OFF_NONE)
        if self.tie_off_contingency is True:
            self.tie_off_contingency = CONTINGENCY_TIE_OFF_THREE_SMALL
        if self.tie_off_contingency is False:
            self.tie_off_contingency = CONTINGENCY_TIE_OFF_NONE

        self.long_stitch_contingency = \
            settings.get("long_stitch_contingency", CONTINGENCY_LONG_STITCH_JUMP_NEEDLE)

        self.matrix = EmbMatrix()
        translate = settings.get("translate", None)
        if translate is not None:
            try:
                self.matrix.post_translate(translate[0], translate[1])
            except IndexError:
                try:
                    self.matrix.post_translate(translate.x, translate.y)
                except AttributeError:
                    pass
        scale = settings.get("scale", None)
        if scale is not None:
            try:
                self.matrix.post_scale(scale[0], scale[1])
            except (IndexError, TypeError):
                try:
                    self.matrix.post_scale(scale.x, scale.y)
                except AttributeError:
                    self.matrix.post_scale(scale, scale)
        rotate = settings.get("rotate", None)
        if rotate is not None:
            self.matrix.post_rotate(rotate)
        self.source_pattern = None
        self.destination_pattern = None
        self.position = 0
        self.order_index = -1
        self.change_sequence = {}
        self.stitch = None
        self.state_trimmed = True
        self.state_sequin_mode = False
        self.state_jumping = False
        self.needle_x = 0
        self.needle_y = 0
        self.high_flags = 0

    def transcode(self, source_pattern, destination_pattern):
        if source_pattern is destination_pattern:
            # both objects are same. Source is copy, destination is cleared.
            source_pattern = destination_pattern.copy()
            destination_pattern.clear()
        self.source_pattern = source_pattern
        self.destination_pattern = destination_pattern
        self.transcode_metadata()
        self.transcode_main()
        return destination_pattern

    def transcode_metadata(self):
        """Transcodes metadata, (just moves)"""
        source = self.source_pattern.extras
        dest = self.destination_pattern.extras
        dest.update(source)

    def get_as_thread_change_sequence_events(self):
        """Generates the sequence change events with their relevant indexes.
        If there is a sewing event prior to the thread sequence event, the first event
        is indexed as 1. If the first event is a discrete event, occurring before
        the sewing starts it's indexed as zero."""
        source = self.source_pattern.stitches
        current_index = 0
        for stitch in source:
            change = decode_embroidery_command(stitch[2])
            command = change[0]
            flags = command & COMMAND_MASK
            if current_index == 0:
                if flags == STITCH or flags == SEW_TO or flags == NEEDLE_AT or flags == SEQUIN_EJECT:
                    current_index = 1
            if flags == SET_CHANGE_SEQUENCE:
                thread = change[1]
                needle = change[2]
                order = change[3]
                yield flags, thread, needle, order, None
            elif flags == NEEDLE_SET or flags == COLOR_CHANGE or flags == COLOR_BREAK:
                change = decode_embroidery_command(command)
                thread = change[1]
                needle = change[2]
                order = change[3]
                yield flags, thread, needle, order, current_index
                current_index += 1

    def build_thread_change_sequence(self):
        """Builds a change sequence to plan out all the color changes for the file."""
        change_sequence = {}
        lookahead_index = 0
        change_sequence[0] = [None, None, None, None]
        for flags, thread, needle, order, current_index in self.get_as_thread_change_sequence_events():
            if flags == SET_CHANGE_SEQUENCE:
                if order is None:
                    try:
                        current = change_sequence[lookahead_index]
                    except KeyError:
                        current = [None, None, None, None]
                        change_sequence[lookahead_index] = current
                    lookahead_index += 1
                else:
                    try:
                        current = change_sequence[order]
                    except KeyError:
                        current = [None, None, None, None]
                        change_sequence[order] = current
            else:
                try:
                    current = change_sequence[current_index]
                except KeyError:
                    current = [None, None, None, None]
                    change_sequence[current_index] = current
                if current_index >= lookahead_index:
                    lookahead_index = current_index + 1
            if flags == COLOR_CHANGE or flags == NEEDLE_SET:
                current[0] = flags
            if thread is not None:
                current[1] = thread
                current[3] = self.source_pattern.get_thread_or_filler(thread)
            if needle is not None:
                current[2] = needle
        # TODO: account for contingency where threadset repeats threads without explicit values set within the commands.

        needle_limit = self.needle_count
        thread_index = 0
        needle_index = 1
        for order, s in change_sequence.items():
            if s[0] is None:
                s[0] = self.thread_change_command
            if s[1] is None:
                s[1] = thread_index
                thread_index += 1
            if s[2] is None:
                s[2] = needle_index
                if s[2] > needle_limit:
                    s[2] = (s[2] - 1) % needle_limit
                    s[2] += 1
                needle_index += 1
            if s[3] is None:
                s[3] = self.source_pattern.get_thread_or_filler(s[1])
        return change_sequence

    def transcode_main(self):
        """Transcodes stitches.
        Converts middle-level commands and potentially incompatible
        commands into a format friendly low level commands."""

        source = self.source_pattern.stitches
        self.state_trimmed = True
        self.needle_x = 0
        self.needle_y = 0
        self.position = 0
        self.order_index = -1
        self.change_sequence = self.build_thread_change_sequence()

        flags = NO_COMMAND
        for self.position, self.stitch in enumerate(source):
            p = self.matrix.point_in_matrix_space(self.stitch)
            x = p[0]
            y = p[1]
            if self.round:
                x = round(x)
                y = round(y)
            flags = self.stitch[2] & COMMAND_MASK
            self.high_flags = self.stitch[2] & FLAGS_MASK

            if flags == NO_COMMAND:
                continue
            elif flags == STITCH:
                if self.state_trimmed:
                    self.declare_not_trimmed()
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    self.tie_on()
                elif self.state_jumping:
                    self.needle_to(x, y)
                    self.state_jumping = False
                else:
                    self.stitch_with_contingency(x, y)
            elif flags == NEEDLE_AT:
                if self.state_trimmed:
                    self.declare_not_trimmed()
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    self.tie_on()
                elif self.state_jumping:
                    self.needle_to(x, y)
                    self.state_jumping = False
                else:
                    self.needle_to(x, y)
            elif flags == SEW_TO:
                if self.state_trimmed:
                    self.declare_not_trimmed()
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    self.tie_on()
                elif self.state_jumping:
                    self.needle_to(x, y)
                    self.state_jumping = False
                else:
                    self.sew_to(x, y)

            # Middle Level Commands.
            elif flags == STITCH_BREAK:
                self.state_jumping = True
            elif flags == FRAME_EJECT:
                self.tie_off_and_trim_if_needed()
                self.jump_to(x, y)
                self.stop_here()
            elif flags == SEQUENCE_BREAK:
                self.tie_off_and_trim_if_needed()
            elif flags == COLOR_BREAK:
                self.color_break()
            elif flags == TIE_OFF:
                self.tie_off()
            elif flags == TIE_ON:
                self.tie_on()

            # Core Commands.
            elif flags == TRIM:
                self.tie_off_and_trim_if_needed()
            elif flags == JUMP:
                if not self.state_jumping:
                    self.jump_to(x, y)
            elif flags == SEQUIN_MODE:
                self.toggle_sequins()
            elif flags == SEQUIN_EJECT:
                if self.state_trimmed:
                    self.declare_not_trimmed()
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    self.tie_on()
                if not self.state_sequin_mode:
                    self.toggle_sequins()
                self.sequin_at(x, y)
            elif flags == COLOR_CHANGE:
                self.tie_off_trim_color_change()
            elif flags == NEEDLE_SET:
                self.tie_off_trim_color_change()
            elif flags == STOP:
                self.stop_here()
            elif flags == SLOW:
                self.slow_command_here()
            elif flags == FAST:
                self.fast_command_here()
            elif flags == END:
                self.end_here()
                break
            # On-the-fly Settings Commands.
            elif flags == CONTINGENCY_TIE_ON_THREE_SMALL:
                self.tie_on_contingency = CONTINGENCY_TIE_ON_THREE_SMALL
            elif flags == CONTINGENCY_TIE_OFF_THREE_SMALL:
                self.tie_off_contingency = CONTINGENCY_TIE_OFF_THREE_SMALL
            elif flags == CONTINGENCY_TIE_ON_NONE:
                self.tie_on_contingency = CONTINGENCY_TIE_ON_NONE
            elif flags == CONTINGENCY_TIE_OFF_NONE:
                self.tie_off_contingency = CONTINGENCY_TIE_OFF_NONE
            elif flags == OPTION_MAX_JUMP_LENGTH:
                x = self.stitch[0]
                self.max_jump = x
            elif flags == OPTION_MAX_STITCH_LENGTH:
                x = self.stitch[0]
                self.max_stitch = x
            elif flags == OPTION_EXPLICIT_TRIM:
                self.explicit_trim = True
            elif flags == OPTION_IMPLICIT_TRIM:
                self.explicit_trim = False
            elif flags == CONTINGENCY_LONG_STITCH_NONE:
                self.long_stitch_contingency = CONTINGENCY_LONG_STITCH_NONE
            elif flags == CONTINGENCY_LONG_STITCH_JUMP_NEEDLE:
                self.long_stitch_contingency = CONTINGENCY_LONG_STITCH_JUMP_NEEDLE
            elif flags == CONTINGENCY_LONG_STITCH_SEW_TO:
                self.long_stitch_contingency = CONTINGENCY_LONG_STITCH_SEW_TO
            elif flags == CONTINGENCY_SEQUIN_REMOVE:
                if self.state_sequin_mode:  # if sequin_mode, turn it off.
                    self.toggle_sequins()
                self.sequin_contingency = CONTINGENCY_SEQUIN_REMOVE
            elif flags == CONTINGENCY_SEQUIN_STITCH:
                if self.state_sequin_mode:  # if sequin_mode, turn it off.
                    self.toggle_sequins()
                self.sequin_contingency = CONTINGENCY_SEQUIN_STITCH
            elif flags == CONTINGENCY_SEQUIN_JUMP:
                if self.state_sequin_mode:  # if sequin_mode, turn it off.
                    self.toggle_sequins()
                self.sequin_contingency = CONTINGENCY_SEQUIN_JUMP
            elif flags == CONTINGENCY_SEQUIN_UTILIZE:
                self.sequin_contingency = CONTINGENCY_SEQUIN_UTILIZE
            elif flags == MATRIX_TRANSLATE:
                self.matrix.post_translate(self.stitch[0], self.stitch[1])
            elif flags == MATRIX_SCALE_ORIGIN:
                self.matrix.post_scale(self.stitch[0], self.stitch[1])
            elif flags == MATRIX_ROTATE_ORIGIN:
                self.matrix.post_rotate(self.stitch[0])
            elif flags == MATRIX_SCALE:
                self.matrix.inverse()
                q = self.matrix.point_in_matrix_space(self.needle_x, self.needle_y)
                self.matrix.inverse()
                self.matrix.post_scale(self.stitch[0], self.stitch[1], q[0], q[1])
            elif flags == MATRIX_ROTATE:
                self.matrix.inverse()
                q = self.matrix.point_in_matrix_space(self.needle_x, self.needle_y)
                self.matrix.inverse()
                self.matrix.post_rotate(self.stitch[0], q[0], q[1])
            elif flags == MATRIX_RESET:
                self.matrix.reset()
        if flags != END:
            self.end_here()

    def update_needle_position(self, x, y):
        self.needle_x = x
        self.needle_y = y

    def declare_not_trimmed(self):
        if self.order_index == -1:
            self.next_change_sequence()
        self.state_trimmed = False

    def add_thread_change(self, command, thread=None, needle=None, order=None):
        x = self.needle_x
        y = self.needle_y
        cmd = encode_thread_change(command, thread, needle, order)
        self.destination_pattern.stitches.append([x, y, cmd])

    def add(self, flags, x=None, y=None):
        if x is None:
            x = self.needle_x
        if y is None:
            y = self.needle_y
        flags |= self.high_flags
        self.destination_pattern.stitches.append([x, y, flags])

    def lookahead_stitch(self):
        """Looks forward from current position and
         determines if anymore stitching will occur."""
        source = self.source_pattern.stitches
        for pos in range(self.position, len(source)):
            stitch = source[pos]
            flags = stitch[2]
            if flags == STITCH:
                return True
            elif flags == NEEDLE_AT:
                return True
            elif flags == SEW_TO:
                return True
            elif flags == TIE_ON:
                return True
            elif flags == SEQUIN_EJECT:
                return True
            elif flags == END:
                return False
        return False

    def color_break(self):
        """Implements color break. Should add color changes add needed only."""
        if self.order_index < 0:
            return  # We haven't stitched anything, colorbreak happens, before start. Ignore.
        if not self.state_trimmed:
            self.tie_off()
            if self.explicit_trim:
                self.trim_here()
        if not self.lookahead_stitch():
            return  # No more stitching will happen, colorchange unneeded.
        self.next_change_sequence()
        self.state_trimmed = True

    def tie_off_trim_color_change(self):
        if not self.state_trimmed:
            self.tie_off()
            if self.explicit_trim:
                self.trim_here()
        self.next_change_sequence()
        self.state_trimmed = True

    def tie_off_and_trim_if_needed(self):
        if not self.state_trimmed:
            self.tie_off_and_trim()

    def tie_off_and_trim(self):
        self.tie_off()
        self.trim_here()

    def tie_off(self):
        if self.tie_off_contingency == CONTINGENCY_TIE_OFF_THREE_SMALL:
            try:
                b = self.matrix.point_in_matrix_space(
                    self.source_pattern.stitches[self.position - 1]
                )
                flags = b[2]
                if flags == STITCH or flags == NEEDLE_AT or \
                        flags == SEW_TO or flags == SEQUIN_EJECT:
                    self.lock_stitch(self.needle_x, self.needle_y,
                                     b[0], b[1], self.max_stitch)
            except IndexError:
                pass  # must be an island stitch. jump-stitch-jump

    def tie_on(self):
        if self.tie_on_contingency == CONTINGENCY_TIE_ON_THREE_SMALL:
            try:
                b = self.matrix.point_in_matrix_space(
                    self.source_pattern.stitches[self.position + 1]
                )
                flags = b[2]
                if flags == STITCH or flags == NEEDLE_AT or \
                        flags == SEW_TO or flags == SEQUIN_EJECT:
                    self.lock_stitch(self.needle_x, self.needle_y,
                                     b[0], b[1], self.max_stitch)
            except IndexError:
                pass  # must be an island stitch. jump-stitch-jump

    def trim_here(self):
        if self.state_sequin_mode:
            # Can't trim in sequin mode. DST uses jumps to trigger sequin eject and to trim.
            self.toggle_sequins()
        self.add(TRIM)
        self.state_trimmed = True

    def toggle_sequins(self):
        """Sequin mode toggle can be called whenever but will only actually turn on if set
        to utilize mode for the sequin contingency."""
        contingency = self.sequin_contingency
        if contingency == CONTINGENCY_SEQUIN_UTILIZE:
            self.add(SEQUIN_MODE)
            self.state_sequin_mode = not self.state_sequin_mode

    def jump_to_within_stitchrange(self, new_x, new_y):
        """Jumps close enough to stitch a position in x,y
        without violating the length constraints."""
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = self.max_jump
        self.interpolate_gap_stitches(x0, y0, new_x, new_y, max_length, JUMP)
        if self.full_jump:
            if self.needle_x != new_x or self.needle_y != new_y:
                self.jump_at(new_x, new_y)
        # We are currently assuming that max_jump is also max_stitch.
        # Properly it might be the case that some format could require
        # a split constraint here where we would need to jump further
        # so that we could then stitch closer.

    def jump_to(self, new_x, new_y):
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = self.max_jump
        self.interpolate_gap_stitches(x0, y0, new_x, new_y, max_length, JUMP)
        self.jump_at(new_x, new_y)

    def jump_at(self, new_x, new_y):
        if self.state_sequin_mode:
            self.toggle_sequins()  # can't jump with sequin mode on.
        self.add(JUMP, new_x, new_y)
        self.update_needle_position(new_x, new_y)

    def stitch_with_contingency(self, new_x, new_y):
        if self.long_stitch_contingency == CONTINGENCY_LONG_STITCH_SEW_TO:
            self.sew_to(new_x, new_y)
        elif self.long_stitch_contingency == CONTINGENCY_LONG_STITCH_JUMP_NEEDLE:
            self.needle_to(new_x, new_y)
        else:
            self.stitch_at(new_x, new_y)

    def sew_to(self, new_x, new_y):
        """Stitches to a specific location, with the emphasis on sewing.
         Subdivides long stitches into additional stitches.
        """
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = self.max_stitch
        self.interpolate_gap_stitches(x0, y0, new_x, new_y, max_length, STITCH)
        self.stitch_at(new_x, new_y)

    def needle_to(self, new_x, new_y):
        """Insert needle at specific location, emphasis on the needle.
        Uses jumps to avoid needle penetrations where possible.

        The limit here is the max stitch limit or jump threshold.
        If jump threshold is set low, it will insert jumps even
        between stitches it could have technically encoded values for.

        Stitches to the new location, adding jumps if needed.
        """
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = self.max_stitch
        self.interpolate_gap_stitches(x0, y0, new_x, new_y, max_length, JUMP)
        self.stitch_at(new_x, new_y)

    def stitch_at(self, new_x, new_y):
        """Inserts a stitch at the specific location.
        Should have already been checked for constraints."""
        self.add(STITCH, new_x, new_y)
        self.update_needle_position(new_x, new_y)

    def sequin_at(self, new_x, new_y):
        """Sequin Ejects at position with the proper Sequin Contingency

        If long stitch contingency is required and since JUMP is often
        sequin eject, the contingency for long stitch is always sew to.
        This shouldn't be exceptionally rare."""
        contingency = self.sequin_contingency
        if contingency == CONTINGENCY_SEQUIN_REMOVE:
            # Do not update the needle position or declare untrimmed.
            return
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = self.max_stitch
        self.interpolate_gap_stitches(x0, y0, new_x, new_y, max_length, STITCH)
        if contingency == CONTINGENCY_SEQUIN_UTILIZE:
            self.add(SEQUIN_EJECT, new_x, new_y)
        elif contingency == CONTINGENCY_SEQUIN_JUMP:
            self.add(JUMP, new_x, new_y)
        elif contingency == CONTINGENCY_SEQUIN_STITCH:
            self.add(STITCH, new_x, new_y)
        self.update_needle_position(new_x, new_y)

    def slow_command_here(self):
        if self.writes_speeds:
            self.add(SLOW)

    def fast_command_here(self):
        if self.writes_speeds:
            self.add(FAST)

    def stop_here(self):
        self.add(STOP)
        self.state_trimmed = True

    def end_here(self):
        self.add(END)
        self.state_trimmed = True

    def next_change_sequence(self):
        self.order_index += 1
        change = self.change_sequence[self.order_index]
        threadlist = self.destination_pattern.threadlist
        threadlist.append(change[3])
        if self.thread_change_command == COLOR_CHANGE:
            if self.order_index != 0:
                self.add_thread_change(COLOR_CHANGE, change[1], change[2])
        elif self.thread_change_command == NEEDLE_SET:
            self.add_thread_change(NEEDLE_SET, change[1], change[2])
        elif self.thread_change_command == STOP:
            self.add_thread_change(STOP, change[1], change[2])
        self.state_trimmed = True

    def position_will_exceed_constraint(self, length=None, new_x=None, new_y=None):
        """Check if the stitch is too long before trying to deal with it."""
        if length is None:
            length = self.max_stitch
        if new_x is None or new_y is None:
            p = self.matrix.point_in_matrix_space(self.stitch[0], self.stitch[1])
            new_x = p[0]
            new_y = p[1]
        distance_x = new_x - self.needle_x
        distance_y = new_y - self.needle_y
        return abs(distance_x) > length or abs(distance_y) > length

    def interpolate_gap_stitches(self, x0, y0, x1, y1, max_length, data):
        """Command sequence line to x, y, respecting length as maximum.
        This does not arrive_at, it steps to within striking distance.
        The next step can arrive at (x, y) without violating constraint.
        If these are already in range, this command will do nothing.

        returns the last stitch interpolated by the code.
        """
        transcode = self.destination_pattern.stitches
        distance_x = x1 - x0
        distance_y = y1 - y0
        if abs(distance_x) > max_length or abs(distance_y) > max_length:
            if data == JUMP and self.state_sequin_mode:
                self.toggle_sequins()  # can't jump with sequin mode on.

            # python 2,3 patch of division that could be integer.
            steps_x = math.ceil(abs(distance_x / (max_length * 1.0)))
            steps_y = math.ceil(abs(distance_y / (max_length * 1.0)))
            if steps_x > steps_y:
                steps = steps_x
            else:
                steps = steps_y
            step_size_x = distance_x / steps
            step_size_y = distance_y / steps
            qx = x0
            qy = y0
            for q in range(1, int(steps)):
                # we need the gap stitches only, not start or end stitch.
                qx += step_size_x
                qy += step_size_y
                stitch = [qx, qy, data | self.high_flags]
                transcode.append(stitch)
                self.update_needle_position(stitch[0], stitch[1])

    def lock_stitch(self, x, y, anchor_x, anchor_y, max_length=None):
        """Tie-on, Tie-off. Lock stitch from current location towards
        anchor location.Ends again at lock location. May not exceed
        max_length in the process."""
        if max_length is None:
            max_length = self.max_stitch
        transcode = self.destination_pattern.stitches
        length = distance(x, y, anchor_x, anchor_y)
        if length > max_length:
            p = oriented(x, y, anchor_x, anchor_y, max_length)
            anchor_x = p[0]
            anchor_y = p[1]
        for amount in (.33, .66, .33, 0):
            transcode.append([
                towards(x, anchor_x, amount),
                towards(y, anchor_y, amount),
                STITCH])


def distance_squared(x0, y0, x1, y1):
    """squared of distance between x0,y0 and x1,y1"""
    dx = x1 - x0
    dy = y1 - y0
    dx *= dx
    dy *= dy
    return dx + dy


def distance(x0, y0, x1, y1):
    """distance between x0,y0 and x1,y1"""
    return math.sqrt(distance_squared(x0, y0, x1, y1))


def towards(a, b, amount):
    """amount between [0,1] -> [a,b]"""
    return (amount * (b - a)) + a


def angle_radians(x0, y0, x1, y1):
    """Angle in radians between x0,y0 and x1,y1"""
    return math.atan2(y1 - y0, x1 - x0)


def oriented(x0, y0, x1, y1, r):
    """from x0,y0 in the direction of x1,y1 in the distance of r"""
    radians = angle_radians(x0, y0, x1, y1)
    return x0 + (r * math.cos(radians)), y0 + (r * math.sin(radians))
