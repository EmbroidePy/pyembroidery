# pyembroidery

Python library for the reading and writing of embroidery files.

Compatible with Python 3. Python 2 support was dropped at end-of-life 1-1-2020.


To install:
```bash
pip install pyembroidery
```

Any suggestions or comments please raise an issue on the github.

pyembroidery was coded from the ground up with all projects in mind. It includes a lot of higher level and middle level pattern composition abilities, and should accounts for any knowable error. If you know an error it does not account for, raise an issue. It should be highly robust with a simple api so as to be reasonable for *any* python embroidery project.

It should be complex enough to go very easily from points to stitches, fine grained enough to let you control everything, and good enough that you shouldn't want to.


## Mandate
pyembroidery must to be small enough to be finished in short order and big enough to pack a punch.

* pyembroidery must read and write: PES, DST, EXP, JEF, VP3.
* pyembroidery must fully support commands: STITCH, JUMP, TRIM, STOP, END, COLOR_CHANGE, NEEDLE_SET, SEQUIN_MODE and SEQUIN_EJECT.

Pyembroidery fully meets and exceeds all of these requirements.
* It writes 9 embroidery formats including the mandated ones. 19 different format in total.
* It reads 40 embroidery formats including the mandated ones. 46 different formats in total.
* It supports all the core commands where that format can use said command as well as FAST and SLOW for .u01.
* SEQUINS work in all supported formats (.dst) that are known to support sequins. Further it supports SEQUIN to JUMP operations on the other formats.

Though previously mandated support for Python 2.7, this support was dropped at the end of life for that version. It is highly recommended that you upgrade. A `python27` branch is availible but that branch was merely forked from when the version was supported.


## Philosophy
Pyembroidery will always attempt to minimize information loss. Embroidery reading and writing, the exporting and importing of embroidery files, is always lossy. If there is information in a file, it is within the purview of the project (but not the mandate) to read that information and provide it to the user. If information can be written to a file, it is within the purview of the project to write that information to the file or provide means by which that can be done.

* Low level commands: Those commands actually found in binary encoded embroidery files.
    * Low level commands will be transcribed and preserved in their exact order, unless doing so will cause an error or lose information.
* Middle level commands: Useful ways of thinking about blocks of low level commands. Commands which describe the way the low level commands are encoded, but are not themselves commands executed by embroidery machines.
    * Middle level commands will be helpful and converted to low-level commands during writing events.
    * These will often be context sensitive converting to slightly different low level commands depending on intended writer, or encoder settings.
* High level commands: Conversion of shapes and fills into useful structures, patterning within stitches, modifiers of structures.
    * High level commands will not exist within this project.

Other reasonable elements:
* Higher level objects like .PES or .THR containing shapes are currently ignored in favor of reading raw stitches. However, loading those elements would be less lossy and thus within the scope of the project.
* Conversions from raw low level commands to some middle level interpretations or iterable generators are provided in the EmbPattern class. Additional methods are entirely reasonable feature requests.
* Complex functionality that requires assistance, especially in cases with significant edge conditions, for example merging patterns.
   

## Overview
Readers are sent a fileobject/stream, an EmbPattern and sometimes a settings dict. The reader parses the file, adding in metadata, threads, and stitches with as much valid information as the file contains.

EmbPattern objects contain all relevant data. You can iterate stitch blocks .get_as_stitchblocks() or access the raw-stitches, threads, or metadata.

Writers are called to save a pattern to disk. The writers save raw-stitch data to disk. This data may, however, not be formatted in a way the writer can utilize effectively. For this reason, writers (except lossless csv) utilize the encoder to ensure whatever the data is in the pattern will be presented to the writer in a manner coherent to the writer.

The encoder encode a low level version of the commands in the pattern, not just from low level but also middle-level commands implemented with the encoder. The writer contain format specific information which is given to the encoder. Each export will reencode the data for the format, without modifying or altering the original data, as doing so would be lossy.

The encoder call can be made directly on the EmbPattern with .get_normalized_pattern() on the pattern, this returns a new pattern. Neither encoding, nor saving, will modify a pattern. The either return a new pattern or utilize one provided. Most operations performed on the data will have some degree of loss, so there is a level of isolation between lossy operation converting the pattern.

* Read
  * File -> Reader -> Pattern
* Write
  * Pattern -> Encoder -> Pattern -> Writer -> File
* Convert
  * File -> Reader -> Pattern -> Encoder -> Pattern -> Writer -> File

