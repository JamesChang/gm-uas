# -*- encoding: utf-8 -*-
#from log import Log
import logging
import performance
import msvcrt

def output_log():
    alogger = logging.getLogger('abilitylog')
    info = performance.RSPTIME
    for key in info.keys():
        if 'dict' in str(info[key].__class__):  #是否为dict
            alogger.info(key + ':')     #请求类型
            alogger.info('Time\tAver\tMax\tMin')
            for tm in info[key]:
                alogger.info('%s\t%s\t%s\t%s'%(tm, 
                                                info[key][tm][0], 
                                                info[key][tm][1], 
                                                info[key][tm][2]))
        else:
            alogger.info('%s:%s'%(key, info[key]))
        alogger.info('=' * 20)
        
def output_log_roach():
    arlogger = logging.getLogger('abilitylog_roach')
    info = performance.RSPTIME_ROACH
    count = len(info)
    performance.RSPTIME_ROACH = performance.RSPTIME_ROACH[count:]
    for unit in info[:count]:
        arlogger.info('%s\t%s\t%s'%(unit[0], unit[1], unit[2]))
    arlogger.info('#'*30)
                         
class Control(object):
#===============================================================================
#    def __init__(selfparams):
#        cd = raw_input()
#        pass
#===============================================================================
    
    def exit(self):
        output_log()
        output_log_roach()
        #Log().ability_log()