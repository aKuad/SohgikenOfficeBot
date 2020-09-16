#
# echo.py
#

# Module import
import requests
import json
import re


# Function define
def echo(TOKEN_BEARER, datas):
  # Option check
  ## Variables initialize
  flag_help = False
  flag_smpl = False
  post_text = datas["text"]

  if datas["text"] == "":
    # When empty imput, print help
    flag_help = True
  else :
    # Divide with space and loop
    for stt_txpart in datas["text"].split():
      if stt_txpart == "--help":
        flag_help = True
        post_text = re.sub("^ *--help", "", post_text)
        post_text = re.sub("^ *", "", post_text)
      elif stt_txpart == "-s" or stt_txpart == "--simple":
        flag_smpl = True
        post_text = re.sub("^ *(-s|--simple)", "", post_text)
        post_text = re.sub("^ *", "", post_text)
      else :
        break


  # Switch help page or not
  ## Make post headder
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}

  if flag_help == True:
    # Help page print
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel_id"],
      "user": datas["user_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "title": "Help for `/echo`",
          "text": "",
          "blocks": [
            {
              "type": "header",
              "text": { "type": "plain_text", "text": "Desctiption & Useage", "emoji": True }
            },
            {
              "type": "section",
              "text": { "type": "plain_text", "text": "Print a entered string", "emoji": True }
            },
            {
              "type": "section",
              "text": { "type": "plain_text", "text": "Useage: `/echo [options] <string>`", "emoji": True }
            },
            {
              "type": "header",
              "text": { "type": "plain_text", "text": "Options", "emoji": True }
            },
            {
              "type": "section",
              "text": { "type": "plain_text", "text": "  `--help` : Print this manual", "emoji": True }
            },
            {
              "type": "section",
              "text": { "type": "plain_text", "text": "  `-s --simple` : Echo without ritch decoration", "emoji": True }
            }
          ],
          "footer": "SohgikenOfficeBot `/echo`"
        }
      ]
    }
  elif flag_smpl == True:
    # Echo without ritch decoration
    ## Make post message
    post_url = "https://slack.com/api/chat.postMessage"
    post_body = {
      "channel": datas["channel_id"],
      "as_user": True,
      "text": post_text
    }
  else :
    # Echo with ritch decoration
    ## Get user icon url
    get_raw = requests.get("https://slack.com/api/users.info?token=" + TOKEN_BEARER + "&user=" + datas["user_id"])
    get_dic = json.loads(get_raw.text)
    post_uico = get_dic["user"]["profile"]["image_72"]

    ## Make post message
    post_url = "https://slack.com/api/chat.postMessage"
    post_body = {
      "channel": datas["channel_id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "good",
          "author_icon": post_uico,
          "author_name": "<@" + datas["user_id"] + "|" + datas["user_name"] + ">",
          "text": post_text,
          "footer": "SohgikenOfficeBot `/echo`"
        }
      ]
    }


  # Post content
  result = requests.post(post_url, headers=post_head, json=post_body)


  # Quit
  return result.text
