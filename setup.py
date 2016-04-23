# -*- coding: utf-8 -*-
import urllib
import re
import os
import platform
import sys
import platform
import stat
# from distutils.core import setup
from setuptools import setup
try:
    import py2exe
    use_py2exe = True
except ImportError:
    use_py2exe = False

if use_py2exe:
    # This is an temporary workaround to deal with importing errors using py2exe.
    if "py2exe" in sys.argv:
        sys.path.append("./mobile_insight")
        sys.path.append("./win_dep")

PY2EXE_OPTIONS = {
    "bundle_files": 1,      # 1: bundle everything
}


def parse_libs(url,suffix):
    pattern = '<a href=".*%s.*">.*</a>' % suffix
    response = urllib.urlopen(url).read()
    res = []
    for item in re.findall(pattern, response):
        lib_start = item.find('href="')
        lib_end = item.find('">')
        lib_name = item[lib_start+6:lib_end]
        res.append(lib_name)
    return res

def download_libs(url,libs,chmod=True):
    for lib in libs:
        if not os.path.isfile("./libs/"+lib):
            urllib.urlretrieve (url+lib, "./libs/"+lib)
    if chmod:   
        for lib in libs: 
            os.chmod("./libs/"+lib,0o755 | stat.S_IEXEC)

def download_unix(url):
    if not os.path.isfile("./ws_dissector/ws_dissector"):
        urllib.urlretrieve (url+"ws_dissector", "./ws_dissector/ws_dissector")
    if not os.path.isfile("./mobile_insight/monitor/dm_collector/dm_collector_c.so"):
        urllib.urlretrieve (url+"dm_collector_c.so", "./mobile_insight/monitor/dm_collector/dm_collector_c.so")
    #os.chmod("./ws_dissector/ws_dissector",0o755 | stat.S_IEXEC)
    #os.chmod("./mobile_insight/monitor/dm_collector/dm_collector_c.so",0o755 | stat.S_IEXEC)

def download_win(url):
    if not os.path.isfile("./ws_dissector/ws_dissector.exe"):
            urllib.urlretrieve (url+"ws_dissector.exe", "./ws_dissector/ws_dissector.exe")
    if not os.path.isfile("./mobile_insight/monitor/dm_collector/dm_collector_c.pyd"):
        urllib.urlretrieve (url+"dm_collector_c.pyd", "./mobile_insight/monitor/dm_collector/dm_collector_c.pyd")

#Download libraries
if not os.path.exists("./libs"):
    os.makedirs("./libs")
if not os.path.exists("./ws_dissector"):
    os.makedirs("./ws_dissector")

print "Downloading libraries..."

if platform.system()=="Darwin":
    
    arch=platform.architecture()
    if arch[0]!='64bit':
        print "Unsupported operating system: "+str(arch)
        sys.exit()

    url = "http://metro.cs.ucla.edu/mobile_insight/libs/osx/libs/"
    libs = parse_libs(url,"dylib")
    download_libs(url,libs)
    download_unix(url)

    PACKAGE_DATA = {'mobile_insight.monitor.dm_collector': ['./dm_collector_c.so']}
    lib_list = ["./libs/"+x for x in os.listdir("./libs/")]
    DATA_FILES = [(sys.exec_prefix+'/mobile_insight/ws_dissector/',['ws_dissector/ws_dissector']),]
                 # ('/usr/lib/',lib_list)]

elif platform.system()=="Linux":

    arch=platform.architecture()
    if arch[0]=='32bit':
        url="http://metro.cs.ucla.edu/mobile_insight/libs/linux-32/libs/"
    elif arch[0]=='64bit':
        url="http://metro.cs.ucla.edu/mobile_insight/libs/linux-64/libs/"
    else:
        print "Unsupported operating system: "+str(arch)
        sys.exit()

    libs = parse_libs(url,"so")
    #download_libs(url,libs)
    #download_unix(url)

    PACKAGE_DATA = {'mobile_insight.monitor.dm_collector': ['./dm_collector_c.so']}
    lib_list = ["./libs/"+x for x in os.listdir("./libs/")]
    DATA_FILES = [("/usr/local/bin/",['ws_dissector/ws_dissector']),
                  ('/usr/lib/',lib_list)]

elif platform.system() == "Windows":
    arch=platform.architecture()
    if arch[0]=='32bit':
        url="http://metro.cs.ucla.edu/mobile_insight/libs/win-32/libs/"
    elif arch[0]=='64bit':
        # url="http://metro.cs.ucla.edu/mobile_insight/libs/win-64/libs/"
        url="http://metro.cs.ucla.edu/mobile_insight/libs/win-32/libs/"
    else:
        print "Unsupported operating system: "+str(arch)
        sys.exit()

    libs = parse_libs(url,"dll")
    download_libs(url,libs,False)
    download_win(url)

    PACKAGE_DATA = {'mobile_insight.monitor.dm_collector': ['./dm_collector_c.pyd']}
    ws_files = ['ws_dissector/ws_dissector.exe']
    # include all dlls
    for root, dirs, files in os.walk('ws_dissector'):
        ws_files.extend(['ws_dissector/' + name for name in files if name.endswith('.dll')])

    lib_list = ["./libs/"+x for x in os.listdir("./libs/")]
    DATA_FILES = [(sys.exec_prefix+'/mobile_insight/ws_dissector',ws_files),
                  (sys.exec_prefix+'/mobile_insight/ws_dissector',lib_list)]
else:
    print "Unsupported operating system: "+str(arch)
    sys.exit()

setup(
    name = 'MobileInsight',
    version = '2.0',
    description = 'Mobile network monitoring and analysis',
    author = 'UCLA WiNG Group and OSU MSSN lab',
    author_email = 'yuanjie.li@cs.ucla.edu, zyuan@cs.ucla.edu',
    url = 'http://metro.cs.ucla.edu/mobile_insight',
    license = 'Apache License 2.0',
    packages = ['mobile_insight',
                'mobile_insight.analyzer',
                'mobile_insight.monitor',
                'mobile_insight.monitor.dm_collector',
                'mobile_insight.monitor.dm_collector.dm_endec',
                ],
    install_requires=[
          'pyserial',
          'crcmod',
          'xmltodict',
      ],
    package_data = PACKAGE_DATA,
    data_files = DATA_FILES,
    options = { 'py2exe' : PY2EXE_OPTIONS },
)
