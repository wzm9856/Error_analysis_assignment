import sqlite3
import requests
import re


def getPage(DepartmentId, PageIndex):
    url = 'http://ir.lib.buaa.edu.cn/Scholar/MemberList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    data = {
        'DepartmentId': DepartmentId,
        'Keyword': '姓名/ORCID',
        'Order': 'FullName',
        'PageIndex': PageIndex,
        'PageSize': 16,
        'RecommendMember': 0
    }
    response = requests.post(url, headers=headers, data=data)
    print(type(response.status_code), response.status_code)
    response.encoding = "utf-8"

    patternID = re.compile("toggleAttention\\('(.*?)',this\\)")
    patternH = re.compile("<span>H指数：</span>(.*?)\\r")
    patternPaper = re.compile('成果：.*?_blank">(.*?)</a>')
    id_list = patternID.findall(response.text)
    if len(id_list) != 16:
        return False
    H_list = patternH.findall(response.text)
    Paper_list = patternPaper.findall(response.text)

    for a in range(0, 16):
        print(id_list[a])
        cursor.execute('INSERT INTO teachers (id, departmentId, indexH, totalPaper) VALUES (' + id_list[
            a] + ',' + str(DepartmentId) + ',' + H_list[a] + ',' + Paper_list[a] + ')')
    return True


if __name__ == '__main__':
    conn = sqlite3.connect('homework.db')
    cursor = conn.cursor()
    command = 'CREATE TABLE if not exists teachers (id INT PRIMARY KEY, departmentId INT, title CHAR(20), totalPaper INT, indexH INT, totalJournal INT, totalConf INT, totalSCIE INT, totalEI INT, SCIRecite INT, highRecite INT, en INT, cn INT, totalYear INT, y2018 INT)'
    print(command)
    cursor.execute(command)
           # id departmentId title totalPaper indexH totalJournal totalConf totalSCIE totalEI SCIRecite highRecite en cn totalYear y2018
    index = 0
    for d in [1,2,3,4,5,6,7,10,11,12,13,14,21]:
        while getPage(d, index):
            print([d, index])
            index = index + 1
        conn.commit()
        index = 1
    cursor.close()
    conn.commit()
    conn.close()
