import spidev
import time
import numpy as np
import pickle
from os import listdir

main_data = {}
data_files = listdir("./data")
for f in data_files:
  with open(f"./data/{f}", 'rb') as pk_file:
    main_data[f] = pickle.load(pk_file)

spi = spidev.SpiDev()
bus = 0
device = 0
spi.open(bus, device)
spi.max_speed_hz = 5000000

speed_count = 0
frame = 0
while True:
  spi_data = []
  with open("spi_file.txt", "r") as d_file:
    power = int(d_file.readline().strip())
    speed = int(d_file.readline().strip())
    data = d_file.readline().strip()

  spi_data = main_data[data]
  spi.xfer3(spi_data[frame])
  print("SPI")  
  time.sleep(0.05)

# TODO: Figure out SPI and WS2813 pio integration.

# for i in range(len(spi_data)):
#   if i%6 == 0:
#     print()
#   print(bin(spi_data[i]), end="")