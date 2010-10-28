import time 
import threading
import stackless
import heapq

class DelayScheduler(object):
  
  def __init__(self, tick=0.200):
    self.tasks = []
    self.tick = tick
    self.running = False
    self.thread=None
    self.mutex = threading.RLock()
    
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
    """caller will be blocked until delay time has passed. thread safe."""
    ct= time.time()
    channel = stackless.channel()
    channel.preference=1 #prefer the sender
    self.mutex.acquire()
    heapq.heappush(self.tasks, (ct+delay, delay, channel))
    self.mutex.release()
    channel.receive()
    
  def _do_work(self):
    while(self.running):
      self.mutex.acquire()
      while len(self.tasks)>0:
        t_expired, t_delay, channel = self.tasks[0] 
        ct = time.time()
        if t_expired < ct:
          heapq.heappop(self.tasks)
          if channel.balance<0: # we do not need to check this. should always be <0
            channel.send(None)
        else:
          break
      self.mutex.release()
      time.sleep(self.tick)
