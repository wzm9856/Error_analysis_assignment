import re
import requests
import sqlite3


def getCiteInfo(id):
    url = 'http://ir.lib.buaa.edu.cn/Scholar/ScholarCard/' + str(id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    response.encoding = "utf-8"
    print(id, response.status_code)
    pattern1 = re.compile('SCI引用频次：<span>(.*?)<.*?单篇最高引用：.*?_blank">(.*?)<', flags=re.DOTALL)
    pattern2 = re.compile('职称.*?14px;">\r\n\s*(.*?)\r', flags=re.DOTALL)
    cite_list = pattern1.search(response.text)
    title = pattern2.search(response.text)
    if cite_list == None:
        cite_list = pattern1.search('SCI引用频次：<span>0<.*?单篇最高引用：.*?_blank">0<')
    command = 'UPDATE teachers SET SCIRecite = ' + str(cite_list.group(1)) + ',highRecite = ' + str(
        cite_list.group(2)) + ',title = \'' + title.group(1) + '\' WHERE id = ' + str(id)
    print(command)
    cursor.execute(command)


def getMoreInfo(id):
    url = 'http://ir.lib.buaa.edu.cn/Scholar/SchloarAchivement'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    data = {
        'currentBibType': '',
        'currentIndb': '',
        'currentYear': '',
        'currentProject': '',
        'currenLanguage': '',
        'Id': id,
        'PageIndex': 1,
        'PageSize': 20,
        'pageType': 0,
        'pageTypeVal': '公开成果',
        'searchValue': 0
    }
    response = requests.post(url, headers=headers, data=data)
    print(id, response.status_code)
    response.encoding = "utf-8"
    pattern1 = re.compile('期刊 <span style="color: ;">\\((.*?)\\)')
    pattern6 = re.compile('会议 <span style="color: ;">\\((.*?)\\)')
    pattern2 = re.compile('ndb">SCIE<span style="color: ;">\\((.*?)\\)')
    pattern3 = re.compile('indb">EI<span style="color: ;">\\((.*?)\\)')
    pattern4 = re.compile('外文<s.*?>\\((.*?)\\)')
    pattern5 = re.compile('中文<s.*?>\\((.*?)\\)')
    jour_list = pattern1.search(response.text)
    if jour_list == None:
        command = 'DELETE FROM teachers WHERE id = ' + str(id)
        print(command)
        cursor.execute(command)
        print(str(id) + ' deleted')
        return
    conf_list = pattern6.search(response.text)
    if conf_list == None:
        conf_list = pattern6.search('会议 <span style="color: ;">(0)')
    scie_list = pattern2.search(response.text)
    if scie_list == None:
        scie_list = pattern2.search('ndb">SCIE<span style="color: ;">(0)')
    ei_list = pattern3.search(response.text)
    if ei_list == None:
        ei_list = pattern3.search('indb">EI<span style="color: ;">(0)')
    en_list = pattern4.search(response.text)
    if en_list == None:
        en_list = pattern4.search('外文<s.*?>(0)')
    cn_list = pattern5.search(response.text)
    if cn_list == None:
        cn_list = pattern5.search('中文<s.*?>(0)')
    command = 'UPDATE teachers SET totalJournal=' + str(jour_list.group(1)) + ',totalConf=' + str(
            conf_list.group(1)) + ',totalSCIE=' + str(scie_list.group(1)) + ',totalEI=' + str(
            ei_list.group(1)) + ',en=' + str(en_list.group(1)) + ',cn=' + str(cn_list.group(1)) + ' WHERE id=' + str(
            id)
    print(command)
    cursor.execute(command)

    getCiteInfo(id)

    pattern2018=re.compile('nf-type="year">2018<span style="color: ;">\\((.*?)\\)</span></a>')
    num=pattern2018.search(response.text)
    command='UPDATE teachers SET y2018 = '+str(num.group(1))+' WHERE id = '+str(id)
    print(command)
    cursor.execute(command)

    for years in range(1, 40):
        pattern_year = re.compile(str(2019 - years))
        isexist = pattern_year.search(response.text)
        if isexist == None:
            command = 'UPDATE teachers SET totalYear=' + str(years - 1) + ' WHERE id=' + str(id)
            print(command)
            cursor.execute(command)
            return
    command = 'UPDATE teachers SET totalYear = 40 WHERE id = ' + str(id)
    print(command)
    cursor.execute(command)



if __name__ == '__main__':
    conn = sqlite3.connect('homework.db')
    cursor = conn.cursor()
    cursor.execute('select id from teachers')
    id_list = cursor.fetchall()
    count = 0
    bug = []
    for single_id in id_list:
        try:
            getMoreInfo(single_id[0])
            conn.commit()
        except:
            bug.append(single_id[0])
            print('bug in ' + str(single_id[0]))
        count = count + 1
        print(count)
    print(bug)
    cursor.close()
    conn.commit()
    conn.close()
