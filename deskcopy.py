#Copyright Bail 2022
#deskcopy 桌面拖入文件自动复制 v1.0_1
#2022.11.18-2022.12.10

TARGET = 'D:\\desktop'

import os,time,shutil,sys

os.chdir(os.path.join(os.path.expanduser('~'),'Desktop'))
filenum = len(os.listdir())

def is_file_number_change():
    '''检测是否出现新文件
返回值:当前（改变后的）文件列表(list)
    技术细节：获取桌面文件列表，统计文件数量，和原来的数量对比。
            若增多，说明有新文件，则退出阻塞，进行下一步操作。'''
    global filenum
    nowfilenum = len(os.listdir())
    if nowfilenum > filenum:
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
def main():
    while True:
        if is_file_number_change():
            filelst = os.listdir()
            for i in filelst:
                target = os.path.join(TARGET,i)
                shutil.copy(i,target)
            print(f'已复制 at {time.time()}')
        time.sleep(30 if len(sys.argv) == 1 else 1)    #如果传入参数就是调试模式，缩短间隔时间

if __name__ == '__main__':
    main()
