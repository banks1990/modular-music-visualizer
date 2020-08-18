"""
===============================================================================

Purpose: MMVPianoRollTopDown object

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

from mmv.common.cmn_coordinates import PolarCoordinates
from mmv.common.cmn_functions import Functions
import numpy as np
import math
import skia


class MMVPianoRollTopDown:
    def __init__(self, MMVVectorial, context, skia_object, midi):
        self.vectorial = MMVVectorial
        self.context = context
        self.skia = skia_object
        self.midi = midi
        self.config = self.vectorial.config
        self.functions = Functions()
    
    def draw_note(self, info):
        pass

    # Build, draw the bar
    def build(self, fftinfo, this_step, config, effects):

        # Get "needed" variables
        total_steps = self.vectorial.context.total_steps
        completion = self.functions.proportion(total_steps, 1, this_step)  # Completion from 0-1 means
        resolution_ratio_multiplier = self.vectorial.context.resolution_ratio_multiplier

        # Average audio amplitude
        average_value = fftinfo["average_value"]

        # Simple mode, only a line with set stroke width
        if self.config["mode"] == "simple":
            pass