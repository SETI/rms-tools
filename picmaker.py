#!/usr/bin/env python3
################################################################################
# picmaker.py
#
# This program reads a binary 2-D or 3-D image file and creates a view in JPEG
# or other popular display format. The image file can be any PDS3-labeled image
# or an image in VICAR or FITS format.
#
# A complete command-line interface is provided. Type
#   picmaker.py -h
# for complete help information.
#
# Mark Showalter, PDS Rings Node, SETI Institute
################################################################################

import os, sys, fnmatch
import traceback
import warnings
from optparse import OptionParser, OptionGroup

import numpy as np
from scipy.ndimage.filters import median_filter
from scipy.stats import rankdata
from PIL import Image, ImageFilter

from vicar import VicarImage, VicarError
from colornames import ColorNames
from tiff16 import WriteTiff16, ReadTiff16
import pdsparser
from tabulation import Tabulation
import pickle

# Use astropy.io.fits if possible; old pyfits is a backup option
try:
    import astropy.io.fits as pyfits
except ImportError:
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        import pyfits

################################################################################
# Command-line program
################################################################################

# warnings.simplefilter('error')

def main():

  # Catch any error at return exit status 1
  try:

    ############################################################################
    # Define the parser...
    ############################################################################

    parser = OptionParser(usage="%prog [options] file1 file2 ...",
                          version="%prog 1.0")

    ### Control options
    group = OptionGroup(parser, "control options")

    # -d, --directory
    group.add_option("--directory", dest="directory", 
        action="store", type="string",
        help="directory in which to place converted files. If the recursive "  +
             "option is selected, this becomes the root of a tree which "      +
             "parallels that of the source files.")

    # -r, --recursive
    group.add_option("-r", "--recursive", dest="recursive", 
        action="store_true", default=False,
        help="search recursively down directory trees.")

    # --pattern
    group.add_option("--pattern", dest="pattern", 
        action="store", type="string", default="*",
        help="pattern describing file names to match, e.g., \*.IMG.")

    # --movie
    group.add_option("--movie", dest="movie",
        action="store_true", default=False,
        help="use the same enhancement limits for all images. In recursive "   +
             "mode, use the same limits for all the images in a single "       +
             "directory. This option takes twice as long.")

    # --versions
    group.add_option("--versions", dest="versions",
        action="store", type="string", default=None,
        help="create multiple versions of the picture using different "        +
             "sets of options, as specified in the named input file. Each "    +
             "line of the input file must contain a a sequence of options as " +
             "if they were typed on the command line. These options are "      +
             "appended to the options in the command line, and one version "   +
             "of each picture is created for each line in the file. This is "  +
             "much faster than multiple runs of picmaker because each image "  +
             "file is only read once. Note that changes to control options "   +
             "in the input file are ignored.")

    # --verbose
    group.add_option("--verbose", dest="verbose",
        action="store", type='int', default=0,
        help="1 to print out the name of each directory in a recursive "       +
             "search; 2 to print out each file path.")

    # --replace
    group.add_option("--replace", dest="replace",
        action="store", type="string", default="all",
        help='what to do when a file already exists. '                         +
             '"all" (the default) to replace the file silently; '              +
             '"none" to skip the file silently; '                              +
             '"warn" to issue a warning and skip the file; '                   +
             '"error" to raise an error condition.')

    # --proceed
    group.add_option("--proceed", dest="proceed",
        action="store_true", default=False,
        help="continue processing subsequent files after an error has been "   +
             "encountered.")

    parser.add_option_group(group)

    ### Output options
    group = OptionGroup(parser, "output options")

    # -x, --extension
    group.add_option("-x", "--extension", dest="extension", 
        action="store", type="choice", default=None,
        choices=("BMP", "bmp", "DIB", "dib",
                 "GIF", "gif",
                 "JPG", "jpg", "JPEG", "jpeg",
                 "PNG", "png",
                 "TIF", "tif", "TIFF", "tiff"),
        help="file name extension for image produced; this also defines the "  +
             "format of the output file; options are bmp, gif, jpg, jpeg, "    +
             "png, tif, and tiff, in lower or upper case. Default is jpg.")

    # -s, --suffix
    group.add_option("-s", "--suffix", dest="suffix", 
        action="store", type="string", default="",
        help="a suffix to append to the end of each file name, prior to the "  +
             "file extension.")

    # --strip
    group.add_option("--strip", dest="strip", 
        action="store", type="string", default="",
        help="a string to strip from output filename if it is present.")

    # --alt-strip
    group.add_option("--alt-strip", "--alt_strip", dest="alt_strip", 
        action="store", type="string", default=None,
        help="an additional string to strip from output filename if it is "    +
             "present.")

    # -q, --quality
    group.add_option("-q", "--quality", dest="quality",
        action="store", type="int", default=75,
        help="output quality value for JPEG files. "                           +
             "Range is 1-100; default is %default.")

    # --16
    group.add_option("--16", dest="twobytes",
        action="store_true", default=False,
        help="output a 16-bit tiff instead of an 8-bit picture.")

    parser.add_option_group(group)

    ### Selection options
    group = OptionGroup(parser, "selection options")

    # -b, --band, --bands
    group.add_option("-b", "--band", dest="band",
        action="store", type="int", default=None,
        help="index of the band to appear in the output image; default 1.")

    group.add_option("--bands", dest="bands",
        action="store", type="int", nargs=2, default=None,
        help="pair of indices indicating a range of bands to be averaged for " +
             "the output image. This serves as an alternative to the --band "  +
             "option.")

    # --rectangle
    group.add_option("--rectangle", dest="rectangle",
        action="store", type="int", nargs=4,
        help="corner coordinates of a rectangular sub-region to appear in "    +
             "the image, as four values: sample1, line1, sample2, line2.")

    # -o, --object
    group.add_option("-o", "--object", dest="obj",
        action="store", type="int", default=None,
        help="numeric index or name of the object in the file to display; "    +
             "default is the first valid image object in the file. Object "    +
             "numbering starts at 0.") 

    # --pointer
    group.add_option("--pointer", dest="pointer",
        action="store", type="string", default="IMAGE",
        help="the PDS pointer identifying the image object; used when the "    +
             "input file is a PDS label. Converted to upper case. Default is " +
             "'IMAGE'.") 

    # --alt-pointer
    group.add_option("--alt-pointer", "--alt_pointer", dest="alt_pointer",
        action="store", type="string", default=None,
        help="an alternative PDS pointer identifying the image object; used "  +
             "when the input file is a PDS label and the first pointer is "    +
             "not found. Converted to upper case.") 

    parser.add_option_group(group)

    ### Sizing options
    group = OptionGroup(parser, "sizing options")

    # --size
    group.add_option("--size", dest="size",
        action="store", type="int", nargs=2,
        help="width and height of the output image in pixels.")

    # --scale, --wscale, --hscale
    group.add_option("--scale", dest="scale",
        action="store", type="float",
        help="percentage by which to scale the size of the image.")

    group.add_option("--wscale", dest="wscale",
        action="store", type="float", nargs=1,
        help="percentage by which to scale the width of the image; use with "  +
             "--hscale to scale the width and height by different amounts.")

    group.add_option("--hscale", dest="hscale",
        action="store", type="float", nargs=1,
        help="percentage by which to scale the width of the image; use with "  +
             "--wscale to scale the width and height by different amounts.")

    # --crop
    group.add_option("--crop", dest="crop",
        action="store", type="float", nargs=1, default=None,
        help="crop away any boundary regions entirely containing the "         +
             "specified value.")

    # --frame
    group.add_option("--frame", dest="frame",
        action="store", type="int", nargs=2,
        help="width and height of the frame within which the image must fit; " +
             "if necessary, the final width and height of the image will be "  +
             "scaled down proportionally to fit within the frame.")

    # --pad
    group.add_option("--pad", dest="pad",
        action="store_true", default=False,
        help="pad the image to match the full size of the frame.")

    # --pad-color
    group.add_option("--pad-color", dest="pad_color",
        action="store", type="string", default="black",
        help="the color to use when padding an image to fill a frame. "        +
             "The color can be specified by X11 name or by (R,G,B) triplet.")

    parser.add_option_group(group)

    ### Layout options
    group = OptionGroup(parser, "layout options")

    # --wrap
    group.add_option("--wrap", dest="wrap",
        action="store_true", default=False,
        help="wrap the sections of an image if it is extremely elongated.")

    # --wrap-ratio
    group.add_option("--wrap-ratio", dest="wrap_ratio",
        action="store", type="float", nargs=1, default=None,
        help="wrap the sections of an image if its width:height ratio or its " +
             "height:width ratio exceeds this value.")

    # --overlap
    group.add_option("--overlap", dest="overlap",
        action="store", type="float", nargs=1, default=None,
        help="percentage of overlap between the end of one wrapped section "   +
             "and the beginning of the next.")

    # --overlaps
    group.add_option("--overlaps", dest="overlaps",
        action="store", type="float", nargs=2, default=None,
        help="range of percentages of overlaps between the end of one "        +
             "wrapped section and the beginning of the next.")

    # --gap-size
    group.add_option("--gap-size", "--gapsize", dest="gap_size",
        action="store", type="int", nargs=1, default=1,
        help="the width of the gap in pixels between sections of a wrapped "   +
             "image.")

    # --gap-color
    group.add_option("--gap-color", "--gapcolor", dest="gap_color",
        action="store", type="string", default="white",
        help="the color of the gap between sections of a wrapped image. "      +
             "A color can be specified by X11 name or by (R,G,B) triplet.")

    # --hst
    group.add_option("--hst", dest="hst",
        action="store_true", default=False,
        help="construct a mosaic using all the detectors of an HST image. "    +
             "This is a 2x2 mosaic (with rotation) for WFPC2 and a 1x2 "       +
             "for WFC.")

    parser.add_option_group(group)

    ### Scaling options
    group = OptionGroup(parser, "scaling options")

    # --valid
    group.add_option("-v", "--valid", dest="valid",
        action="store", type="float", nargs=2,
        help="range of valid pixel values; pixels outside this range are "     +
             "ignored.")

    # -l, --limits
    group.add_option("-l", "--limits", dest="limits",
        action="store", type="float", nargs=2,
        help="pair of pixel values that define the limits of the histogram; "  +
             "values outside this range are set to the 'below' and 'above' "   +
             "highlight colors. Default uses the image minimum and maximum.")

    # -p, --percentiles
    group.add_option("-p", "--percentiles", dest="percentiles",
        action="store", type="float", nargs=2, default=(0., 100.),
        help="pair of values that define the percentiles of the histogram "    +
             "to use for scaling the image; values outside this range are "    +
             "set to the 'below' and 'above' highlight colors.")

    # --trim
    group.add_option("--trim", dest="trim",
        action="store", type="int", nargs=1, default=0,
        help="number of pixels around the edge of the image to trim before "   +
             "computing a histogram. Sometimes edge pixels have bad values "   +
             "that could otherwise corrupt the scaling. Default is zero.")

    # --trim-zeros
    group.add_option("--trim-zeros", "--trimzeros", dest="trim_zeros",
        action="store_true", default=False,
        help="ignore any exterior rows or columns that contain all zeros "     +
             "before calculating the percentiles or limits.")

    # --footprint
    group.add_option("--footprint", dest="footprint",
        action="store", type="int", nargs=1, default=0,
        help="the diameter in pixels of a circular footprint for a median "    +
             "filter. If specified, then this median filter is applied to "    +
             "image and the resulting minimum and maximum values define the "  +
             "limits of the scaling. This procedure can be useful for "        +
             "suppressing localized bad pixels such as cosmic ray hits. It "   +
             "can be more effective then the percentile approach for handling "+
             "images that contain a large amount of dark sky. Zero is the "    +
             "default value, in which case no median filter is applied. If a " +
             "footprint is specified in addition to other limits, then the "   +
             "greater of the lower limits and the lesser of the upper limits"  +
             "are used.")

    # --histogram
    group.add_option("--histogram", dest="histogram",
        action="store_true", default=False,
        help="use a histogram stretch, in which case the returned images has " +
             "a uniform distribution of shadings.")

    parser.add_option_group(group)

    ### Enhancement options
    group = OptionGroup(parser, "enhancement options")

    # -c, --colormap
    group.add_option("-c", "--colormap", dest="colormap",
        action="store", type="string",
        help="colormap to apply, defined by a sequence of color names or "     +
             "[R,G,B] triplets, separated by dashes. Values of R, G, and B "   +
             "range 0-255. The map will be constructed by interpolating "      +
             "between these colors. Default is black-white or "                +
             "[0,0,0]-[255,255,255].")

    # --below, --above, --invalid
    group.add_option("--below", dest="below_color",
        action="store", type="string",
        help="the color to use for pixel values below the lower limit; "       +
             "default is the lowest color of the colormap, typically black. "  +
             "A color can be specified by X11 name or by (R,G,B) triplet.")

    group.add_option("--above", dest="above_color",
        action="store", type="string",
        help="the color to use for pixel values above the upper limit; "       +
             "default is the highest color of the colormap, typically white. " +
             "A color can be specified by X11 name or by (R,G,B) triplet.")

    group.add_option("--invalid", dest="invalid_color",
        action="store", type="string", default="black",
        help="the color to use for invalid pixel values (outside the range "   +
             "specified by the --valid option) and NaNs; default is black. "   +
             "A color can be specified by X11 name or by (R,G,B) triplet.")

    # -g, --gamma
    group.add_option("-g", "--gamma", dest="gamma",
        action="store", type="float", default=1.,
        help="the gamma value to apply to grayscale of the image returned; "   +
             "default 1.")

    # --tint
    group.add_option("--tint", dest="tint",
        action="store_true", default=False,
        help="override the colormap based on the image's filter name.")

    parser.add_option_group(group)

    ### Orientation options
    group = OptionGroup(parser, "orientation options")

    # -u, --up
    group.add_option("-u", "--up", dest="display_upward",
        action="store_true", default=False,
        help="display the image with line numbers increasing upward. This is " +
             "the default for FITS files.")

    # -d, --down
    group.add_option("-d", "--down", dest="display_downward",
        action="store_true", default=False,
        help="display the image with line numbers increasing downward. This "  +
             "is the default for VICAR files.")

    # --rotate
    group.add_option("--rotate", dest="rotate",
        action="store", type="choice", default="none",
        choices=("NONE", "none",
                 "FLIPLR", "fliplr",
                 "FLIPTB", "fliptb",
                 "ROT90", "rot90",
                 "ROT180", "rot180",
                 "ROT270", "rot270"),
        help="rotate or flip the image from its default orientation; "         +
             "choices are fliplr, fliptb, rot90, rot180, or rot270.")

    parser.add_option_group(group)

    ### Special processing options
    group = OptionGroup(parser, "processing options")

    # -f, --filter
    group.add_option("-f", "--filter", dest="filter",
        action="store", type="choice", default="none",
        choices=("NONE", "none",
                 "BLUR", "blur",
                 "CONTOUR", "contour",
                 "DETAIL", "detail",
                 "EDGE_ENHANCE", "edge_enhance",
                 "EDGE_ENHANCE_MORE", "edge_enhance_more",
                 "EMBOSS", "emboss",
                 "FIND_EDGES", "find_edges",
                 "SMOOTH", "smooth",
                 "SMOOTH_MORE", "smooth_more",
                 "SHARPEN", "sharpen",
                 "MEDIAN_3", "median_3",
                 "MEDIAN_5", "median_5",
                 "MEDIAN_7", "median_7",
                 "MINIMUM_3", "minimum_3",
                 "MINIMUM_5", "minimum_5",
                 "MINIMUM_7", "minimum_7",
                 "MAXIMUM_3", "maximum_3",
                 "MAXIMUM_5", "maximum_5",
                 "MAXIMUM_7", "maximum_7"),
        help="name of image processing filter to apply. Choices are: "         +
             "none, blur, contour, detail, edge_enahnce, edge_enhance_more, "  +
             "emboss, find_edges, smooth, smooth_more, sharpen, median_3, "    +
             "median_5, median_7, minimum_3/5/7, and maximum_3/5/7.")

    # --zebra
    group.add_option("--zebra", dest="zebra",
        action="store_true", default=False,
        help="interpolate across black zebra stripes at the beginnings and "   +
             "ends of lines.")

    parser.add_option_group(group)

    ############################################################################
    # Parse the command line and interpret versions
    ############################################################################

    (options, args) = parser.parse_args()

    if options.movie and (options.versions is not None):
        raise ValueError("movie and versions options are incompatible")

    ############################################################################
    # Reserve the control parameters
    ############################################################################

    directory = options.directory
    if directory is not None and directory.endswith('/'):
        directory = directory[:-1]

    recursive = options.recursive
    movie = options.movie
    pattern = options.pattern

    verbose = options.verbose
    if verbose not in (0,1,2):
        raise ValueError('unrecognized verbose option: ' + str(verbose))

    replace = options.replace
    if replace not in ('all', 'none', 'warn', 'error'):
        raise ValueError('unrecognized replace option: "%s"' % str(replace))

    proceed = options.proceed

    ############################################################################
    # Create separate lists of files and directories
    ############################################################################

    filenames = []
    directories = []

    for f in args:
        if os.path.isfile(f):
            filenames.append(f)
        else:
            if f.endswith('/'):
                f = f[:-1]
            directories.append(f)

    ############################################################################
    # Create a list of option sets
    ############################################################################

    # Interpret the versions as a list of alternative options
    if options.versions is not None:
        f = open(options.versions)
        lines = f.readlines()
        f.close()

        options_list = []
        for line in lines:
            new_args = line.split()
            if new_args == []:
                continue

            these_args = sys.argv[1:] + new_args
            options = parser.parse_args(args = these_args)[0]

            options.replace = replace
            if replace not in ('all', 'none', 'warn', 'error'):
                raise ValueError('unrecognized replace option: "%s"' %
                                 str(replace))

            options.proceed = proceed

            options_list.append(options)

    else:
        options_list = [options]

    ############################################################################
    # Convert each options list to a dictionary of parameters passed to the
    # function.
    ############################################################################

    option_dicts = []
    for options in options_list:

        # hst option checks
        if options.hst:
            if options.band is not None or options.bands is not None:
                raise ValueError("hst and band options are incompatible")

        # band vs. bands (except with hst option)
        elif options.band is not None and options.bands is not None:
            if (options.band != options.bands[0] or
                options.band != options.bands[1]):
                    raise ValueError("band and bands options are incompatible")

        # hst and movie
        if options.hst and options.movie:
            raise ValueError("hst and movie options are incompatible")

        # scale, wscale, hscale
        if options.scale is not None and options.wscale is not None:
            raise ValueError("scale and wscale options are incompatible")

        if options.scale is not None and options.hscale is not None:
            raise ValueError("scale and hscale options are incompatible")

        # frame vs. size
        if options.frame is not None and options.size is not None:
            raise ValueError("frame and size options are incompatible")

        # overlap vs. overlaps
        if options.overlap is not None and options.overlaps is not None:
            raise ValueError("overlap and overlaps options are incompatible")

        # up, down
        if options.display_upward and options.display_downward:
            raise ValueError("--up and --down options are incompatible")

        # two-byte options
        if options.twobytes:
            if (options.extension is not None and
                options.extension.lower()[0:3] != 'tif'):
                    raise ValueError("only tiffs can be written in 16-bit mode")

            if options.filter is not None and options.filter.lower() != "none":
                raise ValueError("16-bit filter options are not supported")

        # Select bands, sort and convert for Python indexing
        if not options.hst:
            if options.band is None:
                options.band = 0
            if options.bands is None:
                options.bands = (options.band, options.band+1)

        # Select rectangle coordinates, sort and convert for Python indexing
        if options.rectangle is None:
            samples = None
            lines   = None
        else:
            samples = sorted([options.rectangle[0]-1, options.rectangle[2]])
            lines   = sorted([options.rectangle[1]-1, options.rectangle[3]])

        # Determine scaling factors
        if options.scale is None:
            options.scale = 100.
        if options.wscale is None:
            options.wscale = options.scale
        if options.hscale is None:
            options.hscale = options.scale

        options.scale = (options.wscale, options.hscale)

        # Sort range values
        if options.valid is not None:
            options.valid = tuple(sorted(options.valid))

        if options.limits is not None:
            options.limits = tuple(sorted(options.limits))

        if options.percentiles is not None:
            options.percentiles = tuple(sorted(options.percentiles))

        # Incorporate alt_pointer into pointer list
        if options.alt_pointer is not None:
            options.pointer = [options.pointer, options.alt_pointer]

        # Incorporate alt_strip into strip list
        if options.alt_strip is not None:
            options.strip = [options.strip, options.alt_strip]

        # Interpret overlaps
        if options.overlaps is None:
            if options.overlap is None:
                options.overlaps = (0., 0.)
            else:
                options.overlaps = (options.overlap, options.overlap)

        option_dict = {
            # control parameters
            'replace': replace,
            'proceed': proceed,

            # output options
            'extension': options.extension,
            'suffix': options.suffix,
            'strip': options.strip,
            'quality': options.quality,
            'twobytes': options.twobytes,

            # selection options
            'bands': options.bands,
            'lines': lines,
            'samples': samples,
            'obj': options.obj,
            'pointer': options.pointer,

            # sizing options
            'size': options.size,
            'scale': options.scale,
            'crop': options.crop,
            'frame': options.frame,
            'pad': options.pad,
            'pad_color': options.pad_color,

            # layout options
            'wrap': options.wrap,
            'wrap_ratio': options.wrap_ratio,
            'overlap': options.overlaps,
            'gap_size': options.gap_size,
            'gap_color': options.gap_color,
            'hst': options.hst,

            # scaling options
            'valid': options.valid,
            'limits': options.limits,
            'percentiles': options.percentiles,
            'trim': options.trim,
            'trim_zeros': options.trim_zeros,
            'footprint': options.footprint,
            'histogram': options.histogram,

            # enhancement options
            'colormap': options.colormap,
            'below_color': options.below_color,
            'above_color': options.above_color,
            'invalid_color': options.invalid_color,
            'gamma': options.gamma,
            'tint': options.tint,

            # orientation options
            'display_upward': options.display_upward,
            'display_downward': options.display_downward,
            'rotate': options.rotate.lower(),

            # special processing options
            'filter': options.filter.lower(),
            'zebra': options.zebra,
        }

        option_dicts.append(option_dict)

    ############################################################################
    # Process the files
    ############################################################################

    # Process command line filenames
    filtered = fnmatch.filter(filenames, pattern)
    if filtered != []:
        process_images(filtered, directory, movie, option_dicts,
                       verbose=(verbose > 1))

    # Identify the common prefix of all the command line directories
    # This will not be included in the path from the root directory.
    common_prefix = find_common_path(directories)

    # In a case where we have already processed command line filenames, we need
    # to insert one extra subdirectory
    if filenames != []:
        common_prefix = os.path.split(common_prefix)[0]

    lcommon = len(common_prefix)
    if lcommon == 0:
        lcommon = -1        # because the prefix does not end in slash

    # Process command line directories
    for dirpath in directories:

        # Recursive case
        if recursive:
            for (this_dir, subdirs, filenames_in_this_dir) in os.walk(dirpath):
                filtered = fnmatch.filter(filenames_in_this_dir, pattern)
                if filtered == []:
                    continue

                if verbose:
                    print(this_dir)

                filepaths = [os.path.join(this_dir,f) for f in filtered]

                if directory is None:
                    out_dir = None
                else:
                    out_dir = os.path.join(directory, this_dir[lcommon+1:])

                process_images(filepaths, out_dir, movie, option_dicts,
                               verbose=(verbose > 1))

        # Non-recursive case
        else:
            if verbose:
                print(dirpath)

            filenames_in_dir = os.listdir(dirpath)
            filtered = fnmatch.filter(filenames_in_dir, pattern)
            if filtered == []:
                continue

            filepaths = [os.path.join(dirpath,f) for f in filtered]

            if directory is None:
                out_dir = None
            else:
                out_dir = os.path.join(directory, dirpath[lcommon+1:])

            process_images(filepaths, out_dir, movie, option_dicts,
                           verbose=(verbose > 1))

  except Exception:
    sys.excepthook(*sys.exc_info())
    sys.exit(1)

  except KeyboardInterrupt:
    print('*** KeyboardInterrupt ***')
    sys.exit(2)

