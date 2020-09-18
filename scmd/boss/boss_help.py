# coding=UTF-8
#
# boss/boss_help.py
#

# Module import
## Standard & Extension modules
import requests


# Function define
def boss_help(TOKEN_BEARER, datas):
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
            "text": { "type": "mrkdwn", "text": "Print a cause of boss death in a random" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "Useage (print): `/boss [options] [index]`" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "Useage (operate): `/boss <sub command> <argument>`" }
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
            "text": { "type": "mrkdwn", "text": "`add <string>` `a <string>` : Add a cause of death" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`list` `l` : Print a list  of posted causes" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`delete <index>` `d <index>` : Delete a cause which is selected index" }
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
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": "`-b` `--big` : Print with big image" }
          }
        ],
      },
      {
        "text": "",
        "footer": "SohgikenOfficeBot `/boss`"
      }
    ]
  }
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)


  # Quit
  return
