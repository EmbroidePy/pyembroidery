# pyembroidery

Python library for the reading and writing of embroidery files.
Compatable with Python 2 and 3 Explictly tested with 3.6 and 2.7.

To install:
```bash
pip install pyembroidery
```

Any suggestions or comments please raise an issue.

pyembroidery was originally intended for in inkscape/inkstitch. However, it was entirely coded from the ground up with all projects in mind. It includes a lot of higher level and middle level pattern composition abilities, and accounts for any knowable error. It should be highly robust with a simple api in order to be entirely reasonable for *any* python embroidery project.

It should be complex enough to go very easily from points to stitches, fine grained enough to let you control everything, and good enough that you shouldn't want to.


Mandate
---
pyembroidery must to be small enough to be finished in short order and big enough to pack a punch.

* pyembroidery must read and write: PES, DST, EXP, JEF, VP3.
* pyembroidery must fully support commands: STITCH, JUMP, TRIM, STOP, END, COLOR_CHANGE, SEQUIN_MODE and SEQUIN_EJECT.
* pyembroidery must support and function in Python 2.7

Pyembroidery fully meets and exceeds all of these requirements.
* It writes 9 formats, including the mandated ones.
* It reads 38 formats, including the mandated ones.
* It supports all the core commands where that format can use said command as well as FAST and SLOW for .u01.
* SEQUINS work in all supported formats (.dst) that are known to support sequins. Further it supports SEQUIN to JUMP operations on the other formats.
  * It is currently fully compatable with Python 2.7 and Python 3.6

Philosophy
---
Pyembroidery will always attempt to minimize information loss. Embroidery reading and writing, the exporting and importing of these files, is always lossy. If there is information in a file, it is within the purview of the project (but not the mandate) to read that information and provide it to the user. If information can be written to a file, it is within the purview of the project to write that information to the file or provide means by which that can be done.

* Low level commands: Those commands actually found in binary encoded embroidery files.
    * Low level commands will be transcribed and preserved in their exact order, unless doing so will cause an error.
* Middle level commands: Useful ways of thinking about blocks of low level commands. Commands which describe the way the low level commands are encoded, but are not themselves commands executed by embroidery machines.
    * Middle level commands will be helpful and converted to low-level commands during writing events.
    * These will often be context sensitive converting to slightly different low level commands depending on intended writer, or encoder settings.
* High level commands: Conversion of shapes and fills into useful structures, patterning within stitches, modifiers of structures.
    * High level commands will not exist.

Other reasonable elements:
* Higher level objects like .PES or .THR containing shapes are currently ignored in favor of reading raw stitches, However, loading such things would be less lossy and thus within the scope of the project.
* Conversions from raw low level commands to some middle level interpretations or iterable generators are provided in the EmbPattern class. Additional methods are entirely reasonable feature requests.
   

How it works:
---
Readers are sent a fileobject and an EmbPattern and parses the file, filling in the metadata, threads, stitches.

EmbPattern objects contain all the relevant data. You can iterate stitch blocks .get_as_stitchblocks() or access the raw-stitches, threads, or metadata.

Writers are called to save a pattern to disk. They save raw-stitch data to disk. This data may, however, not be formatted in a way the writer can utilize effectively. For this reason, writers will normalize the data with an encoder.

The encoder encode a low level version of the commands in the pattern, not just from low level but also middle-level commands implemented with the encoder. The writer contain format specific information with which to call to the encoder with some format specific values. Each export will reencode the data for the format, without modifying or altering the original data.

The encoder call can be made directly on the EmbPattern with .get_normalized_pattern() on the pattern, this returns a new pattern. Neither, encoding or saving will modify a pattern. Most operations performed on the data will have some degree of loss. So there is always a level of isolation between all lossy operation converting the pattern.

* Read
  * File -> Reader -> Pattern
* Write
  * Pattern -> Encoder -> Pattern -> Writer -> File
* Convert
  * File -> Reader -> Pattern -> Stablizer -> Pattern -> Encoder -> Pattern -> Writer -> File

Formats:
---

