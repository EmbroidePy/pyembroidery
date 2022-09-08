import pyembroidery
import numpy as np
import matplotlib.pyplot as plt
#from svgelements import * # will use this package to extract path points and colors
from svgelements import (SVG, Line, Polyline, Group, Path)
import svgpathtools       # will use this package to determine SVG width/height for path scaling
from scipy import spatial
import math
import cv2
import re
from PIL import ImageColor


def viz_dst_sim(x_all, y_all, rgb_all, x_stitch_all, y_stitch_all, plt_title, target_units, scale):
    """Visualize resulting .dst file together with animated stitching order.

    :param x_all: A list contains 2~3 sublists, each sublist contains X coordinates of all stitch points of a single superpath.
    :type x_all: list[list[float]]

    :param y_all: A list contains 2~3 sublists, each sublist contains Y coordinates of all stitch points of a single superpath.
    :type y_all: list[list[float]]

    :param rgb_all: Colors of superpaths.
    :type rgb_all: list[list[int]]
    
    :param x_stitch_all: X coordinates of stitch plans for all superpaths
    :type x_stitch_all: list[list[float]]
    
    :param y_stitch_all: Y coordinates of stitch plans for all superpaths
    :type y_stitch_all: list[list[float]]
    
    :param title: Plot title, only used for displaying.
    :type title: str
    
    :param target_units: Target unit, only used for displaying.
    :type target_units: str
    
    :param scale: Scale factor, only used for displaying.
    :type scale: str
    """
    num_paths = len(x_all)

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
        num_stitch = len(x_stitch_all[path_index])
        for i in range(num_stitch):
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
        plt.title(title)
        plt.xlabel('X [%s*%s]' % (target_units, scale))
        plt.ylabel('Y [%s*%s]' % (target_units, scale))

        # Update the plot.
        plt.draw()


def viz_dst(x_all, y_all, rgb_all, x_stitch_all, y_stitch_all, title, target_units, scale):
    """Visualize resulting .dst file.

    :param x_all: A list contains 2~3 sublists, each sublist contains X coordinates of all stitch points of a single superpath.
    :type x_all: list[list[float]]

    :param y_all: A list contains 2~3 sublists, each sublist contains Y coordinates of all stitch points of a single superpath.
    :type y_all: list[list[float]]

    :param rgb_all: Colors of superpaths.
    :type rgb_all: list[list[int]]

    :param x_stitch_all: X coordinates of stitch plans for all superpaths
    :type x_stitch_all: list[list[float]]

    :param y_stitch_all: Y coordinates of stitch plans for all superpaths
    :type y_stitch_all: list[list[float]]
    
    :param title: Plot title, only used for displaying.
    :type title: str
    
    :param target_units: Target unit, only used for displaying.
    :type target_units: str
    
    :param scale: Scale factor, only used for displaying.
    :type scale: str
    """
    plt.clf()  # clear
    num_paths = len(x_all)

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
    plt.title(title)
    plt.xlabel('X [%s*%s]' % (target_units, scale))
    plt.ylabel('Y [%s*%s]' % (target_units, scale))

    # Show the plot and wait for the user to close the window.
    plt.show()


