#Copyright Bail 2022-2024
#deskcopy 桌面拖入文件自动复制 v1.13.4_94
#2022.11.18-2024.4.14

TARGET = 'D:\\desktop'  #复制目标
LOGFILE = 'D:\\desktop\\deskcopy.log'    #日志文件
UPANPATH = 'E:\\'   #U盘挂载点
UPANCOPY_ROOT = 'D:\\'  #U盘复制目标目录的父目录
RUIPATH = r'E:\高三一轮'    #数学一轮复制源文件目录
RUITARGET = r'D:\desktop\高三一轮'  #数学一轮复制目标目录
NOT_UPGRADE_FILE = r'D:\deskcopy\noup'  #禁用自动更新信号
NEED_UPLOAD_FILE = r'D:\deskcopy\need_upload'   #上传信号
DAILY_DIR_FILE = r'D:\deskcopy\dailydir'    #每日文件夹位置
UPANCOPY_ARGV = '--upan' #U盘全盘复制触发选项
OPENCOPY_ARGV = '--open'    #打开复制触发选项
STRFTIME = '%Y.%m.%d %H:%M:%S'  #格式化时间格式
DESKSLEEP = 5   #桌面复制间隔时间
UPANSLEEP = 5   #U盘检测间隔时间
PROCSLEEP = 60  #进程复制间隔时间
UPLOADSLEEP = 60    #上传课件间隔时间
UPGRADE_DELAY = 300 #自动更新延迟启动时间

import os,time,shutil,sys,threading,subprocess,traceback,psutil

desktop_path = os.path.join(os.path.expanduser('~'),'Desktop')
isneedupload = False    #已弃用，在过渡时期防止bug的发生
os.chdir(desktop_path)

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
            copy(sys.argv[1],get_daily_dir())
            sys.exit(0)
def cmd(cmdline:str):
    '''执行系统命令
cmdline(str):命令行'''
    res = subprocess.run(cmdline,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         encoding='gb2312',
                         shell=True)
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
    copydir('.',target,False)
def opencopy(filename:str):
    '''打开文件并复制
filename(str):文件名
'''
    file_suffix = os.path.splitext(filename)[-1][1:]
    if file_suffix in ('doc','docx'):
        threading.Thread(target=lambda:cmd(f'start wps "{filename}"')).start()
    elif file_suffix in ('ppt','pptx'):
        threading.Thread(target=lambda:cmd(f'start wpp "{filename}"')).start()
    elif file_suffix in ('xls','xlsx'):
        threading.Thread(target=lambda:cmd(f'start et "{filename}"')).start()
    elif file_suffix in ('pdf',):
        threading.Thread(target=lambda:cmd(f'start msedge "{filename}"')).start()
    threading.Thread(target=lambda:cmd(f'start pythonw D:\deskcopy\deskcopy.py "{filename}"')).start()
    open(NEED_UPLOAD_FILE,'w').close()
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
def copydir(path:str,target:str,filterlst:tuple):
    '''复制目录下所有文件
path(str):目录路径
target(str):目标路径
filterlst(tuple/False):允许通过的后缀名
                       False:不进行过滤，全部复制
                       ():(空元组)不进行复制，全部跳过
                       (value,...):仅复制后缀名在filterlst中的文件'''
    filelst = os.walk(path)
    for i in filelst:
        for j in i[1]:  #创建文件夹
            dirname = os.path.join(target,i[0],j)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        for j in i[2]:  #复制文件
            filesrc = os.path.join(i[0],j)
            suffix = os.path.splitext(filesrc)[1]
            if filterlst == False:
                filetarget = os.path.join(target,i[0],j)
                copy(filesrc,filetarget)
            elif suffix in filterlst:
                filetarget = os.path.join(target,i[0],j)
                copy(filesrc,filetarget)
            else:
                log('I',f'已跳过 {filesrc}')
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
    filesizes = get_filesizes(desktop_path)
    while True:
        new_filesizes = get_filesizes(desktop_path)
        for i in new_filesizes:
            if (i not in filesizes) or (len(new_filesizes) != len(filesizes)):
                log('I','已触发桌面复制')
                copydir('.',get_daily_dir(),False)
                open(NEED_UPLOAD_FILE,'w').close()
                filesizes = new_filesizes
        time.sleep(DESKSLEEP)
