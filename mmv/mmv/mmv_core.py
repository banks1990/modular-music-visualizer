"""
===============================================================================

Purpose: Wrap and execute every MMV class

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

from mmv.common.cmn_types import *
import numpy as np
import threading
import time
import copy
import os


class Core:
    def __init__(self, mmv) -> None:
        self.mmv = mmv

    # Execute MMV, core loop
    def run(self) -> None:
        
        debug_prefix = "[Core.run]"

        # Create the pipe write thread
        self.pipe_writer_loop_thread = threading.Thread(
            target=self.mmv.ffmpeg.pipe_writer_loop,
            args=(self.mmv.audio.duration,)
        ).start()
        
        # How many steps is the audio duration times the frames per second
        self.total_steps = int(self.mmv.audio.duration * self.mmv.context.fps)
        self.mmv.context.total_steps = self.total_steps

        print(debug_prefix, "Total steps:", self.total_steps)

        # Init skia
        self.mmv.skia.init()

        # Update info that might have been changed by the user
        self.mmv.context.update_biases()

        # Next animation
        for this_step in range(0, self.total_steps):

            # The "raw" frame index we're at
            global_frame_index = this_step
            
            # # # [ Slice the audio ] # # #

            # Add the offset audio step (because interpolation isn't instant for smoothness)
            this_step += self.mmv.context.offset_audio_before_in_many_steps

            # If this step is out of bounds because the offset, set it to its max value
            if this_step >= self.total_steps - 1:
                this_step = self.total_steps - 1
            
            # The current time in seconds we're going to slice the audio based on its samplerate
            # If we offset to the opposite way, the starting point can be negative hence the max function.
            current_time = max( (1/self.mmv.context.fps) * this_step, 0 )

            self.mmv.context.current_time = (1/self.mmv.context.fps) * this_step

            # The current time in sample count to slice the audio
            this_time_in_samples = int(current_time * self.mmv.audio.sample_rate)

            # The slice starts at the this_time_in_samples and end the cut here
            until = int(this_time_in_samples + self.mmv.context.batch_size)

            # Slice the audio
            self.mmv.audio_processing.slice_audio(
                stereo_data = self.mmv.audio.stereo_data,
                mono_data = self.mmv.audio.mono_data,
                sample_rate = self.mmv.audio.sample_rate,
                start_cut = this_time_in_samples,
                end_cut = until,
                batch_size = self.mmv.context.batch_size
            )

            # # # [ Calculate the FFTs ] # # #

            process = [
                # For each sliced channel data we have, process that into the FFTs list
                self.mmv.audio_processing.process(channel_data, self.mmv.audio.sample_rate)
                for channel_data in self.mmv.audio_processing.audio_slice
            ]

            # The fftinfo, or call it "current time audio info", couldn't think a better var name
            fftinfo = {
                "average_value": self.mmv.audio_processing.average_value,
                "fft": [x["fft"] for x in process],
                "frequencies": [x["frequencies"] for x in process],
            }

            # # # [ Next steps ] # # #

            # Reset skia canvas
            self.mmv.skia.reset_canvas()

            # Process next animation with audio info and the step count to process on
            self.mmv.mmv_animation.next(fftinfo, this_step)

            # Next image to pipe
            next_image = self.mmv.skia.canvas_array()

            # Save current canvas's Frame to the final video
            self.mmv.ffmpeg.write_to_pipe(global_frame_index, next_image)

            # [ FAILSAFE ] Reset the canvas (not needed if full background is present (recommended))
            self.mmv.canvas.reset_canvas()
    
        # End pipe
        self.mmv.ffmpeg.close_pipe()
