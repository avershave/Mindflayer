#!/usr/bin/env python3
# Takes in a session from mainMenu of pyRon and you are able to send commands to it
# Has it's own menu which can exit into mainMenu just by returning false

import json
import random

class sessionMod:

    commands = ['ipconfig', 'uuid']

    def __init__(self, client):
        self.client = client
        self.dumpSession()
    
    def dumpSession(self):
        '''
        Dump current session into a json file
        '''
        with open('sessionJSON.json', 'w') as fp:
            json.dump(self.client.client.sessions.list, fp, indent=4)
    
    def retrieveSession(self):
        '''
        Retrieve session from json file
        '''
        json_file = open('sessionJSON.json')
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
            print("press 0 to exit...")
            selection = int(input("[!] Please select an option: "))
            if selection == 1:
                self.sessionPrint()
            if selection == 2:
                self.sessionSendCommand()
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
        print(self.client.client.sessions.session(sessionInput).run_psh_cmd(random.choice(self.commands)))
