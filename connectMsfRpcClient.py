#!/usr/bin/env python3
#Credit goes to Luis Hebendanz
#https://github.com/Luis-Hebendanz/msf-remote-console

from pymetasploit3.msfrpc import MsfRpcClient
from pymetasploit3.msfrpc import MsfRpcError
from ssl import SSLError
import socket

#
class connectMsfRpcClient:

    def __init__(self, username, password, port, host, ssl):
        self.username = username
        self.password = password
        self.port = port
        self.host = host
        self.ssl = ssl

    # Connect to the msfrpcd server
    def connect(self):
        print ("[*] Connecting to server:\n Host => %s,\n Port => %s,\n User => %s,\n " \
              "Pwd => %s,\n SSL => %s\n" % (self.host, self.port, self.username, '*' * len(self.password), self.ssl))
        # Login to msfrpcd server
        try:
            kwargs = {'username': self.username, 'port': self.port, 'server': self.host, 'ssl': self.ssl}
            self.client = MsfRpcClient(self.password, **kwargs)
            print ("[+] Successfully connected")
        except SSLError as msg:
            print ("[-] SSL error: " + str(msg))
            print ("[-] You probably have installed the wrong pymetasploit version try installing it from here: https://github.com/allfro/pymetasploit.git")
            return False
        except socket.error as msg:
            print ("[-] Couldn't connect to server: " + str(msg))
            return False
        except MsfRpcError:
            print ("[-] Login failed. Wrong username or password")
            return False
        self.console = self.client.consoles.console()
        self.console_id = self.console.cid
        print ("[*] Console ID: " + self.console_id)