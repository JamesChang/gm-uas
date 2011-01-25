# -*- encoding: utf-8 -*-
import stackless
import urllib2, urllib
import socket
import struct 
import time,random
from datetime import datetime
import logging

import settings 
import context
import control


from performance import PERF_CH

RLOG = logging.getLogger('runlog')

#game result for dota
def make_game_result():
    from protobuf.res_gameres_pb2 import GameMessage
    rst = GameMessage()
    war3 = rst.war3.add()
    war3.header.war3Version="War3-1.23-6352"
    war3.header.messageType = "game result"
    war3.header.battleType="Dota"
    war3.header.time = 33225
    war3.header.userIDOfSender = 12345
    d = rst.SerializeToString()
    import base64
    d=base64.standard_b64encode(d)
    return d

class User(object):
    def __init__(self,name, password):
        self.name = name
        self.password = password
        self.id = None # user id
        self.sid = None #session id
        self.arena=None #当前所在的arena ID
        self.sock = None #socket 连接
        self.switch = None #事务流程开关
        self.event = None
        self.content = None
        self.error = 0
        self.game_result = make_game_result()
        self.table = [('userTCPLogin',self.on_logined),
                      ('',self.on_logouted)
                      ]
        self.received_packages = stackless.channel()

    def _receive_package(self):
        """按照msg server的协议，解析数据包。输出数据包到self.received_packages  （（命令码和负载数据）"""
        bytes = ''
        while self.switch:
            r= self.sock.recv(2048)
            if r=='':
                raise Exception("connection closed")
            else:
                bytes = self._parse_package(bytes + r)

    def _parse_package(self, bytes):
        if len(bytes) >= 2: #小于数据包长度标示符
            l = struct.unpack("<H", bytes[:2])[0]
            if len(bytes) >= (l + 2): #此包是否完整
                raw_package = bytes[:l+2]
                bytes=bytes[l+2:]
                package = struct.unpack("<HIHHI%ss"%(l-12), raw_package)
                #TODO: 检查返回数据的格式
                self.received_packages.send((package[3], package[5]))
                bytes = self._parse_package(bytes)
        return bytes
  
    def _listen_messages(self):
        """循环监听消息"""
        from protobuf.msg_base_pb2 import Msg
        from protobuf.res_base_pb2 import Response
        pbr = Response()
        msg = Msg()
        while self.switch: 
            cmd, payload = self.received_packages.receive()
            if cmd==0x9003:
                msg.ParseFromString(payload)  #将bit流解析为对象
                srv = [srv for srv in self.table if srv[0] == msg.code]
                if srv:
                    srv[0][1](msg)
#                if msg.code == 0x2103:
#                    #好友状态改变
#                    pass
#                elif msg.code == 0x2301:
#                    self.on_arenaJoined(msg)
#                elif msg.code == 0x2302:
#                    self.on_arenaLeaved(msg)
#                elif msg.code == 0x2303:
#                    pass
#                elif msg.code == 0x2304:
#                    pass
#                elif msg.code ==0x2305:
#                    self.on_arenaMemberUpdated(msg)
#                elif msg.code == 0x2307:
#                    self.on_arenaChated(msg)
#                elif msg.code == 0x2308:
#                    pass
#                elif msg.code == 0x230c:
#                    pass
#                elif msg.code == 0x230b:
#                    self.on_arenaStarted(msg)
#                elif msg.code == 0x230d:
#                    self.on_arenaEnded(msg)
#                else:
#                    RLOG.info('unknow Msg %s'%msg)
            elif cmd==0x9002: #登录登出成功消息
                pbr.ParseFromString(payload)  #将bit流解析为对象
                srv = [srv for srv in self.table if srv[0] == pbr.subMsg][0]
                srv[1](pbr)
