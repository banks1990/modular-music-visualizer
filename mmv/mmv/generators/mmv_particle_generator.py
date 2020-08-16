"""
===============================================================================

Purpose: MMV objects generators

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
# modifier activators
from mmv.modifier_activators.ma_fade import *

from mmv.common.cmn_interpolation import Interpolation
from mmv.mmv_interpolation import MMVInterpolation
from mmv.mmv_music_bar import MMVMusicBars
from mmv.common.cmn_utils import Utils
from mmv.mmv_image import MMVImage
from mmv.mmv_modifiers import *
import random
import copy
import math
import os


class MMVParticleGeneratorConfigure:
    def __init__(self, mmvgenerator):
        self.mmvgenerator = mmvgenerator
    
    def preset_bottom_mid_top(self):
        self.mmvgenerator.generate_function = self.mmvgenerator.preset_bottom_mid_top
    
    def preset_middle_out(self):
        self.mmvgenerator.generate_function = self.mmvgenerator.preset_middle_out



class MMVParticleGenerator():
    def __init__(self, context, skia_object):
        self.context = context
        self.skia = skia_object
        self.utils = Utils()
        self.interpolation = Interpolation()
        self.configure = MMVParticleGeneratorConfigure(self)
        self.type = "mmvgenerator"
        self.generate_function = False

        self.is_deletable = False

    # Duck typing, this doesn't do anything
    def blit(self, _):
        pass
    def resolve_pending(self):
        pass

    def next(self, fftinfo, this_step):
        if this_step % 10 == 0:
            return {
                "object": self.generate_function(),
                "layer": 3
            }
        return {"object": None}
    
    def preset_bottom_mid_top(self):

        resolution_ratio_multiplier = self.context.resolution_ratio_multiplier

        particle = MMVImage(self.context, self.skia)

        particle.image.load_from_path(
            self.utils.random_file_from_dir (
                self.context.assets + os.path.sep + "particles"
            )
        )
        
        horizontal_randomness = int(50 * resolution_ratio_multiplier)
        vertical_randomness_min = self.context.height//1.7
        vertical_randomness_max = self.context.height//2.3

        x1 = random.randint(0, self.context.width)
        y1 = self.context.height
        x2 = x1 + random.randint(-horizontal_randomness, horizontal_randomness)
        y2 = y1 + random.randint(-vertical_randomness_min, -vertical_randomness_max)
        x3 = x2 + random.randint(-horizontal_randomness, horizontal_randomness)
        y3 = y2 + random.randint(-vertical_randomness_min, -vertical_randomness_max)

        particle_shake = MMVModifierShake(
            interpolation_x = MMVInterpolation({
                "function": "remaining_approach",
                "aggressive": 0.01,
                "start": 0,
            }),
            interpolation_y = MMVInterpolation({
                "function": "remaining_approach",
                "aggressive": 0.04,
                "start": 0,
            }),
            distance = 18,
            mode = ModifierMode.OFFSET_VALUE,
        )

        fast = 0.04
        fade_intensity = random.uniform(0.1, 0.7)

        this_steps = random.randint(50, 100)
        particle.animation[0] = {
            "position": {
                "path": [
                    MMVModifierLine(
                        start = (x1, y1),
                        end = (x2, y2),
                        interpolation_x = MMVInterpolation({
                            "function": "remaining_approach",
                            "aggressive": fast,
                        }),
                        interpolation_y = MMVInterpolation({
                            "function": "remaining_approach",
                            "aggressive": fast,
                        }),
                        mode = ModifierMode.OVERRIDE_VALUE_RESET_OFFSET,
                    ),
                    particle_shake
                ],
            },
            "animation": {
                "steps": this_steps,
            },
            "modules": {
                "fade": {
                    "object": MMVModifierFade(
                        interpolation = MMVInterpolation({
                            "function": "linear",
                            "total_steps": 30,
                            "start": 0,
                            "end": fade_intensity,
                        })
                    )
                }
            }
        }
        
        this_steps = random.randint(150, 200)
        particle.animation[1] = {
            "position": {
                "path": [
                    MMVModifierLine(
                        start = (x2, y2),
                        end = (x3, y3),
                        interpolation_x = MMVInterpolation({
                            "function": "remaining_approach",
                            "aggressive": fast,
                        }),
                        interpolation_y = MMVInterpolation({
                            "function": "remaining_approach",
                            "aggressive": fast,
                        }),
                        mode = ModifierMode.OVERRIDE_VALUE_RESET_OFFSET,
                    ),
                    particle_shake
                ],
            },
            "animation": {
                "steps": this_steps
            },
            "modules": {
                "fade": {
                    "object": MMVModifierFade(
                        interpolation = MMVInterpolation({
                            "function": "linear",
                            "total_steps": 30,
                            "start": fade_intensity,
                            "end": 0,
                        })
                    )
                }
            }
        }

        particle.image.resize_by_ratio(
            random.uniform(0.1 * resolution_ratio_multiplier, 0.3 * resolution_ratio_multiplier),
            override=True
        )

        return particle



    def preset_middle_out(self):

        particle = MMVImage(self.context, self.skia)

        particle.image.load_from_path(
            self.utils.random_file_from_dir (
                self.context.assets + os.path.sep + "particles"
            )
        )
        
        horizontal_randomness = int(50 * resolution_ratio_multiplier)
        vertical_randomness_min = self.context.height//1.7
        vertical_randomness_max = self.context.height//2.3

        half_screen_x = self.context.width // 2
        half_screen_y = self.context.height // 2

        x1 = half_screen_x
        y1 = half_screen_y

        x2 = x1 + random.randint(-half_screen_x*2, half_screen_x*2)
        y2 = y1 + random.randint(-half_screen_y*2, half_screen_y*2)

        particle_shake = MMVModifierShake(
            interpolation_x = MMVInterpolation({
                "function": "remaining_approach",
                "aggressive": 0.01,
                "start": 0,
            }),
            interpolation_y = MMVInterpolation({
                "function": "remaining_approach",
                "aggressive": 0.04,
                "start": 0,
            }),
            distance = 18,
            mode = ModifierMode.OFFSET_VALUE,
        )

        fast = 0.05
        fade_intensity = random.uniform(0.1, 0.7)

        this_steps = 2

        particle.animation[0] = {
            "position": {
                "path": [
                    MMVModifierPoint(
                        x = x1, y = y1,
                        mode = ModifierMode.OVERRIDE_VALUE_RESET_OFFSET
                    )
                ],
            },
            "animation": {
                "steps": this_steps,
            },
            "modules": {
                "fade": {
                    "object": MMVModifierFade(
                        interpolation = MMVInterpolation({
                            "function": "linear",
                            "total_steps": 30,
                            "start": 0,
                            "end": fade_intensity,
                        })
                    )
                }
            }
        }

        this_steps = random.randint(50, 100)

        particle.animation[0] = {
            "position": {
                "path": [
                    MMVModifierLine(
                        start = (x1, y1),
                        end = (x2, y2),
                        interpolation_x = MMVInterpolation({
                            "function": "remaining_approach",
                            "aggressive": fast,
                        }),
                        interpolation_y = MMVInterpolation({
                            "function": "remaining_approach",
                            "aggressive": fast,
                        }),
                        mode = ModifierMode.OVERRIDE_VALUE_RESET_OFFSET,
                    ),
                    particle_shake
                ],
            },
            "animation": {
                "steps": this_steps,
            },
            "modules": {
                "fade": {
                    "object": MMVModifierFade(
                        interpolation = MMVInterpolation({
                            "function": "linear",
                            "total_steps": 30,
                            "start": fade_intensity,
                            "end": 0,
                        })
                    )
                }
            }
        }
        

        particle.image.resize_by_ratio(
            random.uniform(0.1  * resolution_ratio_multiplier, 0.3  * resolution_ratio_multiplier),
            override=True
        )

        return particle