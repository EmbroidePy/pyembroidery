# The commands below 0xFF are intended to denote proper commands.
# The encodings beyond this is supplying additional information.

COMMAND_MASK = 0x000000FF
THREAD_MASK = 0x0000FF00
NEEDLE_MASK = 0x00FF0000
ORDER_MASK = 0xFF000000

FLAGS_MASK = 0x0000FF00

NO_COMMAND = -1
STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
END = 4
COLOR_CHANGE = 5
NEEDLE_SET = 9
SEQUIN_MODE = 6
SEQUIN_EJECT = 7
SLOW = 0xB  # 11
FAST = 0xC  # 12

# Assigns the change sequences, allowing the color change commands to trigger any event.
# For these can be processed in some needle, thread, order values to preset or postset the
# Underlying change sequence.
SET_CHANGE_SEQUENCE = 0x10  # 16

# Stitch with implied contingency.
SEW_TO = 0xB0  # 176
NEEDLE_AT = 0xB1  # 177

STITCH_BREAK = 0xE0  # 224

SEQUENCE_BREAK = 0xE1  # 225
COLOR_BREAK = 0xE2  # 226

# Middle Level commands.
TIE_ON = 0xE4  # 228
TIE_OFF = 0xE5  # 229
FRAME_EJECT = 0xE9  # 233

# Matrix Commands.
MATRIX_TRANSLATE = 0xC0  # 192
MATRIX_SCALE_ORIGIN = 0xC1  # 193
MATRIX_ROTATE_ORIGIN = 0xC2  # 194
MATRIX_SCALE = 0xC4  # 196
MATRIX_ROTATE = 0xC5  # 197
MATRIX_RESET = 0xC3  # 195

OPTION_MAX_STITCH_LENGTH = 0xD5
OPTION_MAX_JUMP_LENGTH = 0xD6
OPTION_EXPLICIT_TRIM = 0xD7
OPTION_IMPLICIT_TRIM = 0xD8

CONTINGENCY_TIE_ON_NONE = 0xD3
CONTINGENCY_TIE_ON_THREE_SMALL = 0xD1

CONTINGENCY_TIE_OFF_NONE = 0xD4
CONTINGENCY_TIE_OFF_THREE_SMALL = 0xD2

CONTINGENCY_LONG_STITCH_NONE = 0xF0
CONTINGENCY_LONG_STITCH_JUMP_NEEDLE = 0xF1
CONTINGENCY_LONG_STITCH_SEW_TO = 0xF2

CONTINGENCY_SEQUIN_UTILIZE = 0xF5
CONTINGENCY_SEQUIN_JUMP = 0xF6
CONTINGENCY_SEQUIN_STITCH = 0xF7
CONTINGENCY_SEQUIN_REMOVE = 0xF8

ALTERNATIVE = 0x100  # Generic flag for an alternative form.
