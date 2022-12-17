from os import listdir
from numpy import load
from image_process import convert_image

class EffectManager():
  """
  Handles the loading of effect data within the data directory
  """
  def __init__(self):
    print("EffectManager __init_)")
    self.effects = {}
    self.load_effects()

  def load_effects(self):
    print("load_effects")
    def get_name(n):
      n = n.replace("-", " ")
      n = n.title()
      return n
    # TODO Makes this OS independant
    data_path = "./data"
    effect_directories = listdir(data_path)
    
    effect_types = ["eff", "rgb", "txt"]
    for f in effect_directories:
      if f[:3] in effect_types:
        self.effects[f] = Effect(f, get_name(f[4:]), f"{data_path}/{f}/")

  def get_effect(self, identifier):
    print("get_effect")
    self.load_effects()
    return self.effects[identifier]

  def create_gif(self):
    print("create_gif")
    gif_path = "./gifs/"
    gifs = listdir(gif_path)
    gifs.remove("archive")
    if gifs is None:
      # No gifs
      print("No gifs")
      return None

    for gif in gifs:
      print(gif)
      convert_image(gif)

    



class Effect():
  '''
  Attributes and data of a single effect
  '''
  def __init__(self, identifier="", name="", path=""):
    print("Effect __init__")
    self.identifier = identifier
    self.name = name
    self.path = path
    # self.effect_type = None
    self.is_rgb = None
    self.number_of_frames = len(listdir(self.path))
    self.current_frame = 0

    self.set_rgb()

  def set_rgb(self):
    print("set_rgb")
    if self.identifier[:3] in {"eff", "gif"}:
      self.is_rgb = False
    elif self.identifier[:3] in {"rgb", "txt"}:
      self.is_rgb = True

  def get_next_frame(self):
    print("get_next_frame")
    self.current_frame += 1
    if self.current_frame == self.number_of_frames:
      self.current_frame = 0
    filename = self.identifier + str(self.current_frame).zfill(3) + ".npy"
    return load(f"{self.path}{filename}")

if __name__ == "__main__":
  em = EffectManager()
  em.create_gif()

  # e = em.get_effect('rgb-pulse-fast')
  # print(e.identifier, e.name, e.number_of_frames)
  # for i in range(100):
  #   print(e.get_next_frame())