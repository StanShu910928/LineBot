from flask import Flask, request


# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = 'hh8zCFd+m99yTw8Cdm4pr22jJndsvc5nx/IkP4uUfCEqzoaIM85+LxIsUF6lqL2cFSpYx0c+SSXoXl3n4ql1ES4fLS+BhkZsVWA1yssaSXdOUb2gxBiuF0TH+jSs9o4DtwMmgDZgseH2WymlLtHGugdB04t89/1O/w1cDnyilFU='
        secret = '30b18edbe6f4b7719f6601fa4fc647bc'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        line_bot_api.reply_message(tk,TextSendMessage(msg))  # 回傳訊息
        print(msg, tk)                                       # 印出內容
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                 # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
  app.run()