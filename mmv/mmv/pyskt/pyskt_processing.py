"""
===============================================================================

Purpose: Function routines for PySKT like collision checking, proportions

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

import numpy as np
import skia


class PysktProcessing:
    def __init__(self, pyskt_main):
        self.pyskt_main = pyskt_main

    # Absolute area between two vectors so doesn't matter what direction they are at
    def abs_cross_product(self, V1, V2):
        V1 = np.array(V1)
        V2 = np.array(V2)
        return np.abs(np.cross(V1, V2))
    
    # Get the area of a triangle with three coordinate points
    def three_points_triangle_area(self, P1, P2, P3):

        # Transform the points into an array
        P1 = np.array(P1)
        P2 = np.array(P2)
        P3 = np.array(P3)

        # Vector AB is point B - A

        # V1 = P2->P1 => V1 = P1 - P2
        V1 = P1 - P2

        # V2 = P2->P3 => V1 = P3 - P2
        V2 = P3 - P2

        # Magnitude of cross product is the area of the rhombus or rectangle between the two vectors
        # for a triangle we divide that by two
        return self.abs_cross_product(V1, V2) / 2

    # Is a point of coordinate P = (x, y) inside a rectangle R = (x, y, w, h)?
    # https://math.stackexchange.com/a/190117
    # This was a pretty fun insight :)
    def point_inside_rectangle(self, P, R, method="dot_product"):
        """
        R1 - - - - - - R2
         |     P       |
         |             |
        R3 - - - - - - R4

        Top left R1 is the center, w grows rightwards, h grows downwards
        """

        # Convert the point to a top left center Y grows downward
        # (negative all Y values so we flip the space on the X axis)
        P = [P[0], -P[1]]

        # Rectangle

        x = R[0]
        y = R[1]
        w = R[2]
        h = R[3]

        R1 = np.array([x, y])
        R2 = np.array([x + w, y])
        R3 = np.array([x, y - h])
        R4 = np.array([x + w, y - h])

        # Far more efficient
        if method == "dot_product":
            R1R2 = R2 - R1
            R1R3 = R3 - R1
            R1P = P - R1
            return (0 <= np.dot(R1P, R1R2) < np.dot(R1R2, R1R2)) and (0 <= np.dot(R1P, R1R3) < np.dot(R1R3, R1R3))

        # Nice insight on areas
        elif method == "triangles":

            # # Rectangle

            # We'll get the vector from center R1 and goes to R2 and R3
            # V1 = R1R2 => R2 - R1
            # V2 = R1R3 => R3 - R1
            rectangle_area = self.abs_cross_product(R2 - R1, R3 - R1)

            # # Triangle

            # Triangles points -> (R1 R3 P), (R1, R2, P), (R2, R4, P), (R4, R3, P)
            triangle_areas = [
                self.three_points_triangle_area(R1, R3, P),
                self.three_points_triangle_area(R1, R2, P),
                self.three_points_triangle_area(R2, R4, P),
                self.three_points_triangle_area(R4, R3, P),
            ]

            if sum(triangle_areas) <= rectangle_area:
                return True
            else:
                return False

if __name__ == "__main__":
    
    # Testing

    p = PysktProcessing({})

    print( p.three_points_triangle_area([0, 0], [0, 3], [4, 0]) ) 

    print(p.point_inside_rectangle(
        [1, 0],
        [0, 0, 10, 10]
    ))