def get_segments_intersection(endpoints_1, endpoints_2, return_scenario_info=False, debug=False):
    """Compute the intersection between two line segments.
    The code is based on https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect

    :param endpoints_1: 2x2 numpy arrays of the form [[x1, y1], [x2, y2]].
    :type endpoints_1: NDArray[(2, 2), float]

    :param endpoints_2: 2x2 numpy arrays of the form [[x1, y1], [x2, y2]].
    :type endpoints_2: NDArray[(2, 2), float]

    :param return_scenario_info: Display scenario information. The scenario_info is a `dict` object with `str` type key indicating scenario and `bool` type value indicating whether the scenario happened.
    :type return_scenario_info: bool, optional

    :param debug: Verbose mode. (Default: False)
    :type debug: bool, optional

    :return: The intersection point as a 2-element numpy array.
        If the two segments are colinear and overlapping, will return the midpoint of the intersection area.
        Returns None if the segments do not overlap.
        If return_scenario_info is True, returns a tuple (intersection_point, info) where info is a dict with keys 'parallel' and 'colinear'
    :rtype: NDArray[(2,), float] or None or tuple[DArray[(2,), float], dict]
    """
    if isinstance(endpoints_1, (list, tuple)):
        endpoints_1 = np.array(endpoints_1)
    if isinstance(endpoints_2, (list, tuple)):
        endpoints_2 = np.array(endpoints_2)

    p = endpoints_1[0,:]
    r = endpoints_1[1,:] - endpoints_1[0,:]
    q = endpoints_2[0,:]
    s = endpoints_2[1,:] - endpoints_2[0,:]

    if debug:
        print('p', p, 'r', r)
        print('q', q, 's', s)
    
    scenario_info = {
        'colinear': False,
        'parallel': False
    }

    if np.cross(r, s) == 0 and np.cross((q - p), r) == 0:
        scenario_info['colinear'] = True
        # The segments are colinear, so check if they are overlapping or disjoint.
        # Frist, represent each endpoint in terms of the other segment's reference frame.
        q_in_pFrame_0 = np.dot((q - p), r)/np.dot(r, r)
        q_in_pFrame_1 = np.dot((q + s - p), r)/np.dot(r, r)
        p_in_qFrame_0 = np.dot((p - q), s)/np.dot(s, s)
        p_in_qFrame_1 = np.dot((p + r - q), s)/np.dot(s, s)

        # Take the ones that are on the other segment (the ratio along the segment is in [0,1]).
        intersection_points = []
        if q_in_pFrame_0 >= 0 and q_in_pFrame_0 <= 1:
            intersection_points.append(p + r*q_in_pFrame_0)
        if q_in_pFrame_1 >= 0 and q_in_pFrame_1 <= 1:
            intersection_points.append(p + r*q_in_pFrame_1)
        if p_in_qFrame_0 >= 0 and p_in_qFrame_0 <= 1:
            intersection_points.append(q + s*p_in_qFrame_0)
        if p_in_qFrame_1 >= 0 and p_in_qFrame_1 <= 1:
            intersection_points.append(q + s*p_in_qFrame_1)

        # There should be 2 endpoints that are on the other segment if the segments overlap, and 0 otherwise.
        if len(intersection_points) == 0:
            intersection_point = None
        else:
            # Use the midpoint between the two intersecting endpoints.
            intersection_points = np.array(intersection_points)
            intersection_point = np.mean(intersection_points, axis=0)

    elif np.cross(r, s) == 0 and np.cross((q-p), r) != 0:
        # The lines are parallel and non-intersecting.
        scenario_info['parallel'] = True
        intersection_point = None
    else:
        t = np.cross((q - p), s) / np.cross(r, s)
        u = np.cross((q - p), r) / np.cross(r, s)
        if np.cross(r, s) != 0 and t >= 0 and t <= 1 and u >= 0 and u <= 1:
            # There was an intersection.
            intersection_point = p + t*r
        else:
            # The segments do not intersect (and they are not parallel).
            intersection_point = None
    
    # Print/plot debugging information if desired.
    if debug:
        print('scenario_info:', scenario_info)
        print('intersection_point:', intersection_point)
        
        import matplotlib.pyplot as plt
        plt.clf()
        plt.plot(endpoints_1[:,0], endpoints_1[:,1], '.-')
        plt.plot(endpoints_2[:,0], endpoints_2[:,1], '.-')
        if intersection_point is not None:
            plt.plot(intersection_point[0], intersection_point[1], '.', markersize=25)
        plt.grid(True, color='lightgray')
        plt.waitforbuttonpress(0)
    
    # All done!
    if return_scenario_info:
        return (intersection_point, scenario_info)
    else:
        return intersection_point


