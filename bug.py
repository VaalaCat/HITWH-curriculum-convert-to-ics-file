import requests
import codecs
import time
from datetime import timedelta, date, datetime
import calendar
import random
import re
import cul

StuID = str(input('请输入学号'))
PassWD = str(input('请输入密码'))

NowTime = time.localtime(time.time())
Cookie = StuID + str(NowTime.tm_mon) + str(NowTime.tm_mday) + \
    str(NowTime.tm_hour) + str(NowTime.tm_min) + str(NowTime.tm_sec)

# 这个东西我也不知道有啥意思，加上就对了
jym = 'jym2005=' + str(random.randint(1000, 20000)) + \
    '.' + str(random.randint(100000000000, 200000000000))

LogInUrl = 'http://222.194.15.1:7777/pls/wwwbks/bks_login2.login?' + jym
LogOutUrl = 'http://222.194.15.1:7777/pls/wwwbks/bks_login2.Logout'
CurriculumUrl = 'http://222.194.15.1:7777/pls/wwwbks/xk.CourseView'

# burpsuite扒下来的数据
LogInHeaders = {
    'POST': '/pls/wwwbks/bks_login2.login?' + jym,
    'Host': '222.194.15.1:7777',
    'Proxy-Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://222.194.15.1:7777',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://222.194.15.1:7777/zhxt_bks/xk_login.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': 'ACCOUNT=' + Cookie
}

CurriculumHeaders = {
    'GET': '/pls/wwwbks/xk.CourseView HTTP/1.1',
    'Host': '222.194.15.1:7777',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://222.194.15.1:7777/zhxt_bks/w_left.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': 'ACCOUNT=' + Cookie

}

LogOutHeaders = {
    'GET': '/pls/wwwbks/bks_login2.Logout HTTP/1.1',
    'Host': '222.194.15.1:7777',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://222.194.15.1:7777/zhxt_bks/w_left.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cookie': 'ACCOUNT=' + Cookie
}

data = {
    'stuid': StuID,
    'pwd': PassWD
}

NumberTable = {
    '1': '一',
    '2': '二',
    '3': '三',
    '4': '四',
    '5': '五',
    '6': '六',
    '7': '日'
}

# 登录
def login():
    req = requests.post(LogInUrl, data=data, headers=LogInHeaders)

    # 获取sb教务处的垃圾服务器的错误时间
    # 2019年10月30日14点52分
    # Wed30Oct2019023037
    # 我傻逼了，原来有set cookie qaq，不过已经写了就留在这吧==
    temp = req.headers['Date'].replace(' ', '').replace(
        ':', '').replace(',', '').replace('GMT', '')
    ServerYear = int(temp[8:12])
    ServerMon = list(calendar.month_abbr).index(temp[5:8])
    ServerDay = int(temp[3:5])
    ServerHour = int(temp[12:14])
    ServerMin = int(temp[14:16])
    ServerSec = int(temp[16:18])
    ServerTime = datetime(ServerYear, ServerMon, ServerDay,
                          ServerHour, ServerMin, ServerSec)
    ServerTime = ServerTime + timedelta(hours=8)

    # 获取数据
    CurriculumHeaders['Cookie'] = CurriculumHeaders['Cookie'].replace(Cookie, StuID + str(
        ServerTime).replace('2019', '').replace('-', '').replace(':', '').replace(' ', ''))
    req = requests.get(CurriculumUrl, headers=CurriculumHeaders)
    # 保存到文件
    origin = req.text

    if origin.find('登录再使用') != -1:
        print("登陆失败")
        exit()
    print('登陆成功')
    return origin

# 处理课表
def getcul(curtext):

    # 匹配有效数据
    CulPattern = re.compile(r'''<td width="112" height="20" class=td_biaogexian><p align="center">(.*)&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center"><FONT COLOR="\#FF0000"></FONT>&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center">(.*)&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center">(.*)&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center">(.*)&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center">(.*)&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center">(.*)&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center">(.*)&nbsp;</p></td>
<td width="112" height="20" class=td_biaogexian><p align="center">(.*)周上&nbsp;</p></td>''')
    NormalCur = CulPattern.findall(curtext)

    # 筛除无效数据
    for i in range(0, len(NormalCur)):
        NormalCur[i] = list(NormalCur[i])
        while NormalCur[i].count('') != 0:
            NormalCur[i][NormalCur[i].index('')] = '未知'

    # 分裂多周不连续课
    r = len(NormalCur)
    for i in range(0, r):
        #处理单周课程
        if NormalCur[i][7].find(',') == -1 and NormalCur[i][7].find('-') == -1:
            NormalCur[i][7] = NormalCur[i][7] + '-' + NormalCur[i][7]
        if NormalCur[i][7].find(',') != -1:
            NormalCur[i][7] += ','
            RepPattern = re.compile(r',(.*),')
            temp = RepPattern.findall(NormalCur[i][7])

            for k in temp:
                if k.find('-') == -1:
                    k = k + '-' + k

                NewClass = NormalCur[i][:7]
                NewClass.append(k)
                NormalCur.append(NewClass)

            NormalCur[i][7] = NormalCur[i][7][: NormalCur[i][7].find(',')]

            if NormalCur[i][7].find('-') == -1:
                NormalCur[i][7] = NormalCur[i][7] + '-' + NormalCur[i][7]
    return NormalCur

# 将课表数据使用cul.py之前的函数建立ics文件
def to_file(cur):
    for i in cur:
        cul.ClsName.append(i[0])
        cul.ClsLoc.append(i[5])
        cul.ClsFreq.append(i[7])
        i[6] = NumberTable[i[6][: i[6].index(
            '-')]] + ' ' + i[6][i[6].index('-') + 1:]
        cul.ClsTime.append(i[6])
    print('数据获取成功')

# 退出登录
def logout():
    LogOutHeaders['Cookie'] = CurriculumHeaders['Cookie']
    req = requests.get(LogOutUrl, headers=LogOutHeaders)
    print('已退出登录')


if __name__ == '__main__':
    to_file(getcul(login()))
    cul.convert()
    logout()
