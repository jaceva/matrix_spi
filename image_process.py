import ffmpeg
import numpy as np
import pickle
import os

# ffmepeg to covert images(gifs?) to the right size numpy array
# TODO needs testing
def convert_image(image):
  try:
    out, _ = ffmpeg.input('imports/' + image).filter('scale', 108, 36).output('pipe:', format='rawvideo', pix_fmt='rgb24').run(capture_stdout=True)
    video = np.frombuffer(out, np.uint8).reshape([-1, 36, 108, 3])
    
    print(video[0][14])
  except Exception as e:
    print(e)
  

def get_full_image(dt=np.uint8):
  return np.zeros((36, 108, 3), dtype=dt)

def white_up(name, step):
  if step > 0:
    data_files = os.listdir("/home/pi/matrix_spi/data")
    if name not in data_files:
      os.mkdir(f"/home/pi/matrix_spi/data/{name}")
      frame = get_full_image()
      level = 0
      frame_number = 0
      while level <= 255:
        frame[:,:,:] = level
        np.save(f"/home/pi/matrix_spi/data/{name}/{name}{str(frame_number).zfill(3)}", frame)
        level += step
        frame_number += 1

def column_chase():
  effect = np.zeros((1, 36, 108, 3), dtype=np.ubyte)
  frame = get_full_image()

  for column in range(108):
    frame[:, :, :, :] = 0
    frame[:, :, column, :] = 255
    effect = np.append(effect, frame, axis=0)

  effect = effect[1:]
  return effect

def pulse(step):
  level = 0
  frame = get_full_image(dt=np.half)
  while level <= 1:
    frame[:,:,:] = level
    level = level + step
    yield frame

  level = 1.0
  step *= -1
  while level >= 0:
    level = level + step
    frame[:,:,:] = level
    yield frame


def create_rgb(name, steps_to_max, effect_function):
  data_files = os.listdir("/home/pi/matrix_spi/data")
  rgb_name = f"rgb-{name}"
  if rgb_name not in data_files:
    rgb_dir = f"/home/pi/matrix_spi/data/{rgb_name}"
    os.mkdir(rgb_dir)
    step = 1/steps_to_max
    for i, frame in enumerate(pulse(step)):
      np.save(f"/home/pi/matrix_spi/data/{rgb_name}/{rgb_name}{str(i).zfill(3)}", frame)
      print(frame)
  else:
    print("Name already in directory.") 
 

if __name__ == "__main__":
  # convert_image('sparkle.gif')
  # e = white_pulse(10)
  # white_up("eff-white-up-fast", 25)
  create_rgb("pulse-slow", 255, pulse)
  



# image1 = get_full_image()
# lvl = 0
# step = 8
# while lvl <= 255:
#   print(lvl)
#   image1[:,:,:] = lvl
#   lvl += step