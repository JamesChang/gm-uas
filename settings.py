#-*- encoding: utf-8 -*-
######################
# ENVIRONMENT
######################

#MAPS = {'1':[6,46,47,49],'2':[83,86],'3':[41,42,43,44]} #all

#MAPS = {'2':[86]} #imba

MAPS = {'1':[49]} #1v1

CREAT_ARENA_PARASFORMAT={'1':{"userid":None, 
                              "mode":"对战", 
                              "map":None, 
                              "private":"false"},
                         '2':{"userid":None, 
                              "mode":"rd", 
                              "private":"false"},
                         '3':{"userid":None, 
                              "mode":"对战", 
                              "map":None, 
                              "private":"false"}}


######################
# LOG
######################

PRINT_RUNLOG = True

PRINT_PERFORMANCELOG = False

PRINT_LOG = False  #whether print log

######################
# RANDOM WAIT TIME
######################

BEFORE_READY = 0.02

BEFORE_LISTARENA = 0.02

BEFORE_SUBRESULT = 0.5

USER_RANDOM_SLEEP_TIME = 0.2

######################
# GENERAL SETTINGS
######################

#GLOBAL idle time to prevent busy waiting when no new stackless tasklet in stackless scheduler.
IDLE_INTERVAL = 0.03

PRINT_LOG = True  #whether print log

######################
# OUTER SERVICE
######################

#message server network address in format (string host, int port)
#MSG_SVR = ("180.153.139.142", 13340)
MSG_SVR = ("172.16.4.1", 16667)

#arena server network address in format of (string host, int port)
#ARENA_SVR = ("180.153.139.141", 8090)
ARENA_SVR = ("172.16.4.16", 8080)

#PY_SVR = ("180.153.139.141", 84)
PY_SVR = ("172.16.4.2", 8084)

######################
# Instance Config
######################
#load ../conf/default.py
import os
_filename = "config/default.py"
if (os.path.exists(_filename)):
  execfile(_filename)
