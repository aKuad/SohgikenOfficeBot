# coding=UTF-8
#
# formgo_make.py
#

# Module import
import requests
import json
import os
import re


# Function define
def formgo_make(TOKEN_BEARER, datas):
  # Make answer thread message
  ## Branch with description is exist or not
  if datas["view"]["state"]["values"]["formgo_make_desc"]["formgo_make_desc"]["value"] == None:
    var_desc = u"_無し_"
  else:
    var_desc = datas["view"]["state"]["values"]["formgo_make_desc"]["formgo_make_desc"]["value"]

  ## Make user list
  get_url = "https://slack.com/api/users.list?token=" + TOKEN_BEARER
  get_head = { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8;" }
  get_data = requests.get(get_url, headers=get_head)
  get_dict = json.loads(get_data.text)
  var_tgus = ""
  for stt_uid in datas["view"]["state"]["values"]["formgo_make_member"]["formgo_make_member"]["selected_users"]:
    for stt_memb in get_dict["members"]:
      if stt_uid == stt_memb["id"]:
        var_tgus = "<@" + stt_uid + "|" + stt_memb["id"] + ">,"
  var_tgus = re.sub(",$", "", var_tgus)

  ## Make & post message
  post_url = "https://slack.com/api/chat.postMessage"
  post_head = { "Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER }
  post_body = {
    "as_user": True,
    "text": "",
    "channel": os.environ["S_CHID_FORM"],
    "attachments": [
      {
        "color": "2EB886",
        "blocks": [
          {
            "type": "header",
            "text": { "type": "plain_text", "text": datas["view"]["state"]["values"]["formgo_make_label"]["formgo_make_label"]["value"], "emoji": True }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": u":bar_chart: *フォームタイプ*\n" + datas["view"]["state"]["values"]["formgo_make_type"]["formgo_make_type"]["selected_option"]["text"]["text"] }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": u":page_facing_up: *フォーム説明*\n" + var_desc }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": u":busts_in_silhouette: *未回答者*\n" + var_tgus }
          }
        ]
      },
      {
        "color": "2EB886",
        "text": "",
        "footer": "SohgikenOfficeBot `/formgo`"
      }
    ]
  }
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)
  var_fmts = json.loads(stt_result.text)["ts"]


  # Make answer button message - Branch with form type
  ## Branch with description is exist or not
  if datas["view"]["state"]["values"]["formgo_make_desc"]["formgo_make_desc"]["value"] == None:
    var_desc = u"_無し_"
  else:
    var_desc = datas["view"]["state"]["values"]["formgo_make_desc"]["formgo_make_desc"]["value"]

  ## Make message body
  post_body = {
    "as_user": True,
    "text": "",
    "attachments": [
      {
        "color": "2EB886",
        "blocks": [
          {
            "type": "header",
            "text": { "type": "plain_text", "text": u"あなたが回答対象のフォームが作成されました。", "emoji": True }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": u":label: *" + datas["view"]["state"]["values"]["formgo_make_label"]["formgo_make_label"]["value"] + "*" }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": u":bar_chart: " + datas["view"]["state"]["values"]["formgo_make_type"]["formgo_make_type"]["selected_option"]["text"]["text"] }
          },
          {
            "type": "section",
            "text": { "type": "mrkdwn", "text": u":page_facing_up:" + var_desc }
          },
          {
            "type": "actions",
            "block_id": "sint_formgo_bpsh",
            "elements": [
              {
                "type": "button",
                "text": { "type": "plain_text", "text": u":pencil: 回答する", "emoji": True },
                "action_id": datas["view"]["state"]["values"]["formgo_make_type"]["formgo_make_type"]["selected_option"]["value"],
                "style": "primary",
                "value": var_fmts
              },
              {
                "type": "button",
                "text": { "type": "plain_text", "text": u":x: このメッセージを削除", "emoji": True },
                "action_id": "formgo_delete_nopost",
                "style": "danger",
                "value": var_fmts,
                "confirm": {
                  "title": { "type": "plain_text", "text": u"メッセージを削除しますか？" },
                  "text": { "type": "plain_text", "text": u"このフォームの送信はできなくなります。\n送信の必要が無いことを確かめた上で、メッセージを削除して下さい。" },
                  "confirm": { "type": "plain_text", "text": u"削除する" },
                  "deny": { "type": "plain_text", "text": u"キャンセル" },
                  "style": "danger"
                }
              }
            ]
          }
        ]
      },
      {
        "color": "2EB886",
        "text": "",
        "footer": "SohgikenOfficeBot `/formgo`"
      }
    ]
  }


  # Open and get direct message channel id
  get_url = "https://slack.com/api/conversations.open"
  get_head = { "Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER }
  for stt_uid in datas["view"]["state"]["values"]["formgo_make_member"]["formgo_make_member"]["selected_users"]:
    get_body = { "users": stt_uid }
    get_data = requests.post(get_url, headers=get_head, json=get_body)
    get_dict = json.loads(get_data.text)

    post_body["channel"] = get_dict["channel"]["id"]
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)


  # Post succeed message
  ## Get form owner DM id
  get_url = "https://slack.com/api/conversations.open"
  get_head = { "Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER }
  get_body = { "users": datas["user"]["id"] }
  get_data = requests.post(get_url, headers=get_head, json=get_body)
  get_dict = json.loads(get_data.text)

  ## Make & post message
  post_url = "https://slack.com/api/chat.postEphemeral"
  post_body = {
    "channel": get_dict["channel"]["id"],
    "user": datas["user"]["id"],
    "as_user": True,
    "text": "",
    "attachments": [
      {
        "color": "good",
        "title": ":heavy_check_mark: Form making has succeed.",
        "text": u"Form TS: " + var_fmts,
        "footer": "SohgikenOfficeBot `/formgo`"
      }
    ]
  }
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)


  # Quit
  return ''