################################################################################
# A handy utility
################################################################################

def find_common_path(directories):

    def longest_match(str1, str2):
        kmax = min(len(str1), len(str2))
        for k in range(kmax):
            if str1[k] != str2[k]:
                return str1[:k]
        return str1[:kmax]

    if len(directories) == 0:
        return ''
    if len(directories) == 1:
        return directories[0]

    longest = longest_match(directories[0], directories[1])
    for dir in directories[2:]:
        longest = longest_match(longest, dir)

    last_slash = longest.rfind('/')
    if last_slash < 1:
        return ''

    return longest[:last_slash]

################################################################################
# Circular footprint mask for median filter
################################################################################

def circle_mask(diameter):

    size = int(np.ceil(diameter))
    center = size/2. - 0.5

    r = np.arange(size) - center
    r2 = r**2 + r[:,np.newaxis]**2
    mask = (r2 <= diameter**2/4.)

    if np.sum(mask[0]) == 0:
        mask = mask[1:-1,1:-1]

    return mask

################################################################################
# Function to process all the files in a directory
################################################################################

def process_images(filenames, directory, movie, option_dicts, verbose=False):
    """Process a list of images using a list of option dictionaries."""

    if directory is not None and not os.path.exists(directory):
        os.makedirs(directory)

    # Movie case...
    if movie:

        # Convert all images...
        results = images_to_pics(filenames, directory, reuse=None,
                                 verbose=verbose, **option_dicts[0])
        if results[:2] == (None, None):
            if proceed:
                return
            raise IOError('unable to process movie')

        # Re-convert using a fixed stretch
        movie_dict = option_dicts[0].copy()
        movie_dict['limits'] = results[:2]

        _ = images_to_pics(filenames, directory, reuse=None,
                           verbose=verbose, **movie_dict)

    # Otherwise handle images sequentially
    else:
        for filename in filenames:
            prev_obj = -1
            prev_pointer = None
            for k,option_dict in enumerate(option_dicts):

                if (prev_obj == option_dict['obj'] and
                    prev_pointer == option_dict['pointer']):
                        reuse = results[-1]
                else:
                        reuse = None
                        prev_obj = option_dict['obj']
                        prev_pointer = option_dict['pointer']

                # Convert image...
                results = images_to_pics([filename], directory, reuse=reuse,
                                         verbose=(verbose and k == 0),
                                         **option_dict)

################################################################################
# Main method
################################################################################

