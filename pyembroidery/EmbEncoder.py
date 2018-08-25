import math

from .EmbConstant import *


class Transcoder:
    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        self.max_stitch = settings.get("max_stitch", float('inf'))
        self.max_jump = settings.get("max_jump", float('inf'))
        self.full_jump = settings.get("full_jump", False)
        strip_sequins = settings.get("strip_sequins", True)
        if strip_sequins:
            self.sequin_contingency = CONTINGENCY_SEQUIN_UTILIZE
        else:
            self.sequin_contingency = CONTINGENCY_SEQUIN_JUMP
        self.sequin_contingency = settings.get("sequin_contingency", self.sequin_contingency)

        self.strip_speeds = settings.get("strip_speeds", True)
        self.explicit_trim = settings.get("explicit_trim", True)

        self.has_tie_on = settings.get("tie_on", False)
        self.has_tie_off = settings.get("tie_off", False)
        self.long_stitch_contingency = \
            settings.get("long_stitch_contingency", CONTINGENCY_JUMP_NEEDLE)

        self.matrix = get_identity()
        translate = settings.get("translate", None)
        if translate is not None:
            try:
                m = get_translate(translate[0], translate[1])
                self.matrix = matrix_multiply(self.matrix, m)
            except IndexError:
                try:
                    m = get_translate(translate.x, translate.y)
                    self.matrix = matrix_multiply(self.matrix, m)
                except AttributeError:
                    pass
        scale = settings.get("scale", None)
        if scale is not None:
            try:
                m = get_scale(scale[0], scale[1])
                self.matrix = matrix_multiply(self.matrix, m)
            except (IndexError, TypeError):
                try:
                    m = get_scale(scale.x, scale.y)
                    self.matrix = matrix_multiply(self.matrix, m)
                except AttributeError:
                    m = get_scale(scale, scale)
                    self.matrix = matrix_multiply(self.matrix, m)
        rotate = settings.get("rotate", None)
        if rotate is not None:
            m = get_rotate(rotate)
            self.matrix = matrix_multiply(self.matrix, m)
        self.source_pattern = None
        self.destination_pattern = None
        self.position = 0
        self.color_index = -1
        self.stitch = None
        self.state_trimmed = True
        self.state_sequin_mode = False
        self.needle_x = 0
        self.needle_y = 0
        self.state_jumping = False

    def transcode(self, source_pattern, destination_pattern):
        self.source_pattern = source_pattern
        self.destination_pattern = destination_pattern
        self.transcode_metadata()
        self.transcode_threads()
        self.transcode_stitches()
        return destination_pattern

    def transcode_metadata(self):
        """Transcodes metadata, (just moves)"""
        source = self.source_pattern.extras
        dest = self.destination_pattern.extras
        dest.update(source)

    def transcode_threads(self):
        """Transcodes threads, (just moves)"""
        source = self.source_pattern.threadlist
        dest = self.destination_pattern.threadlist
        dest.extend(source)

    def transcode_stitches(self):
        """Transcodes stitches.
        Converts middle-level commands and potentially incompatible
        commands into a format friendly low level commands."""
        source = self.source_pattern.stitches
        self.state_trimmed = True
        self.needle_x = 0
        self.needle_y = 0
        self.position = 0
        self.color_index = -1

        flags = NO_COMMAND
        for self.position, self.stitch in enumerate(source):
            p = point_in_matrix_space(self.matrix, self.stitch)
            x = p[0]
            y = p[1]
            flags = self.stitch[2]

            if flags == NO_COMMAND:
                continue

            elif flags == STITCH:
                if self.state_trimmed:
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                elif self.state_jumping:
                    self.needle_to(x, y)
                    self.state_jumping = False
                else:
                    self.stitch_with_contingency(x, y)
            elif flags == NEEDLE_AT:
                if self.state_trimmed:
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                elif self.state_jumping:
                    self.needle_to(x, y)
                    self.state_jumping = False
                else:
                    self.needle_to(x, y)
            elif flags == SEW_TO:
                if self.state_trimmed:
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    if self.has_tie_on:
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
                    self.jump_to_within_stitchrange(x, y)
                    self.stitch_at(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                if not self.state_sequin_mode:
                    self.toggle_sequins()
                self.sequin_at(x, y)
            elif flags == COLOR_CHANGE:
                self.tie_off_trim_color_change()
                # If we are told to do something we do it.
                # Even if it's the first command and makes no sense.
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
            elif flags == OPTION_ENABLE_TIE_ON:
                self.has_tie_on = True
            elif flags == OPTION_ENABLE_TIE_OFF:
                self.has_tie_off = True
            elif flags == OPTION_DISABLE_TIE_ON:
                self.has_tie_on = False
            elif flags == OPTION_DISABLE_TIE_OFF:
                self.has_tie_off = False
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
            elif flags == CONTINGENCY_NONE:
                self.long_stitch_contingency = CONTINGENCY_NONE
            elif flags == CONTINGENCY_JUMP_NEEDLE:
                self.long_stitch_contingency = CONTINGENCY_JUMP_NEEDLE
            elif flags == CONTINGENCY_SEW_TO:
                self.long_stitch_contingency = CONTINGENCY_SEW_TO
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
                self.sequin_contingency = CONTINGENCY_SEQUIN_REMOVE
            elif flags == CONTINGENCY_SEQUIN_UTILIZE:
                self.sequin_contingency = CONTINGENCY_SEQUIN_UTILIZE
            elif flags == MATRIX_TRANSLATE:
                m = get_translate(self.stitch[0], self.stitch[1])
                self.matrix = matrix_multiply(self.matrix, m)
            elif flags == MATRIX_SCALE:
                m = get_scale(self.stitch[0], self.stitch[1])
                self.matrix = matrix_multiply(self.matrix, m)
            elif flags == MATRIX_ROTATE:
                m = get_rotate(self.stitch[0])
                self.matrix = matrix_multiply(self.matrix, m)
            elif flags == MATRIX_RESET:
                self.matrix = get_identity()
        if flags != END:
            self.end_here()

    def update_needle_position(self, x, y):
        self.needle_x = x
        self.needle_y = y

    def declare_not_trimmed(self):
        if self.state_trimmed:
            self.state_trimmed = False
            if self.color_index == -1:
                self.color_index = 0

    def add(self, flags, x=None, y=None):
        if x is None:
            x = self.needle_x
        if y is None:
            y = self.needle_y
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
        if self.color_index < 0:
            return  # We haven't stitched anything, colorbreak happens, before start. Ignore.
        if not self.state_trimmed:
            if self.has_tie_off:
                self.tie_off()
            if self.explicit_trim:
                self.trim_here()
        if not self.lookahead_stitch():
            return  # No more stitching will happen, colorchange unneeded.
        self.add(COLOR_CHANGE)
        self.color_index += 1
        self.state_trimmed = True

    def tie_off_trim_color_change(self):
        if not self.state_trimmed:
            if self.has_tie_off:
                self.tie_off()
            if self.explicit_trim:
                self.trim_here()
        self.add(COLOR_CHANGE)
        self.color_index += 1
        self.state_trimmed = True

    def tie_off_and_trim_if_needed(self):
        if not self.state_trimmed:
            self.tie_off_and_trim()

    def tie_off_and_trim(self):
        if self.has_tie_off:
            self.tie_off()
        self.trim_here()

    def tie_off(self):
        try:
            b = point_in_matrix_space(
                self.matrix,
                self.source_pattern.stitches[self.position - 1],
            )
            flags = b[2]
            if flags == STITCH or flags == NEEDLE_AT or \
                    flags == SEW_TO or flags == SEQUIN_EJECT:
                self.lock_stitch(self.needle_x, self.needle_y,
                                 b[0], b[1], self.max_stitch)
        except IndexError:
            pass  # must be an island stitch. jump-stitch-jump

    def tie_on(self):
        try:
            b = point_in_matrix_space(
                self.matrix,
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
        if self.long_stitch_contingency == CONTINGENCY_SEW_TO:
            self.sew_to(new_x, new_y)
        elif self.long_stitch_contingency == CONTINGENCY_JUMP_NEEDLE:
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
        self.declare_not_trimmed()

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
        self.declare_not_trimmed()

    def slow_command_here(self):
        if not self.strip_speeds:
            self.add(SLOW)

    def fast_command_here(self):
        if not self.strip_speeds:
            self.add(FAST)

    def stop_here(self):
        self.add(STOP)
        self.state_trimmed = True

    def end_here(self):
        self.add(END)
        self.state_trimmed = True

    def color_change_here(self):
        self.add(COLOR_CHANGE)
        self.color_index += 1
        self.state_trimmed = True

    def position_will_exceed_constraint(self, length=None, new_x=None, new_y=None):
        """Check if the stitch is too long before trying to deal with it."""
        if length is None:
            length = self.max_stitch
        if new_x is None or new_y is None:
            p = point_in_matrix_space(self.matrix,
                                      self.stitch[0],
                                      self.stitch[1])
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
                stitch = [round(qx), round(qy), data]
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


def get_identity():
    return \
        1, 0, 0, \
        0, 1, 0, \
        0, 0, 1  # identity


def get_scale(sx, sy=None):
    if sy is None:
        sy = sx
    return \
        sx, 0, 0, \
        0, sy, 0, \
        0, 0, 1


def get_translate(tx, ty):
    return \
        1, 0, 0, \
        0, 1, 0, \
        tx, ty, 1


def get_rotate(theta):
    tau = math.pi * 2
    theta *= tau / 360
    ct = math.cos(theta)
    st = math.sin(theta)
    return \
        ct, st, 0, \
        -st, ct, 0, \
        0, 0, 1


def matrix_multiply(a, b):
    return [
        a[0] * b[0] + a[1] * b[3] + a[2] * b[6],
        a[0] * b[1] + a[1] * b[4] + a[2] * b[7],
        a[0] * b[2] + a[1] * b[5] + a[2] * b[8],
        a[3] * b[0] + a[4] * b[3] + a[5] * b[6],
        a[3] * b[1] + a[4] * b[4] + a[5] * b[7],
        a[3] * b[2] + a[4] * b[5] + a[5] * b[8],
        a[6] * b[0] + a[7] * b[3] + a[8] * b[6],
        a[6] * b[1] + a[7] * b[4] + a[8] * b[7],
        a[6] * b[2] + a[7] * b[5] + a[8] * b[8]]


def point_in_matrix_space(matrix, v0, v1=None):
    if v1 is None:
        try:
            return [
                v0[0] * matrix[0] + v0[1] * matrix[3] + 1 * matrix[6],
                v0[0] * matrix[1] + v0[1] * matrix[4] + 1 * matrix[7],
                v0[2]
            ]
        except IndexError:
            return [
                v0[0] * matrix[0] + v0[1] * matrix[3] + 1 * matrix[6],
                v0[0] * matrix[1] + v0[1] * matrix[4] + 1 * matrix[7]
                # Must not have had a 3rd element.
            ]
    return [
        v0 * matrix[0] + v1 * matrix[3] + 1 * matrix[6],
        v0 * matrix[1] + v1 * matrix[4] + 1 * matrix[7]
    ]
