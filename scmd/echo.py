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
  flag_ephe = False
  flag_smpl = False
  post_text = datas["text"]


  # Argument check - is argument exist
  ## When argument is exist
  if datas["text"] != "":
    # Divide with space and loop
    for stt_txpart in datas["text"].split():
      if stt_txpart == "--help":
        flag_help = True
        post_text = re.sub("^ *--help", "", post_text)
        post_text = re.sub("^ *", "", post_text)
      elif stt_txpart == "-e" or stt_txpart == "--ephemeral":
        flag_ephe = True
        post_text = re.sub("^ *(-e|--ephemeral)", "", post_text)
        post_text = re.sub("^ *", "", post_text)
      elif stt_txpart == "-s" or stt_txpart == "--simple":
        flag_smpl = True
        post_text = re.sub("^ *(-s|--simple)", "", post_text)
        post_text = re.sub("^ *", "", post_text)
      else:
        break
  ## When argument is not exist  
  else:
    # Print help page
    flag_help = True


  # Argument check - is echo string is exist
  if post_text == "":
    # Print help page
    flag_help = True


  # Make post headder
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}


  # Switch help page or not
  ## When help page print flag is true
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
          "blocks": [
            {
              "type": "header",
              "text": { "type": "plain_text", "text": "Desctiption & Useage", "emoji": True }
            },
            {
              "type": "section",
              "text": { "type": "mrkdwn", "text": "Print a entered string" }
            },
            {
              "type": "section",
              "text": { "type": "mrkdwn", "text": "Useage: `/echo [options] <string>`" }
            },
            {
              "type": "header",
              "text": { "type": "plain_text", "text": "Options", "emoji": True }
            },
            {
              "type": "section",
              "text": { "type": "mrkdwn", "text": "`--help` : Print this manual" }
            },
            {
              "type": "section",
              "text": { "type": "mrkdwn", "text": "`-e` `--ephemeral` : Print in ephemeral message" }
            },
            {
              "type": "section",
              "text": { "type": "mrkdwn", "text": "`-s` `--simple` : Print without ritch decoration" }
            }
          ]
        },
        {
          "text": "",
          "footer": "SohgikenOfficeBot `/echo`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)

  ## When help page print flag is false
  else:
    # Branch with ephemeral flag is true or not
    post_url = ""
    if flag_ephe == True:
      post_url = "https://slack.com/api/chat.postEphemeral"
    else:
      post_url = "https://slack.com/api/chat.postMessage"

    # Branch with simple flag is true or not
    ## When true, print without ritch decoration
    if flag_smpl == True:
      # Make & post message
      post_body = {
        "channel": datas["channel_id"],
        "user": datas["user_id"],
        "as_user": True,
        "text": post_text
      }
      stt_result = requests.post(post_url, headers=post_head, json=post_body)
      print(stt_result.text)
    ## When false, print with ritch decoration
    else:
      # Get user icon url
      get_raw = requests.get("https://slack.com/api/users.info?token=" + TOKEN_BEARER + "&user=" + datas["user_id"])
      get_dic = json.loads(get_raw.text)
      post_uico = get_dic["user"]["profile"]["image_72"]

      # Make & post message
      post_body = {
        "channel": datas["channel_id"],
        "user": datas["user_id"],
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
      stt_result = requests.post(post_url, headers=post_head, json=post_body)
      print(stt_result.text)


  # Quit
  return
