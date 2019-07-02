#!/usr/bin/env python3

class transportModule():
    '''
    Transport Module
    This will handle transport function within meterpreter
    '''
    def __init__(self, sessionID, msfclient):
        self.sessionID = sessionID
        self.msfclient = msfclient

    def printTransportList(self):
        transport_list = self.msfclient.client.sessions.session(self.sessionID).run_with_output('transport list')
        with open('transport-list.txt', 'w') as f:
            f.write(transport_list)
            f.close()
        transport_dict = self.text_parse()
        for t_id, t_info in transport_dict.items():
            print(f"\nTransport ID: {t_id}")
            for k,v in t_info.items():
                print(f"{k}: {v}")

    def text_parse(self):
        transport_list = []
        transport_dict = {}
        with open("transport-list.txt", "r", newline=None) as fd:
            for line in fd:
                line = line.replace('\n', '')
                if line == '':
                    pass
                elif 'Session' in line:
                    pass
                elif any(char.isdigit() for char in line):
                    transport_list.append(line)
            if transport_list:
                for t in transport_list:
                    transport_info = t.split()
                    if not '*' in transport_info:
                        transport_info.insert(1, '-')
                    transport_dict[transport_info[0]] = {}
                    transport_dict[transport_info[0]]['Current'] = transport_info[1]
                    transport_dict[transport_info[0]]['URI'] = transport_info[2]
            return transport_dict

    def transportAdd(self, payload, lhost, lport):
        transport_add = self.msfclient.client.sessions.session(self.sessionID).run_with_output(f'transport add -t {payload} -l {lhost} -p {lport}')
        print("\n", transport_add)