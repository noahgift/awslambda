"""
Dynamo to SQS
"""

import boto3
import json

DYNAMODB = boto3.resource("dynamodb")
TABLE = "fang"
QUEUE = "producer"
SQS = boto3.client("sqs")

# SETUP LOGGING
import logging
from pythonjsonlogger import jsonlogger

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
LOG.addHandler(logHandler)


def scan_table(table):
    """Scans table and return results"""

    LOG.info(f"Scanning Table {table}")
    producer_table = DYNAMODB.Table(table)
    response = producer_table.scan()
    items = response["Items"]
    LOG.info(f"Found {len(items)} Items")
    return items


def send_sqs_msg(msg, queue_name, delay=0):
    """Send SQS Message

    Expects an SQS queue_name and msg in a dictionary format.
    Returns a response dictionary.
    """

    queue_url = SQS.get_queue_url(QueueName=queue_name)["QueueUrl"]
    queue_send_log_msg = "Send message to queue url: %s, with body: %s" % (
        queue_url,
        msg,
    )
    LOG.info(queue_send_log_msg)
    json_msg = json.dumps(msg)
    response = SQS.send_message(
        QueueUrl=queue_url, MessageBody=json_msg, DelaySeconds=delay
    )
    queue_send_log_msg_resp = "Message Response: %s for queue url: %s" % (
        response,
        queue_url,
    )
    LOG.info(queue_send_log_msg_resp)
    return response


def send_emissions(table, queue_name):
    """Send Emissions"""

    items = scan_table(table=table)
    for item in items:
        LOG.info(f"Sending item {item} to queue: {queue_name}")
        response = send_sqs_msg(item, queue_name=queue_name)
        LOG.debug(response)


def lambda_handler(event, context):
    """
    Lambda entrypoint
    """

    extra_logging = {"table": TABLE, "queue": QUEUE}
    LOG.info(f"event {event}, context {context}", extra=extra_logging)
    send_emissions(table=TABLE, queue_name=QUEUE)