#                if pbr.subMsg == 'userTCPLogin':
#                    self.on_logined(pbr)
#                elif pbr.subMsg == '':
#                    self.on_logouted(pbr)
#                else:
#                    RLOG.info('unknow Response %s'%pbr)
            elif cmd==0x9010: #应为: 0x9010 msg server 发送,说明是正常登陆,被踢,还是踢人
                pass
            else:
                hex_text = "".join(["%02X "%ord(c) for c in payload])
                RLOG.error("unknow package received %s %s"%(cmd, hex_text))
    
    def _java_make_url(self, req):
        """组合URL，连接JAVA写的APP服务器"""
        return "http://%s:%s/app-core/%s?alt=pbbin"%(settings.ARENA_SVR[0],
                                                     settings.ARENA_SVR[1],
                                                     req,
                                                     )

    def _py_make_url(self, req):
        """组合URL，连接PYTHON写的APP服务器"""
        return "http://%s:%s/campus/api/%s?alt=pbbin"%(settings.PY_SVR[0],
                                                       settings.PY_SVR[1],
                                                       req,
                                                       )
  
    def _check_pb_response_ok(self, pb):
        """检查返回的probobuf结果是否正常"""
        return pb.code/100000 == 2
    
    def _send_request(self, partial_url, data=None, srv='java'):
        """发送请求，解析结果，错误处理, 返回pb"""
        if data is not None:
            data = urllib.urlencode(data)
        if srv == 'java':
            url = self._java_make_url(partial_url)
        elif srv == 'py':
            url = self._py_make_url(partial_url)
        ptime = datetime.fromtimestamp(time.time())
        stime = time.clock()
        r = urllib2.urlopen(url, data)
        etime = time.clock()
        ptime = datetime.strftime(ptime,"%Y-%m-%d %H:%M:%S.%f")
        d=r.read()
        #TODO: 处理HTTP错误
        from protobuf.res_base_pb2 import Response
        pbr=Response()
        pbr.ParseFromString(d)
        return {'mtime' : etime - stime, 
                'ptime' : ptime, 
                'data' : pbr,
                }

    def _sleep(self, seconds):
        """休息，休息一会儿"""
        context.delay_service.delay_caller(seconds)
        
    def _heart(self):
        while 1:
            self._sleep(15)
            self.sock.send("\x02\x00ab")
  ##########################################################################
  # 用户行为
  ##########################################################################
    
    def do(self):
        """开始工作"""
        #random sleep for a while
        self.ch = PERF_CH
        st = random.random()*settings.USER_RANDOM_SLEEP_TIME
        self._sleep(st)
        self.login()

    def login(self):
        """登陆msg服务器"""
        self.sock = socket.socket()
        self.sock.connect(settings.MSG_SVR)
        
        #new tasklet to receive network data
        self.switch = True
        stackless.tasklet(self._receive_package)()
        stackless.tasklet(self._listen_messages)()
        
        
        from protobuf.soc_login_pb2 import SocketLoginMessage
        msg = SocketLoginMessage()
        msg.code=1
        msg.userName = self.name
        msg.password = self.password
        msg_data = msg.SerializeToString()
        
        #TODO: 网络错误处理
        len_msg_data = len(msg_data)
        d=struct.pack("<HIHHI%ss"%len_msg_data,
                      len_msg_data + 12,
                      0xABDE, # magic code
                      len_msg_data + 12,
                      0x9001, # 9001 表示flash请求，9002是相应
                      0,
                      msg_data)
        
        t=self.sock.send(d);
        RLOG.info('%s login'%self.name)

    def logout(self):
        """登出"""
        from protobuf.soc_login_pb2 import SocketLoginMessage
        msg = SocketLoginMessage()
        msg.code=3
        msg.sessionID = self.sid
        msg_data = msg.SerializeToString()
          
        #TODO: 网络错误处理
        len_msg_data = len(msg_data)
        d=struct.pack("<HIHHI%ss"%len_msg_data,
                      len_msg_data + 12,
                      0xABDE, # magic code
                      len_msg_data + 12,
                      0x9001, # 9001 表示flash请求，9002是相应
                      0,
                      msg_data)
        self.sock.send(d)
        RLOG.debug("%s_%s logout"%(self.name,self.id))
        
  ##########################################################################
  # 消息处理
  ##########################################################################
    def on_logouted(self, pbr):
        if self._check_pb_response_ok(pbr):
            RLOG.debug('%s_%s logouted'%(self.name, self.id))
            self.switch = False
            self.sock.close()
            self.id = None
            self.sid = None
            self.arena = None
            self.event = None
        else:
            RLOG.error("LOGOUT ERROR %s"%pbr)
  
    def on_logined(self, pbr):
      if self._check_pb_response_ok(pbr):
          self.sid = pbr.userTCPLogin.sid
          self.id = pbr.userTCPLogin.uid
          RLOG.debug("%s_%s logined"%(self.name, self.id))
          #receive one unknow package then discard it, generated by Message Server
          self._sleep(random.random()*settings.BEFORE_LISTARENA)
          self.logout()
      else:
          #TODO: proto 解析失败的处理
          RLOG.error("LOGIN ERROR %s"%pbr)