def images_to_pics(filenames, directory=None, verbose=False,
        replace='all', proceed=False,
        extension='jpg', suffix='', strip=[], quality=75, twobytes=False,
        bands=None, lines=None, samples=None, obj=None, pointer=['IMAGE'],
        size=None, scale=(100.,100.), crop=None, frame=None, pad=False,
            pad_color='black',
        wrap=False, wrap_ratio=None, overlap=(0.,0.), gap_size=1,
            gap_color='white', hst=False,
        valid=None, limits=None, percentiles=None, trim=0, trim_zeros=False,
            footprint=0, histogram=False,
        colormap=None, below_color=None, above_color=None, invalid_color=None,
            gamma=1., tint=False,
        display_upward=False, display_downward=False, rotate=None,
        filter='NONE', zebra=False,
        reuse=None):

    """Converts an image file (VICAR, FITS or TIFF) to a picture file (JPEG,
    TIFF, etc.). In the process, it provides various options for resizing,
    enhancement, and filtering.

    Input:
    filenames           a list of image file names to convert.

    directory           the directory in which to write output files. If None,
                        files will be written to the same directory in which
                        the image files were found.

    verbose             True to print out each file name as it is processed.

    replace             what to do when a file already exists.
                        "all" (the default) to replace the file silently;
                        "none" to skip the file silently;
                        "warn" to issue a warning and skip the file;
                        "error" to raise an error condition.

    proceed             True to print any IO error but continue processing
                        files; False to raise the first error and stop.

    extension           the extension of the output file, which also defines the
                        output file type. Options are jpeg, jpg, tiff, tif, gif,
                        png, dib or bmp, in upper or lower case. The default is
                        jpg for one-byte output and tiff for two-byte output.

    suffix              an optional text string to append to each file name,
                        before the suffix.

    strip               an optional text string ot list of text strings to strip
                        away from the end of the input filename.

    quality             the quality value for jpeg output, 0-100.

    twobytes            True to write a 2-byte tiff rather than a 1-byte file.

    bands               a two-element tuple defining the range of bands to
                        combine for the output file. The pixels in those bands
                        are averaged together. Values follow python indexing
                        conventions, so (0,2) will combine the first two bands,
                        (which are indexed 0 and 1). Default is None, which is
                        equivalent to (0,1).

    lines               an optional tuple defining the range of lines to extract
                        for output. Default is to include all the lines.

    samples             an optional tuple defining the range of samples to
                        extract for output. Default is to include all the
                        samples.

    obj                 the name or index of the image object to extract from
                        the file. Needed for FITS images that can contain more
                        than one image. Default is to extract the first image
                        object in the file. Numbering starts at 0.

    pointer             the name of the PDS pointer identifying the name of the
                        image object; used when the input file is a PDS label.
                        Converted to upper case. This can also be specified as
                        a list of names, in which case the first matching
                        pointer found in the label is used. Default is
                        ['IMAGE'].

    size                the size of the output image. A tuple of values can be
                        used to specify different values for width and
                        height. None implies no change in size

    scale               the scale factor to enlarge the image, as a percentile.
                        Use a tuple to scale each dimension by a different
                        amount. None implies no scaling.

    crop                crop any pixels at the border of the image matching this
                        numeric value. None implies no cropping.

    frame               an optional tuple specifying the absolute upper limit on
                        the dimensions of the image. The final image must fit
                        inside this frame. If either dimension of the output
                        image is too large, then the image is scaled down
                        proportionally until it fits. Smaller images are not
                        enlarged.

    pad                 True to pad the image to match the full size of the
                        frame.

    pad_color           the color to use when padding an image to fill a frame.
                        Colors can be expressed by name, using any of the
                        standard names used in the X11 system. They may also be
                        specifed by triples (r,g,b), where the red, green and
                        blue values are each specified by a value between 0 and
                        255.

    wrap                True to wrap the sections of an image that is extremely
                        elongated. This can make more effective use of the
                        specified size or frame.

    wrap_ratio          wrap the sections of an image if its width:height ratio
                        or its height:width ratio exceeds this value. None to
                        ignore this option.

    overlap             a tuple defining the range of allowed overlaps between
                        the end of one wrapped section and the beginning of the
                        next. For example, (5,10) means that between 5% and 10%
                        of the last pixels in one section of a wrapped image
                        will also appear at the beginning of the next section.

    gap_size            the size of the gap in pixels between the sections of a
                        wrapped image.

    gap_color           the color of the gap pixels in a wrapped image. Colors
                        can be expressed by name, using any of the standard
                        names used in the X11 system. They may also be specifed
                        by triples (r,g,b), where the red, green and blue values
                        are each specified by a value between 0 and 255.

    hst                 True to construct a mosaic involving multiple HST
                        detectors. For WFPC2, it creates a 2x2 mosaic with
                        rotation; for WFC it creates a 1x2 stack of the two
                        CCDs.

    valid               an optional tuple defining the valid range of pixels.
                        Values outside this range are disregarded. In the output
                        file returned, these pixels will be highlighted in a
                        special color.

    limits              a tuple defining the minimum and maximum pixel values to
                        use for enhancement. Pixels below the lower limit or
                        above the upper limit will be highlighted in a special
                        color. Default is to use the minimum and maximum valid
                        pixel values in the file.

    percentiles         a tuple defining defining percentiles of the histogram
                        by which to narrow the limits. For example, a value
                        (1,98) will cause the darkest 1% of the pixels to fall
                        below the lower limit and the brigtest 2% of the pixels
                        to fall above the upper limit. These values are based on
                        a histogram generated after the limits have been
                        applied. Default is (0,100).

    trim                the number of pixels around the edge of the image to
                        trim before computing a histogram. Sometimes edge pixels
                        have bad values that could otherwise corrupt the
                        scaling. Default is zero.

    trim_zeros          ignore any exterior rows or columns that contain all
                        zeros before calculating the percentiles or limits.

    footprint           diameter in pixels of a circular footprint for a median
                        filter. If specified, then this median filter is applied
                        to the image and the resulting minimum and maximum
                        values define the limits of the scaling. This procedure
                        can be useful for suppressing localized bad pixels such
                        as cosmic ray hits. It can be more effective then the
                        percentile approach for handling images that contain a
                        large amount of dark sky. Zero for no median filtering.
                        If a footprint is specified in addition to other limits,
                        then the greater of the lower limits and the lesser of
                        the upper limits are used.

    histogram           True to use a histogram stretch, in which case the
                        returned images has a uniform distribution of shadings.

    colormap            an optional string containing two or more colors
                        separated by dashes. These define the sequence of colors
                        that will be used to represent pixel values ranging from
                        the lower to the upper limit. For example, black-white
                        will create a normap grayscale colormap (the default)
                        but black-blue-white will tint intermediate pixels blue.
                        If only a single color is given, it is interpreted as
                        the intermediate color between black and white. Colors
                        may be expressed by name, using any of the standard
                        names used in the X11 system. They may also be specifed
                        by triples (r,g,b), where the red, green and blue values
                        are each specified by a value between 0 and 255.

    below_color         color to use below the lower limit; None for lowest
                        colormap value.

    above_color         color to use above the upper limit; None for hightest
                        colormap value.

    invalid_color       color to use for invalid pixels; None default to black.

    gamma               an optiona parameter to adjust intermediate intensities
                        in the output image. Values > 1 will make grays brighter
                        relative to black and white; values < 1 will make grays
                        darker. Default is 1. The gamma factor is applied after
                        the colormap.

    tint                True to override the colormap based on the filter name.

    display_upward      True to override the default and display the image with
                        line numbers increasing upward.

    display_downward    True to override the default and display the image with
                        line numbers increasing downward.

    rotate              An optional string specifying one of several ways of
                        orienting the image. Choices are fliplr, fliptb, rot90,
                        rot180, and rot270. Rotations are counter-clockwise.
                        Note that size constraints are applied after rotation.

    filter              An optional string specifying one of several built-in
                        filters to apply to the images. Filters take effect
                        after the color enhancement has been applied. Options
                        are  blur, contour, detail, edge_enhance,
                        edge_enhance_more, emboss, find_edges, smooth,
                        smooth_more, sharpen, median_3, median_5, median_7,
                        minimum_3, minimum_5, minimum_7, maximum_3, maximum_5
                        and maximum_7. The number that follows median, minimum
                        and maximum is the size of a box centered on the given
                        pixel over which the median, minimum or maximum is
                        found.

    zebra               True to search for and erase 'zebra stripes'. For data
                        compression, some Voyager and Cassini images have values
                        of zero near the beginnings or ends of alernating rows.
                        These stripes are erased by averaging the pixels above
                        and below.

    reuse               If not None, this parameter must be a tuple containing:
                            (original 3D image array,
                             True if default z-axis is up; False otherwise,
                             the filter_info tuple)
                        If this parameter is provided, then input operations are
                        suspended and the given information is used instead.
                        This makes it relatively quick to generate multiple
                        pictures from the same image file. The parameter is
                        ignored when multiple input files are given.

    Return:             a tuple containing (low, high, reuse, infile):
        low             the lower limit to the stretch;
        high            the upper limit to the stretch;
        reuse           the reuse tuple if needed for another call. It contains
                        (array3d, default_is_up, filter_info, infile).
    """

    ############################################################################
    # Main code begins here
    ############################################################################

    # Check for incompatible options

    if hst and bands is not None:
        raise ValueError("hst and bands options are incompatible")

    # frame vs. size
    if frame is not None and size is not None:
        raise ValueError("frame and size options are incompatible")

    # frame vs. wrap_ratio
    if frame is not None and wrap_ratio:
        raise ValueError("frame and wrap_ratio options are incompatible")

    # Fill in defaults if necessary
    if bands is None:
        bands = (0,1)

    if extension is None:
        if twobytes:
            extension = "tiff"
        else:
            extension = "jpg"

    # Initialize the list of limits for return in movie mode
    min_limits = []
    max_limits = []
    array3d = None

    # Loop through files...
    for infile in filenames:

      if verbose:
        print(infile)

      # Don't stop on error!
      try:

        # Construct the output file name
        outfile = get_outfile(infile, directory, strip, suffix, extension,
                             replace)
        if outfile == '':
            continue

        # Check for the reuse information
        if len(filenames) == 1 and reuse is not None:
            (array3d, default_is_up, filter_info, infile) = reuse

        # Otherwise, do all the input...
        else:
            # If this is a PDS3 label file, get the image filename(s) and save
            # the filter name
            filter_info = None
            upperfile = infile.upper()
            labelfile = ''
            if upperfile.endswith('.LBL'):
                labelfile = infile
                labeldict = pdsparser.PdsLabel.from_file(infile).as_dict()

                # Get the instrument info if available
                filter_info = None

                if 'INSTRUMENT_HOST_ID' in labeldict:
                    inst_host = labeldict['INSTRUMENT_HOST_ID']
                elif 'SPACECRAFT_ID' in labeldict:
                    inst_host = labeldict['SPACECRAFT_ID']
                elif 'SPACECRAFT_NAME' in labeldict:
                    inst_host = labeldict['SPACECRAFT_NAME']
                else:
                    inst_host = None

                if inst_host is not None:
                    if 'INSTRUMENT_ID' in labeldict:
                        inst_id = labeldict['INSTRUMENT_ID']
                        if 'DETECTOR_ID' in labeldict:
                            detector_id = labeldict['DETECTOR_ID']
                            if isinstance(detector_id, str):
                                inst_id += '/' + detector_id
                    elif 'INSTRUMENT_NAME' in labeldict:
                        inst_id = labeldict['INSTRUMENT_NAME']
                    else:
                        inst_id = None

                    if 'FILTER_NAME' in labeldict:
                        filter_name = labeldict['FILTER_NAME']
                    else:
                        filter_name = None

                    filter_info = (inst_host, inst_id, filter_name)

                # Find the first matching object pointer
                if isinstance(pointer, str):
                    pointer = [pointer]

                pds_obj = None
                for pname in pointer:
                    pname = pname.upper()

                    if not pname.startswith('^'):
                        pname = '^' + pname

                    if pname in labeldict:
                        pds_obj = labeldict[pname]
                        if isinstance(pds_obj, tuple):
                            pds_obj = pds_obj[0]
                        break

                if pds_obj is None:
                    raise KeyError('PDS pointer %s not found' %
                                   pointer[0].upper())

                # Convert to a list of filenames for reading
                if isinstance(pds_obj, str):
                    pds_obj = [pds_obj]

                if obj is None:
                    max_obj = len(pds_obj) - 1
                    imagefile = [os.path.join(os.path.split(infile)[0],
                                              p) for p in pds_obj]
                elif isinstance(obj, int):
                    max_obj = obj
                    imagefile = os.path.join(os.path.split(infile)[0],
                                             pds_obj[obj])
                else:
                    max_obj = max(obj)
                    imagefile = [os.path.join(os.path.split(infile)[0],
                                              pds_obj[o]) for o in obj]

                if max_obj >= len(pds_obj):
                    raise IndexError(('index %d for PDS pointer %s ' +
                                      'out of range') % (max_obj+1, pname[1:]))

            else:
                imagefile = infile

            # Read the image array, select up, try to find the filter
            (array3d, default_is_up,
                      filter_info2) = read_image_array(imagefile, labelfile,
                                                     obj, hst)
            filter_info = filter_info or filter_info2

        # Now construct the picture...

        if display_upward:
            this_display_upward = True
        elif display_downward:
            this_display_upward = False
        else:
            this_display_upward = default_is_up

        # Make note of whether the pixels are integers or floats
        is_int = array3d.dtype.kind in ("i","u")

        # Look up an instrument-specific colormap if necessary
        if tint:
            colormap2 = tinted_colormap(filter_info)
            if colormap2 is not None:
                colormap = colormap2

        # Handle HST mosaics
        if hst and filter_info[0] == 'HST' and \
                   (filter_info[1] in ('ACS/WFC', 'WFPC2')):

            # Flip for downward orientation (PIL images are there already)
            if default_is_up:       # If images were read from a FITS file
                array3d = array3d[:,::-1,:]

            this_display_upward = False

            # Create RGB version of each image
            arraysRGB = []
            for b in range(array3d.shape[0]):

                # Slice out the needed part of the image
                (array2d,
                 invalid_mask) = slice_array(array3d, samples, lines, (b,b+1),
                                                      valid, crop)

                # Fill in zebra stripes (converting to float if necessary)
                if zebra:
                    array2d = fill_zebra_stripes(array2d)

                # Get the histogram limits
                these_limits = get_limits(array2d, invalid_mask,
                                          limits, percentiles,
                                          assume_int=is_int, trim=trim,
                                          trim_zeros=trim_zeros,
                                          footprint=footprint)

                # Apply colormap
                arrayRGB = apply_colormap(array2d, these_limits, histogram,
                                          colormap, invalid_mask,
                                          below_color, above_color,
                                          invalid_color)

                arraysRGB.append(arrayRGB)

            # Assemble mosaic...
            if filter_info[1] == 'WFPC2':

                # Distribute WFPC2 images into quadrants, with rotation
                quadsRGB = np.zeros((4,) + arraysRGB[0].shape)

                for b in range(array3d.shape[0]):
                    if isinstance(imagefile, str):
                        quadsRGB[b] = np.rot90(arraysRGB[b],b)
                    else:
                        testfile = imagefile[b].upper()
                        if 'PC1' in testfile:
                            quadsRGB[0] = arraysRGB[b]
                        elif 'WF2' in testfile:
                            quadsRGB[1] = np.rot90(arraysRGB[b],1)
                        elif 'WF3' in testfile:
                            quadsRGB[2] = np.rot90(arraysRGB[b],2)
                        elif 'WF4' in testfile:
                            quadsRGB[3] = np.rot90(arraysRGB[b],3)
                        else:
                            quadsRGB[b] = np.rot90(arraysRGB[b],b)

                (_, dl, ds, db) = quadsRGB.shape
                arrayRGB = np.empty((2*dl, 2*ds, db))
                arrayRGB[:dl, -ds:] = quadsRGB[0]
                arrayRGB[:dl, :ds ] = quadsRGB[1]
                arrayRGB[-dl:,:ds ] = quadsRGB[2]
                arrayRGB[-dl:,-ds:] = quadsRGB[3]

            else:

                # Handle WFC layout option.
                # Layer 1 = WFC2, on bottom; Layer 4 = WFC1, on top

                if len(arraysRGB) > 1:
                    panelsRGB = np.zeros((2,) + arraysRGB[0].shape)
                    # panelsRGB[0] = WFC1; panelsRGB[1] = WFC2

                    for b in range(2):
                        if isinstance(imagefile, str):
                            panelsRGB[1-b] = arraysRGB[b]
                        else:
                            testfile = imagefile[b].upper()
                            if 'WFC1' in testfile:
                                panelsRGB[0] = arraysRGB[b]
                            elif 'WFC2' in testfile:
                                panelsRGB[1] = arraysRGB[b]
                            else:
                                panelsRGB[b] = arraysRGB[b]

                    (dl, ds, db) = arraysRGB[0].shape
                    arrayRGB = np.zeros((2*dl, ds, db))

                    arrayRGB[:dl]  = panelsRGB[0]   # WFC1 on top
                    arrayRGB[-dl:] = panelsRGB[1]   # WFC2 on bottom

                else:
                    arrayRGB = arraysRGB[0]

        # Standard procedure, no mosaicking
        else:
            # Slice out the needed part of the image
            (array2d,
             invalid_mask) = slice_array(array3d, samples, lines, bands, valid,
                                                  crop)

            # Fill in zebra stripes (converting to float if necessary)
            if zebra:
                array2d = fill_zebra_stripes(array2d)

            # Get the histogram limits
            these_limits = get_limits(array2d, invalid_mask, limits, percentiles,
                                      assume_int=is_int, trim=trim,
                                      trim_zeros=trim_zeros,
                                      footprint=footprint)

            # Save the current limits for movie mode
            min_limits.append(these_limits[0])
            max_limits.append(these_limits[1])

            # Apply colormap
            arrayRGB = apply_colormap(array2d, these_limits, histogram,
                                      colormap, invalid_mask,
                                      below_color, above_color, invalid_color)

        # Apply rotation if necessary
        arrayRGB = rotate_array_rgb(arrayRGB, this_display_upward, rotate)

        # Apply gamma
        arrayRGB = apply_gamma(arrayRGB, gamma)

        # Determine the full output size neglecting any wrap to be applied
        (unwrapped_size, wrapped_size, sections,
         wrap_axis) = get_size(arrayRGB.shape, size, scale, frame, wrap,
                                               wrap_ratio, overlap, gap_size)

        # Convert to PIL image
        image = array_to_pil(arrayRGB, twobytes)

        # Apply filter
        image = filter_image(image, filter)

        # Resize PIL image
        image = resize_image(image, unwrapped_size)

        # Wrap the PIL image if necessary
        if sections > 1:
            image = wrap_image(image, wrapped_size, sections, wrap_axis,
                                      gap_size, gap_color)

        # Pad the PIL image if necessary
        if pad:
            image = pad_image(image, frame, pad_color)

        # Write PIL image via PIL or as a 16-bit TIFF
        write_pil(image, outfile, quality)

      except Exception:
        if proceed:
            (etype, value, tb) = sys.exc_info()
            traceback.print_tb(tb)
            print(infile, '**** %s: %s' % (etype.__name__, value))
        else:
            raise

    # Return the median stretch and reuse tuple when finished
    if min_limits == []:
        return (None, None, None)

    if array3d is None:
        return (np.median(min_limits), np.median(max_limits), None)

    return (np.median(min_limits), np.median(max_limits),
            (array3d, default_is_up, filter_info, infile))

