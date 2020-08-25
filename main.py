# coding: utf-8
#
# main.py

from flask import Flask, request
app = Flask(__name__)

@app.route("/hello", methods=['POST'])
def wh_hello():
  print ("---- Item Received ----")
  print (request.headers)
  print ("body: %s" % request.get_data())
  return '''{"ok": true, "message": "Hello from server"}'''

@app.errorhandler(404)
def er_404(e):
  print ("---- Client error 404 ----")
  return '''{"ok": false, "message": "Invalid path"}''', 404

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=$PATH)
