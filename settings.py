
######################
# RANDOM WAIT TIME
######################

BEFORE_READY = 5

BEFORE_LISTARENA = 11

BEFORE_SUBRESULT = 47

######################
# GENERAL SETTINGS
######################

#GLOBAL idle time to prevent busy waiting when no new stackless tasklet in stackless scheduler.
IDLE_INTERVAL = 0.03

USER_RANDOM_SLEEP_TIME = 10

PRINT_LOG = True  #whether print log

######################
# OUTER SERVICE
######################

#message server network address in format (string host, int port)
#MSG_SVR = ("172.16.0.14", 13340)
MSG_SVR = ("192.168.110.198", 13340)
#arena server network address in format of (string host, int port)
#ARENA_SVR = ("172.16.0.13", 8090)
ARENA_SVR = ("192.168.110.44", 8080) 
#PY_SVR = ("172.16.0.13", 84)
PY_SVR = ("192.168.110.54", 84)
#===============================================================================
# #message server network address in format (string host, int port)
# MSG_SVR = ("58.196.146.28", 13340)
# 
# #arena server network address in format of (string host, int port)
# ARENA_SVR = ("58.196.146.37", 8090)
# 
# PY_SVR = ("58.196.146.37", 84)
#===============================================================================