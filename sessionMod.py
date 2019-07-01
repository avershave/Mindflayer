#!/usr/bin/env python3
# Takes in a session from mainMenu of pyRon and you are able to send commands to it
# Has it's own menu which can exit into mainMenu just by returning false

import json
import random
import time
from pymetasploit3.msfrpc import MsfError

class sessionMod:

    commands = ['ipconfig', 'whoami']

    def __init__(self, msfclient):
        self.msfclient = msfclient
        self.dumpSession()
    
    def dumpSession(self):
        '''
        Dump current session into a json file
        '''
        with open('json/sessionJSON.json', 'w') as fp:
            json.dump(self.msfclient.client.sessions.list, fp, indent=4)
    
    def retrieveSession(self):
        '''
        Retrieve session from json file
        '''
        json_file = open('json/sessionJSON.json')
        json_read = json_file.read()
        sessionFromJson = json.loads(json_read)
        return sessionFromJson
        
    def sessionPrint(self):
        '''
        Prints session by parsing the json file
        '''
        self.dumpSession()
        currentSession = self.retrieveSession()
        for s_id, s_info in currentSession.items():
            print("\nSession ID: ", s_id)
            for info in s_info:
                print(info + ':', s_info[info])
    

    def sessionMenu(self):
        '''
        sessionModule
        1 will print session
        2 will send the command to session
        '''
        menuGoing = False
        print("\n[!]Entering Session Module")
        while menuGoing == False:
            print("\n[***]Session Module[***]\n")
            print("1.) Print Current Sessions")
            print("2.) Send Command to Session")
            print("3.) Start active session controller")
            print("4.) Test Command")
            print("press 0 to exit...")
            selection = int(input("[!] Please select an option: "))
            if selection == 1:
                self.sessionPrint()
            if selection == 2:
                self.sessionSendCommand()
            if selection == 3:
                self.activeSessionController()
            if selection == 4:
                self.msfclient.client.sessions.session('1').run_wit_output('transport list')
            if selection == 0:
                return True
    
    def sessionSendCommand(self):
        '''
        Sends a command to a session.
        Currently just sends a random powershell command and returns the output.
        TODO:
        Want to send more than just powershell commands.
        Can select what kind of command to send.
        '''
        sessionList = []
        self.dumpSession()
        dumpedSesssion = self.retrieveSession()
        for s_id in dumpedSesssion:
            sessionList.append(s_id)
        for avail in sessionList:
            print(f"[+]Session {avail} ready!")
        sessionInput = input("[!]Which session: ")
        print(f'[+]Selected session {sessionInput}')
        print(self.msfclient.client.sessions.session(sessionInput).run_psh_cmd(random.choice(self.commands)))

    def activeSessionController(self):
        '''
        Loops through sending commands to random sessions that are available through dumping and reading the json file.
        TODO:
        Adding a way to better handle dying connections.
        '''
        g = True
        while g == True:
            try:
                sessionList = []
                self.dumpSession()
                dumpedSesssion = self.retrieveSession()
                for s_id in dumpedSesssion:
                    sessionList.append(s_id)
                while not sessionList:
                    print("\n[!]No sessions. Waiting for sessions...\n")
                    time.sleep(5)
                    self.dumpSession()
                    dumpedSesssion = self.retrieveSession()
                    for s_id in dumpedSesssion:
                        sessionList.append(s_id)
                for avail in sessionList:
                    print(f"[+]Session {avail} ready!")
                selectedSession = random.choice(sessionList)
                print(f'[+]Selected session {selectedSession}')
                _output = self.msfclient.client.sessions.session(selectedSession).run_psh_cmd(random.choice(self.commands), timeout=5, timeout_exception=True)
                check_error = _output.split(" ")
                if check_error[0] == '[-]':
                    print(f"[!]Session {selectedSession} threw timeout error.")
                    print("[!]Killing session...")
                    self.msfclient.client.consoles.console(self.msfclient.console).write(f'sessions -k {selectedSession}')
                    time.sleep(10)
                else:
                    print(_output)
                time.sleep(4)
            except KeyboardInterrupt:
                exit = input("[+]Would you like to exit y/n: ").upper()
                if exit == 'Y':
                    return False
                elif exit == 'N':
                    return True
            except MsfError:
                print(f"[!]Session {selectedSession} threw timeout error.")
                print("[!]Killing session...")
                self.msfclient.client.consoles.console(self.msfclient.console).write(f'sessions -k {selectedSession}')
                time.sleep(10)
                continue