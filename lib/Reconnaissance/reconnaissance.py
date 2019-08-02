#!/usr/bin/env python3
from data.recon import Recon
from data.recon import ReconFiles
from data.recon import ReconPrograms
from data.session import Session
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
        try:
            session = Session.objects(_id=sessionInput).first()
            ip = msfclient.client.sessions.session(sessionInput).run_psh_cmd("ipconfig /all")
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
        except Exception as msg:
            logger.info(msg)
            print("There was an error!")
            pass

    def gatherCurrentAdmin(self, msfclient, sessionInput):
        try:
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
        except Exception as msg:
            logger.info(msg)
            print("There was an error!")
            pass

    def gatherWhoAmI(self, msfclient, sessionInput):
        try:
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
        except Exception as msg:
            logger.info(msg)
            print("There was an error!")
            pass
    
    def gatherPWD(self, msfclient, sessionInput):
        try:
            current_pwd = msfclient.client.sessions.session(sessionInput).run_with_output('pwd')
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
        except Exception as msg:
            logger.info(msg)
            print("There was an error!")
            pass
    
    def gatherFiles(self, msfclient, sessionInput):
        try:
            desc_files = ['Mode', 'Size', 'Type', 'Last', 'Modified', 'TimeZone', 'Name']
            listofFiles = msfclient.client.sessions.session(sessionInput).run_with_output('ls').splitlines()
            session = Session.objects(_id=sessionInput).first()
            if session:
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
        except Exception as msg:
            logger.info(msg)
            print("There was an error!")
            pass
    
    def gatherInstalledPrograms(self, msfclient, sessionInput):
        program_desc = ['Name', 'Version']
        current_programs = []
        session = Session.objects(_id=sessionInput).first()
        msfclient.client.sessions.session(sessionInput).write('run post/windows/gather/enum_applications', )
        time.sleep(10)
        run_post = msfclient.client.sessions.session(sessionInput).read()
        listofPrograms = run_post.splitlines()
        if session:
            recon = Recon.objects(_id=sessionInput).first()
            if recon is None:
                 recon = Recon()
                 reconprg = ReconPrograms()
                 recon._id = sessionInput
                 recon.session_id = sessionInput
                 session.recon_id.append(recon.session_id)
                 for p in listofPrograms:
                    program = self.parseProgramList(p)
                    if not program:
                        pass
                    else:
                        programs_mapped = dict(zip(program_desc, program))
                        reconprg.installedprograms.append(programs_mapped)
                        reconprg.gathered = True
                        recon.installedprg = reconprg
            elif recon.installedprg.gathered:
                for d in recon.installedprg.installedprograms:
                    current_programs.append(d['Name'])
                for p in listofPrograms:
                    program = self.parseProgramList(p)
                    if not program:
                        pass
                    else:
                        if program[0] not in current_programs:
                            programs_mapped = dict(zip(program_desc, program))
                            recon.installedprg.installedprograms.append(programs_mapped)
        recon.save()
        session.save()
    
    def gatherPID(self, msfclient, sessionInput):
        pid_list = []
        desc_pid = ['PID', 'Name']
        run_ps = msfclient.client.sessions.session(sessionInput).run_with_output('ps')
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
        elif '=====================================' in file[0]:
            pass
        elif '----' in f:
            pass
        elif 'Mode' in file[0]:
            pass
        else:
            return file
    
    def parseIPData(self, recon, ip):
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
    
    def checkingFileChanges(self, file, _dict):
        i = 0
        for k, v in _dict.items():
            if v == file[i]:
                i = i + 1
                pass
            else:
                _dict[k] = file[i]
                i = i + 1