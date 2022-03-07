import pytchat
import time
import json

def loadJson(video_id,file_cnt):
    file_path = f'chat_data/{video_id}/chat_file_{file_cnt:0>4}.json'

    with open(file_path, 'r') as f:
        chat_data = json.load(f)
    return chat_data

def countSectionSuperChat(chat_data,interval_time = 10000):
    '''
    sectioned_superchat_cnt : 一定区間ごとのスーパーチャットの個数のリスト
    base_time : 参照中の区間の開始時間
    '''
    sectioned_superchat_cnt = []
    base_time = chat_data["chat0"]["timestamp"]
    sectioned_superchat_cnt.append(0)

    for key in chat_data.keys():
        if base_time + interval_time < chat_data[key]["timestamp"]:
            base_time += interval_time
            sectioned_superchat_cnt.append(0)

        if chat_data[key]["amountString"] != "":
            sectioned_superchat_cnt[-1] += 1

    return sectioned_superchat_cnt
if __name__ == "__main__":
    VIDEO_ID = "JPFFHu1X3gY"
    FILE_CNT = 0
    chat_data = loadJson(VIDEO_ID, FILE_CNT)
    print(countSectionSuperChat(chat_data))