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
    self.seconds_per_refresh = 0.030 # 0.020 worked with clock 5MHz without full test
    self.frames = []
    self.current_frame = 0
    self.refresh_count = 0

    self.frame_thread = None

    self.effect_names = {}

    
    self.effect_data = {}
    self.rgb_data = {}
    # whether data can be rgb controlled
    self.is_rgb = False

    self.update_main_data()
    self.init_spi()

  def update_main_data(self):
    def get_name(n):
      n = n.replace("-", " ")
      n = n.title()
      return n

    data_files = listdir("/home/pi/matrix_spi/data")
    
    file_types = ["eff", "rgb", "txt"]
    for f in data_files:
      if f[:3] in file_types:
        self.effect_names[f] = get_name(f[4:])
    

  def init_spi(self):
    print("SPI Init")
    self.spi = spidev.SpiDev()
    bus = 0
    device = 0
    
    self.cs_pin = LED(5)
    self.cs_pin.on()
    self.spi.open(bus, device)
    self.spi.max_speed_hz = 3000000 # 5000000 worked, not run for a long test

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
    try:
        self.next_frame(power=effect_data["power"], speed=effect_data["speed"], 
                        effect=effect_data["effect"], main_level=effect_data["main"],
                        fg_color= effect_data["fg_color"], bg_color= effect_data["bg_color"], )
    except Exception as e:
        print(e)
    
    if self.frame_thread is not None:
      self.frame_thread.cancel()
    self.frame_thread = Timer(self.seconds_per_refresh, self.start_spi, [effect_data])
    self.frame_thread.start()
    # print(time.time()-next_frame)
    
    

  def next_frame(self, power=None, speed=None, 
                effect=None, main_level=None,
                fg_color = None, bg_color=None):

    if effect != self.prev_effect:
      self.prev_effect = effect
      print("New Effect")
      print(f"Loading {effect}")
      frames = listdir(f"/home/pi/matrix_spi/data/{effect}")
      self.total_frames = len(frames)
      self.current_frame = 0
      self.refresh_count = 0

    if self.refresh_count >= (10-speed):
      self.refresh_count = 0
      
      filename = effect + str(self.current_frame).zfill(3) + ".npy"
      effect_frame = np.load(f"/home/pi/matrix_spi/data/{effect}/{filename}")
      file_type = filename[:3]
      fg_green = fg_color["g"]
      fg_red = fg_color["r"]
      fg_blue = fg_color["b"]

      bg_green = bg_color["g"]
      bg_red = bg_color["r"]
      bg_blue = bg_color["b"]
    #   print(fg_green, fg_red, fg_blue)
      effect_frame[:,:,0][effect_frame[:,:,0] > 0] *= fg_green
      effect_frame[:,:,1][effect_frame[:,:,1] > 0] *= fg_red
      effect_frame[:,:,2][effect_frame[:,:,2] > 0] *= fg_blue

      effect_frame[:,:,0][effect_frame[:,:,0] < 0] *= -bg_green
      effect_frame[:,:,1][effect_frame[:,:,1] < 0] *= -bg_red
      effect_frame[:,:,2][effect_frame[:,:,2] < 0] *= -bg_blue

      level_divider = 1/main_level if main_level > 0 else 255
      effect_frame = (effect_frame//level_divider).astype(np.uint8)

      manip_data = bitmanip(effect_frame)
      self.cs_pin.off()
      time.sleep(0.0001)
      self.spi.writebytes2(manip_data)
      self.cs_pin.on()
      # print(self.current_frame)
      self.current_frame += 1
      if self.current_frame == self.total_frames:
        self.current_frame = 0

    self.refresh_count += 1
        
if __name__ == "__main__":
  test_matrix = MatrixLEDs()
  test_matrix.start_spi({"power": 1, 
                        "speed": 10, 
                        "effect": "txt-test8", 
                        "main": 1, 
                        "fg_color": {"r": 255, "g": 255, "b": 255, }, 
                        "bg_color": {"r": 128, "g": 0, "b": 0, }})
  test_matrix.effect_names
