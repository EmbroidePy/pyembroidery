import pyembroidery
import numpy as np
import matplotlib.pyplot as plt
import svgpathtools
from svgpathtools import svg2paths
from scipy import spatial
import math
import cv2
import re

# Parse a size string such as "10mm" into its value, and convert it to the target units.
# Adapted from https://github.com/SebKuzminsky/svg2gcode/blob/94f28c1877c721c66cd90a38750f78d8031ac85a/gcoder.py#L238
def _parse_svg_size_string(size_str, target_units='mm'):
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

def extract_pt_from_svg(file, scale, viz, target_units):
    paths, attributes = svg2paths(file)
    # print (paths) # 0:path, 1:sec, 2:point

    x_all = []
    y_all = []

    for i in range(len(paths)):
        x = []
        y = []
        for j in range(len(paths[i])):
            for k in [0, -1]:
                # print (paths[i][j][k])
                x.append(paths[i][j][k].real)
                y.append(-paths[i][j][k].imag)

        x_all.append(x)
        y_all.append(y)

        if viz:
            plt.scatter(x,y, s=100, c='red')
            plt.show()

    if target_units != None:
    
        # Scale to get the desired units.
        doc = svgpathtools.Document(file)
        svg_attributes = doc.root.attrib
        if 'width' not in svg_attributes or 'height' not in svg_attributes:
            print('Size information was not found in the SVG. Using raw point coordinates.')
        else:
            # Define a helper to scale all arrays of points.
            # For example, point_arrays can be x_all or y_all.
            def scale_point_arrays(point_arrays, target_range, name):
                # Get the min and max of points across all arrays.
                points_min = min([min(points) for points in point_arrays])
                points_max = max([max(points) for points in point_arrays])
                # Compute the scale factor.
                points_range = abs(points_max - points_min)
                scale_factor = target_range / points_range
                # Scale it!
                print('Scaling %s by a factor of %g' % (name, scale_factor))
                for (i, points) in enumerate(point_arrays):
                    point_arrays[i] = [point*scale_factor for point in points]
                return point_arrays
            # Get the actual size in physical units.
            svg_width = _parse_svg_size_string(svg_attributes['width'], target_units=target_units)
            svg_height = _parse_svg_size_string(svg_attributes['height'], target_units=target_units)
            # Scale so the points match the target range.
            x_all = scale_point_arrays(x_all, svg_width, 'x')
            y_all = scale_point_arrays(y_all, svg_height, 'y')
            # plt.figure()
            # plt.plot(x_all[0], y_all[0])
            # plt.show()

    # Apply any user-specified scaling.
    for (i, points) in enumerate(x_all):
        x_all[i] = [point*scale for point in points]
    for (i, points) in enumerate(y_all):
        y_all[i] = [point*scale for point in points]
    return x_all, y_all


def draw_line(pattern, st, ed, pitch, endpoint):
    x_pos = []
    y_pos = []
    x_dis = ed[0] - st[0]
    y_dis = ed[1] - st[1]
    dis = np.sqrt(x_dis**2 + y_dis**2)

    sec = dis//pitch

    if sec == 0:
        sec = 1

    x = np.linspace(st[0], ed[0], int(sec)+1, endpoint=endpoint)
    y = np.linspace(st[1], ed[1], int(sec)+1, endpoint=endpoint)

    # print (len(x))
    for i in range(len(x)):
        pattern.add_stitch_absolute(pyembroidery.STITCH, x[i], y[i])

        x_pos.append(x[i])
        y_pos.append(y[i])

    return x_pos, y_pos

def draw_line_mid(pattern, st, ed, pitch):
    x_pos = []
    y_pos = []
    x_dis = ed[0] - st[0]
    y_dis = ed[1] - st[1]
    dis = np.sqrt(x_dis**2 + y_dis**2)


    if dis <= 3 * pitch:
        x_mid = (st[0] + ed[0])/2
        y_mid = (st[1] + ed[1])/2
        pattern.add_stitch_absolute(pyembroidery.STITCH, x_mid, y_mid)
        return [x_mid], [y_mid]

    else:
        sec = dis//pitch
        x = np.linspace(st[0], ed[0], int(sec), endpoint=True)
        y = np.linspace(st[1], ed[1], int(sec), endpoint=True)

        x = x[1:-1]
        y = y[1:-1]

        # print (len(x))
        for i in range(len(x)):
            pattern.add_stitch_absolute(pyembroidery.STITCH, x[i], y[i])

            x_pos.append(x[i])
            y_pos.append(y[i])

    return x_pos, y_pos


def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    """find the intersection of line segments A=(x1,y1)/(x2,y2) and
    B=(x3,y3)/(x4,y4). Returns a point or None"""
    denom = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    if denom==0: return None
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    if (px - x1) * (px - x2) < 0 and (py - y1) * (py - y2) < 0 \
      and (px - x3) * (px - x4) < 0 and (py - y3) * (py - y4) < 0:
        return [px, py]
    else:
        return None


