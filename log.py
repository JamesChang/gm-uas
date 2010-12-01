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
    plog = logging.getLogger('performancelog')
    plog.setLevel(logging.INFO)
    lpath = _pathrule('performance')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.INFO)
    fmt = logging.Formatter("%(message)s")
    logfile.setFormatter(fmt)
    plog.addHandler(logfile)
    if settings.PRINT_PERFORMANCELOG and settings.PRINT_LOG:
        plog.addHandler(logging.StreamHandler(sys.stdout))  #print to screen
        
def performance_log_roach():
    prlogger = logging.getLogger('performancelog_roach')
    prlogger.setLevel(logging.INFO)
    
    lpath = _pathrule('performancelog_roach')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.INFO)
    fmt = logging.Formatter("%(message)s")
    logfile.setFormatter(fmt)
    prlogger.addHandler(logfile)
    #prlogger.info('request\tpoint_time\tuse_time')
    if settings.PRINT_PERFORMANCELOG and settings.PRINT_LOG:
        prlogger.addHandler(logging.StreamHandler(sys.stdout))  #print to screen
        
def output_log_roach():
    prlogger = logging.getLogger('performancelog_roach')
#    count = len(info)
#    performance.RSPTIME_ROACH = performance.RSPTIME_ROACH[count:]
    for unit in performance.RSPTIME_ROACH:
        prlogger.info('%s\t%s\t%s'%(unit[0], unit[1], unit[2]))
    performance.RSPTIME_ROACH = []
    #prlogger.info('#'*30)
    
def output_log():
    plogger = logging.getLogger('performancelog')
    info = performance.RSPTIME
    for key in info.keys():
        if 'dict' in str(info[key].__class__):  #是否为dict
            plogger.info(key + ':')     #请求类型
            plogger.info('Time\tAver\tMax\tMin')
            for tm in info[key]:
                plogger.info('%s\t%s\t%s\t%s'%(tm, 
                                               info[key][tm][0], 
                                               info[key][tm][1], 
                                               info[key][tm][2]))
        else:
            plogger.info('%s:%s'%(key, info[key]))
        plogger.info('=' * 20)