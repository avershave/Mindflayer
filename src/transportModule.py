#!/usr/bin/env python3
import json
from masterLogger import masterLogger

class transportModule():
    '''
    Transport Module
    This will handle transport function within meterpreter
    '''
    commands = []
    def __init__(self, sessionID, msfclient):
        self.sessionID = sessionID
        self.msfclient = msfclient
        self.text_parse()

    def printTransportList(self):
        transport_dict = self.retrieveTransport()
        for t_id, t_info in transport_dict.items():
            print(f"\nTransport ID: {t_id}")
            for k,v in t_info.items():
                print(f"{k}: {v}")

    def retrieveTransport(self):
        '''
        Retrieve transport from json file
        '''
        json_file = open('json/transportJSON.json')
        json_read = json_file.read()
        transportFromJson = json.loads(json_read)
        return transportFromJson

    def text_parse(self):
        transport_str = self.msfclient.client.sessions.session(self.sessionID).run_with_output('transport list')
        transport_list = []
        transport_dict = {}
        for fd in transport_str.splitlines():
            fd = fd.replace('\n', '')
            if fd == '':
                pass
            elif 'Session' in fd:
                pass
            elif any(char.isdigit() for char in fd):
                transport_list.append(fd)
            if transport_list:
                for t in transport_list:
                    transport_info = t.split()
                    if not '*' in transport_info:
                        transport_info.insert(1, '-')
                    transport_dict[transport_info[0]] = {}
                    transport_dict[transport_info[0]]['Current'] = transport_info[1]
                    transport_dict[transport_info[0]]['URI'] = transport_info[2]
                transport_json = json.dumps(transport_dict, indent=4)
                with open("json/transportJSON.json", 'w') as fp:
                    fp.write(transport_json)
                    fp.close()

    def transportAdd(self, payload, lhost, lport):
        transport_add = self.msfclient.client.sessions.session(self.sessionID).run_with_output(f'transport add -t {payload} -l {lhost} -p {lport}')
        print("\n", transport_add)