def _parse_svg_size_string(size_str, target_units='mm'):
    """Parse a size string such as "10mm" into its value, and convert it to the target units.
        Adapted from https://github.com/SebKuzminsky/svg2gcode/blob/94f28c1877c721c66cd90a38750f78d8031ac85a/gcoder.py#L238

    :param size_str: Size string, a string contains a number and unit of measurement. e.g. '10mm'
    :type size_str: str

    :param target_units: Target units. (Default: 'mm')
    :type target_units: str, optional

    :return: Converted value in target units.
    :rtype: float
    """
    # Get the original value and units.
    m = re.match('^([0-9.]+)([a-zA-Z]*)$', size_str)
    if m == None or len(m.groups()) != 2:
        print("failed to parse SVG viewport height/width: %s" % size_str)
        return None
    val = float(m.group(1))
    units = m.group(2)
    
    # Get a scale factor that converts to mm.
    # (use mm as an intermediate since the below dict was conveniently defined by the code at the above link)
    scales_to_get_mm = {
        # "px" (or "no units") is 96 dpi: 1 inch/96 px * 25.4 mm/1 inch = 25.4/96 mm/px
        '': 25.4/96,
        'px': 25.4/96,
        
        # "pt" is 72 dpi: 1 inch/72 pt * 25.4 mm/1 inch = 25.4/72 mm/pt
        'pt': 25.4/72,
        
        # Units are Picas "pc", 6 dpi: 1 inch/6 pc * 25.4 mm/1 inch = 25.4/6 mm/pc
        'pc': 25.4/6,
        
        'cm': 10.0,
        'mm': 1.0,
        
        # Units are inches: 25.4 mm/1 inch
        'in': 25.4
    }
    scale_to_get_mm = scales_to_get_mm[units]
    
    # Convert to target units.
    if target_units.lower() in ['mm', 'millimeter', 'millimeters']:
        scale = scale_to_get_mm
    elif target_units.lower() in ['cm', 'centimeter', 'centimeters']:
        scale = scale_to_get_mm / 10.0
    elif target_units.lower() in ['in', 'inch', 'inches']:
        scale = scale_to_get_mm / 25.4
    else:
        raise ValueError('Units of %s are not yet supported' % target_units)
    
    return val*scale


def path2polyline(path):
    """Convert data structure of a superpath described in `Path` to `polyline`.
    CAUTION: The input superpath is assume to be only composed of `Lines` and `Move`, curves are not applicable.

    :param path: A superpath to be converted.
    :type path: `svgelements.Path`
    
    :return: A returning `Polyline` object wrapped with a list.
    :rtype: `svgelements.Polyline`
    """
    if not isinstance(path, Path):
        print('Not a path object.')
        return

    # Stacks stitch point coordinates into a list
    values = []
    for element in path:
        if isinstance(element, Line):
            t = [element.start.x, element.start.y, element.end.x, element.end.y]
            values.extend(t)

    return [Polyline(*values, stroke=path.stroke, fill=path.fill)]


def extract_paths_from_groups(element):
    """Extract paths from groups.

    :param element: A single element of SVG file.
    :type element: `svgelements.Polyline` or `svgelements.Group` or `svgelements.Path`
    
    :return: Returns `Polyline` object wrapped with a list.
        Returns empty list if the element is not recognized.
    :rtype: list[`svgelements.Polyline`] or list[]
    """
    if isinstance(element, Polyline):
        return [element]
    elif isinstance(element, Group):
        paths = []
        for subgroup in element:
            paths.extend(extract_paths_from_groups(subgroup))
        return paths
    elif isinstance(element, Path):
        paths = []
        for subgroup in element:
            paths.extend(path2polyline(element))
            return paths
    else:
        return []


def color_integer_encode(rgb_int):
    """Encode into color integer a list representing RGB values.
    e.g. For green, 65280 -> [0,255,0]
         For red, 16711680 -> [255,0,0]

    :param rgb_int: RGB integer.
    :type rgb_int: int
    
    :return: A list of integers representing RGB values. It must be a sequence of size 3.
    :rtype: Annotated[list[int], 3]
    """
    return [(rgb_int >> 16) & 255,
            (rgb_int >> 8) & 255,
            rgb_int & 255]


def scale_point_arrays(point_arrays, name, scale_factor=None):
    """Define a helper to scale all arrays of points.
    For example, point_arrays can be x_all or y_all.
    Can specify a scale factor to use, OR a target range for computing a scale factor.

    :param point_arrays: A list contains 2~3 sublists, each sublist contains X/Y coordinates of all stitch points of a single superpath.
    :type point_arrays: list[list[float]]

    :param name: Name of point array to be scaled, could be 'x' or 'y'.
    :type name: str

    :param scale: Scale factor.
    :type scale: float
    """
    if scale_factor is None:
        print('  Scale factor not specified, point array %s not scaled.' % name)
        return point_arrays
    print('  Scaling %s by a factor of %g' % (name, scale_factor))
    for (i, points) in enumerate(point_arrays):
        point_arrays[i] = [point*scale_factor for point in points]
    return point_arrays


