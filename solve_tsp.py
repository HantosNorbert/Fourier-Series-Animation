import numpy as np
from scipy.spatial import distance_matrix
from draw import plot_points


# Given a distance matrix, put the index numbers [0, 1, ..., length-1] in order by a greedy way:
# starting from 0, choose the closest free index next
def greedy(dist_mat):
    length = dist_mat.shape[0]
    current_node_idx = 0  # can be random between 0 and length-1
    node_order = [current_node_idx]

    free_node_indices = set(range(length))
    free_node_indices.remove(current_node_idx)
    while free_node_indices:
        next_node_idx = np.argmin([dist_mat[current_node_idx][i] if i in free_node_indices else np.inf
                                   for i in range(length)])
        free_node_indices.remove(next_node_idx)
        node_order.append(next_node_idx)
        current_node_idx = next_node_idx

    return node_order


def opt2swap(tour, i, j):
    return tour[:i] + tour[i:j][::-1] + tour[j:]


# Implements the 2-opt algorithm
def opt2(coord_order, dist_mat):
    tour = coord_order + [coord_order[0]]  # Make it a loop
    length = len(tour)

    min_change = -1
    while min_change < 0:
        min_change = 0
        for i in range(1, length - 2):
            for j in range(i + 2, length):
                # If we swap these two nodes, the overall length of the tour would be changed by this amount
                change = dist_mat[tour[i-1], tour[j-1]] - \
                         dist_mat[tour[i-1], tour[i]] + \
                         dist_mat[tour[i], tour[j]] - \
                         dist_mat[tour[j-1], tour[j]]
                # If it's negative, we improved the tour!
                if change < min_change:
                    min_change = change
                    tour = opt2swap(tour, i, j)
    # Don't forget to remove the last element
    return tour[0:-1]


def solve_tsp(original_points):
    print('Solving TSP...')

    print('  Calculating distance matrix...')
    dist_mat = distance_matrix(original_points, original_points)

    print('  Generating route by Greedy algorithm...')
    point_order = greedy(dist_mat)
    points_in_order = [original_points[i] for i in point_order]

    plot_points(points_in_order, 'Initial point order by Greedy algorithm', as_line=True)

    print('  Refine route by 2-OPT algorithm...')
    point_order = opt2(point_order, dist_mat)
    points_in_order = [original_points[i] for i in point_order]

    plot_points(points_in_order, 'Improved point order by 2-OPT algorithm', as_line=True)

    return points_in_order
