# coding=UTF-8
#
# formgo_bpsh.py
#

# Module import
import requests


# Function define
def formgo_bpsh(TOKEN_BEARER, datas):
  if datas["actions"][0]["action_id"] == "answer":
    print("## answer pushed ##")
    pass
  elif datas["actions"][0]["action_id"] == "delete":
    print("## delete pushed ##")
    pass

  # Make & post message
  return ''
