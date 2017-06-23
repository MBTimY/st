# config:utf-8

import os

APPNAME = 'SoTool'
LISTEN_PORT = '8080'
DEBUG = True
COOKIE_SECRET = 'h1_f/XgBog@<oSw+c>8QQ^U/!Gqt?xDvblX!DozHIf=\
                7G@@_gv8Hhh!sVx0My(4m'
XSRF = True
SPROXY_ADDR = ''
SPROXY_PORT = None
CB_LINKER = "http://sotool.co/translink?r=%s&m=%s"
WORK_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAIN_BASE = ''
MGO_CONN = "mongodb://btso:azlmsxkn!2#@45.32.42.152:27017/btso"
MGO_DB = "btso"
