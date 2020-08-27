#
# echo.py
#

import requests
import json

def echo(TOKEN_BEARER, datas):
  # Get user icon url
  post_url = "https://slack.com/api/users.info?token=" + TOKEN_BEARER + "&user=" + datas["user_id"]
  recv_raw = requests.get(post_url)
  recv_txt = json.loads(recv_raw.text)
  recv_uico = recv_txt["user"]["profile"]["image_72"]

  # Make post content
  post_url = "https://slack.com/api/chat.postMessage"
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}
  post_body = {
    "channel": datas["channel_id"],
    "as_user": True,
    "text": "",
    "attachments": [
      {
        "color": "good",
        "author_icon": recv_uico,
        "author_name": "<@" + datas["user_id"] + "|" + datas["user_name"] + ">",
        "text": datas["text"],
        "footer": "SohgikenOfficeBot `/echo`"
      }
    ]
  }

  result = requests.post(post_url, headers=post_head, json=post_body)

  return result.text
