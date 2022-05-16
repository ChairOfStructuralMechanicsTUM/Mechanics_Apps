
import numpy as np
from scipy.fft import fft, fftfreq, ifft, fftshift, ifftshift, rfft, rfftfreq, rfft, rfftfreq, irfft
from calculations import *
import matplotlib.pyplot as plt 

def to_frequency_domain(t, ys):
    T = t[-1] -t[0] # observation length
    N = len(t)  # number of samples in the time domain
    sample_rate = N/T
    yf = rfft(ys, N) *2/sample_rate #times two because the time domain is not symmetric about 0 (only the positiv side)
    return yf
    #fftshift --> origin in center
    #ifftshift --> origin in the beginning
 
def to_time_domain(x, y):
    N = 2*len(x)-1 # Number of samples in the time domain
    T = (len(x)-1) / (x[-1]) # observation length in time
    sample_rate = N/T
    ys =irfft(y*sample_rate/2, N)
    return ys 

