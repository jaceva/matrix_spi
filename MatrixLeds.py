from threading import Timer
import numpy as np
import time
from bitmanip import bitmanip

import spidev
from gpiozero import LED

from Effects import EffectManager

class MatrixLeds():
  '''
  Class that handle the data that gets sent to the LEDs via SPI
  '''
  def __init__(self):

    self.effect_manager = EffectManager()

    self.spi = None
    self.cs_pin = None
    self.speed = 5

    self.effect = None
    self.prev_effect_id = None

    # values from controller
    self.control_speed = 5
    self.control_red = 0
    self.control_green = 0
    self.control_blue = 0

    # next frame vars
    self.seconds_per_refresh = 0.050
    self.refresh_count = 0 # handles frames update (refresh rate)

    self.frame_thread = None # holds the timer instance

    self.init_spi()

  def init_spi(self):
    print("init_spi")
    
    self.spi = spidev.SpiDev()
    bus = 0
    device = 0
    
    self.cs_pin = LED(5)
    self.cs_pin.on()
    self.spi.open(bus, device)
    self.spi.max_speed_hz = 2000000

  def set_data(self, speed=5, effect_name = "",
                red=0, green=0, blue=0):
    
    print("Set Data")
    self.speed = speed
    if effect_name is not None:
      self.effect = self.effect_manager.get_effect(effect_name)

    self.control_red = red
    self.control_green = green
    self.control_blue = blue

  def run_spi(self, effect_data):
    
    print("run_spi")
    # next_frame = time.time()
    try:
        self.send_frame(speed=effect_data["speed"], 
                        effect_id=effect_data["effect"], main_level=effect_data["main"],
                        fg_color= effect_data["fg_color"], bg_color= effect_data["bg_color"], )
    except Exception as e:
        print(e)
    
    if self.frame_thread is not None:
      self.frame_thread.cancel()
      
    self.frame_thread = Timer(self.seconds_per_refresh, self.run_spi, [effect_data])
    self.frame_thread.start()
    # print(time.time()-next_frame)

  def send_frame(self, speed=None, 
                effect_id=None, main_level=None,
                fg_color = None, bg_color=None):

    print("next_frame")
    if self.effect is None or self.effect.identifier != effect_id:
      self.effect = self.effect_manager.get_effect(effect_id)
      self.refresh_count = 0

    if self.refresh_count >= (10-speed):
      self.refresh_count = 0
      level_divider = 1/main_level if main_level > 0 else 255

      effect_frame = self.effect.get_next_frame()
      if self.effect.is_rgb:
        # foreground color
        effect_frame[:,:,0][effect_frame[:,:,0] > 0] *= fg_color["g"]
        effect_frame[:,:,1][effect_frame[:,:,1] > 0] *= fg_color["r"]
        effect_frame[:,:,2][effect_frame[:,:,2] > 0] *= fg_color["b"]

        # background color
        effect_frame[:,:,0][effect_frame[:,:,0] < 0] *= bg_color["g"]
        effect_frame[:,:,1][effect_frame[:,:,1] < 0] *= bg_color["r"]
        effect_frame[:,:,2][effect_frame[:,:,2] < 0] *= bg_color["b"]

      effect_frame = (effect_frame//level_divider).astype(np.uint8)

      # print(effect_frame)
      manip_data = bitmanip(effect_frame)

      self.cs_pin.off()
      time.sleep(0.0001)
      self.spi.writebytes2(manip_data)
      self.cs_pin.on()

if __name__ == "__main__":
  ml = MatrixLeds()
  ml.run_spi({
    "speed": 10, 
    "effect": "rgb-pulse-fast", 
    "main": 1, 
    "fg_color": {"r": 255, "g": 255, "b": 255, }, 
    "bg_color": {"r": 128, "g": 0, "b": 0, }
  })