## EmbPattern
EmbPattern objects contain three primary elements:
* `stitches`: This is a `list` of lists of three elements [x, y, command]
* `threadlist`: This is a `list` of EmbThread class objects.
* `extras`: This is a `dict` of various types of things that were found or referenced within the reading or desired for the writing of the file such as metadata info about the label declared within a file or some internal 1 bit graphics found within the embroidery file.

### EmbPattern Stitches
The stitches contain absolute locations x, y and command. Commands are found defined within the EmbConstant.py file and should be referenced by name rather than value. The commands are the lower 8 bits of the command value. The upper bits of the command values are reserved for additional information (See Thread Changes). For best practices these should be masked off `stitch[stitch_index][2] & COMMAND_MASK`. 

### EmbPattern Threadlist
The threadlist is a reference table of threads and the information about those threads. By default, if not explicitly specified, the threadlist is utilized in the order given. Prior to `pyembroidery` version 1.3, this was the only method to use these. Usually is it sufficient to provide a thread for each color change in the sequence. However, if a color is not provided one, one will be invented when writing to a format that requires one. In some cases like .dst files, no colors exists so this will simply be ignored (except if extended headers are requested as those give a color sequence). The colors are checked and validated during the encoding process, so specifying these elements with greater detail is explicitly possible. See Thread Changes for more details.

### EmbPattern Extras
This can largely be ignored except in cases when the metadata within the file matters. If for example you wish to read files and find the label that exists inside many different embroidery file times, the resulting value will be put into extras. This is to store the metadata and sometimes transfer the metadata from one format type to another. So an internal label might be able to be transferred between a .dst file and .pes file without regard to the external file name. Or the 1-bit images within a PEC file could be viewed.


## Thread Changes
Some formats do not explicitly use a `COLOR_CHANGE` command, some of them use `NEEDLE_SET` in order to change the thread. The difference here is notable. A color change goes to the next needle in a list usually set within the machine or within the file for the next color of thread. However, some machines like Barudan use what is most properly a needle change. They do not specify the color, but explicitly specifies the needle to be used. This often means the current needle is set at the start. But, if omitted most machines use the current needle set in the machine. Setting the same needle again will produce no effect. Color changes occur between different thread usages, but needle sets occur at the start of each needle usage. Calling for a color change, requires that something be changed, and the machine often stopped. Calling for a needle_set may set the value to the current needle.

When data is loaded from a source with needle set commands. These `NEEDLE_SET` commands are explicitly used rather than color changes as they more accurately represent the original intent of the file. During a write, the encoder will transcribe these in the way requested by the writer settings (as determined by the format itself), using the correct thread change command indicated and accounting for the implicit differences.

