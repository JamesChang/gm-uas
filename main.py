#-*- encoding: utf-8 -*-
import stackless
import time

import settings

import user

import context

import log

import performance

from logging import getLogger

from account import Account

import parameter

def _idle(seconds=settings.IDLE_INTERVAL):
    time.sleep(seconds)

def get_time(user_len):
    settings.BEFORE_READY *= user_len

    settings.BEFORE_LISTARENA *= user_len

    settings.BEFORE_SUBRESULT *= user_len

    settings.USER_RANDOM_SLEEP_TIME *= user_len

running = False

PARA = parameter.get()

log.run_log()  #设置log
log.error_log()  #提取runlog中的error信息
log.performance_log_roach()  #设置小强需要的log
RLOG = getLogger('runlog')

USERLIST = Account().parse(PARA.userrule, PARA.psdrule)

if __name__ == "__main__":
  import random
  random.seed(time.time())
  
  RLOG.info("monkey-patching socket...")
  import stacklesssocket
  stacklesssocket.install()

  RLOG.info("starting delay service...")
  import scheduler
  context.delay_service=scheduler.DelayScheduler()
  context.delay_service.start()
  stackless.tasklet(performance.Performance)()  #创建性能统计进程
  RLOG.info("loading users...")
  get_time(len(USERLIST))
  for userpara in USERLIST:
    u = user.Arena(*userpara)
    stackless.tasklet(u.do)()

  RLOG.info("starting stackless python scheduler...")
  running = True
  while(running):
    #TODO: exception handling
    stackless.run()
    _idle()
    
  context.delay_service.stop()