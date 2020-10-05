# coding=UTF-8
#
# gikentips/gikentips_help.py
#

# Module import
## Standard & Extension modules
import requests


# Function define
def gikentips_help(TOKEN_BEARER, datas):
  # Help page make & post
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}
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
            "text": { "type": "mrkdwn", "text": "Print an any giken tips in a random" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "Useage (print): `/gikentips [options]`" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "Useage (operate): `/gikentips <sub command> <argument>`" }
          },
          {
            "type": "header",
            "text": { "type": "plain_text", "text": "Sub commands", "emoji": True }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`--help` `help` : Print this manual" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`add <string>` `a <string>` : Add a giken tips" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`list` `l` : Print a list of posted tips" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`delete <index>` `d <index>` : Delete a tips which is selected index" }
          },
          {
            "type": "header",
            "text": { "type": "plain_text", "text": "Options", "emoji": True }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`-e` `--ephemeral` : Print in ephemeral message" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`-s` `--simple` : Print without ritch decoration" }
          }
        ],
      },
      {
        "text": "",
        "footer": "SohgikenOfficeBot `/gikentips`"
      }
    ]
  }
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)


  # Quit
  return
