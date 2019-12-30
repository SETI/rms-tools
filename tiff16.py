#!/usr/bin/python3
################################################################################
# tiff16.py
#
# Simple method WriteTiff16() to write a numpy array as a 16-bit uncompressed
# tiff, in grayscale, RGB color or palette color.
#
# Associated method ReadTiff16() is not a general implementation of the Tiff
# standard; however, it will successfully read 16-bit Tiffs written by
# WriteTiff16().
#
# Note, however, that 16-bit palette color is not widely supported. For this
# reason, a "translate" option is provided, which converts palette color to RGB.
#
# Mark R. Showalter, SETI Institute, July 2009
################################################################################

from __future__ import print_function

import sys, os
import numpy as np
from struct import *
from PIL import Image

def WriteTiff16(filename, array, palette=None, up=False, byteorder="native",
                translate=True, transpose=None):
    """Writes a 16-bit TIFF file based on the contents of a 2-D or 3-D array.
    Three TIFF formats are supported: grayscale, RGB, and palette.
    
    Inputs:
        filename = the name of the file to write.

        array = a numpy 2-D or 3-D array containing the image pixels. These are
                converted to unsigned 16-bit values if they are not already in
                that format. The order of the indices in the array is expected
                to be (line, sample, band). The third axis is optional. If it
                is present, and the size is >= 3, and no palette is provided,
                then array slices [:,:,0:2] are interpreted as the (R,G,B)
                values for the color of each pixel, ranging from 0 to 65535.
                Otherwise, the value of slice [:,:,0:2] is used as a grayscale
                value or is mapped through the palette to provide color.

        palette = an optional numpy array of shape (65536,3). Values are
                converted to unsigned two-byte integers if they are not in that
                format already. If this palette is provided, then the 0th band
                of the array is used as an index into the palette to derive the
                pixel's (R,G,B) triple. Otherwise, the array values themselves
                are interpreted as grayscale or RGB colors.

        up = True for the line numbers of the image to increase upward; False if
                they are to increase downward. False (downward) is the default.

        byteorder = "native", "little" or "big". This defines the byte ordering
                to be used in the TIFF file. "native" is the default.

        translate = True to translate the image to RGB foromat if a palette has
                been provided. This is the default behavior because many TIFF
                readers do not support 16-bit palettes. If false, the file is
                written using palette color, meaning that the grayscale image
                and palette are stored in the file instead all the RGB values.

        transpose = an optional geometric transformation to perform on the image
                before writing it. Options are designed to match the transpose()
                options in the PIL library. Choices are:
                        Image.FLIP_LEFT_TO_RIGHT
                        Image.FLIP_TOP_BOTTOM
                        Image.ROTATE_90
                        Image.ROTATE_180
                        Image.ROTATE_270
        """

    # Open the output file
    f = open(filename, "wb")

    # Flip if line numbers increase upward
    if up: array = np.flipud(array)

    # Apply transpose operation if needed
    if transpose == Image.FLIP_LEFT_RIGHT: array = np.fliplr(array)
    if transpose == Image.FLIP_TOP_BOTTOM: array = np.flipud(array)
    if transpose == Image.ROTATE_90:       array = np.rot90(array,1)
    if transpose == Image.ROTATE_180:      array = np.rot90(array,2)
    if transpose == Image.ROTATE_270:      array = np.rot90(array,3)

    # Interpret the shape of the image
    if array.ndim == 3:
        (height, width, bands) = array.shape
    else:
        (height, width) = array.shape
        bands = 1
        array = array.reshape((height, width, 1))

    # What type of tiff?
    has_palette = (palette != None)
    is_rgb = bands >= 3
    if has_palette: is_rgb = False  # Palette overrides RGB data

    # Determine how to handle the palette in the output file
    if translate and has_palette:
        has_palette = False
        is_rgb = True
        translate_to_rgb = True
    else:
        translate_to_rgb = False

    # Intepret the byte order
    if byteorder.lower() == "native": byteorder = sys.byteorder

    if byteorder.lower() == "little":
        o = "<"
        flag = b"I"
    else:
        o = ">"
        flag = b"M"

    # Write the Image File Header
    #------- 0 bytes
    f.write(pack("cc", flag, flag))
    f.write(pack(o+"H", 42))                            # TIFF's 42
    f.write(pack(o+"L", 8))                             # IFD begins at offset 8
    #------- 8 bytes

    # Determine the key offsets into the file
    ifd_offset = 8

    if has_palette:
        ifd_entries = 12
        after_bytes = 16 + 65536 * 3 * 2
        pixel_bytes = 2
    elif is_rgb:
        ifd_entries = 12
        after_bytes = 16 + 8
        pixel_bytes = 6
    else:
        ifd_entries = 11
        after_bytes = 16
        pixel_bytes = 2

    ifd_bytes = 2 + 12 * ifd_entries + 4
    after_offset = ifd_offset + ifd_bytes

    data_offset = after_offset + after_bytes

    # Write the Image File Directory
    f.write(pack(o+"H", ifd_entries))                   # number of entries

    f.write(pack(o+"HHLL",  256, 4, 1, width))          # image width
    f.write(pack(o+"HHLL",  257, 4, 1, height))         # image height

    if is_rgb:                                          # bits per sample
        f.write(pack(o+"HHLL", 258, 3, 3, after_offset + 16)) 
    else:
        f.write(pack(o+"HHLHH", 258, 3, 1, 16, 0))

    f.write(pack(o+"HHLHH", 259, 3, 1, 1, 0))           # no compression

    if has_palette:                                     # photometric model
        f.write(pack(o+"HHLHH", 262, 3, 1, 3, 0))       # palette
    elif is_rgb:
        f.write(pack(o+"HHLHH", 262, 3, 1, 2, 0))       # RGB
    else:
        f.write(pack(o+"HHLHH", 262, 3, 1, 1, 0))       # black is zero

    f.write(pack(o+"HHLL",  273, 4, 1, data_offset))    # where data begins

    if is_rgb:                                          # samples per pixel
        f.write(pack(o+"HHLHH", 277, 3, 1, 3, 0))

    f.write(pack(o+"HHLL",  278, 4, 1, height))         # rows per strip
    f.write(pack(o+"HHLL",  279, 4, 1, width * height * pixel_bytes))
                                                        # bytes per strip
    f.write(pack(o+"HHLL",  282, 5, 1, after_offset))   # x resolution
    f.write(pack(o+"HHLL",  283, 5, 1, after_offset + 8))
                                                        # y resolution

    f.write(pack(o+"HHLHH", 296, 3, 1, 2, 0))           # unit is inches

    if has_palette:                                     # start of table
        f.write(pack(o+"HHLL", 320, 3, 3*65536, after_offset + 16))

    f.write(pack(o+"L", 0))                             # end of IFD

    # "After" values pointed to by every IFD
    f.write(pack(o+"LL", 72, 1))                        # x unit is 72/inch
    f.write(pack(o+"LL", 72, 1))                        # y unit is 72/inch

    # Write the palette here if there is one
    if has_palette:
        palette[0:65536,0:3].astype(o+"u2").transpose().tofile(f,sep="")

    # Otherwise, write the size of each RGB pixel if necessary
    elif is_rgb:                                        # samples per pixel
        f.write(pack(o+"HHHH", 16, 16, 16, 0))

    # Translate colors if necessary
    if translate_to_rgb:
        array = palette[array[:,:,0],0:3]

    # Otherwise just slice off the needed bands
    elif is_rgb:
        array = array[:,:,0:3]

    else:
        array = array[:,:,0]

    # Append data to output file
    array.astype(o+"u2").tofile(f, sep="")

    # Close the file
    f.close()

