# -*- coding: utf-8 -*-
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, 
    ApiClient, 
    MessagingApi, 
    ReplyMessageRequest, 
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, AudioMessageContent
import os
import requests
from pydub import AudioSegment

# 設定你的 LINE Bot Channel Token 和 Secret
LINE_CHANNEL_ACCESS_TOKEN = "hh8zCFd+m99yTw8Cdm4pr22jJndsvc5nx/IkP4uUfCEqzoaIM85+LxIsUF6lqL2cFSpYx0c+SSXoXl3n4ql1ES4fLS+BhkZsVWA1yssaSXdOUb2gxBiuF0TH+jSs9o4DtwMmgDZgseH2WymlLtHGugdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "30b18edbe6f4b7719f6601fa4fc647bc"

app = Flask(__name__)

# 設定 LINE Bot API 客戶端
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)

handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 處理 LINE Webhook
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理收到的音檔
@handler.add(MessageEvent, message=AudioMessageContent)
def handle_audio_message(event):
    # 取得音檔 ID
    message_id = event.message.id
    
    # 由於 v3 SDK 有變動，這裡使用 HTTP 請求直接獲取音檔內容
    # 這是一個替代方案，直接使用 requests 庫來獲取音檔內容
    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    # 儲存音檔（LINE 音檔為 .m4a 格式）
    audio_path = f"audio_{message_id}.m4a"
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    # 轉換音檔為 .wav 格式
    wav_path = f"audio_{message_id}.wav"
    audio = AudioSegment.from_file(audio_path, format="m4a")
    audio.export(wav_path, format="wav")
    
    # 這裡可以加上 Whisper 轉錄音檔的功能
    response_text = "Recording completed, converted to wav!"
    
    # 回覆用戶
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=response_text)]
        )
    )

# 啟動 Flask 應用
if __name__ == "__main__":
    app.run(port=5000)