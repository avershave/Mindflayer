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

    # checking for logs dir
    _log_file = pathlib.Path("logs/main.log")
    _log_dir = pathlib.Path("logs")
    if _log_dir.exists() == False:
        os.mkdir("logs")
    if _log_file.exists() == False:
        with open('logs/main.log', 'a') as fp:
            fp.write("CREATING NEW LOG FILE")
            fp.close()
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fmtstr = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    file_handler = logging.FileHandler("logs/main.log")
    file_handler.setFormatter(fmtstr)
    logger.addHandler(file_handler)

except ImportError as msg:
    print ("[-] Library not installed: " + str(msg))
    print ("[*] Try installing it with: pip install " + str(msg.msg))
    sys.exit()

try:
    from pymetasploit3.msfrpc import MsfRpcError, MsfRpcClient
    from pymetasploit3.msfconsole import MsfRpcConsole
    from connectMsfRpcClient import connectMsfRpcClient
    from sessionMod import sessionMod
    from msfrpcdHandler import msfrpcdHandler
except ImportError as msg:
    print(msg)
    print ("[-] Missing library pymetasploit")
    print ("[*] Please clone from \"git clone https://github.com/DanMcInerney/pymetasploit3.git\"")
    print ("[*] \"cd pymetasploit3 && sudo python setup.py install\"")
    sys.exit()

class pyRon:  
    # Conditonals
    emptyPasswordChoice = ''
    setSSL = ''

    # Object
    msfclient = None

    def __init__(self):
        '''
        Init for pyRon.
        Sets up the client and session module.
        Enter for defaults.
        Puts you into mainMenu.
        Automation added to make the setup straight forward.
        '''
        print("[!]Starting msfrpcd on local host")
        msfrpcdHandler()
        # Adding Customization OR using defaults
        try:
            automation = input("[!]Start automation or manual y/n: ").upper()
            if automation == 'Y':
                logger.info("Started Automation")
                pass
            if automation == 'N':
                logger.info("Starting client setup")
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
        runOptions = choice.runoptions
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
                        choice[r] = c
                except ValueError as msg:
                    logger.info("Wrong value for required options")
                    print("Value error: " + str(msg))
                    continue
        try:
            logger.info("Entering changing options for exploit and payload")
            g = False
            print("[+]Printing run options...")
            for options, values in runOptions.items():
                print(options, ":", values)
            uc = input("[!]Do you want to change these values? y/n: ").upper()
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
                            if type(runOptions[c]) == bool:
                                if cv == 'False':
                                    cv = False
                                else:
                                    cv = True
                            if type(runOptions[c]) == (int, float):
                                cv = int(cv)
                            runOptions[c] = cv
                            for options, values in runOptions.items():
                                print(options, ":", values)
                        if c == '':
                            uc = input("[!]Done changing values y/n:")
                        uc = input("[!]Do you want to change another value y/n: ").upper()
                        if uc == 'N':
                            return True
                        else:
                            return False
        except ValueError:
            logger.info("Wrong input in exploit options and payload options. Program exiting.")
            print("Wrong input!")
            sys.exit()


    def execteSimpleExploit(self):
        '''
        User inputting exploit and payload

        TODO: Change so that the input will loop if wrong input
        '''
        try:
            logger.info("Entering choice for exploit")
            print ("[+]Using Exploit...")
            exploit = input("[!]Please enter exploit: ")
            exploit = self.msfclient.client.modules.use('exploit', exploit)
            self.epMenu(exploit)
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
        except ValueError:
            logging.info("Wrong value entering the exploit or payload file path")
            print ("Wrong value for exploit!")
            sys.exit()
        
    def listJobs(self):
        logger.info("Printing job list")
        try:
            self.dumpJobs()
            currentJobs = self.retrieveJobs()
            for s_id, s_info in currentJobs.items():
                print("\nJob ID: ", s_id)
                for info in s_info:
                    print(info + ':', s_info[info])
        except:
            pass

    def dumpJobs(self):
        logger.info("Dumping current jobs. I really need a better name for this.")
        try:
            with open('json/jobsJSON.json', 'w') as fp:
                json.dump(self.msfclient.client.jobs.list, fp, indent=4)
        except:
            pass

    def retrieveJobs(self):
        logger.info("Retrieving jobs from JSON file")
        '''
        Retrieve session from json file
        '''
        json_file = open('json/jobsJSON.json', 'r')
        json_read = json_file.read()
        jobsFromJson = json.loads(json_read)
        return jobsFromJson

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
            if selection ==3:
                self.listJobs()
            if selection == 0:
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
                return True

# Execute Main
try:
    pyRon()
except KeyboardInterrupt:
    print ("[*] Interrpted execution")
    exit(0)