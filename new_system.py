import xlrd
import re
import cul
import urllib
import os
from datetime import date, timedelta

file_path = input("请将下载的课表文件拖到这里：")

AllClasses_name = []
AllTeachers_name = []

grade = ''

TransTable = {
    '1-2': '1',
    '3-4': '2',
    '5-6': '3',
    '7-8': '4',
    '9-10': '5',
    '11-12': '6',
    '1': '大一',
    '2': '大二',
    '3': '大三',
    '4': '大四'
}

# 从文件中获取数据并进行第一次处理


def get_data(data):
    table = data.sheets()[0]
    lesson = []
    for i in range(table.nrows):
        lesson.append(table.row_values(i))
    # 掐头去尾
    lesson.pop(0)
    lesson.pop()
    return lesson


def check(data,prob):
    cur = data.find(prob)
    end = data[cur + len(prob)]
    if cur == 0 and (end== '<' or end=='('):
        return True
    start = data[cur - 1]
    if start == '>' and (end == '<'or end=='('):
        return True
    if (start == '>' or start == '，') and end == '[':
        return True

    return False

# 暴力获取一个格子中的课或者老师数量，返回值为数量和具体的老师或者课程列表

def get_class_num(data, mode):
    num = 0
    ans = []  # 匹配得到的课程按原顺序排列
    que = []
    if mode == 'class':
        que = AllClasses_name
    else:
        que = AllTeachers_name
    for i in que:
        if (i in data) and (i in ans) == False and check(data, i):
            num += 1
            ans.append(i)
    return (num, ans)


def split_week(data):
    data = data.split('，')
    ans = []
    for i in data:
        if i.find('-') == -1:
            ans.append(i + '-' + i)
        else:
            ans.append(i)
    return ans

# 整理数据为以前的规范


def process_data(lesson):
    # 去掉无用数据
    for i in range(len(lesson)):
        lesson[i].pop(0)
    # 删除换行和空格
    for i in range(len(lesson)):
        for j in range(len(lesson[i])):
            lesson[i][j] = lesson[i][j].replace(
                "\r", "").replace("\n", "").replace(" ", "")

    ClsName = []
    ClsLoc = []
    ClsTime = []
    ClsFreq = []
    ClsTeacher = []

    ProcessedList = [] # 课表转换出来的列表
    ans = []

    # 首先将课表转换为一个列表
    for i in lesson[1:]:
        for j in range(len(i)):
            if len(i[j]) > 5:
                ProcessedList.append([i[j], lesson[0][j].replace("\r", "").replace("\n", "").replace(
                    " ", ""), i[0].replace("\r", "").replace("\n", "").replace(" ", "")])
    len1 = len(ProcessedList)

    # 分割一格中的多个课程
    for i in range(len1):
        num, ans = get_class_num(ProcessedList[i][0], 'class')
        if num > 1:
            cur = []
            for j in ans:
                cur.append(ProcessedList[i][0].find(j))
            cur.append(len(ProcessedList[i][0]))
            cur.sort()
            for j in range(len(cur) - 1):
                ProcessedList.append(
                    [ProcessedList[i][0][cur[j]: cur[j + 1]], ProcessedList[i][1], ProcessedList[i][2]])

            ProcessedList[i] = ['', '', '']

    # 删除多余的空数据
    try:
        while -1!=ProcessedList.index(['','','']):
            ProcessedList.pop(ProcessedList.index(['','','']))
    except:
        print("课表提取完成，请检查课表内容")
        print("--------------------------------")
        print(ProcessedList)
        print("--------------------------------")

    # 正则匹配处理数据
    for i in ProcessedList:
        num, ans = get_class_num(i[0], 'class')
        # 防止出错qaq
        if num != 1:
            print("您的课表数据库有误，请自行在数据库中添加课程名称和老师或联系开发者更新数据，出错数据：")
            print(i, num, ans)
            exit()
        TeacherTimePattern = re.compile('[\u4e00-\u9fa5]+\[.*?\]')
        TeacherTimeRaw = re.findall(TeacherTimePattern, i[0])
        TeacherTime = []

        # 处理多周不连续课程
        for j in TeacherTimeRaw:
            week = split_week(j[j.index('[') + 1 : j.index(']')])
            TeacherTime.append([j[: j.index('[')], week])
            
        LocPattern = re.compile(r'[A-Z]楼-\d+')
        Loc = re.findall(LocPattern, i[0])

        for j in TeacherTime:
            for k in j[1]:
                ClsTeacher.append(j[0])
                ClsFreq.append(k)
                ClsName.append(ans[0])
                if Loc == []:
                    Loc = ['未知']
                ClsLoc.append(Loc[0])
                ClsTime.append(i[1] + '第' + TransTable[i[2]] + '大节')

    return (ClsName, ClsLoc, ClsFreq, ClsTime, ClsTeacher)

#:[\u4e00-\u9fa5]+匹配汉字


# 获取基本数据
def init_database(path):
    BaseData = xlrd.open_workbook(path)
    BaseData = BaseData.sheets()[0]
    ClassList = []
    for i in range(BaseData.nrows):
        ClassList.append(BaseData.row_values(i))
    return ClassList

# 链接到cul.py生成ics文件


def connect(ClsName, ClsLoc, ClsFreq, ClsTime, ClsTeacher):
    try:
        for i in range(len(ClsName)):
            cul.ClsFreq.append(ClsFreq[i])
            cul.ClsLoc.append(ClsLoc[i])
            cul.ClsName.append(ClsName[i])
            cul.ClsTime.append(ClsTime[i])
            cul.Teacher.append(ClsTeacher[i])
        cul.convert()
    except:
        print('错误')


def download(url):
    if url == "":
        url = "http://oss.vaala.ink/tmp/class_list.xls"
    print("开始下载...")
    with urllib.request.urlopen(url) as web:
        # 为保险起见使用二进制写文件模式，防止编码错误
        with open('./class_list.xls', 'wb') as outfile:
            outfile.write(web.read())
    print("下载完成")


if __name__ == "__main__":
    StartDay = input("请输入第一个周一的日期，用.分割，例如2020.9.7，若无输入则默认2020.9.7：").split('.')
    if StartDay == ['']:
        StartDay = "2020.9.7".split('.')
    cul.StartDay = date(int(StartDay[0]), int(StartDay[1]), int(StartDay[2]))
    data = xlrd.open_workbook(file_path)
    lesson = get_data(data)
    if os.path.exists('./class_list.xls') == False:
        download(input("请输入课表数据库的url，若无输入则使用Vaala提供的数据库，更新数据库请删除class_list.xls文件："))
    ClassList = init_database('./class_list.xls')

    for i in ClassList:
        AllClasses_name.append(i[5].replace(
            "\r", "").replace("\n", "").replace(" ", ""))
        AllTeachers_name.append(i[17].replace(
            "\r", "").replace("\n", "").replace(" ", ""))

    ClsName, ClsLoc, ClsFreq, ClsTime, ClsTeacher = process_data(lesson)
    connect(ClsName, ClsLoc, ClsFreq, ClsTime, ClsTeacher)
