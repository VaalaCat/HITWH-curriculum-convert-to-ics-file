# 哈尔滨工业大学威海课表转换
因为系统日历有消息推送功能，所以写了个这东西来将教务处的辣鸡课表转换为ics文件方便导入到日历程序

2020年9月7日更新
------
新增了少量测试数据，更新了某些环节的处理逻辑，将数据库移到云端提高下载速度

2020年2月27日更新
------
由于教务处更新系统，所以对新系统做了适配，并且添加了教师数据。
使用说明：

1. 在本项目文件夹内按住shift右键单击空白处，点击在powershell中打开
2. 输入 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U`
3. 输入 `pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`
4. 输入 `pip install -r .\requirements.txt`
5. 输入 `python new_system.py`
6. 请仔细检查下载的文件是否存在分裂周数的数据，若存在则需要手动更改
```
[2，3，7-15]周，[4]周->[2，3，4，7-15]周
```
7. 按程序要求提供所需数据，课表表格可在新系统中下载
8. 享受你得到的ics文件叭

-------------------------
运行完成后请打开 课表.ics，然后利用日历软件导入即可，这里要注意一下gmail不能直接导入，可以使用outlook导入后再导出得到文件。后续会修正这个问题  
另：晚自习时间我记不住qaq，麻烦知道的dalao通知我一下  
By VaalaCat