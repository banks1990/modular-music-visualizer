"""
===============================================================================

Purpose: Apply fourier transformations on numpy array audio data based on
settings like sample size

===============================================================================

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

===============================================================================
"""

from scipy.fftpack import fft
import scipy.signal
import numpy as np
import math

class Fourier:

    # Calculate an Fast Fourier Transform, doesn't return DC bias (first bin)
    # and cuts up to the middle where the useful info ends
    def fft(self, data: np.ndarray) -> np.ndarray:

        debug_prefix = "[Fourier.fft]"

        # Calculate the fft
        transform = fft(data)

        # Only need half the list of fft and don't need the DC bias (first item)
        cut = [1, len(data) // 2]

        return transform[cut[0]:cut[1]]

    # For more information, https://stackoverflow.com/questions/4364823
    def binned_fft(self, data: np.ndarray, sample_rate: int, original_sample_rate: int=48000) -> dict:

        # f_welch, S_xx_welch = scipy.signal.welch(
        #     data,
        #     fs = sample_rate,
        #     scaling = "density", #"spectrum",
        #     window = scipy.signal.exponential(len(data), tau=0.1)
        # )

        # f, t, Sxx = scipy.signal.spectrogram(
        #     data,
        #     sample_rate,
        #     nperseg = 2048
        # )

        # print(f, t,  f.shape, t.shape, Sxx.shape)
        # exit()

        # print(f_welch, len(f_welch))
        # return dict(zip(f, Sxx))
        # # #
        
        # The FFT length
        N = data.shape[0]

        # Get the nth frequency of the fft
        get_bin = lambda n : n * (sample_rate/N)

        # Get the fft
        fft = self.fft(data)

        binned_fft_dict = {}

        # Assign freq vs fft on a dictionary
        for index in range(1, len(fft)):

            # " The height is a reflection of power density, so if you double the sampling frequency,
            # and hence half the width of each frequency bin, you'll double the amplitude of the FFT result.""
            # >> https://wiki.analytica.com/FFT
            #
            # original_sample_rate * 2^n = sample_rate
            # 2^n = original_sample_rate / sample_rate
            # n log(2) = log(sample_rate / original_sample_rate)
            # n = log(sample_rate / original_sample_rate) / log(2)

            n = math.log10(original_sample_rate / sample_rate) / math.log10(2)
            frequency = round(get_bin(index), 2)
            binned_fft_dict[frequency] = fft[index] * (2**n)


        return binned_fft_dict