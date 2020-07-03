"""
===============================================================================

Purpose: Non constant and runtime dependent variables for communicating
between Python scripts

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
import sys


class Controller():
    def __init__(self, context):

        self.context = context
        self.utils = Utils()

        self.stop = False
        self.threads = {}

    def exit(self):

        debug_prefix = "[Controller.exit]"

        print(debug_prefix, "Controller exit called")

        if not self.context.resume:
            print(debug_prefix, "Setting resume=True as we're closing")
            self.context.resume = True

        self.stop = True