def ReadTiff16(filename, up=False, transpose=None):
    """Reads a 16-bit TIFF file that had been written by WriteTiff16. No other
    Tiff file formats are supported.
    
    Inputs:
        filename = the name of the file to read.

        up = True for the line numbers of the image to increase upward; False if
                they are to increase downward. False (downward) is the default.

        transpose = an optional geometric transformation to un-do on the image
                before returning it. Options are designed to match the
                transpose() options in the PIL library. Choices are:
                        Image.FLIP_LEFT_TO_RIGHT
                        Image.FLIP_TOP_BOTTOM
                        Image.ROTATE_90
                        Image.ROTATE_180
                        Image.ROTATE_270

    Return:     A tuple containing the folowing:

        array = a numpy 2-D or 3-D array containing the image pixels. These are
                converted to unsigned 16-bit values if they are not already in
                that format. The order of the indices in the array is expected
                to be (line, sample, band). The third axis is optional. If it
                is present, and the size is >= 3, and no palette is provided,
                then array slices [:,:,0:2] are interpreted as the (R,G,B)
                values for the color of each pixel, ranging from 0 to 65535.
                Otherwise, the value of slice [:,:,0:2] is used as a grayscale
                value or is mapped through the palette to provide color.

        palette = an optional numpy array of shape (65536,3). Values are
                converted to unsigned two-byte integers if they are not in that
                format already. If this palette is provided, then the 0th band
                of the array is used as an index into the palette to derive the
                pixel's (R,G,B) triple. Otherwise, the array values themselves
                are interpreted as grayscale or RGB colors.
        """

    # Open the output file
    f = open(filename, "rb")

    # Read the Image File Header
    #------- 0 bytes
    # f.read(pack("cc", flag, flag))
    # f.read(pack(o+"H", fortytwo))                     # TIFF's 42
    # f.read(pack(o+"L", eight))                        # IFD begins at offset 8
    #------- 8 bytes

    flag1 = f.read(1)
    flag2 = f.read(1)
    if flag1 != flag2: raise IOError("File format is not TIFF")

    if   flag1 == b'I': o = "<"
    elif flag1 == b"M": o = ">"
    else: raise IOError("File format is not TIFF")

    t = unpack(o+"H", f.read(2))
    if t[0] != 42: IOError("File format is not TIFF")

    t = unpack(o+"L", f.read(4))
    my_assert(t[0] == 8)

    # f.write(pack(o+"H", ifd_entries))                 # number of entries
    # f.write(pack(o+"HHLL",  256, 4, 1, width))        # image width
    # f.write(pack(o+"HHLL",  257, 4, 1, height))       # image height

    t = unpack(o+"H", f.read(2))
    ifd_entries = t[0]

    t = unpack(o+"HHLL", f.read(12))
    my_assert((t[0],t[1],t[2]) == (256, 4, 1))
    width = t[3]

    t = unpack(o+"HHLL", f.read(12))
    my_assert((t[0],t[1],t[2]) == (257, 4, 1))
    height = t[3]

    # if is_rgb:                                        # bits per sample
    #     f.write(pack(o+"HHLL", 258, 3, 3, after_offset + 16)) 
    # else:
    #     f.write(pack(o+"HHLHH", 258, 3, 1, 16, 0))

    t = unpack(o+"HHLHH", f.read(12))
    my_assert((t[0],t[1]) == (258, 3))

    if   t[2] == 3: is_rgb = True
    elif t[2] == 1: is_rgb = False
    else:           my_assert(False)

    if is_rgb:
        after_offset = t[3] - 16
    else:
        my_assert((t[3],t[4]) == (16, 0))

    # f.write(pack(o+"HHLHH", 259, 3, 1, 1, 0))         # no compression

    t = unpack(o+"HHLHH", f.read(12))
    my_assert(t == (259, 3, 1, 1, 0))

    # if has_palette:                                   # photometric model
    #    f.write(pack(o+"HHLHH", 262, 3, 1, 3, 0))      # palette
    # elif is_rgb:
    #    f.write(pack(o+"HHLHH", 262, 3, 1, 2, 0))      # RGB
    # else:
    #    f.write(pack(o+"HHLHH", 262, 3, 1, 1, 0))      # black is zero

    t = unpack(o+"HHLHH", f.read(12))
    has_palette = (t == (262, 3, 1, 3, 0))
    test_rgb    = (t == (262, 3, 1, 2, 0))
    is_gray     = (t == (262, 3, 1, 1, 0))

    my_assert(test_rgb == is_rgb)
    my_assert(has_palette or is_rgb or is_gray)

    # Fill in expected sizes now
    ifd_offset = 8

    if has_palette:
        ifd_entries = 12
        after_bytes = 16 + 65536 * 3 * 2
        pixel_bytes = 2
    elif is_rgb:
        ifd_entries = 12
        after_bytes = 16 + 8
        pixel_bytes = 6
    else:
        ifd_entries = 11
        after_bytes = 16
        pixel_bytes = 2

    ifd_bytes = 2 + 12 * ifd_entries + 4
    after_offset = ifd_offset + ifd_bytes

    data_offset = after_offset + after_bytes

    # f.write(pack(o+"HHLL",  273, 4, 1, data_offset))  # where data begins

    t = unpack(o+"HHLL", f.read(12))
    my_assert(t == (273, 4, 1, data_offset))

    # if is_rgb:                                        # samples per pixel
    #    f.write(pack(o+"HHLHH", 277, 3, 1, 3, 0))

    if is_rgb:
        t = unpack(o+"HHLHH", f.read(12))
        my_assert(t == (277, 3, 1, 3, 0))

    # f.write(pack(o+"HHLL",  278, 4, 1, height))       # rows per strip
    # f.write(pack(o+"HHLL",  279, 4, 1, width * height * pixel_bytes))
                                                        # bytes per strip

    t = unpack(o+"HHLL", f.read(12))
    my_assert(t == (278, 4, 1, height))

    if is_rgb: pixel_bytes = 6
    else:      pixel_bytes = 2

    t = unpack(o+"HHLL", f.read(12))
    my_assert(t == (279, 4, 1, width * height * pixel_bytes))

    # f.write(pack(o+"HHLL",  282, 5, 1, after_offset)) # x resolution
    # f.write(pack(o+"HHLL",  283, 5, 1, after_offset + 8))
                                                        # y resolution

    t = unpack(o+"HHLL", f.read(12))
    my_assert(t == (282, 5, 1, after_offset))

    t = unpack(o+"HHLL", f.read(12))
    my_assert(t == (283, 5, 1, after_offset + 8))

    # f.write(pack(o+"HHLHH", 296, 3, 1, 2, 0))         # unit is inches

    t = unpack(o+"HHLHH", f.read(12))
    my_assert(t == (296, 3, 1, 2, 0))

    # if has_palette:                                   # start of table
    #    f.write(pack(o+"HHLL", 320, 3, 3*65536, after_offset + 16))

    if has_palette:
        t = unpack(o+"HHLL", f.read(12))
        my_assert(t == (320, 3, 3*65536, after_offset + 16))

    # f.write(pack(o+"L", 0))                           # end of IFD

    t = unpack(o+"L", f.read(4))
    my_assert(t[0] == 0)

    # "After" values pointed to by every IFD
    # f.write(pack(o+"LL", 72, 1))                      # x unit is 72/inch
    # f.write(pack(o+"LL", 72, 1))                      # y unit is 72/inch

    t = unpack(o+"LL", f.read(8))
    my_assert(t == (72,1))

    t = unpack(o+"LL", f.read(8))
    my_assert(t == (72,1))

    # Read the palette here if there is one
    # if has_palette:
    #    palette[0:65536,0:3].astype(o+"u2").transpose().tofile(f,sep="")

    palette = None
    if has_palette:
        palette = np.fromfile(f, dtype=o+"u2", count=65536*3, sep="")
        palette = palette.reshape((3,65536)).transpose()

    # Otherwise, write the size of each RGB pixel if necessary
    # elif is_rgb:                                      # samples per pixel
    #     f.write(pack(o+"HHHH", 16, 16, 16, 0))

    elif is_rgb:
        t = unpack(o+"HHHH", f.read(8))
        my_assert(t == (16, 16, 16, 0))

    # Append data to output file
    # array.astype(o+"u2").tofile(f, sep="")

    items = width * height
    if is_rgb: items *= 3
    array = np.fromfile(f, dtype=o+"u2", count=items, sep="")

    # Interpret the shape of the image
    # if array.ndim == 3:
    #     (height, width, bands) = array.shape
    # else:
    #     (height, width) = array.shape
    #     bands = 1
    #     array = array.reshape((height, width, 1))

    if is_rgb:
        array = array.reshape(height, width, 3)
    else:
        array = array.reshape(height, width)

    # Apply transpose operation if needed
    # if transpose == Image.FLIP_LEFT_RIGHT: array = np.fliplr(array)
    # if transpose == Image.FLIP_TOP_BOTTOM: array = np.flipud(array)
    # if transpose == Image.ROTATE_90:       array = np.rot90(array,1)
    # if transpose == Image.ROTATE_180:      array = np.rot90(array,2)
    # if transpose == Image.ROTATE_270:      array = np.rot90(array,3)

    if transpose == Image.FLIP_LEFT_RIGHT: array = np.fliplr(array)
    if transpose == Image.FLIP_TOP_BOTTOM: array = np.flipud(array)
    if transpose == Image.ROTATE_90:       array = np.rot90(array,3)
    if transpose == Image.ROTATE_180:      array = np.rot90(array,2)
    if transpose == Image.ROTATE_270:      array = np.rot90(array,1)

    # Flip if line numbers increase upward
    # if up: array = np.flipud(array)

    if up: array = np.flipud(array)

    # Close the file
    f.close()

    return(array, palette)

