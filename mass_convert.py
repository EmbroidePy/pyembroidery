from pyembroidery import *

for file_stream in os.listdir("convert"):
    convert_file = os.path.join("convert", file_stream)
    pattern = read(convert_file)
    if pattern is None:
        continue
    pattern = pattern.get_pattern_interpolate_trim(3)
    # pattern = pattern.get_pattern_merge_jumps()
    for emb_format in supported_formats():
        if emb_format.get('writer', None) is None:
            continue
        results_file = os.path.join("results", file_stream) + \
                       '.' + emb_format["extension"]
        if emb_format["extension"] == "csv":
            write(pattern, results_file, {"encode": False, "deltas": True})
        else:
            write(pattern, results_file)
