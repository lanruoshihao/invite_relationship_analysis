# coding:utf-8

import pandas as pd
# import numpy as np
import networkx as nx
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def data_preprocess(file_path):
    file_open = open(file_path, 'r')
    invite_data = file_open.read()
    data_split = invite_data.split('\n')
    invite_data_list = []
    for data_line in data_split:
        invite_data_list.append(data_line.split(','))
    name_list = [u'被邀请者', u'邀请者']
    invite_df = pd.DataFrame(invite_data_list)
    invite_df.columns = name_list
    # print len(invite_df)
    return invite_df


def read_file(file_path):
    file_open = open(file_path, 'r')
    invite_data = file_open.read()
    data_split = invite_data.split('\n')
    invite_data_list = []
    for data_line in data_split:
        invite_data_list.extend(data_line.split(','))
    return invite_data_list


def construct_graph(invite_df):
    G = nx.DiGraph()
    for js in range(len(invite_df)):
        G.add_edge(invite_df.loc[js, u'邀请者'], invite_df.loc[js, u'被邀请者'])
    return G


def is_exist_path(G, invite_data1, invite_data2):
    data_flag = []
    for js_num in range(len(invite_data2)):
        flag = 0
        for js_cnt in range(len(invite_data1)):
            try:
                path_length_1, node_paths_1 = nx.single_source_dijkstra(G, invite_data2[js_num], invite_data1[js_cnt]) #计算网络中任意两个节点之间的路径长度以及路径上的节点数
                flag = 1
            except Exception:
                continue
            if flag == 1:
                data_flag.append(1)
                break
            try:
                path_length_2, node_paths_2 = nx.single_source_dijkstra(G, invite_data1[js_cnt], invite_data2[js_num]) #计算网络中任意两个节点之间的路径长度以及路径上的节点数
                flag = 1
            except Exception:
                continue
            if flag == 1:
                data_flag.append(1)
                break
        if flag == 0:
            data_flag.append(0)
    return data_flag


if __name__ == '__main__':
    file_path = u't_lxh_20190110_c.txt'

    invite_df = data_preprocess(file_path)
    G = construct_graph(invite_df)

    data_file1 = u'邀请关系数据_user2.txt'
    data_file2 = u'2019_02_20new_user_1.txt'

    user_data1 = read_file(data_file1)
    user_data2 = read_file(data_file2)
    data_flag = is_exist_path(G, user_data1, user_data2)
    pdf = pd.DataFrame()
    pdf['user1_id'] = user_data2
    pdf['data_flag'] = data_flag

    write_file_path = u'new_user_1_invite_data.txt'
    read_line = 0
    with open(write_file_path, 'w+') as f:
        for js_num in range(len(pdf)):
            read_line += 1
            f.write(','.join(str(ele) for ele in list(pdf.ix[js_num])))
            f.write('\n')
            print read_line
    f.close()


