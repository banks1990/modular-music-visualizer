"""
===============================================================================

Purpose: Main package file for MMV where the main wrapper class is located

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

from mmv.mmv_generator import MMVParticleGenerator
from mmv.mmv_music_bar import MMVMusicBars
from mmv.mmv_generator import MMVGenerator
from mmv.pyskt.pyskt_main import PysktMain
from mmv.pygradienter import pygradienter
from mmv.common.cmn_utils import Utils
from mmv.mmv_image import MMVImage
from mmv.mmv_main import MMVMain
import uuid
import time
import sys
import os


# Main wrapper class for the end user, facilitates MMV in a whole
class mmv:

    # Start default configs, creates wrapper classes
    def __init__(self, watch_processing_video_realtime: bool=False) -> None:

        # Main class of MMV
        self.mmv = MMVMain()

        # Utilities
        self.utils = Utils()

        # Start MMV classes that main connects them, do not run
        self.mmv.setup()

        # Default options of performance and quality, 720p60
        self.quality()

        # Configuring options
        self.quality_preset = QualityPreset(self)
        self.audio_processing = AudioProcessingPresets(self)
        self.post_processing = self.mmv.canvas.configure

        # Has the user chosen to watch the processing video realtime?
        self.mmv.context.watch_processing_video_realtime = watch_processing_video_realtime

    # Execute MMV with the configurations we've done
    def run(self) -> None:
        self.mmv.run()

    # Define output video width, height and frames per second
    def quality(self, width: int=1280, height: int=720, fps: int=60, batch_size=2048) -> None:
        self.mmv.context.width = width
        self.mmv.context.height = height
        self.mmv.context.fps = fps
        self.mmv.context.batch_size = batch_size
        self.width = width
        self.height = height
        self.resolution = [width, height]
        self.mmv.canvas.create_canvas()
    
    def set_path(self, path, message="path"):
        path = self.utils.get_abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Input {message} does not exist {path}")
        return path

    # Set the input audio file, raise exception if it does not exist
    def input_audio(self, path: str) -> None:
        self.mmv.context.input_file = self.set_path(path)
    
    # Set the input audio file, raise exception if it does not exist
    def input_midi(self, path: str) -> None:
        self.mmv.context.input_midi = self.set_path(path)
    
    # Output path where we'll be saving the final video
    def output_video(self, path: str) -> None:
        path = self.utils.get_abspath(path)
        self.mmv.context.output_video = path
    
    def offset_audio_steps(self, steps=0):
        self.mmv.context.offset_audio_before_in_many_steps = steps

    # Set the assets dir
    def set_assets_dir(self, path: str) -> None:
        # Remove the last "/"", pathing intuition under MMV scripts gets easier
        if path.endswith("/"):
            path = path[:-1]
        path = self.utils.get_abspath(path)
        self.utils.mkdir_dne(path)
        self.assets_dir = path
        self.mmv.context.assets = path
    
    # # [ MMV Objects ] # #
    
    # Add a given object to MMVAnimation content on a given layer
    def add(self, item, layer: int=0) -> None:

        # Make layers until this given layer if they don't exist
        self.mmv.mmv_animation.mklayers_until(layer)

        # Check the type and add accordingly
        if self.utils.is_matching_type([item], [MMVImage]):
            self.mmv.mmv_animation.content[layer].append(item)
            
        if self.utils.is_matching_type([item], [MMVGenerator]):
            self.mmv.mmv_animation.generators.append(item)

    # Get a blank MMVImage object
    def image_object(self) -> None:
        return MMVImage(self.mmv)
    
    # Get a pygradienter object with many workers for rendering
    def pygradienter(self, workers=4):
        return pygradienter(workers=workers)
    
    # Get a blank MMVGenerator object
    def generator_object(self):
        return MMVGenerator(self.mmv)

    # # [ Utilities ] # #

    def random_file_from_dir(self, path):
        return self.utils.random_file_from_dir(path)
        
    def get_unique_id(self):
        return self.utils.get_hash(str(uuid.uuid4()))

    # # [ APPS ] # #
    def pyskt_test(self, *args, **kwargs):
        print(args, kwargs)
        return PysktMain(self.mmv, *args, **kwargs)


# Presets on width and height
class QualityPreset:

    # Get this file main mmv class
    def __init__(self, mmv) -> None:
        self.mmv = mmv
    
    # Standard definition, 480p @ 24 fps
    def sd24(self) -> None:
        self.mmv.main.context.width = 854 
        self.mmv.main.context.height = 480
        self.mmv.main.context.fps = 24
    
    # (old) HD definition, 720p @ 30 fps
    def hd30(self) -> None:
        self.mmv.main.context.width = 1280 
        self.mmv.main.context.height = 720
        self.mmv.main.context.fps = 30
    
    # Full HD definition, 1080p @ 60 fps
    def fullhd60(self) -> None:
        self.mmv.main.context.width = 1920 
        self.mmv.main.context.height = 1080
        self.mmv.main.context.fps = 60

    # Quad HD (4x720p) definition, 1440p @ 60 fps
    def quadhd60(self) -> None:
        self.mmv.main.context.width = 2560
        self.mmv.main.context.height = 1440
        self.mmv.main.context.fps = 60


# Presets on the audio processing, like how and where to apply FFTs, frequencies we want
class AudioProcessingPresets:

    # Get this file main mmv class
    def __init__(self, mmv: mmv) -> None:
        self.mmv = mmv
    
    # Custom preset, sends directly those dictionaries
    def preset_custom(self, config: dict) -> None:
        self.mmv.mmv.audio_processing.config = config

    # A balanced preset between the bass, mid and high frequencies
    # Good for general type of music
    def preset_balanced(self) -> None:
        self.mmv.mmv.audio_processing.config = {
            0: {
                "sample_rate": 440,
                "get_frequencies": "range",
                "start_freq": 40,
                "end_freq": 220,
                "nbars": "original",
            },

            1: {
                "sample_rate": 4000,
                "get_frequencies": "range",
                "start_freq": 220,
                "end_freq": 2000,
                "nbars": "original", #"300,max",
            },

            2: {
                "sample_rate": 32000,
                "get_frequencies": "range",
                "start_freq": 2000,
                "end_freq": 16000,
                "nbars": "fixed,200,max",
            },
        }
    
    # Get some bazz, som' mid freq
    # Good for heavy low frequencies music
    def preset_bass_mid(self) -> None:
        # self.mmv.main.audio_processing.config = {
        #     0: {
        #         "sample_rate": 4000,
        #         "get_frequencies": "range",
        #         "start_freq": 60,
        #         "end_freq": 2000,
        #         "nbars": "original",
        #     },
        # }

        self.mmv.mmv.audio_processing.config = {
            0: {
                "sample_rate": 1000,
                "get_frequencies": "range",
                "start_freq": 20,
                "end_freq": 500,
                "nbars": "original",
            },
            1: {
                "sample_rate": 1000,
                "get_frequencies": "range",
                "start_freq": 20,
                "end_freq": 500,
                "nbars": "original",
            },
           
        }
    
    def preset_musical_notes(self) -> None:
        self.mmv.mmv.audio_processing.config = {
            # 0: {
            #     "sample_rate": 40000,
            #     "get_frequencies": "musical",
            #     "start_freq": 20,
            #     "end_freq": 10000,
            #     "nbars": "original",
            # }
            0: {
                "sample_rate": 1000,
                "get_frequencies": "musical",
                "start_freq": 20,
                "end_freq": 500,
            },
            1: {
                "sample_rate": 40000,
                "get_frequencies": "musical",
                "start_freq": 500,
                "end_freq": 18000,
            }
        }

    def preset_dummy(self) -> None:
        self.mmv.mmv.audio_processing.config = {}
