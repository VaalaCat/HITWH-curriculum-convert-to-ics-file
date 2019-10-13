from ics import Calendar, Event
import xlrd

ClsName = []
ClsLoc = []
ClsTime = []
ClsFreq = []

cul = Calendar()
les=Event()

def readcul():
    url = 'C:\\Users\\huidc\\Desktop\\大一上课表.xlsx'#input()
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

def time_tans(a):
    
     

def convert():
    for i in range(0,ClsName.__len__):
        les.name = ClsName[i]
        les.location = ClsLoc[i]
        les.begin
        cul.events.add(les)

if __name__ == "__main__":
    readcul()

#写到一半发现有人写过了qaq但是还是想写一下这个东西