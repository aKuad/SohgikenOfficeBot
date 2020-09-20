# coding=UTF-8
#
# formgo.py
#

# Module import
import requests


# Function define
def formgo(TOKEN_BEARER, datas):
  # Make & post message
  post_head = {"Content-type": "application/json; charset=UTF-8;", "Authorization": "Bearer " + TOKEN_BEARER}
  post_url = "https://slack.com/api/dialog.open"
  post_body = {
    "trigger_id": datas["trigger_id"],
    "dialog": {
      "callback_id": "scmd_formgo",
      "title": { "type": "plain_text", "text": u"新規フォーム作成", "emoji": True },
      "type": "modal",
      "submit": { "type": "plain_text", "text": u":postbox: フォーム作成", "emoji": True },
      "close": { "type": "plain_text", "text": u":x: キャンセル", "emoji": True },
      "elements": [
        {
          "type": "input",
          "label": { "type": "plain_text", "text": u":label: フォームラベル", "emoji": True },
          "element": {
            "type": "plain_text_input",
            "multiline": False,
            "placeholder": { "type": "plain_text", "text": u"フォームラベルを入力" }
          },
          "hint": { "type": "plain_text", "text": u"このテキストは、複数のフォームの判別に用いられます", "emoji": True},
          "optional": False
        },
        {
          "type": "divider"
        },
        {
          "type": "input",
          "label": { "type": "plain_text", "text": u":bar_chart: フォームタイプ", "emoji": True },
          "element": {
            "type": "radio_buttons",
            "options": [
              {
                "text": { "type": "plain_text", "text": u":thermometer: 健康状態調査フォーム", "emoji": True },
                "value": "value-0"
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
          "label": {
            "type": "plain_text",
            "text": u":busts_in_silhouette: フォーム回答対象者",
            "emoji": True
          },
          "element": {
            "type": "multi_users_select",
            "placeholder": { "type": "plain_text", "text": u"フォーム回答の対象となるメンバー", "emoji": True }
          },
          "hint": { "type": "plain_text", "text": u"ここに入力されたメンバーに、フォーム回答ボタンが送信されます", "emoji": True },
          "optional": False
        },
        {
          "type": "divider"
        },
        {
          "type": "input",
          "label": { "type": "plain_text", "text": u":page_facing_up: フォーム説明", "emoji": True },
          "element": {
            "type": "plain_text_input",
            "multiline": True,
            "placeholder": { "type": "plain_text", "text": u"フォーム説明を入力", "emoji": True}
          },
          "hint": { "type": "plain_text", "text": u"このテキストは、フォーム回答者のダイアログに表示されます", "emoji": True },
          "optional": True
        }
      ]
    }
  }
  stt_result = requests.post(post_url, headers=post_head, json=post_body)
  print(stt_result.text)


  # Quit
  return
