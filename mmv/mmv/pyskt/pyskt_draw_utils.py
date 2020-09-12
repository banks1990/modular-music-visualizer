"""
===============================================================================

Purpose: Draw utilities for PySKT

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



class SkiaDrawUtils:
    pass

""" 
paint = skia.Paint(AntiAlias=True, Color=skia.ColorRED)
            
# bold_typeface = skia.Typeface('Arial', skia.FontStyle.Bold())
# italic_typeface = skia.Typeface('Arial', skia.FontStyle.Italic())
# print(bold_typeface)
# print(italic_typeface)

# font = skia.Font(skia.Typeface('Times New Roman'), 24)
# print(font)

font = skia.Font(skia.Typeface('Arial'), 24)

center_x = width/2
center_y = height/2

text = "A Really long and hopefully centered text"

t_size = font.measureText(text)
l_size = font.getSpacing()

real_center_x = center_x - (t_size/2)
real_center_y = center_y - (l_size/2)

canvas.drawString(text, real_center_x, real_center_y, font, paint)


c = skia.Color4f(1, 0, 1, 0.3)


for _ in range(30):
    # Rectangle border
    border = skia.Rect(
        random.randint(0, width),
        random.randint(0, height),
        random.randint(0, width),
        random.randint(0, height),
    )
    
    # Draw the border
    canvas.drawRect(border, paint)
"""