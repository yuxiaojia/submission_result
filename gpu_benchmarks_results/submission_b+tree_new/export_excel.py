
# import required module

import re
import pandas as pd
import os
import copy
import pathlib
# assign directory
directory = 'results'
list_hit = []
list_miss = []
list_access = []
list_hit_single = []
list_miss_single = []
list_access_single = []
list_shader = []
list_shader_single = []

#new
list_size = []
list_rp = []
list_folder = []
list_size_deep_copy = []
list_rp_deep_copy = []
list_folder_deep_copy = []
list_size_all = []
list_rp_all = []
list_folder_all = []
 
# iterate over files in
# that directory
j = 0
h = 0
h_track_outer_list = 0
m = 0
m_track_outer_list = 0
a = 0
a_track_outer_list = 0
total_h = 0
total_m = 0
total_a = 0
list_counter = 0
for filename in sorted(os.listdir(directory)):
    #print(filename)
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        continue
    
    # checking if it is a file
    count = 0
    for files in os.listdir(f):
        g = os.path.join(f, files)
        if files == "config.ini":
            with open(g, "r+") as file:
                config_text = file.readlines()
                for line in config_text:
                    count = count + 1
                    if line.strip() == "[system.ruby.tcc_cntrl0.L2cache]":
                        list_counter = list_counter + 1
                        list_size.append(config_text[count + 11])
                        list_folder.append(g)
                        list_rp.append(config_text[count + 17])
                        if list_counter == 12:
                            list_counter = 0

                            list_size_deep_copy = copy.deepcopy(list_size)
                            list_rp_deep_copy = copy.deepcopy(list_rp)
                            list_folder_deep_copy = copy.deepcopy(list_folder)

                            list_size_all.append(list_size_deep_copy)
                            list_rp_all.append(list_rp_deep_copy)
                            list_folder_all.append(list_folder_deep_copy)

                            list_folder.clear()
                            list_size.clear()
                            list_rp.clear()

        if files == "stats.txt":
            with open(g, "r") as file:
                text = file.read()
            results = re.findall("system.ruby.tcc_cntrl.+.L2cache.m_demand\w.+", text)
            i = 0
            for string in results:
                num = re.split("\s+", string)
                if i % 3 == 0:
                    #print("hit")
                    h = h + 1
                    h_track_outer_list = h_track_outer_list + 1
                    total_h = total_h + int(num[1])
                    
                    if h == 8:
                        list_hit_single.append(total_h)
                        h = 0
                        total_h = 0
                    if h_track_outer_list == 96:
                        hit_deep_copy = copy.deepcopy(list_hit_single)
                        list_hit.append(hit_deep_copy)
                        list_hit_single.clear()
                        h_track_outer_list = 0
                    #print(num[1])
                if i % 3 == 1:
                    #print("miss")
                    m = m + 1
                    m_track_outer_list = m_track_outer_list + 1
                    total_m = total_m + int(num[1])
                    
                    if m == 8:
                        list_miss_single.append(total_m)
                        m = 0
                        total_m = 0
                    if m_track_outer_list == 96:
                        miss_deep_copy = copy.deepcopy(list_miss_single)
                        list_miss.append(miss_deep_copy)
                        list_miss_single.clear()
                        m_track_outer_list = 0
                    #print(num[1])
                if i % 3 == 2:
                    #print("access")
                    a = a + 1
                    a_track_outer_list = a_track_outer_list + 1
                    total_a = total_a + int(num[1])
                    
                    if a == 8:
                        list_access_single.append(total_a)
                        a = 0
                        total_a = 0
                    if a_track_outer_list == 96:
                        access_deep_copy = copy.deepcopy(list_access_single)
                        list_access.append(access_deep_copy)
                        list_access_single.clear()
                        a_track_outer_list = 0
                    #print(num[1])
                i = i + 1

            # search for shaderticks    
            result2 = re.search("system.cpu3.shaderActiveTicks\s+(\S+)", text)
            if result2:
                j = j + 1
                # print(j)
                data = result2.group(1)
                list_shader_single.append(data)
                if j == 12:
                    j = 0
                    shader_deep_copy = copy.deepcopy(list_shader_single)
                    list_shader.append(shader_deep_copy)
                    list_shader_single.clear()
                    
excel_rp = pd.DataFrame(list_rp_all,
                  columns=['256KB', '512KB', '1MB', '2MB', '4MB', '8MB','16MB', '32MB', '64MB', '128MB', '256MB', '512MB'], 
                  index=['fifo', 'lfu', 'lip', 'lru', 'mru', 'nru', 'rrip', 'second_chance', 'tree_plru'])

excel_folder = pd.DataFrame(list_folder_all,
                  columns=['256KB', '512KB', '1MB', '2MB', '4MB', '8MB','16MB', '32MB', '64MB', '128MB', '256MB', '512MB'], 
                  index=['fifo', 'lfu', 'lip', 'lru', 'mru', 'nru', 'rrip', 'second_chance', 'tree_plru'])

excel_size = pd.DataFrame(list_size_all,
                  columns=['256KB', '512KB', '1MB', '2MB', '4MB', '8MB','16MB', '32MB', '64MB', '128MB', '256MB', '512MB'], 
                  index=['fifo', 'lfu', 'lip', 'lru', 'mru', 'nru', 'rrip', 'second_chance', 'tree_plru'])

shader_excel = pd.DataFrame(list_shader,
                  columns=['256KB', '512KB', '1MB', '2MB', '4MB', '8MB','16MB', '32MB', '64MB', '128MB', '256MB', '512MB'], 
                  index=['fifo', 'lfu', 'lip', 'lru', 'mru', 'nru', 'rrip', 'second_chance', 'tree_plru'])


hit_excel = pd.DataFrame(list_hit,
                  columns=['256KB', '512KB', '1MB', '2MB', '4MB', '8MB','16MB', '32MB', '64MB', '128MB', '256MB', '512MB'], 
                  index=['fifo', 'lfu', 'lip', 'lru', 'mru', 'nru', 'rrip', 'second_chance', 'tree_plru'])

miss_excel = pd.DataFrame(list_miss,
                  columns=['256KB', '512KB', '1MB', '2MB', '4MB', '8MB','16MB', '32MB', '64MB', '128MB', '256MB', '512MB'], 
                  index=['fifo', 'lfu', 'lip', 'lru', 'mru', 'nru', 'rrip', 'second_chance', 'tree_plru'])


access_excel= pd.DataFrame(list_access,
                  columns=['256KB', '512KB', '1MB', '2MB', '4MB', '8MB','16MB', '32MB', '64MB', '128MB', '256MB', '512MB'], 
                  index=['fifo', 'lfu', 'lip', 'lru', 'mru', 'nru', 'rrip', 'second_chance', 'tree_plru'])


with pd.ExcelWriter('output.xlsx') as writer:  # doctest: +SKIP
    shader_excel.to_excel(writer, sheet_name='Sheet_name_shader')
    hit_excel.to_excel(writer, sheet_name='Sheet_name_hit')
    miss_excel.to_excel(writer, sheet_name='Sheet_name_miss')
    access_excel.to_excel(writer, sheet_name='Sheet_name_access')
    excel_rp.to_excel(writer, sheet_name='Sheet_name_rp')
    excel_size.to_excel(writer, sheet_name='Sheet_name_size')
    excel_folder.to_excel(writer, sheet_name='Sheet_name_folder')
