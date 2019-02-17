from struct import pack
from symbolic_aggregate_approximation import SymbolicAggregateApproximation
from bitmap_module.letter_to_colour_conversion import letter_to_colour
import math

class Bitmap():
  def __init__(s, width, height):
    s._bfType = 19778 # Bitmap signature
    s._bfReserved1 = 0
    s._bfReserved2 = 0
    s._bcPlanes = 1
    s._bcSize = 12
    s._bcBitCount = 24
    s._bfOffBits = 26
    s._bcWidth = width
    s._bcHeight = height
    s._bfSize = 26+s._bcWidth*3*s._bcHeight
    s.clear()


  def clear(s):
    s._graphics = [(0,0,0)]*s._bcWidth*s._bcHeight


  def setPixel(s, x, y, color):
    if isinstance(color, tuple):
      if x<0 or y<0 or x>s._bcWidth-1 or y>s._bcHeight-1:
        raise ValueError('Coords out of range')
      if len(color) != 3:
        raise ValueError('Color must be a tuple of 3 elems')
      s._graphics[y*s._bcWidth+x] = (color[2], color[1], color[0])
    else:
      raise ValueError('Color must be a tuple of 3 elems')


  def write(s, file):
    with open(file, 'wb') as f:
      f.write(pack('<HLHHL', 
                   s._bfType, 
                   s._bfSize, 
                   s._bfReserved1, 
                   s._bfReserved2, 
                   s._bfOffBits)) # Writing BITMAPFILEHEADER
      f.write(pack('<LHHHH', 
                   s._bcSize, 
                   s._bcWidth, 
                   s._bcHeight, 
                   s._bcPlanes, 
                   s._bcBitCount)) # Writing BITMAPINFO
      for px in s._graphics:
        f.write(pack('<BBB', *px))
      for i in range (0, (s._bcWidth*3) % 4):
        f.write(pack('B', 0))



def main():

  sax = SymbolicAggregateApproximation()
  string = sax.generate_walk(1)
  total_images = math.ceil(len(string)/256)
  
  # 256 = 16 x 16 images

  side = 16
  b = Bitmap(side, side)
  for row in range(0, side):
      for col in range(0, side):
        letter_choice = (row * side) + col
        rgb_colour = letter_to_colour(string[letter_choice])
        b.setPixel(row, col, rgb_colour)
  b.write('file.bmp')


if __name__ == '__main__':
  main()