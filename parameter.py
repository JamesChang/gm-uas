# -*- encoding: utf-8 -*-
from optparse import OptionParser

OPT = OptionParser(usage = "usage: %prog [options] arg...")


def get():
    options()
    (paradict, paralist) = OPT.parse_args()
    return paradict
        
def options():
    OPT.add_option('-u', '--users', 
                        default = 'user101-300', 
                        metavar = 'USERRULE', 
                        help = 'set testing users[default:%default]', 
                        dest = 'userrule'
                        )
    OPT.add_option('-p', '--password', 
                        default = 'a', 
                        metavar = 'PASSWORDRULE', 
                        help = 'set testing password[default:%default]', 
                        dest = 'psdrule'
                        )