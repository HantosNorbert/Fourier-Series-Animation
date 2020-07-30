import matplotlib.pyplot as plt
import matplotlib.animation as animation
from fourier import fourier_analysis, fourier_synthesis
from defaults import NUMBER_OF_EPICYCLES, NUMBER_OF_FRAMES, FPS


def plot_points(coords, title, as_line=False):
    plt.clf()
    plt.title(title)
    plt.axis('off')
    if as_line:
        cx = [c[0] for c in coords] + [coords[0][0]]
        cy = [c[1] for c in coords] + [coords[0][1]]
        plt.plot(cx, cy, markersize=2)
    plt.plot([c[0] for c in coords], [c[1] for c in coords], 'ro', markersize=1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


# Normalize the point coordinates so the shape can fit into the (-1, 1) range to display. To leave some margin,
# the coordinates will range from (-0.8, 0.8). The shape keeps its original aspect ratio.
def normalize(coords):
    x_min = min([c[0] for c in coords])
    x_max = max([c[0] for c in coords])
    y_min = min([c[1] for c in coords])
    y_max = max([c[1] for c in coords])

    ratio = 0.8 * 2 / max(x_max - x_min, y_max - y_min)

    def norm(c):
        return (c[0] - x_min/2 - x_max/2)*ratio, (c[1] - y_min/2 - y_max/2)*ratio

    return [norm(c) for c in coords]


# Create a list of polygonal chains; the i-th polygonal chain will be used for the i-th frame of the animation
def calculate_polygonal_chains(coords):
    # Convert the coordinates into a series of complex points...
    points = [complex(x, y) for x, y in normalize(coords)]

    # The frequencies of the cycles are integers: [..., -2, -1, 0, 1, 2, ...]
    # For drawing purposes, we want the frequencies in increasing absolute order: [0, -1, 1, -2, 2, ...]
    frequencies = list(range(-NUMBER_OF_EPICYCLES // 2 + 1, NUMBER_OF_EPICYCLES // 2 + 1))
    frequencies = sorted(frequencies, key=abs)

    weights = fourier_analysis(frequencies, points)
    # The radius of the n-th circle is just the magnitude of the n-th weight
    circle_radii = [abs(cn) for cn in weights]

    polygonal_chains = []
    for i in range(NUMBER_OF_FRAMES):
        t = i / NUMBER_OF_FRAMES
        polygonal_chain = fourier_synthesis(frequencies, weights, t)
        polygonal_chains.append(polygonal_chain)

    return polygonal_chains, circle_radii


# Get the curve outline from the polygonal chains: the last point of every frame
def get_outline(polygonal_chains):
    points = [p[-1] for p in polygonal_chains]
    px = [p.real for p in points]
    py = [p.imag for p in points]
    return px, py


def draw_fourier_animation(coords, save_animation):
    print('Creating animation...')
    polygonal_chains, circle_radii = calculate_polygonal_chains(coords)

    # Each object will be drawn twice: one for regular display, and one for the zoomed-in display
    circles0 = []
    circles1 = []
    lines0 = []
    lines1 = []

    plt.style.use('dark_background')

    fig, axes = plt.subplots(1, 2)
    axes[0].set_aspect('equal')
    axes[0].axis('off')

    axes[1].set_aspect('equal')
    axes[1].axis('off')

    for idx in range(NUMBER_OF_EPICYCLES):
        # The n-th circle will centered at the n-th point of the polygonal chain
        cx = polygonal_chains[0][idx].real
        cy = polygonal_chains[0][idx].imag
        circle0 = plt.Circle((cx, cy), circle_radii[idx], color='darkred', fill=False, lw=1)
        circles0.append(circle0)
        circle1 = plt.Circle((cx, cy), circle_radii[idx], color='darkred', fill=False, lw=1)
        circles1.append(circle1)

        # The n-th line is simply denoted by the the n-th and n+1-th point of the polygonal chain
        p0x = polygonal_chains[0][idx].real
        p0y = polygonal_chains[0][idx].imag
        p1x = polygonal_chains[0][idx + 1].real
        p1y = polygonal_chains[0][idx + 1].imag
        line0 = axes[0].plot([p0x, p1x], [p0y, p1y], color='grey')[0]
        lines0.append(line0)
        line1 = axes[1].plot([p0x, p1x], [p0y, p1y], color='grey')[0]
        lines1.append(line1)

    # For drawing the final approximation of the curve f(t)
    curve_x, curve_y = [], []
    curve0, = axes[0].plot([], [], lw=2, color='blue')
    curve1, = axes[1].plot([], [], lw=2, color='blue')

    # For drawing the entire outline of the curve f(t)
    outline_x, outline_y = get_outline(polygonal_chains)
    axes[0].plot(outline_x, outline_y, lw=1, color='darkblue')
    outline1, = axes[1].plot(outline_x, outline_y, lw=1, color='darkblue')

    # The range of the first plot is set to (-1, 1), the range of the second plot is closed up and centered around
    # the last point of the polygonal chain
    axes[0].set_xlim((-1, 1))
    axes[0].set_ylim((-1, 1))
    axes[1].set_xlim(polygonal_chains[0][-1].real - 0.05, polygonal_chains[0][-1].real + 0.05)
    axes[1].set_ylim(polygonal_chains[0][-1].imag - 0.05, polygonal_chains[0][-1].imag + 0.05)

    def init():
        for c in circles0:
            axes[0].add_patch(c)
        for c in circles1:
            axes[1].add_patch(c)
        return [outline1] + circles0 + circles1 + lines0 + lines1 + [curve0, curve1]

    def animate(i):
        # Update the circles, the polygonal line, and the drawing curve
        for ii in range(NUMBER_OF_EPICYCLES):
            circles0[ii].center = (polygonal_chains[i][ii].real, polygonal_chains[i][ii].imag)
            circles1[ii].center = (polygonal_chains[i][ii].real, polygonal_chains[i][ii].imag)

            new_p0x = polygonal_chains[i][ii].real
            new_p0y = polygonal_chains[i][ii].imag
            new_p1x = polygonal_chains[i][ii + 1].real
            new_p1y = polygonal_chains[i][ii + 1].imag
            lines0[ii].set_data([new_p0x, new_p1x], [new_p0y, new_p1y])
            lines1[ii].set_data([new_p0x, new_p1x], [new_p0y, new_p1y])

        curve_x.append(polygonal_chains[i][-1].real)
        curve_y.append(polygonal_chains[i][-1].imag)
        curve0.set_data(curve_x, curve_y)
        curve1.set_data(curve_x, curve_y)

        # Update the range of the second plot
        axes[1].set_xlim(polygonal_chains[i][-1].real - 0.05, polygonal_chains[i][-1].real + 0.05)
        axes[1].set_ylim(polygonal_chains[i][-1].imag - 0.05, polygonal_chains[i][-1].imag + 0.05)

        return [outline1] + circles0 + circles1 + lines0 + lines1 + [curve0, curve1]

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=NUMBER_OF_FRAMES, interval=10, blit=True)
    if save_animation:
        print('  Creating animation for saving...')
        anim.save(save_animation, fps=FPS)
    else:
        plt.show()
