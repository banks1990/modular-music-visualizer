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
    
    # # #

    # https://stackoverflow.com/questions/7261936

    # https://stackoverflow.com/a/63013204/13477696
    def num2col(self, n):
        n, rem = divmod(n - 1, 26)
        next_char = chr(65 + rem)
        if n:
            return self.num2col(n) + next_char
        else:
            return next_char
    
    # https://stackoverflow.com/a/63013204/13477696
    def col2num(self, s):
        n = ord(s[-1]) - 64
        if s[:-1]:
            return 26 * (self.col2num(s[:-1])) + n
        else:
            return n
            
    # # # 

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

    # https://stackoverflow.com/a/24468019/13477696
    def irregular_polygon_area(self, *points):
        n = len(points) # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        area = abs(area) / 2.0
        return area

    # Information of a point relative to a polygon
    def information_point_polygon(self, P, *polygon_points):
        """
        Given a point P and a polygon of N points, returns:
        {
            "is_inside": bool,
            "minimum_distance": float,
            "minimum_distance_line": see below
        }

        The minimum distance line is something like, you give this function
        (P=(x, y), (0, 0), (10, 5), (3, 5)) =>
        (P, A, B, C)

        If point nearest line is AB, minimum_distance_line returns 0.

        AB - 0   CB - 1   CA - 2
        """

        # Get 
        polygon_area = self.irregular_polygon_area(*polygon_points)

        P = np.array(P)

        # Ordered points: (0, 0), (1, 0), (0, 1)  -->  [('A', (0, 0)), ('B', (1, 0)), ('C', (0, 1))]
        # We use list as those will be easier to manipulate
        op = [(self.num2col(i + 1), np.array(v)) for i, v in enumerate(polygon_points)]

        # [('A', (0, 0)), ('B', (1, 0)), ('C', (0, 1))] Becomes:
        # {'CAP': {'points': [array([0, 1]), array([0, 0]), array([1, 1])], 'area': 0.5}, 'ABP': {'points': ...
        triangles = {f"{op[i][0]}-{op[i+1][0]}-P": {"points": [op[i][1], op[i+1][1], P]} for i in range(-1, len(op) - 1)}
        
        # Now we convert to a dictionary for matching the points later on
        op = {point: coordinate for point, coordinate in op}

        # Calculate 
        for key in triangles.keys():
            triangles[key]["area"] = self.three_points_triangle_area(*triangles[key]["points"])

        print(triangles)

        # Sum the triangle areas
        triangles_areas = [triangles[key]["area"] for key in triangles.keys()]

        # The point is inside the polygon if the areas sum less than the original one
        is_inside = sum(triangles_areas) <= polygon_area

        # Get the triangle with the lowest area so we'll find the closest edge
        lowest_area = min(triangles_areas)
        for key in triangles.keys():
            if triangles[key]["area"] == lowest_area:
                smallest_triangle = key.split("-")
                break

        # To get our minimum_distance_line
        # If the point is AB, we return 0
        # If the point is BC, we return 1
        # If the point is CA, we return 2
        # It is the lowest index of the two points
        point_indexes = [
            self.col2num(smallest_triangle[0]),
            self.col2num(smallest_triangle[1]),
        ]
        print(point_indexes, smallest_triangle)
        minimum_distance_line = min(point_indexes) - 1
        
        # Now we have a triangle in the form XX-YY-P, we'll find the height of the triangle, the minimum distance from P to 
        # the line of XX -- YY

        # The triangle base is the distance between the points (XX) and (YY) so..
        base = np.linalg.norm(
            [ op[smallest_triangle[0]], op[smallest_triangle[1]] ]
        )
        
        # We know its area, it's the lowest_area var!!
        # B*H = A,
        # H = A/B
        lowest_distance = lowest_area / base

        info = {
            "is_inside": is_inside,
            "minimum_distance": lowest_distance,
            "minimum_distance_line": minimum_distance_line,
        }

        print(triangles_areas, polygon_area, is_inside, "smallest:", smallest_triangle)
        print(info)

        return info

    # Is a point of coordinate P = (x, y) inside a rectangle R = (x, y, w, h)?
    # https://math.stackexchange.com/a/190117
    # This was a pretty fun insight :)
    def point_against_rectangle(self, P, R, method="dot_product"):
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

        return self.information_point_polygon(P, R1, R2, R4, R3)

if __name__ == "__main__":
    
    # Testing

    p = PysktProcessing({})

    p.information_point_polygon((1, 0.1), (0, 0), (1, 0), (0, 1))
    # print( p.three_points_triangle_area([0, 0], [0, 3], [4, 0]) ) 

    # print(p.point_against_rectangle(
    #     [1, 0],
    #     [0, 0, 10, 10]
    # ))