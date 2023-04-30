#Copyright Bail 2023
#deskcopy:open 打开复制辅助模块

ARGV = '--open' #打开复制参数

import sys,subprocess

def main():
    subprocess.run(fr'pythonw D:\deskcopy\deskcopy.py {ARGV} "{sys.argv[1]}"')
    return 0

if __name__ == '__main__':
    sys.exit(main())
