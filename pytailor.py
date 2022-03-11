'''
import pytchat
import time
import json
import os
'''
import get_data
import cmn_func
import instantaneous
import numpy as np
import kukan
import autoPleyer
import superChat
import dB_determination

video_id = input('video idを入力してください→')
get_data.get_live_chat(video_id)
chat_data = cmn_func.import_json_info(video_id)
funny_point_list = instantaneous.get_inst_higher(chat_data)

path_string = "./chat_data/" + video_id + "/chat_file_0000.json"
section_time = 30 #一区間は何秒か
jsn = kukan.load_json_function(path_string)
total_time = kukan.total_time_calculation_function(jsn)
ranking_list = []
ranking_list = kukan.calculation_of_sections_function(jsn, total_time, section_time)

FILE_CNT = 0

super_chat_data = superChat.load_json(video_id, FILE_CNT)
super_chat_list = superChat.count_section_super_chat(super_chat_data)

target_url = "https://www.youtube.com/watch?v=" + video_id
dB_chapter_list = dB_determination.dB_determination(target_url)

concatenate_list = [funny_point_list, ranking_list, super_chat_list, dB_chapter_list]
#print('check_funny_point_list:' + str(funny_point_list))
#print('check:ranking_list    :' + str(ranking_list))
#print('check_super_chat_list :' + str(super_chat_list))
#print('check_dB_chapter_list :' + str(dB_chapter_list))
funny_clip = []
funny_clip = cmn_func.time_to_funny_clip(concatenate_list)
print('fun', funny_clip)

autoPleyer.call_selenium(target_url, funny_clip)
