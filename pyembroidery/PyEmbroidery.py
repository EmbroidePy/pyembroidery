import os.path

import pyembroidery.A100Reader as A100Reader
import pyembroidery.A10oReader as A10oReader
import pyembroidery.BroReader as BroReader
import pyembroidery.ColReader as ColReader
import pyembroidery.ColWriter as ColWriter
import pyembroidery.CsvReader as CsvReader
import pyembroidery.CsvWriter as CsvWriter
import pyembroidery.DatReader as DatReader
import pyembroidery.DsbReader as DsbReader
import pyembroidery.DstReader as DstReader
import pyembroidery.DstWriter as DstWriter
import pyembroidery.DszReader as DszReader
import pyembroidery.EdrReader as EdrReader
import pyembroidery.EdrWriter as EdrWriter
import pyembroidery.EmdReader as EmdReader
import pyembroidery.ExpReader as ExpReader
import pyembroidery.ExpWriter as ExpWriter
import pyembroidery.ExyReader as ExyReader
import pyembroidery.FxyReader as FxyReader
import pyembroidery.GcodeReader as GcodeReader
import pyembroidery.GcodeWriter as GcodeWriter
import pyembroidery.GtReader as GtReader
import pyembroidery.HusReader as HusReader
import pyembroidery.InfReader as InfReader
import pyembroidery.InfWriter as InfWriter
import pyembroidery.InbReader as InbReader
import pyembroidery.JefReader as JefReader
import pyembroidery.JefWriter as JefWriter
import pyembroidery.JpxReader as JpxReader
import pyembroidery.JsonWriter as JsonWriter
import pyembroidery.JsonReader as JsonReader
import pyembroidery.KsmReader as KsmReader
import pyembroidery.MaxReader as MaxReader
import pyembroidery.MitReader as MitReader
import pyembroidery.NewReader as NewReader
import pyembroidery.PcdReader as PcdReader
import pyembroidery.PcmReader as PcmReader
import pyembroidery.PcqReader as PcqReader
import pyembroidery.PcsReader as PcsReader
import pyembroidery.PecReader as PecReader
import pyembroidery.PecWriter as PecWriter
import pyembroidery.PesReader as PesReader
import pyembroidery.PesWriter as PesWriter
import pyembroidery.PhbReader as PhbReader
import pyembroidery.PhcReader as PhcReader
import pyembroidery.PmvReader as PmvReader
import pyembroidery.PmvWriter as PmvWriter
import pyembroidery.PngWriter as PngWriter
import pyembroidery.SewReader as SewReader
import pyembroidery.ShvReader as ShvReader
import pyembroidery.StcReader as StcReader
import pyembroidery.StxReader as StxReader
import pyembroidery.SvgWriter as SvgWriter
import pyembroidery.TapReader as TapReader
import pyembroidery.TbfReader as TbfReader
import pyembroidery.TxtWriter as TxtWriter
import pyembroidery.U01Reader as U01Reader
import pyembroidery.U01Writer as U01Writer
import pyembroidery.Vp3Reader as Vp3Reader
import pyembroidery.Vp3Writer as Vp3Writer
import pyembroidery.XxxReader as XxxReader
import pyembroidery.XxxWriter as XxxWriter
# import pyembroidery.ZhsReader as ZhsReader
import pyembroidery.ZxyReader as ZxyReader
from .EmbPattern import EmbPattern


