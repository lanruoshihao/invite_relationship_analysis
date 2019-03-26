# invite_relationship_analysis

项目背景：根据部门领导提出的需求，根据代购之间的邀请关系，在公司代购数据记录表中发现一些有价值的信息。

数据来源：阿里大数据处理平台odps中的sql数据表

当时主要从以下三个方面来进行统计分析：

1、邀请关系网络中邀请人数排在top10的user_id(剔除掉公司内部的user_id)。

2、邀请关系网络中节点间的有向图绘制。

3、找出邀请关系网中的最大路径长度及其对应的节点编号。

4、计算任意两个代购之间是否存在邀请关系。


max_len_path_algorithms.py文件可根据公司所有代购形成的邀请网络关系计算邀请关系最长的路径；

is_exist_invite_relationship.py文件可根据用户user_id，计算任意两个代购之间是否存在直接或者间接的邀请关系。

项目中所用的工具：odps sql、pycharm+anaconda2
