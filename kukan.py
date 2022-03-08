import json
import numpy as np
from sqlalchemy import null

with open('./chat_data/nBZTIJHZZm0/chat_file_0000.json') as f:
    jsn = json.load(f)

jsn = {k: v for k, v in jsn.items() if v["elapsedTime"][0] != "-"}
first_key = list(jsn.keys())[0]
last_key = list(jsn.keys())[-1]

last_key_time = jsn[last_key]["elapsedTime"]
total_time = 0
weight = [60000, 6000, null, 600, 60, null, 10, 1]

#動画総時間の計算
for i in range(-1, (len(last_key_time) + 1) * -1, -1):
    if last_key_time[i] != ":":
        total_time += int(last_key_time[i]) * weight[i]
print(total_time)

#セクション開始と動画の同期
first_key_time = jsn[first_key]["elapsedTime"]
start_time_diff = 0
for i in range(-1, (len(first_key_time) + 1) * -1, -1):
    if first_key_time[i] != ":":
        start_time_diff += int(first_key_time[i]) * weight[i]

start_time = jsn[first_key]["timestamp"] // 1000 - start_time_diff

diff = 10 #秒
section_time = 30
coments = []
all_coments = []
flag = True
jsn_index = 0
timestamp = jsn[first_key]["timestamp"] // 1000
section_start = start_time

for i in range(total_time):
    findtime = start_time + i
    jsn_match = {k: v for k, v in jsn.items() if v["timestamp"] // 1000 == findtime}
    for k in jsn_match.keys():
        coment = jsn[k]["message"]
        coments.append(coment)
    all_coments.append(coments)
    coments = []
    jsn = {k: v for k, v in jsn.items() if v["timestamp"] // 1000 != findtime}

'''
while flag:
    for k in jsn.keys():
        flag = False
        timestamp = jsn[k]["timestamp"] // 1000
        coment = jsn[k]["message"]
        coments.append(coment)
        print(timestamp - section_start, section_time)
        if timestamp - section_start >= section_time:
            all_coments.append(coments)
            jsn = {k: v for k, v in jsn.items() if v["timestamp"] // 1000 > section_start}
            coments = []
            section_start += diff
            flag = True
            break
'''

macth_count = 0
macth_counts = {}

for i in range(len(all_coments)):
    for j in range(len(all_coments[i])):
        if "w" in all_coments[i][j] or "草" in all_coments[i][j] or "ｗ" in all_coments[i][j]:
            macth_count += 1
    macth_counts[i] = macth_count
    macth_count = 0

ranking = sorted(macth_counts.items(), key=lambda x:x[1])
ranking_list = [[ranking[-1][0], ranking[-1][0] + section_time],[ranking[-2][0], ranking[-2][0] + section_time],[ranking[-3][0], ranking[-3][0] + section_time]]

time_weight = np.array([0] * total_time)
for l in ranking_list:
    time_weight[l[0]:l[1]+1] += 1
np.set_printoptions(threshold=60000)