# Error_analysis_project

是《误差理论与数据处理》课程大作业使用的代码

这篇大作业主要研究可否通过某些数据预测下一年的成果发表数量，使用到的数据有如往年平均成果数量，平均SCIE数量，平均SCI引用次数，平均英文和中文文献数量，入职年份等特征，建立多元线性回归模型，研究他们和成果发表数量的关系，将预测值和2018年文献发表数量进行对比研究显著性。


## 文件说明

整篇大作业由两部分组成，第一部分是获取过往研究成果数据，第二部分是对获得的数据进行多元线性回归

#### 获得数据

获取数据的部分使用的是Python的requests库和sqlite库编写爬虫脚本，通过对北航教师成果库网站上的公开数据爬取得到一千余在校教师的过往成果发表数据。工作分为两个部分：

1. [getID.py](https://github.com/wzm9856/Error_analysis_project/blob/master/getID.py) : 浏览各个学院的概览页获得每位教师的ID号
2. [getInfo.py](https://github.com/wzm9856/Error_analysis_project/blob/master/getInfo.py) : 用之前得到的ID直接进入每位教师的详情页进行数据的爬取。

最后将在文件所在目录创建名为 "homework.db" 的数据库文件。


#### 回归计算

回归计算的部分使用的是MATLAB语言。[First_approach.m](https://github.com/wzm9856/Error_analysis_project/blob/master/First_approach.m)和[calculate.m](https://github.com/wzm9856/Error_analysis_project/blob/master/calculate.m)是主文件及其配套的函数，其他文件均是在尝试更好的回归方法（虽然失败了）。
程序开始先读取上一步获得的数据库文件，再进行多元线性回归的计算，最终得到的回归系数和回归性检验结果保存在工作区，可以根据选择进行查看。


最终获得的显著性指标F=169.26，证明在0.01水平上结果高度显著。

