# coding=utf-8
# 作为模块吧
# 懒得复制一遍了
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import time
import codecs
from uuid import uuid1
import xlrd
import re
import os
import requests

WeekTable = {
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '日': '7'
}

StartTime = {
    1: '0800',
    2: '1005',
    3: '1400',
    4: '1605',
    5: '1840',
    6: '2045'
}

EndTime = {
    1: '0945',
    2: '1150',
    3: '1545',
    4: '1750',
    5: '2025',
    6: '2230'
}


ClsName = []
ClsLoc = []
ClsTime = []
ClsFreq = []
Teacher = []

StartDay = date(2020, 1, 1)

# 表格文件读取


def read_cul():
    global ClsName
    global ClsLoc
    global ClsTime
    global ClsFreq
    url = input("请将文件拖入框中")
    wb = xlrd.open_workbook(filename=url)
    cl = wb.sheet_by_index(0)
    ClsName = cl.col(0)
    ClsName.remove(ClsName[0])
    ClsLoc = cl.col(1)
    ClsLoc.remove(ClsLoc[0])
    ClsTime = cl.col(2)
    ClsTime.remove(ClsTime[0])
    ClsFreq = cl.col(3)
    ClsFreq.remove(ClsFreq[0])

# 取得课程第一节时间


def time_trans(cur, m):
    global ClsName
    global ClsLoc
    global ClsTime
    global ClsFreq
    ans = ''
    # 获取当前周数
    WeekNow = int(((date.today() - StartDay).days) / 7) + 1
    BeginDay = StartDay
    # 正则匹配获取数据
    patternwk = re.compile(r'[一二三四五六日]')
    patternles = re.compile(r'[0-9]')
    patternfq = re.compile(r'\d+-\d+')
    week = WeekTable[patternwk.findall(ClsTime[cur])[0]]
    les = patternles.findall(ClsTime[cur])[0]
    # 之前没有处理单周课程，现在处理一下
    fq = patternfq.findall(ClsFreq[cur])[0]
    FirstWeek = int(fq[0:fq.index('-')])
    LastWeek = int(fq[fq.index('-') + 1:])
    if FirstWeek >= WeekNow:
        ans += str(timedelta((FirstWeek - 1) * 7 + int(week) - 1) + BeginDay)
    elif FirstWeek < WeekNow and WeekNow <= LastWeek:
        ans += str(timedelta((WeekNow - 1) * 7 + int(week) - 1) + BeginDay)
    else:
        return False
    if m == 'start':
        ans += 'T' + StartTime[int(les)]
    else:
        ans += 'T' + EndTime[int(les)]
    ans = ans.replace('-', '') + '00'
    return ans


def get_feq(cur):
    patternfq = re.compile(r'\d+-\d+')
    fq = patternfq.findall(ClsFreq[cur])[0]
    WeekNow = int(((date.today() - StartDay).days) / 7) + 1
    FirstWeek = int(fq[0:fq.index('-')]
                    ) if int(fq[0:fq.index('-')]) > WeekNow else WeekNow
    LastWeek = int(fq[fq.index('-') + 1:])
    return LastWeek - FirstWeek + 1


def convert():
    file = codecs.open('课表.ics', 'w', 'utf-8')
    BeginDay = StartDay
    Today = date.today()
    # 文件开头格式
    file.write(u'''BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//CQUT//Syllabus//CN\n''')
    # 开始打印数据
    for i in range(0, len(ClsTime)):
        if time_trans(i, 'start') == False:
            continue
        file.write(u"BEGIN:VEVENT\n")
        file.write(u'SUMMARY:%s\n' % ClsName[i])
        file.write(u"DTSTART;VALUE=DATE-TIME:%s\n" % time_trans(i, 'start'))
        file.write(u"DTEND;VALUE=DATE-TIME:%s\n" % time_trans(i, 'end'))
        file.write(u"DTSTAMP;VALUE=DATE-TIME:%sZ\n" %
                   time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        file.write(u"UID:" + str(uuid1()) + '@HITWH\n')
        if Teacher != []:
            file.write(u"DESCRIPTION:%s\n" % (Teacher[i]))
        file.write(u"RRULE:FREQ=WEEKLY;COUNT=%d;INTERVAL=1\n" % get_feq(i))
        file.write(u"LOCATION:%s\n" % ClsLoc[i])

        alarmuid = str(uuid1())
        file.write(u"BEGIN:VALARM\n")
        file.write(u"ACTION:DISPLAY\n")
        if Teacher != []:
            file.write(u"DESCRIPTION:%s\n" % (Teacher[i]))
        file.write(u"TRIGGER:-P0DT0H10M0S\n")
        file.write(u"END:VALARM\n")

        file.write(u"END:VEVENT\n")
    file.close()
    print('课表.ics文件写入成功')


if __name__ == "__main__":
    read_cul()
    convert()

# 写到一半发现有人写过了qaq但是还是想写一下这个东西
