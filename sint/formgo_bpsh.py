# coding=UTF-8
#
# formgo_bpsh.py
#

# Module import
import requests


# Function define
def formgo_bpsh(TOKEN_BEARER, datas):
  # Branch with pushed button
  ## When answer pushed
  if datas["actions"][0]["action_id"] == "formgo_type_health":
    # Make & post dialog
    post_url = "https://slack.com/api/views.open"
    post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}
    post_body = {
      "trigger_id": datas["trigger_id"],
      "view": {
        "callback_id": "sint_formgo_sbmt",
        "title": { "type": "plain_text", "text": u"健康状態調査フォーム", "emoji": True },
        "type": "modal",
        "submit": { "type": "plain_text", "text": u":incoming_envelope: 送信",	"emoji": True },
        "close": { "type": "plain_text",  "text": u":x: キャンセル", "emoji": True },
        "blocks": [
          {
            "type": "input",
            "label": { "type": "plain_text", "text": u":thermometer: 体温", "emoji": True },
            "element": {
            "type": "plain_text_input",
            "multiline": False,
            "placeholder": { "type": "plain_text", "text": u"体温を入力", "emoji": True }
          },
            "optional": False
          },
          {
            "type": "divider"
          },
          {
            "type": "input",
            "label": { "type": "plain_text", "text": u":heart: 体調", "emoji": True },
            "element": {
              "type": "radio_buttons",
              "options": [
                {
                  "text": { "type": "plain_text", "text": u":partyparrot: 絶好調", "emoji": True },
                  "value": "value-0"
                },
                {
                  "text": { "type": "plain_text", "text": u":yoshi: 良好", "emoji": True },
                  "value": "value-1"
                },
                {
                  "text": { "type": "plain_text", "text": u":face_with_thermometer: 不調", "emoji": True },
                  "value": "value-2"
                }
              ]
            },
            "optional": False
          },
          {
            "type": "divider"
          },
          {
            "type": "input",
            "label": { "type": "plain_text", "text": u":pencil: 備考", "emoji": True },
            "element": {
              "type": "plain_text_input",
              "multiline": True
            },
            "optional": True
          }
        ]
      }
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)

  ## When delete pushed
  elif datas["actions"][0]["action_id"] == "formgo_delete_nopost":
    # Message delete
    post_url = "https://slack.com/api/chat.delete"
    post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}
    post_body = {
      "channel": datas["channel"]["id"],
      "as_user": True,
      "ts": datas["message"]["ts"]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)

    # Succeed message send
    post_url = "https://slack.com/api/chat.postEphemeral"
    post_body = {
      "channel": datas["channel"]["id"],
      "user": datas["user"]["id"],
      "as_user": True,
      "text": "",
      "attachments": [
        {
          "color": "good",
          "title": u"メッセージを削除しました。",
          "text": u"未回答のまま閉じました。",
          "footer": "SohgikenOfficeBot `/formgo`"
        }
      ]
    }
    stt_result = requests.post(post_url, headers=post_head, json=post_body)
    print(stt_result.text)


  # Make & post message
  return ''
