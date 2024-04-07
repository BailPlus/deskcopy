import traceback as err
from deskcopy import log
from time import sleep
sleep(5)
try:
    import psutil as p
    ps = p.pids()
    log('D',str(ps))
    for i in ps:
        try:
            pp = p.Process(i)
            c = pp.cmdline()
            n = pp.name()
        except p.AccessDenied:
            pass
        log('D',str(c)+'\n'+str(n))
except:
    log('F',err.format_exc())
