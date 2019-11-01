import requests
import codecs
import time
from datetime import timedelta, date, datetime
import calendar
import random
import re

StuID = "2191210103"  # str(input('请输入学号'))
PassWD = "IamCZM666/"  # str(input('请输入密码'))

NowTime = time.localtime(time.time())
Cookie = StuID + str(NowTime.tm_mon) + str(NowTime.tm_mday) + \
    str(NowTime.tm_hour) + str(NowTime.tm_min) + str(NowTime.tm_sec)

jym = 'jym2005=' + str(random.randint(1000, 20000)) + \
    '.' + str(random.randint(100000000000, 200000000000))

LogInUrl = 'http://222.194.15.1:7777/pls/wwwbks/bks_login2.login?' + jym
LogOutUrl = 'http://222.194.15.1:7777/pls/wwwbks/bks_login2.Logout'
CurriculumUrl = 'http://222.194.15.1:7777/pls/wwwbks/xk.CourseView'

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
# 登录
req = requests.post(LogInUrl, data=data, headers=LogInHeaders)

while req.status_code != 200:
    print("用户名或密码错误")
print("登陆成功")

# 获取sb教务处的垃圾服务器的错误时间
# 2019年10月30日14点52分
# Wed30Oct2019023037
# 我傻逼了，原来有set cookie qaq，不过已经写了就留在这吧==
temp = req.headers['Date'].replace(' ', '').replace(':', '').replace(',', '').replace('GMT', '')
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
origin = req.text
t = codecs.open('test.html', 'w', 'GBK')

#保存到文件
t.write(origin)

#正则匹配获取课表


# 退出登录
LogOutHeaders['Cookie'] = CurriculumHeaders['Cookie']
req = requests.get(LogOutUrl, headers=LogOutHeaders)
# print(re.text)
