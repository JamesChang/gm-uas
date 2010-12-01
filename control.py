# -*- encoding: utf-8 -*-
#import logging
#import performance
#
#def output_log():
#    alogger = logging.getLogger('performancelog')
#    info = performance.RSPTIME
#    for key in info.keys():
#        if 'dict' in str(info[key].__class__):  #是否为dict
#            alogger.info(key + ':')     #请求类型
#            alogger.info('Time\tAver\tMax\tMin')
#            for tm in info[key]:
#                alogger.info('%s\t%s\t%s\t%s'%(tm, 
#                                                info[key][tm][0], 
#                                                info[key][tm][1], 
#                                                info[key][tm][2]))
#        else:
#            alogger.info('%s:%s'%(key, info[key]))
#        alogger.info('=' * 20)
#        
#
#
#def exit():
#    output_log_roach()