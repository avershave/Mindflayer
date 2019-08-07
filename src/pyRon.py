#!/usr/bin/env python3
#Credit goes to Luis Hebendanz
#https://github.com/Luis-Hebendanz/msf-remote-console



try:
    import time
    import sys
    import logging
    import json
    import pathlib
    import os
except ImportError as msg:
    print ("[-] Library not installed: " + str(msg))
    print ("[*] Try installing it with: pip install " + str(msg.msg))
    sys.exit()

try:
    from pymetasploit3.msfrpc import MsfRpcError, MsfRpcClient
    from pymetasploit3.msfconsole import MsfRpcConsole
except ImportError as msg:
    print(msg)
    print ("[-] Missing library pymetasploit")
    print ("[*] Please clone from \"git clone https://github.com/DanMcInerney/pymetasploit3.git\"")
    print ("[*] \"cd pymetasploit3 && sudo python setup.py install\"")
    sys.exit()
try:
    from connectMsfRpcClient import connectMsfRpcClient
    from sessionMod import sessionMod
    from msfrpcdHandler import msfrpcdHandler
    from msfAutomation import msfAutomation
    from masterLogger import masterLogger
    logger = masterLogger('logs', 'logs/main.log', __name__)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
    import data.data_services as svc
    from mongo_setup import global_init
except ImportError as msg:
    print(msg)
    sys.exit()

