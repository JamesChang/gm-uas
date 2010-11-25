
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
