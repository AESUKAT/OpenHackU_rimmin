import json
import numpy as np
from sqlalchemy import null

def load_json_function(path_string):
    with open(path_string) as f:
        jsn = json.load(f)
    jsn = {k: v for k, v in jsn.items() if v["elapsedTime"][0] != "-"}
    return jsn

def total_time_calculation_function(jsn):
    last_key = list(jsn.keys())[-1]
    total_time = 0
    weight = [60000, 6000, null, 600, 60, null, 10, 1]
    last_key_time = jsn[last_key]["elapsedTime"]

    for i in range(-1, (len(last_key_time) + 1) * -1, -1):
        if last_key_time[i] != ":":
            total_time += int(last_key_time[i]) * weight[i]
    return total_time

def calculation_of_sections_function(jsn, total_time, section_time):
    #動画開始時間とコメント開始時間の差を求める
    weight = [60000, 6000, null, 600, 60, null, 10, 1]
    first_key = list(jsn.keys())[0]
    first_key_time = jsn[first_key]["elapsedTime"]
    start_time_diff = 0
    for i in range(-1, (len(first_key_time) + 1) * -1, -1):
        if first_key_time[i] != ":":
            start_time_diff += int(first_key_time[i]) * weight[i]
    start_time = jsn[first_key]["timestamp"] // 1000 - start_time_diff

    #区間ごとのコメントを集計する処理のための変数
    coments = []
    all_coments = []

    #区間ごとの"w"や"草"を求めるための変数
    macth_count = 0
    macth_counts = {}

    #区間ごとのコメントを集計する処理
    for i in range(total_time):
        findtime = start_time + i
        jsn_match = {k: v for k, v in jsn.items() if v["timestamp"] // 1000 == findtime}
        for k in jsn_match.keys():
            coment = jsn[k]["message"]
            coments.append(coment)
        all_coments.append(coments)
        coments = []
        jsn = {k: v for k, v in jsn.items() if v["timestamp"] // 1000 != findtime}

    #区間ごとの"w"や"草"の数を求めるための処理
    for i in range(len(all_coments)):
        for j in range(len(all_coments[i])):
            if "w" in all_coments[i][j] or "草" in all_coments[i][j] or "ｗ" in all_coments[i][j]:
                macth_count += 1
        macth_counts[i] = macth_count
        macth_count = 0

    #"w"や"草"の数が少ない順にソート
    ranking = sorted(macth_counts.items(), key=lambda x:x[1])
    # ranking_list -> 面白いと予想した区間
    ranking_list = [[ranking[-1][0], ranking[-1][0] + section_time],[ranking[-2][0], ranking[-2][0] + section_time],[ranking[-3][0], ranking[-3][0] + section_time]]
    #print(ranking_list)
    return ranking_list

def main():
    path_string = './chat_data/nBZTIJHZZm0/chat_file_0000.json'
    section_time = 30 #一区間は何秒か
    jsn = load_json_function(path_string)
    total_time = total_time_calculation_function(jsn)
    ranking_list = calculation_of_sections_function(jsn, total_time, section_time)

if __name__=="__main__":
    main()