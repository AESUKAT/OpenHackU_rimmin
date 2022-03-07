import json
import numpy as np

with open('./chat_data/SeWzXV0fYOM/chat_file_0000.json') as f:
    jsn = json.load(f)

jsn = {k: v for k, v in jsn.items() if v["elapsedTime"] != "-"}

first_key = list(jsn.keys())[0]
last_key = list(jsn.keys())[-1]
seconds = (jsn[last_key]["timestamp"] // 1000) - (jsn[first_key]["timestamp"] // 1000)

start_time = jsn["chat0"]["timestamp"] // 1000
diff = 10 #秒
section_time = 30
coments = []
all_coments = []

section_start = start_time
flag = True

while flag:
    for k in jsn.keys():
        flag = False
        timestamp = jsn[k]["timestamp"] // 1000
        coment = jsn[k]["message"]
        coments.append(coment)
        if timestamp - section_start >= section_time:
            all_coments.append(coments)
            jsn = {k: v for k, v in jsn.items() if v["timestamp"] // 1000 > section_start}
            coments = []
            section_start += diff
            flag = True
            break

macth_count = 0
macth_counts = {}

for i in range(len(all_coments)):
    for j in range(len(all_coments[i])):
        if "w" in all_coments[i][j] or "草" in all_coments[i][j] or "ｗ" in all_coments[i][j]:
            macth_count += 1
    macth_counts[i*diff] = macth_count # i*diff キーをdiff秒飛ばしで登録→区間抜き出しの手抜きのため
    macth_count = 0

ranking = sorted(macth_counts.items(), key=lambda x:x[1])
ranking_list = [[ranking[-1][0], ranking[-1][0] + section_time],[ranking[-2][0], ranking[-2][0] + section_time],[ranking[-3][0], ranking[-3][0] + section_time]]

time_weight = np.array([0] * seconds)
for l in ranking_list:
    time_weight[l[0]:l[1]+1] += 1