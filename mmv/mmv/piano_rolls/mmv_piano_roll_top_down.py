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
from mmv.common.cmn_utils import DataUtils
from PIL import ImageColor
import numpy as np
import random
import math
import skia


class PianoKey:
    def __init__(self, midi, skia_object, background_color):
        self.midi = midi
        self.skia = skia_object
        self.background_color = background_color

        # Key info
        self.key_index = None
        self.name = ""

        # Position, states
        self.center_x = None
        self.width = None
        self.height = None
        self.resolution_height = None
        self.active = False

        self.MARKER = True

    # Configure PianoKey by midi key index
    def by_key_index(self, key_index):
        self.note = key_index
        self.name = self.midi.note_to_name(self.note)
        self.configure_color()
        print("by key index", key_index, self.name)
    
    # Configure pressed, idle colors based on key name
    def configure_color(self):

        c = min(self.background_color + (40/255), 1)
        self.marker_color = skia.Color4f(c, c, c, 0.1)

        c = min(self.background_color + (60/255), 1)
        self.marker_color_subtle_brighter = skia.Color4f(c, c, c, 0.3)

        # Note is a sharp key, black idle, gray on press
        if "#" in self.name:
            self.color_active = skia.Color4f(0, 0, 0, 1)
            self.color_idle = skia.Color4f(0.2, 0.2, 0.2, 1)
            self.is_white = False
            self.is_black = True
        else:
            self.color_active = skia.Color4f(0.7, 0.7, 0.7, 1)
            self.color_idle = skia.Color4f(1, 1, 1, 1)
            self.is_white = True
            self.is_black = False

    # Draw this key
    def draw(self, notes_playing):

        if self.is_black:
            away = (self.height * (0.33))
        else:
            away = 0

        coords = [
            self.center_x - (self.width / 2),
            self.resolution_height - self.height,
            self.center_x + (self.width / 2),
            self.resolution_height - away,
        ]

        self.active = self.note in notes_playing

        if self.active:
            color = self.color_active
        else:
            color = self.color_idle

        # Make the skia Paint and
        paint = skia.Paint(
            AntiAlias = True,
            Color = color,
            Style = skia.Paint.kFill_Style,
            StrokeWidth = 2,
        )

        border = skia.Paint(
            AntiAlias = True,
            Color = skia.Color4f(0, 0, 0, 1),
            Style = skia.Paint.kStroke_Style,
            StrokeWidth = 2,
        )

        # Rectangle border
        rect = skia.Rect(*coords)
        
        # Draw the border
        self.skia.canvas.drawRect(rect, paint)
        self.skia.canvas.drawRect(rect, border)
    
    def draw_marker(self):
        if self.MARKER and self.is_black:
            if "G" in self.name:
                color = self.marker_color_subtle_brighter
            else:
                color = self.marker_color

            marker = skia.Paint(
                AntiAlias = True,
                Color = color,
                Style = skia.Paint.kFill_Style,
                # StrokeWidth = 2,
            )

            rect = skia.Rect(
                max(self.center_x - (self.width / 10), 1),
                0,
                max(self.center_x + (self.width / 10), 1),
                self.resolution_height - self.height
            )
            self.skia.canvas.drawRect(rect, marker)

    
