# Data Visualisation on Apache Preset
Apache Preset connected to Clickhouse and Snowflake warehouse for Streaming and Batch-processing pipelines respectively.

# Clickhouse Streaming Data
In preset, three charts were created directly off the clickhouse data. One was a line chart showing the live stock price while another chart was a bar chart showing the calculated percentage change over every 10s window. Lastly, there was a table showing the corresponding price, volume stock and timestamp. The dashboard was set to refresh every 10s to 30s, to illustrate the charts updating as streaming data came in.

**Charts and Dashboards**
![Image](/Docs/Preset_Polygon_Live_Stock_Price.jpg)
![Image](/Docs/Live_Stock_Percentage_Change.jpg)
![Image](/Docs/Live_Stock_Table.jpg)
![Image](/Docs/Preset_Live_Dashboard.jpg)

# Snowflake Historical Data
In preset, a few charts were created off the snowflake mart data. These help in visualizing the stock trend over a particular period of time


**Charts and Dashboards**

![Image](/Docs/preset_Polygon_batch_Stock.png)
![Image](/Docs/Preset_Batch_Process_Chart.png)
