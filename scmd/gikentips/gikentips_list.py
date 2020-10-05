# coding=UTF-8
#
# gikentips/gikentips_list.py
#

# Module import
## Standard & Extension modules
import requests
import json
import os


# Function define
def gikentips_list(TOKEN_BEARER, datas):
  # Get cause list
  ## Send request and receive
  get_url = "https://slack.com/api/conversations.replies?token=" + TOKEN_BEARER + "&channel=" + os.environ['S_CHID_BOTCDN'] + "&ts=" + os.environ['S_MSGTS_GTIPS']
  get_head = {"Content-type": "application/json; charset=UTF-8;"}
  get_data = requests.get(get_url, headers=get_head)
  get_dic = json.loads(get_data.text)

  ## Process received string
  var_atlist = []
  var_cdlist = []
  if get_dic["ok"] == True:
    for stt_dcpart in get_dic["messages"]:
      if stt_dcpart["thread_ts"] == os.environ['S_MSGTS_GTIPS'] and stt_dcpart["ts"] != os.environ['S_MSGTS_GTIPS']:
        var_atlist.append(stt_dcpart["text"].split("\n", 1)[0])
        var_cdlist.append(stt_dcpart["text"].split("\n", 1)[1])


  # Make post headder
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}


  # Branch with cause of death count is 0 or not
  ## When cause count is not 0
  if len(var_cdlist) != 0:
    # Make & post message
    post_text = ""
    for stt_i in range(len(var_cdlist)):
      post_text += str(stt_i + 1) + ". " + var_cdlist[stt_i] + " | by " + var_atlist[stt_i] + "\n"
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "warning",
          "title": "List of giken tips",
          "text": post_text,
          "footer": "SohgikenOfficeBot `/gikentips`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)

  ## When cause count is 0
  else:
    # Make & post message
    post_text = ""
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "warning",
          "text": "No items for giken tips list.",
          "fields": [
            { "title": "To add cause of death:", "value": "`/gikentips add <string>`", "short": False },
            { "title": "To see more help:", "value": "`/gikentips --help`", "short": False },
          ],
          "footer": "SohgikenOfficeBot `/gikentips`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)


  # Quit
  return
