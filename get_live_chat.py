import pytchat
import time
import json
# PytchatCoreオブジェクトの取得

def getLiveChat(video_id):
    livechat = pytchat.create(video_id=video_id)

    file_path = f'comment_data/{video_id}.json'

    with open(file_path, 'w') as f:
        pass

    while livechat.is_alive():
        # チャットデータの取得
        chatdata = livechat.get()

        comment_data = []

        for c in chatdata.items:
            print(f"{c.datetime} {c.author.name} {c.message} {c.amountString}")
            comment_data.append({'datetime': c.datetime, 'author.name': c.author.name, 'message': c.message, 'amountString': c.amountString})

        with open(file_path, 'a') as f:
            json.dump(comment_data, f, indent=4)
        time.sleep(5)

if __name__ == '__main__':
    video_id = "SeWzXV0fYOM"
    getLiveChat(video_id)