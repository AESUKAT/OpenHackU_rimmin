import json
import numpy as np


START_TIME = 0
LAST_CHAT_TIME = 0

BEFORE_TIME = 5
AFTER_TIME = 5

FUNNY_SCORE_BORDER = 2


def import_json_info(video_id):
    global LAST_CHAT_TIME
    file_path = f'chat_data/{video_id}/chat_file_0000.json'

    with open(file_path, 'r') as f:
        cgat_data = json.load(f)

    chat_data = {k: v for k, v in cgat_data.items() if v["elapsedTime"][0] != "-"}

    LAST_CHAT_TIME = time_to_seconds(chat_data[list(chat_data.keys())[-1]]['elapsedTime'])
    
    return chat_data


def time_to_seconds(input_time):
    time = list(map(int, input_time.split(':')))
    hour = 0
    if len(time) > 2:
        hour = time.pop(0)
    minute = time[0]
    second = time[1]

    return hour*60*60 + minute*60 + second


def time_to_funny_clip(time_info_list):
    number_line = time_to_number_line(time_info_list)
    comb_funny_time = search_time(time_info_list)
    funny_clip = number_line_to_funny_clip(number_line, comb_funny_time)

    return funny_clip

def time_to_number_line(time_info_list):
    number_line = np.array([0] * LAST_CHAT_TIME)

    for time_info in time_info_list:
        temp_number_line = np.array([0] * LAST_CHAT_TIME)
        for time in time_info:
            if time[0] < START_TIME:
                time[0] = START_TIME
            if time[1] > LAST_CHAT_TIME:
                time[1] = LAST_CHAT_TIME
            temp_number_line[time[0]:time[1]+1] = 1
        number_line += temp_number_line
    
    return number_line


def search_time(time_info_list):
    comb_time_info = []
    for time_info in time_info_list:
        for time in time_info:
            comb_time_info.append(time)

    comb_time_info.sort(key=lambda x:x[0])
    
    is_next = True
    comb_funny_time = []
    for time in comb_time_info:
        if is_next:
            start_time = time[0]
            finish_time = time[1]
            is_next = False
        else:
            if time[0] < finish_time:
                finish_time = time[1]
            else:
                comb_funny_time.append([start_time, finish_time])
                is_next = True
    else:
        start_time = time[0]
        finish_time = time[1]
        comb_funny_time.append([start_time, finish_time])

    return comb_funny_time


def number_line_to_funny_clip(number_line, comb_funny_time):
    funny_clip = []
    for time in comb_funny_time:
        max_score = max(number_line[time[0]:time[1]+1])
        if max_score >= FUNNY_SCORE_BORDER:
            max_index = np.argmax(number_line[time[0]:time[1]+1] >= max_score)
            max_index += time[0]
            start_time = max_index - BEFORE_TIME
            finish_time = max_index + AFTER_TIME
            if start_time < START_TIME:
                start_time = START_TIME
            if finish_time > LAST_CHAT_TIME:
                finish_time = LAST_CHAT_TIME
            funny_clip.append([start_time, finish_time])

    return funny_clip


def main():
    import instantaneous

    # video_id = input('plz input video_id:')
    video_id = 'SeWzXV0fYOM'

    chat_data = import_json_info(video_id)

    funny_point_list = [instantaneous.get_inst_higher(chat_data)]

    funny_clip = time_to_funny_clip(funny_point_list)
    print(funny_clip)


if __name__ == '__main__':
    main()