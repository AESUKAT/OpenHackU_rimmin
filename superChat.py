import pytchat
import time
import json
import numpy

def loadJson(video_id,file_cnt):
    file_path = f'chat_data/{video_id}/chat_file_{file_cnt:0>4}.json'

    with open(file_path, 'r') as f:
        chat_data = json.load(f)
    return chat_data

def countSectionSuperChat(chat_data,interval_time = 10):
    '''
    sectioned_superchat_cnt : 一定区間ごとのスーパーチャットの個数のリスト
    base_time : 参照中の区間の開始時間
    '''
    sectioned_superchat_cnt = []
    base_time = chat_data["chat0"]["timestamp"]
    sectioned_superchat_cnt.append(0)

    for key in chat_data.keys():
        elapsed_time = chat_data[key]["elapsedTime"]
        elapsed_time = elapsed_time.split(":")
        now_time = 0
        for i in range(len(elapsed_time)):
            now_time += (60**i)*int(elapsed_time[-(1+i)])
        
        if chat_data[key]["amountString"] != "":
            if len(sectioned_superchat_cnt) <= now_time:
                tmp = [0 for i in range(now_time - len(sectioned_superchat_cnt) + 1)]
                sectioned_superchat_cnt.extend(tmp)
                sectioned_superchat_cnt[now_time] += 1
            print(elapsed_time, chat_data[key]["amountString"])
    print(sectioned_superchat_cnt)
    
    return numpy.array(sectioned_superchat_cnt)

if __name__ == "__main__":
    VIDEO_ID = "EY62MO3bOPE"
    FILE_CNT = 0
    chat_data = loadJson(VIDEO_ID, FILE_CNT)
    
    countSectionSuperChat(chat_data)