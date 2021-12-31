from flask import Flask, jsonify, request
from gpiozero import LED

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
    return jsonify({"r": 0, "g": 0, "b": 0})
  
  if request.method == "POST":
    print(request.json)
    
    return jsonify({'value': 200})

# not needed in author
# if __name__ == '__main__':
#   app.run( host='0.0.0.0', port=8000, debug=False )