################################################################################
# Read the 3-D image array from a data file
################################################################################

def read_image_array(filename, labelfile, obj=None, hst=False):
    """Return the 3D pixel array and the default display orientation, given the
    file and optional object number.

    Input:
        filename        input file name, which could be in Vicar, FITS, TIFF, or
                        .npy format. Alternatively, a list of filenames whose
                        arrays are stacked together.
        labelfile       optional name of a PDS3 label file.
        obj             index or name of the object to load; only used if the
                        file contains multiple image objects. Default is to
                        return the first image object. If obj is a list or
                        tuple, then multiple objects are stacked to create a new
                        image cube.
        hst             True to mosaic an HST image involving multiple CCDs.

    Return:             a tuple of three values:
                        [0]: a numpy 3-D array containing the image data.
                        [1]: True if the default display orientation is upward;
                             False if it is downward or unknown.
                        [2]: a tuple containing (instrument_host_name,
                             instrument_name, filter_name), if available.
    """

    if isinstance(filename, str):
        return read_one_image_array(filename, labelfile, obj, hst)

    # In the case of multiple filenames
    results = []
    for k in range(len(filename)):
        results.append(read_one_image_array(filename[k], labelfile, None, hst))

    arrays = [r[0] for r in results]
    for k in range(len(arrays)):
        array = arrays[k]
        if len(array.shape) < 3:
            arrays[k] = np.reshape(array, (1,) + array.shape)

    array = np.vstack(arrays)
    return (array,) + results[0][1:]

def read_one_image_array(filename, labelfile, obj=None, hst=False):
    """Return the 3D pixel array and the default display orientation, given the
    file and optional object number.
    """

    # Attempt to read the Pickle image; IOError if file not found
    try:
        with open(filename, 'rb') as f:
            array3d = pickle.load(f)

        if len(array3d.shape) == 2:
            array3d = array3d.reshape((1,) + array3d.shape)
        return (array3d, False, None)
    except IOError as e:    # Problem reading file
        raise e
    except Exception:       # Not a pickle file
        pass

    # Attempt to read a Numpy save file
    try:
        array3d = np.load(filename)
        if len(array3d.shape) == 2:
            array3d = array3d.reshape((1,) + array3d.shape)
        return (array3d, False, None)
    except (IOError, ValueError):
        pass

    # Attempt to read a VICAR image
    try:
        vic = VicarImage.from_file(filename, extraneous='print')
        array3d = vic.data_3d

        # Get filter name for Cassini ISS
        try:
            if vic['INSTRUMENT_HOST_NAME'] == 'CASSINI ORBITER':
                (filter1, filter2) = vic['FILTER_NAME']
                filter_name = filter1 + "+" + filter2
                return (array3d, False, ('CASSINI', 'ISS', filter_name))
        except (VicarError, KeyError):
            pass

        # Get filter name for Galileo SSI
        try:
            if vic['MISSION'] == 'GALILEO':
                filtno = vic['FILTER']
                filter_name = GALILEO_SSI_NAMES[filtno]
                return (array3d, False, ('GALILEO', 'SSI', filter_name))
        except (VicarError, KeyError):
            pass

        try:
            if vic['LAB01'][:7] == 'GLL/SSI':
                filtno = int(vic['LAB03'].partition('FILTER=')[2][0])
                filter_name = GALILEO_SSI_NAMES[filtno]
                return (array3d, False, ('GALILEO', 'SSI', filter_name))
        except (VicarError, KeyError):
            pass

        # Get filter name for Voyager ISS
        try:
            if vic['LAB02'][:3] == 'VGR':
                filter_name = vic['LAB03'][37:43].rstrip()
                return (array3d, False, ('VOYAGER', 'ISS', filter_name))
        except (VicarError, IndexError, KeyError):
            pass

        return (array3d, False, None)

    except VicarError:
        pass

    # Attempt to read a FITS image
    with open(filename, 'rb') as f:
        test = f.read(9)

    if test == b'SIMPLE  =':
        try:
            with warnings.catch_warnings(): # Error, not warning, if not FITS
                warnings.filterwarnings('error')
                hdulist = pyfits.open(filename)
                fitsobj = hdulist[0]       # IndexError if not a FITS file

                # Get the filter info
                inst_host = None
                inst_id = None
                filter_name = None

                try:
                    inst_host = hdulist[0].header['TELESCOP']  # For HST
                except KeyError:
                  try:
                    inst_host = hdulist[0].header['HOSTNAME']  # For NH
                  except KeyError:
                    pass

                try:
                    inst_id = hdulist[0].header['INSTRUME']
                    if 'DETECTOR' in hdulist[0].header:
                      inst_id += '/' + hdulist[0].header['DETECTOR']  # For HST
                except KeyError:
                  try:
                    inst_id = hdulist[0].header['INSTRU'].upper().strip() # NH
                  except KeyError:
                    pass

                # Get filter name for HST/WFC3 or HST/NICMOS or NH/MVIC
                try:
                    filter_name = hdulist[0].header['FILTER'].upper().strip()
                except KeyError:
                    pass

                # Get filter name for HST/ACS
                try:
                    filter_name = (hdulist[0].header['FILTER1'],
                                   hdulist[0].header['FILTER2'])
                except KeyError:
                    pass

                # Get filter name for HST/WFPC2
                try:
                    filter_name = (hdulist[0].header['FILTNAM1'],
                                   hdulist[0].header['FILTNAM2'])
                except KeyError:
                    pass

                # Load array(s)
                array3d = None

                if obj is None:
                    if hst and inst_id == 'ACS/WFC':
                        array = hdulist[1].data    # WFC2
                        try:
                            array2 = hdulist[4].data
                            shape = (2,) + array.shape
                            array3d = np.empty(shape)
                            array3d[0] = array      # WFC2
                            array3d[1] = array2     # WFC1
                        except IndexError:
                            array3d = array

                    elif hst and inst_id == 'WFPC2':
                        array3d = []
                        for hdu in hdulist:
                            array = hdu.data
                            if not isinstance(array, np.ndarray):
                                continue
                            if len(array.shape) not in (2,3):
                                continue
                            array3d.append(array)
                        array3d = np.array(array3d)

                    else:
                        for hdu in hdulist:
                            array3d = hdu.data
                            if not isinstance(array3d, np.ndarray):
                                continue
                            if len(array3d.shape) in (2,3):
                                break

                elif isinstance(obj, (list,tuple)):
                    layers = []
                    for o in obj:
                        array2d = hdulist[o].data
                        layers.append(array2d)

                    array3d = np.stack(layers)

                else:
                    try:
                        obj = int(obj)
                    except ValueError:
                        pass

                    array3d = hdulist[obj].data.copy()

                if array3d is None:
                    raise IOError("Image array not found in FITS file")

                if len(array3d.shape) == 2:
                    array3d = array3d.reshape((1,) + array3d.shape)

                hdulist.close()

                return(array3d, True, (inst_host, inst_id, filter_name))
 
        except (UserWarning, OSError):          # if not a FITS file
            pass

    # Attempt to read a PIL-compatible file or 16-bit TIFF
    try:
        array2d = read_array(filename, False)
        array3d = array2d.reshape((1,) + array2d.shape)
        return (array3d, False, None)
    except IOError:
        pass

    # Attempt to read a PDS3 label
    if labelfile:
        result = read_pds_labeled_image_array(labelfile, obj)
        if result is not None:
            return result

    raise IOError("Unrecognized image file format: " + filename)

################################################################################
# Support for PDS-labeled images
################################################################################

