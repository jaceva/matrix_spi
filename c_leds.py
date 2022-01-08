import spidev
import time
import numpy as np
import pickle
from os import listdir


class MatrixLEDs():
  def __init__(self, lock=None):
    self.main_data = {}
    self.spi = None
    self.get_main_data()
    self.init_spi()
    self.run_spi()

  def get_main_data(self):
    data_files = listdir("/home/pi/matrix_spi/data")
    for f in data_files:
      with open(f"/home/pi/matrix_spi/data/{f}", 'rb') as pk_file:
        self.main_data[f] = pickle.load(pk_file)

  def init_spi(self):
    print("SPI Init")
    self.spi = spidev.SpiDev()
    bus = 0
    device = 0
    self.spi.open(bus, device)
    self.spi.max_speed_hz = 5000000

  def run_spi(self):
    print("SPI Running")
    spi_time = time.time()
    while True:
      if (time.time() - spi_time) > 5:
        print("SPI")
        spi_time = time.time()
        
        