def supported_formats():
    """Generates dictionary entries for supported formats. Each entry will
    always have description, extension, mimetype, and category. Reader
    will provide the reader, if one exists, writer will provide the writer,
    if one exists.

    Metadata gives a list of metadata read and/or written by that type.

    Options provides accepted options by the format and their accepted values.
    """
    yield ({
        "description": "Brother Embroidery Format",
        "extension": "pec",
        "extensions": ("pec",),
        "mimetype": "application/x-pec",
        "category": "embroidery",
        "reader": PecReader,
        "writer": PecWriter,
        "metadata": ("name")
    })
    yield ({
        "description": "Brother Embroidery Format",
        "extension": "pes",
        "extensions": ("pes",),
        "mimetype": "application/x-pes",
        "category": "embroidery",
        "reader": PesReader,
        "writer": PesWriter,
        "versions": ("1", "6", "1t", "6t"),
        "metadata": ("name", "author", "category", "keywords", "comments")
    })
    yield ({
        "description": "Melco Embroidery Format",
        "extension": "exp",
        "extensions": ("exp",),
        "mimetype": "application/x-exp",
        "category": "embroidery",
        "reader": ExpReader,
        "writer": ExpWriter,
    })
    yield ({
        "description": "Tajima Embroidery Format",
        "extension": "dst",
        "extensions": ("dst",),
        "mimetype": "application/x-dst",
        "category": "embroidery",
        "reader": DstReader,
        "writer": DstWriter,
        "read_options": {
            "trim_distance": (None, 3.0, 50.0),
            "trim_at": (2, 3, 4, 5, 6, 7, 8),
            "clipping": (True, False)
        },
        "write_options": {
            "trim_at": (2, 3, 4, 5, 6, 7, 8)
        },
        "versions": ("default", "extended"),
        "metadata": ("name", "author", "copyright")
    })
    yield ({
        "description": "Janome Embroidery Format",
        "extension": "jef",
        "extensions": ("jef",),
        "mimetype": "application/x-jef",
        "category": "embroidery",
        "reader": JefReader,
        "writer": JefWriter,
        "read_options": {
            "trim_distance": (None, 3.0, 50.0),
            "trims": (True, False),
            "trim_at": (2, 3, 4, 5, 6, 7, 8),
            "clipping": (True, False)
        },
        "write_options": {
            "trims": (True, False),
            "trim_at": (2, 3, 4, 5, 6, 7, 8),
        },
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "vp3",
        "extensions": ("vp3",),
        "mimetype": "application/x-vp3",
        "category": "embroidery",
        "reader": Vp3Reader,
        "writer": Vp3Writer,
    })
    yield ({
        "description": "Scalable Vector Graphics",
        "extension": "svg",
        "extensions": ("svg", "svgz"),
        "mimetype": "image/svg+xml",
        "category": "vector",
        "writer": SvgWriter,
    })
    yield ({
        "description": "Comma-separated values",
        "extension": "csv",
        "extensions": ("csv",),
        "mimetype": "text/csv",
        "category": "debug",
        "reader": CsvReader,
        "writer": CsvWriter,
        "versions": ("default", "delta", "full")
    })
    yield ({
        "description": "Singer Embroidery Format",
        "extension": "xxx",
        "extensions": ("xxx",),
        "mimetype": "application/x-xxx",
        "category": "embroidery",
        "reader": XxxReader,
        "writer": XxxWriter
    })
    yield ({
        "description": "Janome Embroidery Format",
        "extension": "sew",
        "extensions": ("sew",),
        "mimetype": "application/x-sew",
        "category": "embroidery",
        "reader": SewReader
    })
    yield ({
        "description": "Barudan Embroidery Format",
        "extension": "u01",
        "extensions": ("u00", "u01", "u02"),
        "mimetype": "application/x-u01",
        "category": "embroidery",
        "reader": U01Reader,
        "writer": U01Writer
    })
    yield ({
        "description": "Husqvarna Viking Embroidery Format",
        "extension": "shv",
        "extensions": ("shv",),
        "mimetype": "application/x-shv",
        "category": "embroidery",
        "reader": ShvReader
    })
    yield ({
        "description": "Toyota Embroidery Format",
        "extension": "10o",
        "extensions": ("10o",),
        "mimetype": "application/x-10o",
        "category": "embroidery",
        "reader": A10oReader
    })
    yield ({
        "description": "Toyota Embroidery Format",
        "extension": "100",
        "extensions": ("100",),
        "mimetype": "application/x-100",
        "category": "embroidery",
        "reader": A100Reader
    })
    yield ({
        "description": "Bits & Volts Embroidery Format",
        "extension": "bro",
        "extensions": ("bro",),
        "mimetype": "application/x-Bro",
        "category": "embroidery",
        "reader": BroReader
    })
    yield ({
        "description": "Sunstar or Barudan Embroidery Format",
        "extension": "dat",
        "extensions": ("dat",),
        "mimetype": "application/x-dat",
        "category": "embroidery",
        "reader": DatReader
    })
    yield ({
        "description": "Tajima(Barudan) Embroidery Format",
        "extension": "dsb",
        "extensions": ("dsb",),
        "mimetype": "application/x-dsb",
        "category": "embroidery",
        "reader": DsbReader
    })
    yield ({
        "description": "ZSK USA Embroidery Format",
        "extension": "dsz",
        "extensions": ("dsz",),
        "mimetype": "application/x-dsz",
        "category": "embroidery",
        "reader": DszReader
    })
    yield ({
        "description": "Elna Embroidery Format",
        "extension": "emd",
        "extensions": ("emd",),
        "mimetype": "application/x-emd",
        "category": "embroidery",
        "reader": EmdReader
    })
    yield ({
        "description": "Eltac Embroidery Format",
        "extension": "exy",  # e??, e01
        "extensions": ("e00", "e01", "e02"),
        "mimetype": "application/x-exy",
        "category": "embroidery",
        "reader": ExyReader
    })
    yield ({
        "description": "Fortron Embroidery Format",
        "extension": "fxy",  # f??, f01
        "extensions": ("f00", "f01", "f02"),
        "mimetype": "application/x-fxy",
        "category": "embroidery",
        "reader": FxyReader
    })
    yield ({
        "description": "Gold Thread Embroidery Format",
        "extension": "gt",
        "extensions": ("gt",),
        "mimetype": "application/x-exy",
        "category": "embroidery",
        "reader": GtReader
    })
    yield ({
        "description": "Inbro Embroidery Format",
        "extension": "inb",
        "extensions": ("inb",),
        "mimetype": "application/x-inb",
        "category": "embroidery",
        "reader": InbReader
    })
    yield ({
        "description": "Tajima Embroidery Format",
        "extension": "tbf",
        "extensions": ("tbf",),
        "mimetype": "application/x-tbf",
        "category": "embroidery",
        "reader": TbfReader
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "ksm",
        "extensions": ("ksm",),
        "mimetype": "application/x-ksm",
        "category": "embroidery",
        "reader": KsmReader
    })
    yield ({
        "description": "Happy Embroidery Format",
        "extension": "tap",
        "extensions": ("tap",),
        "mimetype": "application/x-tap",
        "category": "embroidery",
        "reader": TapReader
    })
    yield ({
        "description": "Data Stitch Embroidery Format",
        "extension": "stx",
        "extensions": ("stx",),
        "mimetype": "application/x-stx",
        "category": "embroidery",
        "reader": StxReader
    })
    yield ({
        "description": "Brother Embroidery Format",
        "extension": "phb",
        "extensions": ("phb",),
        "mimetype": "application/x-phb",
        "category": "embroidery",
        "reader": PhbReader
    })
    yield ({
        "description": "Brother Embroidery Format",
        "extension": "phc",
        "extensions": ("phc",),
        "mimetype": "application/x-phc",
        "category": "embroidery",
        "reader": PhcReader
    })
    yield ({
        "description": "Ameco Embroidery Format",
        "extension": "new",
        "extensions": ("new",),
        "mimetype": "application/x-new",
        "category": "embroidery",
        "reader": NewReader
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "max",
        "extensions": ("max",),
        "mimetype": "application/x-max",
        "category": "embroidery",
        "reader": MaxReader
    })
    yield ({
        "description": "Mitsubishi Embroidery Format",
        "extension": "mit",
        "extensions": ("mit",),
        "mimetype": "application/x-mit",
        "category": "embroidery",
        "reader": MitReader
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "pcd",
        "extensions": ("pcd",),
        "mimetype": "application/x-pcd",
        "category": "embroidery",
        "reader": PcdReader
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "pcq",
        "extensions": ("pcq",),
        "mimetype": "application/x-pcq",
        "category": "embroidery",
        "reader": PcqReader
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "pcm",
        "extensions": ("pcm",),
        "mimetype": "application/x-pcm",
        "category": "embroidery",
        "reader": PcmReader
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "pcs",
        "extensions": ("pcs",),
        "mimetype": "application/x-pcs",
        "category": "embroidery",
        "reader": PcsReader
    })
    yield ({
        "description": "Janome Embroidery Format",
        "extension": "jpx",
        "extensions": ("jpx",),
        "mimetype": "application/x-jpx",
        "category": "embroidery",
        "reader": JpxReader
    })
    yield ({
        "description": "Gunold Embroidery Format",
        "extension": "stc",
        "extensions": ("stc",),
        "mimetype": "application/x-stc",
        "category": "embroidery",
        "reader": StcReader
    })
    # yield ({
    #     "description": "Zeng Hsing Embroidery Format",
    #     "extension": "zhs",
    #     "mimetype": "application/x-zhs",
    #     "category": "embroidery",
    #     "reader": ZhsReader
    # })
    yield ({
        "description": "ZSK TC Embroidery Format",
        "extension": "zxy",
        "extensions": ("z00", "z01", "z02"),
        "mimetype": "application/x-zxy",
        "category": "embroidery",
        "reader": ZxyReader
    })
    yield ({
        "description": "Brother Stitch Format",
        "extension": "pmv",
        "extensions": ("pmv",),
        "mimetype": "application/x-pmv",
        "category": "stitch",
        "reader": PmvReader,
        "writer": PmvWriter
    })
    yield ({
        "description": "PNG Format, Portable Network Graphics",
        "extension": "png",
        "extensions": ("png",),
        "mimetype": "image/png",
        "category": "image",
        "writer": PngWriter,
        "write_options": {
            "background": (0x000000, 0xFFFFFF),
            "linewidth": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        },
    })
    yield ({
        "description": "txt Format, Text File",
        "extension": "txt",
        "extensions": ("txt",),
        "mimetype": "text/plain",
        "category": "debug",
        "writer": TxtWriter,
        "versions": ("default", "embroidermodder")
    })
    yield ({
        "description": "gcode Format, Text File",
        "extension": "gcode",
        "extensions": ("gcode", "g-code", "ngc", "nc", ".g"),
        "mimetype": "text/plain",
        "category": "embroidery",
        "reader": GcodeReader,
        "writer": GcodeWriter,
        "write_options": {
            "stitch_z_travel": (5.0, 10.0),
        },
    })
    yield ({
        "description": "Husqvarna Embroidery Format",
        "extension": "hus",
        "extensions": ("hus",),
        "mimetype": "application/x-hus",
        "category": "embroidery",
        "reader": HusReader
    })
    yield ({
        "description": "Edr Color Format",
        "extension": "edr",
        "extensions": ("edr",),
        "mimetype": "application/x-edr",
        "category": "color",
        "reader": EdrReader,
        "writer": EdrWriter
    })
    yield ({
        "description": "Col Color Format",
        "extension": "col",
        "extensions": ("col",),
        "mimetype": "application/x-col",
        "category": "color",
        "reader": ColReader,
        "writer": ColWriter
    })
    yield ({
        "description": "Inf Color Format",
        "extension": "inf",
        "extensions": ("inf",),
        "mimetype": "application/x-inf",
        "category": "color",
        "reader": InfReader,
        "writer": InfWriter
    })
    yield ({
        "description": "Json Export",
        "extension": "json",
        "extensions": ("json",),
        "mimetype": "application/json",
        "category": "debug",
        "reader": JsonReader,
        "writer": JsonWriter
    })