Pyembroidery will write:
* .pes (mandated)
* .dst (mandated)
* .exp (mandated)
* .jef (mandated)
* .vp3 (mandated)
* .pec
* .u01
* .csv
* .svg

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
* .zxy

Writing to SVG:
While not a binary writing format, the testing/debugging utility of SVG is unmatched. There is some notable irony in writing an SVG file in a library, whose main genesis is to help another program that *already* writes them.

Writing to CSV:
Prints out a workable CSV file with the given data. It will be encoded like a .DST file by default.


Reading:
---

```python
import pyembroidery
```

To load a pattern from disk:

```python
pattern = pyembroidery.read("myembroidery.exp")
```

If only a file name is given, pyembroidery will use the extension to determine what reader it should use. 
(In the case of .dat where there are two non-compatable embroidery files with the same extension, the difference is detected by the reader.)

For the discrete readers, the file may be a FileObject or a the string of the path.

```python
pattern = pyembroidery.read_dst(file)
pattern = pyembroidery.read_pec(file)
pattern = pyembroidery.read_pes(file)
pattern = pyembroidery.read_exp(file)
pattern = pyembroidery.read_vp3(file)
pattern = pyembroidery.read_jef(file)
```

You can optionally add settings and pattern to these readers, it will use that pattern and append the new stitches to the end.

```python
# append to an existing pattern
pattern = pyembroidery.read_pes(file, None, pattern)

# or even chain together read calls
pattern = pyembroidery.read("secondread.dst", None, pyembroidery.read("firstread.jef"))
```

This will cause the pattern to have the stitches from both files.


