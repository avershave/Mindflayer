#!/usr/bin/env python3
#Credit goes to Luis Hebendanz
#https://github.com/Luis-Hebendanz/msf-remote-console

try:
    import time
    import sys
except ImportError as msg:
    print ("[-] Library not installed: " + str(msg))
    print ("[*] Try installing it with: pip install " + str(msg.msg))
    sys.exit()

try:
    from pymetasploit3.msfrpc import MsfRpcError, MsfRpcClient
    from pymetasploit3.msfconsole import MsfRpcConsole
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
            useDefaults = input("[DEFAULTS] Would you like to use the all defaults? y/n: ").upper()
            if useDefaults == 'Y':
                self.username = 'msf'
                self.password = 'msf'
                self.port = 55553
                self.host = "127.0.0.1"
                self.ssl = True
            elif useDefaults == 'N':
                print ('Press enter for individual defaults')
                self.username = input('[Set Username] Please enter the username: ')
                if self.username == '':
                    print ('[Set Username] Using default username: msf')
                    self.username = 'msf'
                self.password = input('[Set Password] Please enter the password: ')
                if self.password == '':
                    self.emptyPasswordChoice == input('[Set Password] Would you like to set an empty password? y/n: ').upper()
                    if self.emptyPasswordChoice == 'Y':
                        self.password = ''
                    elif self.emptyPasswordChoice == 'N':
                        print ('[Set Password] Using default password: msf')
                        self.password = 'msf'
                self.port = input('[Set Port] Please enter the port: ')
                if self.port == '':
                    print('[Set Port] Using default port: 55553')
                    self.port = 55553
                else:
                    self.port = int(self.port)
                self.host = input('[Set Host] Please select the host: ')
                if self.host == '':
                    print ('[Set Host] Using default host: 127.0.0.1')
                    self.host = '127.0.0.1'
                setSSL = input('[Set SSL] Using ssl? t/F: ').upper()
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
        
        self.mainMenu()

    def execteSimpleExploit(self):
        # Testing sending commands to console to run
        # THIS WORKS FOR EXPLOITS but needs EXE to run
        print ("USING EXPLOIT")
        exploit = input("Please enter exploit: ")
        self.msfclient.console.write('use ' + exploit)
        time.sleep(2)
        print ("SET PAYLOAD")
        payload = input("Please enter payload: ")
        self.msfclient.console.write('set payload ' + payload)
        time.sleep(2)
        print("SET LHOST")
        host = str(input("Please enter LHOST: "))
        self.msfclient.console.write('set LHOST ' + host)
        time.sleep(2)
        print("SET LPORT")
        port = str(input("Please enter LPORT: "))
        self.msfclient.console.write('set LPORT ' + port)
        time.sleep(2)
        print("SET THREAD")
        thread = str(input("Please enter number of threads: "))
        self.msfclient.console.write('set THREADS ' + thread)
        time.sleep(2)
        print("RUNNING")
        self.msfclient.console.write('run')
        time.sleep(10)
    
    def printSessions(self):
        # Only works if you load msgrpc with the correct parameters using the framework
        # Params: Pass=password, default port is 55552
        self.sessions = self.msfclient.client.sessions.list
        for s_id, s_info in self.sessions.items():
            print("\nSession ID: ", s_id)  
            for key in s_info:
                print(key + ':', s_info[key])

    def mainMenu(self):
        '''MainMenu'''
        menuGoing = False
        print("[+] Console Running and Connected!\n")
        print("[!] Entering Main Menu\n")
        while menuGoing == False:
            print("\n[***]Main Menu[***]\n")
            print("1.) Start Exploit and Payload")
            print("2.) Print Current Session")
            print("press 0 to exit...")
            selection = int(input("[!] Please select an option: "))
            if selection == 1:
                self.execteSimpleExploit()
            if selection == 2:
                self.printSessions()
            if selection == 0:
                print("[!!] Exiting...")
                self.msfclient.console.destroy()
                return True

# Execute Main
try:
    pyRon()
except KeyboardInterrupt:
    print ("[*] Interrpted execution")
    exit(0)