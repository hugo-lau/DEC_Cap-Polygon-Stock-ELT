from polygon import WebSocketClient
from polygon.websocket.models import WebSocketMessage, EquityTrade
from confluent_kafka import Producer
from typing import List
import os
import pandas as pd
import logging
import json
import sys
import threading
import time
import signal
import boto3
from botocore.exceptions import ClientError
import io


def get_subscriptions_from_s3(bucket: str, key: str) -> List[str]:
    """
    Fetch subscriptions CSV file from S3 and parse it
    """
    try:
        logger.info(f"Fetching subscriptions from S3 bucket: {bucket}, key: {key}")
        s3_client = boto3.client("s3")
        response = s3_client.get_object(Bucket=bucket, Key=key)

        # Read CSV content from S3
        csv_content = response["Body"].read().decode("utf-8")
        df = pd.read_csv(io.StringIO(csv_content))
        data = df.values.tolist()
        subscriptions = [item for sublist in data for item in sublist]

        logger.info(f"Successfully loaded {len(subscriptions)} subscriptions")
        return subscriptions
    except ClientError as e:
        logger.error(f"Error fetching from S3: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing subscriptions file: {e}")
        raise


def delivery_callback(err, msg):
    if err:
        sys.stderr.write("%% Message failed delivery: %s\n" % err)
    else:
        sys.stderr.write(
            "%% Message delivered to %s [%d] @ %d\n"
            % (msg.topic(), msg.partition(), msg.offset())
        )


def handle_msg(msg: List[WebSocketMessage]):
    for m in msg:
        item = {
            "event_type": m.event_type,
            "symbol": m.symbol,
            "volume": m.volume,
            "accumulated_volume": m.accumulated_volume,
            "official_open_price": m.official_open_price,
            "vwap": m.vwap,
            "open_price": m.open,
            "close_price": m.close,
            "high": m.high,
            "low": m.low,
            "aggregate_vwap": m.aggregate_vwap,
            "average_size": m.average_size,
            "start_timestamp": m.start_timestamp,
            "end_timestamp": m.end_timestamp,
            "otc": m.otc,
        }
        producer.produce(
            topic=os.environ.get("CONFLUENT_TOPIC"),
            key=json.dumps({"symbol": m.symbol}).encode("utf-8"),
            value=json.dumps(item).encode("utf-8"),
            callback=delivery_callback,
        )
        producer.poll(0)
    producer.flush()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Verify environment variables are loaded
    required_env_vars = [
        "KAFKA_BOOTSTRAP_SERVERS",
        "KAFKA_SASL_USERNAME",
        "KAFKA_SASL_PASSWORD",
        "CONFLUENT_TOPIC",
        "api_key",
        "S3_BUCKET",
        "S3_KEY",
    ]

    missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    # Configure Kafka producer using environment variables
    producer_config = {
        "bootstrap.servers": os.environ.get("KAFKA_BOOTSTRAP_SERVERS"),
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": os.environ.get("KAFKA_SASL_USERNAME"),
        "sasl.password": os.environ.get("KAFKA_SASL_PASSWORD"),
        "session.timeout.ms": "45000",
    }

    producer = Producer(producer_config)

    try:
        # Duration from environment variable or default
        duration = int(
            os.environ.get("WEBSOCKET_DURATION_SECONDS", 420)
        )  # default 7 minutes

        logger.info(f"Starting WebSocket connection for {duration/60:.1f} minutes...")

        # Fetch subscriptions from S3
        subscriptions = get_subscriptions_from_s3(
            bucket=os.environ.get("S3_BUCKET"), key=os.environ.get("S3_KEY")
        )

        ws = WebSocketClient(
            api_key=os.environ.get("api_key"),
            feed="delayed.polygon.io",
            market="stocks",
            subscriptions=subscriptions,
            verbose=True,
        )

        # Set up signal handler for graceful shutdown
        def signal_handler(signum, frame):
            logger.info("Signal received, shutting down...")
            producer.flush()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start timer for duration
        def stop_after_duration():
            time.sleep(duration)
            logger.info(f"Duration {duration/60:.1f} minutes reached, shutting down...")
            os.kill(os.getpid(), signal.SIGTERM)

        timer_thread = threading.Thread(target=stop_after_duration)
        timer_thread.daemon = True
        timer_thread.start()

        ws.run(handle_msg=handle_msg)

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        producer.flush()
        sys.exit(1)