def my_assert(test):
    if not test:
        raise IOError("Not a recognized TIFF16 file.")

################################################################################
# Test program for grayscale
################################################################################

from vicar import *
from optparse import OptionParser

ROTATE_DICT = { "none"            : None,
                "flip_left_right" : Image.FLIP_LEFT_RIGHT,
                "flip_top_bottom" : Image.FLIP_TOP_BOTTOM,
                "rotate_90"       : Image.ROTATE_90,
                "rotate_180"      : Image.ROTATE_180,
                "rotate_270"      : Image.ROTATE_270 }

def test():

    ############################################################################
    # Set up the parser
    ############################################################################

    parser = OptionParser(usage="%prog [options] file1 file2 ...",
                          version="%prog 0.9")

    # -d, --down
    parser.add_option("-d", "--down", dest="display_upward",
        action="store_false", default=False,
        help="display the image with line numbers increasing downward. This "  +
             "is the default.")

    # -u, --up
    parser.add_option("-u", "--up", dest="display_upward",
        action="store_true", default=False,
        help="display the image with line numbers increasing upward")

    # -l, --limits
    parser.add_option("-l", "--limits", dest="limits",
        action="store", type="float", nargs=2,
        help="pair of pixel values that correspond to black and white.")

    # -b, --byteorder
    parser.add_option("-b", "--byteorder", dest="byteorder",
        action="store", type="choice", default="native",
        choices=("native", "little", "big"),
        help="byte order for output file: little, big or native (default)")

    # -r, --rotate
    parser.add_option("-r", "--rotate", dest="rotate",
        action="store", type="choice", default="none",
        choices=("NONE", "none",
                 "FLIP_LEFT_RIGHT", "flip_left_right",
                 "FLIP_TOP_BOTTOM", "flip_top_bottom",
                 "ROTATE_90", "rotate_90",
                 "ROTATE_180", "rotate_180",
                 "ROTATE_270", "rotate_270"),
        help="rotate or flip the image from its default orientation; "         +
             "choices are flip_left_right, flip_top_bottom, rotate_90, "       +
             "rotate_180, or rotate_270.")

    # -m, --mode
    parser.add_option("-m", "--mode", dest="mode",
        action="store", type="choice", default="RGB",
        choices=("RGB", "rgb",
                 "PALETTE", "palette",
                 "GRAYSCALE", "grayscale"),
        help="TIFF output mode to use: RGB, GRAYSCALE or PALETTE")

    # -t, --translate
    parser.add_option("-t", "--translate", dest="translate",
        action="store_true", default=False,
        help="translate a palette to RGB format.")

    # Parse the command line
    (options, args) = parser.parse_args()

    # Select the rotation mode
    options.rotate = ROTATE_DICT[options.rotate.lower()]

    # Select the version to call
    if options.mode[0].upper() == "R": rgb_test(options, args)

    elif options.mode[0].upper() == "G": gray_test(options, args)

    elif options.mode[0].upper() == "P": palette_test(options, args)

    else: print("Unrecognized mode")