def read_pds_labeled_image_array(filename, obj=None):

    label = None
    try:
        label = pdsparser.PdsLabel.from_file(filename)
    except pdsparser.ParseException:
        (head,ext) = os.path.splitext(filename)
        if ext.lower() != '.lbl':
            if os.path.exists(head + '.lbl'):
                try:
                    label = pdsparser.PdsLabel.from_file(head + '.lbl')
                except pdsparser.ParseException:
                    pass
            elif os.path.exists(head + '.LBL'):
                try:
                    label = pdsparser.PdsLabel.from_file(head + '.LBL')
                except pdsparser.ParseException:
                    pass

    if not label:
        return None

    if isinstance(obj, str):
        pname = '^' + obj
        if pname not in label:
            raise KeyError('Object %s not found in %s' % (obj, filename))

    else:
        pnames = [node.name for node in label
                  if node.name.startswith('^') and node.name.endswith('IMAGE')]
        if not pnames:
            raise KeyError('No IMAGE objects found in %s' % filename)

        if obj is None:
            obj = 0

        try:
            pname = pnames[obj]
        except IndexError:
            raise IndexError('Object index %s is out of range in %s' %
                             (str(obj), filename))
        except TypeError:
            raise TypeError('Invalid index type %s for %s' %
                             (str(obj), filename))

    node = label[pname]
    if isinstance(node, pdsparser.PdsOffsetPointer):
        imagefile = node.value
        offset = node.offset - 1
        if node.unit == 'RECORDS':
            offset *= label['FILE_RECORDS'].value
    else:
        imagefile = node.value
        offset = 0

    imagefile = os.path.join(os.path.split(filename)[0], imagefile)

    image = label[pname[1:]]
    lines = image['LINES'].value
    samples = image['LINE_SAMPLES'].value
    bytes = image['SAMPLE_BITS'].value // 8
    fmt = image['SAMPLE_TYPE'].value

    try:
        prefix_bytes = image['PREFIX_BYTES'].value
    except KeyError:
        prefix_bytes = 0

    try:
        suffix_bytes = image['SUFFIX_BYTES'].value
    except KeyError:
        suffix_bytes = 0

    prefix_samples = prefix_bytes // bytes
    if prefix_samples * bytes != prefix_bytes:
        raise ValueError('PREFIX_BYTES and SAMPLE_BITS values are '
                         'incompatible in ' + imagefile)

    suffix_samples = suffix_bytes // bytes
    if suffix_samples * bytes != suffix_bytes:
        raise ValueError('SUFFIX_BYTES and SAMPLE_BITS values are '
                         'incompatible in ' + imagefile)

    row_samples = prefix_samples + samples + suffix_samples

    offset_samples = offset // bytes
    if suffix_samples * bytes != suffix_bytes:
        raise ValueError('SAMPLE_BITS and file offset values are '
                         'incompatible in ' + imagefile)

    char1 = '>'
    if 'PC_' in fmt or 'LSB_' in fmt:
        char1 = '<'

    char2 = 'i'
    if 'UNSIGNED' in fmt:
        char2 = 'u'
    if 'REAL' in fmt:
        char2 = 'f'

    dtype = char1 + char2 + str(bytes)

    data = np.fromfile(imagefile, dtype=dtype)
    data = data[offset_samples:]
    data = data[:lines * row_samples]
    array3d = data.reshape(1, lines, row_samples)
    array3d = array3d[..., prefix_samples:prefix_samples + samples]

    # Get supplemental info
    try:
        inst_host = label['INSTRUMENT_NAME'].value
    except KeyError:
        try:
            inst_host = label['SPACECRAFT_NAME'].value
        except KeyError:
            inst_host = ''

    try:
        inst_name = label['INSTRUMENT_HOST_NAME'].value
    except KeyError:
        inst_name = ''

    try:
        filter_name = label['FILTER_NAME'].value
    except KeyError:
        filter_name = ''

    return (array3d, False, (inst_host, inst_name, filter_name))

################################################################################
# Slice out the 2-D subarray of a 3-D array
################################################################################

def slice_array(array3d, samples=None, lines=None, bands=None, valid=None,
                         crop=None):
    """Returns the requested slice of a 3-D array as a 2-D array. The input
    3-D array is not modified.

    Input:
        array3d         a 3-D image array indexed (bands, lines, samples).
        samples         a tuple containing the range of lines to include in the
                        output image; default is None for all.
        lines           a tuple containing the range of lines to include in the
                        output image; default is None for all.
        bands           a tuple containing the range of bands to average for the
                        output 2-D array; default is None for all.
        valid           a tuple containing the numeric range of valid pixels;
                        default is None to make all pixels valid.
        crop            crop any pixels at the border of the image matching this
                        numeric value. None implies no cropping.

    Return:             a tuple containing two values:
                        [0]: a 2-D array in which the image has been averaged
                             across the set of bands selected. Note that invalid
                             pixels are not included in the average.
                        [1]: The mask array, which could be None if no pixels
                             are masked.
    """

    # Slice out the needed part of the image
    slice3d = array3d
    if samples:
        slice3d = slice3d[:, :, samples[0]:samples[1]]
    if lines:
        slice3d = slice3d[:, lines[0]:lines[1], :]
    if bands:
        slice3d = slice3d[bands[0]:bands[1], :, :]

    # Create a masked array if some pixel values are invalid
    masked = slice3d
    has_invalid_pixels = False

    nan_mask = np.isnan(masked)
    if np.any(nan_mask):
        masked = np.ma.masked_invalid(masked)
        masked.data[nan_mask] = 0.
        has_invalid_pixels = True

    if valid:
        masked = np.ma.masked_outside(masked, valid[0], valid[1])
        has_invalid_pixels = True

    # Crop if necessary
    if crop is not None:
        masked = crop_array(masked, crop)

    # Derive mean of bands and convert to 2-D
    if bands[1] - bands[0] > 1:
        array2d = np.ma.mean(masked, axis=0)
    else:
        array2d = masked[0,:,:].copy()

    # Make a final search for invalid pixels
    invalid_mask = None
    if has_invalid_pixels:
        mask = np.ma.getmaskarray(masked)
        mask = masked.mask
        if np.any(mask):
            invalid_mask = mask[0,:,:]

    return (array2d, invalid_mask)

################################################################################
# Trim away missing data around the edges of an image
################################################################################

def crop_array(array, value=0., samples=True, lines=True):
    """Crops away constant values (typically zero) around the periphery of an
    image. Handles masked arrays too.

    Input:
        array           a 2-D image array indexed (lines, samples) or a 3-D
                        array indexed (bands, lines, samples).
        value           the constant value to trim away.
        samples         True to trim away samples; False to leave them.
        lines           True to trim away lines; False to leave them.

    Return:             a slice of the image with possibly reduced dimensions.
    """

    # Return an empty array as is
    if np.ma.allequal(array, value):
        return array

    # Add a leading band axis if necessary
    original_array = array
    if original_array.ndim == 2:
        array = array[np.newaxis,:,:]

    # Get the shape
    (_, nlines, nsamples) = array.shape

    # Count empty lines from each end
    lmin = 0
    lmax = nlines - 1
    if lines:
        while np.ma.allequal(array[:,lmin,:], value):
            lmin += 1
        while np.ma.allequal(array[:,lmax,:], value):
            lmax -= 1

    # Count empty rows from each side
    smin = 0
    smax = nsamples - 1
    if samples:
        while np.ma.allequal(array[:,:,smin], value):
            smin += 1
        while np.ma.allequal(array[:,:,smax], value):
            smax -= 1

    return original_array[..., lmin:lmax+1, smin:smax+1]

################################################################################
# Fill zebra stripes in a 2-D array
################################################################################

def fill_zebra_stripes(array2d):
    """Fills lines of zeros at the beginning and end of each row of nonzero
    values exist above and below them. This removes an artifact associated with
    some spacecraft compression procedures.

    Input:
        array2d         a 2-D numpy array.

    Return:             a pointer to the same array, modified in place.
    """

    # Get the dimensions
    (lines, samples) = array2d.shape

    # Loop through lines
    lprev = 1                       # Avoids indexing error in first line
    for l in range(lines):
        lnext = l + 1
        if lnext == lines:          # Avoids indexing error in last line
            lnext = l - 1

        # Average over stripes starting from left
        for s in range(samples):
            if array2d[l,s] != 0:
                break

            array_above = int(array2d[lprev,s])
            array_below = int(array2d[lnext,s])

            if array_above and array_below:
                array2d[l,s] = (array_above + array_below)/2

        # Average over stripes starting from right
        for s in range(samples-1, -1, -1):
            if array2d[l,s] != 0:
                break

            array_above = int(array2d[lprev,s])
            array_below = int(array2d[lnext,s])

            if array_above and array_below:
                array2d[l,s] = (array_above + array_below)/2

        # Note: It is safe to work on the array in place because we never
        # change a pixel unless it is zero and the pixels above and below
        # are both nonzero.

        lprev = l

    return array2d

################################################################################
# Determine the numeric limits for a stretch
################################################################################

HISTOGRAM_BINS = 1024

def get_limits(array2d, mask, limits=None, percentiles=(0.,100.),
               assume_int=False, trim=0, trim_zeros=False, footprint=0):
    """Determines the stretch limits of an image based on defined limits and/or
    percentiles.
    
    Input:
        array2d         the 2-D numpy array, which may be masked.
        mask            the 2-D mask array, True for masked pixels. None if no
                        pixels are masked

        limits          numeric limits within which to confine histogram, or
                        None for the full dynamic range of the array.

        percentiles     percentiles corresponding to returned lower and upper
                        limits.

        assume_int      True to treat the image array as if it contained
                        integers, even though it may not. Integer histograms
                        actually extend from 0.5 below the lower limit to 0.5
                        above the upper.

        trim            the number of pixels around the image edge to exclude
                        from the histogram. Sometimes the edge of an image can
                        contain bad pixels. Default 0.

        trim_zeros      trim any exterior rows or columns that contain all zeros
                        before calculating the limits.

        footprint       size of the 2-D median filter to apply as an alternative
                        way to set the limits.

    Return: The derived limits for the stretch.
    """

    # Make note of whether the pixels are integers or floats
    is_int = array2d.dtype.kind in ("i","u")
    if assume_int:
        is_int = True

    # Trim the array if necessary
    if trim != 0:
        trimmed = array2d[trim:-trim, trim:-trim]
        if mask is None:
            tmask = np.zeros(trimmed.shape, dtype='bool')
        else:
            tmask = mask[trim:-trim, trim:-trim]
    else:
        trimmed = array2d
        tmask = mask

    trimmed_v1 = trimmed
    tmask_v1 = tmask
    if trim_zeros:
        if tmask is None:
            tmask = np.zeros(trimmed.shape, dtype='bool')

        while trimmed.size and np.all(trimmed[0] == 0):
            trimmed = trimmed[1:]
            tmask = tmask[1:]
        while trimmed.size and np.all(trimmed[-1] == 0):
            trimmed = trimmed[:-1]
            tmask = tmask[:-1]
        while trimmed.size and np.all(trimmed[:,0] == 0):
            trimmed = trimmed[:,1:]
            tmask = tmask[:,1:]
        while trimmed.size and np.all(trimmed[:,-1] == 0):
            trimmed = trimmed[:,:-1]
            tmask = tmask[:,:-1]

        if trimmed.size == 0:
            trimmed = trimmed_v1
            tmask = tmask_v1

    # Identify the dn limits, excluding NANs
    if tmask is None:
        non_nans = trimmed
    else:
        non_nans = trimmed[~tmask]

    if non_nans.size:
        array_min = non_nans.min()
        array_max = non_nans.max()
    else:               # empty image
        array_min = 0
        array_max = 0

    # Deal with a single value
    if array_min == array_max:
        if is_int:
            return (array_min, array_min + 1)
        elif array_min == 0.:
            return (0., 1.)
        elif array_min < 0.:
            return (array_min, 0.)
        else:
            return (array_min, array_min * 2.)

    # Identify the valid extremes of the image
    if limits is None:
        if is_int:
            limits = (array_min - 0.5, array_max + 0.5)
        else:
            limits = (array_min, array_max)

    # Create the histogram and locate percentiles if necessary
    if not percentiles:
        percentiles = (0.,100.)

    if percentiles != (0.,100.):

        # Allow an integer histogram to be optimally sampled
        if is_int:

            # Expand the histogram range to the first half-integer below the
            # the lower limit and above the upper limit
            dn0 = np.floor(limits[0] + 0.5) - 0.5
            dn1 = np.ceil( limits[1] - 0.5) + 0.5

            hbins = dn1 - dn0
            hrange = (dn0, dn1)

            # Reduce the number of bins if it gets ridiculous
            if hbins > HISTOGRAM_BINS:
                hbins = HISTOGRAM_BINS

        else:
            # Sample a floating-point histogram the usual way
            hbins = HISTOGRAM_BINS
            hrange = limits

        # Create histogram
        hbins = int(hbins)
        hist = np.histogram(non_nans, bins=hbins, range=hrange)

        # Generate the cumulative histogram with a leading 0.
        cumhist = np.array([0] * (hbins+1), "float64")
        np.cumsum(hist[0], out=cumhist[1:])

        # Save the dn list too
        dnlist = hist[1]

        # Rescale the cumulative histogram as percentiles 0-100
        cumvals = np.interp(limits, dnlist, cumhist)
        percentlist = 100. * ((cumhist    - cumvals[0]) /
                              (cumvals[1] - cumvals[0]))

        # Locate the percentiles
        limits = (_percentile_lookup(percentiles[0], percentlist, dnlist,
                                                                 limits),
                  _percentile_lookup(percentiles[1], percentlist, dnlist,
                                                                 limits))

    # Median-filter the array if necessary
    if footprint:
        circle_footprint = circle_mask(footprint)
        filtered = median_filter(trimmed, footprint=circle_footprint)

        if tmask is None:
            limits = (max(filtered.min(), limits[0]),
                      min(filtered.max(), limits[1]))
        else:
            limits = (max(filtered[~tmask].min(), limits[0]),
                      min(filtered[~tmask].max(), limits[1]))

    return limits

def _percentile_lookup(p, percentlist, dnlist, limits):

    # Return expected values beyond limits
    if p <= 0.:
        return limits[0]
    if p >= 100.:
        return limits[1]

    # Perform an interpolation
    dn = np.interp(p, percentlist, dnlist)

    # Check limits
    if dn <= limits[0]:
        return limits[0]
    if dn >= limits[1]:
        return limits[1]

    # Failure occurs if the value of p appears more than once in the table
    if np.isnan(dn):
        return np.mean(dnlist[np.where(percentlist == p)])

    # Otherwise all is well
    return dn

################################################################################
# Return the colormap based on filter info
################################################################################

