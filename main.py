from edge_detection import detect_edges
from solve_tsp import solve_tsp
from draw import draw_fourier_animation
import argparse


def main(args):
    edge_points = detect_edges(args.image_name)
    edge_points_in_order = solve_tsp(edge_points)
    draw_fourier_animation(edge_points_in_order, args.save_animation)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fourier series animation.')
    parser.add_argument('image_name', type=str, help='Name of the image with relative or full path.')
    parser.add_argument('-s', '--save_animation', type=str, help='If set, the animation will be saved as the given '
                                                                 'name. If not set, the animation will be showed '
                                                                 'instead.')
    parsed_args = parser.parse_args()
    main(parsed_args)