There are some cases where one software suite will encode U01 (Barudan formatting with needle sets) commands such that, rather than using needle set, it simply uses `STOP` commands (technically in this case C00 or needle #0), while other software will cycle through a list of a few needles, indicating more explicitly these are changes.

There is some ambiguity as to whether the same needle will have the same thread. Whether needle_set=1, needle_set_2, needle_set=1... means use a new color each time, or whether the second "needle_set=1" indicates that we are going back to the first needle with the first thread, or the first needle with a different thread. Pyembroidery therefore makes no affirmative stance as to the meaning indicated here.

In order to properly encode this information, commands with higher level bits sets are `COLOR_CHANGE`, `NEEDLE_SET`, `COLOR_BREAK`, `SET_CHANGE_SEQUENCE` and these encode the color being changed to or the needle being changed to. `0bnnnnnnnnttttttttcccccccc` where `n` is a bit encoding needle and `t` is a bit encoding thread and `c` is a bit encoding command. The `EmbFunctions.py` file contains helper functions for `encode_thread_change` and `decode_embroidery_command` to parse these commands for you. In all cases, `None` for a value means that there is no information about this. So, for example, a `DST` loaded `COLOR_CHANGE` will equal `COLOR_CHANGE unknown thread, unknown needle`. This allows the command sequence to explicitly declare that the information is not known, or to give the value if the value is known.

There is a middle level command, `SET_CHANGE_SEQUENCE` that can be used to preset (or with an order value, postset) the thread change sequence.

`encode_thread_change(SET_CHANGE_SEQUENCE,17)` would, for example, make the first color change switch to the Threadlist index 17. After this, the subsequent color changes would be to index 0, index 1, index 2, ... etc.

There are some other use cases when writing this data out, you could, for example, make the threadlist equal to all the threads you have available and declare their usages simply reference the relevant thread index. To do this you would add all your threads, then at the start of the commands declare a group of SET_CHANGE_SEQUENCE commands to set the order you want. Or to use `COLOR_BREAK`s encoded with the order you desire.

In most cases this information isn't going to matter, but it is provided because it is information sometimes contained within the embroidery file. For writing this information, there are quite often other ways to specify it, but `pyembroidery` tends to be overbuilt by design to capture most known and unknown usecases.

## File I/O

### Embroidery Formats:

Pyembroidery will write:
* .pes (mandated)
* .dst (mandated)
* .exp (mandated)
* .jef (mandated)
* .vp3 (mandated)
* .u01
* .pec
* .xxx
* .gcode

Pyembroidery will read:
* .pes (mandated)
* .dst (mandated)
* .exp (mandated)
* .jef (mandated)
* .vp3 (mandated)
* .10o
* .100
* .bro
* .dat (barudan & sunstar)
* .dsb
* .dsz
* .emd
* .exy
* .fxy
* .gt
* .hus
* .inb
* .jpx
* .ksm
* .max
* .mit
* .new
* .pcd
* .pcm
* .pcq
* .pcs
* .pec
* .phb
* .phc
* .sew
* .shv
* .stc
* .stx
* .tap
* .tbf
* .u01
* .xxx
* .zhs
* .zxy
* .gcode

### Related Formats
Pyembroidery includes some related formats like pure color formats that can be loaded as helpers for formats without colors. Or .pmv which is a stitch pattern format for Brother sewing machines.

Pyembroidery will write:
* .col : Color format.
* .edr : Color format.
* .inf : Color format.
* .pmv : Brother Stitch Format.

Pyembroidery will read:
* .col : Color format.
* .edr : Color format.
* .inf : Color format.
* .pmv : Brother Stitch Format.


### Utility Formats:
CSV and JSON are the two primary forms of lossless saving formats. PNG is an image format, txt output is sometimes used for easy parsing. And SVG is an open source interchange format for vectors.

Pyembroidery will write:
* .csv : comma-separated values 
* .json : JavaScript Object Notation
* .png : Portable Network Graphic
* .txt : text file.
* .svg : Scalable Vector Graphics

Pyembroidery will read:
* .csv : comma-separated values 
* .json : JavaScript Object Notation


#### Versions
Formats within .get_supported_formats() in pyembroidery provides an element called 'versions' this will contain a tuple of values which can be passed to the settings object as `{'version': <my version>}`. This provides version controls for the types of outputs provided within each writer. For example, there is an extended header version of dst called `extended`, there's `6` and `6t` in the PesWriter which exports other and different versions of the file. 

This is intended as a good method to create new versions. For example, gcode can control a many things, but varies greatly from one purpose to another and would be ideal for different versions. There are also different embroidery machines which may require different tweaks. Versions is the intended method to deliver machine specific files.

#### Writing to CSV:
Prints out a workable CSV file with the given data. Starting in 1.3 the csv patterns are written without being encoded. The CSV format is, in this form, lossless. If you wish to encode before you write the file you can set the encoder to True and override the default.

`write_csv(pattern, "file.csv", {"encode": True})`


#### Reading/Writing to JSON:
Saves the pattern as a JSON object. This is intended to be useful as an interchange format since JSON is the most common data interchange format availible currently. 


#### Writing to PNG:
Writes to a image/png file.


#### Writing to TXT:
Writes to a text file. Generally lossy, it does not write threads or metadata, but certainly more easily parsed for a number of homebrew applications. The "mimic" option should mimic the embroidermodder functionality for exporting to txt files. By default it exports a bit less lossy giving the proper command indexes and their explicit names.


#### Writing to Gcode:
The Gcode is intended for a number of hobbyist projects that use a gcode controller to operate a sewing machine, usually X,Y for plotter and Z to turn the handwheel. However, if you have a hobbiest project and need a different command structure feel free to ask or discuss it by raising an issue. Other gcode versions should be able to be added through the versions method.


#### Reading from HUS:
The HUS format requires an obscure and defunct form of compression. The EmbCompress performs this decompression. It is written from the ground up in pure python. It does not require any compiled element or dll file. It has no obfuscation and is intended to be easily understood.


### Reading

```python
import pyembroidery
```

To load a pattern from disk:

```python
pattern = pyembroidery.read("myembroidery.exp")
```

If only a file name is given, pyembroidery will use the extension to determine what reader it should use. 
(In the case of .dat where there are two non-compatible embroidery files with the same extension, the difference is detected by the reader.)

For the discrete readers, the file may be a FileObject or the string of the path.

```python
pattern = pyembroidery.read_dst(file)
pattern = pyembroidery.read_pec(file)
pattern = pyembroidery.read_pes(file)
pattern = pyembroidery.read_exp(file)
pattern = pyembroidery.read_vp3(file)
pattern = pyembroidery.read_jef(file)
pattern = pyembroidery.read_xxx(file)
pattern = pyembroidery.read_csv(file)
pattern = pyembroidery.read_gcode(file)
```

You can optionally add settings and pattern to these readers, it will use that pattern and append the new stitches to the end.

```python
# append to an existing pattern
pattern = pyembroidery.read_pes(file, None, pattern)

# or even chain together read calls
pattern = pyembroidery.read("secondread.dst", None, pyembroidery.read("firstread.jef"))
```
*NOTE*: The merged pattern will still have an `END` command at the end of the first loaded pattern.

If you intend to write the merged pattern as a single unended pattern, convert the `END` commands to `NO_COMMAND` commands.
```python
 for stitch in pattern.get_match_commands(pyembroidery.END):
  stitch[2] = pyembroidery.NO_COMMAND
```

## Writing

To write to a pattern do disk:

```python
pyembroidery.write(pattern,"myembroidery.dst")
```

For the discrete writers, the file may be a FileObject or a string of the path. It does not need to know the filename to judge the extension.

```python
pyembroidery.write_dst(pattern, file)
pyembroidery.write_pec(pattern, file)
pyembroidery.write_pes(pattern, file)
pyembroidery.write_exp(pattern, file)
pyembroidery.write_vp3(pattern, file)
pyembroidery.write_jef(pattern, file)
pyembroidery.write_u01(pattern, file)
pyembroidery.write_svg(pattern, file)
pyembroidery.write_csv(pattern, file)
pyembroidery.write_xxx(pattern, file)
pyembroidery.write_png(pattern, file)
pyembroidery.write_txt(pattern, file)
pyemboridery.write_gcode(pattern,file)
```

In addition, you can add a `dict` object to the writer, reader, and converter with various settings.

```python
pyembroidery.write(pattern, file.dst, { "tie_on": CONTINGENCY_TIE_ON_THREE_SMALL, "tie_off": CONTINGENCY_TIE_OFF_THREE_SMALL, "translate": (40, 50) }
```

The parameters currently have recognized values for:
* `max_stitch`
* `max_jump`
* `full_jump`
* `round`
* `needle_count`
* `thread_change_command`
* `long_stitch_contingency`
* `sequin_contingency`
* `tie_on`
* `tie_off`
* `explicit_trim`
* `writes_speeds`
* `translate`
* `scale`
* `rotate`
* `encode`

The max_stitch, max_jump, full_jump, round, needle_count, thread_change_command, and sequin_contingency properties are appended by default depending on the format being written. For example, DST files support a maximum stitch length of 12.1mm, and this is set automatically. If you set these explicitly, (eg:`{"max_stitch": 2000}`) they will override format values. If overridden or if you disable the encoder (`{"encode": False}`) and the pattern contains values that cannot be accounted for by the reader/writer, it may raise and uncaught issue.

`translate`, `scale` and `rotate` occur in that order. If you need finer grain control over these they can be modified on the fly with middle-level commands. `pattern.add_command(MATRIX_TRANSLATE, 40, 40)`

`long_stitch_contingency` sets the contingency protocol for when a stitch is longer than the format can encode and how to deal with that event.

`sequin_contingency` sets the contingency protocol for when sequins exist in a pattern. By default this tends to be `CONTINGENCY_SEQUIN_JUMP` converting whatever sequins are in the data into jumps (this can sometimes be restored on various embroidery machines). For .dst files it uses `CONTINGENCY_SEQUIN_UTILIZE` as the format is able to fully encode sequin data. You may also use `CONTINGENCY_SEQUIN_REMOVE` to simply remove the commands completely as if they never existed or `CONTINGENCY_SEQUIN_STITCH` which converts the sequin stitches to stitches. This will look better, but is more lossy.

`tie_on` sets the contingency protocol for when a tie_on is needed. This can either be `CONTINGENCY_TIE_ON_THREE_SMALL` which uses three small stitches to tie on the thread or `CONTINGENCY_TIE_ON_NONE` which does not perform a tie_on.

`tie_off` sets the contingency protocol for when a tie_off is needed. This can either be `CONTINGENCY_TIE_OFF_THREE_SMALL` which uses three small stitches to tie off the thread or `CONTINGENCY_TIE_OFF_NONE` which does not perform a tie_off.

Explicitly calling TIE_ON or TIE_OFF within the command sequence performs the set contingency so if this is set to `CONTINGENCY_TIE_OFF_NONE` these will perform no action. These could be modified on the fly by adding a command for `CONTINGENCY_TIE_OFF_THREE_SMALL` to toggle the value on the fly.

`explicit_trim` sets whether the encoder should overtly include a trim before color change event or not. Default is False. Setting this to True will include a trim if we are going to perform a thread-change action.

## Manipulation

There are many fully qualified methods of manipulating patterns. For example if you want to add a pattern to another pattern,
```python
pattern1 += pattern2
```

You can also do pattern3 = pattern1 + pattern2 but that requires making an new pattern. With the `__iadd__()` dunder you can also perform actions like adding a colorchange.

`pattern1 += "red"` will add a color change (if correct to do so), and a red thread to the threadlist.

Other elements like `pattern += ((0,0), (20,20), (0,0))` will also work to append stitches.

You can get a particular stitch of the pattern using `pattern[0]`. You can set string metadata elements `pattern['name'] = "My Design"`

## Conversion

As pyembroidery is a fully fleshed out reader/writer within the mandate, it also does conversion.

```python
pyembroidery.convert("embroidery.jef", "converted.dst")
```

This will read the embroidery.jef file in JEF format and will export it as converted.dst in DST format.

* Reader -> Pattern -> Encoder -> Writer

You can load the file and call some of the helper functions to process the data like, get_pattern_interpolate_trim(), or get_stablized_pattern(). If there's a completely reasonable way to post-process loaded data that isn't accounted for raise an issue. This is still an open question. Since 1.3 the improved conversion testing means most conversions should overtly work.

## Composing a pattern

* Use core commands to compose a pattern
* Use shorthand commands to compose a pattern
  * `STITCH`
  * `SEQUENCE_BREAK`
  * `COLOR_BREAK`
  * `FRAME_EJECT`
* Use bulk dump stitchblock
* Mix these different command levels.

The constants for the stitch types are located in the EmbConstants.py

To compose a pattern you will typically use:

```python
from pyembroidery import *
pattern = EmbPattern()
pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
write_dst(pattern, "file.dst")
```

You can also add relative and command values to the list.
```python
pattern.add_stitch_relative(STITCH, dx, dy)
pattern.add_stitch_absolute(JUMP, x, y)
pattern.add_command(command)
```

You can insert a relative stitch inside a pattern. Note that it is relative to the stitch it's being inserted at. This will cause problems if that is a command without x, y operands.
```python
pattern.trim(position=48)
```

The relative and absolute markers determine whether the numbers given are relative to the last position or an absolute location. Calling add_command does not update the internal record of position. These are taken as positionless and the x and y are taken as parameters. Adding a command that is explicitly positioned with add_command will have undefined behavior.

NOTE: the order here is `command, x, y`, not `x, y command`. Python is good with letting you omit values at the end. And the command is *always* needed but the dx, dy can be dropped quite reasonably. While internally these are stored as [x, y, command] mostly to facilitate using them directly as positions.

For `COMMAND`, you can:
* Use overt low-level commands:
  * `STITCH`
    * move to position and drop needle once to make a stitch
  * `JUMP`
    * move to position without dropping needle
  * `TRIM`
    * trim the thread (for supported machines and file formats)
  * `COLOR_CHANGE`
  * `STOP`
    * pause the machine (for applique, thread-change, etc)
  * `NEEDLE_SET`
    * changes the needle being used on the machine, if set to current needle it will ignore.
  * `END`
    * end the pattern
  * `SEQUIN_EJECT`
    * ejects a sequin. These are overtly saved in .dst format. But, can be made to pattern JUMPs in other formats that may be used with various sequin attachments.
  * `SEQUIN_MODE`
    * turns on sequin mode. this is done automatically for you if you eject a sequin.
  * `SLOW`
    * .u01 only. Runs the machine in slow mode.
  * `FAST`
    * .u01 only. Runs the machine in fast mode.

Shorthand function calls for the above are also available.  These all equate to `pattern.add_stitch_relative` calls using the above constants.  You can omit the `dx` and `dy` parameters if the position should not change (especially useful for trim and color change).

```python
pattern.stitch(dx, dy)
pattern.trim()
pattern.color_change()
```

## StitchBlocks

Conceptually a lot of embroidery can be thought of as unbroken blocks of stitches. Given the ubiquity of this, pyembroidery allows several methods for manipulating stitchblocks for reading and writing.

The stitches within pyembroidery are a list of lists, with each 3 values. x, y, command. The stitchblocks given by commands like .get_as_stitchblock() are subsections of this. For adding stitches like with .add_stitchblock(), iterable set of objects with stitch.command, stitch.x, stitch.y will also works for adding a stitch block to a pattern. 

.add_block():
---
.add_block() takes a lot of other types:

The first parameter is the block with the following formats allowed:
* a list of lists, either 2 or 3 long.
* a list of tuple
* a tuple of tuples
* a list of complex
* a tuple of complex
* a list of integers `[x0,y0,x1,y1,x2,y2,x3,y3,...]`
* a list of floats `[x0,y0,x1,y1,x2,y2,x3,y3,...]`

The second parameter is the thread. The threads are equally agnostic as to what they take.
* EmbThread object
* int (color in 0xRRBBGG)
* `dict` with values for:
   * "name"
   * "description"
   * "desc"
   * "brand"
   * "manufacturer"
   * "color", can be int, hex_string ("#ff00ff","#f0f"), tuple (255,0,255), explicit color name ("red")
   * "hex", overt hex color, may omit the '#'
   * "id", catalog number
   * "catalog", same
* `str` string value of the color, either hex color or explicit color name. 

(Note: explicit color names are those found in the X11/CSS/SVG named colors)

```python
pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
pattern.add_block([0, 0, 0, 100, 100, 100, 100, 0, 0, 0], "#f00")
```

When a call is made to add_stitchblock(), the thread object is required to know whether the current thread is different than the previous one. If a different thread is detected pyembroidery will append a COLOR_BREAK rather than SEQUENCE_BREAK after adding the stitches into the pattern. Depending on your use case, you could implement this yourself using singular calls to add_stitch_relative() or add_stitch_absolute() and then determine the type of break with COLOR_BREAK or SEQUENCE_BREAK afterwards.


### Middle-Level Commands:

The middle-level commands, as they currently stand:
* SET_CHANGE_SEQUENCE - Sets the thread change sequence according to the encoded values. Setting the needle, thread-color, and order of where this occurs. See Thread Changes for more info.
* SEQUENCE_BREAK - Break between stitches. Inserts a trim and jumps to the next stitch in the sequence.
* COLOR_BREAK - Breaks between stitches. Changes to the next color (unless called before anything was stitched)
* FRAME_EJECT(x,y) - Breaks the stitches, jumps to the given location, performs a stop, then goes to next stitch accordingly.
* STITCH_BREAK - Next location is jumped to. Existing jumps are reallocated.
* MATRIX_TRANSLATE(tx,ty) - Applies an inline translation shift for the encoder. It will treat all future stitches translated from here.
* MATRIX_SCALE_ORIGIN(sx,sy) - Applies an inline scale shift. It will scale by that factor for future stitches. Against the origin (0,0)
* MATRIX_ROTATE_ORIGIN(r) - Applies an inline rotation shift. It will rotate by that factor for future stitches (in degrees). Against the origin (0,0)
* MATRIX_SCALE(sx,sy) - Applies an inline scale shift. It will scale by that factor for future stitches. Scaling based on current point.
* MATRIX_ROTATE(r) - Applies an inline rotation shift. It will rotate by that factor for future stitches (in degrees).
* MATRIX_RESET - Resets the affine transformation matrix.
* OPTION_MAX_STITCH_LENGTH(x) - Sets the max stitch length on the fly.
* OPTION_MAX_JUMP_LENGTH(x) - Sets the max jump length on the fly.
* OPTION_EXPLICIT_TRIM - (Default) includes trim command before color-change command explicitly. 
* OPTION_IMPLICIT_TRIM - Sets trim to be implied by the color-change event.
* CONTINGENCY_TIE_ON_THREE_SMALL - Enables Tie_on on the fly.
* CONTINGENCY_TIE_ON_NONE - Enables Tie_off on the fly.
* CONTINGENCY_TIE_OFF_THREE_SMALL - Disables Tie_on on the fly.
* CONTINGENCY_TIE_OFF_NONE - Disables Tie_off on the fly.
* SEW_TO - STITCH but with forced CONTINGENCY_SEW_TO
* NEEDLE_AT - STITCH but with forced CONTINGENCY_JUMP_NEEDLE
* CONTINGENCY_LONG_STITCH_NONE - Disables long stitch contingency encoding.
* CONTINGENCY_LONG_STITCH_JUMP_NEEDLE - Sets, long stitch contingency to jump the needle to the new position.
* CONTINGENCY_LONG_STITCH_SEW_TO - Sets, long stitch contingency to sew to the new position with interpolated stitches.
* CONTINGENCY_SEQUIN_UTILIZE - sets the sequin contingency to use the sequin information.
* CONTINGENCY_SEQUIN_JUMP - Sets the sequin contingency to call the sequins jumps.
* CONTINGENCY_SEQUIN_STITCH - Sets the sequin contingency to call the sequins stitches.
* CONTINGENCY_SEQUIN_REMOVE - Sets the sequin contingency to remove the commands completely.

Note: these do not need to have a 1 to 1 conversion to stitches. Many have 1 to 0 and trigger changes in states for the encoder, or the matrix being used to filter the locations, or specific higher level commands.

The could can be made to do a lot at the encoder level. If something is needed and within scope of the project, raise an issue.

---

COLOR_BREAK and SEQUENCE_BREAK:

The main two middle-level commands simply serve as dividers for series of stitches.
* pattern.command(COLOR_BREAK)
* (add a bunch of stitches)
* pattern.command(SEQUENCE_BREAK)
* (add a bunch of stitches)
* pattern.command(COLOR_BREAK)
* (add a bunch of stitches)
* pattern.command(SEQUENCE_BREAK)

The encoder will by default ignore any COLOR_BREAK that occurs before any stitches have been put down, or sequence or color breaks would occur after all stitching has happened. So you don't have to worry about the order you put them in. They work expressly as breaks that divide one block of stitches from another, and gives information as to whether this change also requires we use a new color.

You can expressly add any of the core commands to the patterns. These are generalized and try to play nice with other commands. When the patterns are written to disk, they call pattern.get_normalized_pattern() and save the normalized pattern. Saving to any format does not modify the pattern, ever. It writes the modified pattern out. It adds the max_jump and max_stitch to the encoding when it normalizes this to save. So each format can compile to a different set of stitches due to the max_jump etc. This is expressly an attempt to maintain as much data integrity as possible.

After a load, the pattern will be filled with raw basic stitch data, it's perfectly reasonable call .get_stable_pattern() on this which will make it into a series of stitches, color_breaks, sequence_breaks or get_pattern_interpolate_trim() which will allow you to introduce trim commands after a series of JUMP commands as specified and merge the untrimmed jumps. Or to iterate through the data with .get_as_stitchblocks() which is a generator that will produce stitch blocks from the raw loaded data. The stabilized pattern simply makes a new pattern, iterates through the current pattern by the stitchblocks and feeds that into add_stitch_block(). This results in a pattern without any jumps, trims, etc.

STITCH_BREAK

Stitch break is only needed for reallocating jumps. It requires that the long stitch contingency is needle_to for the next stitch and any existing jumps directly afterwards are ignored. This causes the jump sequences to reallocate. If an existing jump sequence exists because it was loaded from a file and fed into a write routine. The write routine may only seek a contingency for the long jumps by providing extra subdivisions, because low level commands are only tweaked if a literal transcription would cause errors. However, calling pattern.get_pattern_merge_jumps() returns a pattern with all sequences of JUMP replaced with a single STITCH_BREAK command which is middle level and converted by the encoder into a series of jumps produced by the encoder rather than directly transcribed from their current sequence.

### Stitch Contingency

The encoder needs to decide what to do when a stitch is too long. The current modes here are:
* CONTINGENCY_NEEDLE_JUMP (default)
* CONTINGENCY_SEW_TO
* CONTINGENCY_NONE

When a stitch is beyond max_stitch (whether set by the format or by the user) it must deal with this event, however opinions differ as to how what a stitch beyond the maximum should do. If it is your intent that STITCH means SEW_TO this location then setting the stitch contingency to SEW_TO will create a series of stitches until we get to the end location. If you use the command SEW_TO this overtly works like a stitch with CONTINGENCY_SEW_TO. Likewise NEEDLE_AT is the STITCH flavor that jumps to to the end location and then stitches. If you set CONTINGENCY_NONE then no contingency method is used, long stitches are simply fed to the writer as they appear which may throw an error or crash.

### Sequin Contingency

The encoder needs to decide what to do when there are sequins in a pattern. The current modes here are:
* CONTINGENCY_SEQUIN_UTILIZE - sets the sequin contingency to use the sequin information.
* CONTINGENCY_SEQUIN_JUMP - Sets the sequin contingency to call the sequins jumps.
* CONTINGENCY_SEQUIN_STITCH - Sets the sequin contingency to call the sequins stitches.
* CONTINGENCY_SEQUIN_REMOVE - Sets the sequin contingency to remove the commands completely.

Sequins being written into files that do not support sequins can go several ways, the two typical methods are JUMP and STITCH, this means to replace the SEQUIN_EJECTs with JUMP. This will allow some machines to manually enable sequins for a particular section and interpret the JUMPs as stitches. It is known that some Barudan machines have this ability. The other typical mode is STITCH which will preserve viewable structure of the underlying pattern while destroying the information of where the JUMPs were. With the JUMPs some data will appear to be corrupted, with STITCHes the data will look correct except without the sequins but the information is lost and not recoverable. REMOVE is given for completeness, but it calls all SEQUIN_EJECT commands NO OPERATIONS as if they don't appear in the pattern at all.

### Tie On / Tie Off Contingency

While there's only NONE, and THREE_SMALL for contingencies currently, both the tie-on and tie-off contingencies are setup to be forward compatible with other future potential tie-on and tie-off methods.

### Units

* The core units are 1/10th mm. This is what 1 refers to within most formats, and internally within pyembroidery itself. You are entirely permitted to use floating point numbers. When writing to a format, fractional values will be lost, but this shall happen in such a way to avoid the propagation of error. Relative stitches from position ( 0.0,  0.31 ) of (+5.4, +5.4), (+5.4, +5,4), (+5.4, +5,4) should encode as changes of 5,6 6,5 5,6. Taking the relative distance in the format as the integer change from the last integer position to the new one, maintaining a position as close to the absolute position as possible. All fractional values are considered significant. 

In some read formats the formats themselves have a slightly different unit systems such as .PCD or .MIT these alternative units will be presented seemlessly as 1/10th mm units.

### Core Command Ordering

Stitch is taken to mean move_position(x,y), needle_strike. Jump is taken to mean move_position(x,y), block_needle_bar. In those orders.
If a format takes stitch to mean needle_strike, move_position(x,y) in that order. The encoder will may insert an extra jump in to avoid stitching an unwanted element. These differences matter, and are accounted for by things like FULL_JUMP in places, and within the formats. However, within the pattern the understanding should be consistently be taken as displace then operation.

Note: This is true for sequin_eject too. DST files are the only currently supported format with sequins and they use dx,dy then command. But, note the sequin is ejected at the destination of the dx dy. It will move, then sequin_eject this is the assumed order. It is also the DST order.

So if write your own pattern and you intend to stitch at the origin and then go somewhere you must `stitch, 0, 0` then `stitch, x, y` if you start by stitching somewhere at x, y. It may insert jump stitches to get you to that location, then stitch at that location.

### Coordinate System

Fundamentally pyembroidery stores the positions such that the +y direction is down and -y is up (when viewed horizontally) with +x right and -x left. This is consistent with most modern graphics coordinate systems, but this is different from how these values are stored within embroidery formats. pyembroidery reads by flipping the y-axis, and writes by flipping the y-axis (except for SVG which uses the same coordinate system). This allows for seamless reading, writing, and interfacing. The flips occur at the level of the format readers and writers and is not subject to encoding. However encoding with scale of (1, -1) would invert this during the encoding. All patterns are stored such that `top` is in the -y direction and `bottom` is in the +y direction.

All patterns start at the origin point (0,0). In keeping with the philosophy the absolute positioning of the data is maintained sometimes this means it an off-center pattern will move from the origin to an absolute position some distance from the origin. While this preserves information, it might also not be entirely expected at times. This `pattern.move_center_to_origin()` will lose that information and center the pattern at the origin.

---

This code is based on Embroidermodder/MobileViewer Java code,
Which in turn is based on Embroidermodder/libembroidery C++ code.

Thanks to,
* The Embroidermodder Team
* Josh Varga
* Jonathan Greig redteam316
* fabriciocouto
* frno7
* Trever Adams
* Rudolfo @ http://www.achatina.de/sewing/main/TECHNICL.HTM
* wwderw
* Purple-bobby
* Jason Weiler
* And the countless other people who put forward good works in figuring out these formats, and those who may yet do so. 

---

This software is in no way derived from or based on Jackson Yee's abandoned 2006 "pyembroidery" project. The name was simply taken from libEmbroidery and written in python and thus a portmanteau of those. I was unaware of the project until after the all the principal work on this project was complete. I apologize for any confusion this may cause.
