import time 
import threading
import stackless

class DelayScheduler(object):
  
  def __init__(self, tick=0.200):
    self.tasks = []
    self.tick = tick
    self.running = False
    self.thread=None
    
  def start(self):
    if self.running:
      return
    self.running = True
    t=threading.Thread(target=self._do_work, name = "Scheduler_%s"%id(self))
    self.thread=t
    t.start()
    
  def stop(self):
    self.running=False
    
  def delay_caller(self, delay):
    """caller will be blocked until delay time has passed"""
    #TODO: synchronized
    #TODO: use priority queue, instead of sortin every time
    ct= time.time()
    channel = stackless.channel()
    channel.preference=1 #prefer the sender
    self.tasks.append((ct+delay, delay, channel))
    self.tasks.sort()
    channel.receive()
    
  def _do_work(self):
    while(self.running):
      if len(self.tasks)>0:
        t_expired, t_delay, channel = self.tasks[0]
        ct = time.time()
        if t_expired < ct:
          #TODO: there would be a risk to block this thread if codes below are not synchronized.
          if channel.balance<0:
            channel.send(None)
          del self.tasks[0]
      
      time.sleep(self.tick)
