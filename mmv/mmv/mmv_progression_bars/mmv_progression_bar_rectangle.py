"""
===============================================================================

Purpose: MMVVisualizer object

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


class MMVProgressionBarRectangle:
    def __init__(self, MMVVectorial, context, skia_object):
        self.vectorial = MMVVectorial
        self.context = context
        self.skia = skia_object
        self.config = self.vectorial.config
        self.polar = PolarCoordinates()
        self.functions = Functions()

        # Leave this much of blank space at the left and right edge
        bleed_x = self.vectorial.context.width * (1/19)

        # Where Y starts and ends, ie. what horizontal line to draw the progression bar on
        start_end_y = (19/20) * self.vectorial.context.height

        # End X we have to count the bleed
        self.start_x = bleed_x
        self.end_x = self.vectorial.context.width - bleed_x
        
        self.start_y = start_end_y
        self.end_y = start_end_y

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

            # We push the bar downwards according to the avg amplitude for a nice shaky-blur effect
            offset_by_amplitude = average_value * 14 * resolution_ratio_multiplier

            # White full opacity color
            colors = [1, 1, 1, 1]

            # Make a skia color with the colors list as argument
            color = skia.Color4f(*colors)

            # Make the skia Paint and
            paint = skia.Paint(
                AntiAlias = True,
                Color = color,
                Style = skia.Paint.kStroke_Style,
                StrokeWidth = 10 * resolution_ratio_multiplier, # + (magnitude/4),
                # ImageFilter=skia.ImageFilters.DropShadow(3, 3, 5, 5, skia.ColorWHITE),
            )

            # The direction we're walking centered at origin, $\vec{AB} = A - B$
            path_vector = np.array([self.end_x - self.start_x, self.end_y - self.start_y])

            # Proportion we already walked
            path_vector = path_vector * completion

            # Draw the main line starting at the start coordinates, push down by offset_by_amplitude
            path = skia.Path()
            path.moveTo(self.start_x, self.start_y + offset_by_amplitude)
            path.lineTo(self.start_x + path_vector[0], self.start_y + path_vector[1] + offset_by_amplitude)
            self.skia.canvas.drawPath(path, paint)

            # Borders around image
            if True:
                # Distance away from s
                distance = 9 * resolution_ratio_multiplier

                colors = [1, 1, 1, 0.7]

                # Make a skia color with the colors list as argument
                color = skia.Color4f(*colors)

                # Make the skia Paint and
                paint = skia.Paint(
                    AntiAlias = True,
                    Color = color,
                    Style = skia.Paint.kStroke_Style,
                    StrokeWidth = 2,
                )

                # Rectangle border
                border = skia.Rect(
                    self.start_x - distance,
                    self.start_y - distance + offset_by_amplitude,
                    
                    self.end_x + distance,
                    self.end_y + distance + offset_by_amplitude
                )
                
                # Draw the border
                self.skia.canvas.drawRect(border, paint)



