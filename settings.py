#-*- encoding: utf-8 -*-
######################
# ENVIRONMENT
######################

EVENT = [1,2,3]

MAPS = [[],[6,46,47,48,49], [34,35], [40,41,42,43,44,45]]

CREAT_ARENA_PARASFORMAT=[{},
                         {"userid":None, 
                          "mode":u"对战", 
                          "map":None, 
                          "private":"false",
                         },
                         {"userid":None, 
                          "mode":"rd", 
                          "private":"false",
                         },
                         {"userid":None, 
                          "mode":u"对战", 
                          "map":None, 
                          "private":"false",
                         }   
                        ]


######################
# LOG
######################

PRINT_RUNLOG = True

PRINT_PERFORMANCELOG = False

PRINT_LOG = True  #whether print log

######################
# RANDOM WAIT TIME
######################

BEFORE_READY = 5

BEFORE_LISTARENA = 11

BEFORE_SUBRESULT = 47

USER_RANDOM_SLEEP_TIME = 10

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
#MSG_SVR = ("172.16.0.14", 13340)

#arena server network address in format of (string host, int port)
#ARENA_SVR = ("172.16.0.13", 8090)

#PY_SVR = ("172.16.0.13", 84)

######################
# Instance Config
######################
#load ../conf/default.py
import os
_filename = "config/default.py"
if (os.path.exists(_filename)):
  execfile(_filename)
