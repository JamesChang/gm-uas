import os,sys, time

QUANTILE = [0.5, 0.95, 0.96, 0.97, 0.98, 0.99]

class RequestEntry(object):
  def __init__(self, name):
    self.name = name
    self.count = 0
    self.times = []
    self.quantile = []
    
  def add(self, t):
    self.times.append(t)
  def calculate(self):
    self.count = len(self.times)
    self.times.sort()
    for q in QUANTILE:
      i = int(q*self.count)
      self.quantile.append(self.times[i])
    
    

class RequestCollection(object):
  def __init__(self):
    self.entries = {}
    self.time_map = {}

  def add(self, name, t_response):
    entry = self.entries.get(name, None)
    if entry is None:
      self.entries[name] = RequestEntry(name)
      entry = self.entries[name]
    entry.add(t_response)
    if not self.time_map.has_key(t_response):
      self.time_map[t_response] = 1
    else:
      self.time_map[t_response] += 1
  
  def calculate(self):
    for v in self.entries.values():
      v.calculate()
    
  
  def get_duplicated_time(self):
    t=[(k,v) for k,v in self.time_map.items() if v > 1]
    return t
        

def main():
  print "Performance Log Viewer"
  data = RequestCollection()

  #read log
  subdir = 'log'
  fs = [ f for f in os.listdir(subdir) if "roach" in f]
  most_recent = 0
  most_recent_file = None
  for f in fs:
    filename = os.path.join(subdir, f)
    if os.path.exists(filename):
      t = os.path.getmtime(filename)
      if t>most_recent:
        most_recent = t
        most_recent_file = filename
  if most_recent_file is None:
    print "No performance log file"
    sys.exit(1)
  print "Loading Log '%s'"%most_recent_file
  f = file(most_recent_file, "r")
  items = []
  while True:
    line = f.readline()
    if len(line) == 0: 
      #EOF
      break
    item = line.split()
    data.add(item[0], float(item[3]))

  #calculate
  data.calculate()
  result = []
  for k, entry in data.entries.items():
    result_item = [entry.name, str(entry.count)]
    result_item = result_item + map(lambda x:"%.3f"%x, entry.quantile)
    result.append(result_item)

  #output
  print
  print "[Respose Time]"
  print "request\t\tcount\t" + "\t".join(map(lambda x:"%.0f"%(x*100)+"%",QUANTILE))
  for r in result:
    print "\t".join(r)
  
  print
  print "[Duplication Check]"
  t = data.get_duplicated_time()
  if not t:
    print "OK."
  else:
    print "response","\t","times"
    for i,j in t:
      print i,"\t\t",j
 

if __name__ == "__main__":
  main()
  print
  raw_input("Press enter to exit...")
