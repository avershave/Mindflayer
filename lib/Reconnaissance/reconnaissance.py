#!/usr/bin/env python3
from data.recon import Recon
from data.session import Session
import re

class Reconnaissance():
    '''
    Main use is to gain info on the session, store it, and use it later.
    @TODO
    make different methods for powershell and cmdshell
    '''

    def gatherNetwork(self, msfclient, sessionInput):
        session = Session.objects(_id=sessionInput).first()
        ip = msfclient.client.sessions.session(sessionInput).run_psh_cmd("ipconfig /all")
        if session:
            recon = Recon.objects(session_id=sessionInput).first()
            if recon:
                for lines in ip.splitlines():
                    if 'IPv4' in lines:
                        found_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                        recon.ip_address = found_ip[0]
                    if 'Default Gateway' in lines:
                        found_gateway = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                        recon.defaultgateway = found_gateway[0]
                    if 'DNS Servers' in lines:
                        found_dns =  re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                        recon.dns = found_dns[0]
                    if 'DHCP Server' in lines:
                        found_dhcp = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                    if 'Subnet Mask' in lines:
                        found_subnet_mask = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
            else:
                recon = Recon()
                recon.session_id = sessionInput
                recon._id = sessionInput
                session.recon_id.append(recon.session_id)
                for lines in ip.splitlines():
                    if 'IPv4' in lines:
                        found_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                        recon.ip_address = found_ip[0]
                    if 'Default Gateway' in lines:
                        found_gateway = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                        recon.defaultgateway = found_gateway[0]
                    if 'DNS Servers' in lines:
                        found_dns =  re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                        recon.dns = found_dns[0]
                    if 'DHCP Server' in lines:
                        found_dhcp = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                    if 'Subnet Mask' in lines:
                        found_subnet_mask = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
        recon.save()
        session.save()

    def gatherCurrentAdmin(self, msfclient, sessionInput):
        admin = msfclient.client.sessions.session(sessionInput).run_psh_cmd("net sessions")
        session = Session.objects(_id=sessionInput).first()
        if session:
            recon = Recon.objects(session_id=sessionInput).first()
            if recon:
                for lines in admin.splitlines():
                    if not 'Access is denied.' in lines:
                        recon.isAdmin = True
                    else:
                        recon.isAdmin = False
            else:
                recon = Recon()
                recon.session_id = sessionInput
                recon._id = sessionInput
                session.recon_id.append(recon.session_id)
                for lines in admin.splitlines():
                    if not 'Access is denied.' in lines:
                        recon.isAdmin = True
                    else:
                        recon.isAdmin = False
        recon.save()
        session.save()

    def gatherWhoAmI(self, msfclient, sessionInput):
        whoami_input = []
        whoami = msfclient.client.sessions.session(sessionInput).run_psh_cmd("whoami")
        session = Session.objects(_id=sessionInput).first()
        if session:
            recon = Recon.objects(session_id=sessionInput).first()
            if recon:
                whoami_input = whoami.splitlines()
                recon.whoami = whoami_input[1]
            else:
                recon = Recon()
                recon.session_id = sessionInput
                recon._id = sessionInput
                session.recon_id.append(recon.session_id)
                for lines in whoami.splitlines():
                    recon.whoami = lines
        recon.save()
        session.save()

