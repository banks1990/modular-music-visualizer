"""
===============================================================================

Purpose: Main file initializer and core loop of a Pyskt for window

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

from mmv.pyskt.pyskt_draw_utils import SkiaDrawUtils
from mmv.pyskt.pyskt_context import PysktContext
from mmv.pyskt.pyskt_colors import PysktColors
from OpenGL import GL
import random
import skia
import glfw
import time


# The main code here I got from
# https://github.com/kyamagu/skia-python/issues/105

"""
kwargs:

{
    "context_window_name": "PySKT Window", window name
    "context_show_fps": False, log fps to console
    "context_wait_events": True, don't draw window at each update, only if mouse moved or key pressed
}
"""
class PysktMain:
    def __init__(self, mmv_main, *args, **kwargs):
        self.mmv_main = mmv_main
        self.pyskt_context = PysktContext(self, *args, **kwargs)
        self.draw_utils = SkiaDrawUtils(self)
        self.colors = PysktColors(self)
        
        # # # Make main window

        # Init GLFW        
        if not glfw.init():
            raise RuntimeError('glfw.init() failed')

        # Create window
        self.window = glfw.create_window(
            self.pyskt_context.width,
            self.pyskt_context.height,
            kwargs.get("context_window_name", "PySKT Window"),
            None, None,
        )

        # Make context, init surface
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        context = skia.GrContext.MakeGL()

        # GLFW config
        glfw.window_hint(glfw.STENCIL_BITS, 0)
        glfw.window_hint(glfw.DEPTH_BITS, 0)
        glfw.window_hint(glfw.DECORATED, False)

        # Set render to a display compatible
        backend_render_target = skia.GrBackendRenderTarget(
            self.pyskt_context.width,
            self.pyskt_context.height,
            0,  # sample count
            0,  # stencil bits
            skia.GrGLFramebufferInfo(0, GL.GL_RGBA8)
        )

        # Create draw surface
        self.surface = skia.Surface.MakeFromBackendRenderTarget(
            context, backend_render_target, skia.kBottomLeft_GrSurfaceOrigin,
            skia.kRGBA_8888_ColorType, skia.ColorSpace.MakeSRGB()
        )
        assert self.surface, 'Failed to create a surface'
        self.canvas = self.surface.getCanvas()

        # Where stuff is rendered from and activated

        self.components = {}

    # Run main loop of pyskt window
    def run(self):

        # Calculate fps?
        if self.pyskt_context.show_fps:
            frame_times = [0]*120
            frame = 0
            last_time_completed = time.time()

        # Loop until the user closes the window
        while not glfw.window_should_close(self.window):

            # Wait events if said to
            if self.pyskt_context.wait_events:
                glfw.wait_events()

            # Clear canvas
            self.canvas.clear(self.colors.background)
            
            # We have now to recursively search through the components dictionary

            self.draw_utils.anchored_text(
                canvas = self.canvas,
                text = "A Really long and centered text",
                x = self.pyskt_context.width // 2,
                y = self.pyskt_context.height // 2,
                anchor_x = 0.5,
                anchor_y = 0.5,
            )

            # # #

            # Show fps
            if self.pyskt_context.show_fps:
                frame_times[frame % 120] = time.time() - last_time_completed
                absolute_frame_times = [x for x in frame_times if not x == 0]
                fps = 1/(sum(absolute_frame_times)/len(absolute_frame_times))

                last_time_completed = time.time()
                frame += 1

                self.draw_utils.anchored_text(
                    canvas = self.canvas,
                    text = f"FPS: [{fps:.1f}]",
                    x = 0, y = 0,
                    anchor_x = 0,
                    anchor_y = 0,
                    # kwargs
                    font = skia.Font(skia.Typeface('Arial'), 12),
                )

            # Flush buffer
            self.surface.flushAndSubmit()

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

        # End glfw
        glfw.terminate()
