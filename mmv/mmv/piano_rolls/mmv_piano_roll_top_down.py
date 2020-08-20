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


class PianoKey:
    def __init__(self, midi):
        self.midi = midi

        # Key info
        self.key_index = None
        self.name = ""

        # Position, states
        self.center_x = None
        self.width = None
        self.height = None
        self.active = False

    # Configure PianoKey by midi key index
    def by_key_index(self, key_index):
        self.key_index = key_index
        self.name = self.midi.note_to_name(key_index)
        self.configure_color()
    
    # Configure pressed, idle colors based on key name
    def configure_color(self):
        # Note is a sharp key, black idle, gray on press
        if "#" in self.name:
            self.color_pressed = skia.Color4f(0.2, 0.2, 0.2, 1)
            self.color_idle = skia.Color4f(0, 0, 0, 1)
        else:
            self.color_pressed = skia.Color4f(0.7, 0.7, 0.7, 1)
            self.color_idle = skia.Color4f(1, 1, 1, 1)


    
class MMVPianoRollTopDown:
    def __init__(self, MMVVectorial, context, skia_object, midi):
        self.vectorial = MMVVectorial
        self.context = context
        self.skia = skia_object
        self.midi = midi
        self.config = self.vectorial.config
        self.functions = Functions()
        self.piano_keys = {}
    
    # Bleed is extra keys you put at the lower most and upper most ranged keys
    def generate_piano(self, min_note, max_note, bleed=2):
        for key_index in range(min_note - bleed, max_note + bleed):
            next_key = PianoKey(self.midi)
            next_key.by_key_index(key_index)
            self.piano_keys[key_index] = next_key
    
    def draw_note(self, info):
        pass

    # Build, draw the bar
    def build(self, fftinfo, this_step, config, effects):

        # Get "needed" variables
        current_time = self.vectorial.context.current_time
        resolution_ratio_multiplier = self.vectorial.context.resolution_ratio_multiplier

        # TODO: set these variables in config
        seconds_of_midi_content = 5


