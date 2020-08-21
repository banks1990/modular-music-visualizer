"""
===============================================================================

Purpose: MIDI file utilities for reading, organizing, sorting information

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

from mmv.common.cmn_types import InlineDict
import mido


# Store the range of notes for a (possible) piano roll visualization if user
# choses only to show range of played keys, helps visualization on smaller screens
class RangeNotes:
    def __init__(self):
        self.min = -1
        self.max = -1
    
    # Update min and max variables based on a new note index
    def update(self, new_note):
        # First call, set max and min to incoming note
        if self.min == -1 and self.max == -1:
            self.max = new_note
            self.min = new_note
            return
        # Check if eiter is below or above, update corresponding variable
        if self.max < new_note:
            self.max = new_note
        if new_note < self.min:
            self.min = new_note



# Wrapper and utilities for mido interface, processing MIDI files.
class MidiFile:
    def load(self, path):
        self.midi = mido.MidiFile(path, clip=True)
        self.time = 0
        self.tempo = 120
        self.range_notes = RangeNotes()
    
    # Midi note index (number) to name -> "C3", "A#4", F5, etc
    def note_to_name(self, n):
        # 69 -> A4
        # 60 -> C4
        letters = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = str((n // 12) - 1)
        letter = letters[(n + 60) % 12]
        return letter + octave

    # Create empty list on timestamp with current time
    def create_empty_timestamp_list(self):
        if not self.time in self.timestamps:
            self.timestamps[self.time] = []

    # Basically, MIDI information -> timestamps dictionary
    # Really finicky because how MIDI works on the ticks and channels and whatnot
    def get_timestamps(self):

        # Timestamps dictionary and "ongoing" midi notes, not finished        
        self.timestamps = {}
        ongoing = {}

        # Iterate through each message on ALL midi tracks together...
        # Use synchronous mode if possible TODO: right loop for every mode
        for msg in mido.merge_tracks(self.midi.tracks):
           
            # Convert message time from absolute time
            # in ticks to relative time in seconds.
            if msg.time > 0:
                delta = mido.tick2second(msg.time, self.midi.ticks_per_beat, self.tempo)
            else:
                delta = 0
            
            # Add to current time the delta based on tempo
            self.time += delta

            print("\n\n", self.time)

            # Message is a note we play or release (or weirdly play at zero velocity for releasing)
            if msg.type in ["note_on", "note_off"]:
                
                self.create_empty_timestamp_list()
                velocity = msg.velocity
                note = msg.note

                self.range_notes.update(note)

                if note in ongoing.keys():
                    self.timestamps[self.time].append(InlineDict({
                        "type": "note",
                        "start": ongoing[note].start,
                        "end": self.time,
                        "velocity": velocity,
                        "note": note,
                        "name": self.note_to_name(note),
                    }))
                    print(ongoing[note].start, self.time)

                    del ongoing[note]
                else:
                    ongoing[note] = InlineDict({
                        "start": self.time,
                        "velocity": velocity,
                        "note": note,
                    })
                
                print(ongoing)

            if msg.type == 'set_tempo':
                self.create_empty_timestamp_list()
                self.tempo = msg.tempo

                self.timestamps[self.time].append(InlineDict({
                    "type": "tempo",
                    "value": self.tempo,
                }))

       
        # print(self.timestamps)
        print("Range:", self.range_notes.min, self.range_notes.max)