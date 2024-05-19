#!/data/data/com.termux/files/usr/bin/python
#Copyright Bail 2024
#deskcopy:photocopy 相册新增照片自动复制 v1.0.1_2
#2024.5.18

TARGET = r'/data/data/com.termux/files/home/Photos/Camera/'  #复制目标
LOGFILE = r'/data/data/com.termux/files/home/photocopy.log'    #日志文件
STRFTIME = '%Y.%m.%d %H:%M:%S'  #格式化时间格式
FILEDATE = '%Y%m%d' #文件名包含的日期的格式
DESKSLEEP = 5   #桌面复制间隔时间

import os,time,shutil,sys,traceback

desktop_path = '/storage/emulated/0/DCIM/Camera/'
os.chdir(desktop_path)

def copy(src:str,dst:str):
    '''复制单个文件
src(str):原始文件路径
dst(str):目标文件路径'''
    try:
        shutil.copy(src,dst)
    except Exception as e:
        log('E',f'复制异常 {src}\n{e}')
    else:
        log('I',f'已复制 {src}')
def log(logtype:str,logtext:str):
    '''输出日志
logtype(str):日志类型('D','I','W','E','F')
logtext(str):日志内容'''
    content = f'[{time.strftime(STRFTIME)}][{__name__}] {logtype}: {logtext}'
    print(content,file=sys.stderr)
    with open(LOGFILE,'a') as logfile:
        print(content,file=logfile)
def deskcopy():
    '''桌面复制'''
    copied_files = [i for i in os.listdir(TARGET)]
    log('I',f'''以下文件已存在：
{"""
""".join(copied_files)}''')
    while True:
        files = os.listdir()
        for i in files:
            if (time.strftime(FILEDATE) in i) and (i not in copied_files):
                log('I',f'已触发相册复制:{i}')
                copy(i,TARGET)
                copied_files.append(i)
        time.sleep(DESKSLEEP)
def main():
    log('I','已启动')
    deskcopy()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        log('F',traceback.format_exc())
