import threading
from flask import Flask, jsonify, request
from os import listdir
from c_leds import MatrixLEDs
from image_process import create_text_scroll

app = Flask(__name__)
# app.debug = True

lock = threading.Lock()
ml = MatrixLEDs(lock=lock)
effect_data = {"power": 1, "speed": 5, 
              "effect": "rgb-pulse-slow", 'main': 1, 
              "fg_color": {"r": 255, "g": 255, "b": 255},
              "bg_color": {"r": 255, "g": 255, "b": 255},}
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
    ml.update_main_data()
    return jsonify({"effects": ml.effect_names})

@app.route('/effect', methods = ['GET', 'POST'])
def effect():
  global effect_data
  if request.method == "GET":
    return jsonify([ml.data])
  
  if request.method == "POST":
    spi_data = request.json
    # print(spi_data)
    effect_data["power"] = spi_data["power"] if "power" in spi_data else effect_data["power"]
    effect_data["speed"] = spi_data["speed"] if "speed" in spi_data else effect_data["speed"]
    effect_data["effect"] = spi_data["effect"] if "effect" in spi_data and spi_data["effect"] != effect_data["effect"] else effect_data["effect"]
    effect_data["main"] = spi_data["main"]/100 if "main" in spi_data else effect_data["main"]
    effect_data["fg_color"] = spi_data["fg_color"] if "fg_color" in spi_data else effect_data["fg_color"]
    effect_data["bg_color"] = spi_data["bg_color"] if "bg_color" in spi_data else effect_data["bg_color"]


    return jsonify({'value': 200})

@app.route('/textscroll', methods = ['GET', 'POST'])
def textscroll():
  if request.method == "GET":
    return jsonify({"status": 200})
  
  if request.method == "POST":
    text_data = request.json
    try:
        create_text_scroll(text_data["name"],
                        text_data["scrollText"],
                        int(text_data["height"]),
                        int(text_data["top"]),
                        text_data["font"])
    except Exception as e:
        print(e)
    
    return jsonify({"status": 200})