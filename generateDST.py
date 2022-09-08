# -*- coding: utf-8 -*-
import pyembroidery
#from generateDST_utils import *
from generateDST_utils import (extract_paths_from_svg, stitch_path,
    get_ignore_thread_indices, get_conduct_thread_indices,
    viz_dst_sim, viz_dst)
import argparse
import time
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the input SVG file.
# design_dir = '.'
design_dir = os.path.join(script_dir, 'SVG')

svg_filename = '16x16_test_v2-superpath.svg'
# svg_filename = 'Asset 1finger.svg'
# svg_filename = 'embroidery_sensor_matrix.svg'
# svg_filename = 'test_pattern_1path.svg'
# svg_filename = 'test_pattern_2paths.svg'
# svg_filename = 'test_pattern_2paths_skewed.svg'
# svg_filename = 'test_pattern_3paths.svg'
# svg_filename = 'test_pattern_allPaths.svg'

svg_filepath = os.path.realpath(os.path.join(design_dir, svg_filename))

# Specify where to save the output DST file.
output_dir = os.path.realpath(os.path.join(script_dir, 'DST'))
os.makedirs(output_dir, exist_ok=True)
dst_filename = svg_filename.replace('.svg', '.dst')


def main(args):
    """Script entry point"""

    dst_filepath = os.path.join(args.output_dir, args.output_filename)

    # Read control points from the SVG file.
    print('Extracting paths from %s' % (args.input_filepath))
    start_time_s = time.time()
    x_all, y_all, rgb_all = extract_paths_from_svg(args.input_filepath, args.scale,
                                                   viz=args.viz_svg, target_units=args.target_units,
                                                   remove_duplicates=True)
    num_paths = len(x_all)
    print('Extracted paths in %0.2fs\n' % (time.time() - start_time_s))

    # Start an empty embroidery pattern.
    # x_pos_all and y_pos_all will represent the points that are added to the pattern.
    pattern = pyembroidery.EmbPattern()
    pattern.metadata('name', os.path.splitext(os.path.basename(args.input_filepath))[0])
    x_stitch_all = [None]*num_paths
    y_stitch_all = [None]*num_paths

    # Get ignorance thread indices
    ignore_thread_indices = get_ignore_thread_indices(rgb_all, args.path_color_to_not_stitch)

    # Get conductive thread indices
    conduct_thread_indices = get_conduct_thread_indices(rgb_all, args.conduct_thread_color)
    print('Paths: {} with color: {} are considered to be conductive threads.'.format(conduct_thread_indices, args.conduct_thread_color))

    # Add points to represent each path in the SVG file.
    num_paths_stitched = 0
    for path_index in range(num_paths):
        # if args.path_color_to_not_stitch is not None and (list(args.path_color_to_not_stitch) == list(rgb_all[path_index])):
        if args.path_color_to_not_stitch is not None and path_index in ignore_thread_indices:
            print('NOT stitching path %d/%d since its color is %s\n' % (
                path_index+1, num_paths, args.path_color_to_not_stitch))
            continue
        else:
            print('Stitching path %d/%d' % (path_index+1, num_paths))

        start_time_s = time.time()
        # Switch to a new thread for each new path.
        if num_paths_stitched > 0:
            pattern.color_change()

        # Add stitch points for this path.
        xs, ys = stitch_path(pattern, x_all, y_all,
                           path_index=path_index,
                           pitch=args.pitch,
                           conduct_thread_indices=conduct_thread_indices,
                           min_num_stitches_per_segment=args.min_interSegment_stitches)
        x_stitch_all[path_index] = xs
        y_stitch_all[path_index] = ys
        num_paths_stitched += 1
        print('Stitched path %d in %0.2fs\n' % (path_index+1, time.time() - start_time_s))

    # Write the path to a DST file.
    print('Writing the stitch pattern to %s' % dst_filepath)
    start_time_s = time.time()
    pyembroidery.write_dst(pattern, dst_filepath)
    print('Wrote the DST file in %0.2fs' % (time.time() - start_time_s))

    # Visualize the stitch pattern if desired.
    plot_info = {
       'title': args.input_filepath,
       'target_units': args.target_units,
       'scale': args.scale
    }
    if args.viz_dst:
        # Step through the stitches to more easily visualize the order if desired.
        if args.viz_dst_sim:
            viz_dst_sim(x_all, y_all, rgb_all, x_stitch_all, y_stitch_all, **plot_info)

        # Plot the design, with a single color per path.
        viz_dst(x_all, y_all, rgb_all, x_stitch_all, y_stitch_all, **plot_info)


def str2list(in_str):
    """Parse comma seperated color strings to a list.
    e.g. '#00FF00,#0000FF' -> ['#00FF00', '#0000FF']
         '#00FF00, #0000FF' -> ['#00FF00', '#0000FF']
         '#00FF00' -> ['#00FF00']
    """
    list1 = in_str.split(',')
    ret = [e.strip() for e in list1]
    return ret


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='Generate a .dst file from a .svg file')

    # Parse command line arguments.
    parser = argparse.ArgumentParser()

    # Input and output filepaths.
    parser.add_argument('--input_filepath', type=str, default=svg_filepath, help='input file path')
    parser.add_argument('--output_dir', type=str, default=output_dir, help='output directory')
    parser.add_argument('--output_filename', type=str, default=dst_filename, help='output file name')

    # Whether to interpret/scale SVG points to desired physical units.
    parser.add_argument('--target_units', type=str, default='mm', help='target SVG units') # None to not interpret units

    # Whether to scale the design after the units are interpreted.
    #  NOTE: the embroidery machine's units are 0.1 mm, so a scale factor of 10 is useful.
    parser.add_argument('--scale', type=float, default=10, help='design scale')

    # The target spacing between auto-placed stitches.
    #  This is in the target units specified by target_units, *after* the specified scale factor is applied.
    parser.add_argument('--pitch', type=int, default=20, help='pitch')

    # The minimum number of stitches that should be placed between path intersections.
    parser.add_argument('--min_interSegment_stitches', type=int, default=1, help='min stitches between intersections')

    # Specify a line color to not stitch if desired.
    #  Those paths will still be used for computing intersections with other paths for stitch placement purposes.
    #  Can be a three-element RGB list (scaled out of 255) or None.
    parser.add_argument('--path_color_to_not_stitch', type=str2list, default=None, help='Path color to be ignored. (Usage: --path_color_to_not_stitch "#00FF00,#0000FF")') # A 3-element RGB list, or None to not ignore any paths

    # Specify conductive thread color
    parser.add_argument('--conduct_thread_color', type=str2list, default=['#00FF00', '#0000FF'], help='Conductive thread color. (Usage: --conduct_thread_color "#00FF00,#0000FF")')

    # Visualization.
    parser.add_argument('--viz_svg', type=bool, default=False, help='Visualize input .svg file.')
    parser.add_argument('--viz_dst', type=bool, default=True, help='Visualize resulting .dst file.')
    parser.add_argument('--viz_dst_sim', type=bool, default=False, help='Visualize resulting .dst file together with animated stitching order.')

    return parser.parse_args()


if __name__=='__main__':
    args = parse_args()
    main(args)