#-*- encoding: utf-8 -*-
import stackless
import time

import settings

import context

import log

import performance

from account import Account

import parameter

def _idle(seconds=settings.IDLE_INTERVAL):
  time.sleep(seconds)

running = False

PARA = parameter.get()

log.run_log()  #设置log
log.error_log()  #提取runlog中的error信息
log.performance_log_roach()  #设置小强需要的log
USERLIST = Account().parse(PARA.userrule, PARA.psdrule)

if __name__ == "__main__":
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
  stackless.tasklet(performance.Performance)(ablt_ch)  #创建性能统计进程
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