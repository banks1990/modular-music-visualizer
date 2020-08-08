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
import numpy as np
import math
import skia


class MMVVisualizerCircle:
    def __init__(self, MMVVisualizer, skia_object):
        self.visualizer = MMVVisualizer
        self.skia = skia_object
        self.config = self.visualizer.config
        self.polar = PolarCoordinates()

        self.center_x = self.visualizer.context.width / 2
        self.center_y = self.visualizer.context.height / 2

    def build(self, fitted_ffts: dict, this_step, config, effects) -> np.ndarray:

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

                    # We send an r, theta just in case we want to do something with it later on
                    data[channel]["coordinates"].append([
                        ( self.config["minimum_bar_size"] + magnitude * 9 ) * effects["size"],
                        theta,
                    ])

                    theta += this_step/100

                    colors = [
                        abs( math.sin((theta/2)) ),
                        abs( math.sin((theta + ((1/3)*2*math.pi)) / 2) ),
                        abs( math.sin((theta + ((2/3)*2*math.pi)) / 2) ),
                    ] + [1]

                    color = skia.Color4f(*colors)

                    paint = skia.Paint(
                        AntiAlias = True,
                        Color = color,
                        Style = skia.Paint.kStroke_Style,
                        StrokeWidth = 2,
                    )

                    data[channel]["paints"].append(paint)

            coordinates = data["l"]["coordinates"] + [x for x in reversed(data["r"]["coordinates"]) ]
            paints = data["l"]["paints"] + [x for x in reversed(data["r"]["paints"]) ]
        
            

            # Filled background
            if True: # self.config["draw_background"]

                path = skia.Path()
                white_background = skia.Paint(
                    AntiAlias = True,
                    Color = skia.ColorWHITE,
                    Style = skia.Paint.kFill_Style,
                    StrokeWidth = 2,
                )

                more = 1.1

                self.polar.from_r_theta(coordinates[0][0] * more, coordinates[0][1])
                polar_offset = self.polar.get_rectangular_coordinates()

                path.moveTo(
                    (self.center_x + polar_offset[0]),
                    (self.center_y + polar_offset[1]),
                )

                for coord in coordinates:
                    self.polar.from_r_theta(coord[0] * more, coord[1])
                    polar_offset = self.polar.get_rectangular_coordinates()
                    path.lineTo(
                        (self.center_x + polar_offset[0]),
                        (self.center_y + polar_offset[1]),
                    )
                
                self.skia.canvas.drawPath(path, white_background)

            # Countour, stroke
            if True: # self.config["draw_black_border"]

                more = 1.05

                path = skia.Path()

                self.polar.from_r_theta(coordinates[0][0] ** more, coordinates[0][1])
                polar_offset = self.polar.get_rectangular_coordinates()

                path.moveTo(
                    (self.center_x + polar_offset[0]),
                    (self.center_y + polar_offset[1]),
                )

                black_stroke = skia.Paint(
                    AntiAlias = True,
                    Color = skia.ColorWHITE,
                    Style = skia.Paint.kStroke_Style,
                    StrokeWidth = 3,
                )

                for coord in coordinates:
                    self.polar.from_r_theta(coord[0] ** more, coord[1])
                    polar_offset = self.polar.get_rectangular_coordinates()
                    path.lineTo(
                        (self.center_x + polar_offset[0]),
                        (self.center_y + polar_offset[1]),
                    )
                
                self.skia.canvas.drawPath(path, black_stroke)


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

                


