from generateDST_utils import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, default='./SVG/Asset 2palm.svg', help='input file path')
# parser.add_argument('--input_path', type=str, default='./Asset 1sensor1_exportNotResponsive.svg', help='input file path')
parser.add_argument('--output_path', type=str, default='./output/', help='output path')
parser.add_argument('--output_name', type=str, default='Asset 2palm.dst', help='output file name')
parser.add_argument('--pitch', type=int, default=40, help='pitch')
parser.add_argument('--viz', type=bool, default=True, help='viz')
parser.add_argument('--scale', type=float, default=10/4.2067, help='design scale')
args = parser.parse_args()

pattern = pyembroidery.EmbPattern()

x_all, y_all = extract_pt_from_svg(args.input_path, args.scale,
                                   viz=args.viz, target_units=None)
print ('control points extracted from svg')

'''single path'''
if len(x_all) == 1:
    x_pos_all = []
    y_pos_all = []
    for i in range(len(x_all[0])-1):
        if i%2 == 0:
            x, y = draw_line(pattern, [x_all[0][i], y_all[0][i]], [x_all[0][i+1], y_all[0][i+1]],
                             args.pitch, endpoint=False)
            x_pos_all += x
            y_pos_all += y
    pyembroidery.write_dst(pattern, args.output_path + args.output_name)
    print ('single path, pitch=', args.pitch, ', ', args.output_path + args.output_name, 'saved')
    if args.viz:
        marker_size = (max(x_pos_all)-min(x_pos_all))
        plt.scatter(x_pos_all, y_pos_all, c='green', s=marker_size)
        for i in range(len(x_pos_all)-1):
            plt.plot([x_pos_all[i], x_pos_all[i+1]], [y_pos_all[i], y_pos_all[i+1]])
        plt.show()


'''two crossing paths'''
if len(x_all) == 2:
    x_pos_all = [[],[]]
    y_pos_all = [[],[]]
    print (len(x_all[0]), len(x_all[1]))
    x, y = drawline_halfway_1(pattern, x_all, y_all, pitch=args.pitch)
    x_pos_all[0] += x
    y_pos_all[0] += y
    pattern.color_change()
    x, y = drawline_halfway_2(pattern, x_all, y_all, pitch=args.pitch)
    x_pos_all[1] += x
    y_pos_all[1] += y

    pyembroidery.write_dst(pattern, args.output_path + args.output_name)
    print ('two paths, pitch=', args.pitch, ', ', args.output_path + args.output_name, 'saved')

    if args.viz:
        # marker_size = (max(x_pos_all[0])-min(x_pos_all[0]))
        # print (x_pos_all[0])
        plt.scatter(x_pos_all[0], y_pos_all[0], c='green', s=10)
        for i in range(len(x_pos_all[0])-1):
            plt.plot([x_pos_all[0][i], x_pos_all[0][i+1]], [y_pos_all[0][i], y_pos_all[0][i+1]])
        plt.scatter(x_pos_all[1], y_pos_all[1], c='blue', s=10)
        for i in range(len(x_pos_all[1])-1):
            plt.plot([x_pos_all[1][i], x_pos_all[1][i+1]], [y_pos_all[1][i], y_pos_all[1][i+1]])
        plt.show()



