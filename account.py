# -*- encoding: utf-8 -*-
from re import sub,findall

USERS = {'account' : 't*', 
         'passwd' : 'a', 
         'area' : [1,100],
         }
    
class Account(object):
    def parse(self, sacco, spass):
        dlist=[]
        daccolist = self.myrule(sacco)
        dpasslist = self.myrule(spass)
        for daccono in range(len(daccolist)):
            dacco = daccolist[daccono]
            if daccono < len(dpasslist):
                dpass = dpasslist[daccono]
            dlist.append([dacco, dpass])
        return dlist
    
    def myrule(self, pstr):
        dlist = []
        plist = pstr.split(',')
        for para in plist:
            area = findall('\D*(\d*)-(\d*)\D*', para)
            if area:
                area = list(area[0])
                if not area[0]:
                    area[0] = 0
                else:
                    area[0] = int(area[0])
                if not area[1]:
                    area[1] = 0
                else:
                    area[1] = int(area[1])
                sint = min(area)
                eint = max(area)+1
                for no in range(sint,eint):
                    parsed = sub('\d*-\d*', str(no), para)
                    dlist.append(parsed)
            else:
                dlist = [para]
        return dlist
        
            
            
            
            
            
            
            
            
            
            