VOYAGER_ISS_DICT = {
    "UV"    : (200, 60,255),
    "VIOLET": (200,120,255),
    "BLUE"  : (110,110,255),
    "GREEN" : (110,255,110),
    "ORANGE": (255,170,100),
    "NAD"   : (110,255,110),
    "SODIUM": (110,255,110),
    "CH4_U" : (255, 60, 60),
    "CH4/U" : (255, 60, 60),
    "CH4_JS": (255, 60, 60),
    "CH4/JS": (255, 60, 60),
}

NH_MVIC_DICT = {
    "BLUE"  : (110,110,210),
    "RED"   : (190,100,100),
    "NIR"   : (210, 65, 45),
    "CH4"   : (230, 35, 35),
}

GALILEO_SSI_NAMES = ["CLEAR", "GREEN", "RED", "VIOLET",
                     "IR-7560", "IR-9680", "IR-7270", "IR-8890"]
GALILEO_SSI_DICT = {
    "CLEAR"  : (128,128,128),
    "RED"    : (190,130,100),
    "GREEN"  : (110,190,110),
    "VIOLET" : (160,100,200),
    "IR-7270": (200,100,100),
    "IR-7560": (210, 80, 80),
    "IR-8890": (220, 60, 60),
    "IR-9680": (230, 40, 40),
}

RGB_BY_NM = np.array([                      # [wavelength, r, g, b]
    [380., 200.500,  60.500, 255.999],      # uv
    [410., 200.500, 110.500, 255.999],      # violet
    [480., 110.500, 110.500, 255.999],      # blue
    [540., 110.500, 255.999, 110.500],      # green
    [580., 255.999, 255.999, 110.500],      # yellow
    [610., 255.999, 180.500, 110.500],      # orange
    [650., 255.999, 110.500, 110.500],      # red
    [750., 255.999,  60.500,  60.500],      # ir
])

RFUNC = Tabulation(RGB_BY_NM[:,0], RGB_BY_NM[:,1])
GFUNC = Tabulation(RGB_BY_NM[:,0], RGB_BY_NM[:,2])
BFUNC = Tabulation(RGB_BY_NM[:,0], RGB_BY_NM[:,3])

def tinted_colormap(filter_info):
    """Returns a colormap based on a tuple of filter info.

    Input:
        filter_info     a tuple (instrument_host, instrument_id, filter), where
                        the filter might be a tuple of two filter names.

    Return:             a color map of the form (black, tint, white), where the
                        tint is based on the filter name.
    """

#     global VOYAGER_ISS_DICT, NH_MVIC_DICT, RGB_BY_NM, RFUNC, GFUNC, BFUNC

    if filter_info is None:
        return None

    (inst_host, inst_id, filter_name) = filter_info
    if filter_name is None:
        return None

    if isinstance(filter_name, tuple):
        (filter1,filter2) = filter_name
        if filter1.startswith('CLEAR') or filter1 == 'CL1' or filter1 == 'N/A':
            filter1 = 'CLEAR'

        if filter2.startswith('CLEAR') or filter2 == 'CL2' or filter2 == 'N/A':
            filter2 = 'CLEAR'

        if filter1 == 'CLEAR':
            filter_name = filter2
        elif filter2 == 'CLEAR':
            filter_name = filter1
        else:
            filter_name = filter1 + '+' + filter2

    if filter_name == 'CLEAR':
        return [(0,0,0), (255,255,255)]

    if inst_host is not None:
        if 'HUBBLE' in inst_host or 'HST' in inst_host:
            if filter_name in ['F350LP','F606W', 'LONG_PASS']:
                return [(0,0,0), (255,255,255)]

            wavelength = 0
            for c in filter_name:
                if (c >= '0') and (c <= '9') and wavelength < 1600:
                    wavelength = 10*wavelength + int(c)

            if 'NIC' in inst_id:
                wavelength *= 3.5
            elif ('WFC3' in inst_id or 'IR' in inst_id) and wavelength < 200:
                wavelength *= 3.5
            elif ('ACS' in inst_id or 'SBC' in inst_id) and wavelength < 200:
                wavelength *= 3.5
            elif filter_name.startswith('FQUV'):    # WFPC2 filters
                wavelength = 300
            elif filter_name.startswith('FQCH4'):   # WFPC2 filters
                wavelength = 900
            elif filter_name == 'POL0S':            # NICMOS filter
                wavelength = 110 * 3.5
            elif filter_name == 'POL0L':            # NICMOS filter
                wavelength = 220 * 3.5

            if wavelength == 0:
                print('******UNKNOWN FILTER:', inst_id, filter_name)
                return None

            wavelength = max(wavelength, RGB_BY_NM[ 0,0])
            wavelength = min(wavelength, RGB_BY_NM[-1,0])

            r = int(RFUNC(wavelength))
            g = int(GFUNC(wavelength))
            b = int(BFUNC(wavelength))

            return [(0,0,0), (r,g,b), (255,255,255)]

        if inst_host.startswith('VOYAGER') or inst_host.startswith('VG'):
            if inst_id.startswith('ISS'):
                return [(0,0,0), VOYAGER_ISS_DICT[filter_name], (255,255,255)]
            else:
                return [(0,0,0), (255,255,255)]

        if inst_host.startswith('CASSINI'):
            if inst_id.startswith('ISS'):
                if   "IR"    in filter_name: tint = (200, 80, 80)
                elif "UV"    in filter_name: tint = (160, 80,220)
                elif "VIO"   in filter_name: tint = (160,120,200)
                elif "BL"    in filter_name:
                    if "GRN" in filter_name: tint = (110,180,180)
                    else                   : tint = (110,110,180)
                elif "GRN"   in filter_name:
                    if "RED" in filter_name: tint = (190,190,110)
                    else                   : tint = (110,190,110)
                elif "RED"   in filter_name: tint = (190,110,100)
                elif "MT1"   in filter_name: tint = (190,110,100)
                elif "CB1"   in filter_name: tint = (190,110,100)
                elif "HAL"   in filter_name: tint = (190,110,100)
                elif "MT"    in filter_name: tint = (200, 80, 80)
                elif "CB"    in filter_name: tint = (200, 80, 80)
                else                       : tint = (127,127,127)

                return [(0,0,0), tint, (255,255,255)]
            else:
                return [(0,0,0), (255,255,255)]

        if inst_host.startswith('GALILEO'):
            if inst_id == 'SSI' or inst_id.startswith('SOLID'):
                return [(0,0,0), GALILEO_SSI_DICT[filter_name], (255,255,255)]
            else:
                return [(0,0,0), (255,255,255)]

        if inst_host in ('NEW HORIZONS', 'NH'):
            if inst_id in ('MVIC', 'MVI'):
                return [(0,0,0), NH_MVIC_DICT[filter_name], (255,255,255)]
            else:
                return [(0,0,0), (255,255,255)]

    return None

################################################################################
# Apply rotation
################################################################################

def rotate_array_rgb(arrayRGB, display_upward, rotation_name):
    """Applies an arbitrary orientation to an RGB array.

    Input:
        arrayRGB        an RGB array.
        display_upward  True if the image should be displayed upward;
                        False if it should be displayed downward.
        rotation_name   name of the rotation to be applied. Choices are
                        "FLIPTB", "FLIPLR", "ROT90", "ROT180", ROT270". Case is
                        insignificant.
    """

    # Apply the default orientation
    if display_upward:
        arrayRGB = np.flipud(arrayRGB)

    # Apply an additional rotation if necessary
    if rotation_name:
        rotation_name = rotation_name.upper()

        if rotation_name == "NONE":
            pass

        elif rotation_name == "FLIPLR": arrayRGB = np.fliplr(arrayRGB)
        elif rotation_name == "FLIPTB": arrayRGB = np.flipud(arrayRGB)

        elif rotation_name == "ROT90":  arrayRGB = np.rot90(arrayRGB, 1)
        elif rotation_name == "ROT180": arrayRGB = np.rot90(arrayRGB, 2)
        elif rotation_name == "ROT270": arrayRGB = np.rot90(arrayRGB, 3)

        else: raise KeyError("Unrecognized rotation method: " + rotation_name)

    return arrayRGB

################################################################################
# Apply colormap
################################################################################

def apply_colormap(array2d, limits, histogram=False, colormap=None,
                   invalid_mask=None,
                   below_color=None, above_color=None, invalid_color="black"):
    """Applies the colormap to a grayscale image, producing a 3-D array with
    either one band if grayscale or three bands (R,G,B) if color. The axis
    order is (line,sample,band).

    Input:
        array2d         a 2-D numpy array for colormapping.
        limits          the array values that correspond to the first and last
                        colors in the mapping.
        histogram       True to use histogram shading, in which case the
                        returned images has a uniform distribution of DNs;
                        False otherwise.
        colormap        an N-tuple of colors to map from the lower to upper
                        limit.
        invalid_mask    a boolean mask of invalid pixels, or None if all pixels
                        are valid.
        below_color     the color to use for any pixels below the lower limit.
                        Default is the first color of the colormap.
        above_color     the color to use for any pixels above the upper limit.
                        Default is the last color of the colormap.
        invalid_color   the color to use for invalid pixels.

    Return              a 3-D array containing the new colors mapped to (0.,1.).
                        The array has three bands (R,G,B) if the output is
                        color; it has one band if grayscale.

    Note: Input colors can be specified by name or by (R,G,B) triple. If the
    latter, 0 is black and 255 is white.
    """

    # Defaults
    is_gray = True
    mapcolors = 2

    # Set highlight color values to arrays in range 0-1
    highlights = [below_color, above_color, invalid_color]
    for i in range(len(highlights)):
        if highlights[i]:
            if isinstance(highlights[i], str):
                highlights[i] = ColorNames.lookup(highlights[i])

            highlights[i] = np.array(highlights[i][:], 'float') / 255.

            if (highlights[i][0] != highlights[i][1] or
                highlights[i][0] != highlights[i][2]):
                    is_gray = False

    # An invalid color must be defined, defaults to black
    if highlights[2] is None:
        highlights[2] = np.zeros((3), 'float')

    # Interpret the colormap
    if colormap:

        # Interpret the colormap if it involves strings
        if isinstance(colormap, str):
            names = colormap.split("-")
            colormap = [ColorNames.lookup(name) for name in names]

        # A single color indicates the mid-scale tint
        if len(colormap) == 1:
            colormap = [(0,0,0), colormap[0], (255,255,255)]

        # Count the colors
        mapcolors = len(colormap)

        # Check for colors in colormap
        for c in colormap:
            if (c[0] != c[1] or c[0] != c[2]):
                is_gray = False

        # Extend the map to avoid potential indexing errors below
        if isinstance(colormap, tuple):
            colormap = list(colormap)
        colormap.append(colormap[-1])
        colormap.append(colormap[-1])

        # Convert to an array scaled 0-1
        colormap = np.array(colormap, 'float') / 255.

    # Determine whether we need one or tree channels
    if is_gray:
        channels = 1
    else:
        channels = 3

    # Apply the histogram scaling if necessary
    if histogram:
        normalized = rankdata(array2d)
        normalized = normalized.reshape(array2d.shape)
        mask = (limits[0] <= array2d) & (array2d <= limits[1])
        limits = (np.min(normalized[mask]),
                  np.max(normalized[mask]))
    else:
        normalized = array2d

    # Scale the image to the range zero to number of colors
    scaled = normalized.astype("float")
    denom = limits[1] - limits[0]
    if denom == 0:
        denom = 1.
    scaled = (mapcolors-1) * ((scaled - limits[0]) / float(denom))
    scaled = scaled.clip(0, mapcolors-1)

    # Apply the lookup table if necessary
    if colormap is not None:

        # Extract the index and fractional bit of every pixel
        (indices, fracs) = np.divmod(scaled, 1.)
        indices = indices.astype('int')

        # Map through the lookup table (tricky!)
        result = np.zeros((array2d.shape[0], array2d.shape[1], channels))
        for c in range(channels):
            below = np.take(colormap[:,c], indices)
            above = np.take(colormap[:,c], indices+1)
            result[:,:,c] = (below + fracs * (above - below))
    else:
        if channels == 1:
            result = np.atleast_3d(scaled)
        else:
            result = np.dstack((scaled, scaled, scaled))

    # Apply highlights if necessary
    for c in range(channels):
        slice = result[:,:,c]

        if highlights[0] is not None:
            slice[array2d < limits[0]] = highlights[0][c]
        if highlights[1] is not None:
            slice[array2d > limits[1]] = highlights[1][c]

        if invalid_mask is not None:
            slice[invalid_mask] = highlights[2][c]

    return result

################################################################################
# Apply gamma factor to an array scaled (0-1)
################################################################################

def apply_gamma(array, gamma):
    """Applies the gamma factor to an array already scaled 0-1.

    Input:
        array           a 2-D or 3-D numpy array.
        gamma           gamma factor to apply. > 1 to brighten intermediate
                        grays; < 1 to darken them.

    Return              a pointer to the rescaled array, changed in place.
    """

    if gamma != 1.:
        array = array**(1./gamma)

    return array

################################################################################
# Determine unwrapped image dimensions
################################################################################

