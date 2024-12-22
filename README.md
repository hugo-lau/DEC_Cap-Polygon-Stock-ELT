# Streaming & Batch Pipeline with Kafka-Clickhouse and Airbyte-Snowflake-DBT
This project is about building data pipeline that captures real-time and historical financial data from Polygon APIs and transforms it into analytical insights. This cloud-based solution utilizes Kafka & Clickhouse for real-time analytics of Streaming data each second while employing Airbyte, Snowflake and DBT for batch processing and historical data analysis.  

## Project Structure
- `Main`: Overview of the project and architecture 
- `Integration-elt/`: End to End integration of streaming and batch data pipelines. See details here [Integration](/Integration-elt/README.md)
- `Transformation/`: Real-time and historical-transformations. See details here [Transformation](/Transformation/README.md)
- `Orchestration/`: Scheduling and orchestration of stream and batch pipeline. See details here [Orchestration](/Orchestration/README.md)
- `Visualization/`: BI Consumption with dashboards for streaming and batch analytics. See details here [Visualization](/Visualization/README.md) 
- `Docs/`: Diagrams and images capturing visualization of documents

## Solution Architecture
![solution architecture](/Docs/Polygon_Solution_Architecture.jpg)
There are two pipeline solutions:

### 1. Streaming Pipeline
This completely cloud-hosted solution provides real-time analysis and visualization as stock data as it arrives every second.
- **Polygon Websocket API**: Stream Stock Data (delayed up to 15 min) every second
- **Python,Docker**: Python producer containerized with docker, running on AWS ECS, captures streaming data
- **Confluent Cloud, Kafka**: Kafka handles and processes streaming data, sending it to Clickhouse
- **Clickhouse Cloud**: Fast open-source columnar database optimized for real-time analytics
- **Apache Preset**: Business Intelligence (BI) tools for consuming and visualizing real-time stock data
- **AWS ECS**: Schedules docker container to run when market opens and stops when market closes
- **CI/CD with Github Action**: Ensures lint check and automatic deployment of python docker container to AWS ECR, when triggered by code changes

### 2. Batch Pipeline
This completely cloud-hosted solution provides historical data analysis of multiple stocks
- **Polygon Restful API**: Fetches data from different endpoints including reference data
- **Airbyte Cloud**: Custom Airbyte connector are used to handle incremental data extraction and support different data streams
- **Snowflake**: A cloud-based OLAP data warehouse that stores and processes rata data through staging and marts
- **DBT**: Handles data transformation and model for Polygon data in Snowflake
- **Apache Preset**: BI consumes and visualize transformed batch data
- **Dagster Cloud**: Orchestrate the Airbyte-snowflake ingestion and snowflake-DBT transformation
- **CI/CD with Github Action**: automates deployment to Dagster Cloud when pull requests are made to the Orchestration directory

# CI/CD - Github Actions
GitHub Actions is used to trigger the CI/CD pipeline, for which the status and logs of these workflows can be checked in the GitHub Actions of this repository. The following workflows are set up:
- Linter workflow: Flags improperly formatted SQL and Python code to ensure code quality and consistency
- Deploy_WebsocketContainer workflow is triggered automatically when changes are pushed to the `main` branch in the `Integration-elt/polygon-websocket/**` directory. This workflow builds a Docker container for the Polygon WebSocket client and pushes it to Amazon ECR. The workflow uses GitHub's OpenID Connect (OIDC) token, eliminating the need for AWS credentials
- Serverless Branch Deployments workflow automates deployment to Dagster Cloud when changes are made to the `Orchestration/**` directory via a pull request. The workflow has two jobs: deploying a Docker container or a Python executable, depending on the conditions. It builds and deploys the deployment process to Dagster Cloud.

## Comments, Notes and Future Improvements
- Further analysis such as Candlestick Charts: Add additional analytics such as candlestick charts (OHLC) which would require customization as they are not natively supported in Apache Preset. 
- Cost Consideration: To balance scalability and cost, the solution is scaled down to run for only a few minutes and subscribe to a select set of stocks. In production, it could scale to capture full market data over the entire 8-hour trading day
- API Data Restrictions: Despite the paid subscription, some data endpoints were not available and only open to more premium subscriptions
