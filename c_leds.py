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
    self.eff_red = 0
    self.eff_green = 0
    self.eff_blue = 0
    self.effect = 'eff-white-col-right'
    self.prev_effect = 'blue'
    # whether data can be rgb controlled
    self.is_rgb = False

    self.get_main_data()
    self.init_spi()

  def get_main_data(self):
    data_files = listdir("/home/pi/matrix_spi/data")
    
    for f in data_files:
      
      if ".npy" not in f:
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

  def set_data(self, power=1, speed=5, effect='blue',
                red=0, green=0, blue=0):
    self.power = power
    self.speed = speed
    self.effect = effect
    self.eff_red = red
    self.eff_green = green
    self.eff_blue = blue

  def start_spi(self):
    spi_thread = Thread(name='spi_loop', target=self.run_spi)
    spi_thread.start()

  def run_spi(self):
    print("SPI Running")


    
    frame_total = 0   # frames in effect 
    frame_count = 0   # counter for frames

    refresh_count = 0

    # seconds per frame
    spf = 0.05

    self.speed = 10
    
    # white_level = 0
    # step = -5
    
    manip_time = 0
    spi_time = 0

    while True:
      # print(time.time() - spi_time)
      if (time.time() - spi_time) > spf:
        spi_time = time.time()
        if self.effect != self.prev_effect:
          self.prev_effect = self.effect
          effect_frames = np.load(f"/home/pi/matrix_spi/data/{self.effect}.npy")
          frame_total = effect_frames.shape[0]
          refresh_count = 0
        if refresh_count >= (10-self.speed):
          refresh_count = 0
          with self.lock:
            # manip_time = time.time()
            manip_data = bitmanip(effect_frames[frame_count])
            # print(manip_data.shape)
            # manip_data = bitmanip(get_color_array(r=0, g=0, b=white_level))
            # print(time.time() - manip_time)
            
            # self.cs_pin.off()
            send_time = time.time()
            self.spi.writebytes2(manip_data)
            send_time = time.time() - send_time
            # print(send_time)
            # self.cs_pin.on()

          # next effect frame
          frame_count += 1
          if frame_count == frame_total:
            frame_count = 0

        # effect speed count
        refresh_count += 1
        # if white_level == 255 or white_level == 0:
        #   step *= -1

        # white_level += step

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