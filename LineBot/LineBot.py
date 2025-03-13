from flask import Flask, request


# ���J LINE Message API �����禡�w
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # ���o���쪺�T�����e
    try:
        json_data = json.loads(body)                         # json �榡�ưT�����e
        access_token = 'hh8zCFd+m99yTw8Cdm4pr22jJndsvc5nx/IkP4uUfCEqzoaIM85+LxIsUF6lqL2cFSpYx0c+SSXoXl3n4ql1ES4fLS+BhkZsVWA1yssaSXdOUb2gxBiuF0TH+jSs9o4DtwMmgDZgseH2WymlLtHGugdB04t89/1O/w1cDnyilFU='
        secret = '30b18edbe6f4b7719f6601fa4fc647bc'
        line_bot_api = LineBotApi(access_token)              # �T�{ token �O�_���T
        handler = WebhookHandler(secret)                     # �T�{ secret �O�_���T
        signature = request.headers['X-Line-Signature']      # �[�J�^�Ǫ� headers
        handler.handle(body, signature)                      # �j�w�T���^�Ǫ�������T
        msg = json_data['events'][0]['message']['text']      # ���o LINE ���쪺��r�T��
        tk = json_data['events'][0]['replyToken']            # ���o�^�ǰT���� Token
        line_bot_api.reply_message(tk,TextSendMessage(msg))  # �^�ǰT��
        print(msg, tk)                                       # �L�X���e
    except:
        print(body)                                          # �p�G�o�Ϳ��~�A�L�X���쪺���e
    return 'OK'                 # ���� Webhook �ϥΡA����ٲ�
if __name__ == "__main__":
  app.run()