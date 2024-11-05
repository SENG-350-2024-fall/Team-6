import time
import logging

# Set up logging for heartbeat
logging.basicConfig(filename='heartbeat.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def heartbeat(interval=10):
    """
    Logs a heartbeat message at regular intervals.
    
    :param interval: Time in seconds between each heartbeat log entry.
    """
    while True:
        logging.info("System is running smoothly")
        time.sleep(interval)
