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

        bleed_x = self.vectorial.context.width * (1/19)
        start_end_y = self.vectorial.context.height - (self.vectorial.context.height * (1/19))

        self.start_x = bleed_x
        self.start_y = start_end_y

        self.end_x = self.vectorial.context.width - bleed_x
        self.end_y = start_end_y


    def build(self, fftinfo, this_step, config, effects):

        total_steps = self.vectorial.context.total_steps
        completion = self.functions.proportion(total_steps, 1, this_step)
        resolution_bias = self.vectorial.context.resolution_bias

        average_value = fftinfo["average_value"]

        offset_by_amplitude = average_value * 14 * resolution_bias

        if self.config["mode"] == "bordered":

            colors = [
                1, 1, 1
            ] + [1] # Add full opacity

            # Make a skia color with the colors list as argument
            color = skia.Color4f(*colors)

            # Make the skia Paint and
            paint = skia.Paint(
                AntiAlias = True,
                Color = color,
                Style = skia.Paint.kStroke_Style,
                StrokeWidth = 13, # + (magnitude/4),
                # ImageFilter=skia.ImageFilters.DropShadow(3, 3, 5, 5, skia.ColorWHITE),
            )

            path_vector = [self.end_x - self.start_x, self.end_y - self.start_y]

            to_x = self.functions.proportion(total_steps, path_vector[0], this_step)
            to_y = self.functions.proportion(total_steps, path_vector[1], this_step)

            path = skia.Path()
            path.moveTo(self.start_x, self.start_y + offset_by_amplitude)

            path.lineTo(self.start_x + to_x, self.start_y + to_y + offset_by_amplitude)

            self.skia.canvas.drawPath(path, paint)

            # Borders around image
            if True:
                distance = 9 * resolution_bias

                colors = [
                    1, 1, 1
                ] + [0.7] # Add full opacity

                # Make a skia color with the colors list as argument
                color = skia.Color4f(*colors)

                # Make the skia Paint and
                paint = skia.Paint(
                    AntiAlias = True,
                    Color = color,
                    Style = skia.Paint.kStroke_Style,
                    StrokeWidth = 2, # + (magnitude/4),
                )

                # Top left
                path = skia.Path()
                path.moveTo(self.start_x - distance, self.start_y - distance + offset_by_amplitude)
                
                # Top right
                path.lineTo(self.end_x + distance, self.end_y - distance + offset_by_amplitude)

                # Bottom right
                path.lineTo(self.end_x + distance, self.end_y + distance + offset_by_amplitude)
                self.skia.canvas.drawPath(path, paint)

                # Bottom Left
                path.lineTo(self.start_x - distance, self.start_y + distance + offset_by_amplitude)
                self.skia.canvas.drawPath(path, paint)

                # Top left
                path.lineTo(self.start_x - distance, self.start_y - distance + offset_by_amplitude)
                
                self.skia.canvas.drawPath(path, paint)



