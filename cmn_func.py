import json
import numpy as np

LAST_CHAT_TIME = 0

def import_json_info(video_id):
    global LAST_CHAT_TIME
    file_path = f'chat_data/{video_id}/chat_file_0000.json'

    with open(file_path, 'r') as f:
        cgat_data = json.load(f)

    chat_data = {k: v for k, v in cgat_data.items() if v["elapsedTime"][0] != "-"}

    LAST_CHAT_TIME = chat_data[list(chat_data.keys())[-1]]['elapsedTime']
    
    return chat_data

def time_to_seconds(input_time):
    time = list(map(int, input_time.split(':')))
    print(time)
    hour = 0
    if len(time) > 2:
        hour = time.pop(0)
    minute = time[0]
    second = time[1]

    return hour*60*60 + minute*60 + second

def time_to_number_line(time_info_list):
    movie_seconds = time_to_seconds(LAST_CHAT_TIME)
    number_line = np.array([0] * movie_seconds)

    for time_info in time_info_list:
        temp_number_line = np.array([0] * movie_seconds)
        for time in time_info:
            for start_time, finish_time in time:
                temp_number_line[start_time:finish_time+1] = 1
        number_line += temp_number_line
    
    return number_line

def main():
    # video_id = input('plz input video_id:')
    video_id = 'SeWzXV0fYOM'

    chat_data = import_json_info(video_id)
    print(list(chat_data.keys())[:10])


if __name__ == '__main__':
    main()