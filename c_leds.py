import spidev
import time
import numpy as np
import pickle
from os import listdir


class MatrixLEDs():
  def __init__(self, lock=None):
    self.lock = lock
    self.main_data = {}
    self.spi = None
    self.get_main_data()
    self.init_spi()
    # self.run_spi()

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

  def get_spi_data(self):
    with self.lock:
      with open("/home/pi/matrix_spi/spi_file.txt", "r") as d_file:
        power = int(d_file.readline().strip())
        speed = int(d_file.readline().strip())
        data = d_file.readline().strip()

    return power, speed, data

  def run_spi(self):
    print("SPI Running")
    spf = 0.05
    frame_count = 0
    data_index = 0
    spi_time = time.time()
    power, speed, data = self.get_spi_data()
    with self.lock:
      self.spi.xfer3(self.main_data[data][0])
      
    while True:
      if (time.time() - spi_time) > spf:
        spi_time = time.time()
        frame_count += 1
        
        power, speed, data = self.get_spi_data()
        print(data, speed, data_index)
        # print(f"{frame_count} - {data_index} - {len(self.main_data[data])}")
        if len(self.main_data[data]) > 1 and (frame_count >= (11-speed)):
          
          
          frame_count = 0

          with self.lock:
            self.spi.xfer3(self.main_data[data][data_index])
            data_index += 1
            if data_index >= len(self.main_data[data]):
              data_index = 0
        
        