def gray_test(options, args):

    for filename in args:

        # Get the VICAR data
        vic = VicarImage.FromFile(filename)
        array = vic.Get2dArray()

        # Define the limits
        if options.limits == None:
            limits = (array.min(), array.max())
        else:
            limits = options.limits

        # Re-scale
        array = 65536. * (array - limits[0]) / (limits[1] - limits[0])

        array = array.clip(0,65535).astype("uint16")

        # Construct the output file name
        outfile = os.path.splitext(filename)[0] + ".tiff"

        WriteTiff16(outfile, array, palette=None,
                    up=options.display_upward, byteorder=options.byteorder,
            transpose=options.rotate)

        # Test read
        (new_array, new_palette) = ReadTiff16(outfile,
                                              up=options.display_upward,
                                              transpose=options.rotate)

        print(np.any(array - new_array))

################################################################################
# Test program for RGB
################################################################################

def rgb_test(options, args):

    for filename in args:

        # Get the VICAR data
        vic = VicarImage.FromFile(filename)
        array = vic.Get2dArray()

        # Define the limits
        if options.limits == None:
            limits = (array.min(), array.max())
        else:
            limits = options.limits

        # Re-scale
        array = 65536. * (array - limits[0]) / (limits[1] - limits[0])

        # Convert to RGB and enhance blue
        array = np.array([array, array, np.sqrt(array*65536.)])
        array = array.swapaxes(0,2)
        array = array.swapaxes(0,1)

        array = array.clip(0,65535).astype("uint16")

        # Construct the output file name
        outfile = os.path.splitext(filename)[0] + ".tiff"

        WriteTiff16(outfile, array, palette=None,
                    up=options.display_upward, byteorder=options.byteorder,
            transpose=options.rotate)

        # Test read
        (new_array, new_palette) = ReadTiff16(outfile,
                                              up=options.display_upward,
                                              transpose=options.rotate)

        print(np.any(array - new_array))

