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
import formgo


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

  datas = request.form.to_dict()
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

  datas = request.form.to_dict()
  boss.boss(TOKEN_BEARER, datas)
  return ''

## Slash command '/formgo'
@app.route("/scmd/formgo", methods=['POST'])
def wh_scmd_formgo():
  print("---- Slash command 'formgo' has run ----")
  print(request.headers)
  print("body: %s" % request.get_data())

  if TOKEN_VERIFY != request.form.get("token"):
    return '''{"ok": false, "message": "Invalid token"}''', 401

  datas = request.form.to_dict()
  formgo.formgo(TOKEN_BEARER, datas)
  return ''

## Interactive process
@app.route("/sint", methods=['POST'])
def wh_sint():
  # Received request view and process
  print("---- Interactive action has run ----")
  print(request.headers)
  print("body-payload: %s" % request.form.get("payload"))
  datas = json.loads(request.form.get("payload"))

  # Token verifing
  if TOKEN_VERIFY != datas["token"]:
    return '''{"ok": false, "message": "Invalid token"}''', 401

  # Branch with payload type
  if datas["type"] == "shortcut":
    cbid = datas["callback_id"]
  elif datas["type"] == "view_submission":
    cbid = datas["view"]["callback_id"]
  else:
    print("Received type: " + datas["type"])
    return ''

  # Branch with 'callback_id'
  if cbid == "scmd_formgo":
    formgo.formgo(TOKEN_BEARER, datas)
  elif cbid == "sint_formgo_build":
    pass
  elif cbid == "sint_formgo_post":
    pass

  # Quit
  return ''

## 404 error response
@app.errorhandler(404)
def er_404(e):
  print ("---- Client error 404 ----")
  return '''{"ok": false, "message": "Invalid path"}''', 404


# App run
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=os.environ['PORT'])