def convert(filename_from, filename_to, settings=None):
    pattern = read(filename_from, settings)
    if pattern is None:
        return
    write(pattern, filename_to, settings)


def get_extension_by_filename(filename):
    """extracts the extension from a filename"""
    return os.path.splitext(filename)[1][1:]


def read_embroidery(reader, f, settings=None, pattern=None):
    """Reads fileobject or filename with reader."""
    if reader is None:
        return None
    if pattern is None:
        pattern = EmbPattern()

    if is_str(f):
        text_mode = False
        try:
            text_mode = reader.READ_FILE_IN_TEXT_MODE
        except AttributeError:
            pass
        if text_mode:
            try:
                with open(f, "r") as stream:
                    reader.read(stream, pattern, settings)
                    stream.close()
            except IOError:
                pass
        else:
            try:
                with open(f, "rb") as stream:
                    reader.read(stream, pattern, settings)
                    stream.close()
            except IOError:
                pass
    else:
        reader.read(f, pattern, settings)
    return pattern


def read_dst(f, settings=None, pattern=None):
    """Reads fileobject as DST file"""
    return read_embroidery(DstReader, f, settings, pattern)


def read_pec(f, settings=None, pattern=None):
    """Reads fileobject as PEC file"""
    return read_embroidery(PecReader, f, settings, pattern)


