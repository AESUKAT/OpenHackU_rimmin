import cmn_func

TIME_RANGE = 2
AVE_TIME_RANGE = 5
CHAT_INST_SPEED_MAG = 5

CLIP_TIME = 20
TIME_RATIO = 1/4
LAG_TIME = 5

BEFORE_TIME = 0
AFTER_TIME = 0


def get_funny_range(funny_point):
    return [funny_point-BEFORE_TIME, funny_point+AFTER_TIME]


def set_time():
    global BEFORE_TIME, AFTER_TIME
    if CLIP_TIME * TIME_RATIO >= LAG_TIME:
        BEFORE_TIME = int(CLIP_TIME * TIME_RATIO)
    else:
        BEFORE_TIME = LAG_TIME
    AFTER_TIME = CLIP_TIME - BEFORE_TIME


def get_inst_higher(chat_data):
    set_time()

    key_time = cmn_func.time_to_seconds(chat_data[list(chat_data.keys())[0]]['elapsedTime'])
    chat_cnt_dict = dict()
    chat_cnt_dict[key_time] = 1

    for value in chat_data.values():
        now = cmn_func.time_to_seconds(value['elapsedTime'])
        while now >= (key_time + TIME_RANGE):
            key_time += TIME_RANGE
            chat_cnt_dict[key_time] = 0
        else:
            chat_cnt_dict[key_time] += 1

    temp_key_list = []
    funny_point_list = []
    for i, (key, value) in enumerate(chat_cnt_dict.items()):
        if i > AVE_TIME_RANGE:
            temp_chat_cnt += chat_cnt_dict[temp_key_list[-1]]
            if temp_chat_cnt != 0:
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

    return funny_point_list


if __name__ == '__main__':
    # video_id = input('plz input video_id:')
    video_id = 'YgMffyeAvZI'

    chat_data = cmn_func.import_json_info(video_id)

    funny_point_list = [get_inst_higher(chat_data)]

    funny_clip = cmn_func.time_to_funny_clip(funny_point_list)

    print(funny_clip)
