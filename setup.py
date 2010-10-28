# -*- encoding: utf-8 -*-
import datetime
import sys
if sys.version_info < (2, 5) or sys.version_info >=(3,0):
    print >> sys.stderr, 'error: python 2.5 or higher is required, you are using %s' %'.'.join(
        str(i) for i in sys.version_info)
    sys.exit(1)
    
import ez_setup
ez_setup.use_setuptools()

#def _get_version():
    #m_time=datetime.datetime.now()-datetime.datetime(2008,12,24)
    #return m_time.seconds/60+m_time.days*60
    #return 200
    
from setuptools import setup, find_packages

setup(
    name='GameMate',
    version = '1.5.0',
    description = 'GameMate',
    author = 'Shanghai GameMate Information Techology Co., Ltd.',
    author_email = 'master.gamemate@gmail.com',
    url = 'http://www.gamemate.cn',
    packages=['gm',
                'gm.web',
                    'gm.web.account',
                        #'gm.fixtures',
                        #'gm.tests',
                    'gm.web.business',
                        #'gm.fixtures',
                    'gm.web.log',                    
                    'gm.web.message',
                    'gm.web.session',
                    'gm.web.test',
                    'gm.web.util',
                    'gm.web.view',
                        'gm.web.view.base',
    ],
    include_package_data = True,
    install_requires=['demjson','config','sqlalchemy==0.5.8','flup', 'collective.ordereddict'], 
    #这些软件无法通过easy_install安装：mod-python??,mysql-python #pil pymssql, django
    #这些软件是可选的lxml, flup
    #django debug toolbar, 
    
    )
    
    
