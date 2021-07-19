"""Returns logger object that logs messages to a file and the console.
Code to get logger object:
```
import sys
sys.path.insert(0, '/home/jupyter')
import util.log
logger = util.log.get("log_name")
All information sent to logger will be displayed.
All messages prefixed with a time_date stamp of format "%H%M_%Y%m%d".
"""
import datetime
import logging

def get(log_name):
    # Create logger and set format
    logger = logging.getLogger(log_name)
    now = datetime.datetime.now().strftime("%H%M_%Y%m%d")
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # Log to file
    f_handler = logging.FileHandler("log_" + now + "_train.txt")
    f_handler.setFormatter(log_format)
    logger.addHandler(f_handler)
    
    # Log to console
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(log_format)
    logger.addHandler(c_handler)
    logger.setLevel(logging.INFO)
    
    return logger