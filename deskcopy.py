#Copyright Bail 2022
#deskcopy 桌面拖入文件自动复制 v1.0_1
#2022.11.18-2022.12.10

TARGET = 'D:\\desktop'  #复制目标
ALLOW_SUFFIX = ('.doc','.docx','.ppt','.pptx','.pdf')   #过滤后缀名时允许的类型
LOGFILE = 'D:\\deskcopy.log'    #日志文件
UPACOPY_ARGV = '--upan' #U盘全盘复制启动参数
DESKSLEEP = 5   #桌面复制间隔时间
UPANSLEEP = 5   #U盘检测间隔时间
KILL360SLEEP = 60   #杀死360画报间隔时间
STRFTIME = '%Y.%m.%d %H:%M:%S'  #格式化时间格式

import os,time,shutil,sys,threading

os.chdir(os.path.join(os.path.expanduser('~'),'Desktop'))
filenum = len(os.listdir())

def execute_with_arg():
    '''使用参数启动'''
    if len(sys.argv) == 2:
        if sys.argv[1] == UPACOPY_ARGV:
            upancopy()
            sys.exit()
        else:
            opencopy(sys.argv[1])

            sys.exit()
def is_file_number_change():
    '''检测是否出现新文件
返回值:当前（改变后的）文件列表(list)
    技术细节：获取桌面文件列表，统计文件数量，和原来的数量对比。
            若增多，说明有新文件，则退出阻塞，进行下一步操作。'''
    global filenum
    nowfilenum = len(os.listdir())
    if nowfilenum != filenum:
        filenum = nowfilenum    #复制结束后更新“原文件数量”
        return True
    else:
        return False
def upancopy(): #※不可在Linux下测试
    global TARGET
    while not os.path.exists('E:\\'):
        time.sleep(UPANSLEEP)
    os.chdir('E:\\')
    TARGET = os.path.join(TARGET,time.strftime(STRFTIME))
    os.mkdir(TARGET)
    copy('.',TARGET,isfilter=True)
def opencopy(filename:str):
    '''打开文件并复制
filename(str):文件名
'''
    file_suffix = os.path.splitext(filename)[-1][1:]
    if file_suffix in ('doc','docx'):
        threading.Thread(target=lambda:os.popen(f'start winword {filename}').close()).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
        sys.exit()
    elif file_suffix in ('ppt','pptx'):
        threading.Thread(target=lambda:os.popen(f'start powerpnt {filename}').close()).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
        sys.exit()
    elif file_suffix in ('xls','xlsx'):
        threading.Thread(target=lambda:os.popen(f'start excel {filename}').close()).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
        sys.exit()
    elif file_suffix in ('pdf',):
        threading.Thread(target=lambda:os.popen(fr'start C:\Users\SEEWO\AppData\Roaming\secoresdk\360se6\Application\360se {filename}').close()).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
def copy(path:str,target:str,isfilter:bool):
    '''复制目录下所有文件
path(str):目录路径
target(str):目标路径
isfilter(bool):是否过滤后缀名'''
    filelst = os.walk(path)
    for i in filelst:
        for j in i[1]:
            dirname = os.path.join(target,i[0],j)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        for j in i[2]:
            filesrc = os.path.join(i[0],j)
            suffix = os.path.splitext(filesrc)[-1]
            if (suffix in ALLOW_SUFFIX) or (not isfilter):
                filetarget = os.path.join(target,i[0],j)
                try:
                    shutil.copy(filesrc,filetarget)
                except Exception as e:
                    log('E',f'复制异常 {filesrc}\n{e}')
                else:
                    log('I',f'已复制 {filesrc}')
            else:
                log('I',f'已跳过 {filesrc}')
def kill360():
    '''自动杀死360画报'''
    while True:
        os.popen('taskkill /f /im 360huabao.exe').close()
        time.sleep(KILL360SLEEP)
def log(logtype:str,logtext:str):
    '''输出日志
logtype(str):日志类型('D','I','W','E','F')
logtext(str):日志内容'''
    content = f'[{time.strftime(STRFTIME)}][{__name__}] {logtype}: {logtext}'
    print(content,file=sys.stderr)
    with open(LOGFILE,'a') as logfile:
        print(content,file=logfile)
def deskcopy():
    while True:
        if is_file_number_change():
            copy('.',TARGET,isfilter=False)
        time.sleep(DESKSLEEP)
def main():
    execute_with_arg()
    log('I','已启动')
    threading.Thread(target=kill360).start()
    deskcopy()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        log('F',e)