def get_size(array_shape, size=None, scale=(100.,100.), frame=None, wrap=False,
                          wrap_ratio=None, overlap=(0.,0.), gap_size=1):
    """Returns the output image size (width, height) and wrap properties based
    on the shape of the array (neglecting bands, if any).
    
    Input:
        array_shape     shape of the numpy array, which could be 2-D or 3-D.
                        Index order is (lines, samples) or (lines, samples,
                        bands).
        size            a new set of dimensions (width, height). Use a single
                        value for a square image, or None to preserve the given
                        array size.
        scale           a scale factor to apply to the image. Provide a tuple
                        to scale the width and height by different amounts. None
                        implies no scaling.
        frame           the firm outer limit on the size of the output image.
                        If the result of the above parameters exceeds the frame
                        in either dimension, the image is scaled down
                        proportionally to fit inside the frame. A single value
                        implies a square frame; a tuple can be used to specify
                        each dimension; None implies no frame constraint.
        wrap            True to wrap the image in a way that maximizes detail
                        and minimizes distortion.
        wrap_ratio      wrap the sections of an image if its width:height ratio
                        or its height:width ratio exceeds this value. None to
                        ignore this option.
        overlap         a tuple defining the range of allowed overlaps between
                        the end of one wrapped section and the beginning of the
                        next. For example, (5,10) means that between 5% and 10%
                        of the last pixels in one section of a wrapped image.
        gap_size        number of pixels to reserve as blank between any wrapped
                        sections of the array.

    Return:             a tuple (unwrapped_shape, wrapped_shape, sections,
                                                                 wrap_axis)
        unwrapped_size  shape of the PIL image (w,h) before wrapping but after
                        any re-scaling.
        wrapped_size    shape of the PIL image (w,h) after wrapping.
        sections        number of sections to wrap.
        wrap_axis       0 to wrap horizontally, 1 to wrap vertically.
    """

    # Normalize inputs
    if size is not None:
        if not isinstance(size, (list,tuple)):
            size = (size, size)

    if scale is not None:
        if not isinstance(scale, (list,tuple)):
            scale = (scale, scale)

    if frame is not None:
        if not isinstance(frame, (list,tuple)):
            frame = (frame, frame)

    # Apply scale factor to shape
    array_size = [array_shape[1], array_shape[0]]   # [width, height]
    if scale is not None:
        array_size[0] *= scale[0]/100.
        array_size[1] *= scale[1]/100.

    # Determine the output size based on size or frame
    if size is not None:
        (unwrapped_size, quality,
         expand) = _get_size_for_size(array_size, size, 0, 1., 1.)
    elif frame is not None:
        (unwrapped_size, expanded_size, quality,
         expand) = _get_size_for_frame(array_size, frame, 0, 1., 1.)
    else:
        unwrapped_size = [int(array_size[0] + 0.5), int(array_size[1] + 0.5)]

        # Handle a limit on the wrap ratio
        if wrap_ratio:
          if unwrapped_size[0] > wrap_ratio * unwrapped_size[1]:
            for k in range(2, 101):
                expand = 1. + overlap[0]/100. * (k-1.)/k
                wrapped_size = [int(unwrapped_size[0]/k * expand + 0.5),
                                unwrapped_size[1] * k + gap_size * (k-1)]
                if wrapped_size[0] <= wrap_ratio * wrapped_size[1]:
                    return (unwrapped_size, wrapped_size, k, 0)

          if unwrapped_size[1] > wrap_ratio * unwrapped_size[0]:
            for k in range(2, 101):
                expand = 1. + overlap[0]/100. * (k-1.)/k
                wrapped_size = [unwrapped_size[0] * k + gap_size * (k-1),
                                int(unwrapped_size[1]/k * expand + 0.5)]
                if wrapped_size[1] <= wrap_ratio * wrapped_size[0]:
                    return (unwrapped_size, wrapped_size, k, 1)

    # Without the wrapping option, we're done
    if not wrap or ((size is None) and (frame is None)):
        return (unwrapped_size, unwrapped_size, 1, 0)

    best_quality = quality
    best_sections = 1
    best_axis = 0
    best_unwrapped = unwrapped_size
    best_wrapped = unwrapped_size
    best_overlap = 0.

    quality_1x1 = quality

    # Try horizontal, then vertical wrapping
    for axis in (0,1):

      # Increment number of wrap sections until quality starts to drop
      for k in range(2, 101):

        tweak = (k-1.) / k
        expand_min = 1. + overlap[0]/100. * tweak
        expand_max = 1. + overlap[1]/100. * tweak

        # Adjust size and frame for axis, sections and gap
        if size is not None:

            # Calculate the number of pixels (w,h) available for the image if
            # we wrap it into k sections.
            temp_size = [size[0], size[1]]
            temp_size[axis] *= k
            temp_size[1-axis] -= (k-1) * gap_size
            temp_size[1-axis] //= k

            # Get the image size if it is forced to fit into this area
            (unwrapped_size, quality,
             expand) = _get_size_for_size(array_size, temp_size, axis,
                                                      expand_min, expand_max)
            test_overlap = (expand - 1.) / tweak * 100.

            wrapped_size = size

        else:
            temp_frame = [frame[0], frame[1]]
            temp_frame[axis] *= k
            temp_frame[1-axis] -= (k-1) * gap_size
            temp_frame[1-axis] //= k

            (unwrapped_size, expanded_size, quality,
             expand) = _get_size_for_frame(array_size, temp_frame, axis,
                                                       expand_min, expand_max)
            test_overlap = (expand - 1.) / tweak * 100.

            wrapped_size = [expanded_size[0], expanded_size[1]]
            wrapped_size[axis] = (wrapped_size[axis] + (k-1)) // k
            wrapped_size[1-axis] *= k
            wrapped_size[1-axis] += (k-1) * gap_size
            wrapped_size[0] = min(wrapped_size[0], frame[0])
            wrapped_size[1] = min(wrapped_size[1], frame[1])

        if quality < best_quality:
            break

        # If the improvement from 1x1 to 1x2 is marginal, stick with 1x1
        if frame is not None and k == 2 and quality < quality_1x1 * 1.1:
            continue

        best_quality = quality
        best_sections = k
        best_axis = axis
        best_unwrapped = unwrapped_size
        best_wrapped = wrapped_size
        best_overlap = test_overlap

    quality = best_quality
    sections = best_sections
    axis = best_axis
    unwrapped_size = best_unwrapped
    wrapped_size = best_wrapped
    test_overlap = best_overlap

    return (unwrapped_size, wrapped_size, sections, axis)

def _get_size_for_size(array_size, size, axis, expand_min, expand_max):
    # Calculate the size and quality when attempting to fit an image array into
    # a pixel area.
    #
    # Input:
    #   array_size      (w,h) of the image array.
    #   size            (w,h) of the available pixels.
    #   axis            the axis being wrapped: 0 for width; 1 for height.
    #   expand_min      minimum allowed expansion factor on the specified axis.
    #   expand_max      maximum allowed expansion factor on the specified axis.
    #
    # Return: (unexpanded_size, quality, expand)
    #   unexpanded_size exact size of the image to insert into the pixel area,
    #                   before expansion.
    #   quality         quality metric, which is maximized when the image has
    #                   least distortion.
    #   expand          expansion factor to use along the specified axis.

    # Derive the (w,h) scale factors required to fit the image array into the
    # available size, neglecting expansion along the axis
    scale = [size[0] / float(array_size[0]),
             size[1] / float(array_size[1])]

    # Adjust the along-axis scale factor for minimum and maximum expansion
    scale_expmin = [scale[0], scale[1]]
    scale_expmin[axis] /= expand_min

    scale_expmax = [scale[0], scale[1]]
    scale_expmax[axis] /= expand_max

    # Derive distortion factors for minimum and maximum expansion
    # We take the log, so distortion == 0 for a 1:1 ratio of scale factors
    distortion_expmin = np.log(scale_expmin[1] / scale_expmin[0])
    distortion_expmax = np.log(scale_expmax[1] / scale_expmax[0])

    # Select the expansion factor that produces distortion closer to zero
    if abs(distortion_expmin) <= abs(distortion_expmax):
        expand = expand_min
        distortion = abs(distortion_expmin)
    else:
        expand = expand_max
        distortion = abs(distortion_expmax)

    # Choose an intermediate expansion factor if it can give us zero distortion
    if distortion_expmin * distortion_expmax < 0:
        expand = scale[axis] / scale[1-axis]
        distortion = 0.

    # Quality = 1 for zero distortion, smaller for larger distortion ratios
    quality = np.exp(-distortion)

    # Determine the size of the array to wrap
    unexpanded_size = [size[0], size[1]]
    unexpanded_size[axis] = int(unexpanded_size[axis]/expand + 0.5)

    return (unexpanded_size, quality, expand)

def _get_size_for_frame(array_size, frame, axis, expand_min, expand_max):
    # Calculate the size and quality when attempting to fit an image array into
    # a given pixel frame.
    #
    # Input:
    #   array_size      (w,h) of the image array.
    #   frame           (w,h) of the available frame.
    #   axis            the axis being wrapped: 0 for width; 1 for height.
    #   expand_min      minimum allowed expansion factor on the specified axis.
    #   expand_max      maximum allowed expansion factor on the specified axis.
    #
    # Return: (unexpanded_size, quality, expand)
    #   unexpanded_size exact size of the image to insert into the pixel frame,
    #                   before expansion.
    #   expanded_size   size of the image after expansion.
    #   quality         quality metric, which is maximized when the image has
    #                   least distortion.
    #   expand          expansion factor to use along the specified axis.

    # Determine optimal image size inside the frame, assuming minimal expansion
    array_size_expmin = [array_size[0], array_size[1]]
    array_size_expmin[axis] *= expand_min

    scalings = [frame[0] / float(array_size_expmin[0]),
                frame[1] / float(array_size_expmin[1])]

    scale = min(scalings[0], scalings[1])

    optimal_size_float = [scale * array_size_expmin[0],
                          scale * array_size_expmin[1]]

    optimal_size = [min(int(optimal_size_float[0] + 0.5), frame[0]),
                    min(int(optimal_size_float[1] + 0.5), frame[1])]

    # Quality is the fractional filling factor of the image when inserted into
    # the frame
    quality = optimal_size[0] * optimal_size[1] / float(frame[0] * frame[1])

    # Determine size of image before expansion
    unexpanded_size_float = [scale * array_size[0], scale * array_size[1]]
    unexpanded_size = [optimal_size[0], optimal_size[1]]
    unexpanded_size[axis] = int(unexpanded_size_float[axis] + 0.5)

    # Increase the expansion factor for better filling, if possible
    expanded_size = [optimal_size[0], optimal_size[1]]
    expanded_length = unexpanded_size_float[axis] * expand_max
    expanded_size[axis] = min(int(expanded_length + 0.5), frame[axis])

    expand = expanded_size[axis]/scale / float(array_size[axis])

    return (unexpanded_size, expanded_size, quality, expand)

################################################################################
# Convert an array to a PIL image (or list of RGB images).
################################################################################

def array_to_pil(array, twobytes=False, rescale=True):
    """Converts an array to a PIL image. For the special case of a 16-bit RGB
    image, it converts it to a list of three PIL images.

    Input:
        array           image array, scaled 0-1, containing one band of
                        grayscale or three bands if RGB.
        twobytes        True for 16-bit images; False for 8-bit images.
        rescale         True to scale values from unit; False to leave alone.
    Return:             A PIL image or a vector of three.
    """

    # Get the array size in image ordering
    array = np.atleast_3d(array)
    old_size = (array.shape[1], array.shape[0])

    # Determine the number of channels
    channels = array.shape[2]

    # Use PIL 32-bit mode for two-byte images
    if twobytes:

        # Re-scale from unity if necessary
        if rescale:
            array *= 65535.9999

        array = array.astype("int32")

        # Return a list if there are RGB channels
        if channels >= 3:
            result = []
            for c in range(3):
                im = Image.new(mode="I", size=old_size)
                im.putdata(array[:,:,c].flatten())
                result.append(im)

        # Otherwise, return a single PIL image
        else:
            result = Image.new(mode="I", size=old_size)
            result.putdata(array[:,:,0].flatten())

    # Use a PIL "L" or "RGB" image for one-byte images
    else:

        # Re-scale from unity
        if rescale:
            array *= 255.99999

        array = array.astype("uint8")

        imlist = []
        for c in range(channels):
            imlist.append(Image.new(mode="L", size=old_size))
            imlist[c].putdata(array[:,:,c].flatten())

        if channels >= 3:
            result = Image.merge("RGB", imlist[0:3])
        else:
            result = imlist[0]

    return result

################################################################################
# Convert a PIL image (or list of RGB images) to an array.
################################################################################

def pil_to_array(image, rescale=True):
    """Converts a PIL image (or list of RGB images) to an array. The shape of
    the returned array is (lines, samples, bands) for an RGB image or (lines,
    samples) for a grayscale image.

    Input:
        image           a PIL image or list/tuple of three.
        rescale         True to scale values to the range 0-1; False to leave
                        them alone.
    Return:             An array.
    """

    # Determine if it's a triple
    if isinstance(image, (list,tuple)):
        bands = []
        for i in image:
            bands.append(_one_pil_to_array(i, rescale))

        return np.dstack((bands[0], bands[1], bands[2]))

    # Deal with an RGB image in three bands
    if image.mode.startswith("RGB"):
        (r,g,b) = image.split()[:3]

        r = _one_pil_to_array(r, rescale)
        g = _one_pil_to_array(g, rescale)
        b = _one_pil_to_array(b, rescale)

        array = np.dstack((r, g, b))
        return array

    # Otherwise it's a simple case
    return _one_pil_to_array(image, rescale)

def _one_pil_to_array(image, rescale):

    # 32-bit case...
    if image.mode == "I":
        array = np.array(image.getdata(), dtype="uint32")
        array = array.reshape((image.size[1], image.size[0]))

        if rescale:
            array = array.astype("float") / 65535.
        else:
            array = array.astype("uint16")

        return array

    # 8-bit grayscale case...
    if image.mode == "L":
        array = np.array(image.getdata(), dtype="uint8")
        return array.reshape((image.size[1], image.size[0]))

        if rescale:
            array = array.astype("float") / 255.

        return array

    raise IOError("Unsupported PIL image format")

################################################################################
# Filter a PIL mage
################################################################################