def scale_stitch_plan_auto(x_all, y_all, svg_attributes, target_units):
    """Automatically scale entire stitch plan to fit the size of canvas.

    :param x_all: A list contains 2~3 sublists, each sublist contains X coordinates of all stitch points of a single superpath.
    :type x_all: list[list[float]]

    :param y_all: A list contains 2~3 sublists, each sublist contains Y coordinates of all stitch points of a single superpath.
    :type y_all: list[list[float]]

    :return: Resulting point arrays.
    :rtype: tuple[list[list[float]], list[list[float]]]
    """
    def get_scale_factor(point_arrays, target_range, name):
        """Define a helper to scale all arrays of points.
        For example, point_arrays can be x_all or y_all.
        """
        # Get the min and max of points across all arrays.
        points_min = min([min(points) for points in point_arrays])
        points_max = max([max(points) for points in point_arrays])
        # Compute the scale factor.
        points_range = abs(points_max - points_min)
        scale_factor = target_range / points_range
        print('  Computed scale factor for %s: %g' % (name, scale_factor))
        return scale_factor
    
    # Get the actual size in physical units.
    svg_width = _parse_svg_size_string(svg_attributes['width'], target_units=target_units)
    svg_height = _parse_svg_size_string(svg_attributes['height'], target_units=target_units)
    print(' Scaling SVG to width %f %s and height %f %s' % (svg_width, target_units, svg_height, target_units))

    # Scale so the points match the target range.
    # Use the same scale factor for both X and Y (they're usually very similar but slightly different).
    scale_factor_x = get_scale_factor(x_all, svg_width, 'X')
    scale_factor_y = get_scale_factor(y_all, svg_height, 'Y')
    scale_factor = np.mean([scale_factor_x, scale_factor_y])
    x_all = scale_point_arrays(x_all, name='x', scale_factor=scale_factor)
    y_all = scale_point_arrays(y_all, name='y', scale_factor=scale_factor)
    # plt.figure()
    # plt.plot(x_all[0], y_all[0])
    # plt.show()
    
    return x_all, y_all


def get_coords_from_paths(svg_paths, viz=False):
    """Convert all paths into lists of coordinates.

    :param svg_paths: A list of superpaths extracted from .svg file, they must be `Polyline` object.
    :type svg_paths: list[`svgelements.Polyline`]

    :param viz: Visualize resulting endpoints.
    :type viz: bool

    :return: Resulting point arrays.
    :rtype: tuple[list[list[float]], list[list[float]]]
    """
    x_all = []
    y_all = []
    rgb_all = []
    for (i, path) in enumerate(svg_paths):
        # Ignore empty paths.
        if len(path) <= 1:
            continue
        xs = [point.x for point in path]
        ys = [-point.y for point in path]

        # Get the path color.
        if hasattr(path.stroke, 'rgb'):
            rgb = color_integer_encode(path.stroke.rgb)
        else:
            rgb = None

        # Append the new path.
        x_all.append(xs)
        y_all.append(ys)
        rgb_all.append(rgb)

        # Visualize the control points if desired.
        if viz:
            plt.scatter(xs, ys, s=10, c='red')
            plt.gca().set_aspect('equal')
            plt.show()
    print('colors: ', rgb_all)
    return x_all, y_all, rgb_all


