
import pyembroidery
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
# Specify a line color to not stitch if desired.
#   Those paths will still be used for computing intersections with other paths for stitch placement purposes.
parser.add_argument('--path_color_to_not_stitch', type=list, default=None, help='path-color-to-ignore') # A 3-element RGB list, or None to not ignore any paths

args = parser.parse_args()
dst_filepath = os.path.join(args.output_dir, args.output_filename)

# Read control points from the SVG file.
print ('Extracting control points from %s' % (args.input_path))
start_time_s = time.time()
x_all, y_all, rgb_all = extract_paths_from_svg(args.input_path, args.scale,
                                               viz=args.viz_svg, target_units='mm',
                                               remove_duplicates=True)
num_paths = len(x_all)
print('Extracted control points in %0.2fs' % (time.time() - start_time_s))
print()

# Start an embroidery pattern.
# x_pos_all and y_pos_all will represent the points that are added to the pattern.
pattern = pyembroidery.EmbPattern()
pattern.metadata('name', os.path.splitext(os.path.basename(args.input_path))[0])
x_stitch_all = [None]*num_paths
y_stitch_all = [None]*num_paths

# Add points to represent each path in the SVG file.
for path_index in range(num_paths):
    if args.path_color_to_not_stitch is not None and (list(args.path_color_to_not_stitch) == list(rgb_all[path_index])):
        print('NOT stitching path %d/%d since its color is %s' % (path_index+1, num_paths, args.path_color_to_not_stitch))
        print()
        continue
    else:
        print('Stitching path %d/%d' % (path_index+1, num_paths))
    start_time_s = time.time()
    # Switch to a new thread for each new path.
    if path_index > 0:
        pattern.color_change()
    # Add stitch points for this path.
    x, y = stitch_path(pattern, x_all, y_all,
                       path_index=path_index, pitch=args.pitch)
    x_stitch_all[path_index] = x
    y_stitch_all[path_index] = y
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
            plt.plot(x_stitch_all[path_index][0], y_stitch_all[path_index][0], 'kD')
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
            plt.plot(x_stitch_all[path_index][0], y_stitch_all[path_index][0], 'kD')
    # Show the real aspect ratio of the design.
    plt.gca().set_aspect('equal')
    # Show the plot and wait for the user to close the window.
    plt.show()



