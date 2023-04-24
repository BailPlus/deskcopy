#Copyright Bail 2022-2023
#deskcopy 桌面拖入文件自动复制 v1.8.5_36
#2022.11.18-2023.4.18

TARGET = 'D:\\desktop'  #复制目标
LOGFILE = 'D:\\deskcopy.log'    #日志文件
UPANPATH = 'E:\\'
ALLOW_SUFFIX = ('.doc','.docx','.ppt','.pptx','.pdf')   #过滤后缀名时允许的类型
UPACOPY_ARGV = '--upan' #U盘全盘复制启动参数
STRFTIME = '%Y.%m.%d %H:%M:%S'  #格式化时间格式
DESKSLEEP = 5   #桌面复制间隔时间
UPANSLEEP = 5   #U盘检测间隔时间
KILL360SLEEP = 60   #杀死360画报间隔时间
UPLOADSLEEP = 60    #上传课件间隔时间

import os,time,shutil,sys,threading,subprocess

os.chdir(os.path.join(os.path.expanduser('~'),'Desktop'))
isneedupload = False

def execute_with_arg():
    '''使用参数启动'''
    if len(sys.argv) == 2:
        if sys.argv[1] == UPACOPY_ARGV:
            upancopy()
            sys.exit()
        else:
            opencopy(sys.argv[1])
            sys.exit()
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
    target = os.path.join(TARGET,time.strftime('%Y%m%d%H%M%S'))
    os.mkdir(target)
    copydir('.',target,isfilter=True)
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
def deskcopy():
    '''桌面复制'''
    global isneedupload
    filesizes = []
    for i in os.listdir():
        filesizes.append(os.stat(i).st_size)
    while True:
        for i in os.listdir():
            if os.stat(i).st_size not in filesizes:
                copydir('.',TARGET,isfilter=False)
                isneedupload = True
                filesizes = []
                for j in os.listdir():
                    filesizes.append(os.stat(j).st_size)
        time.sleep(DESKSLEEP)
def auto_upgrade():
    '''自动更新程序（从github）'''
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
