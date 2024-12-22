# Transformation
Details below along with visual documentation for transformation of each pipeline

# Streaming Pipeline
There are two transformations that take place, one Kafka via KSQLDB and the other in Clickhouse Materialized view.

**KSQLDB in Kafka**
This KsqlDB Transformation is designed to:
1.	Removes unnecessary data fields from the stream, reducing storage space on Clickhouse.
2.	Adds a human-readable timestamp in the format `yyyy-MM-dd’T’HH:mm:ss.SSS’Z’` format suitable for Clickhouse and Apache Preset

Data from the topic `polygon_stream_aggregates` is ingested into the KSQLDB stream `POLYGON_STREAM_AGGREGATES_STREAM` where a persistent query `CSAS_FILTERED_STOCK_DATA_19` is applied to modify into a new stream `FILTERED_STOCK_DATA` then persisted to `custom_filtered_stock_data_topic` available for consumers.

**Clickhouse**
Clickhouse creates a materialized view in ClickHouse that processes real-time stock price data from Kafka. It calculates the price difference (`delta_price_10s`) and percentage change (`percentage_change_10s`) over the last 10 seconds for each stock symbol using a sliding window function(`anyLast`), which partitions the data by stock symbol and orders it by the readable timestamp. The view is updated automatically as new data streams in, providing near-real-time insights into stock price changes. The SQL Code is as follows:
```sql
CREATE MATERIALIZED VIEW stock_delta_changes
ENGINE = MergeTree()
ORDER BY (SYMBOL, READABLE_TIMESTAMP)
AS
SELECT 
    SYMBOL,
    CLOSE_PRICE,
    anyLast(CLOSE_PRICE) OVER w as price_10s_ago,
    CLOSE_PRICE - anyLast(CLOSE_PRICE) OVER w AS delta_price_10s,
    round(((CLOSE_PRICE - anyLast(CLOSE_PRICE) OVER w) / 
           nullIf(anyLast(CLOSE_PRICE) OVER w, 0)) * 100, 2) AS percentage_change_10s,
    READABLE_TIMESTAMP
FROM custom_filtered_stock_data_topic
WINDOW w AS (
    PARTITION BY SYMBOL 
    ORDER BY READABLE_TIMESTAMP
    ROWS BETWEEN 10 PRECEDING AND 1 PRECEDING
);
```

# Batch Pipeline
With the rest API endpoints available under the current subscription, we took 6 tables (‘daily_open_close’, ‘exchanges’, ‘grouped_daily’, ‘stock_split’, ‘ticker_types’, ‘tickers’) and transformed it into (‘dim_exchanges’, ‘dim_ticker_split’, ‘fact_tickers’, ‘report_tickers’) using dbt to take it through staging and marts.
‘dim_ticker_split’ was an inner_join between ‘stock_split’ and ‘ticker_types’ while ‘dim_ticker_exchange’ was an inner join of ‘tickers’ and ‘exchanges’, while report tickers is consolidation of all the available data fields.

# Screenshots of Transforming Stream Pipeline
**KSQLDB Streaming Persistent Query**
![Image](/Docs/ConfluentCloud_KSQLDB_Persistent_Query.jpg)

# Screenshots of Transforming Batch Pipeline 
