#SETUP LOGGING
import logging
from pythonjsonlogger import jsonlogger

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)

def process_event_msg(event):
    """process sns"""

    LOG.info(f"Recieved event {event}")
    message = event['Records'][0]['Sns']["Message"]
    LOG.info(f"Received paylod: MESSAGE {message}")
    return message

def lambda_handler(event, context):
    """Entry point for lambda"""

    LOG.info(f"context {context} and event {event}")
    process_event_msg(event)   
    return True