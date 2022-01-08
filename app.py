from flask import Flask, jsonify, request
from gpiozero import LED
from os import listdir

app = Flask(__name__)
app.debug = True

led1 = LED(21)
led1.on()

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/effect', methods = ['GET', 'POST'])
def effect():
  if request.method == "GET":
    data_files = listdir("./data")
    return jsonify(data_files)
  
  if request.method == "POST":
    spi_data = request.json
    with open('spi_file.txt', 'w') as s:
      s.write(f"{spi_data['power']}\n")
      s.write(f"{spi_data['speed']}\n")
      s.write(f"{spi_data['file']}\n")
    return jsonify({'value': 200})

# not needed in author
# if __name__ == '__main__':
#   app.run( host='0.0.0.0', port=8000, debug=False )