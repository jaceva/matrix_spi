from flask import Flask, jsonify, request, abort
from MatrixLeds import MatrixLeds
from effects import EffectManager

app = Flask(__name__)

matrix = MatrixLeds()
effects_manager = EffectManager()
matrix.next_frame()

# TODO use abort for error codes

@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

# TODO add configs as a dictionary
@app.route("/config", methods = ["GET"])
def get_config():
  if request.method == "GET":
    return jsonify(["CONFIGS"])

# TODO add effects as a dictionary
# Update effects list with post
@app.route("/effects", methods = ["GET", "POST"])
def effects():
  if request.method == "GET":
    return jsonify({
      "success": True, 
      "effects": effects_manager.get_effect_names()
    })
  
  # if request.method == "POST":
  #   new_data = request.json
  #   effs.append(new_data["effect_id"])

  #   return jsonify({
  #     "success": True, 
  #     "effects": effs,
  #   })

# TODO update active effect with post?
@app.route("/state", methods = ["GET", "POST"])
def set_state():
  '''Set effect and '''
  if request.method == "GET":
    return {
        "success": True,
        "state": matrix.get_data()
      }
  if request.method == "POST":
    state = request.json
    try:
      matrix.set_data(
        state['effect_id'], 
        state['speed'], 
        state['bright'],
        state['fg_color'],
        state['bg_color']
      )
    except Exception as e:
      print(f"Error: {e.with_traceback}")
      return jsonify({
        "success": False,
        "error": str(e)
      })
    print(matrix.get_data())

    return {
        "success": True,
        "state": matrix.get_data()
      }
