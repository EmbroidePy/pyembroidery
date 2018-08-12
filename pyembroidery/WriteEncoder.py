import pyembroidery.EmbPattern as EmbPattern
import math


def distance_squared(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    dx *= dx
    dy *= dy
    return dx + dy


def distance(x0, y0, x1, y1):
    return math.sqrt(distance_squared(x0, y0, x1, y1))


def towards(a, b, amount):
    return (amount * (b - a)) + a


def angleR(x0, y0, x1, y1):
    return math.atan2(y1 - y0, x1 - x0)


def oriented(x0, y0, x1, y1, r):
    radians = angleR(x0, y0, x1, y1)
    return (x0 + (r * math.cos(radians)), y0 + (r * math.sin(radians)))


class WriteEncoder():
    def __init__(self):
        self.max_jump = float('inf')  # type: float
        self.max_stitch = float('inf')  # type: float
        self.tie_on = False  # type: bool
        self.tie_off = False  # type: bool
        self.needle_x = 0  # type: float
        self.needle_y = 0  # type: float
        self.translate_x = 0  # type: float
        self.translate_y = 0  # type: float

    def set_translation(self, x, y):
        self.translate_x = x
        self.translate_y = y

    def jumpTo(self, transcode, x, y):
        self.step_to(transcode, x, y, self.max_jump, EmbPattern.JUMP)
        transcode.append([x, y, EmbPattern.JUMP])

    def stitchTo(self, transcode, x, y):
        self.step_to(transcode, x, y, self.max_stitch, EmbPattern.STITCH)
        transcode.append([x, y, EmbPattern.STITCH])

    def step_to(self, transcode, x, y, length, data):
        distance_x = x - self.needle_x
        distance_y = y - self.needle_y
        if abs(distance_x) > length or abs(distance_y) > length:
            stepsX = math.ceil(abs(distance_x / length))
            stepsY = math.ceil(abs(distance_y / length))
            if (stepsX > stepsY):
                steps = stepsX
            else:
                steps = stepsY
            stepSizeX = distance_x / steps
            stepSizeY = distance_y / steps

            q = 0
            qe = steps
            qx = self.needle_x
            qy = self.needle_y
            while q < qe:
                transcode.append([round(qx), round(qy), data])
                q += 1
                qx += stepSizeX
                qy += stepSizeY

    def lock_stitch(self, transcode, lock_x, lock_y, anchor_x, anchor_y):
        dist = distance(lock_x, lock_y, anchor_x, anchor_y)
        if dist > self.max_stitch:
            p = oriented(lock_x, lock_y, anchor_x, anchor_y, self.max_stitch)
            anchor_x = p[0]
            anchor_y = p[1]
        f = (towards(lock_x, anchor_x, .33), towards(lock_y, anchor_y, .33))
        s = (towards(lock_x, anchor_x, .66), towards(lock_y, anchor_y, .66))
        self.stitchTo(transcode, lock_x, lock_y)
        self.stitchTo(transcode, f[0], f[1])
        self.stitchTo(transcode, s[0], s[1])
        self.stitchTo(transcode, f[0], f[1])

    def process(self, p):
        self.needle_x = 0
        self.needle_y = 0
        copy = EmbPattern.EmbPattern()
        EmbPattern.set(p, copy)
        layer = copy.stitches
        for stitch in layer:
            stitch[0] = round(stitch[0] - self.translate_x)
            stitch[1] = round(stitch[1] - self.translate_y)
        p.stitches = []
        p.threadlist = []
        self.write_code(copy, p)
        self.write_thread(copy, p)
        return p

    def write_thread(self, pattern_from, pattern_to):
        threads_to = pattern_to.threadlist
        threads_to.extend(pattern_from.threadlist)

    def write_code(self, pattern_source, pattern_dest):
        source = pattern_source.stitches
        dest = pattern_dest.stitches
        flags = EmbPattern.NO_COMMAND
        trimmed = True
        for i, stitch in enumerate(source):
            x = stitch[0]
            y = stitch[1]
            flags = stitch[2]
            if flags == EmbPattern.STITCH:
                if trimmed:
                    self.jumpTo(dest, x, y)
                    self.needle_x = x
                    self.needle_y = y
                    if self.tie_on:
                        b = source[i + 1]
                        bx = b[0]
                        by = b[1]
                        self.lock_stitch(dest, x, y, bx, by)
                    dest.append([x, y, EmbPattern.STITCH])
                    trimmed = False;
                else:
                    self.stitchTo(dest, x, y)
            elif flags == EmbPattern.FRAME_EJECT:
                if not trimmed:
                    dest.append([self.needle_x, self.needle_y, EmbPattern.TRIM])
                    trimmed = True
                self.jumpTo(dest, x, y)
                dest.append([x, y, EmbPattern.STOP])
            elif flags == EmbPattern.BREAK:
                if not trimmed:
                    dest.append([self.needle_x, self.needle_y, EmbPattern.TRIM])
                    trimmed = True
                continue # do not update the needle.
            elif flags == EmbPattern.BREAK_COLOR:
                if not trimmed:
                    dest.append([self.needle_x, self.needle_y, EmbPattern.TRIM])
                    trimmed = True
                dest.append([x, y, EmbPattern.COLOR_CHANGE])
                continue # do not update the needle.
            elif flags == EmbPattern.STITCH_FINAL:
                if self.tie_off:
                    b = source[i - 1]
                    bx = b[0]
                    by = b[1]
                    self.lock_stitch(dest, x, y, bx, by)
                self.stitchTo(dest, x, y)
                dest.append([x, y, EmbPattern.TRIM])
                trimmed = True
            elif flags == EmbPattern.STITCH_FINAL_COLOR:
                if self.tie_off:
                    b = source[i - 1]
                    bx = b[0]
                    by = b[1]
                    self.lock_stitch(dest, x, y, bx, by)
                self.stitchTo(dest, x, y)
                dest.append([x, y, EmbPattern.TRIM])
                dest.append([x, y, EmbPattern.COLOR_CHANGE])
                trimmed = True
            else:
                dest.append(stitch)
            self.needle_x = x
            self.needle_y = y
        if flags != EmbPattern.END:
            dest.append([self.needle_x, self.needle_y, EmbPattern.END])