def drawline_halfway_1(pattern, x_all, y_all, pitch):
    pos_x = []
    pos_y = []
    for i in range(len(x_all[0])//2):
        pt_x = []
        pt_y = []
        pt_x.append(x_all[0][2*i])
        pt_y.append(y_all[0][2*i])

        for j in range(len(x_all[1])//2):
            int_pt = line_intersection(x_all[0][2*i], y_all[0][2*i], x_all[0][2*i+1], y_all[0][2*i+1],
                                       x_all[1][2*j], y_all[1][2*j], x_all[1][2*j+1], y_all[1][2*j+1])

            if int_pt:
                pt_x.append(int_pt[0])
                pt_y.append(int_pt[1])

        pt_x.append(x_all[0][2*i+1])
        pt_y.append(y_all[0][2*i+1])


        # print ('compare', x_all[1][2*i], x_all[1][2*i+1], pt_x[-2], pt_x[1])
        if len(pt_x) > 3:
            if (x_all[0][2*i] > x_all[0][2*i+1] and pt_x[-2] > pt_x[1]) or (x_all[0][2*i] < x_all[0][2*i+1] and pt_x[-2] < pt_x[1]):
                temp_x = pt_x[1:-1]
                x = temp_x[::-1]
                temp_y = pt_y[1:-1]
                y = temp_y[::-1]
                pt_x[1:-1] =  x
                pt_y[1:-1] =  y


        # for l in range(len(pt_x)):
        #     # print (pt_x[l], pt_y[l])
        #     plt.scatter(pt_x[:l+1], pt_y[:l+1], c='red', s=20)
        #     # plt.ylim(-400, 0)
        #     # plt.xlim(-100, 600)
        #     # plt.show()


        if len(pt_x) <= 1:
            raise Exception("error!")
        elif len(pt_x) == 2:
            for l in range(len(pt_x)-1):
                x, y = draw_line(pattern, [pt_x[l], pt_y[l]], [pt_x[l+1], pt_y[l+1]], pitch, True)
                pos_x += x
                pos_y += y
        else:
            # x, y = draw_line(pattern, [pt_x[0], pt_y[0]], [pt_x[1], pt_y[1]], pitch, False)
            # print ('x0',len(x))
            # pos_x += x
            # pos_y += y
            for l in range(len(pt_x)-1):
                x, y = draw_line_mid(pattern, [pt_x[l], pt_y[l]], [pt_x[l+1], pt_y[l+1]], pitch)
                pos_x += x
                pos_y += y

        #     x, y = draw_line(pattern, [pt_x[-2], pt_y[-2]], [pt_x[-1], pt_y[-1]], pitch, False)
        # #     print ('x1', len(x))
        #     pos_x += x
        #     pos_y += y
        # print (len(pos_x))
    return  pos_x, pos_y

def drawline_halfway_2(pattern, x_all, y_all, pitch):
    pos_x = []
    pos_y = []
    for i in range(len(x_all[1])//2):
        pt_x = []
        pt_y = []
        pt_x.append(x_all[1][2*i])
        pt_y.append(y_all[1][2*i])

        for j in range(len(x_all[0])//2):
            int_pt = line_intersection(x_all[1][2*i], y_all[1][2*i], x_all[1][2*i+1], y_all[1][2*i+1],
                                       x_all[0][2*j], y_all[0][2*j], x_all[0][2*j+1], y_all[0][2*j+1])

            if int_pt:
                pt_x.append(int_pt[0])
                pt_y.append(int_pt[1])

        pt_x.append(x_all[1][2*i+1])
        pt_y.append(y_all[1][2*i+1])

        if len(pt_x) > 3:
            if (y_all[1][2*i] > y_all[1][2*i+1] and pt_y[-2] > pt_y[1]) or (y_all[1][2*i] < y_all[1][2*i+1] and pt_y[-2] < pt_y[1]):
                temp_x = pt_x[1:-1]
                x = temp_x[::-1]
                temp_y = pt_y[1:-1]
                y = temp_y[::-1]
                pt_x[1:-1] =  x
                pt_y[1:-1] =  y


        if len(pt_x) <= 1:
            raise Exception("error!")
        elif len(pt_x) == 2:
            for l in range(len(pt_x)-1):
                x, y = draw_line(pattern, [pt_x[l], pt_y[l]], [pt_x[l+1], pt_y[l+1]], pitch, True)
                pos_x += x
                pos_y += y
        else:
            # x, y = draw_line(pattern, [pt_x[0], pt_y[0]], [pt_x[1], pt_y[1]], pitch, False)
            # pos_x += x
            # pos_y += y
            for l in range(len(pt_x)-1):
                x, y = draw_line_mid(pattern, [pt_x[l], pt_y[l]], [pt_x[l+1], pt_y[l+1]], pitch)
                pos_x += x
                pos_y += y
            # x, y = draw_line(pattern, [pt_x[-2], pt_y[-2]], [pt_x[-1], pt_y[-1]], pitch, True)
            # pos_x += x
            # pos_y += y
    return  pos_x, pos_y