class Arena(User):
    def __init__(self,name, password):
        super(Arena,self).__init__(name, password)
        self.table += [(0x2301,self.on_arenaJoined),
                       (0x2302,self.on_arenaLeaved),
                       (0x2305,self.on_arenaMemberUpdated),
                       (0x230b,self.on_arenaStarted),
                       (0x230d,self.on_arenaEnded)
                       ]
    
    def list_arena(self):
        """获取arena列表，如果有房间就加入，没有房间就创建一个等人进"""
        self.event = random.sample(settings.EVENT, 1)[0]
        rps = self._send_request("events/%s/list"%self.event)
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            #没满的房间
            RLOG.info('%s_%s list_arena'%(self.name,self.id))
            rooms = [i for i in r.ca03ArenaList.items if i.mcount.split("/")[0] != i.mcount.split("/")[1]]
            n = len(rooms)
            if (n==0):
                self.create_arena()
            else:
                #随机找一个
                a = random.sample(rooms,1)
                self.enter_arena(a[0].id)
        else:
            send = False
            RLOG.error("list_arena_%s_%sRESPONSE ERROR: %s"%(self.name,self.id, r))
    #      self.ch.send(['error', ['list_arena', 
    #                              rps['ptime'], 
    #                              r.code]])
        if send:
            self.ch.send(['rsptime', ['list_arena', 
                                      rps['ptime'], 
                                      rps['mtime']]])
        
    def create_arena(self):
        """创建房间"""
        self.paras = settings.CREAT_ARENA_PARASFORMAT[self.event]
        if settings.MAPS[self.event]:
            self.paras['map'] = random.sample(settings.MAPS[self.event], 1)[0]
        else:
            self.paras['map'] = None
        self.paras['userid'] = self.id
        rps=self._send_request("events/%s/create"%self.event,
                                self.paras
                              )
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            RLOG.info('%s_%s create_arena'%(self.name,self.id))
        else:
            send = False
            RLOG.error("create_arena_%s_%sRESPONSE ERROR: %s"%(self.name, self.id, r))
        if send:
            self.ch.send(['rsptime', ['create_arena', 
                                  rps['ptime'], 
                                  rps['mtime']]])
    
    def enter_arena(self, arena_id):
        """加入一个房间"""
        rps=self._send_request("arenas/%s/enter"%arena_id, {"userid":self.id})
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            RLOG.info('%s_%s enter_arena'%(self.name,self.id))
        else:
            if r.code == 419004:
            # arena is full
                self.list_arena()
            elif r.code/1000 == 404:
                # arena does not exist
                self.list_arena()
            elif r.code/1000 == 403:
                # arena has begin
                self.list_arena()
            else:
                send = False
                RLOG.error("enter_arena_%s_%sRESPONSE ERROR: %s"%(self.name, self.id, r))    
        if send:
            self.ch.send(['rsptime', ['enter_arena', 
                                      rps['ptime'], 
                                      rps['mtime']]])

    def make_ready(self):
        """准备"""
        assert self.arena is not None
        rps=self._send_request("arenas/%s/ready"%self.arena, {"userid":self.id})
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            RLOG.info('%s_%s make_ready'%(self.name,self.id))
        else:
            send = False
            RLOG.error("make_ready_%s_%sRESPONSE ERROR: %s"%(self.name, self.id, r))
            #TODO: 处理各种失败，包括人不在Arena, arena已经开始等等异常。不重要，可以不做。
        if send:
            self.ch.send(['rsptime', ['make_ready', 
                                      rps['ptime'], 
                                      rps['mtime']]])

    def leave_arena(self):
        """离开房间"""
        assert self.arena is not None
        rps=self._send_request("arenas/%s/leave"%self.arena, {"userid":self.id})
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            RLOG.info("%s_%s leave_arena %s"%(self.name, self.id, self.arena))
        else:
            send = False
            RLOG.error("leave_arena_%s_%sRESPONSE ERROR: %s"%(self.name, self.id, r))
        if send:
            self.ch.send(['rsptime', ['leave_arena', 
                                    rps['ptime'], 
                                    rps['mtime']]])
    def start_game(self):
        """开始游戏"""
        assert self.arena is not None
        rps=self._send_request("arenas/%s/start"%self.arena, {"userid":self.id})
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            RLOG.info("%s_%s start_arena %s"%(self.name, self.id, self.arena))
        else:
            if (r.code/1000 == 403):
                #not in this arena or not the leader or has started, just ignore this action
                pass
            elif(r.code/1000 == 419):
                #someone in the arena is not ready or offline or they all sit at the  same side.
                pass
            else:
                send = False
                RLOG.error("start_game_%s_%sRESPONSE ERROR: %s"%(self.name, self.id, r))
        if send:
            self.ch.send(['rsptime', ['start_game', 
                                      rps['ptime'], 
                                      rps['mtime']]])
        
    def submit_result(self):
        """提交游戏结果"""
        assert self.arena is not None
        rps=self._send_request("arenas/%s/submit_result"%self.arena, {"userid":self.id, "result":self.game_result})
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            RLOG.debug("%s_%s submit_result %s"%(self.name, self.id, self.arena))
        else:
            if r.code == 403000:
                pass
            else:
                send = False
                RLOG.error("submit_result_%s_%sRESPONSE ERROR: %s"%(self.name, self.id, r))
        if send:
            self.ch.send(['rsptime', ['submit_result', 
                                      rps['ptime'], 
                                      rps['mtime']]])
