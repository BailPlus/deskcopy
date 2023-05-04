#Copyright Bail 2022-2023
#deskcopy 桌面拖入文件自动复制 v1.9.12_49
#2022.11.18-2023.5.3

TARGET = 'D:\\desktop'  #复制目标
LOGFILE = 'D:\\deskcopy.log'    #日志文件
UPANPATH = 'E:\\'   #U盘挂载点
UPANCOPY_ROOT = 'D:\\'  #U盘复制目标目录的父目录
WPS_ENABLE_FILE = r'D:\deskcopy\wps'    #wps启用信号
NOT_UPGRADE_FILE = r'D:\deskcopy\noup'  #禁用自动更新信号
ALLOW_SUFFIX = ('.doc','.docx','.ppt','.pptx','.pdf')   #过滤后缀名时允许的类型
UPANCOPY_ARGV = '--upan' #U盘全盘复制触发选项
OPENCOPY_ARGV = '--open'    #打开复制触发选项
STRFTIME = '%Y.%m.%d %H:%M:%S'  #格式化时间格式
DESKSLEEP = 5   #桌面复制间隔时间
UPANSLEEP = 5   #U盘检测间隔时间
KILL360SLEEP = 60   #杀死360画报间隔时间
UPLOADSLEEP = 60    #上传课件间隔时间
UPGRADE_DELAY = 300 #自动更新延迟启动时间

import os,time,shutil,sys,threading,subprocess

os.chdir(os.path.join(os.path.expanduser('~'),'Desktop'))
isneedupload = False

def execute_with_arg():
    '''使用参数启动'''
    if len(sys.argv) >= 2:
        if sys.argv[1] == UPANCOPY_ARGV:
            upancopy()
            sys.exit(0)
        elif sys.argv[1] == OPENCOPY_ARGV:
            opencopy(sys.argv[2])
            sys.exit(0)
        else:
            shutil.copy(sys.argv[1],TARGET)
            sys.exit(0)
def cmd(cmdline:str):
    '''执行系统命令
cmdline(str):命令行'''
    res = subprocess.run(cmdline,shell=True)
    if res.returncode == 0:
        log('D',f'命令执行成功: {cmdline}')
    else:
        log('W',f'执行 {cmdline} 时发生 {res.returncode}\n{res.stdout}\n{res.stderr}')
def upancopy():
    '''U盘全盘复制'''
    while not os.path.exists(UPANPATH):
        time.sleep(UPANSLEEP)
    os.chdir(UPANPATH)
    target = os.path.join(UPANCOPY_ROOT,time.strftime('upancopy_%Y%m%d%H%M%S'))
    os.mkdir(target)
    copydir('.',target,isfilter=True)
def opencopy(filename:str):
    '''打开文件并复制
filename(str):文件名
'''
    file_suffix = os.path.splitext(filename)[-1][1:]
    if file_suffix in ('doc','docx'):
        if os.path.exists(WPS_ENABLE_FILE):
            threading.Thread(target=lambda:cmd(f'start wps "{filename}"')).start()
        else:
            threading.Thread(target=lambda:cmd(f'start winword "{filename}"')).start()
    elif file_suffix in ('ppt','pptx'):
        if os.path.exists(WPS_ENABLE_FILE):
            threading.Thread(target=lambda:cmd(f'start wpp "{filename}"')).start()
        else:
            threading.Thread(target=lambda:cmd(f'start powerpnt "{filename}"')).start()
    elif file_suffix in ('xls','xlsx'):
        threading.Thread(target=lambda:cmd(f'start excel "{filename}"')).start()
    elif file_suffix in ('pdf',):
        threading.Thread(target=lambda:cmd(fr'start C:\Users\SEEWO\AppData\Roaming\secoresdk\360se6\Application\360se "{filename}"')).start()
    threading.Thread(target=lambda:cmd(f'start pythonw D:\deskcopy\deskcopy.py "{filename}"')).start()
def copydir(path:str,target:str,isfilter:bool):
    '''复制目录下所有文件
path(str):目录路径
target(str):目标路径
isfilter(bool):是否过滤后缀名'''
    filelst = os.walk(path)
    for i in filelst:
        for j in i[1]:  #创建文件夹
            dirname = os.path.join(target,i[0],j)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        for j in i[2]:  #复制文件
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
    log('I','开始杀死360画报')
    while True:
        cmd('taskkill /f /im 360huabao.exe')
        time.sleep(KILL360SLEEP)
def log(logtype:str,logtext:str):
    '''输出日志
logtype(str):日志类型('D','I','W','E','F')
logtext(str):日志内容'''
    content = f'[{time.strftime(STRFTIME)}][{__name__}] {logtype}: {logtext}'
    print(content,file=sys.stderr)
    with open(LOGFILE,'a') as logfile:
        print(content,file=logfile)
def get_filesizes(path:str=None)->list:
    '''获取目录下所有文件大小
path(str):要获取的目录，默认为工作目录
返回值:包括该目录下所有文件大小的列表(list)'''
    filesizes = []
    for i in os.listdir(path):
        filesizes.append(os.stat(i).st_size)
    return filesizes
def deskcopy():
    '''桌面复制'''
    global isneedupload
    filesizes = get_filesizes()
    while True:
        new_filesizes = get_filesizes()
        for i in new_filesizes:
            if (i not in filesizes) or (len(new_filesizes) != len(filesizes)):
                copydir('.',TARGET,isfilter=False)
                isneedupload = True
                filesizes = new_filesizes
        time.sleep(DESKSLEEP)
def auto_upgrade():
    '''自动更新程序（从github）'''
    if not os.path.exists(NOT_UPGRADE_FILE):
        time.sleep(UPGRADE_DELAY)
        cmd(r'D:\deskcopy\auto-upgrade.bat')
        log('I','自动更新完毕')
def upload_cached_files():
    '''上传已缓存的文件（向gitlink）'''
    global isneedupload
    while True:
        if isneedupload:
            cmd(r'D:\deskcopy\pushfile.bat')
            isneedupload = False
            log('I','自动上传完毕')
        time.sleep(UPLOADSLEEP)
def main():
    execute_with_arg()
    log('I','已启动')
    threading.Thread(target=kill360).start()
    threading.Thread(target=auto_upgrade).start()
    threading.Thread(target=upload_cached_files).start()
    deskcopy()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        log('F',e)
