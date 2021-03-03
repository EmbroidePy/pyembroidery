import os.path

from .EmbPattern import EmbPattern

supported_formats = EmbPattern.supported_formats
convert = EmbPattern.convert
get_extension_by_filename = EmbPattern.get_extension_by_filename

read_embroidery = EmbPattern.read_embroidery
read_dst = EmbPattern.read_dst
read_pec = EmbPattern.read_pec
read_pes = EmbPattern.read_pes
read_exp = EmbPattern.read_exp
read_vp3 = EmbPattern.read_vp3
read_jef = EmbPattern.read_jef
read_u01 = EmbPattern.read_u01
read_csv = EmbPattern.read_csv
read_gcode = EmbPattern.read_gcode
read_xxx = EmbPattern.read_xxx
read = EmbPattern.static_read

write_embroidery = EmbPattern.write_embroidery
write_dst = EmbPattern.write_dst
write_pec = EmbPattern.write_pec
write_pes = EmbPattern.write_pes
write_exp = EmbPattern.write_exp
write_vp3 = EmbPattern.write_vp3
write_jef = EmbPattern.write_jef
write_u01 = EmbPattern.write_u01
write_csv = EmbPattern.write_csv
write_txt = EmbPattern.write_txt
write_gcode = EmbPattern.write_gcode
write_xxx = EmbPattern.write_xxx
write_svg = EmbPattern.write_svg
write_png = EmbPattern.write_png
write = EmbPattern.static_write
is_str = EmbPattern.is_str