def remove_duplicate_points(x_all, y_all):
    """Remove successive duplicate points.
    
    :param x_all: A list contains 2~3 sublists, each sublist contains X coordinates of all stitch points of a single superpath.
    :type x_all: list[list[float]]
    
    :param y_all: A list contains 2~3 sublists, each sublist contains Y coordinates of all stitch points of a single superpath.
    :type y_all: list[list[float]]
    
    :return: Resulting point arrays.
    :rtype: tuple[list[list[float]], list[list[float]]]
    """
    x_all_unique = []
    y_all_unique = []
    num_paths = len(x_all)
    for path_index in range(num_paths):
        x_all_unique.append([])
        y_all_unique.append([])
        # Add the first point.
        x_all_unique[path_index].append(x_all[path_index][0])
        y_all_unique[path_index].append(y_all[path_index][0])
        # Add points that do not duplicate their previous point.
        for point_index in range(1, len(x_all[path_index])):
            x = x_all[path_index][point_index]
            x_prev = x_all[path_index][point_index - 1]
            y = y_all[path_index][point_index]
            y_prev = y_all[path_index][point_index - 1]
            if not (x == x_prev and y == y_prev):
                x_all_unique[path_index].append(x)
                y_all_unique[path_index].append(y)
    return x_all_unique, y_all_unique


def extract_paths_from_svg(filepath, scale, viz, target_units=None, remove_duplicates=True):
    """Extract points stored in an SVG file.
    
    :param filepath: SVG file path.
    :type filepath: str

    :param scale: A user-specified scale factor to apply to the design after converting to target units.
    :type scale: float

    :param viz: Visualize stitch points by scatter plot.
    :type viz: bool

    :param target_units: If provided, will look for scale informaion in the SVG metadata
        and, if found, will scale the points to be in the target units. (Default: None)
    :type target_units: str, optional

    :param remove_duplicates: Whether to remove successive duplicate points.
        Otherwise, it seems the SVG can have back-to-back duplicates
        (that may or may not start at the first point). (Default: True)
    :type remove_duplicates: bool, optional
    
    :return: (x_all, y_all) where x_all and y_all are lists.
        Each entry represents a path in the SVG, and contains a list of coordinates.
        So point i of path p is at (x_all[p][i], y_all[p][i]).
    :rtype: tuple[list[list[float]], list[list[float]], list[list[int]]]
    """
    print('Parsing the SVG file %s' % filepath)
    # Read paths from the SVG file.
    # Lines may be contained within groups in the SVG,
    #  so will recursively dive through groups to find Polyline instances.
    svg_path_elements = list(SVG.parse(filepath))

    svg_paths = []
    for svg_path_element in svg_path_elements:
        ph = extract_paths_from_groups(svg_path_element)
        svg_paths.extend(ph)

    # Convert the paths into lists of coordinates.
    x_all, y_all, rgb_all = get_coords_from_paths(svg_paths, viz)
    print(' Found %d total paths and %d non-empty paths' % (len(svg_paths), len(x_all)))

    # Scale to specified units if desired.
    if target_units is not None:
        doc = svgpathtools.Document(filepath)
        svg_attributes = doc.root.attrib
        if 'width' not in svg_attributes or 'height' not in svg_attributes:
            print(' Size information was not found in the SVG. Using raw point coordinates.')
        else:
            x_all, y_all = scale_stitch_plan_auto(x_all, y_all, svg_attributes, target_units)

    # Apply any user-specified scaling.
    x_all = scale_point_arrays(x_all, 'x', scale)
    y_all = scale_point_arrays(y_all, 'y', scale)

    # Remove successive duplicate points if desired.
    if remove_duplicates:
        x_all, y_all = remove_duplicate_points(x_all, y_all)

    # Return the control points!
    return x_all, y_all, rgb_all


def get_ignore_thread_indices(rgb_all, ignore_thread_colors):
    """Get ignorance thread indices.
    
    :param rgb_all: Colors of all superpaths.
    :type rgb_all: list[list[int]]

    :param conduct_thread_colors: Conductive thread color.
    :type ignore_thread_colors: list[int, ...]

    :return: Indices of conductive threads. Returns None if ignore_thread_colors is not list type.
    :rtype: list[int, ...] or None
    """
    if not isinstance(ignore_thread_colors, list):
        return None
    ret = []
    for ignore_color in ignore_thread_colors:
        ignore_color = ImageColor.getcolor(ignore_color, 'RGB')  # returns a trinary tuple
        for i, color in enumerate(rgb_all):
            if list(color)==list(ignore_color):
                ret.append(i)
    return ret


