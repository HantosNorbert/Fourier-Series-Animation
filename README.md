# Fourier Series Animation

This application demonstrates how any closed curve can be approximated by a series of epicycles, known as Fourier series.

![Epicycles drawing an elephant](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/elephant.gif?raw=true)

*Epycicles drawing an elephant. Left: original, right: close up.*

In the animation above, there are 101 little white line segments, each one rotates at some constant integer frequency. They are added together, tip to tail, and the path of the tip of the last one marked with blue. The length, frequency and starting angle of each line segment are set in a specific way so that the resulted blue curve resembles an elephant. The rotating parts called [epicycles](https://en.wikipedia.org/wiki/Deferent_and_epicycle), and the resulted curve is called the [complex Fourier series](https://en.wikipedia.org/wiki/Fourier_series).

## Mathematical definition

Given a closed curve *f(t)* on the complex plane with *0 ≤ t < 1*, *f(t)* can be expressed as the sum of epicycles:

![equation](https://latex.codecogs.com/gif.latex?f%28t%29%20%3D%20%5Csum_n%20c_n%20%5Ccdot%20e%5E%7Bn%202%20%5Cpi%20i%20t%7D)

where *n* in *{..., -2, -1, 0, 1, 2, ...}* are the integer frequencies of the epicycles, and *c_n* is the weight of the *n*-th epicycle, representing its radius and starting angle as a complex number. The weight *c_n* can be calculated as:

![equation](https://latex.codecogs.com/gif.latex?c_n%20%3D%20%5Cint_0%5E1%20f%28t%29e%5E%7B-2%20%5Cpi%20i%20n%20t%7D%20dt)

In practice, the integral is approximated numerically, and the sequence of frequencies is finite, containing the integers of lower magnitude: *n* in *{0, -1, 1, -2, 2, -3, 3, ..., -N, N}*. The bigger the value *N*, the closer the resulted curve will be to the original.

## Steps of the Animation

1) Load any image. Siluette images are preffered, since they already have a nice contour.
1) Run an edge detector. In this application, it's the [Canny edge detector](https://en.wikipedia.org/wiki/Canny_edge_detector), where the user can adjust the sigma value, the lower and the upper threshold parameters. The pixels of the resulted image will be our points on the complex plane representing the curve *f(t)*.
1) Reduce the number of points by random sampling (optional). This can speed up the next step, but might lose accuracy on the curve.
1) Sort the points so they describe a closed curve. This is done by solving the [Traveling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem), which is approximated in two steps:
    1) Set up an initial route in a greedy way: select the first point, then choose the closest unused point iteratively.
    1) Refine the route by the [2-OPT](https://en.wikipedia.org/wiki/2-opt) algorithm.
1) Based on *f(t)*, calculate the weight *c_n* of the epicycle of frequency *n*, for a set of predetermined frequencies.
1) Draw the animation, where *t* goes from *0* to *1*. The positions of the circles and line segments can be derived directly from the series of weights.

## Requirements

- Python
- NumPy
- SciPy
- scikit-image
- Matplotlib

## How to Run the Application

To start the application start `main.py` with the image as its first command-line argument:

```
python main.py images/castle.jpg
```

This will show the resulted animation on screen. However, if you want to save it as a GIF instead, run:

```
python main.py images/castle.jpg -s castle.gif
```

After the application loaded the image, you will see the edge detection screen:

![Castle edges](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/castle_edges.png?raw=true)

Tweak the parameters until you satisfied with the result. Close the window to see the result of the greedy route building algorithm:

![Castle greedy route](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/castle_greedy.png?raw=true)

After closing the window, you will see the result of the final route, refined by the 2-opt algorithm. This may take a while if there are a lot of points.

![Castle 2-opt route](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/castle_2opt.png?raw=true)

Close it and you will see the final animation (or wait until the application saves it as a GIF).

![Castle gif](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/castle.gif?raw=true)

## Fine Tune Some Parameters

The file `defaults.py`contains some extra parameters you can tweak. Here you can change the number of frames of the animation, the fps of the resulted GIF, the number of epicycles, etc.

Notes:
- `NUMBER_OF_EPICYCLES` should be around 101 or lower for simpler curves, and 201, 301 or even bigger for more complicated and detailed curves. The higher the number, the more precise the curve will be, but the application can slow down drastically. Odd numbers are preferred, but not required. If the number is too high, there can be issues due to the limit of floating point precision.
- `FOURIER_DT` controls the step size of the numerical intergration. Should be close to 0, but the smaller the value is, the more computationally intense the calculation becomes.
- `SAMPLING_SIZE` determines how many points should represent the original curve at most. Technically, random `SAMPLING_SIZE` number of points will be selected from the edge image. If `DO_SAMPLING` is set to `False`, this step will be skipped, and all the edge points will be considered in the route building. But be aware that the 2-opt algorithm can be very slow.

## Example Animations

![Octogon](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/images/octogon.png?raw=true)

![Octogon gif](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/octogon.gif?raw=true)

![Cat](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/images/cat.png?raw=true)

![Cat gif](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/cat.gif?raw=true)

![Girl](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/images/girl.png?raw=true)

![Girl gif](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/girl.gif?raw=true)

![Dragon](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/images/dragon.jpg?raw=true)

![Dragon gif](https://github.com/HantosNorbert/Fourier-Series-Animation/blob/master/screenshots/dragon.gif?raw=true)


## Possible Improvements

- Faster animation rendering.
- Interactive animation; e.g., the user can change the number of epicycles on the run.
- More sophisticated point sampling algorithm: sparse sampling at straight lines, dense sampling at curves.
- Better numerical integration tools.
- Faster TSP solving (using GPU for example).
- Process vector image formats - they already contain a route to describe the image!

---

This project was inspired by the youtube channel [3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw) and its video on the [Fourier series](https://www.youtube.com/watch?v=-qgreAUpPwM).

*Norbert Hantos, 2020. 07. 31.*
