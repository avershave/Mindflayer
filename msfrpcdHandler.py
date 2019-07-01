#!/usr/bin/env python3

import os, time, psutil, signal, sys
import threading
from threading import Thread
import logging
import pathlib

_log_file = pathlib.Path("logs/handler.log")
_log_dir = pathlib.Path("logs")
if _log_dir.exists() == False:
    os.mkdir("logs")
if _log_file.exists() == False:
    with open('logs/handler.log', 'a') as fp:
        fp.write("CREATING NEW LOG FILE")
        fp.close()

class msfrpcdHandler:
    fmtstr = "%(asctime)s: %(levelname)s: %(message)s"
    logging.basicConfig(filename=_log_file,
                    level=logging.DEBUG,
                    filemode="w",
                    format=fmtstr)
    
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
            os.system(f"gnome-terminal -- bash -c \"msfrpcd -P 'password' -S -f -n -a 127.0.0.1; exec bash\"")
            logging.info("Terminal Started and executed handler")
            # os.system("sudo msfrpcd -P 'password' -n -a 127.0.0.1")
            time.sleep(10)
            if self.checkMsfrpcd():
                print("[!]Started MetasploitRPCD")
                logging.info("Started initial MRPCD")
            else:
                print("[!!]Not started. Please try again...")
                logging.warning("Did not run and system exited")
                sys.exit()
    
    def msfrpcdIsAlive(self):
        thread_going = True
        while thread_going:
            try:
                if self.checkMsfrpcd():
                    logging.info("MSFRPCD Still Active")
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
                        logging.info("Old MSFRPCD process was destroyed")