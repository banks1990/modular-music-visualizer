"""
===============================================================================

Purpose: Context for a Pyskt window

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

class PysktContext:
    def __init__(self, kwargs):
        self.width = 1280
        self.height = 720

        self.show_fps = kwargs.get("show_fps", False)
        self.wait_events = kwargs.get("wait_events", True)