from generateDST_utils import *
import argparse
import time
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the input SVG file.
# design_dir = '.'
design_dir = os.path.join(script_dir, 'SVG')

# svg_filename = 'embroidery_sensor_matrix.svg'
# svg_filename = 'test_pattern_1path.svg'
# svg_filename = 'test_pattern_2paths.svg'
# svg_filename = 'test_pattern_2paths_skewed.svg'
# svg_filename = 'test_pattern_3paths.svg'
svg_filename = 'test_pattern_allPaths.svg'

svg_filepath = os.path.realpath(os.path.join(design_dir, svg_filename))

# Specify where to save the output DST file.
output_dir = os.path.realpath(os.path.join(script_dir, 'DST'))
os.makedirs(output_dir, exist_ok=True)
dst_filename = svg_filename.replace('.svg', '.dst')

# Parse command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default=svg_filepath, help='input file path')
parser.add_argument('--output_dir', type=str, default=output_dir, help='output directory')
parser.add_argument('--output_filename', type=str, default=dst_filename, help='output file name')
parser.add_argument('--pitch', type=int, default=30, help='pitch')
parser.add_argument('--viz_svg', type=bool, default=False, help='viz')
parser.add_argument('--viz_dst', type=bool, default=True, help='viz')
parser.add_argument('--viz_dst_sim', type=bool, default=False, help='viz')
# NOTE: the embroidery machine's units are 0.1 mm, so a scale factor of 10 is useful.
parser.add_argument('--scale', type=float, default=10, help='design scale')
args = parser.parse_args()
dst_filepath = os.path.join(args.output_dir, args.output_filename)

# Read control points from the SVG file.
print ('Extracting control points from %s' % (args.input_path))
start_time_s = time.time()
x_all, y_all = extract_pt_from_svg(args.input_path, args.scale,
                                   viz=args.viz_svg, target_units='mm',
                                   remove_duplicates=True)
num_paths = len(x_all)
print('Extracted control points in %0.2fs' % (time.time() - start_time_s))
print()

# Start an embroidery pattern.
# x_pos_all and y_pos_all will represent the points that are added to the pattern.
pattern = pyembroidery.EmbPattern()
x_stitch_all = [[] for p in range(num_paths)]
y_stitch_all = [[] for p in range(num_paths)]

# Add points to represent each path in the SVG file.
for path_index in range(num_paths):
    print ('Stitching path %d/%d' % (path_index+1, num_paths))
    start_time_s = time.time()
    # Switch to a new thread for each new path.
    if path_index > 0:
        pattern.color_change()
    # Add stitch points for this path.
    x, y = stitch_path(pattern, x_all, y_all,
                       path_index=path_index, pitch=args.pitch)
    x_stitch_all[path_index] += x
    y_stitch_all[path_index] += y
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
            sim_handles = []
            # Plot the path without markers.
            sim_handles.append(plt.plot(x_stitch_all[path_index], y_stitch_all[path_index], '-'))
            # Show the real aspect ratio of the design.
            plt.gca().set_aspect('equal')
            # Show markers in stitch order.
            for i in range(len(x_stitch_all[path_index])):
                sim_handles.append(plt.plot(x_stitch_all[path_index][i],
                                            y_stitch_all[path_index][i], '.'))
                # Show the plot and wait for a specified timeout (or for the user to click the window).
                plt.waitforbuttonpress(0.01)
            # Remove the simulated stitches.
            for sim_handle in sim_handles:
                for h in sim_handle:
                    h.remove()
            # Plot the final design with stitch markers, all in a single color.
            plt.plot(x_stitch_all[path_index], y_stitch_all[path_index], '.-')
            # Indicate the starting stitch.
            plt.plot(x_stitch_all[path_index][0], y_stitch_all[path_index][0], 'k.')
    # Plot the design, with a single color per path.
    plt.clf()
    for path_index in range(num_paths):
        # Plot the final design with stitch markers, all in a single color.
        plt.plot(x_stitch_all[path_index], y_stitch_all[path_index], '.-')
        # Indicate the starting stitch.
        plt.plot(x_stitch_all[path_index][0], y_stitch_all[path_index][0], 'k.')
    # Show the real aspect ratio of the design.
    plt.gca().set_aspect('equal')
    # Show the plot and wait for the user to close the window.
    plt.show()