def read_pes(f, settings=None, pattern=None):
    """Reads fileobject as PES file"""
    return read_embroidery(PesReader, f, settings, pattern)


def read_exp(f, settings=None, pattern=None):
    """Reads fileobject as EXP file"""
    return read_embroidery(ExpReader, f, settings, pattern)


def read_vp3(f, settings=None, pattern=None):
    """Reads fileobject as VP3 file"""
    return read_embroidery(Vp3Reader, f, settings, pattern)


def read_jef(f, settings=None, pattern=None):
    """Reads fileobject as JEF file"""
    return read_embroidery(JefReader, f, settings, pattern)


def read_u01(f, settings=None, pattern=None):
    """Reads fileobject as U01 file"""
    return read_embroidery(U01Reader, f, settings, pattern)


def read_csv(f, settings=None, pattern=None):
    """Reads fileobject as CSV file"""
    return read_embroidery(CsvReader, f, settings, pattern)


def read_gcode(f, settings=None, pattern=None):
    """Reads fileobject as GCode file"""
    return read_embroidery(GcodeReader, f, settings, pattern)


def read_xxx(f, settings=None, pattern=None):
    """Reads fileobject as XXX file"""
    return read_embroidery(XxxReader, f, settings, pattern)


def read(filename, settings=None, pattern=None):
    """Reads file, assuming type by extension"""
    extension = get_extension_by_filename(filename)
    extension = extension.lower()
    for file_type in supported_formats():
        if file_type['extension'] != extension:
            continue
        reader = file_type.get("reader", None)
        return read_embroidery(reader, filename, settings, pattern)
    return None


