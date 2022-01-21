import threading
from flask import Flask, jsonify, request
from os import listdir
from c_leds import MatrixLEDs

app = Flask(__name__)
# app.debug = True

lock = threading.Lock()
ml = MatrixLEDs(lock=lock)

# led_thread = threading.Thread(name='leds', target=ml.run_spi)
# led_thread.start()
ml.start_spi()

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/effects', methods = ['GET'])
def effects():
  if request.method == "GET":
    data_files = listdir("/home/pi/matrix_spi/data")
    return jsonify(data_files)

@app.route('/effect', methods = ['GET', 'POST'])
def effect():
  if request.method == "GET":
    return jsonify([ml.data])
  
  if request.method == "POST":
    spi_data = request.json
    print(spi_data)
    
    ml.set_data(spi_data["power"], spi_data["speed"], spi_data["file"])
      # with open('/home/pi/matrix_spi/spi_file.txt', 'w') as s:
      #   s.write(f"{spi_data['power']}\n")
      #   s.write(f"{spi_data['speed']}\n")
      #   s.write(f"{spi_data['file']}\n")
    return jsonify({'value': 200})