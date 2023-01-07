from threading import Timer
import numpy as np
import time
import json
from bitmanip import bitmanip

# TODO uncomment on RPi
# import spidev
# from gpiozero import LED

from effects import EffectManager

class MatrixLeds():
  '''
  Class that handle the data that gets sent to the LEDs via SPI
  '''
  def __init__(self):

    self.effect_manager = EffectManager()
    
    self.spi = None
    self.spi_data = None

    # TODO Should spi_speed and refresh be added?
    with open("./led_config.json") as cfg:
      config = json.load(cfg)

    # TODO uncomment on RPi
    # self.cs_pin = LED(config["cs_pin"])

    # values for controller
    
    self.effect = self.effect_manager.get_effect(config["effect_id"])
    self.speed = config["speed"]
    self.bright = config["bright"] / 100
    
    self.fg_color = config["fg_color"]
    self.bg_color = config["bg_color"]
    
    self.prev_effect_id = None

    # next frame vars
    self.seconds_per_refresh = 0.050 # 20fps
    self.refresh_count = 0 # handles frames update (refresh rate)

    self.frame_thread = None # holds the timer instance

    self.init_spi()

  def init_spi(self):
    
    # TODO uncomment on RPi
    # self.spi = spidev.SpiDev()
    # bus = 0
    # device = 0
    
    # self.cs_pin.on()
    # self.spi.open(bus, device)
    # self.spi.max_speed_hz = 2000000

    print("init_spi")

  def get_data(self):
    return {
      'effect_id': self.effect.identifier,
      'effect_name': self.effect.name,
      'speed': self.speed,
      'bright': self.bright,
      'fg_color': self.fg_color,
      'bg_color': self.bg_color,
    }

  def set_data(self, 
                effect_id, 
                speed, 
                bright,
                fg_color,
                bg_color):
    
    print("set_data")
    # TODO this is the point where loading all of a single effects frame could help frame2frame performance
    if effect_id != self.prev_effect_id:
      self.prev_effect_id = effect_id
      self.effect = self.effect_manager.get_effect(effect_id)
      self.refresh_count = 0
    
    # TODO speed is now 0 - 100
    self.speed = speed 
    self.bright = bright / 100

    self.fg_color = fg_color
    self.bg_color = bg_color

  def next_frame(self):
    if self.refresh_count >= (100-self.speed):
      self.refresh_count = 0
      print("next_frame")
    # next_frame = time.time()
      try:
        self.process_frame()
      except Exception as e:
          print(e)

      try:
        self.send_frame()
      except Exception as e:
          print(e)
    
    self.set_thread()
    # print(time.time()-next_frame)
    self.refresh_count += 1

  def process_frame(self):
    effect_frame = self.effect.get_next_frame()
    if self.effect.is_rgb:
      # foreground color
      effect_frame[:,:,0][effect_frame[:,:,0] > 0] *= self.fg_color["g"]
      effect_frame[:,:,1][effect_frame[:,:,1] > 0] *= self.fg_color["r"]
      effect_frame[:,:,2][effect_frame[:,:,2] > 0] *= self.fg_color["b"]

      # background color
      effect_frame[:,:,0][effect_frame[:,:,0] < 0] *= -self.bg_color["g"]
      effect_frame[:,:,1][effect_frame[:,:,1] < 0] *= -self.bg_color["r"]
      effect_frame[:,:,2][effect_frame[:,:,2] < 0] *= -self.bg_color["b"]

    effect_frame = (effect_frame * self.bright).astype(np.uint8)

    self.spi_data = bitmanip(effect_frame)

  def send_frame(self):

      # TODO uncomment on RPi
      # self.cs_pin.off()
      # time.sleep(0.0001)
      # self.spi.writebytes2(self.spi_data)
      # self.cs_pin.on()

      print("Send Frame")

  def set_thread(self):
    if self.frame_thread is not None:
      self.frame_thread.cancel()
      
    self.frame_thread = Timer(self.seconds_per_refresh, self.next_frame)
    self.frame_thread.start()

if __name__ == "__main__":
  ml = MatrixLeds()
  ml.set_data("rgb-test-frame", 
              100, 
              50,
              {"r": 255, "g": 255, "b": 255},
              {"r": 0, "g": 0, "b": 0}
  )
  ml.next_frame()