def write_embroidery(writer, pattern, stream, settings=None):
    if pattern is None:
        return
    if settings is None:
        settings = {}
    else:
        settings = settings.copy()
    try:
        encode = writer.ENCODE
    except AttributeError:
        encode = True

    if settings.get("encode", encode):
        if not ("max_jump" in settings):
            try:
                settings["max_jump"] = writer.MAX_JUMP_DISTANCE
            except AttributeError:
                pass
        if not ("max_stitch" in settings):
            try:
                settings["max_stitch"] = writer.MAX_STITCH_DISTANCE
            except AttributeError:
                pass
        if not ("full_jump" in settings):
            try:
                settings["full_jump"] = writer.FULL_JUMP
            except AttributeError:
                pass
        if not ("round" in settings):
            try:
                settings["round"] = writer.ROUND
            except AttributeError:
                pass
        if not ("writes_speeds" in settings):
            try:
                settings["writes_speeds"] = writer.WRITES_SPEEDS
            except AttributeError:
                pass
        if not ("sequin_contingency" in settings):
            try:
                settings["sequin_contingency"] = writer.SEQUIN_CONTINGENCY
            except AttributeError:
                pass
        if not ("thread_change_command" in settings):
            try:
                settings["thread_change_command"] = writer.THREAD_CHANGE_COMMAND
            except AttributeError:
                pass
        if not ("translate" in settings):
            try:
                settings["translate"] = writer.TRANSLATE
            except AttributeError:
                pass
        if not ("scale" in settings):
            try:
                settings["scale"] = writer.SCALE
            except AttributeError:
                pass
        if not ("rotate" in settings):
            try:
                settings["rotate"] = writer.ROTATE
            except AttributeError:
                pass
        pattern = pattern.get_normalized_pattern(settings)

    if is_str(stream):
        text_mode = False
        try:
            text_mode = writer.WRITE_FILE_IN_TEXT_MODE
        except AttributeError:
            pass
        if text_mode:
            try:
                with open(stream, "w") as stream:
                    writer.write(pattern, stream, settings)
            except IOError:
                pass
        else:
            try:
                with open(stream, "wb") as stream:
                    writer.write(pattern, stream, settings)
            except IOError:
                pass
    else:
        writer.write(pattern, stream, settings)


