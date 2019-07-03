#!/usr/bin/env python3

import os
import time
import psutil
import signal
import sys
import threading
from threading import Thread
import logging
import pathlib
from masterLogger import masterLogger
logger = masterLogger('logs', 'logs/handler.log', __name__)

class msfrpcdHandler:
    
    def __init__(self):
        self.msfrpcdStart()
        _isAliveThread = Thread(target=self.msfrpcdIsAlive)
        _isAliveThread.setName("_isAliveThread")
        _isAliveThread.daemon = True
        _isAliveThread.start()

    def msfrpcdStart(self):
        if self.checkMsfrpcd():
            print("[!]MetasploitRPCD is already running!")
        else:
            os.system(f"gnome-terminal -- bash -c \"sudo msfrpcd -P 'password' -S -f -n -a 127.0.0.1; exec bash\"")
            logger.info("Terminal Started and executed handler")
            # os.system("sudo msfrpcd -P 'password' -n -a 127.0.0.1")
            time.sleep(10)
            if self.checkMsfrpcd():
                print("[!]Started MetasploitRPCD")
                logger.info("Started initial MRPCD")
            else:
                print("[!!]Not started. Please try again...")
                logger.warning("Did not run and system exited")
                sys.exit()
    
    def msfrpcdIsAlive(self):
        thread_going = True
        while thread_going:
            try:
                if self.checkMsfrpcd():
                    logger.info("MSFRPCD Still Active")
                else:
                    self.shutdownMsfrpcd()
                    self.msfrpcdStart()
                time.sleep(10)
            except KeyboardInterrupt:
                print("Inerrupted! Shutting down msfrpcd...")
                self.shutdownMsfrpcd()

    def checkMsfrpcd(self):
        for s in psutil.net_connections():
            if s.laddr[1] == 55553:
                return True

    def shutdownMsfrpcd(self):
        for s in psutil.net_connections():
                    if s.laddr[1] == 55553:
                        #os.kill(s.pid, signal.SIGKILL)
                        os.system(f"gnome-terminal -e 'bash -c \"sudo fuser -k 55553/tcp ; exec bash\"'")
                        print('[!]Old MSFRPCD process destroyed.')
                        logger.info("Old MSFRPCD process was destroyed")