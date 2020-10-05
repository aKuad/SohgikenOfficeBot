# coding=UTF-8
#
# gikentips/gikentips_print.py
#

# Module import
## Standard & Extension modules
import requests
import json
import random
import os


# Function define
def gikentips_print(TOKEN_BEARER, datas, flag_ephe, flag_smpl):
  # Make post headder
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}


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


  # Branch with cause of death count is 0 or not
  ## When cause count is 0
  if len(var_cdlist) == 0:
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
            { "title": "To add tips:", "value": "`/gikentips add <string>`", "short": False },
            { "title": "To see more help:", "value": "`/gikentips --help`", "short": False },
          ],
          "footer": "SohgikenOfficeBot `/gikentips`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)
    return


  # Choice send cause of death and image in random
  post_text = var_cdlist[random.randint(0, len(var_cdlist) - 1)]
  post_foot = var_atlist[random.randint(0, len(var_atlist) - 1)]


  # Branch with ephemeral option enable or not
  ## When ephemeral option is enable
  if flag_ephe == True:
    post_url = "https://slack.com/api/chat.postEphemeral"
  ## When ephemeral option is not enable
  else:
    post_url = "https://slack.com/api/chat.postMessage"


  ## Print without ritch decoration
  if flag_smpl == True:
    # Make message
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "Tips: " + post_text
    }
  else:
    # Get user icon url
    get_data = requests.get("https://slack.com/api/users.info?token=" + TOKEN_BEARER + "&user=" + post_foot.split("<@")[1].split("|")[0])
    get_dic = json.loads(get_data.text)
    post_uico = get_dic["user"]["profile"]["image_72"]

    # Make message
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "2E78B8",
          "author_icon": post_uico,
          "author_name": "<@" + datas["user_id"] + "|" + datas["user_name"] + ">",
          "title": "Tips",
          "text": post_text,
          "footer": "Advised by: " + post_foot,
          "footer_icon": post_uico
        },
        {
          "color": "2E78B8",
          "text": "",
          "footer": "SohgikenOfficeBot `/gikentips`"
        }
      ]
    }


  # Post message
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)


  # Quit
  return
