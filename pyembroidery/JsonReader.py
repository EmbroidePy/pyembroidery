from .EmbFunctions import *
from .EmbThread import EmbThread


def decoded_command(command_dict,name):
    split = name.split(' ')
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
    return command


def read(f, out, settings=None):
    import json
    json_object = json.load(f)
    command_dict = get_command_dictionary()
    stitches = json_object['stitches']
    extras = json_object['extras']
    threadlist = json_object['threadlist']
    for t in threadlist:
        color = t["color"]
        thread = EmbThread(color)
        thread.description = t["description"]
        thread.catalog_number = t["catalog_number"]
        thread.details = t["details"]
        thread.brand = t["brand"]
        thread.chart = t["chart"]
        thread.weight = t["weight"]
        out.add_thread(thread)
    for s in stitches:
        out.stitches.append(
            [
                s[0],
                s[1],
                decoded_command(command_dict, s[2])
            ]
        )
    out.extras.update(extras)