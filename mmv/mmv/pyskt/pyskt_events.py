"""
===============================================================================

Purpose: Events (mouse, keyboard) for a GLFW window

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

import glfw

class PysktEvents:
    def __init__(self, pyskt_main):
        self.pyskt_main = pyskt_main

        self.left_click = False
        self.right_click = False
        self.middle_click = False

        # If your mouse has the left side buttons
        self.side_front = False
        self.side_back = False

        self.scroll = ""
        
    def mouse_callback(self, *events):
        # Mouse click
        # events = (<glfw.LP__GLFWwindow>, 0, 0, 0)
        if len(events) == 4:
            state = bool(events[2])
            button = events[1] # 0 - left, 1 - right
            if state:
                print(f"Mouse button {button} clicked")
            else:
                print(f"Mouse button {button} released")
            
            if button == 0:
                self.left_click = state
            elif button == 1:
                self.right_click = state
            elif button == 2:
                self.middle_click = state
            elif button == 3:
                self.side_front = state
            elif button == 4:
                self.side_back = state
                

        # Scroll
        # events = (<glfw.LP__GLFWwindow>, 0.0, 1.0)
        if len(events) == 3:
            if events[2] == 1:
                direction = "up"
            elif events[2] == -1:
            
                direction = "down"
            print(f"Mouse scroll {direction}")

            self.scroll = direction