def auto_upgrade():
    '''自动更新程序（从github）'''
    if os.path.exists(NOT_UPGRADE_FILE):
        log('W','检测到阻止更新信号文件，将不会自动更新')
    else:
        time.sleep(UPGRADE_DELAY)
        cmd(r'D:\deskcopy\auto-upgrade.bat')
        log('I','自动更新完毕')
def upload_cached_files():
    '''上传已缓存的文件（向gitlink）'''
    while True:
        if os.path.exists(NEED_UPLOAD_FILE):
            os.remove(NEED_UPLOAD_FILE)
            cmd(r'D:\deskcopy\pushfile.bat')
            log('I','自动上传完毕')
        time.sleep(UPLOADSLEEP)
def ruicopy():
    '''数学一轮资料自动复制'''
    while not os.path.exists(RUIPATH):
        time.sleep(UPANSLEEP)
    log('I','已触发数学一轮资料自动复制')
    os.chdir(RUIPATH)
    if not os.path.exists(RUITARGET):
        os.makedirs(RUITARGET)
    copydir('.',RUITARGET,False)
    open(NEED_UPLOAD_FILE,'w').close()
    os.chdir(desktop_path)   #切出高三一轮目录，防止U盘占用
def openupan():
    '''插入U盘自动打开
---------
用于顶替360的U盘助手功能'''
    isopened = False
    while True:
        if os.path.exists(UPANPATH):
            if not isopened:
                cmd(f'explorer "{UPANPATH}"')
                isopened = True
                log('I','已打开U盘')
        else:
            if isopened:
                isopened = False
                log('I','已拔出U盘')
        time.sleep(UPANSLEEP)
def remove_git_lock():
    '''去除pptcopy(班级电脑为D:\desktop)仓库锁，防止因git异常退出而导致无法上传的问题'''
    lockfile = os.path.join(TARGET,'.git','index.lock')
    if os.path.exists(lockfile):
        log('W','检测到复制目标仓库被异常锁定，正在尝试解锁')
        os.remove(lockfile)
        log('I','解锁成功')
def create_daily_dir():
    '''创建每日文件夹'''
    daily_dir = os.path.join(TARGET,time.strftime('%Y.%m.%d'))
    if (not os.path.exists(DAILY_DIR_FILE)) or (get_daily_dir() != daily_dir):
        os.mkdir(daily_dir)
        with open(DAILY_DIR_FILE,'w') as f:
            f.write(daily_dir)
        log('I','已创建今日文件夹')
    else:
        log('I','今日文件夹已存在')
def get_daily_dir()->str:
    '''获取每日文件夹路径
返回值:每日文件夹路径，即DAILY_DIR_FILE文件内容(str)'''
    with open(DAILY_DIR_FILE) as f:
        return f.read()
def proccopy():
    '''进程复制
检测wps.exe进程并复制其启动参数中附带的文件'''
    recorded_wps_pids = [] # 已记录的wps pid
    while True:
        #获取pid列表
        ps = psutil.pids()
        #获取进程信息
        for i in ps:
            try:
                proc = psutil.Process(i)
                procname = proc.name()
                proccmd = proc.cmdline()
            except (psutil.AccessDenied,psutil.NoSuchProcess):
                pass
        #判定为wps进程
            if (procname == 'wps.exe') and (i not in recorded_wps_pids):
                #记录pid
                recorded_wps_pids.append(i)
                #尝试提取文件路径
                for j in proccmd[1:]:
                    if os.path.exists(j):
                        log('I',f'找到wps打开文件进程：{" ".join(proccmd)}')
                        filepath = j
                        break
                else:
                    log('W',f'“{" ".join(proccmd)}”貌似不是wps用于打开文件的进程')
                    continue
                #复制文件
                copy(filepath,get_daily_dir())
                open(NEED_UPLOAD_FILE,'w').close()
        time.sleep(PROCSLEEP)
def main():
    execute_with_arg()
    remove_git_lock()
    create_daily_dir()
    log('I','已启动')
    threading.Thread(target=auto_upgrade).start()
    threading.Thread(target=upload_cached_files).start()
    threading.Thread(target=ruicopy).start()
    threading.Thread(target=openupan).start()
    threading.Thread(target=proccopy).start()
    deskcopy()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception:
        log('F',traceback.format_exc())
