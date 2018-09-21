# The commands below 0xFF are intended to denote proper commands.
# The encodings beyond this is supplying additional information.

COMMAND_MASK = 0x000000FF
THREAD_MASK = 0x0000FF00
NEEDLE_MASK = 0x00FF0000
ORDER_MASK = 0xFF000000

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
SLOW = 0xB
FAST = 0xC

# Assigns the change sequences, allowing the color change commands to trigger any event.
# For these can be processed in some needle, thread, order values to preset or postset the
# Underlying change sequence.
SET_CHANGE_SEQUENCE = 0x10

# Stitch with implied contingency.
SEW_TO = 0xB0
NEEDLE_AT = 0xB1

STITCH_BREAK = 0xE0

SEQUENCE_BREAK = 0xE1
COLOR_BREAK = 0xE2

# Middle Level commands.
TIE_ON = 0xE4
TIE_OFF = 0xE5
FRAME_EJECT = 0xE9

# Matrix Commands.
MATRIX_TRANSLATE = 0xC0
MATRIX_SCALE_ORIGIN = 0xC1
MATRIX_ROTATE_ORIGIN = 0xC2
MATRIX_SCALE = 0xC4
MATRIX_ROTATE = 0xC5
MATRIX_RESET = 0xC3

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


def encode_thread_change(command, thread=None, needle=None, order=None):
    if thread is None:
        thread = 0
    else:
        thread += 1
        thread &= 0xFF
    if needle is None:
        needle = 0
    else:
        needle += 1
        needle &= 0xFF
    if order is None:
        order = 0
    else:
        order += 1
        order &= 0xFF
    command &= COMMAND_MASK
    return command | (order << 24) | (needle << 16) | (thread << 8)


def decode_thread_change(command):
    flag = command & COMMAND_MASK
    thread = command & THREAD_MASK
    thread >>= 8
    thread -= 1
    needle = command & NEEDLE_MASK
    needle >>= 16
    needle -= 1
    order = command & ORDER_MASK
    order >>= 24
    order -= 1
    return flag, thread, needle, order


def get_command_dictionary():
    return {
        "NO_COMMAND": NO_COMMAND,
        "STITCH": STITCH,
        "JUMP": JUMP,
        "TRIM": TRIM,
        "STOP": STOP,
        "END": END,
        "SLOW": SLOW,
        "FAST": FAST,
        "COLOR_CHANGE": COLOR_CHANGE,
        "NEEDLE_SET": NEEDLE_SET,
        "SET_CHANGE_SEQUENCE": SET_CHANGE_SEQUENCE,
        "SEQUIN_MODE": SEQUIN_MODE,
        "SEQUIN_EJECT": SEQUIN_EJECT,
        "SEW_TO": SEW_TO,
        "NEEDLE_AT": NEEDLE_AT,
        "STITCH_BREAK": STITCH_BREAK,
        "SEQUENCE_BREAK": SEQUENCE_BREAK,
        "COLOR_BREAK": COLOR_BREAK,
        "TIE_ON": TIE_ON,
        "TIE_OFF": TIE_OFF,
        "FRAME_EJECT": FRAME_EJECT,
        "MATRIX_TRANSLATE": MATRIX_TRANSLATE,
        "MATRIX_SCALE_ORIGIN": MATRIX_SCALE_ORIGIN,
        "MATRIX_ROTATE_ORIGIN": MATRIX_ROTATE_ORIGIN,
        "MATRIX_SCALE": MATRIX_SCALE,
        "MATRIX_ROTATE": MATRIX_ROTATE,
        "MATRIX_RESET": MATRIX_RESET,
        "CONTINGENCY_TIE_ON_THREE_SMALL": CONTINGENCY_TIE_ON_THREE_SMALL,
        "CONTINGENCY_TIE_OFF_THREE_SMALL": CONTINGENCY_TIE_OFF_THREE_SMALL,
        "CONTINGENCY_TIE_ON_NONE": CONTINGENCY_TIE_ON_NONE,
        "CONTINGENCY_TIE_OFF_NONE": CONTINGENCY_TIE_OFF_NONE,
        "OPTION_MAX_STITCH_LENGTH": OPTION_MAX_STITCH_LENGTH,
        "OPTION_MAX_JUMP_LENGTH": OPTION_MAX_JUMP_LENGTH,
        "OPTION_IMPLICIT_TRIM": OPTION_IMPLICIT_TRIM,
        "OPTION_EXPLICIT_TRIM": OPTION_EXPLICIT_TRIM,
        "CONTINGENCY_LONG_STITCH_NONE": CONTINGENCY_LONG_STITCH_NONE,
        "CONTINGENCY_LONG_STITCH_JUMP_NEEDLE": CONTINGENCY_LONG_STITCH_JUMP_NEEDLE,
        "CONTINGENCY_LONG_STITCH_SEW_TO": CONTINGENCY_LONG_STITCH_SEW_TO,
    }