class pyRon:
    # starting mongo
    global_init()
    # clearing sessions for new sessions
    svc.deleteSessions()
    # Conditonals
    setSSL = ''

    # Object
    msfclient = None

    meta = {
        'db_alias': 'core',
        'collections': 'sessions'
    }

    def __init__(self):
        '''
        Init for pyRon.
        Sets up the client and session module.
        Enter for defaults.
        Puts you into mainMenu.
        Automation added to make the setup straight forward.
        '''
        dir_path = os.path.dirname(os.path.realpath(__file__))
        json_path = dir_path+'/json'
        if not os.path.isdir(json_path):
            os.mkdir(json_path)
        with open(json_path+'/jobsJSON.json'): pass
        with open(json_path+'/sessionJSON.json'): pass
        with open(json_path+'/transportJSON.json'): pass

        # Adding Customization OR using defaults
        try:
            automation = input("[!]Start automation or manual y/n: ").upper()
            if automation == 'Y':
                logger.info("Started Automation")
                self.msfclient = connectMsfRpcClient('msf', 'password', '55553', '127.0.0.1', 'False')
                msfAutomation(self.msfclient)
                self.Exit()
            if automation == 'N':
                logger.info("Starting client setup")
                msfrpcdHandler()
                useDefaults = input("[DEFAULTS] Would you like to use the all defaults? y/n: ").upper()
                if useDefaults == 'Y':
                    self.username = 'msf'
                    self.password = 'password'
                    self.port = 55553
                    self.host = "127.0.0.1"
                    self.ssl = False
                elif useDefaults == 'N':
                    print ('Press enter for individual defaults')
                    self.username = input('[Set Username] Please enter the username: ')
                    if self.username == '':
                        print ('[Set Username] Using default username: msf')
                        self.username = 'msf'
                    self.password = input('[Set Password] Please enter the password: ')
                    if self.password == '':
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
            logger.info("User put wrong info for client and program is exiting")
            print ('Wrong input!')
            sys.exit()

        # Objects
        logger.info("Connecting to client with info")
        self.msfclient = connectMsfRpcClient(self.username, self.password, self.port, self.host, self.ssl)

        # Connect to msfrpcd
        if self.msfclient.connect() is False:
            logger.info("Client did not connect and program is exiting")
            sys.exit()
        self.sessionMod = sessionMod(self.msfclient)
        logger.info("Entering main menu")
        self.mainMenu()

    def epMenu(self, *args):
        '''
        Checking for required exploit and payload values.
        The user can provide required and edit any other run values.
        Can't run more than two arguments!!!
        '''
        choice = args[0]
        runOptions = choice.options
        if not choice.missing_required:
            print("[!]No required options!")
        else:
            logger.info("Entering required options")
            print("[+]Printing required options...")
            print("[!]Please fill out required options...")
            while choice.missing_required:
                try:
                    for r in choice.missing_required:
                        c = input(f"[!]{r}: ")
                        if '.' in c:
                            pass
                        else:
                            if any(char.isdigit() for char in c):
                                c = int(c)
                        choice[r] = c
                except ValueError as msg:
                    logger.info("Wrong value for required options")
                    print("Value error: " + str(msg))
                    continue
        menu = True
        while menu:
            try:
                logger.info("Entering changing options for exploit and payload")
                g = False
                print("[+]Printing run options...")
                for options in runOptions:
                    print(options)
                uc = input("[!]Do you want to change these values? y/n: ").upper()
                if uc not in ['Y', 'N']:
                    raise ValueError
                while g == False:
                    if uc == 'N':
                        return True
                    elif uc == "Y":
                        sg = False
                        while sg == False:
                            c = input("[!]Which option would you like to change: ")
                            # _isTrue = c in runOptions REMOVE IF IF STATEMENT WORKS
                            if c in runOptions:
                                cv = input("[!]Please enter new value: ")
                                if '.' in cv:
                                    pass
                                else:
                                    if any(char.isdigit() for char in cv):
                                        cv = int(cv)
                                choice[c] = cv
                                for options in runOptions:
                                    print(options)
                            if c == '':
                                uc = input("[!]Done changing values y/n:")
                            uc = input("[!]Do you want to change another value y/n: ").upper()
                            if uc == 'N':
                                return True
                            else:
                                return False
                return False
            except KeyboardInterrupt:
                logger.info('Keyboard interrupt in exploit and payload options')
                print('\n[!!]Exit Exploit and Payload Options')
                break
            except ValueError:
                logger.info("Wrong input in exploit options and payload options. Program exiting.")
                print("Wrong input!")
                continue


    def execteSimpleExploit(self):
        '''
        User inputting exploit and payload
        '''
        menu = True
        exploit = None
        _payload = None
        while menu:
            try:
                if exploit is None:
                    logger.info("Entering choice for exploit")
                    print ("[+]Using Exploit...")
                    exploit = input("[!]Please enter exploit: ")
                    exploit = self.msfclient.client.modules.use('exploit', exploit)
                    self.epMenu(exploit)
                if _payload is None:
                    logger.info("Entering choice for payload")
                    print ("[+]Setting payload...")
                    payload = input("[!]Please enter payload: ")
                    _payload = self.msfclient.client.modules.use('payload', payload)
                    self.epMenu(_payload)
                print("[+]Executing exploit...")
                exploit.execute(payload=_payload)
                time.sleep(10)
                sessions = self.msfclient.client.sessions.list
                if not sessions:
                    print('[!]No sessions connected directly after!')
                    print('[!]Please select option two in main menu to print connected sessions.')
                return False
            except KeyboardInterrupt:
                print('\n[!!]Exit Exploit and Payload Menu')
                break
            except ValueError as msg:
                logging.info("Wrong value entering the exploit or payload file path")
                logging.info(msg)
                print ("\n[!!]Wrong value for exploit! or payload")
                break
            except TypeError:
                logging.info("Wrong value entering the exploit or payload file path")
                print ("\n[!!]Wrong value for exploit or payload!")
                continue
        
    def listJobs(self):
        '''
        Prints currently running jobs.
        '''
        logger.info("Printing job list")
        try:
            self.dumpJobs()
            currentJobs = self.retrieveJobs()
            for s_id, s_info in currentJobs.items():
                print("\nJob ID: ", s_id)
                for info in s_info:
                    print(info + ':', s_info[info])
        except Exception as msg:
            print(msg)
            pass

    def dumpJobs(self):
        '''
        Dumps current jobs into a JSON file in order to read.
        '''
        logger.info("Dumping current jobs. I really need a better name for this.")
        try:
            with open('json/jobsJSON.json', 'w') as fp:
                json.dump(self.msfclient.client.jobs.list, fp, indent=4)
        except Exception as msg:
            print(msg)
            pass

    def retrieveJobs(self):
        logger.info("Retrieving jobs from JSON file")
        '''
        Retrieve session from json file
        '''
        try:
            json_file = open('json/jobsJSON.json', 'r')
            json_read = json_file.read()
            jobsFromJson = json.loads(json_read)
            return jobsFromJson
        except Exception as msg:
            print(msg)
            pass

    def mainMenu(self):
        '''
        MainMenu
        Option 1 will walk through exploit execution
        Option 2 will start session module
        '''
        menuGoing = False
        print("[+]Console Running and Connected!")
        print("\n[!]Entering Main Menu")
        while menuGoing == False:
            try:
                logger.info("Entering menu choice")
                print("\n[***]Main[***]\n")
                print("1.) Start Exploit and Payload")
                print("2.) Enter Session Module")
                print("press 0 to exit...")
                selection = int(input("[!] Please select an option: "))
                if selection == 1:
                    self.execteSimpleExploit()
                if selection == 2:
                    logging.info("Changing over sessionMod")
                    self.sessionMod.sessionMenu()
                if selection == 3:
                    self.listJobs()
                if selection == 0:
                    self.Exit()
                    exit(0)
            except Exception as msg:
                print(msg)
                print('\n[!!]Wrong input. Please select the correct input.')
                continue

    def Exit(self):
        logger.info("User is exiting")
        print("[!!] Exiting...")
        killall = input("[+]Kill all sessions? y/n: ").upper()
        if killall == 'Y':
            logger.info("User killing sessions")
            self.msfclient.client.consoles.console(self.msfclient.console).write('sessions -K')
        jobs = self.retrieveJobs()    
        if jobs:
            killjobs = input("[+]Kill all jobs? y/n: ").upper()
            if killjobs == 'Y':
                logger.info("User killing jobs")
                for k in jobs:
                    self.msfclient.client.jobs.stop(k)
        self.msfclient.client.consoles.destroy(self.msfclient.console)

# Execute Main
try:
    pyRon()
except KeyboardInterrupt:
    print ("[*] Interrpted execution")
    exit(0)