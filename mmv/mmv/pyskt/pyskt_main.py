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

from mmv.mmv.pyskt.pyskt_context import PysktContext
from OpenGL import GL
import skia
import glfw
import time
import random


# The main code here I got from
# https://github.com/kyamagu/skia-python/issues/105

"""
Init kwargs: dictionary

{
    "name": window name
    "show_fps": log fps to console
    "wait_events": don't draw window at each update, only if mouse moved or key pressed
}
"""
class PysktMain:
    def __init__(self, main, **kwargs):
        self.main = main
        self.pyskt_context = PysktContext(kwargs)
        
        # # # Make main window

        # GLFW config
        glfw.window_hint(glfw.STENCIL_BITS, 0)
        glfw.window_hint(glfw.DEPTH_BITS, 0)
        glfw.window_hint(glfw.DECORATED, False)

        # Init GLFW        
        if not glfw.init():
            raise RuntimeError('glfw.init() failed')

        # Create window
        self.window = glfw.create_window(
            self.pyskt_context.width,
            self.pyskt_context.height,
            kwargs.get("name", "Pyskt Window"),
            None,
            None,
        )

        # Make context, init surface
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        context = skia.GrContext.MakeGL()

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
        self.run()

    # Run main loop of pyskt window
    def run(self):

        # Calculate fps?
        if self.pyskt_context.show_fps:
            start = time.time()
            frames = 1

        # Loop until the user closes the window
        while not glfw.window_should_close(self.window):

            # Wait events if said to
            if self.pyskt_context.wait_events:
                glfw.wait_events()

            # Clear canvas
            self.canvas.clear(skia.ColorBLACK)

            
            # We have now to recursively search through the components dictionary


            # # #

            # Flush buffer
            self.surface.flushAndSubmit()

            # Swap front and back buffers
            glfw.swap_buffers(self.window)

            # Poll for and process events
            glfw.poll_events()

            # Show fps
            if self.pyskt_context.show_fps:
                frames += 1
                print("fps: ", frames / (time.time() - start) )

        # End glfw
        glfw.terminate()
