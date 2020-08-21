"""
===============================================================================

Purpose: Basic usage example of MMV

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

"""
# # # [ IMPORTANT ] # # #

When setting coordinates like path points, the reference is the following:

Center (0, 0) is at the top left corner of the video,
and the "object" position is at the top left corner of its image as well

X increases rightwards
Y increases downwards
"""

# Import MMV module
import mmv

# Create the wrapper class
processing = mmv.mmv(
    watch_processing_video_realtime=False
)

# Set the video quality
processing.quality(
    width=1920,
    height=1080,
    fps=60
)

processing.offset_audio_steps(0)

# If you want to create some assets, set the assets dir first !!
processing.assets_dir("assets/free_assets")

# I/O options, input a audio, output a video
processing.audio_processing.preset_dummy()
processing.input_audio("assets/piano_roll/contingency-times.ogg")
processing.input_midi("assets/piano_roll/contingency-times.mid")
processing.output_video("mmv-output.mkv")

piano_roll = processing.image_object()
piano_roll.configure.init_animation_layer()
piano_roll.configure.simple_add_piano_roll(
    seconds_offset = 0,
    bpm = 130
)

processing.add(piano_roll, layer=1)

# Run and generate the final video
processing.run()