FILTER_DICT = { "NONE"              : None,
                "BLUR"              : ImageFilter.BLUR,
                "CONTOUR"           : ImageFilter.CONTOUR,
                "DETAIL"            : ImageFilter.DETAIL,
                "EDGE_ENHANCE"      : ImageFilter.EDGE_ENHANCE,
                "EDGE_ENHANCE_MORE" : ImageFilter.EDGE_ENHANCE_MORE,
                "EMBOSS"            : ImageFilter.EMBOSS,
                "FIND_EDGES"        : ImageFilter.FIND_EDGES,
                "SMOOTH"            : ImageFilter.SMOOTH,
                "SMOOTH_MORE"       : ImageFilter.SMOOTH_MORE,
                "SHARPEN"           : ImageFilter.SHARPEN,
                "MEDIAN_3"          : ImageFilter.MedianFilter(3),
                "MEDIAN_5"          : ImageFilter.MedianFilter(5),
                "MEDIAN_7"          : ImageFilter.MedianFilter(7),
                "MINIMUM_3"         : ImageFilter.MinFilter(3),
                "MINIMUM_5"         : ImageFilter.MinFilter(5),
                "MINIMUM_7"         : ImageFilter.MinFilter(7),
                "MAXIMUM_3"         : ImageFilter.MaxFilter(3),
                "MAXIMUM_5"         : ImageFilter.MaxFilter(5),
                "MAXIMUM_7"         : ImageFilter.MaxFilter(7) }

def filter_image(image, filter_name):
    """Applies an arbitrary filtering to a PIL image. Note that this does not
    work for two-byte images.

    Input:
        image           a PIL image as 8-bit RGB or grayscale.
        filter_name     name of the filter to be applied. Choices are "NONE",
                        "BLUR", "CONTOUR", "DETAIL" ,"EDGE_ENHANCE",
                        "EDGE_ENHANCE_MORE", "EMBOSS", "FIND_EDGES", "SMOOTH",
                        "SMOOTH_MORE", "SHARPEN", "MEDIAN_3", "MEDIAN_5",
                        "MEDIAN_7", "MINIMUM_3", "MINIMUM_5", "MINIMUM_7"
                        ,"MAXIMUM_3", "MAXIMUM_5", and "MAXIMUM_7".

    Return:             a pointer to the filtered image.
    """

    if isinstance(image, list):
        raise ValueError("filtering of 2-byte images is not supported")

    # Look up filter method
    if filter:
        filter_method = FILTER_DICT[filter_name.upper()]
    else:
        filter_method = None

    # Apply filter if necessary
    if filter_method:
        image = image.filter(filter_method)

    return image

################################################################################
# Re-size a PIL image
################################################################################

def resize_image(image, new_size):
    """Re-sizes a PIL image or a list of PIL images.

    Input:
        image           a single PIL image or a list of three images.
        new_size        new (width, height) of image.

    Return:             the re-sized image(s).
    """

    # If the size is unchanged, just return
    if image.size == new_size:
        return image

    # Handle one or three PIL image objects
    if isinstance(image, (list,tuple)):
        result = []
        for i in image: list.append(_resize_one_image(i, new_size))
    else:
        result = _resize_one_image(image, new_size)

    return result

def _resize_one_image(image, new_size):
    """This internal method re-sizes a single PIL image."""

    # Scale up if necessary using NEAREST
    if new_size[0] > image.size[0] or new_size[1] > image.size[1]:
        image = image.resize((max(new_size[0], image.size[0]),
                              max(new_size[1], image.size[1])), Image.NEAREST)

    # Scale down if necessary using ANTIALIAS
    if new_size[0] < image.size[0] or new_size[1] < image.size[1]:
        image = image.resize(new_size, Image.ANTIALIAS)

    return image

################################################################################
# Wrap a PIL image
################################################################################

def wrap_image(image, wrapped_size, sections, wrap_axis, gap_size, gap_color):
    """Wraps a PIL image.

    Input:
        image           a PIL image.
        wrapped_size    (width,height) of the final wrapped images.
        sections        number of sections to wrap.
        wrap_axis       0 to wrap horizontally; 1 to wrap vertically.
        gap_size        width of gap in pixels between each section of the
                        wrapped image.
        gap_color       color to use in the gap, specified as an X11 name or an
                        (R,G,B) triple.

    Return:             a new PIL image of the requested size.
    """

    # Get the gap color if necessary
    if gap_size > 0:
        if isinstance(gap_color, str):
            gap_color = list(ColorNames.lookup(gap_color))
    else:
        gap_color = [0,0,0]

    # Get the image array
    array = pil_to_array(image, rescale=False)
    array = np.atleast_3d(array)
    two_bytes = (array.dtype.itemsize == 2)

    # Create an empty buffer (and convert to RGB if necessary)
    if array.shape[2] == 1 and gap_size > 0 and \
       (gap_color[0] != gap_color[1] or gap_color[0] != gap_color[2]):
        buffer = np.empty((wrapped_size[1], wrapped_size[0], 3),
                           dtype=array.dtype)
    else:
        buffer = np.empty((wrapped_size[1], wrapped_size[0], array.shape[2]),
                          dtype=array.dtype)

    # Match the gap color to the byte size
    if two_bytes:
        gap_color[0] = int(gap_color[0]/255. * 65535.9999)
        gap_color[1] = int(gap_color[1]/255. * 65535.9999)
        gap_color[2] = int(gap_color[2]/255. * 65535.9999)

    # Pre-fill the buffer with the gap color
    if buffer.shape[2] == 1:
        buffer[:,:,0] = gap_color[0]
    else:
        buffer[:,:,0] = gap_color[0]
        buffer[:,:,1] = gap_color[1]
        buffer[:,:,2] = gap_color[2]

    # Insert the sections using horizontal wrapping
    if wrap_axis == 0:
        di = wrapped_size[0]
        dj = (wrapped_size[1] + gap_size) // sections

        dl = dj - gap_size

        float_s0 = 0.5
        float_ds = (image.size[0] - wrapped_size[0]) / (sections - 1.)

        j0 = int((wrapped_size[1] - dj * sections - gap_size)/2. + 0.5)
        for k in range(sections):
            s0 = int(float_s0)
            s1 = s0 + di
            j1 = j0 + dl

            buffer[j0:j1,:] = array[:,s0:s1]

            float_s0 += float_ds
            j0 += dj

    # Otherwise, insert using vertical wrapping
    else:
        di = (wrapped_size[0] + gap_size) // sections
        dj = wrapped_size[1]

        ds = di - gap_size

        float_l0 = 0.5
        float_dl = (image.size[1] - wrapped_size[1]) / (sections - 1.)

        i0 = int((wrapped_size[0] - di * sections - gap_size)/2. + 0.5)
        for k in range(sections):
            l0 = int(float_l0)
            l1 = l0 + dj
            i1 = i0 + ds

            buffer[:,i0:i1] = array[l0:l1,:]

            float_l0 += float_dl
            i0 += di

    # Convert the new buffer back to a PIL image
    return array_to_pil(buffer, two_bytes, rescale=False)

################################################################################
# Wrap a PIL image
################################################################################

def pad_image(image, frame, pad_color):
    """Pads a PIL image to fill a specified frame size.

    Input:
        image           a PIL image.
        pad_color       color to use in the gap, specified as an X11 name or an
                        (R,G,B) triple.

    Return:             a new PIL image of the requested size.
    """

    # Make sure padding is needed
    if frame is None:
        return image

    if image.width >= frame[0] and image.height >= frame[1]:
        return image

    # Get the pad color
    if isinstance(pad_color, str):
        pad_color = list(ColorNames.lookup(pad_color))

    # Get the image array
    array = pil_to_array(image, rescale=False)
    array = np.atleast_3d(array)
    two_bytes = (array.dtype.itemsize == 2)

    # Create an empty buffer (and convert to RGB if necessary)
    width  = max(image.width,  frame[0])
    height = max(image.height, frame[1])

    if array.shape[2] == 1 and \
       (pad_color[0] != pad_color[1] or pad_color[0] != pad_color[2]):
        buffer = np.empty((height, width, 1), dtype=array.dtype)
    else:
        buffer = np.empty((height, width, array.shape[2]), dtype=array.dtype)

    # Match the gap color to the byte size
    if two_bytes:
        pad_color[0] = int(pad_color[0]/255. * 65535.9999)
        pad_color[1] = int(pad_color[1]/255. * 65535.9999)
        pad_color[2] = int(pad_color[2]/255. * 65535.9999)

    # Pre-fill the buffer with the gap color
    if buffer.shape[2] == 1:
        buffer[:,:,0] = pad_color[0]
    else:
        buffer[:,:,0] = pad_color[0]
        buffer[:,:,1] = pad_color[1]
        buffer[:,:,2] = pad_color[2]

    # Insert the image
    l0 = (height - image.height) // 2
    s0 = (width  - image.width ) // 2

    l1 = l0 + image.height
    s1 = s0 + image.width

    buffer[l0:l1,s0:s1] = array[:,:]

    # Convert the new buffer back to a PIL image
    return array_to_pil(buffer, two_bytes, rescale=False)

################################################################################
# Write a PIL image (or list of RGB images) to a file. It recognizes the case of
# 32-bit integers and writes them as 16-bit TIFFs.
################################################################################

def write_pil(image, outfile, quality=75):
    """Writes a PIL image (or list of RGB images) to a file.

    Input:
        image           a PIL image or a list of three images.
        outfile         the output file to write.
        quality         quality factor 0-100 to use for jpeg output.
    """

    # Create the parent directory if necessary
    parent = os.path.split(outfile)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)

    # If it's a list, write a RGB 16-bit Tiff
    if isinstance(image, (list,tuple)):

        # Convert images back to a numpy arrays
        newarrays = []
        for c in range(3):
            newarrays.append(np.array(image[c].getdata(), dtype="int32"))

        array = np.dstack((newarrays[0], newarrays[1], newarrays[2]))

        # Reshape, clip and convert back to two bytes
        array = array.reshape((image[c].size[1], image[c].size[0], 3))
        array = array.clip(0,65535).astype("uint16")

        # Write file
        WriteTiff16(outfile, array)

    # If it's a single 32-bit image, write a grayscale Tiff
    elif image.mode == "I":
        array = np.array(image.getdata(), dtype="int32")
        array = array.reshape((image.size[1], image.size[0], 1))
        array = array.clip(0,65535).astype("uint16")

        # Write file
        WriteTiff16(outfile, array)

    # Otherwise use the standard PIL output mechanism
    else:
        image.save(outfile, quality=quality)

################################################################################
# Read a PIL image.
################################################################################

def read_pil(infile):
    """Reads a PIL image (or list of RGB images) from a file.

    Input:
        infile          the input file to read.

    Return:
        image           a PIL image or a list of three images.
    """

    # Check for 16-bit TIFF
    testfile = infile.upper()
    if testfile.endswith(".TIFF") or testfile.endswith(".TIF"):
        try:
            (array, palette) = ReadTiff16(infile)
        except IOError:
            array = None
            palette = None

        if array is not None:
            if palette is not None:
                return IOError("16-bit palette option is not supported")

            return array_to_pil(array, twobytes=True, rescale=False)

    # Otherwise just use PIL method
    im = Image.open(infile)
    im.load()
    return im

################################################################################
# Read a PIL image and convert to an array.
################################################################################

def read_array(infile, rescale):
    """Reads a numpy array from a file.

    Input:
        infile          the input file to read.
        rescale         True to scale the values to the range (0-1).

    Return:
        array           a numpy 2-D or 3-D array.
    """

    # Check for 16-bit TIFF
    array = None
    testfile = infile.upper()
    if testfile.endswith(".TIFF") or testfile.endswith(".TIF"):
        try:
            (array, palette) = ReadTiff16(infile)
        except IOError:
            array = None
            palette = None

    if array is not None:
        if palette is not None:
            return IOError("16-bit palette option is not supported")

        if rescale:
            array = array.astype("float") / 65535.

        return array

    # Read PIL file
    return pil_to_array(Image.open(infile), rescale)

################################################################################
# Construct the output file name
################################################################################

def get_outfile(infile, outdir=None, strip=[], suffix="", extension="jpg",
                replace='all'):
    """Derive the name of the output file.
    
    Input:
        infile          name of the input file.
        outdir          name of the output directory if different from that of
                        the input directory; None otherwise.
        strips          an optional string or list of strings to strip from the
                        input file name before adding the suffix.
        suffix          an optional string of characters to add to the end of
                        the file name, before the extension.
        extension       the extension for the output file, which must be one of
                        the PIL supported types such as jpg, jpeg, gif, tif, or
                        tiff. Lower and uppercase extensions are acceptable.
        replace         what to do when a file already exists:
                        "all" (the default) to replace the file silently;
                        "none" to skip the file silently;
                        "warn" to issue a warning and skip the file;
                        "error" to raise an error condition.

    Return:             the name of the output file.

    Side effects:       if the directory tree for the output file does not
                        already exist, it is created (recursively).
    """

    if suffix is None:
        suffix = ''
    if strip is None:
        strip = ['']

    outfile = infile

    # Strip substrings
    if isinstance(strip, str):
        strip = [strip]
    for substring in strip:
        loc = outfile.rfind(substring)
        if loc >= 0:
            outfile = outfile[:loc] + outfile[loc + len(substring):]

    # Insert the output directory
    if outdir is not None:
        outfile = os.path.join(outdir, os.path.split(outfile)[1])

    # Insert the suffix and extension
    outfile = os.path.splitext(outfile)[0]
    outfile += suffix + "." + extension

    # Create the directory tree if necessary
    path = os.path.split(outfile)[0]
    if path != "" and not os.path.exists(path):
        os.makedirs(path)

    # Raise an error if the file already exists
    if os.path.exists(outfile):
        if replace == 'none':
            return ''
        elif replace == 'error':
            raise IOError("File already exists: " + outfile)
        elif replace == 'warn':
            warnings.warn("File overwritten: " + outfile)

    return outfile

################################################################################
# Execute the main command-line progam if this package is not imported
################################################################################

if __name__ == "__main__": main()

