import numpy as np
import time

def bitmanip(a, control_shape=15552):
  bits = np.array([], dtype=np.uint8)
  a1 = np.unpackbits(a, axis=2)
  for i in range(0, 36, 6):
    a2 = np.rot90(a1[i:i+6], k=1, axes=(2,1))
    a3 = np.rot90(a2, k=1, axes=(0,2))
    a4 = np.reshape(a3, control_shape)

    bits = np.concatenate((bits, a4), axis=0)
  return np.packbits(bits)

def print_array(a):
  ua = np.unpackbits(a)
  for i in range(0, len(ua), 6):
    if i != 0 and i % 144 == 0:
      print()
    print([d for d in ua[i:i+6]])

if __name__ == "__main__":

  test2 = np.zeros((36, 108, 3), dtype=np.ubyte)
  test2[:,:,:] = 0x55

  single_led = np.zeros((36, 1, 3), dtype=np.ubyte)
  single_led[0::8,:,:] = 64
  single_led[1::8,:,:] = 4
  single_led[2::8,:,:] = 16
  single_led[3::8,:,:] = 1
  single_led[4::8,:,:] = 128
  single_led[5::8,:,:] = 32
  single_led[6::8,:,:] = 8
  single_led[7::8,:,:] = 2

  start = time.time()
  spi_data = bitmanip(test2)
  print(time.time() - start)
  print(len(spi_data))
  print(spi_data)
  # print_array(spi_data)

  # start = time.time()
  # spi_data = bitmanip(test2)
  # print(time.time() - start)
  # print(len(spi_data))
  # print([b for b in spi_data])