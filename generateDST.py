
import pyembroidery
from generateDST_utils import *
import argparse
import time
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the input SVG file.
# design_dir = '.'
design_dir = os.path.join(script_dir, 'SVG')

svg_filename = 'Manus_Glove_V4_fingers.svg'
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
parser.add_argument('--path_color_to_not_stitch', type=list, default=None, help='path-color-to-ignore') # A 3-element RGB list, or None to not ignore any paths
# Visualization.
parser.add_argument('--viz_svg', type=bool, default=False, help='viz')
parser.add_argument('--viz_dst', type=bool, default=True, help='viz')
parser.add_argument('--viz_dst_sim', type=bool, default=False, help='viz')

args = parser.parse_args()
dst_filepath = os.path.join(args.output_dir, args.output_filename)

# Read control points from the SVG file.
print ('Extracting paths from %s' % (args.input_filepath))
start_time_s = time.time()
x_all, y_all, rgb_all = extract_paths_from_svg(args.input_filepath, args.scale,
                                               viz=args.viz_svg, target_units=args.target_units,
                                               remove_duplicates=True)
num_paths = len(x_all)
print('Extracted paths in %0.2fs' % (time.time() - start_time_s))
print()

# Start an embroidery pattern.
# x_pos_all and y_pos_all will represent the points that are added to the pattern.
pattern = pyembroidery.EmbPattern()
pattern.metadata('name', os.path.splitext(os.path.basename(args.input_filepath))[0])
x_stitch_all = [None]*num_paths
y_stitch_all = [None]*num_paths

# Add points to represent each path in the SVG file.
num_paths_stitched = 0
for path_index in range(num_paths):
    if args.path_color_to_not_stitch is not None and (list(args.path_color_to_not_stitch) == list(rgb_all[path_index])):
        print('NOT stitching path %d/%d since its color is %s' % (path_index+1, num_paths, args.path_color_to_not_stitch))
        print()
        continue
    else:
        print('Stitching path %d/%d' % (path_index+1, num_paths))
    start_time_s = time.time()
    # Switch to a new thread for each new path.
    if num_paths_stitched > 0:
        pattern.color_change()
    # Add stitch points for this path.
    x, y = stitch_path(pattern, x_all, y_all,
                       path_index=path_index,
                       pitch=args.pitch, min_num_stitches_per_segment=args.min_interSegment_stitches)
    x_stitch_all[path_index] = x
    y_stitch_all[path_index] = y
    num_paths_stitched += 1
    print('Stitched path %d in %0.2fs' % (path_index+1, time.time() - start_time_s))
    print()

# Write the path to a DST file.
print('Writing the stitch pattern to %s' % dst_filepath)
start_time_s = time.time()
pyembroidery.write_dst(pattern, dst_filepath)
print('Wrote the DST file in %0.2fs' % (time.time() - start_time_s))

# Visualize the stitch pattern if desired.
if args.viz_dst:
    # Step through the stitches to more easily visualize the order if desired.
    if args.viz_dst_sim:
        for path_index in range(num_paths):
            # If the path was not stitched, just show the original path in gray.
            if x_stitch_all[path_index] is None:
                plt.plot(x_all[path_index], y_all[path_index], '.-', color=np.array([1,1,1])*0.8)
                continue
            # Otherwise, simulate the stitching then show the final path.
            sim_handles = []
            path_color = np.array(rgb_all[path_index])/255 if rgb_all[path_index] is not None else None
            # Plot the path without markers.
            sim_handles.append(plt.plot(x_stitch_all[path_index], y_stitch_all[path_index], '-', color=path_color))
            # Show the real aspect ratio of the design.
            plt.gca().set_aspect('equal')
            # Show markers in stitch order.
            for i in range(len(x_stitch_all[path_index])):
                sim_handles.append(plt.plot(x_stitch_all[path_index][i],
                                            y_stitch_all[path_index][i], '.', color=path_color))
                # Show the plot and wait for a specified timeout (or for the user to click the window).
                plt.waitforbuttonpress(0.02)
                plt.draw()
            # Remove the simulated stitches.
            for sim_handle in sim_handles:
                for h in sim_handle:
                    h.remove()
            # Plot the final design with stitch markers, all in a single color.
            plt.plot(x_stitch_all[path_index], y_stitch_all[path_index], '.-', color=path_color)
            # Indicate the starting stitch.
            plt.plot(x_stitch_all[path_index][0], y_stitch_all[path_index][0], 'D', color=path_color)
            # Formatting.
            plt.title(args.input_filepath)
            plt.xlabel('X [%s*%s]' % (args.target_units, args.scale))
            plt.ylabel('Y [%s*%s]' % (args.target_units, args.scale))
            # Update the plot.
            plt.draw()
    # Plot the design, with a single color per path.
    plt.clf()
    for path_index in range(num_paths):
        # If the path was not stitched, just show the original path in gray.
        if x_stitch_all[path_index] is None:
            plt.plot(x_all[path_index], y_all[path_index], '.-', color=np.array([1,1,1])*0.8)
        # Plot the final design with stitch markers, all in a single color.
        else:
            path_color = np.array(rgb_all[path_index])/255 if rgb_all[path_index] is not None else None
            plt.plot(x_stitch_all[path_index], y_stitch_all[path_index], '.-', color=path_color)
            # Indicate the starting stitch.
            plt.plot(x_stitch_all[path_index][0], y_stitch_all[path_index][0], 'D', color=path_color)
    # Show the real aspect ratio of the design.
    plt.gca().set_aspect('equal')
    # Formatting.
    plt.title(args.input_filepath)
    plt.xlabel('X [%s*%s]' % (args.target_units, args.scale))
    plt.ylabel('Y [%s*%s]' % (args.target_units, args.scale))
    # Show the plot and wait for the user to close the window.
    plt.show()



