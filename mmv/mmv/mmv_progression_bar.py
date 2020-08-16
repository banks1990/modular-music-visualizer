"""
===============================================================================

Purpose: MMVMusicBars object

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


from mmv.mmv_progression_bars.mmv_progression_bar_rectangle import MMVProgressionBarRectangle
from mmv.common.cmn_coordinates import PolarCoordinates
from mmv.common.cmn_interpolation import Interpolation
from mmv.common.cmn_functions import Functions
from mmv.common.cmn_functions import FitIndex
from mmv.common.cmn_skia import SkiaWrapper
from mmv.common.cmn_frame import Frame
from mmv.common.cmn_utils import Utils
from mmv.mmv_modifiers import *
from resampy import resample
import random
import math
import os


class MMVProgressionBar:
    def __init__(self, context, config: dict, skia_object) -> None:
        
        debug_prefix = "[MMVMusicBars.__init__]"
        
        self.context = context
        self.config = config
        self.skia = skia_object

        self.functions = Functions()
        self.utils = Utils()

        self.path = {}

        self.x = 0
        self.y = 0
        self.size = 1
        self.is_deletable = False
        self.offset = [0, 0]

        self.image = Frame()

        # We have different files with different classes of ProgressionBars

        # Simple, rectangle bar
        if self.config["type"] == "rectangle":
            self.builder = MMVProgressionBarRectangle(self, self.context, self.skia)

    # Call builder for drawing directly on the canvas
    def next(self, fftinfo, this_step, effects):
        self.builder.build(fftinfo, this_step, self.config, effects)

  