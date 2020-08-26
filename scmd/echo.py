#
# echo.py
#

import requests

def echo(TOKEN, datas):
  post_url = "https://slack.com/api/chat.postMessage"
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN}
  post_body = {
    "channel": datas["channel_id"],
    "as_user": True,
    "text": "",
    "attachments": [
      {
        "color": "good",
        "text": datas["text"],
        "footer": "by <@" + datas["user_id"] + "|" + datas["user_name"] + ">"
      }
    ]
  }

  result = requests.post(post_url, headers=post_head, json=post_body)

  return result.text
