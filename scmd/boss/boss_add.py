#
# boss/boss_add.py
#

# Module import
## Standard & Extension modules
import requests
import os
import sys


# Function define
def boss_add(TOKEN_BEARER, datas, var_intext):
  # Make post headder
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}


  # Branch with argument exist or not
  ## When argument is exist
  if var_intext != "":
    # Make & post posted cause to cdn channel
    post_url = "https://slack.com/api/chat.postMessage"
    post_body = {
      "channel": datas["channel_id"],
      "text": "<@" + datas["user_id"] + "|" + datas["user_name"] + ">\n" + var_intext
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
          "title": "Success to add",
          "text": "Added '" + var_intext + "'"
          "footer": "SohgikenOfficeBot `/boss`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)

  ## When argument is empty
  else:
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
          "title": "Failed to add",
          "text": "Error - No argument.",
          "fields": [
            { "title": "Useage:", "value": "`/boss add <string>`", "short": False },
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
