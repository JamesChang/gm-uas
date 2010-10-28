Gamemate User Simulator

Prerequirements
==================

1) Stackless Python 2.6 or newer.  

2) Google's Protobuffer 2.1.0.


Usage
=====

  1) edit settings.py, modify MSG_SVR and ARENA_SVR
  2) python main.py
  
MODULES
=========

  --protobuf              生成protobuffer文件
  main.py                 启动脚本
  context.py              维护一个全局可引用的对象空间
  scheduler.py            延迟调度服务
  stacklesssocket.py      用于stackless的socket，替换了python的原生socket。内部依赖于asyncore。
  settings.py             配置文件
  user.py                 用户行为模型
  ez_setup.py             setuptools的下载文件
  setup.py                setuptools的安装文件
  
