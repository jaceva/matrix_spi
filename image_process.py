import ffmpeg
import numpy as np
import pickle


# out, _ = ffmpeg.input('sparkle.gif').filter('scale', 108, 36).output('pipe:', format='rawvideo', pix_fmt='rgb24').run(capture_stdout=True)
# video = np.frombuffer(out, np.uint8).reshape([-1, 36, 108, 3])

# print(video.shape)

def get_full_image():
  return np.zeros((36, 108, 3), dtype=np.ubyte)

def get_spi_data(np_array):
  # TODO the following 2 loops need to be preprocess and stored
  # each entry of bit data represents one bit for 6 strands of a controller
  # 24 entries equal the color of a column of leds on the 6 strands of a controller
  bit_data = [0] * (6*8*108*3)

  for con in range(6):
    for led in range(108):
      for color in range(3):
        for strand, color_data in enumerate(np_array[con*6:con*6+6,led, color]):
          for byte in range(8):
            index = (con*2592)+(led*24)+(8*color)+byte
            bit_data[index] |= (((color_data >> byte) & 1) << strand)
          # print(f"Controller: {con}, Strand: {con*6+strand}, LED: {led}, Color: {color}, Data: {bit_data[index]}")
  # print([bin(b) for b in bit_data])

  spi_data = []

  for i in range(int(len(bit_data)/4)):
    # Check this data. It looks maybe off in serial output.
    spi_index = 4*i
    spi_data.append(int(bit_data[spi_index] | bit_data[spi_index+1] << 6) & 0xff)
    spi_data.append(int((bit_data[spi_index+1] >> 2) | bit_data[spi_index+2] << 4) & 0xff)
    spi_data.append(int((bit_data[spi_index+2] >> 4) | bit_data[spi_index+3] << 2) & 0xff)

  return spi_data

def write_spi_to_file(data):
  with open("./data/white-pulse-slow", "wb") as pk_file:
    pickle.dump(data, pk_file)



spi_data = []
image1 = get_full_image()
lvl = 0
step = 8
while lvl <= 255:
  print(lvl)
  image1[:,:,:] = lvl
  lvl += step
  spi_data.append(get_spi_data(image1))
write_spi_to_file(spi_data)