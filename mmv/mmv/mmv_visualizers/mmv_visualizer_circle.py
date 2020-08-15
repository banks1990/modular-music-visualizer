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


class MMVVisualizerCircle:
    def __init__(self, MMVVectorial, context, skia_object):
        self.vectorial = MMVVectorial
        self.context = context
        self.skia = skia_object
        self.config = self.vectorial.config
        self.polar = PolarCoordinates()
        self.functions = Functions()

        self.center_x = self.vectorial.context.width / 2
        self.center_y = self.vectorial.context.height / 2

    def build(self, fitted_ffts: dict, frequencies: list, this_step: int, config: dict, effects):

        resolution_ratio_multiplier = self.vectorial.context.resolution_ratio_multiplier

        if self.config["mode"] == "symetric":

            data = {}
            
            for channel in (["l", "r"]):

                data[channel] = {
                    "coordinates": [],
                    "paints": [],
                }

                this_channel_fft = fitted_ffts[channel]
                npts = len(this_channel_fft)

                for index, magnitude in enumerate(this_channel_fft):

                    if channel == "l":
                        theta = (math.pi/2) - ((index/npts)*math.pi)

                    elif channel == "r":
                        theta = (math.pi/2) + ((index/npts)*math.pi)

                    magnitude = (magnitude / 720) * self.context.height

                    minimum_multiplier = 0.4
                    maximum_multiplier = 17

                    size = (magnitude) * self.functions.ax_plus_b_two_points(
                        x = frequencies[0][index],
                        end_x = 20000,
                        zero_value = minimum_multiplier,
                        max_value = maximum_multiplier,
                    )

                    # size = (magnitude*6) * ( (( (maximum_multiplier - minimum_multiplier)*index) / len(this_channel_fft)) + minimum_multiplier )

                    # We send an r, theta just in case we want to do something with it later on
                    data[channel]["coordinates"].append([
                        # ( self.config["minimum_bar_size"] + magnitude*(2e6) ) * effects["size"],
                        ( self.config["minimum_bar_size"] + size ) * effects["size"],
                        theta,
                    ])

                    # Rotate the colors a bit on each step
                    theta += this_step / 100

                    # Define the color of the bars
                    colors = [
                        abs( math.sin((theta/2)) ),
                        abs( math.sin((theta + ((1/3)*2*math.pi)) / 2) ),
                        abs( math.sin((theta + ((2/3)*2*math.pi)) / 2) ),
                    ] + [0.7] # Add full opacity

                    # Make a skia color with the colors list as argument
                    color = skia.Color4f(*colors)

                    # Make the skia Paint and
                    paint = skia.Paint(
                        AntiAlias = True,
                        Color = color,
                        Style = skia.Paint.kStroke_Style,
                        StrokeWidth = 8 * resolution_ratio_multiplier # + (magnitude/4),
                    )

                    # Store it on a list do draw in the end
                    data[channel]["paints"].append(paint)

            # Our list of coordinates and paints, invert the right channel for drawing the path in the right direction
            # Not reversing it will yield "symetric" bars along the diagonal
            coordinates = data["l"]["coordinates"] + [x for x in reversed(data["r"]["coordinates"]) ]
            paints = data["l"]["paints"] + [x for x in reversed(data["r"]["paints"]) ]
        
            # Filled background
            if False: # self.config["draw_background"]

                path = skia.Path()
                white_background = skia.Paint(
                    AntiAlias = True,
                    Color = skia.ColorWHITE,
                    Style = skia.Paint.kFill_Style,
                    StrokeWidth = 3,
                    ImageFilter=skia.ImageFilters.DropShadow(3, 3, 5, 5, skia.ColorBLACK),
                    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.0)
                )

                more = 1.05

                self.polar.from_r_theta(coordinates[0][0] * more, coordinates[0][1])
                polar_offset = self.polar.get_rectangular_coordinates()

                path.moveTo(
                    (self.center_x + polar_offset[0]),
                    (self.center_y + polar_offset[1]),
                )

                for coord_index, coord in enumerate(coordinates):

                    # TODO: implement this function in DataUtils for not repeating myself
                    get_nearby = 4

                    size_coordinates = len(coordinates)
                    real_state = coordinates*3

                    nearby_coordinates = real_state[
                        size_coordinates + (coord_index - get_nearby):
                        size_coordinates + (coord_index + get_nearby)
                    ]

                    # [0, 1, 2, 3, 4] --> weights=
                    #  3  4  5, 4, 3

                    n = len(nearby_coordinates)

                    weights = [n - abs( (n / 2) - x) for x in range(n)]

                    s = 0
                    for index, item in enumerate(nearby_coordinates):
                        s += item[0] * weights[index]

                    avg_coord = s / sum(weights)

                    self.polar.from_r_theta(avg_coord * more, coord[1])

                    polar_offset = self.polar.get_rectangular_coordinates()

                    path.lineTo(
                        (self.center_x + polar_offset[0]),
                        (self.center_y + polar_offset[1]),
                    )
                
                self.skia.canvas.drawPath(path, white_background)

            # Countour, stroke
            if False: # self.config["draw_black_border"]

                more = 2

                path = skia.Path()

                black_stroke = skia.Paint(
                    AntiAlias = True,
                    Color = skia.ColorWHITE,
                    Style = skia.Paint.kStroke_Style,
                    StrokeWidth = 6,
                    ImageFilter=skia.ImageFilters.DropShadow(3, 3, 5, 5, skia.ColorWHITE),
                    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 1.0)
                )

                for coord_index, coord in enumerate(coordinates):

                    get_nearby = 10

                    size_coordinates = len(coordinates)
                    real_state = coordinates*3

                    nearby_coordinates = real_state[
                        size_coordinates + (coord_index - get_nearby):
                        size_coordinates + (coord_index + get_nearby)
                    ]

                    n = len(nearby_coordinates)

                    weights = [n - abs( (n / 2) - x) for x in range(n)]

                    s = 0
                    for index, item in enumerate(nearby_coordinates):
                        s += item[0] * weights[index]

                    avg_coord = s / sum(weights)

                    self.polar.from_r_theta(self.config["minimum_bar_size"] + ( (avg_coord - self.config["minimum_bar_size"]) * more), coord[1])
                    polar_offset = self.polar.get_rectangular_coordinates()

                    coords = [ (self.center_x + polar_offset[0]), (self.center_y + polar_offset[1]) ]

                    if coord_index == 0:
                        path.moveTo(*coords)
                    path.lineTo(*coords)
                
                self.skia.canvas.drawPath(path, black_stroke)


            # Draw the main bars
            for index, coord in enumerate(coordinates):

                more = 1

                path = skia.Path()
                path.moveTo(self.center_x, self.center_y)

                self.polar.from_r_theta(coord[0], coord[1])
                polar_offset = self.polar.get_rectangular_coordinates()

                path.lineTo(
                    (self.center_x + polar_offset[0]) * more,
                    (self.center_y + polar_offset[1]) * more,
                )

                self.skia.canvas.drawPath(path, paints[index])

                


