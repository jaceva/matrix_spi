from os import listdir
from numpy import load
# from image_process import convert_image

EFFECTTYPES = ["eff", "rgb"]
EFFECTSDIR = "./data"

class EffectManager():
  """
  Handles the loading of effect data within the data directory
  """
  def __init__(self):
    print("EffectManager __init_)")
    self.effects = {}
    self.load_effects()
    self.output_effects()

  def load_effects(self):
    print("load_effects")
    def get_name(n):
      n = n.replace("-", " ")
      n = n.title()
      return n

    effect_directories = listdir(EFFECTSDIR)
    
    for f in effect_directories:
      if f[:3] in EFFECTTYPES:
        self.effects[f] = Effect(f, get_name(f[4:]), f"{EFFECTSDIR}/{f}/")

  def get_effect_names(self):
    self.load_effects()
    return {identifier: effect.name for identifier, effect in self.effects.items()}

  def get_effect(self, identifier):
    print("get_effect")

    # TODO does this need to be here
    # self.load_effects()
    return self.effects[identifier]

  def output_effects(self):
    for effect_id, effect in self.effects.items():
      print(f"{effect_id} - {effect.name}")

  # def create_gif(self):
  #   print("create_gif")
  #   gif_path = "./gifs/"
  #   gifs = listdir(gif_path)
  #   gifs.remove("archive")
  #   if gifs is None:
  #     # No gifs
  #     print("No gifs")
  #     return None

  #   for gif in gifs:
  #     print(gif)
  #     convert_image(gif)

    



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

  # TODO What would it take to load the numpy at startup?
  def get_next_frame(self):
    # print("get_next_frame")
    self.current_frame += 1
    if self.current_frame == self.number_of_frames:
      self.current_frame = 0
    filename = self.identifier + str(self.current_frame).zfill(3) + ".npy"
    return load(f"{self.path}{filename}")

if __name__ == "__main__":
  em = EffectManager()
  effect = em.effects["rgb-pulse-fast"]
  print(f"{effect.number_of_frames}")
  # while True:
  #   print(f"{effect.current_frame}", end='\r')
  #   effect.get_next_frame()

  print(em.get_effect_names())
  # em.create_gif()

  # e = em.get_effect('rgb-pulse-fast')
  # print(e.identifier, e.name, e.number_of_frames)
  # for i in range(100):
  #   print(e.get_next_frame())