################################################################################
# Test program with magenta palette
################################################################################

def palette_test(options, args):

    for filename in args:

        # Get the VICAR data
        vic = VicarImage.FromFile(filename)
        array = vic.Get2dArray()

        # Define the limits
        if options.limits == None:
            limits = (array.min(), array.max())
        else:
            limits = options.limits

        # Define the palette
        palette = np.zeros((65536,3), "int32")  # Rely on conversion to uint16

        scale = 1. / (limits[1] - limits[0])
        for dn in range(limits[0],65536):
            frac = min((dn - limits[0]) * scale, 1.)
            palette[dn,0] = int(65535.999 * frac)
            palette[dn,1] = 0
            palette[dn,2] = palette[dn,0]

        array = array.clip(0,65535).astype("int32") # Internally to uint16

        # Construct the output file name
        outfile = os.path.splitext(filename)[0] + ".tiff"

        WriteTiff16(outfile, array, palette=palette,
                    up=options.display_upward, byteorder=options.byteorder,
            transpose=options.rotate, translate=options.translate)

        # Test read
        (new_array, new_palette) = ReadTiff16(outfile,
                                              up=options.display_upward,
                                              transpose=options.rotate)

        print(np.any(array - new_array), np.any(palette - new_palette))

# Execute the main test progam if this is not imported
if __name__ == "__main__": test()
