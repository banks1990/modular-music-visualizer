"""
===============================================================================

Purpose: MMVPianoRoll object for MIDI visualization

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

from mmv.piano_rolls.mmv_piano_roll_top_down import MMVPianoRollTopDown
from mmv.common.cmn_midi import MidiFile
from mmv.common.cmn_utils import Utils


class MMVPianoRoll:
    def __init__(self, context, config: dict, skia_object) -> None:
        
        debug_prefix = "[MMVPianoRoll.__init__]"
        
        self.context = context
        self.config = config
        self.skia = skia_object

        self.utils = Utils()

        self.is_deletable = False
        self.offset = [0, 0]

        self.midi = MidiFile()
        self.midi.load(self.context.input_midi)
        self.midi.get_timestamps()

        # We have different files with different classes of PianoRolls

        # Simple, rectangle bar
        if self.config["type"] == "top-down":
            self.builder = MMVPianoRollTopDown(self, self.context, self.skia, self.midi)

        self.builder.generate_piano(self.midi.range_notes.min, self.midi.range_notes.max)

    # Call builder for drawing directly on the canvas
    def next(self, fftinfo, this_step, effects):
        self.builder.build(fftinfo, this_step, self.config, effects)
