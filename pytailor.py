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

video_id = 'JPFFHu1X3gY'
get_data.get_live_chat(video_id)
chat_data = cmn_func.import_json_info(video_id)
"""
chat_data = cmn_func.import_json_info(video_id)
funny_point_list = [instantaneous.get_inst_higher(chat_data)]
number_line = []
number_line = cmn_func.time_to_number_line(funny_point_list)
np.set_printoptions(threshold=60000)
print(number_line)
"""
path_string = "./chat_data/" + video_id + "/chat_file_0000.json"
section_time = 30 #一区間は何秒か
jsn = kukan.load_json_function(path_string)
total_time = kukan.total_time_calculation_function(jsn)
ranking_list = []
ranking_list = kukan.calculation_of_sections_function(jsn, total_time, section_time)

target_url = "https://www.youtube.com/watch?v=" + "JPFFHu1X3gY"
autoPleyer.call_selenium(target_url, ranking_list)