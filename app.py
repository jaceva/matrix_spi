import threading
from flask import Flask, jsonify, request
from os import listdir
from c_leds import MatrixLEDs

app = Flask(__name__)
# app.debug = True

lock = threading.Lock()
ml = MatrixLEDs(lock=lock)
effect_data = {"power": 1, "speed": 5, "effect": "eff-white-up-slow"}
ml.start_spi(effect_data)

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/effects', methods = ['GET'])
def effects():
  if request.method == "GET":
    return jsonify({"effects": ml.effect_names})

@app.route('/effect', methods = ['GET', 'POST'])
def effect():
  global effect_data
  if request.method == "GET":
    return jsonify([ml.data])
  
  if request.method == "POST":
    spi_data = request.json
    print(spi_data)
    effect_data["power"] = spi_data["power"] if "power" in spi_data else 1
    effect_data["speed"] = spi_data["speed"] if "speed" in spi_data else 5
    effect_data["effect"] = spi_data["effect"] if "effect" in spi_data and spi_data["effect"] != effect_data["effect"] else effect_data["effect"]
    
    return jsonify({'value': 200})