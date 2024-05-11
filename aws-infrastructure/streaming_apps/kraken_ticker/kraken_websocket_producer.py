import asyncio
import websockets
import json
import boto3
import logging
import os
import argparse
import datetime

args = argparse.ArgumentParser()
args.add_argument("--log_level", help="Set log level", default=None)
args.add_argument("--trade_pair", help="Set Trade Pair", default="BTC/USD")
parsed_args = args.parse_args()

def setup_logger(script_name,log_level=None):

    '''
    Default log level is info. Pass log level to set lower.
    '''
    logger = logging.getLogger(script_name)
    if not log_level:
        logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))  
    else:
        logger.setLevel(os.environ.get("LOGLEVEL", log_level))

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Logger Setup")
    return logger

log = setup_logger(f"kraken-websocket{parsed_args.trade_pair}",parsed_args.log_level)
log.info(f"Logging set to: {log.getEffectiveLevel()}")

# Create SQS client
sqs = boto3.client('sqs', region_name='aws region', aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

queue_url = 'sqs url here'

async def connect_to_websocket():
    uri = "wss://ws.kraken.com/v2"

    async with websockets.connect(uri) as websocket:
        # Define the subscription payload
        payload = {
            "method": "subscribe",
            "params": {
                "channel": "ticker",
                "symbol": [f"{parsed_args.trade_pair}"],
            }
        }

        # Send the subscription payload
        await websocket.send(json.dumps(payload))
        log.info("Subscription payload sent.")

        # Listen for incoming messages
        counter = 0
        while True:
            counter+=1
            try:
                message = await websocket.recv()
                log.info(f"Received message: {message}")
                try:
                    j_message = json.loads(message)
                    if j_message["channel"] == "heartbeat":
                        log.debug("only a heartbeat - skipping")
                        continue
                except:
                    continue
                timestamp = datetime.datetime.now().isoformat()
                message = {
                    "timestamp": timestamp,
                    "message": message
                }
                log.debug(f"Pre-upload message: {message}")
                # Send message to SQS queue
                response = sqs.send_message(
                    QueueUrl=queue_url,
                    DelaySeconds=10,
                    MessageBody=(str(message))
                )
                log.info(f"Sent to SQS: {response['MessageId']}")

                # Process the message here
            except websockets.ConnectionClosed:
                log.info("Connection closed, attempting to reconnect...")
                break

async def main():
    while True:
        await connect_to_websocket()
        await asyncio.sleep(2)  # Reconnect after a delay if connection is closed

asyncio.run(main())