import json

with open('./chat_data/nBZTIJHZZm0/chat_file_0000.json') as f:
    jsn = json.load(f)
#5分=300秒
start_time = jsn["chat1"]["datetime"] // 1000
diff = 30 #秒
coments = []
all_coments = []

section_start = start_time

for k in jsn.keys():
    timestamp = jsn[k]["datetime"] // 1000
    coment = jsn[k]["message"]
    coments.append(coment)
    if timestamp - section_start >= 30:
        all_coments.append(coments)
        coments = []
        section_start = timestamp

macth_count = 0
macth_counts = {}

for i in range(len(all_coments)):
    for j in range(len(all_coments[i])):
        if "w" in all_coments[i][j] or "草" in all_coments[i][j] or "ｗ" in all_coments[i][j]:
            macth_count += 1
    macth_counts[i*diff] = macth_count
    macth_count = 0

ranking = sorted(macth_counts.items(), key=lambda x:x[1])
#print(ranking[-1][0]) 一番多かった区間

import csv
top_n = 3
columns = []

for i in range(top_n):
    column = [str(ranking[(i+1)*-1][0]), str(ranking[(i+1)*-1][0]+180)]
    columns.append(column)
print(columns)

with open('test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(columns)
