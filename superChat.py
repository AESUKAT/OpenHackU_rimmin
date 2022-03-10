import time
import json
import cmn_func
from math import ceil,floor

'''
def load_json(video_id,file_cnt):
    file_path = f'chat_data/{video_id}/chat_file_{file_cnt:0>4}.json'

    with open(file_path, 'r') as f:
        chat_data = json.load(f)
    return chat_data
'''
def count_section_super_chat(chat_data,interval_time = 10):

    sectioned_superchat_cnt = []
    sectioned_superchat_cnt.append(0)
    base_time = 10

    for key in chat_data.keys():

        elapsed_time = chat_data[key]["elapsedTime"]
        now_time = cmn_func.time_to_seconds(elapsed_time)
        

        if chat_data[key]["amountString"] != "":
            if base_time <= now_time:
                tmp = [0 for i in range(ceil((now_time - base_time + 1)/10))]
                sectioned_superchat_cnt.extend(tmp)
                base_time = len(sectioned_superchat_cnt)*10
            

            now_i = floor(now_time/10)
            #print(now_time,now_i)
            if now_i >= 0:
                sectioned_superchat_cnt[now_i] += 1

    sectioned_superchat_value = []
    for i in range(len(sectioned_superchat_cnt)-2):
        tmp = sectioned_superchat_cnt[i] + sectioned_superchat_cnt[i+1] + sectioned_superchat_cnt[i+2]
        sectioned_superchat_value.append(tmp)
    
    max_values = []
    for i in range(3):
        max_value = max(sectioned_superchat_value)
        max_index = sectioned_superchat_value.index(max_value)
        
        sectioned_superchat_value[max_index] = 0
        for j in range(1,3):
            if max_index+j < len(sectioned_superchat_value):
                sectioned_superchat_value[max_index+j] = 0
            if max_index-j > 0:
                sectioned_superchat_value[max_index-j] = 0
        
        max_index -= 6
        max_values.append([max_index*10,max_index*10+30])
    #print(numpy.array(max_values))
    return max_values   

if __name__ == "__main__":
    VIDEO_ID = "EY62MO3bOPE"
    FILE_CNT = 0
    chat_data = load_json(VIDEO_ID, FILE_CNT)

    count_section_super_chat(chat_data)