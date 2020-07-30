from skimage import feature, io
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import random
from defaults import CANNY_SIGMA_DEFAULT, CANNY_LOW_THRESHOLD_DEFAULT, CANNY_HIGH_THRESHOLD_DEFAULT
from defaults import DO_SAMPLING, SAMPLING_SIZE, RANDOM_SEED


# Select random SAMPLING_SIZE number of points from the original list
def sampling(coords):
    if len(coords) <= SAMPLING_SIZE:
        return coords

    random.seed(RANDOM_SEED)
    random_indices = list(range(len(coords)))
    random.shuffle(random_indices)
    return [coords[random_indices[i]] for i in range(SAMPLING_SIZE)]


# Given an image name, return with a set of points representing the edges
def detect_edges(image_name):
    print('Detecting edges...')
    image = io.imread(image_name, as_gray=True)

    # Initial Canny edge detection
    edges = feature.canny(image, CANNY_SIGMA_DEFAULT, CANNY_LOW_THRESHOLD_DEFAULT, CANNY_HIGH_THRESHOLD_DEFAULT,
                          use_quantiles=True)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.imshow(image, cmap=plt.cm.gray)
    ax1.axis('off')
    ax1.set_title('Image', fontsize=20)

    edge_im = ax2.imshow(edges, cmap=plt.cm.gray)
    ax2.axis('off')
    ax2.set_title('Canny edges', fontsize=20)

    # Set up the sliders: the lower and upper threshold percentages can be set by the user
    axcolor = 'lightgoldenrodyellow'
    ax_sigma_th = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    s_sigma_th = Slider(ax_sigma_th, 'Sigma threshold', 0.0, 10.0, valinit=CANNY_SIGMA_DEFAULT)
    ax_low_th = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    s_low_th = Slider(ax_low_th, 'Low threshold', 0.0, 1.0, valinit=CANNY_LOW_THRESHOLD_DEFAULT)
    ax_high_th = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
    s_high_th = Slider(ax_high_th, 'High threshold', 0.0, 1.0, valinit=CANNY_HIGH_THRESHOLD_DEFAULT)

    # If a slider changes, re-apply Canny
    def update(val):
        new_edges = feature.canny(image, s_sigma_th.val, s_low_th.val, s_high_th.val, use_quantiles=True)
        edge_im.set_data(new_edges)
        fig.canvas.draw_idle()

    s_sigma_th.on_changed(update)
    s_low_th.on_changed(update)
    s_high_th.on_changed(update)

    plt.show()

    # x and y coordinates are just the non-zero points of the edge-image
    x_coords, y_coords = np.nonzero(edge_im.get_array())
    # The x and y axes of an image differs from the x and y axes of a plot, so we have to go from (x,y) to (y,-x).
    # Otherwise we would se the image flipped.
    points = list(zip(y_coords, -x_coords))

    print(f'  Number of initial points: {len(points)}')
    # Reduce the number of points if requested
    if DO_SAMPLING:
        points = sampling(points)
    print(f'  Number of final points: {len(points)}')

    return points