class MMVPianoRollTopDown:
    def __init__(self, MMVVectorial, context, skia_object, midi):
        self.vectorial = MMVVectorial
        self.context = context
        self.skia = skia_object
        self.midi = midi
        self.config = self.vectorial.config
        self.functions = Functions()
        self.datautils = DataUtils()
        self.piano_keys = {}
        self.keys_centers = {}

        self.background_color = 22/255
    
    # Bleed is extra keys you put at the lower most and upper most ranged keys
    def generate_piano(self, min_note, max_note, bleed=3):

        # NOTE: EDIT HERE STATIC VARIABLES  TODO: set them on config
        self.piano_height = (3.5/19) * self.vectorial.context.height
        self.viewport_height = self.vectorial.context.height - self.piano_height

        # TODO: set these variables in config
        self.seconds_of_midi_content = 3

        for key_index in range(min_note - bleed, max_note + bleed):
            next_key = PianoKey(self.midi, self.skia, self.background_color)
            next_key.by_key_index(key_index)
            self.piano_keys[key_index] = next_key

        print(len(self.piano_keys.keys()))
        
        # We get the center of keys based on the "distance walked" in between intervals
        # As black keys are in between two white keys, we walk half white key width on those
        # and a full white key between E and F, B and C.

        divisions = 0

        for index, key_index in enumerate(self.piano_keys.keys()):

            key = self.piano_keys[key_index]
            
            # First index of key can't compare to previous key, starts at current_center
            if not index == 0:

                prevkey = self.piano_keys[key_index - 1]

                # Distance is a tone
                if (prevkey.is_white) and (key.is_white):
                    divisions += 2

                # Distance is a semitone
                else:
                    divisions += 1


        # for key_index in self.piano_keys.keys():
        #     if "#" in self.piano_keys[key_index].name:
        #         divisions += 1
        #     else:
        #         divisions += 2
            
        # Now we have the divisions, we can calculate the real key width based on the resolution

        # print("width", self.vectorial.context.width)

        # The keys intervals for walking
        self.semitone_width = self.vectorial.context.width / divisions
        self.tone_width = self.semitone_width * 2

        # print(self.semitone_width, self.tone_width, divisions)
        # exit()

        # Current center we're at
        current_center = 0

        for index, key_index in enumerate(self.piano_keys.keys()):

            key = self.piano_keys[key_index]
            
            # First index of key can't compare to previous key, starts at current_center
            if not index == 0:

                prevkey = self.piano_keys[key_index - 1]

                # Distance is a tone
                if (prevkey.is_white) and (key.is_white):
                    current_center += self.tone_width

                # Distance is a semitone
                else:
                    current_center += self.semitone_width

            # Set the 
            if key.is_white:
                this_note_width = self.tone_width
            else:
                this_note_width = (4/6) * self.tone_width

            self.piano_keys[key_index].width = this_note_width
            self.piano_keys[key_index].height = self.piano_height
            self.piano_keys[key_index].resolution_height = self.vectorial.context.height
            self.piano_keys[key_index].center_x = current_center

            self.keys_centers[key_index] = current_center

    def draw_piano(self):
        for key_index in self.piano_keys.keys():
            if self.piano_keys[key_index].is_white:
                self.piano_keys[key_index].draw(self.notes_playing)

        for key_index in self.piano_keys.keys():
            if self.piano_keys[key_index].is_black:
                self.piano_keys[key_index].draw(self.notes_playing)
            
    def draw_markers(self):

        c = 0.35
        white_white_color = skia.Color4f(c, c, c, 1)

        white_white_paint = skia.Paint(
            AntiAlias = True,
            Color = white_white_color,
            Style = skia.Paint.kStroke_Style,
            StrokeWidth = 1,
        )

        current_center = 0

        for index, key_index in enumerate(self.piano_keys.keys()):
            key = self.piano_keys[key_index]
            if not index == 0:
                prevkey = self.piano_keys[key_index - 1]
                if (prevkey.is_white) and (key.is_white):
                    current_center += self.tone_width
                    rect = skia.Rect(
                        current_center - self.semitone_width,
                        0,
                        current_center + 1 - self.semitone_width,
                        self.vectorial.context.height
                    )
                    self.skia.canvas.drawRect(rect, white_white_paint)
                else:
                    current_center += self.semitone_width

        for key_index in self.piano_keys.keys():
            self.piano_keys[key_index].draw_marker()

    def draw_note(self, velocity, start, end, channel, note, name):

        color_channels = {
            0: {
                "plain": ImageColor.getcolor("#ffcc00", "RGB"),
                "sharp": ImageColor.getcolor("#ff9d00", "RGB"),
            },
            1: {
                "plain": ImageColor.getcolor("#00ff0d", "RGB"),
                "sharp": ImageColor.getcolor("#00a608", "RGB"),
            },
            2: {
                "plain": ImageColor.getcolor("#6600ff", "RGB"),
                "sharp": ImageColor.getcolor("#39008f", "RGB"),
            },
            3: {
                "plain": ImageColor.getcolor("#ff0000", "RGB"),
                "sharp": ImageColor.getcolor("#990000", "RGB"),
            },
            4: {
                "plain": ImageColor.getcolor("#00fffb", "RGB"),
                "sharp": ImageColor.getcolor("#00b5b2", "RGB"),
            },
            5: {
                "plain": ImageColor.getcolor("#ff006f", "RGB"),
                "sharp": ImageColor.getcolor("#a10046", "RGB"),
            },
            6: {
                "plain": ImageColor.getcolor("#aaff00", "RGB"),
                "sharp": ImageColor.getcolor("#75b000", "RGB"),
            },

            7: {
                "plain": ImageColor.getcolor("#e1ff00", "RGB"),
                "sharp": ImageColor.getcolor("#a9bf00", "RGB"),
            },
            8: {
                "plain": ImageColor.getcolor("#ff3300", "RGB"),
                "sharp": ImageColor.getcolor("#a82200", "RGB"),
            },
            9: {
                "plain": ImageColor.getcolor("#00ff91", "RGB"),
                "sharp": ImageColor.getcolor("#00b567", "RGB"),
            },
            10: {
                "plain": ImageColor.getcolor("#ff00aa", "RGB"),
                "sharp": ImageColor.getcolor("#c40083", "RGB"),
            },
            11: {
                "plain": ImageColor.getcolor("#c800ff", "RGB"),
                "sharp": ImageColor.getcolor("#8e00b5", "RGB"),
            },
            12: {
                "plain": ImageColor.getcolor("#00ff4c", "RGB"),
                "sharp": ImageColor.getcolor("#00c93c", "RGB"),
            },
            13: {
                "plain": ImageColor.getcolor("#ff8a8a", "RGB"),
                "sharp": ImageColor.getcolor("#bf6767", "RGB"),
            },
            14: {
                "plain": ImageColor.getcolor("#ffde7d", "RGB"),
                "sharp": ImageColor.getcolor("#c4aa5e", "RGB"),
            },
            15: {
                "plain": ImageColor.getcolor("#85ebff", "RGB"),
                "sharp": ImageColor.getcolor("#5ca7b5", "RGB"),
            },
            16: {
                "plain": ImageColor.getcolor("#ff7aa4", "RGB"),
                "sharp": ImageColor.getcolor("#bd5978", "RGB"),
            },

            "default": {
                "plain": ImageColor.getcolor("#dddddd", "RGB"),
                "sharp": ImageColor.getcolor("#ffffff", "RGB"),
            },
        }

        note_colors = color_channels.get(channel, color_channels["default"])
        
        if "#" in name:
            width = self.semitone_width*0.9
            c = note_colors["sharp"]
            color = skia.Color4f(c[0]/255, c[1]/255, c[2]/255, 1)

        else:
            width = self.tone_width*0.6
            c = note_colors["plain"]
            color = skia.Color4f(c[0]/255, c[1]/255, c[2]/255, 1)

        # Make the skia Paint and
        paint = skia.Paint(
            AntiAlias = True,
            Color = color,
            Style = skia.Paint.kFill_Style,
            # Shader=skia.GradientShader.MakeLinear(
            #     points=[(0.0, 0.0), (self.vectorial.context.width, self.vectorial.context.height)],
            #     colors=[skia.Color4f(0, 0, 1, 1), skia.Color4f(0, 1, 0, 1)]),
            StrokeWidth = 2,
        )

        # c = ImageColor.getcolor("#d1ce1d", "RGB") 
        c = (0, 0, 0)
        border = skia.Paint(
            AntiAlias = True,
            Color = skia.Color4f(c[0]/255, c[1]/255, c[2]/255, 1),
            Style = skia.Paint.kStroke_Style,
            # ImageFilter=skia.ImageFilters.DropShadow(3, 3, 5, 5, skia.ColorBLUE),
            # MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 2.0),
            StrokeWidth = max(self.vectorial.context.resolution_ratio_multiplier * 2, 1),
        )
        
        x = self.keys_centers[note]

        y = self.functions.proportion(
            self.seconds_of_midi_content,
            self.viewport_height, #*2,
            self.vectorial.context.current_time - start
        )

        height = self.functions.proportion(
            self.seconds_of_midi_content,
            self.viewport_height,
            end - start
        ) 

        coords = [
            x - (width / 2),
            y + (self.viewport_height) - height,
            x + (width / 2),
            y + (self.viewport_height),
        ]

        # Rectangle border
        rect = skia.Rect(*coords)
        
        # Draw the border
        self.skia.canvas.drawRect(rect, paint)
        self.skia.canvas.drawRect(rect, border)


    # Build, draw the bar
    def build(self, fftinfo, this_step, config, effects):

        c = self.background_color
        self.skia.canvas.clear(skia.Color4f(c, c, c, 1))
        self.seconds_of_midi_content = config["seconds-of-midi-content"]
        SECS_OFFSET = config["seconds-offset"]

        self.draw_markers()

        # Get "needed" variables
        current_time = self.vectorial.context.current_time + SECS_OFFSET
        resolution_ratio_multiplier = self.vectorial.context.resolution_ratio_multiplier

        # contents = self.datautils.dictionary_items_in_between(
        #     self.midi.timestamps,
        #     current_time - 2,
        #     current_time + self.seconds_of_midi_content * 2
        # )

        accept_minimum_time = current_time - self.seconds_of_midi_content
        accept_maximum_time = current_time + self.seconds_of_midi_content

        self.notes_playing = []

        for channel in self.midi.timestamps.keys():
            for key in self.midi.timestamps[channel]:
                if isinstance(key, int):

                    note = key
                    times = self.midi.timestamps[channel][note]["time"]
                    delete = []

                    for index, interval in enumerate(times):

                        # Out of bounds
                        if interval[1] < accept_minimum_time:
                            delete.append(index)
                            continue
                        
                        if interval[0] > accept_maximum_time:
                            break

                        current_time_in_interval = (interval[0] < current_time < interval[1])
                        accepted_render = (accept_minimum_time < current_time < accept_maximum_time)

                        if current_time_in_interval:
                            self.notes_playing.append(note)

                        if current_time_in_interval or accepted_render:
                            self.draw_note(
                                velocity = 128,
                                start = interval[0] - SECS_OFFSET,
                                end = interval[1] - SECS_OFFSET,
                                channel = channel,
                                note = note,
                                name = self.midi.note_to_name(note),
                            )
                    
                    for index in reversed(delete):
                        del self.midi.timestamps[channel][note]["time"][index]


        self.draw_piano()