import traceback as err
from deskcopy import log
from time import sleep
sleep(5)
try:
    import psutil as p
    ps = p.pids()
    log('D',str(ps))
    for i in ps:
        pp = p.Process(i)
        log('D',pp.cmdline())
except:
    log('F',err.format_exc())
