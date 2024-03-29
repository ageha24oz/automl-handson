from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)
from linebot.models import (
     MessageEvent, TextMessage, TextSendMessage, ImageMessage,
    StickerMessage, StickerSendMessage
)
import logging
import os
import sys
import random

app = Flask(__name__)

# ログを標準出力に出力する
app.logger.addHandler(logging.StreamHandler(sys.stdout))
# （レベル設定は適宜行ってください）
app.logger.setLevel(logging.ERROR)

#環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
#環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)



@app.route("/")
def hello_world():
    return "hello world!"
    
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

# テキストメッセージの場合
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = ''

    # ユーザ名を取得
    print(event.source)
    if event.source.type == 'user':
        profile = line_bot_api.get_profile(event.source.user_id)
    elif event.source.type == 'group':
        profile = line_bot_api.get_group_member_profile(
            event.source.group_id, event.source.user_id)
    elif event.source.type == 'room':
        profile = line_bot_api.get_room_member_profile(
            event.source.room_id, event.source.user_id)

    if profile is not None:
        name = profile.display_name
        message = name + 'さん\n'

    str_list = [
        '私以外私じゃないの あたりまえだけどね',
        '両成敗が止まらないもう泊まらない 呆れちゃうよな',
        'ダルマさんが転んだ あっかんべーあっかんべーって',
        '僕にはありあまる ロマンスがありあまる',
        'ぼんやり浮かぶ悲しいメロディー またふと流れる美しいメロディー',
        'たった今わかったんだ キラーボールが回る最中に',
        '戦ってしまうよ戦ってしまうよ 境界を観ながら',
        '猟奇的なキスを私にして 最後まで離さないで',
        'どうやって抱きしめたら 心が弄ばれないのか',
        '雨にまで流されて 影に紛れてたんだよ',
        'どうせアイツいつものように 色目使ってんでしょ',
        '誰が理想ってやつなんだ これが理想ってやつなんか？',
        'ホワイトなエッジが効いたワルツ 小気味良く鳴り響くワルツ',
        'ナイチンゲールが恋に落ちたって風の噂流れた',
        '今日もまた嫌なことばっかり 泣いたふりで避けてばっかり',
        '大人じゃないからさ 無理をしてまで笑えなくてさ'
    ]
    message += random.choice(str_list)
    send_message(event, message)

# スタンプメッセージの場合
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    sticker_list = [
        '51626496', '51626497', '51626502', '51626504',
        '51626508', '51626511', '51626517', '51626530'
    ]

    sticker_message = StickerSendMessage(
        package_id='11538',
        sticker_id=random.choice(sticker_list)
    )

    line_bot_api.reply_message(
        event.reply_token,
        sticker_message
    )


def send_message(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message)
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0", port=port)