#!/usr/bin/env python3.7

import adafruit_mlx90640
import board
import busio
import math
import os
import json
import logging
from logging.handlers import RotatingFileHandler
import time

PIXEL_WIDTH = int(os.environ.get("PIXEL_WIDTH"))
PIXEL_HEIGHT = int(os.environ.get("PIXEL_HEIGHT"))
file = os.environ.get("SENSOR_LOG_FILE")

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768
while True:
  try:
    mlx.getFrame(frame)
  except ValueError:
    # these happen, no biggie - retry
    continue
  print(frame)
  data = [{
    'x': i % (PIXEL_WIDTH-1),
    'y': math.floor(i/PIXEL_HEIGHT),
    'value': value
  } for i,value in enumerate(frame)]
  with open(file, 'w') as filetowrite:
    filetowrite.write(json.dumps(data))


# import time
# import board
# import busio
# import adafruit_amg88xx
#
#
# i2c_bus = busio.I2C(board.SCL, board.SDA)
# amg = adafruit_amg88xx.AMG88XX(i2c_bus)
#
# while True:
#
#     for row in amg.pixels:
#
#         print(['{0:.1f}'.format(temp) for temp in row])
#         print("")
#     print("\n")
#     time.sleep(4)
#
# #low range of the sensor (this will be blue on the screen)
# MINTEMP = 26.
#
# #high range of the sensor (this will be red on the screen)
# MAXTEMP = 32.
#
# #how many color values we can have
# COLORDEPTH = 1024
#
# os.putenv('SDL_FBDEV', '/dev/fb1')
# pygame.init()
#
# # pylint: disable=invalid-slice-index
# points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
# grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
# # pylint: enable=invalid-slice-index
#
# #sensor is an 8x8 grid so lets do a square
# height = 240
# width = 240
#
# #the list of colors we can choose from
# blue = Color("indigo")
# colors = list(blue.range_to(Color("red"), COLORDEPTH))
#
# #create the array of colors
# colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
#
# displayPixelWidth = width / 30
# displayPixelHeight = height / 30
#
# # lcd = pygame.display.set_mode((width, height))
# #
# # lcd.fill((255, 0, 0))
# #
# # pygame.display.update()
# # pygame.mouse.set_visible(False)
# #
# # lcd.fill((0, 0, 0))
# # pygame.display.update()
#
# #some utility functions
# def constrain(val, min_val, max_val):
#   return min(max_val, max(min_val, val))
#
# def map_value(x, in_min, in_max, out_min, out_max):
#   return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
#
# #let the sensor initialize
# time.sleep(.1)
#
# while True:
#
#   #read the pixels
#   pixels = []
#   for row in sensor.pixels:
#     pixels = pixels + row
#   pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
#
#   #perform interpolation
#   bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
#
#   #draw everything
#   for ix, row in enumerate(bicubic):
#     for jx, pixel in enumerate(row):
#       print("color")
#         # pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
#         #                  (displayPixelHeight * ix, displayPixelWidth * jx,
#         #                   displayPixelHeight, displayPixelWidth))
#
#   pygame.display.update()