#===============================================================================
# return message
#===============================================================================
    def on_logined(self, pbr):
        if self._check_pb_response_ok(pbr):
            self.sid = pbr.userTCPLogin.sid
            self.id = pbr.userTCPLogin.uid
            RLOG.debug("%s_%s logined"%(self.name, self.id))
            #receive one unknow package then discard it, generated by Message Server
            self._sleep(random.random()*settings.BEFORE_LISTARENA)
            stackless.tasklet(self._heart)()
            self.list_arena()
        else:
            #TODO: proto 解析失败的处理
            RLOG.error("LOGIN ERROR %s"%pbr)

    def on_arenaJoined(self, msg):
        """我加入了一个房间"""
        self.arena = msg.arenaJoined.arena.id
        RLOG.debug("%s_%s arenaJoined %s"%(self.name, self.id, self.arena))
        self._sleep(random.random()*settings.BEFORE_READY)
        if self.arena in context.arena_member.keys():
            context.arena_member[self.arena]+=1
        else:
            context.arena_member[self.arena]=0
        self.make_ready()
        
    def on_arenaLeaved(self, msg):
        """我离开了一个房间"""
        RLOG.debug("%s_%s arenaLeaved %s"%(self.name, self.id, self.arena))
        self.arena = None
        self._sleep(random.random()*settings.BEFORE_LISTARENA)
        self.list_arena()
        
    def on_arenaMemberUpdated(self, msg):
        """用户状态更新，包括自己"""
        if msg.arenaMemberUpdated.userID == self.id and msg.arenaMemberUpdated.arenaID==self.arena:
            #Ready
            if msg.arenaMemberUpdated.ready is not None:
                self.ready = msg.arenaMemberUpdated.ready
            #当自己有开始权限的时候，就开始
            if "start" in msg.arenaMemberUpdated.actions:
                #control.exit()
                if self.arena:
                    self.start_game()

    def on_arenaStarted(self, msg):
        """游戏开始"""
        RLOG.debug("%s_%s arenaStarted %s"%(self.name, self.id, self.arena))
        self._sleep(random.random()*settings.BEFORE_SUBRESULT)
        if self.arena:
            self.submit_result()
      
    def on_arenaEnded(self, msg):
        """游戏结束"""
        RLOG.debug("%s_%s arenaEnded %s"%(self.name, self.id, self.arena))
        self._sleep(random.random()*settings.USER_RANDOM_SLEEP_TIME)
        rno = random.randrange(1,3)
        if rno % 2 == 0:
            self.leave_arena()
        else:
            self.make_ready()
            