Writing:
---

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
pyembroidery.write_svg(pattern, file)
```

In addition, you can add a dict object to the writer, reader, and converter with various settings.

```python
pyembroidery.write(pattern, file.dst, { "tie_on": True, "tie_off": True, "translate": (40, 50) }
```

The parameters currently have recognized values for:
* `max_stitch`
* `max_jump`
* `full_jump`
* `long_stitch_contingency`
* `sequin_contingency`
* `explicit_trim`
* `translate`
* `scale`
* `rotate`
* `tie_on`
* `tie_off`
* `encode`
* `stable`

The max_stitch, max_jump, full_jump, and sequin_contingency properties are appended by default depending on the format being writing to. For example, DST files support a maximum stitch length of 12.1mm, and this is set automatically. If you set these, they will override those values. If you override them in ways that cannot be accounted for by the reader, it may cause a crash. If you disable the encoder "encode" = False, it may crash. If you disable the stablizer for conversions "stable" = False, it will have less defined behavior. And may may have undefined behavior between specific different formats.

Translate, Scale and Rotate occur in that order. If you need finer grain control over these they can be modified on the fly with middle-level commands.

long_stitch_contingency sets the contingency protocol for when a stitch is longer than the format can encode and how to deal with that event.

sequin_contingency sets the contingency protocol for when sequins exist in a file. By default this tends to be CONTINGENCY_SEQUIN_JUMP converting whatever sequins are in the data into jumps (this can sometimes be restored on various embroidery machines). For .dst files it uses CONTINGENCY_SEQUIN_UTILIZE as the format is able to fully encode sequin data. You may also use CONTINGENCY_SEQUIN_REMOVE to simply remove the commands completely as if they never existed or CONTINGENCY_SEQUIN_STITCH which converts the sequin stitches to stitches. This will look better, but is overtly more lossy.

Explicit Trim sets whether the encoder should overtly include a trim before color change event or not. Default is True. Setting this to false will omit the trim if it is going to perform a color-change action.

Conversion:
---

As pyembroidery is a fully fleshed out reader/writer within the mandate, it also does conversion.

```python
pyembroidery.convert("embroidery.jef", "converted.dst")
```

This will read the embroidery.jef file in JEF format and will export it as converted.dst in DST format.

Internally this stablizes the format:
* Reader -> Pattern -> Pattern.get_stablized_pattern() -> Encoder -> Writer

The stablized pattern clips out the order of the particlar trims, jumps, colorchanges, stops, and turns it into middle-level commands of STITCH, COLOR_BREAK, SEQUENCE_BREAK.

The stablizer can be disabled by setting "stable" to False.

You can perform some finer grain controls like get_pattern_interpolate_trim(), or process the data yourself if you need this information. If there's a completely reasonable way to post-process loaded data that isn't accounted for, raise an issue. This is still an open question.

```python
pyembroidery.convert("embroidery.jef", "converted.dst", {"stable": False})
```

Depending on the formats and files in question this does not have a guarenteed result. It will still use the encoder and should be effective.

You can disable both the stablizer and the encoder:

```python
pyembroidery.convert("embroidery.jef", "converted.dst", {"stable": False, "encode": False})
```


Composing a pattern:
---

* Use core commands to compose a pattern
* Use shorthand commands to compose a pattern
  * `pyembroidery.STITCH`
  * `pyembroidery.SEQUENCE_BREAK`
  * `pyembroidery.COLOR_BREAK`
  * `pyembroidery.FRAME_EJECT`
* Use bulk dump stitchblock
* Mix these different command levels.


The constants for the stitch types are located in the EmbConstants.py

To compose a pattern you will typically use:

```python
import pyembroidery
pattern = pyembroidery.EmbPattern()
pattern.add_stitch_relative(COMMAND, dx, dy)
pattern.add_stitch_absolute(COMMAND, x, y)
pattern.add_command(command)
pattern.add_stitchblock(stitchblock)
```
The relative and absolute markers determine whether the numbers given are relative to the last position or an absolute location. Calling add_command does not update the internal record of position. These are taken as positionless and the x and y are taken as parameters. Adding a command that is explicitly positioned with add_command will have undefined behavior.

NOTE: the order here is `command, x, y`, not `x,y command`. Python is good with letting you omit values at the end. And the command is *always* needed but the dx,dy can be dropped quite reasonably.

For `COMMAND`, you can:
* Use overt low-level commands:
  * `pyembroidery.STITCH`
    * move to position and drop needle once to make a stitch
  * `pyembroidery.JUMP`
    * move to position without dropping needle
  * `pyembroidery.TRIM`
    * trim the thread (for supported machines and file formats)
  * `pyembroidery.COLOR_CHANGE`
  * `pyembroidery.STOP`
    * pause the machine (for applique, thread-change, etc)
  * `pyembroidery.END`
    * end the pattern
  * `pyembroidery.SEQUIN_EJECT`
    * ejects a sequin. These are overtly saved in .dst format. But, can be made to pattern JUMPs in other formats that may be used with various sequin attachments.
  * `pyembroidery.SEQUIN_MODE`
    * turns on sequin mode. this is done automatically for you if you eject a sequin.
  * `pyembroidery.SLOW`
    * .u01 only. Runs the machine in slow mode.
  * `pyembroidery.FAST`
    * .u01 only. Runs the machine in fast mode.

Shorthand function calls for the above are also available.  These all equate to `pattern.add_stitch_relative` calls using the above constants.  You can omit the `dx` and `dy` parameters if the position should not change (especially useful for trim and color change).

```python
pattern.stitch(dx, dy)
pattern.trim()
pattern.color_change()
```

StitchBlocks:
---
Conceptually a lot of embroidery can be thought of as unbroken blocks of stitches. Given the ubiquity of this, pyembroidery allows several methods for manipulating stitchblocks for reading and writing.

A stitch block currently has two parts a block and thread.

The block is a list of lists, with each 3 values. x, y, command. iterable set of objects with stitch.command, stitch.x, stitch.y will also works for adding a stitch block to a pattern. 

If your internal schema is different than this, raise an issue to have it accounted for within pyembroidery.

When a call is made to add_stitchblock(), the thread object is required to whether the current thread is different than the previous one. If a different thread is detected pyembroidery will append a COLOR_BREAK rather than SEQUENCE_BREAK after it adds the stitches into the pattern. Depending on your use case, you could implement this yourself using singular calls to add_stitch_relative() or add_stitch_absolute() and then determine the type of break with COLOR_BREAK or SEQUENCE_BREAK afterwards. No break command will cause it to merge these stitches (likely invoking whatever long_stitch_contingency is needed).


Middle-Level Commands:
----

The middle-level commands, as they currently stand:
* SEQUENCE_BREAK - Break between stitches. Inserts a trim and jumps to the next stitch in the sequence.
* COLOR_BREAK - Breaks between stitches. Changes to the next color (unless called before anything was stitched)
* FRAME_EJECT(x,y) - Breaks the stitches, jumps to the given location, performs a stop, then goes to next stitch accordingly.
* STITCH_BREAK - Next location is jumped to. Existing jumps are reallocated.
* MATRIX_TRANSLATE(tx,ty) - Applies an inline translation shift for the encoder. It will treat all future stitches translated from here.
* MATRIX_SCALE(sx,sy) - Applies an inline scale shift. It will scale by that factor for future stitches.
* MATRIX_ROTATE(r) - Applies an inline rotateion shift. It will rotate by that factor for future stitches (in degrees).
* MATRIX_RESET - Resets the affine transformation matrix.
* OPTION_ENABLE_TIE_ON - Enables Tie_on on the fly.
* OPTION_ENABLE_TIE_OFF - Enables Tie_off on the fly.
* OPTION_DISABLE_TIE_ON - Disables Tie_on on the fly.
* OPTION_DISABLE_TIE_OFF - Disables Tie_off on the fly.
* OPTION_MAX_STITCH_LENGTH(x) - Sets the max stitch length on the fly.
* OPTION_MAX_JUMP_LENGTH(x) - Sets the max jump length on the fly.
* OPTION_EXPLICIT_TRIM - (Default) includes trim command before color-change command explicitly. 
* OPTION_IMPLICIT_TRIM - Sets trim to be implied by the color-change event.
* SEW_TO - STITCH but with forced CONTINGENCY_SEW_TO
* NEEDLE_AT - STITCH but with forced CONTINGENCY_JUMP_NEEDLE
* CONTINGENCY_NONE - Disables long stitch contingency encoding.
* CONTINGENCY_JUMP_NEEDLE - Sets, long stitch contingency to jump the needle to the new position.
* CONTINGENCY_SEW_TO - Sets, long stitch contingency to sew to the new position with interpolated stitches.
* CONTINGENCY_SEQUIN_UTILIZE - sets the equin contingency to use the sequin information.
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

After a load, the pattern will be filled with raw basic stitch data, it's perfectly reasonable call .get_stable_pattern() on this which will make it into a series of stitches, color_breaks, sequence_breaks or get_pattern_interpolate_trim() which will allow you to introduce trim commands after a series of JUMP commands as specified and merge the untrimmed jumps. Or to iterate through the data with .get_as_stitchblocks() which is a generator that will produce stitch blocks from the raw loaded data. The stablized pattern simply makes a new pattern, iterates through the current pattern by the stitchblocks and feeds that into add_stitch_block(). This results in a pattern without any jumps, trims, etc.

STITCH_BREAK

Stitch break is only needed for reallocating jumps. It requires that the long stitch contingency is needle_to for the next stitch and any existing jumps directly afterwards are ignored. This causes the jump sequences to reallocate. If an existing jump sequence exists because it was loaded from a file and fed into a write routine. The write routine may only seek a contingency for the long jumps by providing extra subdivisions, because low level commands are only tweaked if a literal transcription would cause errors. However, calling pattern.get_pattern_merge_jumps() returns a pattern with all sequences of JUMP replaced with a single STITCH_BREAK command which is middle level and converted by the encoder into a series of jumps produced by the encoder rather than directly transcribed from their current sequence.

Stitch Contingency
---
The encoder needs to decide what to do when a stitch is too long. The current modes here are:
* CONTINGENCY_NEEDLE_JUMP (default)
* CONTINGENCY_SEW_TO
* CONTINGENCY_NONE

When a stitch is beyond max_stitch (whether set by the format or by the user) it must deal with this event, however opinions differ as to how what a stitch beyond the maximum should do. If it is your intent that STITCH means SEW_TO this location then setting the stitch contingency to SEW_TO will create a series of stitches until we get to the end location. If you use the command SEW_TO this overtly works like a stitch with CONTINGENCY_SEW_TO. Likewise NEEDLE_AT is the STITCH flavor that jumps to to the end location and then stitches. If you set CONTINGENCY_NONE then no contingency method is used, long stitches are simply fed to the writer as they appear which may throw an error or crash.

Sequin Contingency
---
The enconder needs to decide what to do when there are sequins in a pattern. The current modes here are:
* CONTINGENCY_SEQUIN_UTILIZE - sets the equin contingency to use the sequin information.
* CONTINGENCY_SEQUIN_JUMP - Sets the sequin contingency to call the sequins jumps.
* CONTINGENCY_SEQUIN_STITCH - Sets the sequin contingency to call the sequins stitches.
* CONTINGENCY_SEQUIN_REMOVE - Sets the sequin contingency to remove the commands completely.

Sequins being written into files that do not support sequins can go several ways, the two typical methods are JUMP and STITCH, this means to replace the SEQUIN_EJECTs with JUMP. This will allow some machines to manually enable sequins for a particular section and interpret the JUMPs as stitches. It is known that some Barudan machines have this ability. The other typical mode is STITCH which will preserve viewable structure of the underlying pattern while destroying the information of where the JUMPs were. With the JUMPs some data will appear to be corrupted, with STITCHes the data will look correct except without the sequins but the information is lost and not recoverable. REMOVE is given for completeness, but it calls all SEQUIN_EJECT commands NO OPERATIONS as if they don't appear in the pattern at all.

Units
---
* The core units are 1/10th mm. This is what 1 refers to within most formats, and internally within pyembroidery itself. You are entirely permitted to use floating point numbers. When writing to a format, fractional values will be lost, but this shall happen in such a way to avoid the propagation of error. Relative stitches from position ( 0.0,  0.31 ) of (+5.4, +5.4), (+5.4, +5,4), (+5.4, +5,4) should encode as changes of 5,6 6,5 5,6. Taking the relative distance in the format as the integer change from the last integer position to the new one, maintaining a position as close to the absolute position as possible. All fractional values are considered significant. 

In some read formats the formats themselves have a slightly different unit systems such as .PCD or .MIT these alternative units will be presented seemlessly as 1/10th mm units.

Core Command Ordering
---
Stitch is taken to mean move_position(x,y), needle_strike. Jump is taken to mean move_position(x,y), block_needle_bar. In those orders.
If a format takes stitch to mean needle_strike, move_position(x,y) in that order. The encoder will may insert an extra jump in to avoid stitching an unwanted element. These differences matter, and are accounted for by things like FULL_JUMP in places, and within the formats. However, within the pattern the understanding should be consistently be taken as displace then operation.

Note: This is true for sequin_eject too. DST files are the only currently supported format with sequins and they use dx,dy then command. But, note the sequin is ejected at the destination of the dx dy. It will move, then sequin_eject this is the assumed order. It is also the DST order.

So if write your own pattern and you intend to stitch at the origin and then go somewhere you must `stitch, 0, 0` then `stitch, x, y` if you start by stitching somewhere at x, y. It may insert jump stitches to get you to that location, then stitch at that location.

Coordinate System
---
Fundamentally pyembroidery stores the positions such that the +y direction is down and -y is up (when viewed horizontally) with +x right and -x left. This is consistent with most modern graphics coordinate systems, but this is different from how these values are stored within embroidery formats. pyembroidery reads by flipping the y-axis, and writes by flipping the y-axis (except for SVG which uses the same coordinate system). This allows for seemless reading, writing, and interfacing. The flips occur at the level of the format readers and writers and is not subject to encoding. However encoding with scale of (1, -1) would invert this during the encoding. All patterns are stored such that `top` is in the -y direction and `bottom` is in the +y direction.

All patterns start at the origin point (0,0).

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

This software is in no way derived from or based on Jackson Yee's abandoned 2006 "pyembroidery" project. The name was simply taken from libEmbroidery and written in python and thus a portmanteau of those. I was unaware of the project until after the all the principle work on this project was complete. I apologize for any confusion this may cause.
