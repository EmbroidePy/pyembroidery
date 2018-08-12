from pyembroidery.EmbConstant import *

READ_FILE_IN_TEXT_MODE = True


def read(f, out, settings=None):
    import csv
    csv_reader = csv.reader(f, delimiter=',')
    command_dict = get_command_dictionary()
    for row in csv_reader:
        if len(row) == 0:
            continue
        if "*" in row[0]:
            command = command_dict[row[2]]
            if len(row) == 3:
                out.add_command(command)
            else:
                out.add_stitch_absolute(command, float(row[3]), float(row[4]))
        elif "#" in row[0]:
            continue
        elif "@" in row[0]:
            if len(row) != 3:
                continue
            out.metadata(row[1], row[2])
        elif "$" in row[0]:
            thread_add = {}
            if len(row) == 7 and len(row[2]) <= 3 and len(row[3]) <= 3 and len(row[4]) <= 3:
                # This is an embroidermodder csv file, I changed the colors and added more details.
                # [THREAD_NUMBER], [RED], [GREEN], [BLUE], [DESCRIPTION], [CATALOG_NUMBER]\"\n");
                thread_add["rgb"] = (int(row[2]), int(row[3]), int(row[4]))
                thread_add["description"] = row[5]
                thread_add["catalog"] = row[6]
            else:
                try:
                    thread_add["rgb"] = row[2]
                except IndexError:
                    pass
                try:
                    thread_add["name"] = row[3]
                except IndexError:
                    pass
                try:
                    thread_add["brand"] = row[4]
                except IndexError:
                    pass
                try:
                    thread_add["catalog"] = row[5]
                except IndexError:
                    pass
                try:
                    thread_add["details"] = row[6]
                except IndexError:
                    pass
                try:
                    thread_add["weight"] = row[7]
                except IndexError:
                    pass
            out.add_thread(thread_add)


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
        "MATRIX_SCALE": MATRIX_SCALE,
        "MATRIX_ROTATE": MATRIX_ROTATE,
        "MATRIX_RESET": MATRIX_RESET,
        "OPTION_ENABLE_TIE_ON": OPTION_ENABLE_TIE_ON,
        "OPTION_ENABLE_TIE_OFF": OPTION_ENABLE_TIE_OFF,
        "OPTION_DISABLE_TIE_ON": OPTION_DISABLE_TIE_ON,
        "OPTION_DISABLE_TIE_OFF": OPTION_DISABLE_TIE_OFF,
        "OPTION_MAX_STITCH_LENGTH": OPTION_MAX_STITCH_LENGTH,
        "OPTION_MAX_JUMP_LENGTH": OPTION_MAX_JUMP_LENGTH,
        "OPTION_IMPLICIT_TRIM": OPTION_IMPLICIT_TRIM,
        "OPTION_EXPLICIT_TRIM": OPTION_EXPLICIT_TRIM,
        "CONTINGENCY_NONE": CONTINGENCY_NONE,
        "CONTINGENCY_JUMP_NEEDLE": CONTINGENCY_JUMP_NEEDLE,
        "CONTINGENCY_SEW_TO": CONTINGENCY_SEW_TO,
    }
