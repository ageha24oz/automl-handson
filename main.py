# インポートするライブラリ
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
)


# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__)




line_bot_api = LineBotApi('z4CdGyH921J8TOnPe1Z+FFtVCQ+ZNtOIvfJmimhD+Kcc0e+IrEIxJCgwoVMR7AI7mnJ9uQrzE2QdRTHV927nMapipSelbSDKfE672LBvhvqDFzVf8G3xSwuzR696nMi3PvhYPjTwnC7eHEbKFc10rAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7e1a4872c937789c5a8003c2d51d5add')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='「' + event.message.text + '」って何？')
     )

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=port)
    