def write_dst(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(DstWriter, pattern, stream, settings)


def write_pec(pattern, stream, settings=None):
    """Writes fileobject as PEC file"""
    write_embroidery(PecWriter, pattern, stream, settings)


def write_pes(pattern, stream, settings=None):
    """Writes fileobject as PES file"""
    write_embroidery(PesWriter, pattern, stream, settings)


def write_exp(pattern, stream, settings=None):
    """Writes fileobject as EXP file"""
    write_embroidery(ExpWriter, pattern, stream, settings)


def write_vp3(pattern, stream, settings=None):
    """Writes fileobject as Vp3 file"""
    write_embroidery(Vp3Writer, pattern, stream, settings)


def write_jef(pattern, stream, settings=None):
    """Writes fileobject as JEF file"""
    write_embroidery(JefWriter, pattern, stream, settings)


def write_u01(pattern, stream, settings=None):
    """Writes fileobject as U01 file"""
    write_embroidery(U01Writer, pattern, stream, settings)


def write_csv(pattern, stream, settings=None):
    """Writes fileobject as CSV file"""
    write_embroidery(CsvWriter, pattern, stream, settings)


def write_txt(pattern, stream, settings=None):
    """Writes fileobject as CSV file"""
    write_embroidery(TxtWriter, pattern, stream, settings)


def write_gcode(pattern, stream, settings=None):
    """Writes fileobject as Gcode file"""
    write_embroidery(GcodeWriter, pattern, stream, settings)


def write_xxx(pattern, stream, settings=None):
    """Writes fileobject as XXX file"""
    write_embroidery(XxxWriter, pattern, stream, settings)


def write_svg(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(SvgWriter, pattern, stream, settings)


def write_png(pattern, stream, settings=None):
    """Writes fileobject as PNG file"""
    write_embroidery(PngWriter, pattern, stream, settings)


def write(pattern, filename, settings=None):
    """Writes file, assuming type by extension"""
    extension = get_extension_by_filename(filename)
    extension = extension.lower()

    for file_type in supported_formats():
        if file_type['extension'] != extension:
            continue
        writer = file_type.get("writer", None)
        if writer is None:
            continue
        write_embroidery(writer, pattern, filename, settings)


def is_str(obj):
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)
