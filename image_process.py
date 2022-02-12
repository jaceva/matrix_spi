from PIL import Image, ImageDraw, ImageFont
import ffmpeg
import numpy as np
import pickle
import os
import pwd
import grp

uid = pwd.getpwnam("pi").pw_uid
gid = grp.getgrnam("www-data").gr_gid

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
      while level <= 256:
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
    frame[:,:,:] = level
    level = level + step
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
  else:
    print("Name already in directory.") 
 
def test_frame():
  pattern_name = "rgb-test-scroll"
  os.mkdir(f"/home/pi/matrix_spi/data/{pattern_name}")
  frame = get_full_image(dt=np.half)
  # green
  for j in range(6):
    frame[0*6+j, 0:j+1, 0] = 1
    frame[0*6+j, -1-j:, 0] = 1
    
  # red
  for j in range(6):
    frame[1*6+j, 0:j+2, 1] = 1
    frame[1*6+j, -2-j:, 1] = 1
    
  # blue
  for j in range(6):
    frame[2*6+j, 0:j+3, 2] = 1
    frame[2*6+j, -3-j:, 2] = 1
    
  # yellow
  for j in range(6):
    frame[3*6+j, 0:j+4, 0] = 1
    frame[3*6+j, 0:j+4, 1] = 1
    frame[3*6+j, -4-j:, 0] = 1
    frame[3*6+j, -4-j:, 1] = 1
    
  # cyan
  for j in range(6):
    frame[4*6+j, 0:j+5, 0] = 1
    frame[4*6+j, 0:j+5, 2] = 1
    frame[4*6+j, -5-j:, 0] = 1
    frame[4*6+j, -5-j:, 2] = 1
    
  # magenta
  for j in range(6):
    frame[5*6+j, 0:j+6, 1] = 1
    frame[5*6+j, 0:j+6, 2] = 1
    frame[5*6+j, -6-j:, 1] = 1
    frame[5*6+j, -6-j:, 2] = 1

  for k in range(86):
    frame[:,k+11,:] = 1
    np.save(f"/home/pi/matrix_spi/data/{pattern_name}/{pattern_name}{str(k).zfill(3)}", frame)

def create_text_scroll(name, text, height, top, font_name="arial.ttf"):
  data_files = os.listdir("/home/pi/matrix_spi/data")
  txt_name = f"txt-{name}"
  if txt_name not in data_files:
    txt_dir = f"/home/pi/matrix_spi/data/{txt_name}"
    os.mkdir(txt_dir)
    # os.chown(txt_dir, uid, gid)
    font_size = 1
    text_length = None
    font = ImageFont.truetype(font_name, font_size)
    while font.getsize(text)[1] < height: 
      font_size += 1
      font = ImageFont.truetype(font_name, font_size)

    text_length = font.getsize(text)[0]
    text_image = Image.new("RGB", (300+text_length, 36))
    draw_image = ImageDraw.Draw(text_image)
    draw_image.text((108, top), text, font=font, fill=(255, 255, 255,))
    # text_image = text_image.convert("1")
    text_array = np.array(text_image, dtype=np.int16)
    text_array[text_array < 32] = -1
    text_array[text_array >= 32] = 1
    print(text_array)
    text_image.save(f"/home/pi/matrix_spi/thumbs/{txt_name}.jpg")
    frame_total = text_array.shape[1] - 107
    for f in range(0, frame_total-1, 2):
      np.save(f"/home/pi/matrix_spi/data/{txt_name}/{txt_name}{str(f//2).zfill(3)}", text_array[:,f:108+f])    


if __name__ == "__main__":
  # convert_image('sparkle.gif')
  # e = white_pulse(10)
  # white_up("eff-white-up-fast", 25)
  create_rgb("pulse-fast", 16, pulse)
#   test_frame()
#   create_text_scroll("test8", "| | | | | | | | ", 30, 0)
  
