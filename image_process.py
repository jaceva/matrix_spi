import ffmpeg
import numpy as np
import pickle

# ffmepeg to covert images(gifs?) to the right size numpy array
# TODO needs testing
def convert_image(image):
  try:
    out, _ = ffmpeg.input('imports/' + image).filter('scale', 108, 36).output('pipe:', format='rawvideo', pix_fmt='rgb24').run(capture_stdout=True)
    video = np.frombuffer(out, np.uint8).reshape([-1, 36, 108, 3])
    
    print(video[0][14])
  except Exception as e:
    print(e)
  

def get_full_image():
  return np.zeros((1, 36, 108, 3), dtype=np.ubyte)

def white_up(step):
  if step > 0:
    effect = np.zeros((1, 36, 108, 3), dtype=np.ubyte)
    frame = get_full_image()
    level = 0
    while level <= 255:
      frame[:,:,:] = level
      level += step
      effect = np.append(effect, frame, axis=0)
    
    effect = effect[1:]
    return effect

def column_chase():
  effect = np.zeros((1, 36, 108, 3), dtype=np.ubyte)
  frame = get_full_image()

  for column in range(108):
    frame[:, :, :, :] = 0
    frame[:, :, column, :] = 255
    effect = np.append(effect, frame, axis=0)

  effect = effect[1:]
  return effect



    

  return None
  

if __name__ == "__main__":
  # convert_image('sparkle.gif')
  # e = white_pulse(10)


  e = column_chase()
  print(e.shape[0])
  np.save("data/eff-white-col-right", e)



# image1 = get_full_image()
# lvl = 0
# step = 8
# while lvl <= 255:
#   print(lvl)
#   image1[:,:,:] = lvl
#   lvl += step