def get_conduct_thread_indices(rgb_all, conduct_thread_colors):
    """Get conductive thread indices. There must be only 2 conductive threads in an tactile sensor embroidery pattern.

    :param rgb_all: Colors of all superpaths.
    :type rgb_all: list[list[int]]

    :param conduct_thread_colors: Conductive thread color. Size of this sequence is not more than 2.
    :type conduct_thread_color: Annotated[list[int], 1] or Annotated[list[int], 2]

    :return: Indices of conductive threads. It must be a sequence of size 2.
    :rtype: Annotated[list[int], 2]

    :raise AssertionError:
    """
    if not isinstance(conduct_thread_colors, list):
        return None
    ret = []
    for conduct_color in conduct_thread_colors:
        conduct_color = ImageColor.getcolor(conduct_color, 'RGB')  # returns a trinary tuple
        for i, color in enumerate(rgb_all):
            if list(color)==list(conduct_color):
                ret.append(i)
    assert len(ret)==2, 'Only 2 conductive threads allowed in an tactile sensor embroidery pattern.'
    return ret


def stitch_path(pattern, x_all, y_all, path_index, pitch, conduct_thread_indices, min_num_stitches_per_segment=1, print_debug=False):
    """Create a sequence of stitches for the specified path of the provided SVG control points.
    For each line segment, will compute the intersections with all other SVG paths.
    Then for each inter-intersection section of the segment, will add stitches according to the specified pitch (avoiding the intersections themselves).
    Will place stitches for each segment according to the directionality of the original SVG path.
    Will also ensure that stitches are placed at the SVG control points.

    :param pattern: Embroidery pattern loaded from SVG file.
    :type pattern: pyembroidery.EmbPattern.EmbPattern

    :param x_all: A list contains 2~3 sublists, each sublist contains X coordinates of all stitch points of a single superpath.
    :type x_all: list[list[float]]

    :param y_all: A list contains 2~3 sublists, each sublist contains Y coordinates of all stitch points of a single superpath.
    :type y_all: list[list[float]]

    :param conduct_thread_indices: Specify indices of conductive threads, it must be a sequence of size 2. Input `None` to disable this feature.
    :type conduct_thread_indices: Annotated[list[int], 2] or None

    :param path_index: Index of paths. It is uesd to index x_all and y_all.
    :type path_index: int

    :param pitch: Legnth between stitch points.
    :type pitch: float
    
    :param min_num_stitches_per_segment: Minmum number of stitch points between two intersections. (Default: 1)
    :type min_num_stitches_per_segment: int, optional
    
    :param print_debug: Verbose mode. (Default: False)
    :type print_debug: bool, optional
    
    :return: Stitch plan of a specific superpath, described in lists of x coordinates and y coordinates of stitches.
    :rtype: tuple[list[float], list[float]]
    """
    x_stitch = []
    y_stitch = []
    num_paths = len(x_all)
    # Iterate through each of the SVG control points.
    num_points = len(x_all[path_index])
    for point_index in range(num_points-1):
        # Will create a list of notable points that define the line segment starting at the current point.
        segment_points_x = np.array([])
        segment_points_y = np.array([])

        # Add the current control point as the starting point.
        segment_points_x = np.append(segment_points_x, x_all[path_index][point_index])
        segment_points_y = np.append(segment_points_y, y_all[path_index][point_index])

        # Add any intersection points between the segment from this control point to the next one,
        #  and any segment of any other paths in the SVG.
        for other_path_index in range(num_paths):

            # Find intersections only if both paths are conductive threads, the conductive thread would be specified by its color.
            if other_path_index == path_index:
                continue

            if conduct_thread_indices:
                if not ((path_index==conduct_thread_indices[0] and other_path_index==conduct_thread_indices[1]) or (path_index==conduct_thread_indices[1] and other_path_index==conduct_thread_indices[0])):
                    continue

            num_other_points = len(x_all[other_path_index])
            for other_point_index in range(num_other_points-1):
                # if print_debug:
                #     print('intersecting (%0.2f, %0.2f)-(%0.2f, %0.2f) with (%0.2f, %0.2f)-(%0.2f, %0.2f)' %
                #           (x_all[path_index][point_index], y_all[path_index][point_index],
                #            x_all[path_index][point_index+1], y_all[path_index][point_index+1],
                #            x_all[other_path_index][other_point_index], y_all[other_path_index][other_point_index],
                #            x_all[other_path_index][other_point_index+1], y_all[other_path_index][other_point_index+1]))
                segment_1 = [[x_all[path_index][point_index], y_all[path_index][point_index]],
                     [x_all[path_index][point_index+1], y_all[path_index][point_index+1]]]
                segment_2 = [[x_all[other_path_index][other_point_index], y_all[other_path_index][other_point_index]],
                     [x_all[other_path_index][other_point_index+1], y_all[other_path_index][other_point_index+1]]]
                intersection = get_segments_intersection(segment_1, segment_2)
                if intersection is not None:
                    segment_points_x = np.append(segment_points_x, intersection[0])
                    segment_points_y = np.append(segment_points_y, intersection[1])

        # Add the next control point as the ending point.
        segment_points_x = np.append(segment_points_x, x_all[path_index][point_index+1])
        segment_points_y = np.append(segment_points_y, y_all[path_index][point_index+1])
        
        # Sort the segment points by their x then y coordinate,
        #  using the same directionality as the original SVG path.
        if x_all[path_index][point_index+1] > x_all[path_index][point_index]:
            x_sort_direction = 1
        else:
            x_sort_direction = -1
        if y_all[path_index][point_index+1] > y_all[path_index][point_index]:
            y_sort_direction = 1
        else:
            y_sort_direction = -1
        sorted_indexes = np.lexsort((y_sort_direction*np.array(segment_points_y),
                                     x_sort_direction*np.array(segment_points_x)))
        segment_points_x = segment_points_x[sorted_indexes]
        segment_points_y = segment_points_y[sorted_indexes]
        
        # plt.figure()
        # plt.plot(pt_x, pt_y, '.-')
        # plt.title('path %d point %d' % (path_index, i))
        # plt.show()
        
        # Add a stitch at the first point (the control point).
        x_stitch.append(x_all[path_index][point_index])
        y_stitch.append(y_all[path_index][point_index])

        # For each section of the line segment as divided by the intersection points,
        #  add however many stitches will fit according to the specified pitch.
        for start_point_index in range(len(segment_points_x)-1):
            start_point = np.array([segment_points_x[start_point_index], segment_points_y[start_point_index]])
            end_point = np.array([segment_points_x[start_point_index+1], segment_points_y[start_point_index+1]])
            distance = np.linalg.norm(end_point - start_point)

            # Compute the number of stitches that can fit.
            # Will compute the number of inter-stitch gaps that can fit, which is one more
            #  than the number of stitches since there will also be the start/end stitch.
            num_stitches = np.floor(distance/pitch).astype(int)-1

            # Put at least one stitch between each intersection pair.
            num_stitches = max(min_num_stitches_per_segment, num_stitches)

            # Then compute the ratio along the segment that each stitch will be.
            stitch_position_ratios = np.arange(0, 1, 1/(num_stitches+1))[1:]

            # Finally, compute the actual stitch positions.
            for stitch_index in range(num_stitches):
                stitch_position = start_point + (end_point-start_point)*(stitch_position_ratios[stitch_index])
                x_stitch.append(stitch_position[0])
                y_stitch.append(stitch_position[1])
            if print_debug:
                print('path_index',path_index)
                print('point_index',point_index)
                print('start_point_index',start_point_index)
                print('start_point',start_point)
                print('end_point',end_point)
                print('distance', distance)
                print('num_stitches', num_stitches)
                print('stitch_position_ratios\n',stitch_position_ratios)
        # Add a stitch at the next point (the control point), if it's the last point in the path.
        # If it's not the last point, then the next iteration of the loop will add it as the starting point.
        if point_index == (num_points-1)-1:
            x_stitch.append(x_all[path_index][point_index+1])
            y_stitch.append(y_all[path_index][point_index+1])

    # Stitch it!
    for stitch_index in range(len(x_stitch)):
        pattern.add_stitch_absolute(pyembroidery.STITCH,
                                    x_stitch[stitch_index],
                                    y_stitch[stitch_index])

    return  x_stitch, y_stitch