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

from utils import Utils
import threading
import time
import os


class Core():
    def __init__(self, context, controller, canvas, assets, fourier, ffmpeg, audio, mmvanimation):
        self.context = context
        self.controller = controller
        self.canvas = canvas
        self.assets = assets
        self.fourier = fourier
        self.ffmpeg = ffmpeg
        self.audio = audio
        self.mmvanimation = mmvanimation
        
        self.utils = Utils()

        self.ROOT = self.context.ROOT

    # Calls and starts threads 
    def start(self):

        debug_prefix = "[Core.start]"

        # Create the pipe write thread
        self.controller.threads["pipe_writer_loop"] = threading.Thread(target=self.ffmpeg.pipe_writer_loop)
        print(debug_prefix, "Created thread video.ffmpeg.pipe_writer_loop")
        
        # Start the threads, warn the user that the output is no more linear
        print(debug_prefix, "[WARNING] FROM NOW ON NO OUTPUT IS LINEAR AS THREADING STARTS")

        # For each thread, start them
        for thread in self.controller.threads:
            print(debug_prefix, "Starting thread: [\"%s\"]" % thread)
            self.controller.threads[thread].start()
        
        print(debug_prefix, "Started!!")

        self.testrun()

    def testrun(self):

        total_steps = int(self.context.duration * self.context.fps)

        print("Total steps:", total_steps)

        # Generate the assets
        self.assets.pygradienter("particles", 100, 100, 1)

        # Generate a Animation
        self.mmvanimation.generate()
        self.canvas.reset_canvas()

        # Next animation
        for this_step in range(0, total_steps):
            # print(" > Next step")

            this_step += self.context.offset_audio_before_in_many_steps

            if this_step >= total_steps - 1:
                this_step = total_steps - 1

            this_time = max(
                (1/self.context.fps) * this_step,
                0
            )

            this_time_sample = int(this_time * self.audio.info["sample_rate"])

            until = int(this_time_sample + self.context.batch_size)

            audio_slice = self.audio.data[0][this_time_sample:until]

            fft = self.fourier.fft(
                audio_slice,
                self.audio.info
            )

            self.mmvanimation.next(audio_slice, fft, this_step)
            self.ffmpeg.write_to_pipe(self.canvas.canvas)
            # self.canvas.canvas.save("data/canvas%s.png" % this_step)
            self.canvas.reset_canvas()

        self.ffmpeg.close_pipe()
