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

    def epMenu(self, *args):
        '''
        Checking for required exploit and payload values.
        The user can provide required and edit any other run values.
        '''
        choice = args[0]
        runOptions = choice.runoptions
        if not choice.missing_required:
            print("[!]No required options!")
        else:
            print("[+]Printing required options...")
            print("[!]Please fill out required options...")
            while choice.missing_required:
                try:
                    for r in choice.missing_required:
                        c = input(r+": ")
                        choice[r] = c
                except ValueError as msg:
                    print("Value error: " + str(msg))
                    continue

        g = False
        print("[+]Printing run options...")
        for options, values in runOptions.items():
            print(options, ":", values)
        uc = input("Do you want to change these values? y/n: ").upper()
        while g == False:
            if uc == 'N':
                return True
            elif uc == "Y":
                sg = False
                while sg == False:
                    c = input("Which option would you like to change: ")
                    # _isTrue = c in runOptions REMOVE IF IF STATEMENT WORKS
                    if c in runOptions:
                        cv = input("Please enter new value: ")
                        if type(runOptions[c]) == bool:
                            cv = bool(cv)
                        if type(runOptions[c]) == (int, float):
                            cv = int(cv)
                        runOptions[c] = cv
                        for options, values in runOptions.items():
                            print(options, ":", values)
                    uc = input("Do you want to change another value: ").upper()
                    if uc == 'N':
                        return True
                    else:
                        return False
                


    def execteSimpleExploit(self):
        # Testing sending commands to console to run
        # THIS WORKS FOR EXPLOITS but needs EXE to run
        print ("[+]Using Exploit...")
        exploit = input("[!]Please enter exploit: ")
        exploit = self.msfclient.client.modules.use('exploit', exploit)
        self.epMenu(exploit)
        print ("[+]Setting payload...")
        payload = input("[!]Please enter payload: ")
        payload = self.msfclient.client.modules.use('payload', payload)
        self.epMenu(payload)
        print("[+]Executing exploit...")
        exploit.execute(payload=payload)
        time.sleep(10)
        sessions = self.msfclient.client.sessions.list
        if not sessions:
            print('[!]No sessions connected directly after!')
            print('[!]Please select option two in main menu to print connected sessions.')
    
    def printSessions(self):
        self.sessions = self.msfclient.client.sessions.list
        for s_id, s_info in self.sessions.items():
            print("\nSession ID: ", s_id)  
            for key in s_info:
                print(key + ':', s_info[key])

    def mainMenu(self):
        '''MainMenu'''
        menuGoing = False
        print("[+]Console Running and Connected!")
        print("\n[!]Entering Main Menu")
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
                killall = input("[+]Kill all sessions? y/n: ").upper()
                if killall == 'Y':
                    self.msfclient.console.write('sessions -K')
                self.msfclient.console.destroy('1')
                return True

# Execute Main
try:
    pyRon()
except KeyboardInterrupt:
    print ("[*] Interrpted execution")
    exit(0)