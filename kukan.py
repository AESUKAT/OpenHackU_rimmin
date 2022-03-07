import json

with open('chat_file_0000.json') as f:
    jsn = json.load(f)
start_time = jsn["chat1"]["datetime"] // 1000
diff = 40 #秒
section_time = 120
coments = []
all_coments = []

section_start = start_time
flag = True

#デバッグ用 総秒数
#print(jsn["chat5641"]["datetime"]//1000 - jsn["chat1"]["datetime"]//1000)

while flag:
    for k in jsn.keys():
        flag = False
        timestamp = jsn[k]["datetime"] // 1000
        coment = jsn[k]["message"]
        coments.append(coment)
        if timestamp - section_start >= section_time:
            all_coments.append(coments)
            jsn = {k: v for k, v in jsn.items() if v["datetime"] // 1000 > section_start}
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
    macth_counts[i*diff] = macth_count # i*diff キーをdiff秒飛ばしで登録するため
    macth_count = 0

ranking = sorted(macth_counts.items(), key=lambda x:x[1])
#print(ranking[-1][0]) 一番多かった区間

import csv
top_n = 3
columns = []

for i in range(top_n):
    column = [str(ranking[(i+1)*-1][0]), str(ranking[(i+1)*-1][0]+section_time)]
    columns.append(column)

with open('moment.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(columns)