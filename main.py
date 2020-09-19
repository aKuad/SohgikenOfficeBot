# coding=UTF-8
#
# main.py
#

# Module import
## Standard & Extension modules
from flask import Flask, request
import json
import os
import sys

## Local modules
sys.path.append("./scmd")
import echo
import boss


# App object make and token load
app = Flask(__name__)
TOKEN_BEARER = os.environ['S_TOKEN_BEARER']
TOKEN_VERIFY = os.environ['S_TOKEN_VERIFY']


# App route define
## Server response test
@app.route("/hello", methods=['POST'])
def wh_hello():
  print ("---- Item Received ----")
  print (request.headers)
  print ("body: %s" % request.get_data())
  return '''{"ok": true, "message": "Hello from server"}'''

## Slash command '/echo'
@app.route("/scmd/echo", methods=['POST'])
def wh_scmd_echo():
  print ("---- Slash command 'echo' has run ----")
  print (request.headers)
  print ("body: %s" % request.get_data())

  if TOKEN_VERIFY != request.form.get("token"):
    return '''{"ok": false, "message": "Invalid token"}''', 401

  datas = {
    "channel_id": request.form.get("channel_id"),
    "user_id": request.form.get("user_id"),
    "user_name": request.form.get("user_name"),
    "text": request.form.get("text")
  }
  echo.echo(TOKEN_BEARER, datas)
  return ''

## Slash command '/boss'
@app.route("/scmd/boss", methods=['POST'])
def wh_scmd_boss():
  print("---- Slash command 'boss' has run ----")
  print(request.headers)
  print("body: %s" % request.get_data())

  if TOKEN_VERIFY != request.form.get("token"):
    return '''{"ok": false, "message": "Invalid token"}''', 401

  datas = {
    "channel_id": request.form.get("channel_id"),
    "user_id": request.form.get("user_id"),
    "user_name": request.form.get("user_name"),
    "text": request.form.get("text")
  }
  boss.boss(TOKEN_BEARER, datas)
  return ''

## Interactive process
@app.route("/sint", methods=['POST'])
def wh_sint():
  print("---- Interactive action has run ----")
  print(request.headers)
  print("bosy-payload: %s" % request.form.get("payload"))
  datas = json.loads(request.form.get("payload"))

  if TOKEN_VERIFY != datas["token"]:
    return '''{"ok": false, "message": "Invalid token"}''', 401

  return ''

## 404 error response
@app.errorhandler(404)
def er_404(e):
  print ("---- Client error 404 ----")
  return '''{"ok": false, "message": "Invalid path"}''', 404


# App run
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ['PORT'])
