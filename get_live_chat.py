import pytchat
import time
import json
import os

chat_max_cnt = 32760

def makeNewFile(file_path):
    with open(file_path, 'w') as f:
        pass

def getLiveChat(video_id):
    livechat = pytchat.create(video_id=video_id)

    # 一つ一つのコメントに対してユニークな値をあたえる必要があるから
    # コメントを約2^15個ごとにファイルを分けている。
    # chat_cntはファイル内のコメントのindex。
    chat_cnt = 0
    file_cnt = 0

    dir_path = f'chat_data/{video_id}'

    if os.path.exists(dir_path):
        print('dir already exists')
    else:
        print('made a new dir')
        os.mkdir(dir_path)

    file_path = f'chat_data/{video_id}/chat_file_{file_cnt:0>4}.json'

    makeNewFile(file_path)

    while livechat.is_alive():
        # チャットデータの取得
        chatdata = livechat.get()

        temp_data = dict()

        if chat_cnt == 0:
            chat_data = dict()
        else:
            with open(file_path, 'r') as f:
                chat_data = json.load(f)

        for c in chatdata.items:
            print(f"{c.timestamp} {c.author.name} {c.message} {c.amountString}")
            temp_data[f'chat{chat_cnt}'] = {'timestamp': c.timestamp, 'author.name': c.author.name, 'message': c.message, 'amountString': c.amountString}
            chat_cnt += 1

        chat_data.update(temp_data)

        with open(file_path, 'w') as f:
            json.dump(chat_data, f, indent=4)

        if chat_cnt >= chat_max_cnt:
            chat_cnt = 0
            file_cnt += 1
            file_path = f'chat_data/{video_id}/chat_file_{file_cnt:0>4}.json'
            makeNewFile(file_path)

        time.sleep(5)

if __name__ == '__main__':
    video_id = input()
    getLiveChat(video_id)