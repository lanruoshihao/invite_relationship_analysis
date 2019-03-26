# coding:utf-8

import pandas as pd
import numpy as np
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


if __name__ == '__main__':
    file_path = u't_lxh_20190110_c.txt'
    invite_df = data_preprocess(file_path)
    node_dict, indegree0_node = construct_node_code(invite_df)

    print 'invite_df:', invite_df[u'邀请者']

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    G = nx.DiGraph()
    for df_len in range(100):
        G.add_edge(node_dict[invite_df.loc[df_len, u'邀请者']], node_dict[invite_df.loc[df_len, u'被邀请者']])
    # # nx.draw(G, node_color='r', with_labels=True, node_size=10, edge_color='b')
    nx.draw(G, node_color='r', with_labels=True, node_size=10, edge_color='b')
    plt.show()

