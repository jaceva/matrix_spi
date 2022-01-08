import threading
from flask import Flask, jsonify, request
from os import listdir
from c_leds import MatrixLEDs

app = Flask(__name__)
# app.debug = True

lock = threading.Lock()
ml = MatrixLEDs(lock=lock)

led_thread = threading.Thread(name='leds', target=ml.run_spi)
led_thread.start()

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/effect', methods = ['GET', 'POST'])
def effect():
  if request.method == "GET":
    data_files = listdir("/home/pi/matrix_spi/data")
    return jsonify(data_files)
  
  if request.method == "POST":
    spi_data = request.json
    print(spi_data)
    with lock:
      with open('/home/pi/matrix_spi/spi_file.txt', 'w') as s:
        s.write(f"{spi_data['power']}\n")
        s.write(f"{spi_data['speed']}\n")
        s.write(f"{spi_data['file']}\n")
    return jsonify({'value': 200})

# not needed in author
# if __name__ == '__main__':
#   app.run( host='0.0.0.0', port=8000, debug=False )