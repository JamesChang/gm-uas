#-*- encoding: utf-8 -*-
import stackless
import time

import settings

import context

#from log import Log  #######################
import logging,sys

import ability

from account import Account

#import parameter  #######################

def _idle(seconds=settings.IDLE_INTERVAL):
  time.sleep(seconds)

running = False

#PARA = parameter.get()  #######################

#Log().run_log()  #设置log  #######################
#USERLIST = Account().parse(PARA.userrule, PARA.psdrule)

def _pathrule(type):  #*****************************************
  from datetime import datetime
  tm = time.strftime('%Y-%m-%d %H_%M_%S',time.gmtime())
  return r'.\data\log\\' + tm + ' ' + type + '.txt'


if __name__ == "__main__":
  import logging,sys
  logging.getLogger().setLevel(logging.DEBUG)
  if settings.PRINT_LOG:
      logging.getLogger().addHandler(logging.StreamHandler(sys.stdout)) #加入标准输出源
  lpath = _pathrule('runlog')
  logfile = logging.FileHandler(lpath, "w+")
  logfile.setLevel(logging.DEBUG)
  _fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
  logfile.setFormatter(_fmt)
  rlogger = logging.getLogger('runlog')
  rlogger.setLevel(logging.DEBUG)
  rlogger.addHandler(logfile)
  
  lpath = _pathrule('abilitylog')
  logfile = logging.FileHandler(lpath, "w")
  logfile.setLevel(logging.INFO)
  _fmt = logging.Formatter("%(message)s")
  logfile.setFormatter(_fmt)
  alogger = logging.getLogger('abilitylog')
  alogger.setLevel(logging.INFO)
  alogger.addHandler(logfile)
  
  lpath = _pathrule('abilitylog_roach')
  logfile = logging.FileHandler(lpath, "w+")
  logfile.setLevel(logging.INFO)
  _fmt = logging.Formatter("%(message)s")
  logfile.setFormatter(_fmt)
  arlogger = logging.getLogger('abilitylog_roach')
  arlogger.setLevel(logging.INFO)
  arlogger.addHandler(logfile)
  
  
  from optparse import OptionParser
  OPT = OptionParser(usage = "usage: %prog [options] arg...")
  OPT.add_option('-u', '--users', 
                      default = 't1-19', 
                      metavar = 'USERRULE', 
                      help = 'set testing users[default:%default]', 
                      dest = 'userrule'
                      )
  OPT.add_option('-p', '--password', 
                      default = 'a', 
                      metavar = 'PASSWORDRULE', 
                      help = 'set testing password[default:%default]', 
                      dest = 'psdrule'
                      )
  (paradict, paralist) = OPT.parse_args()
  PARA = paradict
  USERLIST = Account().parse(PARA.userrule, PARA.psdrule)
  arlogger.info('users:%s'%(PARA.userrule))
  arlogger.info('request\tpoint_time\tuse_time')

#===============================================================================
# 
#===============================================================================

  import random
  random.seed(time.time())
  
  print "monkey-patching socket..."
  import stacklesssocket
  stacklesssocket.install()

  print "starting delay service..."
  import scheduler
  context.delay_service=scheduler.DelayScheduler()
  context.delay_service.start()
  ablt_ch = stackless.channel()  #性能数据传输通道
  stackless.tasklet(ability.Ability)(ablt_ch)  #创建性能统计进程
  from user import User
  print "loading users..."
  for user in USERLIST:
    u = User(*user)
    stackless.tasklet(u.do)(ablt_ch)

  print "starting stackless python scheduler..."
  running = True
  while(running):
    #TODO: exception handling
    stackless.run()
    _idle()
    
  context.delay_service.stop()