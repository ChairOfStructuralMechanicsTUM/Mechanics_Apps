# Fourier
Information provided in the [documentation](https://github.com/BenjaminRueth/Visualization/blob/master/FourierApp/Doc/fourierSpecification.pdf)

One can also enter any function for computing its Fourier series. For the input we use `sympy` syntax.

## Running
This app can be run by typing
```
$ bokeh serve fourier_app.py
```
into bash and then open
```
http://localhost:5006/fourier_app
```
in the browser.

## ToDos
- [x] Change structure of the App in the style of the sliders example
- [x] Update to Bokeh 0.11
- [x] Add controls for setting periodicity and interval (e.g. [-pi,pi] or [0,2pi] or [0,2])
- [x] Improve GUI
- [x] make sympy input faster (see convolution app as an example implementation)
- [x] make coeff and function value computation faster by using fft and matrix computations (see analytical solution in [PDEApp](https://github.com/BenjaminRueth/Visualization/tree/master/PDEApp)).
- [x] add streaming data update for user view. See Mandelbrot App
- [x] proper documentation
- [ ] print analytical expression of fourier series using [this](http://thelivingpearl.com/2015/10/09/pytex2png-make-pretty-math-png-files-with-latex-python-and-c/)
- [ ] Improve FFT: Currently we are using brute force for getting a nice result (just use many samples and hope the result is good.) A better way would be 
    1. computing the FFT coefficients only once for the function (not always new w.r.t changing N) and reuse the same coefficient vector for different N (only the relevant coefficients 0...N are used).
    2. The maximum number of necessary sampling points (M) can be determined via the maximum resolution of the plot. i.e. if we are plotting with 1000 samples, we cannot detect features that are too small for this resolution. See also [this Paper](https://www.math.upenn.edu/~cle/papers/fftvsft.pdf) especially p.9.    
- [ ] Add code for embedding, such that the app can be published on the internet.
- [ ] Implement dynamic printing of analytical expression in embedded html
