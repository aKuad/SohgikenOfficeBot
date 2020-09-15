#
# boss/boss_print.py
#

# Module import
## Standard & Extension modules
import requests
import random
import os
import sys


# Function define
def boss_print(TOKEN_BEARER, datas, var_intext, flag_ephe, flag_smpl, flag_bimg):
  # Make post headder
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}


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


  # Get image url list
  ## Send request and receive
  get_url = "https://slack.com/api/conversations.replies?token=" + TOKEN_BEARER + "&ts=" + os.environ['S_MSGTS_BOSS_IMGURL']
  get_head = {"Content-type": "application/json; charset=UTF-8;"}
  get_data = requests.get(post_url, headers=post_head)
  get_dic = json.loads(get_data.text)

  ## Process received string
  var_iulist = []
  for stt_dcpart in data_dic["messages"]:
    if stt_dcpart["thread_ts"] == os.environ['S_MSGTS_BOSS_IMGURL'] and stt_dcpart["ts"] != os.environ['S_MSGTS_BOSS_IMGURL']:
      var_iulist.append(stt_dcpart["files"][0]["url_private"])


  # Argument check - Branch with argumeni is exist or not
  ## When argument is exist
  if var_intext != "":
    # Branch with argument is integer or not
    ## When argument is integer
    try:
      int(var_intext)
      # Branch with index is exist or not
      ## When exist index entered
      if 0 < int(var_intext) and int(var_intext) <= len(var_rslist):
        post_text = var_rslist[int(var_intext)]
        post_foot = var_atlist[int(var_intext)]
        post_imgu = var_iulist[random.randint(0, len(var_iulist) - 1)]
      ## When not exist index entered
      else:
        # Make & post warning message
        post_url = "https://slack.com/api/chat.postEphemeral"
        post_body = {
          "channel": datas["channel_id"],
          "user": datas["user_id"],
          "as_user": True,
          "text": "",
          "attachments": [
            {
              "color": "warning",
              "title": "Argument can't accepted",
              "text": "Warning - Invalid index '" + var_intext + "'. It is not exist index..",
              "fields": [
                { "title": "Useage:", "value": "`/boss [options] [index]`", "short": False },
                { "title": "To see more help:", "value": "`/boss --help`", "short": False },
              ],
              "footer": "SohgikenOfficeBot `/boss`"
            }
          ]
        }
        stt_result = requests.post(post_url, headers=post_head, json=post_body)
        print(stt_result.text)

        # Choice send reason and image in random
        post_text = var_rslist[random.randint(0, len(var_rslist) - 1)]
        post_foot = var_atlist[random.randint(0, len(var_atlist) - 1)]
        post_imgu = var_iulist[random.randint(0, len(var_iulist) - 1)]

    ## When argument is not integer
    except:
      # Make & post warning message
      post_url = "https://slack.com/api/chat.postEphemeral"
      post_body = {
        "channel": datas["channel_id"],
        "user": datas["user_id"],
        "as_user": True,
        "text": "",
        "attachments": [
          {
            "color": "warning",
            "title": "Argument can't accepted",
            "text": "Warning - Invalid index '" + var_intext + "'. It is not integer.",
            "fields": [
              { "title": "Useage:", "value": "`/boss [options] [index]`", "short": False },
              { "title": "To see more help:", "value": "`/boss --help`", "short": False },
            ],
            "footer": "SohgikenOfficeBot `/boss`"
          }
        ]
      }
      stt_result = requests.post(post_url, headers=post_head, json=post_body)
      print(stt_result.text)

      # Choice send reason and image in random
      post_text = var_rslist[random.randint(0, len(var_rslist) - 1)]
      post_foot = var_atlist[random.randint(0, len(var_atlist) - 1)]
      post_imgu = var_iulist[random.randint(0, len(var_iulist) - 1)]

  ## When argument is not exist
  else:
    # Choice send reason and image in random
    post_text = var_rslist[random.randint(0, len(var_rslist) - 1)]
    post_foot = var_atlist[random.randint(0, len(var_atlist) - 1)]
    post_imgu = var_iulist[random.randint(0, len(var_iulist) - 1)]


  # Branch with ephemeral option enable or not
  ## When ephemeral option is enable
  if True:
    post_url = "https://slack.com/api/chat.postEphemeral"
  ## When ephemeral option is not enable
  else:
    post_url = "https://slack.com/api/chat.postMessage"


  ## Print without ritch decoration
  if flag_smpl == True:
    # Make message
    post_body = {
      "channel": datas["channel_id"],
      "as_user": True,
      "text": "今日のボス: " + post_text
    }

  ## Print with normal size image
  elif flag_bimg == False:
    # Get user icon url
    get_data = requests.get("https://slack.com/api/users.info?token=" + TOKEN_BEARER + "&user=" + datas["user_id"])
    get_dic = json.loads(get_data.text)
    post_uico = recv_json["user"]["profile"]["image_72"]

    # Make message
    post_url = "https://slack.com/api/chat.postMessage"
    post_body = {
      "channel": datas["channel_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "danger",
          "author_icon": post_uico,
          "author_name": "<@" + datas["user_id"] + "|" + datas["user_name"] + ">",
          "title": "今日のボス",
          "text": post_text,
          "thumb_url": post_imgu,
          "footer": "Killed by: " + post_foot
        },
        {
          "color": "danger",
          "footer": "SohgikenOfficeBot `/boss`"
        }
      ]
    }

  ## Print with big size image
  else:
    # Get user icon url
    get_data = requests.get("https://slack.com/api/users.info?token=" + TOKEN_BEARER + "&user=" + datas["user_id"])
    get_dic = json.loads(get_data.text)
    post_uico = recv_json["user"]["profile"]["image_72"]

    # Make message
    post_url = "https://slack.com/api/chat.postMessage"
    post_body = {
      "channel": datas["channel_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "danger",
          "author_icon": post_uico,
          "author_name": "<@" + datas["user_id"] + "|" + datas["user_name"] + ">",
          "title": "今日のボス",
          "text": post_text,
          "image_url": post_imgu,
          "footer": "Killed by: " + post_foot
        },
        {
          "color": "danger",
          "footer": "SohgikenOfficeBot `/boss`"
        }
      ]
    }


  # Post message
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)


  # Quit
  return
