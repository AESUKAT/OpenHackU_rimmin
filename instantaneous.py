import cmn_func

TIME_RANGE = 2
AVE_TIME_RANGE = 5
CHAT_INST_SPEED_MAG = 2

BEFORE_TIME = 15
AFTER_TIME = 45

def get_funny_range(funny_point):
    return [funny_point-BEFORE_TIME, funny_point+AFTER_TIME]

def get_inst_higher(chat_data):
    temp_time = cmn_func.time_to_seconds(chat_data[list(chat_data.keys())[0]]['elapsedTime'])
    chat_cnt_dict = dict()
    chat_cnt_dict[temp_time] = 1

    for value in chat_data.values():
        now = cmn_func.time_to_seconds(value['elapsedTime'])
        if (now - temp_time) >= TIME_RANGE:
            temp_time = now
            chat_cnt_dict[temp_time] = 1
        else:
            chat_cnt_dict[temp_time] += 1

    temp_key_list = []
    funny_point_list = []
    for i, (key, value) in enumerate(chat_cnt_dict.items()):
        if i > AVE_TIME_RANGE:
            temp_chat_cnt += chat_cnt_dict[temp_key_list[-1]]
            if chat_cnt_dict[key] > CHAT_INST_SPEED_MAG*(temp_chat_cnt/AVE_TIME_RANGE):
                funny_point_list.append(get_funny_range(key))
            temp_chat_cnt -= chat_cnt_dict[temp_key_list[0]]
            temp_key_list.pop(0)
            temp_key_list.append(key)
        elif i == AVE_TIME_RANGE:
            temp_chat_cnt = 0
            for key in temp_key_list:
                temp_chat_cnt += chat_cnt_dict[key]
            if chat_cnt_dict[key] > CHAT_INST_SPEED_MAG*(temp_chat_cnt/AVE_TIME_RANGE):
                funny_point_list.append(get_funny_range(key))
            temp_chat_cnt -= chat_cnt_dict[temp_key_list[0]]
            temp_key_list.pop(0)
            temp_key_list.append(key)
        else:
            temp_key_list.append(key)

    print(funny_point_list)

if __name__ == '__main__':
    # video_id = input('plz input video_id:')
    video_id = 'SeWzXV0fYOM'

    chat_data = cmn_func.import_json_info(video_id)

    get_inst_higher(chat_data)
