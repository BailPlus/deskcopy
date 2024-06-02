import os,shutil,time,deskcopy,traceback
print('9秒后开始卸载。请确保电脑处于解冻状态！',end='\r')
for i in range(9,1,-1):
    print(i,end='\r')
    time.sleep(1)

deskcopy.log('I','开始卸载')
files = (r'D:\upancopy.lnk',r'C:\users\seewo\.gitconfig')
dirs = (r'D:\deskcopy',r'D:\desktop',r'D:\geph',r'C:\users\seewo\.ssh','D:\Portable-Git')

for i in files:
    try:
        os.remove(i)
    except Exception:
        deskcopy.log('E',f'删除文件失败: {i}\n{traceback.format_exc()}')
    else:
        deskcopy.log('I',f'已文件删除: {i}')

for i in dirs:
    try:
        shutil.rmtree(i)
    except Exception:
        deskcopy.log('E',f'删除目录失败: {i}\n{traceback.format_exc()}')
    else:
        deskcopy.log('I',f'已目录删除: {i}')

deskcopy.log('I','卸载完成，请继续将python卸载')
input() #保留控制台
