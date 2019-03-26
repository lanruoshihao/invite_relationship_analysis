# coding:utf-8

import pandas as pd
# import numpy as np
from pylab import *
# import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
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
    print len(invite_df)
    invite_df.drop(index=[len(invite_df) - 1], inplace=True)
    return invite_df


def construct_node_code(invite_df):
    '''
    构建每个节点对应的编号
    :param invite_df:
    :return:
    '''
    invite_set = set(invite_df[u'邀请者'])
    invited_by_set = set(invite_df[u'被邀请者'])
    indegree0_node = list(invite_set.difference(invited_by_set))
    node_set = list(invite_set | invited_by_set)
    node_dict = {}
    for node_num in range(len(node_set)):
        node_dict[node_set[node_num]] = node_num + 1
    return node_dict, indegree0_node


def construct_graph(node_dict, invite_df):
    G = nx.DiGraph()
    for js in range(len(invite_df)):
        G.add_edge(node_dict[invite_df.loc[js, u'邀请者']], node_dict[invite_df.loc[js, u'被邀请者']])
    return G


def all_path_len(G, invite_df):
    node_dict, indegree0_node = construct_node_code(invite_df)
    path_len = [0 for node_code in indegree0_node]
    node_path = [0 for node_code in indegree0_node]
    for js_num in range(len(indegree0_node)):
        print u'入度节点编号：', indegree0_node[js_num]
        for node_key, node_value in node_dict.items():
            if node_key in indegree0_node:
                continue
            try:
                path_length, node_paths = nx.single_source_dijkstra(G, node_dict[indegree0_node[js_num]], node_value) #计算网络中任意两个节点之间的路径长度以及路径上的节点数
            except Exception:
                path_length, node_paths = 0, 0
            if path_length > path_len[js_num]:
                path_len[js_num], node_path[js_num] = path_length, node_paths
    return path_len, node_path


def max_value_and_path(path_len, node_path):
    max_value = np.max(path_len)
    max_node_path = []
    for js_count in range(len(path_len)):
        if path_len[js_count] == max_value:
            max_node_path.append(node_path[js_count])
    return max_node_path


if __name__ == '__main__':
    file_path = u't_lxh_20190110_c.txt'
    invite_df = data_preprocess(file_path)
    node_dict, indegree0_node = construct_node_code(invite_df)

    G_graph = construct_graph(node_dict, invite_df)

    groupby_data = invite_df.groupby(u'邀请者').agg('count')
    groupby_datalist = groupby_data.sort_values(by=u'被邀请者', ascending=False)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    path_len, node_path = all_path_len(G_graph, invite_df)
    max_node_path = max_value_and_path(path_len, node_path)

    for node_path_iter in max_node_path:
        print 'node_path_iter:', node_path_iter
        print 'len(node_path_iter)=', len(node_path_iter)
    for df_len in range(100):
        G_graph.add_edge(node_dict[invite_df.loc[df_len, u'邀请者']], node_dict[invite_df.loc[df_len, u'被邀请者']])
    nx.draw(G_graph, node_color='r', with_labels=True, node_size=10, edge_color='b')
    plt.show()

