import spidev
from gpiozero import LED
import time
import numpy as np
import pickle
from os import listdir
from threading import Thread, Lock
from bitmanip import bitmanip, get_color_array, get_vline_array


class MatrixLEDs():
  def __init__(self, lock=Lock()):
    self.lock = lock
    self.main_data = {}
    self.spi = None
    self.power = 1
    self.speed = 5
    self.data = 'blue'
    self.prev_data = 'blue'

    self.get_main_data()
    self.init_spi()

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
    
    self.cs_pin = LED(5)
    self.cs_pin.on()
    self.spi.open(bus, device)
    self.spi.max_speed_hz = 4000000

  def set_data(self, power, speed, data):
    self.power = power
    self.speed = speed
    self.data = data

  def start_spi(self):
    spi_thread = Thread(name='spi_loop', target=self.run_spi)
    spi_thread.start()

  def run_spi(self):
    print("SPI Running")
    

    # counter for movie data
    frame_count = 0

    # frame index?
    data_index = 0

    # TODO start testing
    # YOU HAVE DISABLED UWSGI SERVICE FOR TESTING
    test_index = 0
    test_data1 = get_color_array(r=255, g=255, b=255)
    # test_data2 = get_vline_array(r1=0, g1=0, b1=255, 
    #                              r2=255, g2=0, b2=0, )
    manip_time = 0
    
    # seconds per frame
    spf = 0.05
    # TODO for testing
    # spf = 1

    spi_time = 0
    white_level = 0
    step = -5
    
    while True:
      if (time.time() - spi_time) > spf:
        spi_time = time.time()
        with self.lock:
          manip_time = time.time()
          # manip_data = bitmanip(test_data1)
          manip_data = bitmanip(get_color_array(r=0, g=0, b=white_level))
          
          # break
          # print(len(manip_data))
          # print(time.time() - manip_time)
          # self.spi.xfer3(manip_data)
          # print(manip_data)
          
          # spi send
          # self.cs_pin.off()
          send_time = time.time()
          self.spi.writebytes2(manip_data)
          send_time = time.time() - send_time
          print(send_time)
          # self.cs_pin.on()

        if white_level == 255 or white_level == 0:
          step *= -1

        white_level += step

    # TODO Commented out to simplify loop for error testing 
    # first send (for static images)
    # spi_time = 0
    # with self.lock:
    #   self.spi.xfer3(self.main_data[self.data][0])

    # while True:
    #   if (time.time() - spi_time) > spf:
    #     spi_time = time.time()
    #     frame_count += 1
        
    #     if self.prev_data != self.data or (len(self.main_data[self.data]) > 1 and (frame_count >= (11-self.speed))):
    #       frame_count = 0
    #       self.prev_data = self.data
    #       with open("data.log", "a") as dtl:
    #         dtl.writeline(f"{self.data}\n")

    #       with self.lock:
    #         self.spi.xfer3(self.main_data[self.data][data_index])
    #         data_index += 1
    #         if data_index >= len(self.main_data[self.data]):
    #           data_index = 0
        
if __name__ == "__main__":
  test_matrix = MatrixLEDs()
  test_matrix.start_spi()