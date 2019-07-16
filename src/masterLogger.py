#!/usr/bin/env python3
import logging
import pathlib
import os

def masterLogger(log_dir, log_file, name):
    try:
        _log_file = pathlib.Path(log_file)
        _log_dir = pathlib.Path(log_dir)
        if _log_dir.exists() == False:
            os.mkdir(log_dir)
        if _log_file.exists() == False:
            with open(log_file, 'a') as fp:
                fp.write("CREATING NEW LOG FILE")
                fp.close()

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        fmtstr = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(fmtstr)
        logger.addHandler(file_handler)
        logger.propagate = False
        return logger
    except Exception as msg:
        print(msg)