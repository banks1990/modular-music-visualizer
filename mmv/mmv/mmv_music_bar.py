"""
===============================================================================

Purpose: MMVMusicBars object for music bars

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

from mmv.music_bars.mmv_music_bar_circle import MMVMusicBarsCircle
from mmv.common.cmn_coordinates import PolarCoordinates
from mmv.common.cmn_interpolation import Interpolation
from mmv.common.cmn_functions import Functions
from mmv.common.cmn_functions import FitIndex
from mmv.common.cmn_skia import SkiaWrapper
from mmv.common.cmn_frame import Frame
from mmv.common.cmn_utils import Utils
from mmv.mmv_modifiers import *
from resampy import resample
import numpy as np
import random
import math
import os


class MMVMusicBars:
    def __init__(self, context, config: dict, skia_object) -> None:
        
        debug_prefix = "[MMVMusicBars.__init__]"
        
        self.context = context
        self.config = config
        self.skia = skia_object

        self.fit_transform_index = FitIndex()
        self.functions = Functions()
        self.utils = Utils()

        self.path = {}

        self.x = 0
        self.y = 0
        self.size = 1
        self.is_deletable = False
        self.offset = [0, 0]
        self.polar = PolarCoordinates()

        self.current_fft = {}

        self.image = Frame()

        # We use separate file and classes for each type of visualizer

        # Circle, radial visualizer
        if self.config["type"] == "circle":
            self.builder = MMVMusicBarsCircle(self, self.context, self.skia)

    # Smooth an array
    def smooth(self, array, smooth):
        if smooth > 0:
            box = np.ones(smooth)/smooth
            array_smooth = np.convolve(array, box, mode='same')
            return array_smooth
        return array

    # Next step of animation
    def next(self, fftinfo, this_step, effects):

        # # # We start with a bunch of routines for interpolating our fft on the three channels
        # # # according to the last value

        # Get info
        fitfourier = self.config["fourier"]["fitfourier"]
        frequencies = fftinfo["frequencies"]
        ffts = fftinfo["fft"]

        # Abs of left and right channel
        ffts = [
            np.abs(ffts[0]),
            np.abs(ffts[1])
        ]

        # Add mean FFT, the "mid/mean" (m) channel
        ffts.append( (ffts[0] + ffts[1]) / 2 )

        # Smooth the ffts
        ffts = [ self.smooth(fft, fitfourier["pre_fft_smoothing"]) for fft in ffts ]

        # The order of channels on the ffts list
        channels = ["l", "r", "m"]

        # The points to draw the visualization
        points = {}

        # Start each channel point's empty
        for channel in channels:
            points[channel] = []

        # Dictionary with all the data to make a visualization bar
        fitted_ffts = {}

        # Loop on each channel
        for channel_index, channel in enumerate(channels):

            # Get this channel raw fft and its size
            fft = ffts[channel_index]
            fft_size = fft.shape[0]
            
            # Create a empty zeros array as a starting point for the interpolation
            if not channel in list(self.current_fft.keys()):
                self.current_fft[channel] = np.zeros(fft_size)

            # The interpolation dictionary
            interpolation = self.config["fourier"]["interpolation"]

            # Interpolate the next fft with the current one
            for index in range(len(self.current_fft[channel])):
                
                interpolation.start_value = self.current_fft[channel][index]
                interpolation.target_value = fft[index]
                interpolation.current_value = self.current_fft[channel][index]

                self.current_fft[channel][index] = interpolation.next()

            # Start a zero fitted fft list
            fitted_fft = np.copy( self.current_fft[channel] )

            # # Smoothing can look weird, "musical notes" preset fixes almost everything

            # Smooth the peaks
            if fitfourier["pos_fft_smoothing"] > 0:
                fitted_fft = self.smooth(fitted_fft, fitfourier["pos_fft_smoothing"])

            # Apply "subdivision", break jagged edges into more smooth parts
            if fitfourier["subdivide"] > 0:
                fitted_fft = resample(fitted_fft, fitted_fft.shape[0], fitted_fft.shape[0] * fitfourier["subdivide"])

            # Send the fitted fft to its list
            fitted_ffts[channel] = np.copy(fitted_fft)

        # Call our actual visualizer for drawing directly on the canvas
        self.builder.build(fitted_ffts, frequencies, this_step, self.config, effects)
  