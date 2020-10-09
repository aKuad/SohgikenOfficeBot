# coding=UTF-8
#
# boss/boss_delete.py
#

# Module import
## Standard & Extension modules
import requests
import json
import os


# Function define
def boss_delete(TOKEN_BEARER, datas, var_intext):
  # Make post headder
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}


  # Argument check (is empty)
  ## When argument is not integer
  if var_intext == "":
    # Make & post error message
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "danger",
          "title": "Failed to delete",
          "text": "Error - No argument.",
          "fields": [
            { "title": "Useage:", "value": "`/boss delete <index>`", "short": False },
            { "title": "To see more help:", "value": "`/boss --help`", "short": False },
          ],
          "footer": "SohgikenOfficeBot `/boss`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)
    return


  # Argument check (is integer)
  try:
    int(var_intext)
  ## When argument is not integer
  except:
    # Make & post error message
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "danger",
          "title": "Failed to delete",
          "text": "Error - Invalid argument '" + var_intext + "'. It is not integer.",
          "fields": [
            { "title": "Useage:", "value": "`/boss delete <index>`", "short": False },
            { "title": "To see more help:", "value": "`/boss --help`", "short": False },
          ],
          "footer": "SohgikenOfficeBot `/boss`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)
    return


  # Get cause list
  ## Send request and receive
  get_url = "https://slack.com/api/conversations.replies?token=" + TOKEN_BEARER + "&channel=" + os.environ['S_CHID_BOTCDN'] + "&ts=" + os.environ['S_MSGTS_BOSS_TEXT']
  get_head = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8;"}
  get_data = requests.get(get_url, headers=get_head)
  get_dic = json.loads(get_data.text)

  ## Process received string
  var_cdlist = []
  var_tslist = []
  if get_dic["ok"] == True:
    try:
      for stt_dcpart in get_dic["messages"]:
        if stt_dcpart["thread_ts"] == os.environ['S_MSGTS_BOSS_TEXT'] and stt_dcpart["ts"] != os.environ['S_MSGTS_BOSS_TEXT']:
          var_cdlist.append(stt_dcpart["text"].split("\n", 1)[1])
          var_tslist.append(stt_dcpart["ts"])
    except:
      pass


  # Argument check (is exist index)
  ## When exist index entered
  if 0 < int(var_intext) and int(var_intext) <= len(var_tslist):
    # Delete a cause in cdn channel
    post_url = "https://slack.com/api/chat.delete"
    post_body = {
      "channel": os.environ['S_CHID_BOTCDN'],
      "as_user": True,
      "ts": var_tslist[int(var_intext) - 1]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)

    # Make & post success message to user
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "good",
          "title": "Success to delete",
          "text": "Deleted '" + var_intext + ". " + var_cdlist[int(var_intext) - 1] + "'",
          "footer": "SohgikenOfficeBot `/boss`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)

  ## When not exist entered index
  else:
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "danger",
          "title": "Failed to delete",
          "text": "Error - Invalid index '" + var_intext + "'. It is not exist index.",
          "fields": [
            { "title": "Useage:", "value": "`/boss delete <index>`", "short": False },
            { "title": "To see more help:", "value": "`/boss --help`", "short": False },
          ],
          "footer": "SohgikenOfficeBot `/boss`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)


    # Quit
    return
