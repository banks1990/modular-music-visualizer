"""
===============================================================================

Purpose: Wrapper for MMV modules that write directly to the canvas like
the visualizer bars, progression bar

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

from mmv.mmv_progression_bar import MMVProgressionBar
from mmv.mmv_piano_roll import MMVPianoRoll
from mmv.mmv_music_bar import MMVMusicBars


class MMVVectorial:
    def __init__(self, mmv, config: dict) -> None:
        self.mmv = mmv
        self.config = config

        # Visualizer bars
        if self.config["type_class"] == "visualizer":
            self.next_object = MMVMusicBars(
                context = self.mmv.context,
                config = self.config,
                skia_object = self.mmv.skia,
            )
        
        # Progression bar object
        if self.config["type_class"] == "progression-bar":
            self.next_object = MMVProgressionBar(
                context = self.mmv.context,
                config = self.config,
                skia_object = self.mmv.skia,
            )
        
        # Progression bar object
        if self.config["type_class"] == "piano-roll":
            self.next_object = MMVPianoRoll(
                context = self.mmv.context,
                config = self.config,
                skia_object = self.mmv.skia,
            )

    # Next function
    def next(self, fftinfo, this_step, effects):
        self.next_object.next(
            fftinfo = fftinfo,
            this_step = this_step,
            effects = effects
        )