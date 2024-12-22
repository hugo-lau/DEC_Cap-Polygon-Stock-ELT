# Orchestration
Details below along with visual documentation for orchestrating each pipeline

# Streaming Pipeline
In this streaming data pipeline, data coming into Kafka automatically flows through to Clickhouse and Apache Preset. So we only need to trigger the Polygon WebSocket client (Python producer) runs during market hours to capture real-time data. As such, we do not need Dagster and it is containerized and deployed on ECS, scheduled to start automatically when the market opens and spin down when it closes, optimizing resource usage. ECS provides auto-recovery and restart, ensuring the WebSocket client is resilient to failures. Note: For demo purposes, the websocket client was set to run for 3-5 minutes.

# Batch Pipeline
In this pipeline, Dagster Cloud utilizes a declarative approach for asset materialization to orchestrate the data flow from Polygon Restful API to Snowflake. Dagster defines an asset representing the raw data ingestion, which triggers Airbyte to replicate data from Polygon into Snowflake. Once the data is successfully ingested, Dagster sets up a dependency to trigger the DBT transformation process, which converts the raw data into marts in Snowflake data. 

# Screenshots of Scheduling Streaming Pipeline
**Websocket Client scheduled to run at 3:53 pm est**
![Image](/Docs/ECS_Scheduled_Task.jpg)
**AWS Logs show Producer Websocket Client ran at 3:53 pm est**
![Image](/Docs/CloudWatch_StartofLogs.jpg)
**AWS Logs show Producer Websocket Client end 5 mins later**
![Image](/Docs/CloudWatch_Logsshow_ECS_Task_ended.jpg)
**Polygon Confirms Websocket ran around the same time**
![Image](/Docs/Polygon_Websocket_Called.jpg)	

# Screenshots of Dagster Orchestration of Batch-Processing Pipeline
