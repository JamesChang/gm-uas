# -*- encoding: utf-8 -*-
import logging,sys
import settings
import os


def _pathrule(type):
    from time import strftime,localtime
    time = strftime('%Y-%m-%d %H_%M_%S',localtime())
    if not os.path.exists("log"):
        os.mkdir("log")
    return r'.\log\%s %s.log'%(time,type)
    
def run_log():
    rlog = logging.getLogger('runlog')
    rlog.setLevel(logging.DEBUG)
    lpath = _pathrule('run')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logfile.setFormatter(fmt)
    rlog.addHandler(logfile)
    if settings.PRINT_RUNLOG and settings.PRINT_LOG:
        rlog.addHandler(logging.StreamHandler(sys.stdout))  #print to screen
    
def error_log():
    rlog = logging.getLogger('runlog')
    lpath = _pathrule('error')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.ERROR)
    fmt = logging.Formatter("%(asctime)s - %(message)s")
    logfile.setFormatter(fmt)
    rlog.addHandler(logfile)
            
def performance_log():
    alog = logging.getLogger('performancelog')
    alog.setLevel(logging.INFO)
    lpath = _pathrule('performance')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.INFO)
    fmt = logging.Formatter("%(message)s")
    logfile.setFormatter(fmt)
    alog.addHandler(logfile)
    if settings.PRINT_PERFORMANCELOG and settings.PRINT_LOG:
        alog.addHandler(logging.StreamHandler(sys.stdout))  #print to screen
        
def performance_log_roach():
    lpath = _pathrule('performancelog_roach')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.INFO)
    _fmt = logging.Formatter("%(message)s")
    logfile.setFormatter(_fmt)
    arlogger = logging.getLogger('performancelog_roach')
    arlogger.setLevel(logging.INFO)
    arlogger.addHandler(logfile)
    arlogger.info('request\tpoint_time\tuse_time')
    if settings.PRINT_PERFORMANCELOG and settings.PRINT_LOG:
        arlogger.addHandler(logging.StreamHandler(sys.stdout))  #print to screen