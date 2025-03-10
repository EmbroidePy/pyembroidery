from .EmbFunctions import *

READ_FILE_IN_TEXT_MODE = True


def read(f, out, settings=None):
    import csv

    csv_reader = csv.reader(f, delimiter=",")
    command_dict = get_command_dictionary()
    for row in csv_reader:
        if len(row) == 0:
            continue
        if "*" in row[0]:
            split = row[2].split(" ")
            command = command_dict[split[0]]
            for sp in split[1:]:
                if sp[0] == "n":
                    needle = int(sp[1:])
                    command |= (needle + 1) << 16
                if sp[0] == "o":
                    order = int(sp[1:])
                    command |= (order + 1) << 24
                if sp[0] == "t":
                    thread = int(sp[1:])
                    command |= (thread + 1) << 8
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
            if (
                len(row) == 7
                and len(row[2]) <= 3
                and len(row[3]) <= 3
                and len(row[4]) <= 3
            ):
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
