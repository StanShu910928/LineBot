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
import subprocess
import re

# �]�w�A�� LINE Bot Channel Token �M Secret
LINE_CHANNEL_ACCESS_TOKEN = "hh8zCFd+m99yTw8Cdm4pr22jJndsvc5nx/IkP4uUfCEqzoaIM85+LxIsUF6lqL2cFSpYx0c+SSXoXl3n4ql1ES4fLS+BhkZsVWA1yssaSXdOUb2gxBiuF0TH+jSs9o4DtwMmgDZgseH2WymlLtHGugdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "30b18edbe6f4b7719f6601fa4fc647bc"

app = Flask(__name__)

# �]�w LINE Bot API �Ȥ��
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)

handler = WebhookHandler(LINE_CHANNEL_SECRET)

# �B�z LINE Webhook
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# �B�z���쪺����
@handler.add(MessageEvent, message=AudioMessageContent)
def handle_audio_message(event):
    # ���o���� ID
    message_id = event.message.id
    
    # �ѩ� v3 SDK ���ܰʡA�o�̨ϥ� HTTP �ШD����������ɤ��e
    # �o�O�@�Ӵ��N��סA�����ϥ� requests �w��������ɤ��e
    url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    
    # �x�s���ɡ]LINE ���ɬ� .m4a �榡�^
    audio_path = f"input.m4a"
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    # �ഫ���ɬ� .wav �榡
    wav_path = f"input.wav"
    audio = AudioSegment.from_file(audio_path, format="m4a")
    audio.export(wav_path, format="wav")

    # ���� Whisper ������O�����������G
    result = subprocess.run(["whisper", wav_path, "--model", "small", "--language", "Chinese"], capture_output=True, text=True)

    # ���� Whisper ���浲�G���������r
    transcript = result.stdout.strip()
 # �ϥΥ��h��F���h���ɶ��W
    clean_transcript = re.sub(r"\[.*?\]", "", transcript)

    # �p�G������\�A��^�����r�F�Y������ѫh��^���~�T��
    if clean_transcript:
        response_text = f"{clean_transcript.strip()}"
    else:
        response_text = "Fail"
    
    # �^�ХΤ�
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=response_text)]
        )
    )

# �Ұ� Flask ����
if __name__ == "__main__":
    app.run(port=5000)