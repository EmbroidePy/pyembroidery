from .EmbConstant import *


def encode_thread_change(command, thread=None, needle=None, order=None):
    if thread is None:
        thread = 0
    else:
        thread &= 0xFF
        thread += 1
    if needle is None:
        needle = 0
    else:
        needle &= 0xFF
        needle += 1
    if order is None:
        order = 0
    else:
        order &= 0xFF
        order += 1
    command &= COMMAND_MASK
    return command | (order << 24) | (needle << 16) | (thread << 8)


def decode_embroidery_command(command):
    flag = command & COMMAND_MASK
    thread = command & THREAD_MASK
    thread >>= 8
    thread -= 1
    if thread == -1:
        thread = None
    needle = command & NEEDLE_MASK
    needle >>= 16
    needle -= 1
    if needle == -1:
        needle = None
    order = command & ORDER_MASK
    order >>= 24
    order -= 1
    if order == -1:
        order = None
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
