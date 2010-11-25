# -*- encoding: utf-8 -*-
import logging,sys
import settings
import os


def _pathrule(type):
    from time import strftime,localtime
    time = strftime('%Y-%m-%d %H_%M_%S',localtime())
    if not os.path.exists("log"):
        os.mkdir("log")
    return r'.\log\%s %s.txt'%(time,type)
    
def run_log():
    rlog = logging.getLogger('runlog')
    rlog.setLevel(logging.DEBUG)
    lpath = _pathrule('runlog')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logfile.setFormatter(fmt)
    rlog.addHandler(logfile)
    if settings.PRINT_RUNLOG:
        rlog.addHandler(logging.StreamHandler(sys.stdout))  #print to screen
    
def error_log():
    rlog = logging.getLogger('runlog')
    lpath = _pathrule('error')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.ERROR)
    fmt = logging.Formatter("%(asctime)s - %(message)s")
    logfile.setFormatter(fmt)
    rlog.addHandler(logfile)
            
def ability_log():
    alog = logging.getLogger('abilitylog')
    alog.setLevel(logging.INFO)
    lpath = _pathrule('abilitylog')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.INFO)
    fmt = logging.Formatter("%(message)s")
    logfile.setFormatter(fmt)
    alog.addHandler(logfile)
    if settings.PRINT_ABILITYLOG:
        alog.addHandler(logging.StreamHandler(sys.stdout))  #print to screen
        
def ability_log_roach():
    lpath = _pathrule('abilitylog_roach')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.INFO)
    _fmt = logging.Formatter("%(message)s")
    logfile.setFormatter(_fmt)
    arlogger = logging.getLogger('abilitylog_roach')
    arlogger.setLevel(logging.INFO)
    arlogger.addHandler(logfile)
    arlogger.info('request\tpoint_time\tuse_time')
    if settings.PRINT_ABILITYLOG:
        arlogger.addHandler(logging.StreamHandler(sys.stdout))  #print to screen