class arenaChat(Arena):
    def __init__(self, name, password):
        super(arenaChat,self).__init__(name, password)
        self.table += [(0x2307,self.on_arenaChated)]
    
    def chat(self, content):
        rps=self._send_request("arenas/%s/chat"%self.arena, {"userid":self.id, "content":content})
        send = True
        r = rps['data']
        if (self._check_pb_response_ok(r)):
            RLOG.debug("%s_%s chat %s"%(self.name, self.id, content))
        else:
            send = False
            RLOG.error("chat_%s_%sRESPONSE ERROR: %s"%(self.name, self.id, r))
        if send:
            self.ch.send(['rsptime', ['chat', 
                                      rps['ptime'], 
                                      rps['mtime']]])
            
#===============================================================================
# return message
#===============================================================================
    def on_arenaMemberUpdated(self, msg):
        """用户状态更新，包括自己"""
        if msg.arenaMemberUpdated.userID == self.id and msg.arenaMemberUpdated.arenaID==self.arena:
            #Ready
            if msg.arenaMemberUpdated.ready is not None:
                self.ready = msg.arenaMemberUpdated.ready
            #当自己有开始权限的时候，就开始
            if "start" in msg.arenaMemberUpdated.actions:
                #control.exit()
                if self.arena:
                    if self.content == None and context.arena_member[self.arena]==9:
                        self.content = 0
                        i = 0
                        while True:
                            self._sleep(0.1)
                            context.content[str(i)]=[0]
                            self.chat(str(i))
                            i+=1

    def on_arenaChated(self, msg):
        context.chat_print += 1
        if context.chat_print%1000 == 0:
            RLOG.debug(context.content)
        if context.content[msg.groupChat.content][0]==context.arena_member[self.arena]-1:
            context.content.__delitem__(msg.groupChat.content)
        else:
            if context.content[msg.groupChat.content][0] == 0:
                context.content[msg.groupChat.content].append(msg.uuid)
            context.content[msg.groupChat.content][0]+=1
#      if self.content == None:
#          self.content = int(msg.groupChat.content)
#      if msg.groupChat.content == str(self.content):
#          RLOG.debug("%s_%s arenaChated %s %s"%(self.name, self.id, msg.groupChat.content, msg.uuid))
#          self.content+=1
#          self.error = 0
#      else:
#          RLOG.error("%s_%s should receive %s,but receive %s now %s"%(self.name, self.id, self.content, msg.groupChat.content, msg.uuid))
#          if self.error == 3:
#              self.switch = False
#          else:
#              self.error += 1
