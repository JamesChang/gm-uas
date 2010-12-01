# -*- encoding: utf-8 -*-

from logging import getLogger

PRLOG = getLogger('performancelog_roach')

RSPTIME = {}
RSPTIME_ROACH = []
PUT = {}
RESOURCE = {}
HITS = {}
USERS = {}
ERROR = {}

def _aver(old, new):
    return (old + new)/2

def _max(old, new):
    if old > new:
        return old
    else:
        return new

def _min(old, new):
    if old < new:
        return old
    else:
        return new
    
def _count(old):
    return old + 1

def _sreach_location(list, elmt):
    m = len(list)/2
    if elmt < list[m]:
        if m:
            l = 0 + _sreach_location(list[:m], elmt)[0]
        else:
            l = 0
    elif elmt > list[m]:
        if m:
            l = m + _sreach_location(list[m:], elmt)[0]
        else:
            l = 1
    return (l,m)

def _median(list, elmt):
    d = _sreach_location(list, elmt)
    list.insert(d[0], elmt)
    return d[1]
    
#===============================================================================
# def _output(dict):
#    for key in dict.keys():
#        log().ability_log(key + ':' + dict(key))
#===============================================================================

class Performance(object):
    def __init__(self, ch):
        while True:
            rinf = ch.receive() #接收性能数据,rinf[0]测试类型,rinf[1]测试数据
            if rinf[0] == 'rsptime':
                #self.response_time(rinf[1])
                #RSPTIME_ROACH.append(rinf[1])
                PRLOG.info('%s\t%s\t%s'%(rinf[1][0],rinf[1][1],rinf[1][2]))
            elif rinf[0] == 'put' :
                self.throughput()
            elif rinf[0] == 'resource' :
                self.resource_utilization()
            elif rinf[0] == 'hits' :
                self.hits_per_second()
            elif rinf[0] == 'error' :
                self.error_stat(rinf[1])

    def response_time(self, dlist): #响应时间,dlist[0]请求类型,dlist[1]触发时间,dlist[2]响应时间
        if dlist[0] in RSPTIME.keys():
            if dlist[1] in RSPTIME[dlist[0]]:
                okey = dlist[1]
            else:
                okey = max(RSPTIME[dlist[0]].keys())
            averv = _aver(RSPTIME[dlist[0]][okey][0], dlist[2])
            maxv = _max(RSPTIME[dlist[0]][okey][1], dlist[2])
            minv = _min(RSPTIME[dlist[0]][okey][2], dlist[2])
            RSPTIME[dlist[0]][dlist[1]] = [averv, maxv, minv]
        else:
            RSPTIME[dlist[0]] = {}
            RSPTIME[dlist[0]][dlist[1]] = [dlist[2], dlist[2], dlist[2]]
    
    def throughput(self): #吞吐量
        pass
    
    def resource_utilization(self): #资源使用率
        pass
    
    def hits_per_second(self): #点击响应数
        pass
    
    def concurrent_users(self): #并发用户数
        pass
    
    def error_stat(self, dlist):  #错误统计
        if not dlist[0] in self.inf.keys():
            self.inf[dlist[0]] = {}
            self.inf[dlist[0]]['Time'] = []  #请求时间点
            self.inf[dlist[0]]['Count'] = []
            self.inf[dlist[0]]['Time'].append(dlist[2])
            self.inf[dlist[0]]['Count'].append(_count(0))
        else:
            oindex = len(self.inf[dlist[0]]['Time']) - 1
            self.inf[dlist[0]]['Time'].append(dlist[2])
            self.inf[dlist[0]]['Count'].append(_count(self.inf[dlist[0]]['Count'][oindex]))