def get_common_name_dictionary():
    return {
        NO_COMMAND: "NO_COMMAND",
        STITCH: "STITCH",
        JUMP: "JUMP",
        TRIM: "TRIM",
        STOP: "STOP",
        END: "END",
        SLOW: "SLOW",
        FAST: "FAST",
        COLOR_CHANGE: "COLOR_CHANGE",
        NEEDLE_SET: "NEEDLE_SET",
        SET_CHANGE_SEQUENCE: "SET_CHANGE_SEQUENCE",
        SEQUIN_MODE: "SEQUIN_MODE",
        SEQUIN_EJECT: "SEQUIN_EJECT",
        SEW_TO: "SEW_TO",
        NEEDLE_AT: "NEEDLE_AT",
        STITCH_BREAK: "STITCH_BREAK",
        SEQUENCE_BREAK: "SEQUENCE_BREAK",
        COLOR_BREAK: "COLOR_BREAK",
        TIE_ON: "TIE_ON",
        TIE_OFF: "TIE_OFF",
        FRAME_EJECT: "FRAME_EJECT",
        MATRIX_TRANSLATE: "MATRIX_TRANSLATE",
        MATRIX_SCALE: "MATRIX_SCALE",
        MATRIX_ROTATE: "MATRIX_ROTATE",
        MATRIX_SCALE_ORIGIN: "MATRIX_SCALE_ORIGIN",
        MATRIX_ROTATE_ORIGIN: "MATRIX_ROTATE_ORIGIN",
        MATRIX_RESET: "MATRIX_RESET",
        CONTINGENCY_TIE_ON_THREE_SMALL: "CONTINGENCY_TIE_ON_THREE_SMALL",
        CONTINGENCY_TIE_OFF_THREE_SMALL: "CONTINGENCY_TIE_OFF_THREE_SMALL",
        CONTINGENCY_TIE_ON_NONE: "CONTINGENCY_TIE_ON_NONE",
        CONTINGENCY_TIE_OFF_NONE: "CONTINGENCY_TIE_OFF_NONE",
        OPTION_MAX_STITCH_LENGTH: "OPTION_MAX_STITCH_LENGTH",
        OPTION_MAX_JUMP_LENGTH: "OPTION_MAX_JUMP_LENGTH",
        OPTION_IMPLICIT_TRIM: "OPTION_IMPLICIT_TRIM",
        OPTION_EXPLICIT_TRIM: "OPTION_EXPLICIT_TRIM",
        CONTINGENCY_LONG_STITCH_NONE: "CONTINGENCY_LONG_STITCH_NONE",
        CONTINGENCY_LONG_STITCH_JUMP_NEEDLE: "CONTINGENCY_LONG_STITCH_JUMP_NEEDLE",
        CONTINGENCY_LONG_STITCH_SEW_TO: "CONTINGENCY_LONG_STITCH_SEW_TO"
    }
