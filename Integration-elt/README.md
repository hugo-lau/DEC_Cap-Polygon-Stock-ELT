# Integration
Details below along with visual documentation for integrating each pipeline.

# Streaming Pipeline
This real-time streaming pipeline uses the Polygon python library to create a WebSocket client that subscribes to configurable data streams, sending JSON messages every second. The subscriptions are defined in a CSV file stored in an S3 bucket
Given the large volume of real-time financial data, key design decisions include:
- The Polygon WebSocket client is containerized with Docker and deployed on ECS Fargate, enabling scalable compute resources.
- Kafka acts as the message broker, facilitating real-time data flow between the Polygon WebSocket producer and ClickHouse consumer, ensuring scalability and fault tolerance. It also allows for future consumers to be added

Two Kafka topics are used: `polygon_stream_aggregates` for incoming messages and `custom_filtered_stock_data_topic` for pre-processed data. A Kafka ClickHouse sink connector streams this processed data into ClickHouse, which stores it in a MergeTree table optimized for real-time analytics, indexed by timestamp and stock symbol. This architecture supports continuous and scalable data ingestion. 

# Batch Pipeline
For data ingestion, we initially considered using the polygon python library for restful API. However, we opted to build a custom Airbyte connector for the following reasons:
-	Scalability: Airbyte is designed for scalable, automated, and repeatable data ingestion workflows
-	Integration: Airbyte allows seamless integration of multiple data streams. 
-	Centralized orchestration: Leveraging Dagster for managing and orchestrating data pipelines, particularly for batch processing
-	Ease of data replication: Airbyte simplies the process of replicating data from Polygon to Snowflake

The airbyte connector was configured to support incremental data extraction, using the  `last_updated_utc` field. Data collection was structured by date and/stock, ensuring that only the most recent daily data was ingested efficiently. 
Initially, we planned to deploy Airbyte on an EC2 instance. Although Airbyte was successfully installed on a T2.medium instance, we found that the updated version required a T2.large instance. By the time this issue was discovered and resolved, the custom Airbyte connector was already integrated into Airbyte Cloud, and the decision was made to continue with this cloud-based setup for ease of use and scalability.

# Screenshots for Streaming Pipeline
**Policy for S3 Websocket Subscriptions**
![Image](/Docs/IAM_Websocket_Policy.jpg)
**Kafka Incoming Topic from Producer**
![Image](/Docs/ConfluentCloud_Incoming_Topic.jpg)
**Kafka Outgoing Topic for Consumer**
![Image](/Docs/ConfluentCloud_Outgoing_Topic.jpg)
**Clickhouse Merge Tree Table**
![Image](/Docs/Clickhouse_Incoming_Table.jpg)

# Screenshots for Batch Pipeline 
**Airbyte Custom Stream of Grouped Daily Endpoint**
![Image](/Docs/EC2_Airbyte_Grouped_Daily.jpg)
**Airbyte Custom Stream of Tickers Endpoint**
![Image](/Docs/EC2_Airbyte_Tickers.jpg)

