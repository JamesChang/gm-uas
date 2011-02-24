#-*- encoding: utf-8 -*-
######################
# ENVIRONMENT
######################

MAPS = {'1':[6,46,47,49],'2':[83,86],'3':[41,42,43,44]} #all

MAPS = {'1':[46]} #1v1

CREAT_ARENA_PARASFORMAT=[{},
                         {"userid":None, 
                          "mode":"对战", 
                          "map":None, 
                          "private":"false",
                         },
                         {"userid":None, 
                          "mode":"rd", 
                          "private":"false",
                         },
                         {"userid":None, 
                          "mode":"对战", 
                          "map":None, 
                          "private":"false",
                         }   
                        ]


######################
# LOG
######################

PRINT_RUNLOG = True

PRINT_PERFORMANCELOG = False

PRINT_LOG = False  #whether print log

######################
# RANDOM WAIT TIME
######################

BEFORE_READY = 0.2

BEFORE_LISTARENA = 0.2

BEFORE_SUBRESULT = 60

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
MSG_SVR = ("180.153.139.142", 13340)

#arena server network address in format of (string host, int port)
ARENA_SVR = ("180.153.139.141", 8090)

PY_SVR = ("180.153.139.141", 84)

######################
# Instance Config
######################
#load ../conf/default.py
import os
_filename = "config/default.py"
if (os.path.exists(_filename)):
  execfile(_filename)
