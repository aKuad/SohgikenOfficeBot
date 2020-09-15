#
# boss/boss_list.py
#
# -*- coding: UTF-8 -*-
#

# Module import
## Standard & Extension modules
import requests
import os
import sys


# Function define
def boss_list(TOKEN_BEARER, datas):
  # Get cause list
  ## Send request and receive
  get_url = "https://slack.com/api/conversations.replies?token=" + TOKEN_BEARER + "&ts=" + os.environ['S_MSGTS_BOSS_TEXT']
  get_head = {"Content-type": "application/json; charset=UTF-8;"}
  get_data = requests.get(post_url, headers=post_head)
  get_dic = json.loads(get_data.text)

  ## Process received string
  var_atlist = []
  var_rslist = []
  for stt_dcpart in get_dic["messages"]:
    if stt_dcpart["thread_ts"] == os.environ['S_MSGTS_BOSS_TEXT'] and stt_dcpart["ts"] != os.environ['S_MSGTS_BOSS_TEXT']:
      var_atlist.append(stt_dcpart["text"].split("\n", 1)[0])
      var_rslist.append(stt_dcpart["text"].split("\n", 1)[1])


  # Make & post message
  post_text = ""
  for stt_i in range(len(var_rslist)):
    post_text += str(stt_i + 1) + ". " + var_rslist[stt_i] + " | by " + var_atlist[stt_i] + "\n"
  post_url = "https://slack.com/api/chat.postEphemeral"
  post_body = {
    "channel": datas["channel_id"],
    "user": datas["user_id"],
    "as_user": True,
    "text": post_text,
    "attachments": [
      {
        "color": "warning",
        "title": "List of reason of deth",
        "text": post_text,
        "footer": "SohgikenOfficeBot `/boss`"
      }
    ]
  }
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)


  # Quit
  return
