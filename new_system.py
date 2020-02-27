import xlrd
import re
import cul

file_path = input("请将下载的课表文件拖到这里")

AllClasses_name = []
AllTeachers_name = []

TransTable = {
    '1-2': '1',
    '3-4': '2',
    '5-6': '3',
    '7-8': '4',
    '9-10': '5',
    '11-12': '6'
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

# 暴力获取一个格子中的课或者老师数量


def get_class_num(data, mode):
    num = 0
    ans = []  # 匹配得到的课程按原顺序排列
    que = []
    if mode == 'class':
        que = AllClasses_name
    else:
        que = AllTeachers_name
    for i in que:
        if i in data and (i in ans) == False:
            num += 1
            ans.append(i)
    return (num, ans)

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

    ProcessedList = []
    ans = []

    # 首先将课表转换为一个列表
    for i in lesson[1:]:
        for j in i:
            if len(j) > 5:
                ProcessedList.append([j, lesson[0][i.index(j)].replace("\r", "").replace(
                    "\n", "").replace(" ", ""), i[0].replace("\r", "").replace("\n", "").replace(" ", "")])
    len1 = len(ProcessedList)

    # 分割字符串
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
    for i in ProcessedList:
        if i[0] == '':
            ProcessedList.pop(ProcessedList.index(i))

    # 正则匹配处理数据
    for i in ProcessedList:
        num, ans = get_class_num(i[0], 'class')
        # 防止出错qaq
        if num != 1:
            print("您的课表数据有误，请检查数据或联系开发者,出错数据：")
            print(i, num, ans)
            exit()
        TeacherTimePattern = re.compile('[\u4e00-\u9fa5]+\[\d+-\d+\]')
        TeacherTime = re.findall(TeacherTimePattern, i[0])
        LocPattern = re.compile(r'[A-Z]楼-\d+')
        Loc = re.findall(LocPattern, i[0])

        for j in TeacherTime:
            cur = j.index('[')
            ClsTeacher.append(j[:cur])
            ClsFreq.append(j[cur:-1])
            ClsName.append(ans[0])
            if Loc == []:
                Loc = ['']
            ClsLoc.append(Loc[0])
            ClsTime.append(i[1] + '第' + TransTable[i[2]] + '大节')

    return (ClsName,ClsLoc,ClsFreq,ClsTime,ClsTeacher)

#:[\u4e00-\u9fa5]+匹配汉字


# 获取基本数据
def init_database(path):
    BaseData = xlrd.open_workbook(path)
    BaseData = BaseData.sheets()[0]
    ClassList = []
    for i in range(BaseData.nrows):
        ClassList.append(BaseData.row_values(i))
    return ClassList

#链接到cul.py生成ics文件
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

if __name__ == "__main__":
    data = xlrd.open_workbook(file_path)
    lesson = get_data(data)
    ClassList = init_database('./2020_class_list.xls')

    for i in ClassList:
        AllClasses_name.append(i[5].replace(
            "\r", "").replace("\n", "").replace(" ", ""))
        AllTeachers_name.append(i[17].replace(
            "\r", "").replace("\n", "").replace(" ", ""))

    ClsName, ClsLoc, ClsFreq, ClsTime, ClsTeacher = process_data(lesson)
    connect(ClsName, ClsLoc, ClsFreq, ClsTime, ClsTeacher)
