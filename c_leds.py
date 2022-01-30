import spidev
from gpiozero import LED
import time
import numpy as np
import pickle
from os import listdir
from threading import Thread, Lock, Timer
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
    self.effect = 'eff-white-up-slow'
    self.prev_effect = ''

    # next frame vars
    self.seconds_per_refresh = 0.02
    self.frames = []
    self.current_frame = 0
    self.refresh_count = 0

    self.frame_thread = None

    self.effect_names = {}

    
    self.effect_data = {}
    self.rgb_data = {}
    # whether data can be rgb controlled
    self.is_rgb = False

    self.get_main_data()
    self.init_spi()

  def get_main_data(self):
    def get_name(n):
      n = n.replace("-", " ")
      n = n.title()
      return n

    data_files = listdir("/home/pi/matrix_spi/data")
    
    for f in data_files:
      if f[:3] == "eff" or f[:3] == "rgb":
        self.effect_names[f] = get_name(f[4:])
    

  def init_spi(self):
    print("SPI Init")
    self.spi = spidev.SpiDev()
    bus = 0
    device = 0
    
    self.cs_pin = LED(5)
    self.cs_pin.on()
    self.spi.open(bus, device)
    self.spi.max_speed_hz = 4000000

  def set_data(self, power=1, speed=5, effect=None,
                red=0, green=0, blue=0):
    
    print("Set Data")
    self.power = power
    self.speed = speed
    if effect is not None:
      self.effect = effect
    if effect[:3] == "eff":
      self.is_rgb = False
    elif effect[:3] == "rgb":
      self.is_rgb = True
    self.eff_red = red
    self.eff_green = green
    self.eff_blue = blue

  def start_spi(self, effect_data):
    
    # next_frame = time.time()
    self.next_frame(power=effect_data["power"], speed=effect_data["speed"], 
                    effect=effect_data["effect"])
    
    if self.frame_thread is not None:
      self.frame_thread.cancel()
    self.frame_thread = Timer(self.seconds_per_refresh, self.start_spi, [effect_data])
    self.frame_thread.start()
    # print(time.time()-next_frame)
    
    

  def next_frame(self, power=None, speed=None, effect=None):
    if effect != self.prev_effect:
      self.prev_effect = effect
      print("New Effect")
      print(f"Loading {effect}")
      # self.prev_effect = self.effect
      frames = listdir(f"/home/pi/matrix_spi/data/{effect}")
      self.total_frames = len(frames)
      self.current_frame = 0
      self.refresh_count = 0

    if self.refresh_count >= (10-speed):
      self.refresh_count = 0
      # print(self.frames[self.current_frame])
      filename = effect + str(self.current_frame).zfill(3) + ".npy"
      effect_frame = np.load(f"/home/pi/matrix_spi/data/{effect}/{filename}") 
      # print(effect_frame)   
      manip_data = bitmanip(effect_frame)

      self.spi.writebytes2(manip_data)

      # print(self.current_frame)
      self.current_frame += 1
      if self.current_frame == self.total_frames:
        self.current_frame = 0

    self.refresh_count += 1

  def run_spi(self):
    
    print("SPI Running")


    
    frame_total = 0   # frames in effect 
    frame_count = 0   # counter for frames

    refresh_count = 0

    # seconds per frame
    spf = 0.05

    
    white_level = 0
    step = -5
    
    manip_time = 0
    spi_time = 0

    while True:
      # print(time.time() - spi_time)
      if (time.time() - spi_time) > spf:
        spi_time = time.time()
        if self.effect != self.prev_effect:
          self.prev_effect = self.effect
          frames = listdir(f"/home/pi/matrix_spi/data/{self.effect}")
          frames.sort(key=lambda file: int(file[-7:-4]))
          frame_count = 0
          refresh_count = 0
          frame_total = len(frames)
          print(frames)
          print(frame_total)

        if refresh_count >= (10-self.speed):
          refresh_count = 0
          with self.lock:
            
            # manip_time = time.time()
            # print(frames[frame_count])
            effect_frame = np.load(f"/home/pi/matrix_spi/data/{self.effect}/{frames[frame_count]}")
            
            manip_data = bitmanip(effect_frame)
            
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
        
if __name__ == "__main__":
  test_matrix = MatrixLEDs()
  test_matrix.start_spi()
  test_matrix.effect_names